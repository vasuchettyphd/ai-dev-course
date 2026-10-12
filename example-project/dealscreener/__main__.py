"""Ask for one listing's numbers, then print its results and the buy-box check.

Run it from the example-project folder with:  python3 -m dealscreener
"""
from __future__ import annotations

import math

from dealscreener.buybox import check, money, passes, percent
from dealscreener.calculator import Listing, analyse

TOO_BIG = 1e12  # a trillion: far beyond any real listing, small enough to work out

# Each question: (Listing field, prompt, kind of answer). Every kind takes a number
# from 0 up to TOO_BIG. "price" must also be more than 0, "percent" at most 100,
# "years" a whole number, 1 or more. "dollars" has no extra rule. A "percent" between
# 0 and 1, like 0.07, gets one follow-up question: did you mean 7%?
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
    print_fn(f"Cap rate: {percent(results.cap_rate_pct)}")
    print_fn(f"Cash-on-cash return: {percent(results.cash_on_cash_pct)}")
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
            value = parse_answer(input_fn(prompt), kind)
        except ValueError as problem:
            print_fn(str(problem))
            continue
        if kind == "percent" and 0 < value < 1:
            # 0.07 might mean 7% typed as a decimal: ask rather than guess.
            return confirm_small_percent(value, input_fn, print_fn)
        return value


def confirm_small_percent(value, input_fn, print_fn) -> float:
    """Ask whether a percentage between 0 and 1, like 0.07, meant 7%. Returns the one chosen."""
    as_percent = round(value * 100, 10)  # round away floating-point noise, like 7.000000000000001
    question = (
        f"You typed {value:g}. Did you mean {as_percent:g}%? "
        f"Type y for {as_percent:g}%, or n to keep {value:g}%: "
    )
    while True:
        reply = input_fn(question).strip().lower()
        if reply in ("y", "yes"):
            return as_percent
        if reply in ("n", "no"):
            return value


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
