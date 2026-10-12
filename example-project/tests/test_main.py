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
