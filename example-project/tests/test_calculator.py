"""Tests for the calculator. The expected numbers were worked out by hand first."""
import unittest

from dealscreener.calculator import (
    Assumptions,
    Listing,
    analyse,
    monthly_mortgage_payment,
)


def make_listing(**changes):
    """Listing A from the docs/ task plan, with any fields changed that a test asks for."""
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


class HoaTest(unittest.TestCase):
    def test_listing_a_with_a_150_dollar_hoa_matches_the_hand_worked_numbers(self):
        # Costs go up by $150 a month, to 300 + 150 + 144 = 594, so cash flow
        # drops by exactly $150: 1710 - 594 - 997.95 = 118.05.
        results = analyse(make_listing(monthly_hoa=150), ASSUMPTIONS)
        self.assertAlmostEqual(results.monthly_mortgage, 997.95, delta=0.01)
        self.assertAlmostEqual(results.monthly_cash_flow, 118.05, delta=0.01)
        self.assertAlmostEqual(results.cap_rate_pct, 6.696, delta=0.001)
        self.assertAlmostEqual(results.cash_on_cash_pct, 2.530, delta=0.001)


class OtherAssumptionsTest(unittest.TestCase):
    def test_listing_a_with_10_percent_vacancy_and_5_percent_repairs(self):
        # Rent kept: 1800 x 0.90 = 1620. Repairs: 1800 x 0.05 = 90, so costs
        # are 300 + 0 + 90 = 390. Cash flow: 1620 - 390 - 997.95 = 232.05.
        results = analyse(make_listing(), Assumptions(vacancy_pct=10, repairs_reserve_pct=5))
        self.assertAlmostEqual(results.monthly_mortgage, 997.95, delta=0.01)
        self.assertAlmostEqual(results.monthly_cash_flow, 232.05, delta=0.01)
        self.assertAlmostEqual(results.cap_rate_pct, 7.380, delta=0.001)
        self.assertAlmostEqual(results.cash_on_cash_pct, 4.972, delta=0.001)


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
