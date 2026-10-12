# Deal Screener First Three Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the deal screener's first three steps from `PLAN.md`: a calculator for one listing, the buy-box check, and a program that asks for a listing's numbers and prints the results.

**Architecture:** Three small Python files in a `dealscreener` package, one per build step. `calculator.py` does the math and knows nothing about rules or typing. `buybox.py` takes the calculator's results and checks them against the rules. `__main__.py` asks the questions, calls the other two and prints the report. Each file is built test first.

**Tech Stack:** Python 3.9 or newer, standard library only. Tests use `unittest` and run with `python3 -m unittest`.

**Spec:** `PLAN.md` (sections "Must-haves" and "First three build steps").

All paths and commands below are relative to the `example-project/` folder.

## Global Constraints

- Python 3.9 or newer, because the Python that comes with a Mac's Command Line Tools may be as old as 3.9. The code files in `dealscreener/` start with `from __future__ import annotations`, so their type hints work on 3.9. No `match` statements and no `X | Y` types.
- Standard library only. Nothing to install.
- Tests run with `python3 -m unittest` from the `example-project/` folder.
- Percentages are written as 25 for 25%, everywhere.
- Assumptions: vacancy 5% of monthly rent, repairs reserve 8% of monthly rent before vacancy. (`PLAN.md` left the repairs reserve open; 8% is decided here, and Task 1 updates `PLAN.md`.)
- Buy box: cash-on-cash return at least 10%, monthly cash flow at least $100. "At least" means a value equal to the rule passes.
- Money in tests is checked to the cent (`delta=0.01`), percentages to a thousandth of a point (`delta=0.001`).
- The program never shows a Python error (a "traceback") for anything a person types.

## Review Focus

1. **Letters, a blank line, or "nan" typed instead of a number.** The program says "Please type a number, like 1500." and asks the same question again. (Task 3: `test_bad_price_is_asked_again_without_a_traceback`, `test_blank_and_not_a_number_answers_are_asked_again`.)
2. **0% down and $0 closing costs, so no cash is invested.** Cash-on-cash return would divide by zero. The calculator raises a plain-English error, and the program prints it and asks the loan questions again. (Task 1: `test_zero_cash_invested_raises`; Task 3: `test_zero_cash_invested_explains_and_asks_again_from_the_down_payment`.)
3. **A 0% or tiny interest rate.** The usual loan formula divides by zero. At 0% the payment is the loan split evenly over the months, and a tiny rate gives almost the same. (Task 1: `test_zero_interest_splits_the_loan_evenly`, `test_tiny_interest_rate_does_not_divide_by_zero`.)
4. **A percentage over 100, a price of 0, a loan term of 0 or 2.5 years, or a huge number like 1e308.** The program says what to type and asks again, and never prints "nan" or "inf". (Task 1: `test_numbers_too_large_to_work_out_raise`; Task 3: `test_percentage_over_100_is_asked_again`, `test_zero_price_is_asked_again`, `test_loan_term_must_be_whole_years`, `test_huge_numbers_are_asked_again`.)
5. **The input stops early** (Ctrl+D, Ctrl+C, or piped input runs out). The program says it stopped, with no traceback. (Task 3: `test_running_out_of_input_stops_without_a_traceback`.)

## Files

| File | What it does |
|---|---|
| `dealscreener/__init__.py` | Marks `dealscreener` as a Python package. |
| `dealscreener/calculator.py` | `Listing`, `Assumptions`, `Results`, `monthly_mortgage_payment()`, `analyse()`. |
| `dealscreener/buybox.py` | `BuyBox`, `RuleResult`, `check()`, `passes()`, `money()`. |
| `dealscreener/__main__.py` | `run()`: the program you start with `python3 -m dealscreener`. |
| `tests/__init__.py` | Lets `python3 -m unittest` find the tests. |
| `tests/test_calculator.py`, `tests/test_buybox.py`, `tests/test_main.py` | One test file per code file. |

## Hand-worked listings

Both listings use vacancy 5% and repairs 8%. The answers were worked out by hand first, then confirmed with a one-line Python check.

| Field | Listing A | Listing B |
|---|---|---|
| Price | 200000 | 150000 |
| Rent | 1800 | 1700 |
| Tax (yearly) | 2400 | 2400 |
| Insurance (yearly) | 1200 | 1200 |
| HOA (monthly) | 0 | 0 |
| Down payment | 25% | 25% |
| Interest rate | 7% | 7% |
| Loan term | 30 years | 30 years |
| Closing costs | 6000 | 6000 |
| **Mortgage** | **997.95** | **748.47** |
| **Cash flow** | **268.05** | **430.53** |
| **Cap rate** | **7.596%** | **9.432%** |
| **Cash-on-cash** | **5.744%** | **11.877%** |
| **Buy box** | **FAIL** on cash-on-cash; cash flow passes | **PASS** |

The working for listing A:

- Down payment = 200000 x 25% = 50000. Loan = 200000 - 50000 = 150000.
- Mortgage = 150000 x r / (1 - (1 + r)^-360), with r = 7% / 12 = 0.0058333, so 997.95 a month.
- Effective rent = 1800 x (1 - 5%) = 1710. Repairs reserve = 1800 x 8% = 144.
- Operating costs = (2400 + 1200) / 12 + 0 + 144 = 300 + 144 = 444.
- Cash flow = 1710 - 444 - 997.95 = 268.05.
- Cap rate = (1710 - 444) x 12 / 200000 = 15192 / 200000 = 7.596%.
- Cash invested = 50000 + 6000 = 56000. Cash-on-cash = 268.05 x 12 / 56000 = 3216.60 / 56000 = 5.744%.

The working for listing B:

- Down payment = 150000 x 25% = 37500. Loan = 112500. Mortgage = 748.47 a month.
- Effective rent = 1700 x 95% = 1615. Repairs reserve = 1700 x 8% = 136. Operating costs = 300 + 136 = 436.
- Cash flow = 1615 - 436 - 748.47 = 430.53.
- Cap rate = (1615 - 436) x 12 / 150000 = 14148 / 150000 = 9.432%.
- Cash invested = 37500 + 6000 = 43500. Cash-on-cash = 430.53 x 12 / 43500 = 5166.36 / 43500 = 11.877%.

The one-line check (type it in the Terminal or the Ubuntu window):

```bash
python3 -c "r=0.07/12; print(150000*r/(1-(1+r)**-360), 112500*r/(1-(1+r)**-360))"
```

Expected: about `997.9537 748.4653`.

---

### Task 1: The calculator for one listing

**Files:**
- Create: `dealscreener/__init__.py`
- Create: `dealscreener/calculator.py`
- Create: `tests/__init__.py` (empty)
- Test: `tests/test_calculator.py`
- Modify: `PLAN.md` (the repairs reserve is 8%)

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `Listing` (frozen dataclass). All fields are floats except `loan_term_years: int`. Fields, in order: `purchase_price`, `monthly_rent`, `yearly_property_tax`, `yearly_insurance`, `monthly_hoa`, `down_payment_pct`, `interest_rate_pct`, `loan_term_years`, `closing_costs`.
  - `Assumptions(vacancy_pct=5.0, repairs_reserve_pct=8.0)`.
  - `Results(monthly_mortgage, monthly_cash_flow, cap_rate_pct, cash_on_cash_pct)`.
  - `monthly_mortgage_payment(principal, annual_rate_pct, years) -> float`.
  - `analyse(listing, assumptions=Assumptions()) -> Results`. Raises `ValueError` with a plain-English message for a purchase price of 0 or less, a negative amount, a percentage outside 0-100, a loan term below 1, zero cash invested (the message contains "cash invested"), or results too large to work out (the message contains "too large").

- [ ] **Step 1: Write the failing test**

Create an empty `tests/__init__.py`, then `tests/test_calculator.py`:

```python
"""Tests for the calculator. The expected numbers were worked out by hand first."""
import unittest

from dealscreener.calculator import (
    Assumptions,
    Listing,
    analyse,
    monthly_mortgage_payment,
)


def make_listing(**changes):
    """Listing A from the plan, with any fields changed that a test asks for."""
    fields = dict(
        purchase_price=200000,
        monthly_rent=1800,
        yearly_property_tax=2400,
        yearly_insurance=1200,
        monthly_hoa=0,
        down_payment_pct=25,
        interest_rate_pct=7,
        loan_term_years=30,
        closing_costs=6000,
    )
    fields.update(changes)
    return Listing(**fields)


ASSUMPTIONS = Assumptions(vacancy_pct=5, repairs_reserve_pct=8)


class ListingATest(unittest.TestCase):
    def test_listing_a_matches_the_hand_worked_numbers(self):
        results = analyse(make_listing(), ASSUMPTIONS)
        self.assertAlmostEqual(results.monthly_mortgage, 997.95, delta=0.01)
        self.assertAlmostEqual(results.monthly_cash_flow, 268.05, delta=0.01)
        self.assertAlmostEqual(results.cap_rate_pct, 7.596, delta=0.001)
        self.assertAlmostEqual(results.cash_on_cash_pct, 5.744, delta=0.001)


class ListingBTest(unittest.TestCase):
    def test_listing_b_matches_the_hand_worked_numbers(self):
        results = analyse(make_listing(purchase_price=150000, monthly_rent=1700), ASSUMPTIONS)
        self.assertAlmostEqual(results.monthly_mortgage, 748.47, delta=0.01)
        self.assertAlmostEqual(results.monthly_cash_flow, 430.53, delta=0.01)
        self.assertAlmostEqual(results.cap_rate_pct, 9.432, delta=0.001)
        self.assertAlmostEqual(results.cash_on_cash_pct, 11.877, delta=0.001)


class EdgeCaseTest(unittest.TestCase):
    def test_default_assumptions_are_5_percent_vacancy_and_8_percent_repairs(self):
        self.assertEqual(Assumptions(), ASSUMPTIONS)

    def test_zero_interest_splits_the_loan_evenly(self):
        self.assertAlmostEqual(monthly_mortgage_payment(120000, 0, 10), 1000.00, delta=0.01)

    def test_tiny_interest_rate_does_not_divide_by_zero(self):
        self.assertAlmostEqual(monthly_mortgage_payment(120000, 1e-300, 10), 1000.00, delta=0.01)

    def test_zero_down_with_closing_costs_works(self):
        results = analyse(make_listing(down_payment_pct=0, closing_costs=6000), ASSUMPTIONS)
        self.assertLess(results.monthly_cash_flow, 0)

    def test_zero_cash_invested_raises(self):
        with self.assertRaisesRegex(ValueError, "cash invested"):
            analyse(make_listing(down_payment_pct=0, closing_costs=0), ASSUMPTIONS)

    def test_negative_rent_raises(self):
        with self.assertRaises(ValueError):
            analyse(make_listing(monthly_rent=-100), ASSUMPTIONS)

    def test_down_payment_over_100_percent_raises(self):
        with self.assertRaises(ValueError):
            analyse(make_listing(down_payment_pct=120), ASSUMPTIONS)

    def test_purchase_price_of_zero_raises(self):
        with self.assertRaises(ValueError):
            analyse(make_listing(purchase_price=0), ASSUMPTIONS)

    def test_loan_term_below_one_year_raises(self):
        with self.assertRaises(ValueError):
            analyse(make_listing(loan_term_years=0), ASSUMPTIONS)

    def test_numbers_too_large_to_work_out_raise(self):
        with self.assertRaisesRegex(ValueError, "too large"):
            analyse(make_listing(purchase_price=1e308, monthly_rent=1e308), ASSUMPTIONS)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest`
Expected: FAIL with `ModuleNotFoundError: No module named 'dealscreener'`

- [ ] **Step 3: Write the calculator**

`dealscreener/__init__.py`:

```python
"""Rental deal screener: the course's worked example."""
```

`dealscreener/calculator.py`:

```python
"""Work out a rental listing's mortgage, cash flow, cap rate and cash-on-cash return."""
from __future__ import annotations

import math
from dataclasses import astuple, dataclass


@dataclass(frozen=True)
class Listing:
    """One listing's numbers. Percentages are written as 25 for 25%."""

    purchase_price: float
    monthly_rent: float
    yearly_property_tax: float
    yearly_insurance: float
    monthly_hoa: float
    down_payment_pct: float
    interest_rate_pct: float
    loan_term_years: int
    closing_costs: float


@dataclass(frozen=True)
class Assumptions:
    """Settings chosen once, used for every listing."""

    vacancy_pct: float = 5.0
    repairs_reserve_pct: float = 8.0  # % of monthly rent, before vacancy


@dataclass(frozen=True)
class Results:
    monthly_mortgage: float
    monthly_cash_flow: float
    cap_rate_pct: float
    cash_on_cash_pct: float


def monthly_mortgage_payment(principal: float, annual_rate_pct: float, years: float) -> float:
    """The standard fixed-rate loan payment."""
    months = float(years) * 12
    if annual_rate_pct == 0:
        return principal / months  # no interest: split the loan evenly
    monthly_rate = annual_rate_pct / 100 / 12
    # This is 1 - (1 + rate) ** -months, written so a tiny rate can't round it to 0.
    denominator = -math.expm1(-months * math.log1p(monthly_rate))
    return principal * monthly_rate / denominator


def analyse(listing: Listing, assumptions: Assumptions = Assumptions()) -> Results:
    """Check the inputs, then work out the three numbers (and the mortgage)."""
    _check_inputs(listing, assumptions)

    down_payment = listing.purchase_price * listing.down_payment_pct / 100
    cash_invested = down_payment + listing.closing_costs
    if cash_invested == 0:
        raise ValueError(
            "The cash invested (down payment plus closing costs) is $0, "
            "so cash-on-cash return can't be worked out."
        )

    effective_rent = listing.monthly_rent * (1 - assumptions.vacancy_pct / 100)
    repairs_reserve = listing.monthly_rent * assumptions.repairs_reserve_pct / 100
    operating_costs = (
        (listing.yearly_property_tax + listing.yearly_insurance) / 12
        + listing.monthly_hoa
        + repairs_reserve
    )
    mortgage = monthly_mortgage_payment(
        listing.purchase_price - down_payment,
        listing.interest_rate_pct,
        listing.loan_term_years,
    )
    cash_flow = effective_rent - operating_costs - mortgage

    results = Results(
        monthly_mortgage=mortgage,
        monthly_cash_flow=cash_flow,
        cap_rate_pct=(effective_rent - operating_costs) * 12 / listing.purchase_price * 100,
        cash_on_cash_pct=cash_flow * 12 / cash_invested * 100,
    )
    if not all(math.isfinite(number) for number in astuple(results)):
        raise ValueError("These numbers are too large to work out.")
    return results


def _check_inputs(listing: Listing, assumptions: Assumptions) -> None:
    """Raise ValueError with a plain-English message for numbers that make no sense."""
    _check_amount("Purchase price", listing.purchase_price)
    if listing.purchase_price <= 0:
        raise ValueError("Purchase price must be more than $0.")
    _check_amount("Monthly rent", listing.monthly_rent)
    _check_amount("Yearly property tax", listing.yearly_property_tax)
    _check_amount("Yearly insurance", listing.yearly_insurance)
    _check_amount("Monthly HOA fee", listing.monthly_hoa)
    _check_amount("Closing costs", listing.closing_costs)
    _check_percentage("Down payment", listing.down_payment_pct)
    _check_percentage("Interest rate", listing.interest_rate_pct)
    _check_percentage("Vacancy", assumptions.vacancy_pct)
    _check_percentage("Repairs reserve", assumptions.repairs_reserve_pct)
    _check_amount("Loan term", listing.loan_term_years)
    if listing.loan_term_years < 1:
        raise ValueError("Loan term must be at least 1 year.")


def _check_amount(label: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{label} must be a number.")
    if value < 0:
        raise ValueError(f"{label} can't be negative.")


def _check_percentage(label: str, value: float) -> None:
    _check_amount(label, value)
    if value > 100:
        raise ValueError(f"{label} must be between 0% and 100%.")
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest`
Expected: `Ran 12 tests` and `OK`

- [ ] **Step 5: Record the repairs reserve decision in `PLAN.md`**

In "Must-haves", item 2, change "a repairs reserve as a % of monthly rent before vacancy (I pick the number; see open questions)" to "a repairs reserve of 8% of monthly rent before vacancy (decided in week 5, while building)". In "Data it uses", change "the repairs reserve" to "8% repairs reserve". In "Open questions", delete the line "How big should the repairs reserve be: 5%, 8% or 10% of rent?".

- [ ] **Step 6: Commit**

```bash
git add dealscreener/__init__.py dealscreener/calculator.py tests/__init__.py tests/test_calculator.py PLAN.md
git commit -m "Add the calculator, tested against two hand-worked listings"
```

### Task 2: The buy-box check

**Files:**
- Create: `dealscreener/buybox.py`
- Test: `tests/test_buybox.py`

**Interfaces:**
- Consumes: `Results` from `dealscreener.calculator`.
- Produces:
  - `BuyBox(min_cash_on_cash_pct=10.0, min_monthly_cash_flow=100.0)`.
  - `RuleResult(name, value, threshold, passed, reason)`.
  - `check(results, buy_box=BuyBox()) -> list` of two `RuleResult`s, cash-on-cash first. A rule passes when `round(value, 2) >= threshold`: the value is rounded to 2 decimals, the same as the reason shows it, so the reason never contradicts the result.
  - `passes(rule_results) -> bool`: True only if every rule passed.
  - `money(amount) -> str`: `1234.5` becomes `"$1,234.50"`, `-50` becomes `"-$50.00"`.
  - Reason texts look like `"Cash-on-cash return 5.74% is below 10.00% by 4.26 points"`, `"Cash-on-cash return 11.88% is at least 10.00%"`, `"Monthly cash flow $268.05 is at least $100.00"` and `"Monthly cash flow $50.00 is below $100.00 by $50.00"`.

- [ ] **Step 1: Write the failing test**

`tests/test_buybox.py`:

```python
"""Tests for the buy-box check."""
import unittest

from dealscreener.buybox import BuyBox, check, passes
from dealscreener.calculator import Results


def make_results(cash_on_cash_pct, monthly_cash_flow):
    return Results(
        monthly_mortgage=0,
        monthly_cash_flow=monthly_cash_flow,
        cap_rate_pct=0,
        cash_on_cash_pct=cash_on_cash_pct,
    )


# The hand-worked numbers for listings A and B.
LISTING_A = make_results(cash_on_cash_pct=5.744, monthly_cash_flow=268.05)
LISTING_B = make_results(cash_on_cash_pct=11.877, monthly_cash_flow=430.53)


class BuyBoxTest(unittest.TestCase):
    def test_default_rules(self):
        self.assertEqual(BuyBox(), BuyBox(min_cash_on_cash_pct=10.0, min_monthly_cash_flow=100.0))

    def test_listing_a_fails_on_cash_on_cash_only(self):
        cash_on_cash, cash_flow = check(LISTING_A)
        self.assertFalse(cash_on_cash.passed)
        self.assertEqual(
            cash_on_cash.reason, "Cash-on-cash return 5.74% is below 10.00% by 4.26 points"
        )
        self.assertTrue(cash_flow.passed)
        self.assertEqual(cash_flow.reason, "Monthly cash flow $268.05 is at least $100.00")
        self.assertFalse(passes([cash_on_cash, cash_flow]))

    def test_listing_b_passes(self):
        rule_results = check(LISTING_B)
        self.assertEqual(
            rule_results[0].reason, "Cash-on-cash return 11.88% is at least 10.00%"
        )
        self.assertTrue(passes(rule_results))

    def test_exactly_10_percent_passes(self):
        cash_on_cash, _ = check(make_results(cash_on_cash_pct=10.0, monthly_cash_flow=500))
        self.assertTrue(cash_on_cash.passed)

    def test_exactly_100_dollars_passes(self):
        _, cash_flow = check(make_results(cash_on_cash_pct=20, monthly_cash_flow=100.00))
        self.assertTrue(cash_flow.passed)

    def test_cash_flow_of_50_fails_with_its_reason(self):
        _, cash_flow = check(make_results(cash_on_cash_pct=20, monthly_cash_flow=50))
        self.assertFalse(cash_flow.passed)
        self.assertEqual(cash_flow.reason, "Monthly cash flow $50.00 is below $100.00 by $50.00")

    def test_just_under_10_percent_that_shows_as_10_00_passes(self):
        cash_on_cash, _ = check(make_results(cash_on_cash_pct=9.996, monthly_cash_flow=500))
        self.assertTrue(cash_on_cash.passed)
        self.assertEqual(cash_on_cash.reason, "Cash-on-cash return 10.00% is at least 10.00%")

    def test_just_under_10_percent_that_shows_as_9_99_fails(self):
        cash_on_cash, _ = check(make_results(cash_on_cash_pct=9.994, monthly_cash_flow=500))
        self.assertFalse(cash_on_cash.passed)
        self.assertEqual(
            cash_on_cash.reason, "Cash-on-cash return 9.99% is below 10.00% by 0.01 points"
        )

    def test_negative_cash_flow_fails(self):
        _, cash_flow = check(make_results(cash_on_cash_pct=20, monthly_cash_flow=-50))
        self.assertFalse(cash_flow.passed)
        self.assertEqual(
            cash_flow.reason, "Monthly cash flow -$50.00 is below $100.00 by $150.00"
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest`
Expected: FAIL with `ModuleNotFoundError: No module named 'dealscreener.buybox'`

- [ ] **Step 3: Write the buy-box check**

`dealscreener/buybox.py`:

```python
"""Check a listing's results against my buy box: the rules a deal must pass."""
from __future__ import annotations

from dataclasses import dataclass

from dealscreener.calculator import Results


@dataclass(frozen=True)
class BuyBox:
    min_cash_on_cash_pct: float = 10.0
    min_monthly_cash_flow: float = 100.0


@dataclass(frozen=True)
class RuleResult:
    name: str
    value: float
    threshold: float
    passed: bool
    reason: str


def check(results: Results, buy_box: BuyBox = BuyBox()) -> list:
    """Check each rule, cash-on-cash first. Returns a list of RuleResult."""
    return [
        _check_cash_on_cash(results.cash_on_cash_pct, buy_box.min_cash_on_cash_pct),
        _check_cash_flow(results.monthly_cash_flow, buy_box.min_monthly_cash_flow),
    ]


def passes(rule_results: list) -> bool:
    """A deal passes only if every rule passes."""
    return all(rule.passed for rule in rule_results)


def money(amount: float) -> str:
    """Format dollars, for example 1234.5 -> '$1,234.50' and -50 -> '-$50.00'."""
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):,.2f}"


# Both rules compare the value rounded to 2 decimals, the same as the reason
# shows it, so the reason never contradicts pass or fail (9.996% shows as
# 10.00% and passes).


def _check_cash_on_cash(value: float, threshold: float) -> RuleResult:
    name = "Cash-on-cash return"
    shown = round(value, 2)
    passed = shown >= threshold
    if passed:
        reason = f"{name} {shown:.2f}% is at least {threshold:.2f}%"
    else:
        reason = f"{name} {shown:.2f}% is below {threshold:.2f}% by {threshold - shown:.2f} points"
    return RuleResult(name, value, threshold, passed, reason)


def _check_cash_flow(value: float, threshold: float) -> RuleResult:
    name = "Monthly cash flow"
    shown = round(value, 2)
    passed = shown >= threshold
    if passed:
        reason = f"{name} {money(shown)} is at least {money(threshold)}"
    else:
        reason = f"{name} {money(shown)} is below {money(threshold)} by {money(threshold - shown)}"
    return RuleResult(name, value, threshold, passed, reason)
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest`
Expected: `Ran 21 tests` and `OK`

- [ ] **Step 5: Commit**

```bash
git add dealscreener/buybox.py tests/test_buybox.py
git commit -m "Add the buy-box check with a reason for each rule"
```

### Task 3: A simple way to run it

**Files:**
- Create: `dealscreener/__main__.py`
- Test: `tests/test_main.py`
- Modify: `README.md` (how to run the tests and the program)

**Interfaces:**
- Consumes: `Listing`, `analyse` from `dealscreener.calculator`; `check`, `passes`, `money` from `dealscreener.buybox`.
- Produces: `run(input_fn=input, print_fn=print) -> int`. It asks for each `Listing` field in order, re-asks with a short message when an answer makes no sense (not a number, below 0, over 100 for a percentage, over a trillion, and so on), prints the numbers, each rule's PASS or FAIL with its reason, and a last line `Overall: PASS` or `Overall: FAIL`. It returns 0, or 1 if the input stopped early. `python3 -m dealscreener` calls it. Passing in `input_fn` and `print_fn` lets the tests type answers and read the output without a keyboard.

- [ ] **Step 1: Write the failing test**

`tests/test_main.py`:

```python
"""Tests for the program you run: typed answers in, printed report out."""
import unittest

from dealscreener.__main__ import run

# Listing B, in the order the program asks: price, rent, tax, insurance,
# HOA, down payment %, interest rate %, loan term (years), closing costs.
LISTING_B = ["150000", "1700", "2400", "1200", "0", "25", "7", "30", "6000"]


class FakeConsole:
    """Stands in for the keyboard and screen: answers come from a list, output goes to a list."""

    def __init__(self, answers):
        self.answers = list(answers)
        self.prompts = []
        self.lines = []

    def input(self, prompt):
        self.prompts.append(prompt)
        if not self.answers:
            raise EOFError  # what input() raises when there is nothing left to read
        return self.answers.pop(0)

    def print(self, text=""):
        self.lines.append(str(text))

    def output(self):
        return "\n".join(self.lines)


def run_with(answers):
    console = FakeConsole(answers)
    exit_code = run(input_fn=console.input, print_fn=console.print)
    return console, exit_code


class RunTest(unittest.TestCase):
    def test_listing_b_prints_its_numbers_and_passes(self):
        console, exit_code = run_with(LISTING_B)
        self.assertEqual(exit_code, 0)
        self.assertIn("430.53", console.output())
        self.assertIn("PASS", console.output())
        self.assertEqual(console.lines[-1], "Overall: PASS")

    def test_listing_a_fails(self):
        listing_a = ["200000", "1800"] + LISTING_B[2:]
        console, _ = run_with(listing_a)
        self.assertIn("Cash-on-cash return 5.74% is below 10.00% by 4.26 points", console.output())
        self.assertEqual(console.lines[-1], "Overall: FAIL")

    def test_bad_price_is_asked_again_without_a_traceback(self):
        console, exit_code = run_with(["abc", "-5"] + LISTING_B)
        self.assertEqual(console.prompts[:3], ["Purchase price ($): "] * 3)
        self.assertIn("Please type a number, like 1500.", console.lines)
        self.assertIn("Please type a number that is 0 or more.", console.lines)
        self.assertNotIn("Traceback", console.output())
        self.assertIn("430.53", console.output())
        self.assertEqual(exit_code, 0)

    def test_zero_cash_invested_explains_and_asks_again_from_the_down_payment(self):
        answers = ["150000", "1700", "2400", "1200", "0", "0", "7", "30", "0"]
        answers += ["25", "7", "30", "6000"]  # the second try at the loan details
        console, exit_code = run_with(answers)
        self.assertIn("cash invested", console.output())
        self.assertEqual(console.prompts[9], "Down payment (%): ")
        self.assertEqual(console.lines[-1], "Overall: PASS")
        self.assertEqual(exit_code, 0)

    def test_blank_and_not_a_number_answers_are_asked_again(self):
        console, _ = run_with(["", "nan", "inf"] + LISTING_B)
        self.assertEqual(console.prompts[:4], ["Purchase price ($): "] * 4)
        self.assertEqual(console.lines[-1], "Overall: PASS")

    def test_zero_price_is_asked_again(self):
        console, _ = run_with(["0"] + LISTING_B)
        self.assertIn("The purchase price must be more than 0.", console.lines)

    def test_huge_numbers_are_asked_again(self):
        console, _ = run_with(["1e308"] + LISTING_B)
        self.assertIn("Please type a smaller number.", console.lines)
        self.assertNotIn("nan", console.output())
        self.assertNotIn("inf", console.output())
        self.assertEqual(console.lines[-1], "Overall: PASS")

    def test_percentage_over_100_is_asked_again(self):
        answers = LISTING_B[:5] + ["120"] + LISTING_B[5:]
        console, _ = run_with(answers)
        self.assertIn("Please type a percentage from 0 to 100.", console.lines)
        self.assertEqual(console.lines[-1], "Overall: PASS")

    def test_loan_term_must_be_whole_years(self):
        answers = LISTING_B[:7] + ["0", "2.5"] + LISTING_B[7:]
        console, _ = run_with(answers)
        self.assertEqual(
            console.lines.count("Please type a whole number of years, 1 or more."), 2
        )
        self.assertEqual(console.lines[-1], "Overall: PASS")

    def test_dollar_signs_commas_and_percent_signs_are_allowed(self):
        console, _ = run_with(["$150,000", "1,700", "2400", "1200", "0", "25%", "7%", "30", "6000"])
        self.assertIn("430.53", console.output())

    def test_running_out_of_input_stops_without_a_traceback(self):
        console, exit_code = run_with(LISTING_B[:3])
        self.assertEqual(exit_code, 1)
        self.assertIn("Stopped", console.output())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest`
Expected: FAIL with `ModuleNotFoundError: No module named 'dealscreener.__main__'`

- [ ] **Step 3: Write the program**

`dealscreener/__main__.py`:

```python
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
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest`
Expected: `Ran 32 tests` and `OK`

- [ ] **Step 5: Run it by hand with listing B**

Run:

```bash
printf '150000\n1700\n2400\n1200\n0\n25\n7\n30\n6000\n' | python3 -m dealscreener
```

Expected (the prompts run together on one line because the answers are piped in, not typed):

```
Rental deal screener. Type each number and press Enter.
Purchase price ($): Monthly rent ($): Yearly property tax ($): Yearly insurance ($): Monthly HOA fee ($, 0 if none): Down payment (%): Interest rate (%): Loan term (years): Closing costs ($): 
Monthly mortgage payment: $748.47
Monthly cash flow: $430.53
Cap rate: 9.43%
Cash-on-cash return: 11.88%

PASS  Cash-on-cash return 11.88% is at least 10.00%
PASS  Monthly cash flow $430.53 is at least $100.00

Overall: PASS
```

Then run `python3 -m dealscreener` and type listing A's numbers yourself. Expected: monthly cash flow $268.05, cash-on-cash 5.74% fails by 4.26 points, and `Overall: FAIL`.

- [ ] **Step 6: Update `README.md`**

Add a "How to run it" section: you need Python 3.9 or newer, run `python3 -m unittest` (the last line should say `OK`), then run `python3 -m dealscreener` and try listing B. List the new files under "What's here now".

- [ ] **Step 7: Commit**

```bash
git add dealscreener/__main__.py tests/test_main.py README.md
git commit -m "Add the program that asks for a listing and prints the report"
```
