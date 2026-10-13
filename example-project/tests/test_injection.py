"""Tests for the prompt injection set (week 13). A fake client stands in for the model:
no network, no key, no credit."""
import json
import os
import pathlib
import shutil
import tempfile
import unittest
from unittest import mock

from dealscreener import evaluate, extract
from tests.test_evaluate import FakeClient

PROJECT = pathlib.Path(__file__).resolve().parent.parent
INJECTION_CASES = str(PROJECT / evaluate.INJECTION_FILE)


class LoadInjectionCasesTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.folder)
        shutil.copytree(PROJECT / "evals" / "injection" / "listings", os.path.join(self.folder, "listings"))
        with open(INJECTION_CASES, encoding="utf-8") as f:
            self.cases = json.load(f)

    def load(self, cases):
        path = os.path.join(self.folder, "expected.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cases, f)
        return evaluate.load_cases(path, case_count=evaluate.INJECTION_COUNT, held_out_count=0)

    def test_the_real_file_passes(self):
        cases = evaluate.load_cases(INJECTION_CASES, case_count=evaluate.INJECTION_COUNT, held_out_count=0)
        self.assertEqual(len(cases), 8)
        self.assertEqual([case["id"] for case in cases], [f"inj-0{n}" for n in range(1, 9)])
        for case in cases:
            self.assertFalse(case["held_out"])
            self.assertEqual(case["category"], "injection")
            self.assertIn("Fictional listing written for this course example", case["text"])

    def test_7_cases_are_refused_with_the_count_named(self):
        with self.assertRaises(evaluate.EvalError) as caught:
            self.load(self.cases[:7])
        self.assertIn("has 7 cases; it needs exactly 8", str(caught.exception))

    def test_one_held_out_case_is_refused_with_the_count_named(self):
        self.cases[0]["held_out"] = True
        with self.assertRaises(evaluate.EvalError) as caught:
            self.load(self.cases)
        self.assertIn("marks 1 cases as held out; it needs exactly 0", str(caught.exception))

    def test_the_week_12_counts_are_still_the_default(self):
        with self.assertRaises(evaluate.EvalError) as caught:
            evaluate.load_cases(INJECTION_CASES)
        self.assertIn("has 8 cases; it needs exactly 20", str(caught.exception))


class MainInjectionTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.folder)
        for patcher in (mock.patch.object(evaluate, "RESULTS_DIR", self.folder),
                        mock.patch.object(evaluate, "INJECTION_FILE", INJECTION_CASES),
                        mock.patch.object(extract, "load_env_file", lambda path=".env": None),
                        mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})):
            patcher.start()
            self.addCleanup(patcher.stop)
        self.client = FakeClient()
        self.lines = []

    def run_main(self, argv):
        return evaluate.main(argv, print_fn=self.lines.append, client_factory=lambda: self.client)

    def test_injection_runs_the_8_cases_and_saves_its_own_file(self):
        self.assertEqual(self.run_main(["--injection"]), 0)
        self.assertEqual(len(self.client.calls), 8)
        self.assertIn(f"Running the 8 injection cases with {extract.MODEL}.", self.lines)
        ids = [line.split()[0] for line in self.lines if line.startswith("inj-")]
        self.assertEqual(ids, [f"inj-0{n}" for n in range(1, 9)])
        self.assertEqual(os.listdir(self.folder), [f"{evaluate.today()}-injection.md"])
        self.assertTrue(self.lines[-1].endswith(f"{evaluate.today()}-injection.md"))

    def test_the_usage_names_the_injection_flag(self):
        self.assertIn("  --injection the 8 hostile listings (week 13)", evaluate.USAGE)

    def test_an_unknown_flag_still_returns_2(self):
        self.assertEqual(self.run_main(["--hostile"]), 2)
        self.assertEqual(self.client.calls, [])
        self.assertEqual(self.lines, [evaluate.USAGE])


if __name__ == "__main__":
    unittest.main()
