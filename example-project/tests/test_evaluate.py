"""Tests for the evaluation of the listing step. A fake extract function stands in for the model:
no network, no key, no credit."""
import json
import os
import pathlib
import shutil
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from dealscreener import evaluate, extract

PROJECT = pathlib.Path(__file__).resolve().parent.parent
REAL_CASES = str(PROJECT / "evals" / "expected.json")

GOOD = {"purchase_price": 150000, "monthly_rent": 1700, "yearly_property_tax": 2400,
        "yearly_insurance": 1200, "monthly_hoa": 0}


def extraction(values, input_tokens=400, output_tokens=60):
    return extract.Extraction(values={k: (None if v is None else float(v)) for k, v in values.items()},
                              input_tokens=input_tokens, output_tokens=output_tokens)


class FakeAPIError(Exception):
    """Like the SDK's API errors: carries the HTTP status code."""

    def __init__(self, status_code, message="error"):
        super().__init__(message)
        self.status_code = status_code


class FieldOkTest(unittest.TestCase):
    def test_within_one_dollar_is_right(self):
        self.assertTrue(evaluate.field_ok(1700, 1700))
        self.assertTrue(evaluate.field_ok(1700, 1701.0))
        self.assertTrue(evaluate.field_ok(1700, 1699.0))

    def test_more_than_one_dollar_is_wrong(self):
        self.assertFalse(evaluate.field_ok(1700, 1701.01))
        self.assertFalse(evaluate.field_ok(1700, 1698.99))

    def test_nulls(self):
        self.assertTrue(evaluate.field_ok(None, None))
        self.assertFalse(evaluate.field_ok(None, 0))
        self.assertFalse(evaluate.field_ok(0, None))


class IsAmountTest(unittest.TestCase):
    def test_numbers_of_zero_or_more(self):
        self.assertTrue(evaluate.is_amount(0))
        self.assertTrue(evaluate.is_amount(1700.5))

    def test_not_amounts(self):
        for value in (-1, float("nan"), float("inf"), True, "1700", None):
            self.assertFalse(evaluate.is_amount(value), value)


class LoadCasesTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.folder)
        shutil.copytree(PROJECT / "evals" / "listings", os.path.join(self.folder, "listings"))
        with open(REAL_CASES, encoding="utf-8") as f:
            self.cases = json.load(f)

    def write(self, cases):
        path = os.path.join(self.folder, "expected.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cases, f)
        return path

    def assert_refused(self, cases, *words):
        with self.assertRaises(evaluate.EvalError) as caught:
            evaluate.load_cases(self.write(cases))
        for word in words:
            self.assertIn(word, str(caught.exception))

    def test_the_real_file_passes(self):
        cases = evaluate.load_cases(REAL_CASES)
        self.assertEqual(len(cases), 20)
        self.assertEqual(sum(c["held_out"] for c in cases), 5)
        self.assertIn("Fictional listing", cases[0]["text"])

    def test_the_real_file_from_the_project_folder(self):
        old = os.getcwd()
        os.chdir(PROJECT)
        self.addCleanup(os.chdir, old)
        self.assertEqual(len(evaluate.load_cases()), 20)

    def test_a_missing_listing_file(self):
        os.remove(os.path.join(self.folder, "listings", "case-07.txt"))
        self.assert_refused(self.cases, "case-07", "case-07.txt", "missing")

    def test_a_duplicate_id(self):
        self.cases[5]["id"] = "case-05"  # case-06 now has case-05's id
        self.assert_refused(self.cases, "case-05")

    def test_a_misspelt_field(self):
        expected = self.cases[2]["expected"]
        expected["montly_rent"] = expected.pop("monthly_rent")
        self.assert_refused(self.cases, "case-03", "montly_rent")

    def test_19_cases(self):
        self.assert_refused(self.cases[:19], "19")

    def test_4_held_out(self):
        held = [c for c in self.cases if c["held_out"]]
        held[0]["held_out"] = False
        self.assert_refused(self.cases, "4", "held out")

    def test_a_negative_value(self):
        self.cases[9]["expected"]["yearly_insurance"] = -5
        self.assert_refused(self.cases, "case-10", "yearly_insurance")

    def test_a_value_that_is_text(self):
        self.cases[0]["expected"]["purchase_price"] = "182000"
        self.assert_refused(self.cases, "case-01", "purchase_price")


class RunCasesTest(unittest.TestCase):
    def setUp(self):
        self.cases = [
            {"id": "case-01", "category": "clean", "text": "perfect", "expected": dict(GOOD)},
            {"id": "case-02", "category": "trap", "text": "yearly rent", "expected": dict(GOOD)},
            {"id": "case-03", "category": "missing", "text": "guess", "expected": {**GOOD, "yearly_insurance": None}},
            {"id": "case-04", "category": "missing", "text": "null", "expected": dict(GOOD)},
            {"id": "case-05", "category": "clean", "text": "refused", "expected": dict(GOOD)},
            {"id": "case-06", "category": "clean", "text": "busy", "expected": dict(GOOD)},
            {"id": "case-07", "category": "clean", "text": "perfect", "expected": dict(GOOD)},
        ]
        self.calls = []

        def fake(text):
            self.calls.append(text)
            if text == "perfect":
                return extraction(GOOD)
            if text == "yearly rent":
                return extraction({**GOOD, "monthly_rent": 20400})
            if text == "guess":
                return extraction(GOOD)
            if text == "null":
                return extraction({**GOOD, "monthly_rent": None})
            if text == "refused":
                raise extract.ExtractionError("The model declined to read this listing.")
            raise FakeAPIError(429)

        self.lines = []
        self.results = evaluate.run_cases(self.cases, fake, print_fn=self.lines.append)

    def test_every_case_runs_even_after_errors(self):
        self.assertEqual(len(self.calls), 7)
        self.assertEqual([r.id for r in self.results], [c["id"] for c in self.cases])

    def test_a_perfect_case(self):
        self.assertEqual(self.lines[0], "case-01  5/5")
        self.assertIsNone(self.results[0].error)
        self.assertEqual(self.results[0].fields["monthly_rent"], (1700, 1700.0, True))
        self.assertEqual((self.results[0].input_tokens, self.results[0].output_tokens), (400, 60))

    def test_one_wrong_field(self):
        self.assertEqual(self.lines[1], "case-02  4/5  monthly_rent: expected 1700, got 20400")
        self.assertEqual(self.results[1].category, "trap")

    def test_a_guess_where_null_was_expected(self):
        self.assertEqual(self.lines[2], "case-03  4/5  yearly_insurance: expected null, got 1200")

    def test_a_null_where_a_number_was_expected(self):
        self.assertEqual(self.lines[3], "case-04  4/5  monthly_rent: expected 1700, got null")

    def test_an_extraction_error(self):
        self.assertEqual(self.lines[4], "case-05  ERROR  The model declined to read this listing.")
        self.assertEqual(self.results[4].error, "The model declined to read this listing.")
        self.assertEqual(self.results[4].fields, {})
        self.assertEqual((self.results[4].input_tokens, self.results[4].output_tokens), (0, 0))

    def test_an_api_error_uses_the_plain_sentence(self):
        sentence = extract.describe_error(FakeAPIError(429))
        self.assertEqual(self.lines[5], f"case-06  ERROR  {sentence}")
        self.assertTrue(sentence.startswith("Too many requests"))

    def test_two_wrong_fields_on_one_line(self):
        lines = []
        evaluate.run_cases([{"id": "case-09", "category": "x", "text": "t", "expected": dict(GOOD)}],
                           lambda text: extraction({**GOOD, "monthly_rent": 1650.5, "monthly_hoa": None}),
                           print_fn=lines.append)
        self.assertEqual(lines, ["case-09  3/5  monthly_rent: expected 1700, got 1650.5; "
                                 "monthly_hoa: expected 0, got null"])


class SummariseTest(unittest.TestCase):
    def test_counts_and_cost(self):
        cases = [{"id": f"case-0{i}", "category": "c", "text": str(i), "expected": dict(GOOD)} for i in range(1, 5)]
        replies = {"1": extraction(GOOD, 1000, 100), "2": extraction(GOOD, 1000, 100),
                   "3": extraction({**GOOD, "monthly_hoa": 50}, 1000, 200)}

        def fake(text):
            if text in replies:
                return replies[text]
            raise FakeAPIError(500)

        results = evaluate.run_cases(cases, fake, print_fn=lambda line: None)
        summary = evaluate.summarise(results)
        self.assertEqual(summary["fields_right"], 14)
        self.assertEqual(summary["fields_total"], 15)
        self.assertEqual(summary["cases_all_right"], 2)
        self.assertEqual(summary["cases_scored"], 3)
        self.assertEqual(summary["errors"], 1)
        self.assertEqual(summary["input_tokens"], 3000)
        self.assertEqual(summary["output_tokens"], 400)
        # 3000 x $0.10 / 1,000,000 + 400 x $0.50 / 1,000,000 = $0.0005
        self.assertAlmostEqual(summary["cost"], 0.0005)


class WriteResultsTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.folder)
        cases = [{"id": "case-01", "category": "clean", "text": "a", "expected": dict(GOOD)},
                 {"id": "case-13", "category": "trap", "text": "b", "expected": dict(GOOD)},
                 {"id": "case-20", "category": "clean", "text": "c", "expected": dict(GOOD)}]
        replies = {"a": extraction(GOOD), "b": extraction({**GOOD, "monthly_rent": 20400})}

        def fake(text):
            if text in replies:
                return replies[text]
            raise FakeAPIError(401, "invalid x-api-key sk-ant-secret")

        self.results = evaluate.run_cases(cases, fake, print_fn=lambda line: None)
        self.summary = evaluate.summarise(self.results)

    def test_the_file_has_the_score_the_misses_and_the_date(self):
        with mock.patch.object(evaluate, "RESULTS_DIR", self.folder):
            path = evaluate.write_results(self.results, self.summary, "dev")
        self.assertTrue(path.startswith(self.folder))
        self.assertTrue(path.endswith("-dev.md"))
        text = pathlib.Path(path).read_text(encoding="utf-8")
        today = evaluate.today()
        self.assertIn(today, os.path.basename(path))
        self.assertIn(today, text)
        self.assertIn(extract.MODEL, text)
        self.assertIn("Score: 9 of 10 fields right (90%), 1 of 2 cases fully right. Errors: 1.", text)
        self.assertIn("| case-13 | trap | monthly_rent | 1700 | 20400 |", text)
        self.assertIn("case-20: The API key was not accepted.", text)
        self.assertIn("Cost: about $", text)
        self.assertNotIn("sk-ant-", text)

    def test_a_second_run_on_the_same_day_gets_its_own_file(self):
        with mock.patch.object(evaluate, "RESULTS_DIR", self.folder):
            first = evaluate.write_results(self.results, self.summary, "dev")
            second = evaluate.write_results(self.results, self.summary, "dev")
        self.assertNotEqual(first, second)
        self.assertTrue(second.endswith("-dev-2.md"))

    def test_a_path_given_is_used(self):
        path = os.path.join(self.folder, "mine.md")
        self.assertEqual(evaluate.write_results(self.results, self.summary, "all", path=path), path)
        self.assertTrue(os.path.exists(path))


class FakeClient:
    """Stands in for anthropic.Anthropic(): every call returns listing B's numbers."""

    def __init__(self):
        self.calls = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=json.dumps(GOOD))],
                               stop_reason="end_turn",
                               usage=SimpleNamespace(input_tokens=500, output_tokens=80))


class MainTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.folder)
        for patcher in (mock.patch.object(evaluate, "RESULTS_DIR", self.folder),
                        mock.patch.object(evaluate, "CASES_FILE", REAL_CASES),
                        mock.patch.object(extract, "load_env_file", lambda path=".env": None)):
            patcher.start()
            self.addCleanup(patcher.stop)
        self.client = FakeClient()
        self.lines = []

    def run_main(self, argv, key="test-key"):
        env = {"ANTHROPIC_API_KEY": key} if key else {}
        with mock.patch.dict(os.environ, env, clear=False):
            if not key:
                os.environ.pop("ANTHROPIC_API_KEY", None)
            return evaluate.main(argv, print_fn=self.lines.append, client_factory=lambda: self.client)

    def test_no_key_gives_the_week_9_sentence_and_runs_nothing(self):
        self.assertEqual(self.run_main([], key=None), 1)
        self.assertEqual(self.client.calls, [])
        self.assertIn("No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README).", self.lines)
        self.assertEqual(os.listdir(self.folder), [])

    def test_the_no_key_sentence_matches_week_9(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("ANTHROPIC_API_KEY", None)
            with self.assertRaises(extract.ExtractionError) as caught:
                extract.make_client()
        self.assertEqual(str(caught.exception), evaluate.NO_KEY)

    def test_the_default_runs_the_15_dev_cases(self):
        self.assertEqual(self.run_main([]), 0)
        self.assertEqual(len(self.client.calls), 15)
        self.assertIn(f"Running the 15 dev cases with {extract.MODEL}.", self.lines)
        case_lines = [line for line in self.lines if line.startswith("case-")]
        self.assertEqual(len(case_lines), 15)
        self.assertNotIn("case-03", " ".join(case_lines))

    def test_held_out_prints_the_reminder_first_and_runs_only_5(self):
        self.assertEqual(self.run_main(["--held-out"]), 0)
        self.assertEqual(self.lines[0], evaluate.HELD_OUT_REMINDER)
        self.assertIn("Run them once, after your change", self.lines[0])
        self.assertEqual(len(self.client.calls), 5)
        ids = [line.split()[0] for line in self.lines if line.startswith("case-")]
        self.assertEqual(ids, ["case-03", "case-07", "case-11", "case-14", "case-17"])

    def test_all_runs_20(self):
        self.assertEqual(self.run_main(["--all"]), 0)
        self.assertEqual(len(self.client.calls), 20)
        self.assertIn(f"Running all 20 cases with {extract.MODEL}.", self.lines)

    def test_score_cost_and_saved_lines(self):
        self.assertEqual(self.run_main(["--all"]), 0)
        score = [line for line in self.lines if line.startswith("Score: ")]
        self.assertEqual(len(score), 1)
        self.assertRegex(score[0], r"^Score: \d+ of 100 fields right \(\d+%\), \d+ of 20 cases fully right\. Errors: 0\.$")
        self.assertTrue(any(line.startswith("Cost: about $") for line in self.lines))
        saved = self.lines[-1]
        self.assertTrue(saved.startswith("Saved: "))
        self.assertTrue(os.path.exists(saved[len("Saved: "):]))

    def test_misses_still_return_0(self):
        # Every reply is listing B's numbers, so almost every case has misses.
        self.assertEqual(self.run_main([]), 0)

    def test_a_results_folder_that_cant_be_written_is_reported(self):
        blocker = os.path.join(self.folder, "a-file")
        pathlib.Path(blocker).write_text("not a folder", encoding="utf-8")
        with mock.patch.object(evaluate, "RESULTS_DIR", os.path.join(blocker, "results")):
            self.assertEqual(self.run_main(["--held-out"]), 1)
        self.assertEqual(len(self.client.calls), 5)
        self.assertTrue(any(line.startswith("Score: ") for line in self.lines))
        self.assertTrue(self.lines[-1].startswith("Couldn't save the results file"))

    def test_every_case_failing_returns_1(self):
        def broken(**kwargs):
            raise FakeAPIError(401, "invalid x-api-key")
        self.client.create = broken
        self.assertEqual(self.run_main(["--held-out"]), 1)
        self.assertTrue(any(line.startswith("Saved: ") for line in self.lines))
        self.assertTrue(self.lines[-1].startswith("Every case failed"))

    def test_an_unknown_flag_prints_usage_and_returns_2(self):
        self.assertEqual(self.run_main(["--everything"]), 2)
        self.assertEqual(self.client.calls, [])
        self.assertTrue(self.lines[0].startswith("Usage: python3 -m dealscreener.evaluate"))

    def test_a_broken_cases_file_is_a_setup_problem(self):
        with mock.patch.object(evaluate, "CASES_FILE", os.path.join(self.folder, "nothing.json")):
            self.assertEqual(self.run_main([]), 1)
        self.assertEqual(self.client.calls, [])
        self.assertIn("missing", self.lines[-1])

    def test_a_client_that_cant_be_made_is_a_setup_problem(self):
        def no_package():
            raise extract.ExtractionError("The anthropic package isn't installed (pip install -r requirements.txt).")
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            self.assertEqual(evaluate.main([], print_fn=self.lines.append, client_factory=no_package), 1)
        self.assertIn("The anthropic package isn't installed (pip install -r requirements.txt).", self.lines)


if __name__ == "__main__":
    unittest.main()
