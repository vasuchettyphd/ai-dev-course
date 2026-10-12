"""Tests for the program you run: typed answers in, printed report out."""
import unittest

from dealscreener.__main__ import run
from dealscreener.extract import ExtractionError
from tests.test_extract import GOOD, FakeAPIError, FakeClient, reply

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


def listing_b_with_rate(*rate_answers):
    answers = list(LISTING_B)
    answers[6:7] = list(rate_answers)
    return answers


class SmallPercentTest(unittest.TestCase):
    def test_rate_typed_as_a_fraction_asks_and_yes_means_percent(self):
        console, exit_code = run_with(listing_b_with_rate("0.07", "y"))
        self.assertEqual(exit_code, 0)
        self.assertIn("You typed 0.07. Did you mean 7%? Type y for 7%, or n to keep 0.07%: ", console.prompts)
        plain, _ = run_with(LISTING_B)
        self.assertEqual(console.output().splitlines()[-9:], plain.output().splitlines()[-9:])

    def test_no_keeps_the_small_rate(self):
        console, exit_code = run_with(listing_b_with_rate("0.07", "n"))
        self.assertEqual(exit_code, 0)
        self.assertIn("Monthly mortgage payment: $315.80", console.output())

    def test_yes_and_no_ignore_case_and_spaces(self):
        yes, _ = run_with(listing_b_with_rate("0.07", " YES "))
        plain, _ = run_with(LISTING_B)
        self.assertEqual(yes.output().splitlines()[-9:], plain.output().splitlines()[-9:])
        no, _ = run_with(listing_b_with_rate("0.07", "No"))
        self.assertIn("Monthly mortgage payment: $315.80", no.output())

    def test_other_answers_ask_the_follow_up_again(self):
        console, exit_code = run_with(listing_b_with_rate("0.07", "", "maybe", "y"))
        self.assertEqual(exit_code, 0)
        follow_up = "You typed 0.07. Did you mean 7%? Type y for 7%, or n to keep 0.07%: "
        self.assertEqual(console.prompts.count(follow_up), 3)

    def test_shows_the_number_without_extra_zeros(self):
        console, _ = run_with(listing_b_with_rate("0.065", "y"))
        self.assertIn("You typed 0.065. Did you mean 6.5%? Type y for 6.5%, or n to keep 0.065%: ", console.prompts)

    def test_zero_and_whole_percentages_are_not_questioned(self):
        for rate in ("0", "1", "7", "100"):
            console, _ = run_with(listing_b_with_rate(rate))
            self.assertFalse(any(p.startswith("You typed") for p in console.prompts), rate)

    def test_down_payment_typed_as_a_fraction_is_asked_too(self):
        answers = list(LISTING_B)
        answers[5:6] = ["0.25", "y"]
        console, exit_code = run_with(answers)
        self.assertEqual(exit_code, 0)
        self.assertIn("You typed 0.25. Did you mean 25%? Type y for 25%, or n to keep 0.25%: ", console.prompts)
        plain, _ = run_with(LISTING_B)
        self.assertEqual(console.output().splitlines()[-9:], plain.output().splitlines()[-9:])

    def test_running_out_of_input_at_the_follow_up_stops_politely(self):
        console, exit_code = run_with(LISTING_B[:6] + ["0.07"])
        self.assertEqual(exit_code, 1)
        self.assertIn("Stopped before all the numbers were typed.", console.output())


# What to type for the loan questions with listing B (the property numbers come from the listing).
LOAN_B = LISTING_B[5:]
ACCEPT_ALL = ["", "", "", "", ""]  # press Enter at each of the five property questions
FALLBACK = " For now, type the numbers yourself."


def run_listing(answers, client=None, factory=None):
    """Run with the listing step on. The factory hands out the fake client, never a real one."""
    console = FakeConsole(answers)
    made = []

    def fake_factory():
        made.append(True)
        return client

    exit_code = run(input_fn=console.input, print_fn=console.print, use_listing=True,
                    client_factory=factory or fake_factory)
    return console, exit_code, made


class ListingStepTest(unittest.TestCase):
    def test_without_the_flag_nothing_changes(self):
        console, exit_code = run_with(LISTING_B)
        self.assertEqual(exit_code, 0)
        self.assertFalse(any("Paste" in line for line in console.lines))
        self.assertFalse(any("from the listing" in p for p in console.prompts))
        self.assertEqual(console.prompts[0], "Purchase price ($): ")

    def test_pasted_listing_values_are_confirmed_with_enter(self):
        client = FakeClient(reply(GOOD))
        console, exit_code, made = run_listing(["line one", "", "line two", "done"] + ACCEPT_ALL + LOAN_B, client)
        self.assertEqual(exit_code, 0)
        plain, _ = run_with(LISTING_B)
        self.assertEqual(console.lines[-9:], plain.lines[-9:])
        self.assertIn("Purchase price ($) [from the listing: 150000]: ", console.prompts)
        self.assertIn("Monthly HOA fee ($, 0 if none) [from the listing: 0]: ", console.prompts)
        self.assertIn("Used 400 input and 60 output tokens", console.output())
        self.assertIn("line one\n\nline two", client.calls[0]["messages"][0]["content"])
        self.assertEqual(len(client.calls), 1)

    def test_typing_a_number_replaces_the_listing_value(self):
        client = FakeClient(reply(GOOD))
        console, _, _ = run_listing(["a listing", "done", "160000", "", "", "", ""] + LOAN_B, client)
        typed, _ = run_with(["160000"] + LISTING_B[1:])
        self.assertEqual(console.lines[-9:], typed.lines[-9:])
        self.assertNotEqual(console.lines[-9:], run_with(LISTING_B)[0].lines[-9:])

    def test_missing_values_are_asked_normally(self):
        client = FakeClient(reply(dict(GOOD, monthly_hoa=None)))
        console, exit_code, _ = run_listing(["a listing", "done", "", "", "", "", "0"] + LOAN_B, client)
        self.assertIn("Monthly HOA fee ($, 0 if none): ", console.prompts)
        self.assertFalse(any(p.startswith("Monthly HOA fee") and "[from the listing" in p for p in console.prompts))
        self.assertEqual(console.lines[-1], "Overall: PASS")
        self.assertEqual(exit_code, 0)

    def test_an_extracted_value_that_fails_the_checks_is_asked_again(self):
        client = FakeClient(reply(dict(GOOD, purchase_price=0)))
        console, exit_code, _ = run_listing(["a listing", "done", "", "150000", "", "", "", ""] + LOAN_B, client)
        self.assertIn("Purchase price ($) [from the listing: 0]: ", console.prompts)
        self.assertIn("The purchase price must be more than 0.", console.lines)
        self.assertIn("Purchase price ($): ", console.prompts)
        self.assertEqual(console.lines[-1], "Overall: PASS")
        self.assertEqual(exit_code, 0)

    def test_a_bad_typed_answer_offers_the_listing_value_again(self):
        client = FakeClient(reply(GOOD))
        console, _, _ = run_listing(["a listing", "done", "abc", ""] + ACCEPT_ALL[1:] + LOAN_B, client)
        self.assertIn("Please type a number, like 1500.", console.lines)
        self.assertEqual(console.prompts.count("Purchase price ($) [from the listing: 150000]: "), 2)
        self.assertEqual(console.lines[-1], "Overall: PASS")

    def test_loan_questions_are_always_asked_normally(self):
        client = FakeClient(reply(GOOD))
        console, _, _ = run_listing(["a listing", "done"] + ACCEPT_ALL + LOAN_B, client)
        for prompt in ("Down payment (%): ", "Interest rate (%): ", "Loan term (years): ", "Closing costs ($): "):
            self.assertIn(prompt, console.prompts)

    def test_skip_with_done_makes_no_call(self):
        console, exit_code, made = run_listing(["done"] + LISTING_B)
        self.assertEqual(made, [])
        self.assertEqual(console.lines[-1], "Overall: PASS")
        self.assertEqual(exit_code, 0)

    def test_only_blank_lines_makes_no_call(self):
        console, _, made = run_listing(["", "  ", "done"] + LISTING_B)
        self.assertEqual(made, [])
        self.assertEqual(console.lines[-1], "Overall: PASS")

    def test_no_key_falls_back_to_typing(self):
        def no_key():
            raise ExtractionError("No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README).")

        console, exit_code, _ = run_listing(["a listing", "done"] + LISTING_B, factory=no_key)
        self.assertIn("No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README)." + FALLBACK,
                      console.lines)
        self.assertEqual(console.prompts.count("Purchase price ($): "), 1)
        plain, _ = run_with(LISTING_B)
        self.assertEqual(console.lines[-9:], plain.lines[-9:])
        self.assertEqual(exit_code, 0)

    def test_a_bad_reply_falls_back_to_typing(self):
        client = FakeClient(reply("not json"))
        console, exit_code, _ = run_listing(["a listing", "done"] + LISTING_B, client)
        self.assertIn("The model's answer wasn't in the expected form." + FALLBACK, console.lines)
        self.assertEqual(exit_code, 0)

    def test_api_errors_fall_back_without_a_traceback(self):
        for error, words in ((FakeAPIError(401), "not accepted"), (FakeAPIError(429), "Wait a minute"),
                             (ConnectionError("down"), "reach Anthropic")):
            console, exit_code, _ = run_listing(["a listing", "done"] + LISTING_B, FakeClient(error=error))
            self.assertTrue(any(words in line and line.endswith(FALLBACK) for line in console.lines), words)
            self.assertNotIn("Traceback", console.output())
            self.assertEqual(console.lines[-1], "Overall: PASS")
            self.assertEqual(exit_code, 0)

    def test_too_long_paste_makes_no_call(self):
        console, _, made = run_listing(["x" * 20001, "done"] + LISTING_B)
        self.assertIn("That listing is too long (over 20,000 characters). Type the numbers yourself.", console.lines)
        self.assertEqual(made, [])
        self.assertEqual(console.lines[-1], "Overall: PASS")

    def test_running_out_of_input_while_pasting_stops_politely(self):
        console, exit_code, made = run_listing(["only a line"])
        self.assertEqual(exit_code, 1)
        self.assertIn("Stopped before all the numbers were typed.", console.output())
        self.assertEqual(made, [])

    def test_done_is_case_and_space_insensitive(self):
        client = FakeClient(reply(GOOD))
        console, exit_code, _ = run_listing(["a listing", "  DONE "] + ACCEPT_ALL + LOAN_B, client)
        self.assertEqual(client.calls[0]["messages"][0]["content"].count("DONE"), 0)
        self.assertEqual(console.lines[-1], "Overall: PASS")
        self.assertEqual(exit_code, 0)

    def test_the_paste_prompt_and_the_cost_line_are_shown(self):
        client = FakeClient(reply(GOOD, input_tokens=1000, output_tokens=200))
        console, _, _ = run_listing(["a listing", "done"] + ACCEPT_ALL + LOAN_B, client)
        self.assertIn("Paste the listing text, then type done on a line by itself and press Enter. "
                      "To skip and type the numbers yourself, type done now.", console.lines)
        self.assertIn("Asking the model to read the listing...", console.lines)
        self.assertIn("Used 1000 input and 200 output tokens, about $0.0002.", console.lines)


if __name__ == "__main__":
    unittest.main()
