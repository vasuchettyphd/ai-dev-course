"""Tests for the agent loop (week 11). A fake client plays the model from a script of
replies: no network, no key, no credit, no packages."""
import json
import os
import unittest
from types import SimpleNamespace
from unittest import mock

from dealscreener import agent, extract, tools

LISTING_B = {"purchase_price": 150000, "monthly_rent": 1700, "yearly_property_tax": 2400,
             "yearly_insurance": 1200, "monthly_hoa": 0, "down_payment_pct": 25,
             "interest_rate_pct": 7, "loan_term_years": 30, "closing_costs": 6000}


def thinking():
    return SimpleNamespace(type="thinking", thinking="", signature="sig")


def tool_use(tool_input, block_id="toolu_1", name="screen_listing"):
    return SimpleNamespace(type="tool_use", id=block_id, name=name, input=tool_input)


def text(words):
    return SimpleNamespace(type="text", text=words)


def reply(*blocks, stop_reason=None, input_tokens=500, output_tokens=100):
    """A fake model reply. With no stop_reason given: tool_use if a block asks for a tool."""
    if stop_reason is None:
        asks = any(block.type == "tool_use" for block in blocks)
        stop_reason = "tool_use" if asks else "end_turn"
    return SimpleNamespace(content=list(blocks), stop_reason=stop_reason,
                           usage=SimpleNamespace(input_tokens=input_tokens, output_tokens=output_tokens))


class FakeClient:
    """Stands in for anthropic.Anthropic(): returns the scripted replies in order and records
    what each call sent. The history list is copied, because the loop keeps adding to it."""

    def __init__(self, *replies, repeat_last=False, error=None):
        self.replies, self.repeat_last, self.error = list(replies), repeat_last, error
        self.calls = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(dict(kwargs, messages=list(kwargs["messages"])))
        if self.error:
            raise self.error
        if self.repeat_last and len(self.replies) == 1:
            return self.replies[0]
        return self.replies.pop(0)


class FakeAPIError(Exception):
    def __init__(self, status_code):
        super().__init__("error")
        self.status_code = status_code


def run(client, question="Screen listing B"):
    printed = []
    result = agent.run_agent(question, client, print_fn=printed.append)
    return result, printed


class RunAgentTest(unittest.TestCase):
    def test_one_tool_call_then_the_answer(self):
        first = reply(thinking(), tool_use(LISTING_B), input_tokens=600, output_tokens=150)
        client = FakeClient(first, reply(text("Cash flow is $430.53 a month. It passes."),
                                         input_tokens=900, output_tokens=80))
        result, printed = run(client)
        self.assertEqual(result.text, "Cash flow is $430.53 a month. It passes.")
        self.assertEqual((result.turns, result.tool_calls), (2, 1))
        self.assertEqual((result.input_tokens, result.output_tokens), (1500, 230))
        # The second call: the question, the assistant turn unchanged, then the tool result.
        history = client.calls[1]["messages"]
        self.assertEqual(history[0], {"role": "user", "content": "Screen listing B"})
        self.assertEqual(history[1]["role"], "assistant")
        self.assertIs(history[1]["content"], first.content)  # the thinking block is kept as it was
        self.assertEqual(history[1]["content"][0].type, "thinking")
        last = history[-1]
        self.assertEqual(last["role"], "user")
        self.assertEqual(len(last["content"]), 1)
        result_block = last["content"][0]
        self.assertEqual(result_block["type"], "tool_result")
        self.assertEqual(result_block["tool_use_id"], "toolu_1")
        self.assertIn("430.53", result_block["content"])
        self.assertNotIn("is_error", result_block)
        self.assertEqual(json.loads(result_block["content"])["overall"], "PASS")
        self.assertEqual(printed, ["Calling screen_listing with " + json.dumps(LISTING_B, separators=(",", ":"))])

    def test_bad_tool_input_goes_back_as_an_error_and_the_loop_continues(self):
        bad = dict(LISTING_B, interest_rate_pct=0.07)
        client = FakeClient(reply(tool_use(bad)), reply(text("Did you mean 7%?")))
        result, _ = run(client)
        self.assertEqual(result.text, "Did you mean 7%?")
        result_block = client.calls[1]["messages"][-1]["content"][0]
        self.assertIs(result_block["is_error"], True)
        self.assertEqual(result_block["content"], "interest_rate_pct is 0.07: percentages are written "
                                                  "as 7 for 7%. Ask the user which they meant.")

    def test_unknown_tool_name(self):
        client = FakeClient(reply(tool_use({}, name="delete_listing")), reply(text("Sorry.")))
        result, _ = run(client)
        result_block = client.calls[1]["messages"][-1]["content"][0]
        self.assertIs(result_block["is_error"], True)
        self.assertEqual(result_block["content"], "Unknown tool.")
        self.assertEqual(result_block["tool_use_id"], "toolu_1")
        self.assertEqual(result.text, "Sorry.")

    def test_two_tool_calls_in_one_reply_get_both_results_in_one_message(self):
        listing_a = dict(LISTING_B, purchase_price=200000, monthly_rent=1800)
        client = FakeClient(reply(text("Checking both."), tool_use(LISTING_B, "toolu_b"),
                                  tool_use(listing_a, "toolu_a")),
                            reply(text("B passes, A fails.")))
        result, printed = run(client)
        self.assertEqual(result.tool_calls, 2)
        self.assertEqual(len(printed), 2)
        history = client.calls[1]["messages"]
        self.assertEqual(len(history), 3)
        results = history[-1]["content"]
        self.assertEqual([block["type"] for block in results], ["tool_result", "tool_result"])
        self.assertEqual([block["tool_use_id"] for block in results], ["toolu_b", "toolu_a"])
        self.assertEqual(json.loads(results[0]["content"])["overall"], "PASS")
        self.assertEqual(json.loads(results[1]["content"])["overall"], "FAIL")

    def test_stops_after_five_turns_without_a_final_answer(self):
        client = FakeClient(reply(tool_use(LISTING_B)), repeat_last=True)
        result, printed = run(client)
        self.assertIsNone(result.text)
        self.assertEqual(agent.MAX_TURNS, 5)
        self.assertEqual(len(client.calls), 5)
        self.assertEqual((result.turns, result.tool_calls), (5, 5))
        self.assertEqual((result.input_tokens, result.output_tokens), (2500, 500))

    def test_answer_text_blocks_are_joined_and_thinking_is_left_out(self):
        client = FakeClient(reply(thinking(), text("Part one."), text("Part two.")))
        result, _ = run(client)
        self.assertEqual(result.text, "Part one.\nPart two.")
        self.assertEqual((result.turns, result.tool_calls), (1, 0))

    def test_cut_off_answer(self):
        client = FakeClient(reply(text("The cash fl"), stop_reason="max_tokens"))
        with self.assertRaises(extract.ExtractionError) as caught:
            run(client)
        self.assertEqual(str(caught.exception), "The model's answer was cut off before it finished.")

    def test_refusal(self):
        client = FakeClient(reply(stop_reason="refusal"))
        with self.assertRaises(extract.ExtractionError) as caught:
            run(client)
        self.assertEqual(str(caught.exception), "The model declined to answer.")

    def test_each_call_sends_the_tool_and_lets_the_model_choose(self):
        client = FakeClient(reply(tool_use(LISTING_B)), reply(text("Done.")))
        run(client)
        for call in client.calls:
            self.assertEqual(call["tools"], [tools.TOOL_SCHEMA])
            self.assertEqual(call["model"], extract.MODEL)
            self.assertEqual(call["max_tokens"], 2000)
            self.assertEqual(call["system"], agent.SYSTEM_PROMPT)
            self.assertNotIn("tool_choice", call)
            self.assertNotIn("temperature", call)


class SystemPromptTest(unittest.TestCase):
    def test_the_three_rules_are_in_the_prompt(self):
        for sentence in (
            "Use the screen_listing tool for every number you report; never work numbers out yourself.",
            "If the question is missing any of the nine numbers, ask the user for them and do not call the tool.",
            "Explain the result in plain English for a beginner.",
        ):
            self.assertIn(sentence, agent.SYSTEM_PROMPT)


@mock.patch.dict(os.environ, {}, clear=True)
@mock.patch.object(extract, "load_env_file", lambda path=".env": None)  # never read a real .env
class MainTest(unittest.TestCase):
    def main(self, argv, client=None, factory=None):
        printed = []
        code = agent.main(argv, print_fn=printed.append,
                          client_factory=factory or (lambda: client))
        return code, printed

    def test_question_tool_call_answer_and_cost(self):
        client = FakeClient(reply(tool_use(LISTING_B), input_tokens=1000, output_tokens=200),
                            reply(text("It passes: $430.53 a month."), input_tokens=1500, output_tokens=300))
        code, printed = self.main(["Screen", "listing B"], client)
        self.assertEqual(code, 0)
        self.assertTrue(printed[0].startswith("Calling screen_listing with {"))
        self.assertIn("It passes: $430.53 a month.", printed)
        # 2500 input tokens at $0.10 per million plus 500 output at $0.50 per million = $0.0005.
        self.assertEqual(printed[-1], "Used 2500 input and 500 output tokens on Claude in 2 turns, about $0.00050.")
        self.assertEqual(client.calls[0]["messages"][0]["content"], "Screen listing B")

    def test_cap_reached_says_so_and_returns_1(self):
        client = FakeClient(reply(tool_use(LISTING_B)), repeat_last=True)
        code, printed = self.main(["Screen listing B"], client)
        self.assertEqual(code, 1)
        self.assertIn("Stopped after 5 turns without a final answer.", printed)
        self.assertTrue(printed[-1].startswith("Used 2500 input and 500 output tokens on Claude in 5 turns"))

    def test_no_question_shows_usage(self):
        code, printed = self.main([], FakeClient())
        self.assertEqual(code, 2)
        self.assertIn('python3 -m dealscreener.agent "your question"', printed[0])
        code, _ = self.main(["   "], FakeClient())
        self.assertEqual(code, 2)

    def test_no_key_gives_the_week_9_sentence(self):
        code, printed = self.main(["Screen listing B"], factory=extract.make_client)
        self.assertEqual(code, 1)
        self.assertEqual(printed, ["No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README)."])

    def test_api_errors_give_plain_sentences(self):
        for status, sentence in ((401, "The API key was not accepted."), (429, "Too many requests"),
                                 (529, "busy or having a problem")):
            code, printed = self.main(["Screen listing B"], FakeClient(error=FakeAPIError(status)))
            self.assertEqual(code, 1)
            self.assertIn(sentence, printed[-1])

    def test_connection_error(self):
        code, printed = self.main(["Screen listing B"], FakeClient(error=ConnectionError("down")))
        self.assertEqual(code, 1)
        self.assertEqual(printed[-1], "Couldn't reach Anthropic. Check your internet connection.")

    def test_cut_off_answer_gives_the_sentence(self):
        code, printed = self.main(["Screen listing B"], FakeClient(reply(stop_reason="max_tokens")))
        self.assertEqual(code, 1)
        self.assertEqual(printed[-1], "The model's answer was cut off before it finished.")

    def test_env_file_is_loaded_first(self):
        calls = []
        with mock.patch.object(extract, "load_env_file", lambda path=".env": calls.append(path)):
            self.main([], FakeClient())
        self.assertEqual(calls, [".env"])


if __name__ == "__main__":
    unittest.main()
