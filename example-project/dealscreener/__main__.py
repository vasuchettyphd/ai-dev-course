"""Ask for one listing's numbers, then print its results and the buy-box check.

Run it from the example-project folder with:  python3 -m dealscreener
"""
from __future__ import annotations

import math

from dealscreener.buybox import check, money, passes
from dealscreener.calculator import Listing, analyse

TOO_BIG = 1e12  # a trillion: far beyond any real listing, small enough to work out

# Each question: (Listing field, prompt, kind of answer). Every kind takes a number
# from 0 up to TOO_BIG. "price" must also be more than 0, "percent" at most 100,
# "years" a whole number, 1 or more. "dollars" has no extra rule.
PROPERTY_QUESTIONS = [
    ("purchase_price", "Purchase price ($): ", "price"),
    ("monthly_rent", "Monthly rent ($): ", "dollars"),
    ("yearly_property_tax", "Yearly property tax ($): ", "dollars"),
    ("yearly_insurance", "Yearly insurance ($): ", "dollars"),
    ("monthly_hoa", "Monthly HOA fee ($, 0 if none): ", "dollars"),
]
LOAN_QUESTIONS = [
    ("down_payment_pct", "Down payment (%): ", "percent"),
    ("interest_rate_pct", "Interest rate (%): ", "percent"),
    ("loan_term_years", "Loan term (years): ", "years"),
    ("closing_costs", "Closing costs ($): ", "dollars"),
]


def run(input_fn=input, print_fn=print) -> int:
    """Run the screener once. Returns 0 when done, or 1 if the input stopped early."""
    print_fn("Rental deal screener. Type each number and press Enter.")
    try:
        answers = ask_all(PROPERTY_QUESTIONS + LOAN_QUESTIONS, input_fn, print_fn)
        while True:
            try:
                results = analyse(Listing(**answers))
                break
            except ValueError as problem:
                # For example: 0% down and $0 closing costs means no cash invested.
                print_fn(f"{problem} Please type the loan details again.")
                answers.update(ask_all(LOAN_QUESTIONS, input_fn, print_fn))
    except (EOFError, KeyboardInterrupt):
        # Ctrl+D, Ctrl+C, or piped input ran out: stop politely, no traceback.
        print_fn("")
        print_fn("Stopped before all the numbers were typed.")
        return 1

    print_fn("")
    print_fn(f"Monthly mortgage payment: {money(results.monthly_mortgage)}")
    print_fn(f"Monthly cash flow: {money(results.monthly_cash_flow)}")
    print_fn(f"Cap rate: {results.cap_rate_pct:.2f}%")
    print_fn(f"Cash-on-cash return: {results.cash_on_cash_pct:.2f}%")
    print_fn("")
    rule_results = check(results)
    for rule in rule_results:
        print_fn(f"{'PASS' if rule.passed else 'FAIL'}  {rule.reason}")
    print_fn("")
    print_fn(f"Overall: {'PASS' if passes(rule_results) else 'FAIL'}")
    return 0


def ask_all(questions, input_fn, print_fn) -> dict:
    """Ask each question in order. Returns {field: answer}."""
    return {field: ask(prompt, kind, input_fn, print_fn) for field, prompt, kind in questions}


def ask(prompt, kind, input_fn, print_fn):
    """Ask one question until the answer makes sense."""
    while True:
        try:
            return parse_answer(input_fn(prompt), kind)
        except ValueError as problem:
            print_fn(str(problem))


def parse_answer(text: str, kind: str):
    """Turn typed text into a number, or raise ValueError saying what to type instead."""
    cleaned = text.strip().replace("$", "").replace(",", "").replace("%", "")
    try:
        value = float(cleaned)
    except ValueError:
        value = math.nan
    if not math.isfinite(value):
        raise ValueError("Please type a number, like 1500.")
    if value < 0:
        raise ValueError("Please type a number that is 0 or more.")
    if value > TOO_BIG:
        raise ValueError("Please type a smaller number.")
    if kind == "price" and value == 0:
        raise ValueError("The purchase price must be more than 0.")
    if kind == "percent" and value > 100:
        raise ValueError("Please type a percentage from 0 to 100.")
    if kind == "years":
        if value < 1 or not value.is_integer():
            raise ValueError("Please type a whole number of years, 1 or more.")
        return int(value)
    return value


if __name__ == "__main__":
    raise SystemExit(run())
