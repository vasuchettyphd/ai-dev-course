"""Work out a rental listing's mortgage, cash flow, cap rate and cash-on-cash return."""
from __future__ import annotations

import math
from dataclasses import dataclass


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
    return principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)


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

    return Results(
        monthly_mortgage=mortgage,
        monthly_cash_flow=cash_flow,
        cap_rate_pct=(effective_rent - operating_costs) * 12 / listing.purchase_price * 100,
        cash_on_cash_pct=cash_flow * 12 / cash_invested * 100,
    )


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
