"""The screen_listing tool (week 11): the deal screener's calculator, ready for a model to call.

A model never works the numbers out itself: it asks this tool, and the tool answers with
the same numbers the program prints. Every input is checked first, with the same rules
as the questions the program asks, and a problem comes back as one plain sentence naming
the field, so the model can fix it or ask the user. The tool only calculates: it reads
no files, writes nothing and sends nothing.

This file uses only Python's standard library. The agent (agent.py) and the MCP server
(mcp_server.py) both use it.
"""
from __future__ import annotations

import math

from dealscreener.__main__ import parse_answer
from dealscreener.buybox import check, passes
from dealscreener.calculator import Assumptions, Listing, analyse

TOOL_NAME = "screen_listing"

# The nine Listing fields, in order, with the kind of answer each one is (the kinds of
# dealscreener/__main__.py: price, dollars, percent, years) and its description.
FIELD_INFO = [
    ("purchase_price", "price", "The asking price in dollars. Must be more than 0."),
    ("monthly_rent", "dollars", "The rent in dollars per month."),
    ("yearly_property_tax", "dollars", "Property tax in dollars per year."),
    ("yearly_insurance", "dollars", "Insurance in dollars per year."),
    ("monthly_hoa", "dollars", "The HOA fee in dollars per month. 0 if there is no HOA."),
    ("down_payment_pct", "percent", "The down payment as a percentage of the price, written as 25 for 25%."),
    ("interest_rate_pct", "percent", "The loan's yearly interest rate, written as 7 for 7%."),
    ("loan_term_years", "years", "The length of the loan in whole years, for example 30."),
    ("closing_costs", "dollars", "The closing costs in dollars, paid once when buying."),
]
FIELDS = [field for field, _, _ in FIELD_INFO]
KINDS = {field: kind for field, kind, _ in FIELD_INFO}

TOOL_SCHEMA = {
    "name": TOOL_NAME,
    "description": (
        "Screens one rental property listing with the investor's own deal calculator. "
        "Give it the nine numbers of one listing: plain numbers with no $ signs or commas, "
        "and percentages are written as 25 for 25%. "
        "It returns the monthly mortgage payment, the monthly cash flow, the cap rate and the "
        "cash-on-cash return, then checks the investor's buy box rules and says PASS or FAIL. "
        f"It already sets aside {Assumptions().vacancy_pct:g}% of the rent for empty months (vacancy) "
        f"and {Assumptions().repairs_reserve_pct:g}% of the rent for repairs. "
        "Use it for every number you report about a listing. Do not call it with a guessed "
        "number: if the user didn't give one of the nine numbers, ask them for it instead. "
        "If a number is wrong, it returns an error sentence naming the field."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            field: {"type": "integer" if kind == "years" else "number", "description": description}
            for field, kind, description in FIELD_INFO
        },
        "required": list(FIELDS),
        "additionalProperties": False,
    },
}


class ToolInputError(Exception):
    """The tool's input was wrong. The message is one plain sentence naming the field,
    which goes back to the model as the tool's error."""


def check_input(raw: dict) -> Listing:
    """Check the tool's input and turn it into a Listing, or raise ToolInputError."""
    if not isinstance(raw, dict):
        raise ToolInputError("The input must be an object with the nine numbers.")
    for name in raw:
        if name not in KINDS:
            raise ToolInputError(f"Unknown field: {name}.")
    values = {}
    for field in FIELDS:
        if field not in raw:
            raise ToolInputError(f"Missing field: {field}.")
        values[field] = check_number(field, raw[field])
    return Listing(**values)


def check_number(field: str, value):
    """One number, checked with the same rules as the program's questions."""
    # bool counts as a number in Python (True is 1), so it is turned away first.
    if isinstance(value, bool):
        raise ToolInputError(f"{field} must be a number, not true or false.")
    if isinstance(value, str):
        raise ToolInputError(f"{field} must be a number, not text.")
    if not isinstance(value, (int, float)):
        raise ToolInputError(f"{field} must be a number.")
    try:
        number = float(value)  # a huge whole number, like 10**400, can't become a float
    except OverflowError:
        raise ToolInputError(f"{field} is too large.") from None
    if not math.isfinite(number):
        raise ToolInputError(f"{field} must be a finite number.")
    kind = KINDS[field]
    try:
        checked = parse_answer(str(value), kind)  # the program's own rules for this kind
    except ValueError as problem:
        # The program's sentences talk to a person typing ("Please type a smaller number.");
        # the tool's sentences talk about the value ("it must be a smaller number.").
        message = str(problem).replace("Please type ", "it must be ")
        raise ToolInputError(f"{field} is {number:g}: {message[0].lower()}{message[1:]}") from None
    if kind == "percent" and 0 < checked < 1:
        # 0.07 might mean 7% written as a decimal: the tool refuses, and the model asks.
        as_percent = round(checked * 100, 10)  # round away floating-point noise
        raise ToolInputError(
            f"{field} is {checked:g}: percentages are written as {as_percent:g} for {as_percent:g}%. "
            "Ask the user which they meant."
        )
    return checked


def screen_listing(raw: dict) -> dict:
    """Run the calculator and the buy box on one listing. Numbers are rounded to cents."""
    listing = check_input(raw)
    try:
        results = analyse(listing)
    except ValueError as problem:  # for example: no cash invested
        raise ToolInputError(str(problem)) from None
    rule_results = check(results)
    return {
        "monthly_mortgage": round(results.monthly_mortgage, 2),
        "monthly_cash_flow": round(results.monthly_cash_flow, 2),
        "cap_rate_pct": round(results.cap_rate_pct, 2),
        "cash_on_cash_pct": round(results.cash_on_cash_pct, 2),
        "rules": [{"passed": rule.passed, "reason": rule.reason} for rule in rule_results],
        "overall": "PASS" if passes(rule_results) else "FAIL",
    }
