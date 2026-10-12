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

    def test_negative_cash_flow_fails(self):
        _, cash_flow = check(make_results(cash_on_cash_pct=20, monthly_cash_flow=-50))
        self.assertFalse(cash_flow.passed)
        self.assertEqual(
            cash_flow.reason, "Monthly cash flow -$50.00 is below $100.00 by $150.00"
        )


if __name__ == "__main__":
    unittest.main()
