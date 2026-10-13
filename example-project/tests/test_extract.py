"""Tests for reading a listing with a model. A fake client stands in for Anthropic: no network, no credit."""
import json
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from dealscreener import extract

GOOD = {"purchase_price": 150000, "monthly_rent": 1700, "yearly_property_tax": 2400,
        "yearly_insurance": 1200, "monthly_hoa": 0}


def reply(values, input_tokens=400, output_tokens=60, thinking=True, stop_reason="end_turn"):
    """A fake model reply: an optional thinking block, then the JSON answer in a text block."""
    text = values if isinstance(values, str) else json.dumps(values)
    blocks = [SimpleNamespace(type="text", text=text)]
    if thinking:
        blocks.insert(0, SimpleNamespace(type="thinking", thinking=""))
    return SimpleNamespace(content=blocks, stop_reason=stop_reason,
                           usage=SimpleNamespace(input_tokens=input_tokens, output_tokens=output_tokens))


class FakeClient:
    """Stands in for anthropic.Anthropic(): records each call and returns a set reply."""

    def __init__(self, result=None, error=None):
        self.result, self.error, self.calls = result, error, []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.result


class FakeAPIError(Exception):
    """Like the SDK's API errors: carries the HTTP status code."""

    def __init__(self, status_code, message="error"):
        super().__init__(message)
        self.status_code = status_code


class ExtractListingTest(unittest.TestCase):
    def test_reads_the_five_numbers_and_the_token_counts(self):
        result = extract.extract_listing("a listing", FakeClient(reply(GOOD)))
        self.assertEqual(result.values, {k: float(v) for k, v in GOOD.items()})
        self.assertEqual((result.input_tokens, result.output_tokens), (400, 60))

    def test_a_reply_without_a_thinking_block_works_too(self):
        result = extract.extract_listing("a listing", FakeClient(reply(GOOD, thinking=False)))
        self.assertEqual(result.values["monthly_rent"], 1700.0)

    def test_sends_one_structured_output_call_with_capped_tokens(self):
        client = FakeClient(reply(GOOD))
        extract.extract_listing("a listing", client)
        self.assertEqual(len(client.calls), 1)
        call = client.calls[0]
        self.assertEqual(call["model"], extract.MODEL)
        self.assertEqual(call["max_tokens"], 2000)
        self.assertEqual(extract.MAX_TOKENS, 2000)
        output_format = call["output_config"]["format"]
        self.assertEqual(output_format["type"], "json_schema")
        self.assertEqual(set(output_format["schema"]["properties"]), set(extract.FIELDS))
        self.assertIs(output_format["schema"]["additionalProperties"], False)
        for name in ("temperature", "top_p", "top_k", "tool_choice", "tools"):
            self.assertNotIn(name, call)
        self.assertIn("a listing", str(call["messages"]))
        self.assertTrue(call["system"])

    def test_missing_null_negative_and_text_values_become_none(self):
        odd = {"purchase_price": 150000, "monthly_rent": None, "yearly_property_tax": -5,
               "yearly_insurance": "about 1200"}
        values = extract.extract_listing("x", FakeClient(reply(odd))).values
        self.assertEqual(values["purchase_price"], 150000.0)
        for field in ("monthly_rent", "yearly_property_tax", "yearly_insurance", "monthly_hoa"):
            self.assertIsNone(values[field], field)

    def test_infinite_and_nan_values_become_none(self):
        # json.dumps writes these as Infinity and NaN, which json.loads reads back.
        values = extract.extract_listing("x", FakeClient(reply({"purchase_price": float("inf"),
                                                                "monthly_rent": float("nan")}))).values
        self.assertIsNone(values["purchase_price"])
        self.assertIsNone(values["monthly_rent"])

    def test_a_whole_number_too_big_for_a_float_becomes_none(self):
        # json.loads reads 1 followed by 400 zeros as a Python int that float() can't hold.
        values = extract.extract_listing("x", FakeClient(reply('{"purchase_price": 1' + "0" * 400 + "}"))).values
        self.assertIsNone(values["purchase_price"])

    def test_true_and_false_are_not_numbers(self):
        values = extract.extract_listing("x", FakeClient(reply({"monthly_hoa": True}))).values
        self.assertIsNone(values["monthly_hoa"])

    def test_a_cut_off_reply_is_an_extraction_error(self):
        with self.assertRaises(extract.ExtractionError) as caught:
            extract.extract_listing("x", FakeClient(reply('{"purchase_', stop_reason="max_tokens")))
        self.assertIn("cut off", str(caught.exception))

    def test_a_refusal_is_an_extraction_error(self):
        with self.assertRaises(extract.ExtractionError) as caught:
            extract.extract_listing("x", FakeClient(reply("I can't help with that.", stop_reason="refusal")))
        self.assertIn("declined", str(caught.exception))

    def test_text_that_is_not_json_is_an_extraction_error(self):
        with self.assertRaises(extract.ExtractionError):
            extract.extract_listing("x", FakeClient(reply("The price is $150,000.")))

    def test_json_that_is_not_an_object_is_an_extraction_error(self):
        with self.assertRaises(extract.ExtractionError):
            extract.extract_listing("x", FakeClient(reply([150000, 1700])))

    def test_a_reply_without_a_text_block_is_an_extraction_error(self):
        thinking_only = SimpleNamespace(content=[SimpleNamespace(type="thinking", thinking="")],
                                        usage=SimpleNamespace(input_tokens=1, output_tokens=1),
                                        stop_reason="end_turn")
        with self.assertRaises(extract.ExtractionError):
            extract.extract_listing("x", FakeClient(thinking_only))


class DescribeErrorTest(unittest.TestCase):
    def test_each_status_gets_its_own_plain_sentence(self):
        cases = {400: "couldn't read the request", 401: "not accepted", 402: "credit has run out",
                 403: "isn't allowed", 404: "model name", 413: "too long", 429: "Wait a minute",
                 500: "busy", 529: "busy", 418: "call to the model failed"}
        for status, words in cases.items():
            self.assertIn(words, extract.describe_error(FakeAPIError(status)), status)

    def test_any_5xx_means_busy(self):
        for status in (502, 503, 504):
            self.assertIn("busy", extract.describe_error(FakeAPIError(status)), status)

    def test_a_key_without_a_workspace_is_named(self):
        message = extract.describe_error(FakeAPIError(
            400, "This API key is not scoped to a workspace, so this request must include the "
                 "anthropic-workspace-id header"))
        self.assertIn("isn't tied to a workspace", message)

    def test_low_credit_is_named(self):
        message = extract.describe_error(FakeAPIError(400, "Your credit balance is too low"))
        self.assertIn("credit has run out", message)

    def test_your_own_spend_limit_is_named(self):
        for text in ("You have reached your specified API usage limits. You will regain access on 2026-11-01.",
                     "You have reached your specified workspace API usage limits."):
            message = extract.describe_error(FakeAPIError(400, text))
            self.assertIn("spend limit has been reached", message)
            self.assertNotIn("2026-11-01", message)

    def test_no_status_means_the_network(self):
        self.assertIn("reach Anthropic", extract.describe_error(ConnectionError("down")))

    def test_the_key_never_appears_in_a_message(self):
        key = "sk-ant-test-secret-123"
        for status in (None, 400, 401, 402, 403, 404, 413, 429, 500, 529, 418):
            error = FakeAPIError(status, f"bad key {key}") if status else ConnectionError(f"key {key}")
            self.assertNotIn(key, extract.describe_error(error))


class MakeClientTest(unittest.TestCase):
    def test_no_key_says_how_to_add_one(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(extract.ExtractionError) as caught:
                extract.make_client()
        self.assertIn("No API key found", str(caught.exception))

    def test_missing_package_says_how_to_install_it(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-x"}), \
             mock.patch.dict("sys.modules", {"anthropic": None}):
            with self.assertRaises(extract.ExtractionError) as caught:
                extract.make_client()
        self.assertIn("pip install -r requirements.txt", str(caught.exception))
        self.assertNotIn("sk-ant-x", str(caught.exception))


class LoadEnvFileTest(unittest.TestCase):
    def test_reads_keys_skips_comments_and_keeps_existing_values(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, ".env")
            with open(path, "w") as f:
                f.write("# my key\n\nANTHROPIC_API_KEY=\"sk-ant-from-file\"\nOTHER=1\nSINGLE='x y'\n")
            with mock.patch.dict(os.environ, {"OTHER": "kept"}, clear=True):
                extract.load_env_file(path)
                self.assertEqual(os.environ["ANTHROPIC_API_KEY"], "sk-ant-from-file")
                self.assertEqual(os.environ["OTHER"], "kept")
                self.assertEqual(os.environ["SINGLE"], "x y")

    def write_env(self, folder, text, encoding="utf-8"):
        path = os.path.join(folder, ".env")
        with open(path, "w", encoding=encoding) as f:
            f.write(text)
        return path

    def test_a_file_saved_with_a_byte_order_mark_still_works(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_env(folder, "ANTHROPIC_API_KEY=sk-ant-bom\n", encoding="utf-8-sig")
            with mock.patch.dict(os.environ, {}, clear=True):
                extract.load_env_file(path)
                self.assertEqual(os.environ.get("ANTHROPIC_API_KEY"), "sk-ant-bom")

    def test_export_in_front_and_a_note_after_are_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_env(folder, "export ANTHROPIC_API_KEY=sk-ant-exp # my key\nQUOTED=\"a # b\"\n")
            with mock.patch.dict(os.environ, {}, clear=True):
                extract.load_env_file(path)
                self.assertEqual(os.environ.get("ANTHROPIC_API_KEY"), "sk-ant-exp")
                self.assertEqual(os.environ.get("QUOTED"), "a # b")

    def test_a_missing_file_does_nothing(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            extract.load_env_file("/no/such/.env")
            self.assertNotIn("ANTHROPIC_API_KEY", os.environ)


class CostTest(unittest.TestCase):
    def test_cost_uses_the_published_prices(self):
        expected = (1_000_000 * extract.PRICES_PER_MILLION["input"]
                    + 1_000_000 * extract.PRICES_PER_MILLION["output"]) / 1e6
        self.assertAlmostEqual(extract.cost_usd(1_000_000, 1_000_000), expected)
        self.assertEqual(extract.cost_usd(0, 0), 0)

    def test_haiku_prices_from_the_pricing_page(self):
        self.assertEqual(extract.MODEL, "claude-haiku-5-5")
        self.assertEqual(extract.PRICES_PER_MILLION, {"input": 0.10, "output": 0.50})


if __name__ == "__main__":
    unittest.main()
