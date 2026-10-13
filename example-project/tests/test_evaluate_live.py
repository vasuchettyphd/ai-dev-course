"""The 15 dev cases against the real model, run only on request: it needs a key and costs a
small amount of credit.

From the example-project folder, with the key in your environment (see the README):
    RUN_LIVE_TESTS=1 python -m unittest tests.test_evaluate_live -v
Without RUN_LIVE_TESTS=1 and a key, this test is skipped, so python3 -m unittest stays offline.
"""
import os
import pathlib
import unittest

from dealscreener import evaluate, extract

CASES = pathlib.Path(__file__).resolve().parent.parent / "evals" / "expected.json"

# The share of fields the dev cases must get right. See the README for how it was chosen.
FLOOR = 0.8


@unittest.skipUnless(os.environ.get("RUN_LIVE_TESTS") == "1" and os.environ.get("ANTHROPIC_API_KEY"),
                     "live test: set RUN_LIVE_TESTS=1 and a key")
class LiveEvaluateTest(unittest.TestCase):
    def test_the_dev_cases_score_at_least_the_floor(self):
        cases = [case for case in evaluate.load_cases(str(CASES)) if not case["held_out"]]
        self.assertEqual(len(cases), 15)
        client = extract.make_client()
        results = evaluate.run_cases(cases, lambda text: extract.extract_listing(text, client))
        summary = evaluate.summarise(results)
        print(f"\n{evaluate.score_line(summary)} {evaluate.cost_line(summary)}")
        self.assertGreater(summary["fields_total"], 0)
        self.assertGreaterEqual(summary["fields_right"] / summary["fields_total"], FLOOR)


if __name__ == "__main__":
    unittest.main()
