# Week 11 on the Gemini path

This page is for students on the **Gemini path**: you agreed with your instructor that you can't pay for Anthropic API credit, and in week 9 you set up `~/first-call` with Google's free tier instead (see [week 9 on the Gemini path](../09-calling-a-model/gemini.md)). Follow the [week 11 README](README.md) as usual, and use this page in place of the parts that call Claude through the API. Each section below matches a README step.

What stays the same: the tool rules, the git rules, the review, Docker and the pull request. **Claude Code and the MCP part (step 5) are unchanged**: they use your Claude Pro login, not an API key.

Two reminders from week 9:

- **Free tier, free of charge.** You never add billing for this course. Your real cost this week is $0. You still work out what each call would cost on Google's paid tier, so you learn the arithmetic.
- **Google may use what you send.** On the free tier, Google uses your inputs to improve its products (week 10 step 2c quotes the terms). Everything your program sends must be course-safe: no personal, customer or real business data.

**Tested with** (28 October 2026): `google-genai` 2.30.0, `gemini-3.5-flash-lite` on a free-tier key, Python 3.12, with real calls (the output below is from that run). **Being tested:** every step on a Mac or in Windows (WSL), and your own project's agent.

## Before you start

The README's list, with one change: instead of an Anthropic key, you need **your Google key** in `~/first-call/.env` as `GEMINI_API_KEY=AIza...` (week 9 on the Gemini path), and `google-genai` 2.30.0 in `~/first-call/.venv`. Check it in your terminal, in `~/first-call` with `(.venv)` showing:

```bash
python -c "import google.genai as g; print(g.__version__)"
grep -c '^GEMINI_API_KEY=' .env
```

The first prints `2.30.0`; the second prints `1`. Never use someone else's key, Anthropic's or Google's.

## 1. Tools, agents and MCP in plain words

Same as the README. Everything in it is true of Gemini too: the model asks for a tool, **your program** runs it, and the model writes the answer from your result.

## 2. Your first tool call, by hand

In your terminal, in `~/first-call`, with `(.venv)` showing and your key loaded (`set -a; . ./.env; set +a`), paste this whole block and press Enter. It creates `tool_call.py`, the Gemini version of the README's program:

```bash
cat > tool_call.py <<'EOF'
import json
from google import genai
from google.genai import types

client = genai.Client()

# 1. Describe the tool to Gemini: its name, what it's for, and the inputs it takes.
tool = types.Tool(function_declarations=[{
    "name": "percent_change",
    "description": "Work out the percentage change from an old number to a new number.",
    "parameters_json_schema": {
        "type": "object",
        "properties": {
            "old": {"type": "number", "description": "The old number"},
            "new": {"type": "number", "description": "The new number"},
        },
        "required": ["old", "new"],
    },
}])
config = types.GenerateContentConfig(tools=[tool], max_output_tokens=1000)


# 2. The real function, in your code. Gemini never runs it; your program does.
def percent_change(old, new):
    return round((new - old) / old * 100, 2)


contents = [types.Content(role="user", parts=[types.Part(text="The rent went from $1,500 to $1,700 a month. By what percent did it go up?")])]

first = client.models.generate_content(model="gemini-3.5-flash-lite", contents=contents, config=config)
print("Call 1 stopped because:", first.candidates[0].finish_reason.name)
print("Call 1 asked for a tool:", bool(first.function_calls))
print("Call 1 tokens:", first.usage_metadata.prompt_token_count, "in,", first.usage_metadata.candidates_token_count, "out")

# 3. If Gemini asked for the tool, run it and send the result back.
if first.function_calls:
    contents.append(first.candidates[0].content)  # Gemini's turn, unchanged
    results = []
    for call in first.function_calls:
        print("Gemini asked for:", call.name, json.dumps(call.args))
        answer = percent_change(call.args["old"], call.args["new"])
        print("Our code worked out:", answer)
        results.append(types.Part(function_response=types.FunctionResponse(id=call.id, name=call.name, response={"result": answer})))
    contents.append(types.Content(role="user", parts=results))

    second = client.models.generate_content(model="gemini-3.5-flash-lite", contents=contents, config=config)
    print("Call 2 stopped because:", second.candidates[0].finish_reason.name)
    print("Call 2 tokens:", second.usage_metadata.prompt_token_count, "in,", second.usage_metadata.candidates_token_count, "out")
    print()
    print(second.text)
EOF
```

Run it: `python tool_call.py`. The course's run:

```text
Call 1 stopped because: STOP
Call 1 asked for a tool: True
Call 1 tokens: 108 in, 24 out
Gemini asked for: percent_change {"old": 1500, "new": 1700}
Our code worked out: 13.33
Call 2 stopped because: STOP
Call 2 tokens: 148 in, 13 out

The rent went up by **13.33%**.
```

What happened, and how it differs from Claude:

- **There is no `tool_use` stop reason.** Call 1 finished with `STOP`, the same as a normal answer, even though Gemini asked for the tool instead of answering. So the program doesn't look at the stop reason; it checks `first.function_calls`, which holds Gemini's tool requests (empty when it answered by itself).
- **Gemini's turn goes back unchanged** (`first.candidates[0].content`), just like Claude's. Don't rebuild it by hand: it can carry hidden parts the model needs to see again. Google's function calling guide is at <https://ai.google.dev/gemini-api/docs/function-calling> (read 28 October 2026); it also says "The model doesn't execute the function itself."
- **The result goes back as a `function_response`**, with the same `id` and `name` as Gemini's request. That's Gemini's version of Claude's `tool_result` with its `tool_use_id`.
- **Call 2** finished with `STOP`: the answer, built on your number. Gemini sometimes answers in Markdown (the `**` around `13.33%` means bold). In an earlier run it added `(or $\frac{40}{3}\%$)`, a fraction nobody asked for: read real answers, as the README says.
- **Two calls, and you pay nothing** on the free tier. On the paid tier, it would be (108 + 148) x $0.30 / 1,000,000 + (24 + 13) x $2.50 / 1,000,000 = $0.0000768 + $0.0000925 = about $0.00017.

One more difference: the `google-genai` package can run a Python function for you automatically ("automatic function calling") if you hand it the function itself, but this program hands it only a description, so nothing runs unless **your code** runs it.

## 3. The agent loop, on the deal screener

The deal screener's agent uses Claude, so it needs an Anthropic key. **Don't run the agent** (the `python3 -m dealscreener.agent ...` lines in 3a to 3c). Do run the other lines of 3a (`cd ~/ai-dev-course`, `git pull`, `cd example-project`, `source .venv/bin/activate`, `python3 --version`, `pip install -r requirements.txt`): step 5 needs them. Then read the README's step 3 and its recorded runs instead: the tool call, the answer with exactly the week 5 numbers, the run with numbers left out, and the run with "an interest rate of 0.07".

The ideas are the same on Gemini, and you'll use every one in step 4:

- The model decides the inputs; **your code** does every sum.
- The tool **checks every input** the model sends, with the same rules as a person's input, and sends a refusal back as a sentence so the model can fix its request or ask you.
- The loop **stops after 5 turns**.
- The system prompt says to use the tool for every number and to ask for missing inputs instead of guessing, and you **test it with real runs** ("What the live runs taught").

## 4. Give your project one tool

**a and b.** Same as the README.

**c. Plan and build it.** Use this prompt in place of the README's (replace the parts in angle brackets):

```text
/superpowers:writing-plans Write an implementation plan to give my project one tool the model can call: <name>, which <what it reads or calculates>, using <the existing function, if there is one>. Use Google's official google-genai package pinned to 2.30.0 with the model gemini-3.5-flash-lite and an agent loop: send the tool's name, description and parameters_json_schema as a function declaration; when the reply has function_calls, run each tool and send back a function_response part with the same id and name (errors as {"error": "..."}), appending Gemini's turn to the conversation unchanged; when it has no function_calls and finished with STOP, that's the answer; stop after 5 turns and say so; handle MAX_TOKENS and SAFETY finish reasons with a plain sentence; pass the tool as a declaration, not a Python function, so nothing runs automatically; omit temperature. If a call fails with a 429 or 503 error, say so in one plain sentence and carry on. Rules: the tool only reads or calculates; check every input the model sends, the same way the program checks a person's input; tell the model in the system prompt to use the tool for every number and to ask for missing inputs instead of guessing; print each tool call, the input tokens and output tokens, and the cost it would have on the paid tier ($0.30 per million input, $2.50 per million output tokens, counting thinking tokens as output), with "$0 (free tier)" as the real cost; read the key only from the GEMINI_API_KEY environment variable and never read or print .env; tests must use a fake model that asks for the tool, including a bad input, two tool calls in one reply, and hitting the 5-turn limit, and never call Google, plus one live test that runs only when I set RUN_LIVE_TESTS=1. I'm not a programmer, so keep each task small.
```

Sending errors back as `{"error": "..."}` is the course's choice: it's Gemini's equivalent of Claude's `is_error: true`. The course tested only the Python package; for a Node.js project, ask Claude Code to use Google's official package for Node instead (being tested).

Then `/superpowers:subagent-driven-development Execute the plan docs/superpowers/plans/<your-plan-file>.md.` as in the README.

**d and e.** Same as the README: load your key with `set -a; . ./.env; set +a`, ask your three questions (course-safe ones only), copy one run's output, and run the tests with `.env` moved out of the folder.

## 5. Make your tool an MCP server

Unchanged. It uses Claude Code and your Claude Pro login, and your MCP server needs no API key. Follow the README's step 5 as written, including the deal screener's server in 5b to 5d: it never calls a model, so it works without an Anthropic key.

In step 5c, your key-free window check should also cover your Google key. Run this as well; it should print `clear`:

```bash
[ -z "$GEMINI_API_KEY" ] && echo clear
```

## 6. Review, Docker and PR

Same as the README, with your key's names in place of Anthropic's:

- **a.** In the review prompt, change "whether any test calls Anthropic by default" to "whether any test calls Google by default".
- **b.** Run your agent in the container with `--env-file .env`, as in the README.
- **c.** In **Files changed**, Find `AIza` and `GEMINI_API_KEY=` instead of `sk-ant-` and `ANTHROPIC_API_KEY=`. Neither may appear.

## What's different in your hand-in

Everything in the [assignment](assignment.md) is the same, with the same points, except:

- **(c) One agent run's printed output:** your cost line shows the input and output tokens, the paid-tier figure, and "$0 (free tier)".
- **No `.env` and no real key** means no `AIza...` key anywhere, including `.mcp.json`.

## Troubleshooting

| What you see | What to do |
|---|---|
| `ValueError: No API key was provided. ...` | Your key isn't loaded. In the folder with `.env`: `set -a; . ./.env; set +a`. Check `grep -c '^GEMINI_API_KEY=' .env` prints `1`. |
| `400 INVALID_ARGUMENT` with `API key not valid` | Check the `GEMINI_API_KEY=` line in `.env`, or make a new key (week 10 step 2b). |
| `429` | You hit a free-tier rate limit (per minute or per day). Wait a minute and run again. The daily count resets at midnight Pacific time. |
| `503 UNAVAILABLE` with `This model is currently experiencing high demand` | Google's model is busy. Wait a minute and run again. Your agent should treat it like any failed call: say so in one plain sentence and carry on. |
| The model answered without calling the tool, or did sums itself | Tighten the tool's description and the system prompt, as in the README's step 3, "What the live runs taught": say exactly what the tool is for, and "use the tool for every number; never work numbers out yourself". Then read a real answer again. |
| Anything else | See [week 9 on the Gemini path](../09-calling-a-model/gemini.md) and the README's [Troubleshooting](README.md#troubleshooting). |
