"""One real run of the agent, only on request: it needs a key and costs a tiny amount of credit.

From the example-project folder, with the key in your environment (see the README):
    RUN_LIVE_TESTS=1 python -m unittest tests.test_agent_live -v
Without RUN_LIVE_TESTS=1 and a key, this test is skipped, so python3 -m unittest stays offline.
"""
import os
import unittest

from dealscreener import agent, extract

LISTING_B_QUESTION = (
    "Should I buy this rental? The price is $150,000 and the rent is $1,700 a month. "
    "Property tax is $2,400 a year, insurance is $1,200 a year and there is no HOA fee. "
    "I'd put 25% down on a 30-year loan at 7% interest, with $6,000 in closing costs."
)


@unittest.skipUnless(os.environ.get("RUN_LIVE_TESTS") == "1" and os.environ.get("ANTHROPIC_API_KEY"),
                     "live test: set RUN_LIVE_TESTS=1 and a key")
class LiveAgentTest(unittest.TestCase):
    def test_listing_b_question_uses_the_tool_and_reports_its_cash_flow(self):
        result = agent.run_agent(LISTING_B_QUESTION, extract.make_client())
        self.assertGreaterEqual(result.tool_calls, 1)
        self.assertIsNotNone(result.text)
        self.assertIn("430.53", result.text)
        print(f"\nlive agent: {result.turns} turns, {result.tool_calls} tool calls, "
              f"{result.input_tokens} input and {result.output_tokens} output tokens, "
              f"about ${extract.cost_usd(result.input_tokens, result.output_tokens):.4f}")


if __name__ == "__main__":
    unittest.main()
