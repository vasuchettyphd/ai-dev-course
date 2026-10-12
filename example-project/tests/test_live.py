"""One real call to the model, run only on request: it needs a key and costs a tiny amount of credit.

From the example-project folder, with the key in your environment (see the README):
    RUN_LIVE_TESTS=1 python -m unittest tests.test_live -v
Without RUN_LIVE_TESTS=1 and a key, this test is skipped, so python3 -m unittest stays offline.
"""
import os
import pathlib
import unittest

from dealscreener import extract

LISTING_B = {"purchase_price": 150000, "monthly_rent": 1700, "yearly_property_tax": 2400,
             "yearly_insurance": 1200, "monthly_hoa": 0}


@unittest.skipUnless(os.environ.get("RUN_LIVE_TESTS") == "1" and os.environ.get("ANTHROPIC_API_KEY"),
                     "live test: set RUN_LIVE_TESTS=1 and a key")
class LiveExtractTest(unittest.TestCase):
    def test_listing_b_text_gives_listing_b_numbers(self):
        text = (pathlib.Path(__file__).parent.parent / "listings" / "listing-b.txt").read_text(encoding="utf-8")
        result = extract.extract_listing(text, extract.make_client())
        for field, expected in LISTING_B.items():
            self.assertIsNotNone(result.values[field], field)
            self.assertAlmostEqual(result.values[field], expected, delta=1, msg=field)
        self.assertGreater(result.input_tokens, 0)
        self.assertGreater(result.output_tokens, 0)
        print(f"\nlive call: {result.input_tokens} input and {result.output_tokens} output tokens, "
              f"about ${extract.cost_usd(result.input_tokens, result.output_tokens):.4f}")


if __name__ == "__main__":
    unittest.main()
