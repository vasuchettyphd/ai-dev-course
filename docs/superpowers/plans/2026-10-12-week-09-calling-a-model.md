# Week 9 (Calling a model from code) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 9. Students:
- learn what changes when their own code calls a model: API credit separate from Claude Pro, tokens, and the cost of one call
- make an Anthropic Console account, buy credit, set a spend limit, and put an API key in `.env` themselves, never in a chat
- make a first call from a scratch folder with the official Python SDK in a virtual environment, read the token usage and work out the cost by hand
- learn the settings that matter: system prompt, temperature, `max_tokens`, structured output, and choosing a model
- add one AI feature to `semester-project` on branch `ai-feature`, with offline tests and a working fallback when there is no key
- review it with `safe-and-private`, run it in Docker with `--env-file .env`, and merge through a PR

The week also gives the deal screener an optional "paste the listing" step (tag `week-09`) and adds slides, the assignment, instructor notes with a demo script, and checklist rows.

**Architecture:**
- Same approach as weeks 2-8.
- Facts come from Anthropic's official docs: the API overview, getting started, the Python SDK README, models overview (IDs, prices, context), pricing, tool use (forced `tool_choice`), structured outputs if available, temperature and `max_tokens`, errors and status codes, rate limits, Console spend limits and billing, and API key safety. All are recorded on a fact sheet with URLs.
- Live calls use a course key with a low spend limit that the user puts in `~/claude/ai-dev-course/.env` (git-ignored). Nothing reads, prints or copies that file except the program, through the environment. If the key isn't there when Task 2 needs it, the controller asks the user, and live numbers are marked "being tested" until it is.
- The deal screener stays usable without the SDK, without a key, and offline. Its tests use a fake client and never spend credit. One live test runs only when it is asked for.

**Tech Stack:** Markdown, Marp (`npm run slides` in Docker), Python 3.9+ (standard library for the program's own logic), the official `anthropic` Python SDK (pinned in `requirements.txt`), Docker Engine for the container check, Anthropic API (a Haiku model).

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 9 row ("Calling a model from code | API keys, tokens, cost, temperature, structured output, choosing a model | Add one AI feature"), the student cost line (about $5 of one-time API credit), and the out-of-scope line (fine-tuning mentioned as an option students rarely need, not taught). The week 9 design was approved in conversation on 2026-10-12. Decisions:
- Provider: the Anthropic API for weeks 9-11.
- Live testing uses a course key the user adds to `~/claude/ai-dev-course/.env`.
- The deal screener's feature: paste the listing text, Haiku extracts the five property numbers as structured output, the user confirms or retypes each one, and the existing maths runs unchanged. With no key or a failed call, it says so and falls back to typing.
- Assignment: merged AI feature PR with offline tests including a no-key test 4, cost log of 3 real calls 2, screenshot of the feature working plus the no-key fallback 2, reflection on model and temperature choice 2.

## Global Constraints

- Audience: business and non-CS students in week 9. They have Claude Code, git, `gh`, Superpowers, the week 6 reviewers, Docker Desktop, and a merged version 1 of private `semester-project` with tests. Their projects may not be Python. Plain language. Every command and prompt is shown exactly and labelled with where to type it: Terminal, the Ubuntu window, a text editor, or inside Claude Code.
- Platforms: Mac (Apple chip), Mac (Intel) and Windows (WSL 2 Ubuntu). The virtual environment and `pip install` steps are shown for each; on Windows they run in the Ubuntu window. Any extra package Ubuntu needs (for example `python3-venv`) comes from the fact sheet's dry run.
- **Key safety, non-negotiable:**
  - students create the key in the Console and type or paste it into `.env` with a text editor themselves
  - never paste a key into Claude Code, any chat, a screenshot, a commit or a PR
  - check `.env` is ignored by git (`git check-ignore .env`) before the first commit that follows
  - the program reads the key only from the environment and never prints it, even in error messages
  - Docker gets the key with `--env-file .env` at run time; `.env` never goes into the image
  - a leaked key is revoked in the Console first, then cleaned up
  - set a monthly spend limit before making calls
- Cost: every price, limit and model ID comes from Anthropic's pages on the fact sheet, with the date read. No invented numbers. Cost per call is worked out from the reply's `usage` and the published per-million-token prices.
- Git rules from weeks 3-8:
  - make a branch before Claude changes anything
  - never change `main`
  - push and open a PR, read Files changed, merge on GitHub, then pull
  - the repo stays private
  - plain "Yes" for git prompts
  - "No" to `reset --hard`, `--force`, `git clean` and `rm -rf`
  - the week 5 rescue (`#if-it-committed-to-main`) for work committed to `main`
- Tests for an AI feature never call the real API by default. A live test, if any, runs only when the student asks for it.
- Every fact comes from the fact sheet with its URL. Anything not observed is marked "being tested". Pin the versions tested (SDK version, model ID).
- No em dashes (U+2014) or en dashes (U+2013). The rubric is a table under `## Rubric` with points in the last column, totalling 10.
- `example-project/` stays the labelled instructor example. It passes `scripts/check_course.py`, and its offline tests run with `python3 -m unittest` on the host (with or without the SDK installed) and in the container.
- Instructor-only material goes in the private repo.
- Branch `week-09-calling-a-model` in the course repo and `week-09` in the instructor repo. The user merges. Links come first, one bare URL per line.

## Review Focus

1. **The key leaks.** It could be committed in `.env`, copied into the image, printed in an error or traceback, or pasted into Claude Code. `.gitignore` and `.dockerignore` already list `.env`. Task 2 adds a test that no error message contains the key, and checks the image has no `.env`. The README has students run `git check-ignore .env` and `git status` before committing.
2. **The model returns wrong, missing or absurd numbers.** A missing field, `null`, a negative or huge value, text instead of a number, or yearly rent instead of monthly. Every extracted number is shown and confirmed by the user, and goes through the existing `parse_answer` checks. A missing or invalid value is asked for normally. Task 2 tests each case.
3. **The call fails:** no SDK installed, no key, a bad key (401), rate limit (429), out of credit, model not found (404), API overloaded (529 or other 5xx), or the network is down. The program says what happened in one plain sentence and falls back to typing the numbers, with no traceback. Task 2 tests each case with a fake client.
4. **The pasted text is awkward:** blank lines inside it, a very long paste, nothing useful in it, or end of input while pasting. Pasting ends with a line containing only `done`. Blank lines are kept. Text over the limit is refused before any call. End of input stops politely. Task 2 tests each case.
5. **Cost surprises.** `max_tokens` is capped, the model is Haiku, the paste is limited in length, the tokens and estimated cost are printed after each call, and the README has students set a spend limit first. Task 2 tests the cost arithmetic against the fact sheet prices.

---

### Task 1: Fact sheet and dry run

**Files:** none in the repo. Write the report only.

- [ ] **Step 1:** Record each fact with its URL and the date read:
  - **Account and money:**
    - how to make a Console account
    - how to buy credit, and the minimum purchase
    - how to set a monthly spend limit, and what happens when it is reached
    - where usage and cost are shown
    - whether Claude Pro includes API credit (it is expected not to; quote the source)
  - **Keys:**
    - how to create and name a key, and whether it is shown once
    - how to revoke a key
    - the environment variable the SDK reads (`ANTHROPIC_API_KEY`)
    - Anthropic's guidance on keeping keys safe
  - **Python SDK:**
    - package name, install command, current version and minimum Python version
    - the minimal example from the docs, exactly
    - the reply's shape: `content` blocks, `usage.input_tokens`, `usage.output_tokens`, `stop_reason`
    - the exception classes and their `status_code` values
  - **Other SDKs**, for students whose project isn't Python: the official TypeScript/JavaScript SDK name and install command, and the list of other official SDKs.
  - **Models:**
    - the current Haiku, Sonnet and Opus model IDs and aliases
    - input and output prices per million tokens
    - context window and maximum output
    - Anthropic's own guidance on which model to choose
  - **Settings:**
    - `system`
    - `temperature`: its range and default, and whether any current model restricts it (quote it exactly if so)
    - `max_tokens`, and what `stop_reason` says when it is hit
  - **Structured output:**
    - forced tool use: `tools` with `input_schema`, `tool_choice` `{"type": "tool", "name": ...}`, and reading the `tool_use` block's `input`
    - whether a separate structured outputs feature exists, is GA or beta, and which models support it
    - which of the two the course should teach (record the reason)
  - **Errors:** the documented HTTP status codes and error types (400, 401, 403, 404, 413, 429, 500, 529), and the exact message or type for a credit balance that is too low, if documented.
  - **Rate limits:** the tier a new account starts on, in general terms from the docs.
  - **Fine-tuning:** one sourced sentence on whether and where Anthropic offers it, for the "rarely needed" mention.
- [ ] **Step 2: Dry run in a clean `ubuntu:24.04` container, as a non-root user:**
  - `python3 -m venv .venv` (record whether `python3-venv` must be installed first, and the exact apt package and message)
  - `source .venv/bin/activate`
  - `pip install anthropic==<current version>`
  - `python -c "import anthropic; print(anthropic.__version__)"`
  - run the docs' minimal example with no key set, and record the exact error
  - never enter a key in the container
- [ ] **Step 3: Live check, only if `~/claude/ai-dev-course/.env` exists:**
  - Load it into the environment of one command only, without printing it: `set -a; . ~/claude/ai-dev-course/.env; set +a; python ...`.
  - Run the minimal example with the Haiku ID from Step 1 and record the reply's `usage` and the model ID it echoes.
  - Make one forced tool-use call and record the `tool_use` block shape.
  - Make one call with an invalid key, `ANTHROPIC_API_KEY=sk-ant-invalid python ...`, and record the exception class, `status_code` and message.
  - Record the total cost of these calls from `usage` and the published prices.
  - If the file doesn't exist, mark each live item "being tested" and say so in the report.
- [ ] **Step 4:** Write the report: facts, transcripts, versions (SDK, Python, model IDs) and the date. Never write the key, or any part of it, into the report.

### Task 2: Deal screener "paste the listing" step (example-project)

**Files:**
- Create: `example-project/dealscreener/extract.py`, `example-project/tests/test_extract.py`, `example-project/tests/test_live.py`, `example-project/requirements.txt`, `example-project/listings/listing-b.txt`, `example-project/listings/messy-listing.txt`, `example-project/.env.example`
- Modify: `example-project/dealscreener/__main__.py` (an optional listing step behind `--listing`), `example-project/tests/test_main.py` (new tests for the listing step), `example-project/Dockerfile` (`pip install -r requirements.txt`), `example-project/.dockerignore` (keep `.env` out, already there; add `listings/` only if the program doesn't need it at run time), `example-project/README.md` (a "What's here now (week 9)" section, the week 9 row in "How it grows", "How to use the listing step" with the key setup, the Docker run with `--env-file`, and a cost record)

**Interfaces (quoted by the README and slides):**
- **`dealscreener/extract.py`** (standard library only at import time; `anthropic` is imported only inside `make_client`):
  - `MODEL = "<the Haiku model ID from the fact sheet>"`, `MAX_TOKENS = 300`, `MAX_LISTING_CHARS = 20000`
  - `PRICES_PER_MILLION = {"input": <fact sheet>, "output": <fact sheet>}` for `MODEL`, with a comment giving the pricing page URL and the date read
  - `FIELDS`: the five property fields in the program's order, `purchase_price`, `monthly_rent`, `yearly_property_tax`, `yearly_insurance`, `monthly_hoa`
  - `class ExtractionError(Exception)`: its message is one plain-English sentence for the user, and never contains the key
  - `@dataclass class Extraction: values: dict` (field -> float or None), `input_tokens: int`, `output_tokens: int`
  - `load_env_file(path=".env") -> None`: reads `KEY=VALUE` lines (ignores blank lines and `#` comments, strips optional quotes), and sets only variables not already set in `os.environ`. A missing file does nothing.
  - `make_client()`:
    - If `ANTHROPIC_API_KEY` is not set, raises `ExtractionError("No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README); for now, type the numbers yourself.")`.
    - If `anthropic` can't be imported, raises `ExtractionError("The anthropic package isn't installed (pip install -r requirements.txt); for now, type the numbers yourself.")`.
    - Otherwise returns `anthropic.Anthropic()`.
  - `extract_listing(text: str, client, model: str = MODEL) -> Extraction`:
    - One `client.messages.create(...)` call with `model`, `max_tokens=MAX_TOKENS`, `temperature=0` (unless the fact sheet says the model forbids it), a short `system` prompt, and the listing text as the user message.
    - It forces one tool, `record_listing`, whose `input_schema` has the five fields, each `{"type": ["number", "null"], "description": ...}`. The descriptions say "monthly" or "yearly" and tell the model to use null when the listing doesn't say.
    - It reads the first `tool_use` block's `input`. Values that are not finite non-negative numbers become `None`.
  - `describe_error(error) -> str`: maps an exception to a plain sentence by `getattr(error, "status_code", None)`. No `status_code` means "Couldn't reach Anthropic. Check your internet connection." The message never includes `str(error)` if that could contain the key; use fixed sentences only:
    - 400 with "credit" in the message: "Your API credit has run out. Add credit in the Anthropic Console."
    - other 400: "Anthropic couldn't read the request."
    - 401: "The API key was not accepted. Check the key in your .env file."
    - 403: "This API key isn't allowed to do that."
    - 404: "The model name wasn't found."
    - 413: "The listing text is too long."
    - 429: "Too many requests or tokens for now. Wait a minute and try again."
    - 500 and 529: "Anthropic's service is busy or having a problem. Try again later."
    - anything else: "The call to the model failed."
    - The caller appends " For now, type the numbers yourself."
  - `cost_usd(input_tokens: int, output_tokens: int) -> float` = `input_tokens * input_price / 1e6 + output_tokens * output_price / 1e6`
- **`__main__.py`:**
  - `run(input_fn=input, print_fn=print, use_listing=False, client_factory=None) -> int`. With `use_listing=False` it behaves exactly as now (every existing test passes unchanged). `client_factory` defaults to `extract.make_client`.
  - `python3 -m dealscreener --listing` turns the step on: `if __name__ == "__main__": raise SystemExit(run(use_listing="--listing" in sys.argv[1:]))`, after `extract.load_env_file()`.
  - **The listing step**, before the property questions:
    1. Print "Paste the listing text, then type done on a line by itself and press Enter. To skip and type the numbers yourself, type done now."
    2. Read lines with `input_fn("")` until a line whose stripped text is `done` (any case). Blank lines are kept.
    3. An empty paste skips the step. A paste longer than `MAX_LISTING_CHARS` prints "That listing is too long (over 20,000 characters). Type the numbers yourself." and skips the step.
    4. Otherwise print "Asking the model to read the listing...", call `client_factory()` then `extract_listing(text, client)`, and print "Used {in} input and {out} output tokens, about ${cost:.4f}."
    5. Any exception from the factory or the call prints `describe_error(...)` (for `ExtractionError`, its own message) plus " For now, type the numbers yourself.", and the step ends.
    6. End of input while pasting goes to the existing "Stopped before all the numbers were typed." path.
  - **Confirming numbers:**
    - For each property field with an extracted value, the prompt becomes the usual prompt with the value shown: `"Purchase price ($) [from the listing: 150000]: "` (formatted with `:g`).
    - Pressing Enter on a blank answer accepts the value, which still goes through `parse_answer` with that field's kind. If it fails the check, print the problem and ask normally.
    - Typing a number replaces it.
    - Fields with `None` are asked normally.
    - Loan questions are always asked normally.
  - Helper: `ask_with_default(prompt, kind, default, input_fn, print_fn)`.
- **`requirements.txt`:** `anthropic==<the version tested in Task 1>` with a comment line.
- **`.env.example`:** `ANTHROPIC_API_KEY=put-your-key-here` with a comment saying to copy it to `.env` and never commit `.env`.
- **Dockerfile:**
  - Before `COPY . .`, add `COPY requirements.txt .` and `RUN pip install --no-cache-dir -r requirements.txt`, with plain-English comments. Replace week 7's "No package install step" comment.
  - The run command for the listing step: `docker run -it --rm --env-file .env dealscreener python -m dealscreener --listing`.
- **`listings/listing-b.txt`:** a realistic listing description in prose whose numbers are listing B's property numbers ($150,000 price, $1,700 a month rent, $2,400 a year tax, $1,200 a year insurance, no HOA), with blank lines between paragraphs and some numbers that are not inputs (bedrooms, square feet, year built).
- **`listings/messy-listing.txt`:**
  - the HOA given monthly
  - the tax given monthly ($200 a month) so the model must convert it, or the user must notice
  - no insurance figure, which must come back null
  - a distracting "price reduced from $165,000"

**Tests (`tests/test_extract.py`, offline, no SDK needed):**

```python
"""Tests for reading a listing with a model. A fake client stands in for Anthropic: no network, no credit."""
import os
import unittest
from types import SimpleNamespace
from unittest import mock

from dealscreener import extract

GOOD = {"purchase_price": 150000, "monthly_rent": 1700, "yearly_property_tax": 2400,
        "yearly_insurance": 1200, "monthly_hoa": 0}


def reply(tool_input, input_tokens=400, output_tokens=60):
    block = SimpleNamespace(type="tool_use", name="record_listing", input=tool_input)
    return SimpleNamespace(content=[block], usage=SimpleNamespace(input_tokens=input_tokens, output_tokens=output_tokens),
                           stop_reason="tool_use")


class FakeClient:
    def __init__(self, result=None, error=None):
        self.result, self.error, self.calls = result, error, []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.result


class FakeAPIError(Exception):
    def __init__(self, status_code, message="error"):
        super().__init__(message)
        self.status_code = status_code


class ExtractListingTest(unittest.TestCase):
    def test_reads_the_five_numbers_and_the_token_counts(self):
        result = extract.extract_listing("a listing", FakeClient(reply(GOOD)))
        self.assertEqual(result.values, {k: float(v) for k, v in GOOD.items()})
        self.assertEqual((result.input_tokens, result.output_tokens), (400, 60))

    def test_sends_one_forced_tool_call_with_capped_tokens(self):
        client = FakeClient(reply(GOOD))
        extract.extract_listing("a listing", client)
        call = client.calls[0]
        self.assertEqual(call["model"], extract.MODEL)
        self.assertEqual(call["max_tokens"], extract.MAX_TOKENS)
        self.assertEqual(call["tool_choice"], {"type": "tool", "name": "record_listing"})
        self.assertEqual(set(call["tools"][0]["input_schema"]["properties"]), set(extract.FIELDS))
        self.assertIn("a listing", str(call["messages"]))

    def test_missing_null_negative_and_text_values_become_none(self):
        odd = {"purchase_price": 150000, "monthly_rent": None, "yearly_property_tax": -5,
               "yearly_insurance": "about 1200"}
        values = extract.extract_listing("x", FakeClient(reply(odd))).values
        self.assertEqual(values["purchase_price"], 150000.0)
        for field in ("monthly_rent", "yearly_property_tax", "yearly_insurance", "monthly_hoa"):
            self.assertIsNone(values[field], field)

    def test_infinite_and_nan_values_become_none(self):
        values = extract.extract_listing("x", FakeClient(reply({"purchase_price": float("inf"),
                                                                "monthly_rent": float("nan")}))).values
        self.assertIsNone(values["purchase_price"])
        self.assertIsNone(values["monthly_rent"])

    def test_a_reply_without_a_tool_block_is_an_extraction_error(self):
        text_only = SimpleNamespace(content=[SimpleNamespace(type="text", text="hi")],
                                    usage=SimpleNamespace(input_tokens=1, output_tokens=1), stop_reason="end_turn")
        with self.assertRaises(extract.ExtractionError):
            extract.extract_listing("x", FakeClient(text_only))


class DescribeErrorTest(unittest.TestCase):
    def test_each_status_gets_its_own_plain_sentence(self):
        cases = {401: "not accepted", 403: "isn't allowed", 404: "model name", 413: "too long",
                 429: "Wait a minute", 500: "busy", 529: "busy"}
        for status, words in cases.items():
            self.assertIn(words, extract.describe_error(FakeAPIError(status)), status)

    def test_low_credit_is_named(self):
        message = extract.describe_error(FakeAPIError(400, "Your credit balance is too low"))
        self.assertIn("credit has run out", message)

    def test_no_status_means_the_network(self):
        self.assertIn("reach Anthropic", extract.describe_error(ConnectionError("down")))

    def test_the_key_never_appears_in_a_message(self):
        key = "sk-ant-test-secret-123"
        for status in (None, 400, 401, 403, 404, 413, 429, 500, 529, 418):
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


class LoadEnvFileTest(unittest.TestCase):
    def test_reads_keys_skips_comments_and_keeps_existing_values(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, ".env")
            with open(path, "w") as f:
                f.write('# my key\n\nANTHROPIC_API_KEY="sk-ant-from-file"\nOTHER=1\n')
            with mock.patch.dict(os.environ, {"OTHER": "kept"}, clear=True):
                extract.load_env_file(path)
                self.assertEqual(os.environ["ANTHROPIC_API_KEY"], "sk-ant-from-file")
                self.assertEqual(os.environ["OTHER"], "kept")

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
```

**Tests added to `tests/test_main.py`** (new class `ListingStepTest`, using `FakeConsole` and the fakes above imported from `tests.test_extract`):
- `test_without_the_flag_nothing_changes`: `run_with(LISTING_B)` output is unchanged (the existing tests already pin this; assert no prompt mentions "Paste").
- `test_pasted_listing_values_are_confirmed_with_enter`:
  - `use_listing=True`, a fake factory returning `FakeClient(reply(GOOD))`, answers `["line one", "", "line two", "done", "", "", "", "", "", "25", "7", "30", "6000"]`
  - the report's last 9 lines equal listing B's
  - the prompt `"Purchase price ($) [from the listing: 150000]: "` was shown
  - "Used 400 input and 60 output tokens" is printed
  - the client received the text "line one\n\nline two"
- `test_typing_a_number_replaces_the_listing_value`: type `160000` at the price prompt, and the report's mortgage changes accordingly.
- `test_missing_values_are_asked_normally`: the fake returns `monthly_hoa: None`, and the HOA prompt has no "[from the listing" part.
- `test_an_extracted_value_that_fails_the_checks_is_asked_again`: the fake returns a price of `0` (it becomes 0.0, not None). Pressing Enter shows "The purchase price must be more than 0." and asks again.
- `test_skip_with_done_makes_no_call`: answers start `["done", ...]` plus listing B, and the factory is never called.
- `test_no_key_falls_back_to_typing`: the factory raises `ExtractionError("No API key found. ...")`, the message and " For now, type the numbers yourself." are printed, and listing B's report follows.
- `test_api_errors_fall_back_without_a_traceback`: for 401, 429 and a `ConnectionError`, the fallback sentence is printed and the exit code is 0.
- `test_too_long_paste_makes_no_call`: one line of 20,001 characters, then `done`, prints "That listing is too long" and the factory is not called.
- `test_running_out_of_input_while_pasting_stops_politely`: answers `["only a line"]`, exit code 1, and "Stopped before all the numbers were typed." is printed.
- `test_done_is_case_and_space_insensitive`: `"  DONE "` ends the paste.

**Live test (`tests/test_live.py`):** `@unittest.skipUnless(os.environ.get("RUN_LIVE_TESTS") == "1" and os.environ.get("ANTHROPIC_API_KEY"), "live test: set RUN_LIVE_TESTS=1 and a key")`. It reads `listings/listing-b.txt`, calls `extract_listing` with `make_client()`, and asserts the five values match listing B (within 1 dollar) and both token counts are positive.

- [ ] **Step 1:** Write `listings/`, `.env.example` and `requirements.txt`.
- [ ] **Step 2:** Write `tests/test_extract.py`, run it and watch it fail (no `extract` module).
- [ ] **Step 3:** Write `dealscreener/extract.py` with the fact sheet's model ID and prices, then run `python3 -m unittest tests.test_extract -v` until it passes. It must pass without `anthropic` installed: run it with plain `python3` outside any venv.
- [ ] **Step 4:** Write the `ListingStepTest` tests, watch them fail, change `__main__.py`, and run them until they pass. Run the whole suite: `python3 -m unittest`, every old test unchanged and passing. Record the total.
- [ ] **Step 5: Live run.** Only if `~/claude/ai-dev-course/.env` exists. Load it for one command only, and never print it:
  - Run `RUN_LIVE_TESTS=1 python -m unittest tests.test_live -v` in a venv with `requirements.txt` installed.
  - Pipe `listings/listing-b.txt` plus `done` and the confirmations into `python -m dealscreener --listing`, and record the output.
  - Do the same with `messy-listing.txt`, and record what the model returned for each field, including whether it converted the monthly tax and left insurance null.
  - Record the tokens and cost of each call in the report and in the example README's cost record.
  - If the key isn't there, mark the cost record "being tested" and tell the controller.
- [ ] **Step 6: Container:**
  - `docker build -t dealscreener-w9 .`
  - `docker run --rm dealscreener-w9 python -m unittest` must pass.
  - `docker run --rm dealscreener-w9 ls -a /app` shows no `.env`.
  - With the key: `docker run -i --rm --env-file <course .env path> dealscreener-w9 python -m dealscreener --listing < input.txt` gives the same report as the host.
  - Remove the image.
- [ ] **Step 7:** Update the example README and `.dockerignore`. Run `python3 scripts/check_course.py` from the repo root and check it prints OK. Check there are no dashes. Run `git status` and `git check-ignore -v .env` to prove no `.env` is staged. Commit on `week-09-calling-a-model`.

### Task 3: README, slides and assignment

**Files:** `weeks/09-calling-a-model/README.md` (replace the stub, starting from `templates/README.md`), `slides.md`, `slides.pdf`, `assignment.md`.

- [ ] **README:** follow the approved design, steps 1-7:
  1. **What changes this week:**
     - your code calls a model, which costs API credit separate from Claude Pro
     - tokens in and out
     - the cost of one call, worked from the deal screener's real numbers (or "being tested")
  2. **Get a key safely (before class):**
     - Console account, buying credit, setting a spend limit
     - creating a key and putting it in `.env` with a text editor (TextEdit in plain-text mode on a Mac, `nano` in the Ubuntu window on Windows, or the editor the fact sheet supports)
     - `git check-ignore .env`
     - the key rules, as a box
     - what to do if a key leaks
  3. **First call** in a scratch folder (`~/first-call`), not `semester-project`:
     - venv and `pip install` for each platform
     - the docs' minimal example, run with the key loaded from `.env`
     - reading `usage`
     - working out the cost by hand
  4. **The settings that matter:**
     - system prompt
     - temperature: run the same prompt 3 times at 0 and at 1 and compare
     - `max_tokens` and `stop_reason`
     - structured output with forced tool use (or the structured outputs feature, as the fact sheet decided)
     - a model-choice table (ID, price in and out, when to use it)
     - one sentence on fine-tuning
  5. **Add one AI feature to `semester-project`:**
     - branch `ai-feature` first
     - three example feature ideas for business projects
     - the Superpowers prompt, with the guardrails written into it: key from the environment only, works without a key, errors handled, offline tests with a fake model, a live test only on request, `requirements.txt` (or the stack's equivalent) pinned, a cost line printed
     - Yes/No rules: No to putting the key in code, No to tests that call the API by default, No to printing the key
     - students whose project isn't Python: the official SDK for their language from the fact sheet
  6. **Review and run:**
     - `safe-and-private` scoped to the new feature and `.env` handling
     - Docker with `--env-file .env`, checking no `.env` is in the image
     - push, open a PR, read Files changed (no `.env`), merge, then pull
  7. **Check it worked, and troubleshooting:**
     - 401
     - 403
     - 404 model not found
     - 429
     - credit too low
     - 529 overloaded
     - `ModuleNotFoundError: anthropic` (the venv isn't active)
     - `python3 -m venv` fails on Ubuntu
     - the key isn't found (`.env` is in the wrong folder, or not loaded)
     - the key was committed (revoke first)
     - a big bill (spend limit)
     - the model's numbers are wrong (that's why you confirm)
     - the week 5 rescue

  Mark everything not observed "being tested". Give versions in "Tested with".
- [ ] **Slides:** 16-20 slides matching the README, including:
  - "Claude Pro vs API credit"
  - a token and cost worked example
  - the key rules
  - the temperature comparison
  - the deal screener's tool schema
  - the listing step's confirm prompt

  Build with `npm run slides`, restore every other week's PDF, then render the slides and look at them.
- [ ] **Assignment:**
  - **Hand in:**
    - the merged PR URL
    - a cost log of 3 real calls: tokens in, tokens out, the cost worked out, and the Console usage page screenshot that matches it (crop out anything secret)
    - screenshots of the feature working and of the no-key fallback
    - the reflection
  - **Rubric:**
    - Merged AI feature PR with offline tests, including a no-key test; no key in the repo. 4 points.
    - Cost log of 3 real calls, worked out from `usage`. 2 points.
    - Screenshots of the feature working and the no-key fallback. 2 points.
    - Reflection: which model and temperature you chose, and why. 2 points.
    - Total: 10 points.
- [ ] **Checks:** `python3 scripts/check_course.py` prints OK. No dashes. A command-to-source table in the report.

### Task 4: Instructor notes, demo script and checklist rows (private repo)

- [ ] `weeks/09-calling-a-model/notes.md` with the four headings:
  - **Timing:** a 75-minute plan. The key setup happens before class, with a pre-class email.
  - **Common problems:**
    - no card, or can't buy credit. Say this is the instructor's decision, give the options without inventing a policy, and mark it "decide before class".
    - keys pasted into chats or screenshots
    - keys committed
    - venv not active
    - Ubuntu missing `python3-venv`
    - projects that aren't Python
    - 429 in a full classroom on one network or account tier
    - students whose tests call the real API
    - unexpected cost
  - **Discussion answers.**
  - **Grading guidance:**
    - worked 10/10 and 6/10 examples that add up
    - how to check a PR for a key: search the diff and the history
    - how to check that tests run offline: unset the key and run them
  - Also a **demo script:** add the listing step to the deal screener live from a scratch clone at tag `week-08`, with the exact prompts and commands, about 20 minutes, the instructor's own key loaded from `.env` and never shown on screen, and a fallback to the tagged `week-09` files.
- [ ] `weeks/09-calling-a-model/test-checklist.md`: Mac (Apple chip), Mac (Intel) and Windows rows for every README step and troubleshooting row, with identical numbering, in the same format as week 8.
- [ ] No dashes. No key in any file. Commit on `week-09`.

### Task 5: PRs, tag and tracking (controller)

- [ ] Before pushing, check both branches for anything that looks like a key: `git log -p main..HEAD | grep -nE "sk-ant-[A-Za-z0-9_-]{10,}"` should find nothing beyond the obvious test fakes (`sk-ant-test-secret-123`, `sk-ant-x`, `sk-ant-from-file`, `sk-ant-invalid`).
- [ ] Push both branches and open the PRs. Links come first, and ask for a merge commit.
- [ ] After merge, tag `week-09`, close the OpenProject task, and delete the branches and the workspace.
