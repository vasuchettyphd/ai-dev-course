"""Tests for the screen_listing tool (week 11). Plain Python only: no packages, no key."""
import math
import unittest

from dealscreener import tools

LISTING_B = {"purchase_price": 150000, "monthly_rent": 1700, "yearly_property_tax": 2400,
             "yearly_insurance": 1200, "monthly_hoa": 0, "down_payment_pct": 25,
             "interest_rate_pct": 7, "loan_term_years": 30, "closing_costs": 6000}


def listing_b(**changes):
    """Listing B with some numbers changed."""
    raw = dict(LISTING_B)
    raw.update(changes)
    return raw


class ScreenListingTest(unittest.TestCase):
    def test_listing_b_passes_with_the_same_numbers_as_the_program(self):
        result = tools.screen_listing(LISTING_B)
        self.assertEqual(result["monthly_cash_flow"], 430.53)
        self.assertEqual(result["overall"], "PASS")
        self.assertEqual(set(result), {"monthly_mortgage", "monthly_cash_flow", "cap_rate_pct",
                                       "cash_on_cash_pct", "rules", "overall"})
        for rule in result["rules"]:
            self.assertEqual(set(rule), {"passed", "reason"})
            self.assertTrue(rule["passed"])

    def test_numbers_are_rounded_to_cents(self):
        result = tools.screen_listing(LISTING_B)
        for name in ("monthly_mortgage", "monthly_cash_flow", "cap_rate_pct", "cash_on_cash_pct"):
            self.assertEqual(result[name], round(result[name], 2))

    def test_listing_a_fails(self):
        result = tools.screen_listing(listing_b(purchase_price=200000, monthly_rent=1800))
        self.assertEqual(result["overall"], "FAIL")
        self.assertIn(False, [rule["passed"] for rule in result["rules"]])

    def test_zero_cash_invested_gives_the_calculators_sentence(self):
        with self.assertRaises(tools.ToolInputError) as caught:
            tools.screen_listing(listing_b(down_payment_pct=0, closing_costs=0))
        self.assertIn("cash invested", str(caught.exception))


class CheckInputTest(unittest.TestCase):
    def assert_refused(self, raw, *words):
        with self.assertRaises(tools.ToolInputError) as caught:
            tools.check_input(raw)
        for word in words:
            self.assertIn(word, str(caught.exception))
        return str(caught.exception)

    def test_good_input_becomes_a_listing(self):
        listing = tools.check_input(LISTING_B)
        self.assertEqual(listing.purchase_price, 150000.0)
        self.assertEqual(listing.loan_term_years, 30)
        self.assertIsInstance(listing.loan_term_years, int)

    def test_input_that_is_not_an_object(self):
        self.assert_refused(["150000"], "object")

    def test_missing_field(self):
        raw = listing_b()
        del raw["monthly_rent"]
        self.assert_refused(raw, "Missing field: monthly_rent.")

    def test_unknown_field(self):
        self.assert_refused(listing_b(vacancy_pct=5), "Unknown field: vacancy_pct.")

    def test_text_instead_of_a_number(self):
        self.assert_refused(listing_b(monthly_rent="1700"), "monthly_rent")

    def test_true_or_false_instead_of_a_number(self):
        self.assert_refused(listing_b(monthly_hoa=False), "monthly_hoa")

    def test_negative(self):
        self.assert_refused(listing_b(yearly_insurance=-5), "yearly_insurance")

    def test_not_a_number_or_infinite(self):
        self.assert_refused(listing_b(yearly_property_tax=math.nan), "yearly_property_tax")
        self.assert_refused(listing_b(yearly_property_tax=math.inf), "yearly_property_tax")
        self.assert_refused(listing_b(yearly_property_tax=10 ** 400), "yearly_property_tax")

    def test_rate_over_100(self):
        self.assert_refused(listing_b(interest_rate_pct=250), "interest_rate_pct", "0 to 100")

    def test_part_years(self):
        self.assert_refused(listing_b(loan_term_years=30.5), "loan_term_years", "whole number")

    def test_whole_years_written_as_a_decimal_are_fine(self):
        self.assertEqual(tools.check_input(listing_b(loan_term_years=30.0)).loan_term_years, 30)

    def test_price_of_zero(self):
        self.assert_refused(listing_b(purchase_price=0), "purchase_price", "more than 0")

    def test_huge_number(self):
        self.assert_refused(listing_b(monthly_rent=1e300), "monthly_rent", "smaller")

    def test_percentage_written_as_a_fraction_is_refused_with_the_exact_sentence(self):
        message = self.assert_refused(listing_b(interest_rate_pct=0.07))
        self.assertEqual(message, "interest_rate_pct is 0.07: percentages are written as 7 for 7%. "
                                  "Ask the user which they meant.")

    def test_zero_percent_is_fine(self):
        self.assertEqual(tools.check_input(listing_b(interest_rate_pct=0)).interest_rate_pct, 0.0)


class ToolSchemaTest(unittest.TestCase):
    def test_nine_fields_all_required_and_nothing_else(self):
        self.assertEqual(tools.TOOL_SCHEMA["name"], "screen_listing")
        self.assertEqual(tools.TOOL_NAME, "screen_listing")
        schema = tools.TOOL_SCHEMA["input_schema"]
        self.assertEqual(schema["type"], "object")
        self.assertEqual(list(schema["properties"]), tools.FIELDS)
        self.assertEqual(len(tools.FIELDS), 9)
        self.assertEqual(schema["required"], tools.FIELDS)
        self.assertIs(schema["additionalProperties"], False)

    def test_each_field_has_a_type_and_a_description(self):
        for field, spec in tools.TOOL_SCHEMA["input_schema"]["properties"].items():
            self.assertIn(spec["type"], ("number", "integer"), field)
            self.assertTrue(spec["description"], field)
        self.assertEqual(tools.TOOL_SCHEMA["input_schema"]["properties"]["loan_term_years"]["type"],
                         "integer")

    def test_description_says_how_percentages_are_written(self):
        self.assertIn("percentages are written as 25 for 25%", tools.TOOL_SCHEMA["description"])

    def test_description_says_vacancy_and_repairs_are_already_allowed_for(self):
        # Without this, a live run told the user the calculator leaves them out.
        self.assertIn("5% of the rent for empty months (vacancy)", tools.TOOL_SCHEMA["description"])
        self.assertIn("8% of the rent for repairs", tools.TOOL_SCHEMA["description"])

    def test_fields_match_the_listing(self):
        from dataclasses import fields
        from dealscreener.calculator import Listing
        self.assertEqual(tools.FIELDS, [field.name for field in fields(Listing)])


if __name__ == "__main__":
    unittest.main()
