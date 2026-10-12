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
    amount = round(amount, 2)  # so -0.004 shows as $0.00, not -$0.00
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):,.2f}"


def percent(value: float) -> str:
    """Format a percentage, for example 9.432 -> '9.43%' (and -0.004 -> '0.00%')."""
    return f"{round(value, 2) + 0.0:.2f}%"  # adding 0.0 turns -0.0 into 0.0


# Both rules compare the value rounded to 2 decimals, the same as the reason
# shows it, so the reason never contradicts pass or fail (9.996% shows as
# 10.00% and passes).


def _check_cash_on_cash(value: float, threshold: float) -> RuleResult:
    name = "Cash-on-cash return"
    shown = round(value, 2)
    passed = shown >= threshold
    if passed:
        reason = f"{name} {percent(shown)} is at least {percent(threshold)}"
    else:
        reason = (
            f"{name} {percent(shown)} is below {percent(threshold)}"
            f" by {threshold - shown:.2f} points"
        )
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
