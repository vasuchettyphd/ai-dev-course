# Week 9 on the Gemini path

This page is for students on the **Gemini path**: no API credit. You set it up this week. You told your instructor before class and the department couldn't fund credit on your own account, so you do the same week with Google's **free tier** and the model `gemini-3.5-flash-lite` instead of Claude Haiku 5.5. Never use someone else's key, Anthropic or Google.

You must be **18 or older**: Google says "You must be 18 years of age or older to use the APIs." Under 18 with no card? Talk to your instructor: there's an offline version of this week.

**On the free tier, Google uses what you send, and human reviewers may read it** (week 10 step 2c quotes Google's terms). Send only course-safe data. Anything you type into AI Studio's web page is on the free tier too, so keep that course-safe as well.

## What changes and what doesn't

**Changes:**

- You call Google's model with Google's package, `google-genai`, using a **Google key** (`GEMINI_API_KEY`). You get it this week, by following week 10's key steps early.
- Your calls cost **$0**. You still work out what each call **would** cost on Google's paid tier, so you learn the arithmetic.
- **Privacy:** see the note above. It covers everything your program sends in weeks 9 to 12: no personal, customer or real business data.
- No Console, no credit and no spend limit. Instead: **don't add billing** to your Google account for this course. Google's free tier has limits per minute and per day; if you hit one, you get error 429: wait and try again.
- The deal screener's AI steps use Claude, so where the README runs them with a Claude key, you read the README's recorded output instead.

**Doesn't change:** everything else. Same project, same feature, same branch, same Superpowers steps, same tests with a fake model, same Docker steps, same pull request. Claude Code itself still uses your Claude Pro login, not API credit. And **the key rules** still apply, with these swaps:

- Rule 5 (spend limit) becomes: never add billing for this course.
- Rule 6 becomes: if a key leaks, **delete it in AI Studio first** (week 10 step 2e), then clean up.
- Wherever the README says "anything starting `sk-ant-`", read "anything starting `sk-ant-` or `AIza`" (Google keys usually start with `AIza`; the course's test key did).

The steps below are keyed to the README's step numbers. Where a step isn't listed, or says "as in the README", do it exactly as the README says.

**Tested with** (28 October 2026): `google-genai` 2.30.0 with Python 3.12 and a free-tier key. The replies, token counts and errors below are from those real calls; yours will differ a little. Prices from <https://ai.google.dev/gemini-api/docs/pricing> (page last updated 27 October 2026). Steps 2 to 4 were also run in Windows (WSL, Ubuntu 26.04, Python 3.14.4) on 29 October 2026, with the same replies and token counts. **Being tested:** every step in AI Studio, everything inside a signed-in Claude Code session, everything on GitHub, and every step on a Mac.

## Steps

### 1. What changes this week

Read the README's step 1: tokens work the same way. The prices are different:

- **Free tier** (what you use): input and output are "Free of charge".
- **Paid tier** (for the arithmetic only): **$0.30 per million input tokens and $2.50 per million output tokens**. Google counts the model's "thinking" as output: "Output price (including thinking tokens)".

The README's worked example (500 input tokens, 200 output tokens) on the paid tier:

```text
500 x $0.30 / 1,000,000  =  $0.00015
200 x $2.50 / 1,000,000  =  $0.00050
total                    =  $0.00065
```

What you actually pay: $0. For comparison, the first call in step 3 would cost about $0.000102 on Gemini's paid tier; the README's Claude run cost about $0.000031 on Claude Haiku 5.5 (a different run, with different token counts).

### 2. Get a key safely (before class)

Skip the README's 2a to 2c (Console, credit, spend limit) and 2d's Anthropic key. Instead, **get your Google key now** by following [week 10 step 2, parts a to f](../10-embeddings-and-rag/README.md#2-get-a-google-key-safely-before-class). Three differences from what week 10 says:

- Create the key in a **new** project, not one that has billing switched on (a key in a project with billing is on the paid tier and is charged). Check AI Studio shows the key on the free tier (being tested).
- Make the `~/first-call` folder and open a new `.env` exactly as in the README's step 2d item 3.
- Your `.env` holds just **one** line, the Google key, with no spaces and no quote marks:

  ```text
  GEMINI_API_KEY=AIza...your Google key...
  ```

  Check it without showing the key: in `~/first-call`, `grep -c '^GEMINI_API_KEY=' .env` prints `1`. Don't also set `GOOGLE_API_KEY` (week 10 step 2d says why).

Everything else in the README's step 2 still applies: don't `cat` the file in class, close the editor before you share your screen, and if the key leaks, delete it in AI Studio first (week 10 step 2e), then make a new one.

### 3. Your first call

**a.** As in the README.

**b.** As in the README, but install Google's package instead of `anthropic`:

```bash
cd ~/first-call
python3 -m venv .venv
source .venv/bin/activate
pip install google-genai==2.30.0
```

Check:

```bash
python -c "from google import genai; print(genai.__version__)"
```

It prints `2.30.0`. (The ensurepip fix in the README is the same.)

**c. Write the first program.** In your terminal, in `~/first-call`, paste this whole block and press Enter:

```bash
cat > first_call.py <<'EOF'
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="In one sentence, what is a cap rate in real estate?",
    config=types.GenerateContentConfig(max_output_tokens=1000),
)

print(response.text)
print()
print("Stopped because:", response.candidates[0].finish_reason.name)
usage = response.usage_metadata
output_tokens = (usage.candidates_token_count or 0) + (usage.thoughts_token_count or 0)
print("Input tokens:", usage.prompt_token_count)
print("Output tokens:", output_tokens)
cost = (usage.prompt_token_count * 0.30 + output_tokens * 2.50) / 1_000_000
print(f"Cost: $0 on the free tier (about ${cost:.6f} on the paid tier)")
EOF
```

What it does, in plain words:

- `genai.Client()` reads your key from the environment, from `GEMINI_API_KEY`. As in the README, the program does **not** contain your key.
- `max_output_tokens` is Gemini's name for the README's `max_tokens`: a cap on how much the model may write.
- `response.text` is the answer. The "Stopped because" line shows why the model stopped.
- The model sometimes "thinks" before it answers. Google counts those thinking tokens separately (`thoughts_token_count`, empty when the model didn't think) but charges them as output on the paid tier, so the program adds them to the output tokens.

Examples on Google's own site may look different: some use a newer way of calling the model. This course uses `client.models.generate_content`, which is what was tested with 2.30.0.

**d. Run it.** As in the README (`set -a; . ./.env; set +a`, then `python first_call.py`). The course's run:

```text
A capitalization rate (cap rate) is the expected annual rate of return on a real estate investment, calculated by dividing the property’s net operating income by its current market value or purchase price.

Stopped because: STOP
Input tokens: 14
Output tokens: 39
Cost: $0 on the free tier (about $0.000102 on the paid tier)
```

`STOP` is Gemini's way of saying the model finished its answer (Claude's `end_turn`). Check what it would cost on the paid tier by hand, with step 1's arithmetic. Where the README says to check the Console's **Usage** page: AI Studio has usage and rate-limit screens, but which page shows your calls is **being tested**.

If you see `ValueError: No API key was provided. Please pass a valid API key. ...`, the key isn't loaded: run the `set -a` line again, in `~/first-call`. Other errors: see Troubleshooting below.

### 4. The settings that matter

Same lessons as the README, with Gemini's names. Every setting goes inside `types.GenerateContentConfig(...)`, next to `max_output_tokens`.

**a. The same question, three times.** Run `for i in 1 2 3; do python first_call.py; done`. In the course's run, two answers were word for word the same and the third left out "or purchase price" (all about 39 output tokens); an earlier run gave three identical answers. So answers **can** repeat exactly, but that's not a promise. Google's package does accept a `temperature` setting, but the course leaves it out, by the same rule as the README: you can't make a model give the same words every time, so you make its answers **dependable** with a specific prompt, a token cap, structured output and checks in your code.

**b. A system prompt.** Gemini calls it `system_instruction`. Change the `config=` line to:

```python
    config=types.GenerateContentConfig(
        max_output_tokens=1000,
        system_instruction="You explain real estate terms to beginners. Answer in one short sentence, with no jargon.",
    ),
```

The course's run: `A cap rate is the expected yearly return on a property, calculated by dividing its net income by its purchase price.` (33 input tokens, 23 output, `STOP`).

**c. `max_output_tokens`.** Change `1000` to `20` and run it. In the course's run the answer stopped mid-sentence, at `A cap rate (capitalization rate) is a percentage used to estimate the potential`, with `Stopped because: MAX_TOKENS` (Gemini counted 16 output tokens, fewer than the cap). The point is the reason: your program must check it and not trust a cut-off answer. Put it back to `1000`.

**d. Structured output.** Same schema as the README; in Gemini it goes in `response_json_schema`, with `response_mime_type="application/json"`. Paste this into your terminal, in `~/first-call`:

```bash
cat > structured.py <<'EOF'
import json
from google import genai
from google.genai import types

client = genai.Client()

schema = {
    "type": "object",
    "properties": {
        "price": {"type": ["number", "null"], "description": "Asking price in dollars"},
        "bedrooms": {"type": ["number", "null"], "description": "Number of bedrooms"},
    },
    "required": ["price", "bedrooms"],
    "additionalProperties": False,
}

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Cozy 3 bed, 2 bath bungalow, now $189,000.",
    config=types.GenerateContentConfig(
        max_output_tokens=1000,
        system_instruction="Pull numbers out of real estate listings. Use null for any number the listing does not state.",
        response_mime_type="application/json",
        response_json_schema=schema,
    ),
)

if response.candidates[0].finish_reason.name != "STOP":
    print("No usable answer. Stopped because:", response.candidates[0].finish_reason.name)
else:
    answer = json.loads(response.text)
    print(answer)
    usage = response.usage_metadata
    print("Input tokens:", usage.prompt_token_count, "Output tokens:", usage.candidates_token_count)
EOF
python structured.py
```

The course's run printed `{'price': 189000, 'bedrooms': 3}`, then `Input tokens: 42 Output tokens: 23`. If it seems to hang, wait: the package retries quietly when Google is busy (one test run took over 2 minutes). After a few minutes, press Ctrl+C and try again later. This run's token counts don't include thinking tokens (structured.py prints only the answer's tokens); your own program should add `thoughts_token_count`, as first_call.py does. Google's guide: <https://ai.google.dev/gemini-api/docs/structured-output> (its examples use the newer way of calling, so they look different). As in the README: structured output fixes the **shape** of the answer, not whether it's **right**.

**e. Choosing a model.** You use `gemini-3.5-flash-lite` on the free tier. Google's models page (<https://ai.google.dev/gemini-api/docs/models>, read 28 October 2026) lists it as a current stable model and, for new projects, recommends "3.5 Flash-Lite or 3.8 Flash". Stay on Flash-Lite for this course. Read the README's table anyway: you're expected to understand the Claude choices too.

### 5. Add one AI feature to your project

As in the README, except:

- **5b.** Your `~/first-call/.env`, which you copy in, holds `GEMINI_API_KEY`. Everything else (`git check-ignore .env`, the deny rule) is the same, including: if Claude Code suggests typing `! cat .env`, don't, because that puts your key into the conversation.
- **5d.** Use this planning prompt instead (replace the part in angle brackets):

  ```text
  /superpowers:writing-plans Write an implementation plan to add one AI feature to this project: <one sentence: what the feature does>. Use Google's official google-genai package pinned to 2.30.0 with the model gemini-3.5-flash-lite and structured output (response_mime_type application/json with response_json_schema) if the answer must be read by the program. Rules: the program reads the key only from the GEMINI_API_KEY environment variable (it may load .env into the environment when it starts), and you, Claude, must never open, read, print or log .env or the key; never write a key in any file; the program must still work when there is no key, no internet or the call fails, saying what happened in one plain sentence and carrying on without the feature; if the call fails with a 429 or 503 error, say so in one plain sentence and carry on; check the finish reason and check every value the model returns before using it; print the input tokens and output tokens of each call, and the cost it would have on the paid tier ($0.30 per million input, $2.50 per million output tokens, counting thinking tokens as output); tests must use a fake model and never call the real API, plus one live test that runs only when I set RUN_LIVE_TESTS=1; include a test for "no key"; update the Dockerfile so it installs the package; add a .env.example with a fake key and say in the README how to set up .env. I'm not a programmer, so keep each task small.
  ```

  When you watch the build: **No** to a key, or anything starting `sk-ant-` or `AIza`, in a file. Python's official package is `google-genai`, and a Node.js project uses `@google/genai` (npm shows it published from github.com/googleapis/js-genai); for any other name, ask "Is this Google's official package?" before answering Yes.
- **5e and 5f.** As in the README. Remember everything you send is course-safe test data. For your cost log, write down the tokens each real call printed and what it would cost on the paid tier; real cost $0 (free tier).
- **The deal screener's version** needs a Claude key, so don't run it: read the README's recorded output instead.

### 6. Review and run

As in the README, except in the 6a review prompt, change "an API key or anything starting sk-ant- in any file tracked by git" to "an API key or anything starting sk-ant- or AIza in any file tracked by git". In 6b, skip the deal screener's Docker command.

### 7. Finish

As in the README, except in 7b use the browser's Find for **both** `sk-ant-` and `AIza`. If a real key is there, don't merge: delete it in AI Studio first (week 10 step 2e).

In "Check it worked", the last line becomes: you never added billing, and your three logged calls show tokens, what they would cost on the paid tier worked out from them, and real cost $0 (free tier).

## Hand-in differences

Same assignment, same rubric, same points. Where the assignment says "cost", give what it would cost on the paid tier, worked out by you, **and** the real cost $0 (free tier).

- **(a)** As in the assignment, and no real key of either kind (`sk-ant-` or `AIza`) anywhere.
- **(b) Cost log:** three real calls with input and output tokens; real cost $0 (free tier); show the arithmetic once (required) for what each would cost on the paid tier ($0.30 / $2.50 per million). Instead of the Console screenshot: a screenshot of AI Studio's usage or rate-limit page, if it shows your calls (being tested). If it doesn't, say so.
- **(c)** As in the assignment.
- **(d) 1. Which model, and why:** say you used `gemini-3.5-flash-lite` on the free tier, what one call would cost on the paid tier, what the free tier costs you instead (Google may use what you send), and whether a stronger Gemini model, or Claude, would be worth paying for in your feature.
- **(d) 2. Dependable answers:** the same question. You left temperature out (step 4a), so how did you make the answers dependable?

If you think a key got into your hand-in or your repo, delete it in AI Studio first (week 10 step 2e).

## Troubleshooting

| What you see | What to do |
|---|---|
| `ValueError: No API key was provided. Please pass a valid API key. ...` | The key isn't loaded. In the same terminal window, in the folder with `.env`, run `set -a; . ./.env; set +a`. Check `grep -c '^GEMINI_API_KEY=' .env` prints `1`. In Docker, add `--env-file .env`. |
| `google.genai.errors.ClientError: 400 INVALID_ARGUMENT` with `API key not valid` | The key is wrong, or has spaces or quote marks around it. Check the line in `.env`, or make a new key (week 10 step 2b). Also check you haven't set `GOOGLE_API_KEY` as well. |
| `google.genai.errors.ServerError: 503 UNAVAILABLE` with `This model is currently experiencing high demand` | Google is busy (it happened in the course's test). Wait a minute and run again. Your program should treat it like any failed call: say so in one sentence and carry on without the feature. |
| Error 429 | You hit a free-tier limit (per minute or per day). Wait and try again; the daily count resets at midnight Pacific time. Don't add billing. |
| "You do not have access to Google AI Studio" | Your school account has AI Studio switched off: use a personal Google account (week 10 step 2a). |
| `ModuleNotFoundError` when you run the program | The `.venv` isn't active: `source .venv/bin/activate`, then try again. In a new folder, install `google-genai==2.30.0` first (step 3b). |
| `Stopped because: MAX_TOKENS`, and the answer is cut off | Raise `max_output_tokens` (1000 is a good start), and make your program check the finish reason. |
| You pasted a key into Claude Code, a chat or a screenshot, or committed it | Delete it in AI Studio first (week 10 step 2e), then make a new one. |
| Anything else | See the README's Troubleshooting table: most rows (`.env` in `git status`, wrong numbers, work committed to `main`) are the same. |
