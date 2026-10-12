"""Ask for one listing's numbers, then print its results and the buy-box check.

Run it from the example-project folder with:  python3 -m dealscreener
To paste a listing first and let a model read its numbers:  python3 -m dealscreener --listing
"""
from __future__ import annotations

import math
import sys

from dealscreener import extract
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


def run(input_fn=input, print_fn=print, use_listing=False, client_factory=None) -> int:
    """Run the screener once. Returns 0 when done, or 1 if the input stopped early.

    With use_listing=True it first offers to read a pasted listing with a model; the
    numbers it finds are shown at each question for you to accept or replace.
    """
    print_fn("Rental deal screener. Type each number and press Enter.")
    try:
        from_listing = {}
        if use_listing:
            from_listing = listing_step(input_fn, print_fn, client_factory or extract.make_client)
        answers = {
            field: ask_with_default(prompt, kind, from_listing.get(field), input_fn, print_fn)
            for field, prompt, kind in PROPERTY_QUESTIONS
        }
        answers.update(ask_all(LOAN_QUESTIONS, input_fn, print_fn))
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


def listing_step(input_fn, print_fn, client_factory) -> dict:
    """Read a pasted listing and ask the model for its numbers. Returns {field: number or None}.

    Returns {} when the step is skipped or fails: then every question is asked as usual.
    """
    print_fn(
        "Paste the listing text, then type done on a line by itself and press Enter. "
        "To skip and type the numbers yourself, type done now."
    )
    lines = []
    while True:
        line = input_fn("")
        if line.strip().lower() == "done":
            break
        lines.append(line)  # blank lines are kept: they separate the listing's paragraphs
    text = "\n".join(lines).strip()
    if not text:
        return {}
    if len(text) > extract.MAX_LISTING_CHARS:
        print_fn("That listing is too long (over 20,000 characters). Type the numbers yourself.")
        return {}
    print_fn("Asking the model to read the listing...")
    try:
        result = extract.extract_listing(text, client_factory())
    except extract.ExtractionError as problem:
        print_fn(f"{problem} For now, type the numbers yourself.")
        return {}
    except Exception as error:  # any failed call: a plain sentence, never a traceback or the key
        print_fn(f"{extract.describe_error(error)} For now, type the numbers yourself.")
        return {}
    cost = extract.cost_usd(result.input_tokens, result.output_tokens)
    print_fn(f"Used {result.input_tokens} input and {result.output_tokens} output tokens, about ${cost:.4f}.")
    print_fn("Check each number from the listing: press Enter to keep it, or type the right number.")
    return result.values


def ask_with_default(prompt, kind, default, input_fn, print_fn):
    """Ask one question, offering a number from the listing that Enter accepts.

    With no number from the listing (default is None), it is the usual question.
    """
    if default is None:
        return ask(prompt, kind, input_fn, print_fn)
    # "Purchase price ($): " becomes "Purchase price ($) [from the listing: 150000]: ".
    # .12g shows 1250000 as 1250000 rather than 1.25e+06.
    offer = f"{prompt.rstrip().rstrip(':')} [from the listing: {default:.12g}]: "
    while True:
        typed = input_fn(offer)
        if not typed.strip():
            try:
                return parse_answer(repr(default), kind)  # the listing's number gets the same checks
            except ValueError as problem:
                print_fn(str(problem))
                return ask(prompt, kind, input_fn, print_fn)
        try:
            return parse_answer(typed, kind)
        except ValueError as problem:
            print_fn(str(problem))


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
    use_listing = "--listing" in sys.argv[1:]
    if use_listing:
        extract.load_env_file()  # the API key, from a .env file in this folder, if there is one
    raise SystemExit(run(use_listing=use_listing))
