# Week 11: Tools, agents and MCP

**Goal:** let a model **use your code** instead of guessing. You'll make a first tool call by hand, turn it into a small **agent** (a loop that keeps going until it has an answer, with a limit), give your project one safe tool, and then package that tool as an **MCP server** so Claude Code itself can use it, merged through a pull request.

**Time:** plan for about 2 to 3 hours of your own time after class (an estimate). **Cost:** a few Claude calls, from your week 9 API credit: the deal screener's agent run cost about $0.0008 (step 3). Nothing new to pay for.

**Tested with** (13 October 2026; these are the versions tested, yours may be newer):

- `anthropic` 1.13.0 and `claude-haiku-5-5`, with real calls from a container (the outputs below are from those runs).
- The official MCP Python package `mcp` 2.3.0, in a container with Python 3.12, and Claude Code 2.1.296's `claude mcp add`, `list`, `get` and `remove` commands (not signed in).
- The deal screener's new tool, agent and MCP server, with 184 tests.
- Everything inside a signed-in Claude Code session (approving the server, `/mcp`, the permission prompt, Claude Code calling the tool) was tested in Windows (WSL, Ubuntu 26.04, Claude Code 2.1.312) on 29 October 2026. **Being tested:** everything on GitHub, and every step on a Mac.

## Before you start

You need:

- Weeks 9 and 10 done: your Anthropic key in `.env`, the `Read(./.env)` deny rule in `.claude/settings.json`, `~/first-call/.venv` (week 9 step 3), and the course repo's `example-project` set up as in week 10 step 4a (its own `.venv` and `.env`).
- **Python 3.11 or newer** for the MCP part (step 5): `python3 --version`. Ubuntu 24.04 has 3.12 and 26.04 has 3.14; on a Mac, if `python3 --version` says 3.10 or lower, install a newer one from python.org as in [week 5 step 3c](../05-building-with-ai/README.md#3-pick-your-tools).
- `gh` signed in to **your** GitHub account, and Claude Code signed in with your Claude Pro account.

**On the Gemini path** (no Anthropic credit, agreed with your instructor in week 9)? Use [week 11 on the Gemini path](gemini.md) alongside this page.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows. Claude Code and your MCP server both run there; on Windows, nothing this week goes in PowerShell.

### How you'll work this week

As in weeks 9 and 10: plain-English prompts, plain **Yes** for git, a branch first, a pull request last, and the key rules (your key only in `.env`, never printed, never in a chat).

**The tool rules, new this week:**

1. **Your first tool only reads or calculates.** No deleting, sending, paying, posting or writing files. (Week 13 is planned to cover what can go wrong when tools can do more.)
2. **Your program checks every input** the model sends to the tool, the same way it checks a person's input.
3. **Errors go back to the model as text**, so it can fix its request or ask the user, instead of your program crashing.
4. **The loop has a limit** (5 turns for the deal screener), so it can't run forever or run up costs.
5. **Only add MCP servers you wrote or trust.** An MCP server is a program that runs on your laptop.
6. **Start Claude Code in a window where no key is loaded** (week 9 step 5a): the MCP servers it starts would get the key too.

| Claude asks to | Choose |
|---|---|
| Create or edit your code and tests on your `tool` branch | **Yes** |
| A tool that reads or calculates | **Yes** |
| A tool that deletes, sends, pays, posts or writes files | **No**. Type: "This week the tool may only read or calculate." |
| `pip install` the official packages, pinned, in your project's `.venv` (steps 4 and 5) | **Yes** |
| `claude mcp add ...` for **your own** server (step 5) | **Yes** |
| Add an MCP server you didn't write, or one from a website or a chat | **No** |
| Read or print `.env`, or put a key in any file, including `.mcp.json` | **No** |
| `git add`, `git commit`, `git push` on your `tool` branch, `gh pr create` | plain **Yes**, after `git status` shows no `.env` |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

At the end of the build, Superpowers may ask to `rm -rf` its own scratch folder (`.superpowers/sdd/...`). Answering **No** is safe: the folder is ignored by git and can stay.

## Steps

### 1. Tools, agents and MCP in plain words

A model on its own can only write text. It can't look things up in your files, and it isn't reliable at arithmetic. **Tool use** fixes that: your program tells the model about a function it may ask for (a name, a description, and the inputs it takes). Then:

1. Your program sends the question, plus the tool's description.
2. The model replies "please run `percent_change` with old 1500 and new 1700": a **tool call**. It doesn't run anything itself.
3. **Your program** runs the function and sends back the result: `13.33`.
4. The model writes the answer using that result.

An **agent** is that cycle in a loop: ask, maybe call a tool, look at the result, repeat, until the model gives a final answer. Your program decides how many times it may go round. Anthropic's docs don't set a limit; the course uses 5.

**MCP** (Model Context Protocol) is a standard way to package tools so any AI app that speaks MCP can use them, Claude Code included. You write the tool once, as a small **MCP server**, and Claude Code can call it while it works on your project.

### 2. Your first tool call, by hand

In your terminal, in `~/first-call` (week 9), with `(.venv)` showing and your keys loaded (`set -a; . ./.env; set +a`), paste this whole block and press Enter. It creates `tool_call.py`:

```bash
cat > tool_call.py <<'EOF'
import json
import anthropic

client = anthropic.Anthropic()

# 1. Describe the tool to Claude: its name, what it's for, and the inputs it takes.
tools = [{
    "name": "percent_change",
    "description": "Work out the percentage change from an old number to a new number.",
    "input_schema": {
        "type": "object",
        "properties": {
            "old": {"type": "number", "description": "The old number"},
            "new": {"type": "number", "description": "The new number"},
        },
        "required": ["old", "new"],
    },
}]


# 2. The real function, in your code. Claude never runs it; your program does.
def percent_change(old, new):
    return round((new - old) / old * 100, 2)


messages = [{"role": "user", "content": "The rent went from $1,500 to $1,700 a month. By what percent did it go up?"}]

first = client.messages.create(model="claude-haiku-5-5", max_tokens=1000, tools=tools, messages=messages)
print("Call 1 stopped because:", first.stop_reason)
print("Call 1 tokens:", first.usage.input_tokens, "in,", first.usage.output_tokens, "out")

# 3. If Claude asked for the tool, run it and send the result back.
if first.stop_reason == "tool_use":
    messages.append({"role": "assistant", "content": first.content})  # Claude's turn, unchanged
    results = []
    for block in first.content:
        if block.type == "tool_use":
            print("Claude asked for:", block.name, json.dumps(block.input))
            answer = percent_change(block.input["old"], block.input["new"])
            print("Our code worked out:", answer)
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": str(answer)})
    messages.append({"role": "user", "content": results})

    second = client.messages.create(model="claude-haiku-5-5", max_tokens=1000, tools=tools, messages=messages)
    print("Call 2 stopped because:", second.stop_reason)
    print("Call 2 tokens:", second.usage.input_tokens, "in,", second.usage.output_tokens, "out")
    print()
    for block in second.content:
        if block.type == "text":
            print(block.text)
EOF
```

Run it: `python tool_call.py`. The course's run:

```text
Call 1 stopped because: tool_use
Call 1 tokens: 432 in, 71 out
Claude asked for: percent_change {"old": 1500, "new": 1700}
Our code worked out: 13.33
Call 2 stopped because: end_turn
Call 2 tokens: 511 in, 56 out

Your rent went up by about 13.33%, from $1,500 to $1,700 a month. That's a $200 increase, and $200 is 13.33% of $1,500.
```

What happened:

- **Call 1** stopped with `tool_use`: Claude didn't answer; it asked for the tool, with the inputs it picked.
- Your code ran `percent_change` and sent the result back as a `tool_result`, matched to Claude's request by its `id`.
- **Call 2** stopped with `end_turn`: the answer, built on your number.
- That's **two calls**, and you pay for both: (432 + 511) x $0.10 / 1,000,000 + (71 + 56) x $0.50 / 1,000,000 = about $0.00016.

Two details matter. Claude's turn goes back into the conversation **unchanged** (`first.content`): Anthropic's docs say any thinking in it must be passed back "complete and unmodified" (<https://platform.claude.com/docs/en/build-with-claude/thinking>, read 13 October 2026; the tool use docs are at <https://platform.claude.com/docs/en/agents-and-tools/tool-use/>). And in your reply, the `tool_result` comes first.

### 3. The agent loop, on the deal screener

Step 2 handled one tool call by hand. Real questions can need several: the model calls a tool, looks at the result, maybe calls it again, then answers. An **agent** is that, in a loop:

1. Send the question, the tool's description and the conversation so far.
2. If Claude stopped with `end_turn`, print the answer: done.
3. If it stopped with `tool_use`, run each tool it asked for, **after checking the inputs**, add the results to the conversation, and go back to 1.
4. If you've gone round 5 times, stop and say so.

The deal screener now has one: `python3 -m dealscreener.agent "your question"` ([`dealscreener/agent.py`](../../example-project/dealscreener/agent.py)). Its one tool, `screen_listing`, is the calculator you built in week 5: Claude decides the nine numbers from your question, and **your code** does every sum. The system prompt says "Use the screen_listing tool for every number you report; never work numbers out yourself."

**a. Try it.** In your terminal:

```bash
cd ~/ai-dev-course
git pull
cd example-project
source .venv/bin/activate
python3 --version
pip install -r requirements.txt
python3 -m dealscreener.agent "Should I buy this rental? The price is \$150,000 and the rent is \$1,700 a month. Property tax is \$2,400 a year, insurance is \$1,200 a year and there is no HOA fee. I'd put 25% down on a 30-year loan at 7% interest, with \$6,000 in closing costs."
```

`python3 --version` must say 3.11 or newer for step 5 (if not, see Troubleshooting, "No module named 'mcp'"). The agent loads your key from this folder's `.env` by itself, so there's no `set -a` line. (The `\$` keeps your terminal from treating `$1` as something else.) The course's run printed the tool call, then the answer (shortened here):

```text
Calling screen_listing with {"purchase_price":150000,"monthly_rent":1700,"yearly_property_tax":2400,"yearly_insurance":1200,"monthly_hoa":0,"down_payment_pct":25,"interest_rate_pct":7,"loan_term_years":30,"closing_costs":6000}

The screen says this listing passes your buy box. ...
- Monthly mortgage payment: $748.47
- Monthly cash flow: $430.53. ...
...
Used 3072 input and 988 output tokens on Claude in 2 turns, about $0.00080.
```

Those are exactly the numbers the program gives in week 5, because the program worked them out.

**b. Leave numbers out.** Ask "Should I buy a rental priced at \$150,000 that rents for \$1,700 a month?". The prompt tells Claude: "If the question is missing any of the nine numbers, ask the user for them and do not call the tool." In the course's run it listed the seven missing numbers and called no tool (1 turn, about $0.00031).

**c. What the tool checks.** The model can send anything, so `screen_listing` checks every input with the same rules the program uses for typed answers: every field present, numbers not words, no negatives, percentages up to 100, whole years. A rate sent as `0.07` is refused with a sentence telling Claude that percentages are written as 7 for 7% (the week 8 bug, now guarded at the tool too). A refusal goes back to Claude as a `tool_result` with `is_error: true`, so it can fix the request or ask you, and the loop carries on. In the course's run with "an interest rate of 0.07", Claude sent 7 and said "I read your 0.07 interest rate as 7%."

**What the live runs taught.** The first versions of the prompt let Claude say the calculator left out vacancy and repairs (it doesn't), and round $430.53 to "about $431" and do its own sums. Two sentences fixed that: the tool's description now says 5% vacancy and 8% repairs are included, and the prompt says to give the tool's numbers exactly. Test your prompt with real runs, and read the answers.

### 4. Give your project one tool

> Tested in a signed-in session in Windows (WSL) on 29 October 2026: the plan prompt gave a 9-task plan with the fake-model tests, and subagent-driven-development built it (36 tests passing offline). The deal screener's version was built and tested on 13 October 2026.

**a. Make the branch first.** In a **new** terminal window (no keys loaded), `cd ~/semester-project`, start `claude`, and in Claude Code:

```text
Switch to main, pull the latest changes from GitHub, then create a new branch called tool and switch to it.
```

**b. Pick one safe tool.** It should be a function your project **already has** or obviously needs, that **reads or calculates**:

| Good first tools | Not this week |
|---|---|
| A calculator your project already has (a budget total, a grade average, a price with tax) | Anything that deletes, sends email or messages, pays, posts, or writes files |
| Looking something up in your own course-safe data (your week 10 documents, a table in your project) | Anything that reaches other people's accounts or data |
| Converting units, dates or currencies with fixed rates | Running commands or code the model writes |

**c. Plan and build it.** In Claude Code (replace the parts in angle brackets):

```text
/superpowers:writing-plans Write an implementation plan to give my project one tool the model can call: <name>, which <what it reads or calculates>, using <the existing function, if there is one>. Use Anthropic's anthropic package pinned to 1.13.0 (or @anthropic-ai/sdk for a Node.js project) with claude-haiku-5-5 and an agent loop: send the tool's name, description and input_schema; when stop_reason is tool_use, run the tool and send back a tool_result with the same tool_use_id (errors as text with is_error true), appending Claude's turn to the conversation unchanged; stop at end_turn; stop after 5 turns and say so; handle max_tokens and refusal with a plain sentence; omit tool_choice and temperature. Rules: the tool only reads or calculates; check every input the model sends, the same way the program checks a person's input; tell the model in the system prompt to use the tool for every number and to ask for missing inputs instead of guessing; print each tool call and the total tokens and cost; read the key only from the environment and never read or print .env; tests must use a fake model that asks for the tool, including a bad input, two tool calls in one reply, and hitting the 5-turn limit, and never call Anthropic, plus one live test that runs only when I set RUN_LIVE_TESTS=1. I'm not a programmer, so keep each task small.
```

Then `/superpowers:subagent-driven-development Execute the plan docs/superpowers/plans/<your-plan-file>.md.` as in weeks 9 and 10. Answer as in the table at the top.

**d. Try it.** In a second terminal window (not the Claude Code one): activate `.venv`, load the key, and ask your agent three questions: one it can answer with the tool, one with an input missing, and one with a bad input (Claude may ask you about it before calling the tool, or the tool may refuse it with an `is_error` result; either is fine, as long as it doesn't guess or crash). Copy one run's printed output, with the tool calls and the cost line: you hand it in.

**e. Run the tests** with `.env` moved out of the folder, as in week 9 steps 5e and 5f: they must all pass.

### 5. Make your tool an MCP server

> Tested signed in (Claude Code 2.1.312, Windows (WSL), 29 October 2026): Claude Code shows `New MCP server found in this project: dealscreener`, `/mcp` lists `✔ dealscreener 1 tool`, and the permission prompt is titled `dealscreener - Screen Listing Tool: (MCP)` with `1. Yes`, `2. Yes, and don't ask again ...`, `3. No`. `claude mcp add`, `list`, `get` and `remove` were also run for real (Claude Code 2.1.296, not signed in). **Being tested:** Mac and GitHub.

**a. Trust first.** An MCP server is a program on your laptop that Claude Code will start and talk to. Claude Code's security page: "We encourage either writing your own MCP servers or using MCP servers from providers that you trust." Anthropic "does not security-audit or manage any MCP server" (<https://code.claude.com/docs/en/security#mcp-security>). And its MCP page: "Verify you trust each server before connecting it. Servers that fetch external content can expose you to prompt injection risk." (<https://code.claude.com/docs/en/mcp>). This week you connect only the one you write.

**b. The deal screener's server.** It is about 60 lines: [`dealscreener/mcp_server.py`](../../example-project/dealscreener/mcp_server.py). It uses the official MCP Python package, `mcp` (<https://github.com/modelcontextprotocol/python-sdk>), pinned to `mcp[cli]==2.3.0`, which needs **Python 3.11 or newer**. The core is:

```python
from mcp.server import MCPServer

mcp = MCPServer("dealscreener")

@mcp.tool()
def screen_listing(...):
    ...the same checks and calculator as the agent's tool...
```

Older tutorials call `MCPServer` by its old name, `FastMCP`; in version 2.3.0 that name no longer exists. To send a plain error sentence back to the client, the server raises `ToolError` (from `mcp.server.mcpserver.exceptions`); the client sees `Error executing tool screen_listing: ` followed by your sentence.

**c. Connect it to Claude Code.** Open a **new** terminal window with **no key loaded** (tool rule 6), `cd ~/ai-dev-course/example-project`, and check three things:

```bash
[ -z "$ANTHROPIC_API_KEY" ] && echo clear
grep -c 'Read(./.env)' .claude/settings.json
.venv/bin/python --version
```

The first prints `clear` (no key loaded in this window). The second prints `1`: this folder holds your real `.env` from week 10, so the course repo comes with the week 9 deny rule in `example-project/.claude/settings.json`, which stops Claude Code reading it: asked to show `.env`, it replied `I can't read .env. Your permission settings deny access to that file's directory, so the read was blocked.` If Claude Code suggests `! cat .env`, don't: the `!` runs the command and prints your key into the chat. The third says 3.11 or newer. You can test the server on its own first, without Claude Code: `.venv/bin/python -m unittest tests.test_mcp_server -v` starts it, lists its tool and screens listing B. Then:

```bash
claude mcp add dealscreener --scope project -e PYTHONPATH="$PWD" -- "$PWD/.venv/bin/python" -m dealscreener.mcp_server
claude mcp list
```

- `--scope project` saves the server in a file called `.mcp.json` in this folder, so it belongs to this project only.
- `-e PYTHONPATH="$PWD"` tells Python where the `dealscreener` code is, wherever Claude Code starts the server from.
- After `--` comes the command that starts the server. It uses the **full path** to the `.venv`'s Python, because Claude Code saves the command exactly as you typed it.

`claude mcp list` should show, among any other servers your account has, ``dealscreener: ... ⏸ Pending approval (run `claude` to approve)``. A project's servers wait until you approve them, as a safety check. `.mcp.json` holds no key; open it and check.

**d. Use it.** In that same key-free window, start `claude`. Claude Code shows `New MCP server found in this project: dealscreener`. Use the arrow keys to pick **Use this MCP server** and press Enter (the highlighted default, `Continue without using this MCP server`, skips it). Then ask it something that needs the tool, for example "Use the dealscreener tool to check listing B: price 150000, rent 1700 a month, property tax 2400 a year, insurance 1200 a year, no HOA, 25% down, 7% interest, 30 years, closing costs 6000." Claude Code should ask permission to run the tool: plain **Yes**. Its answer should give the cash flow as $430.53. Type `/mcp` to see your server's status: `✔ dealscreener 1 tool`, and Enter on it shows `Status: ✔ connected` and its tool `screen_listing`. Take a screenshot of Claude Code calling your tool, with nothing secret on screen: you hand it in.

**e. For your own project.** In Claude Code, on your `tool` branch:

```text
Add a small MCP server for my <tool name> tool, using the official mcp Python package pinned to mcp[cli]==2.3.0 and MCPServer (not FastMCP), or for a Node.js project the official @modelcontextprotocol/server package. It must call the same function and the same input checks as my agent's tool, raise a bad input as ToolError (from mcp.server.mcpserver.exceptions) so the model gets my own error sentence, need no API key and never read .env. Add a test that starts the server and calls the tool through the mcp package's client, once with good input and once with bad input, skipped when mcp isn't installed. Then tell me the exact claude mcp add command for it, with --scope project, -e PYTHONPATH and the full path to the .venv's Python, but don't run it.
```

Run the `claude mcp add` command yourself after reading it, in a second terminal window with no key loaded, in your project folder, after checking `.venv/bin/python --version` says 3.11 or newer (if not, see Troubleshooting, "No module named 'mcp'"). For a Node.js project, the official TypeScript package is `@modelcontextprotocol/server` (being tested; <https://github.com/modelcontextprotocol/typescript-sdk>). To remove a server: `claude mcp remove <name> -s project`.

`.mcp.json` holds the full path of **your** laptop's folder. Whether to commit it is your choice: it's no secret (no key in it), but it won't work on anyone else's laptop as it is.

### 6. Review, Docker and PR

**a. Review it with `safe-and-private`.** In Claude Code:

```text
Run the safe-and-private reviewer as a subagent on the files changed on this branch compared with main (git diff main --name-only), and on .mcp.json if it exists. Focus on: whether the tool can do anything except read or calculate; whether every input the model sends is checked; whether the agent loop is capped; whether an API key could be printed, logged or saved in any file including .mcp.json (search tracked files with git grep only, never open .env); whether any test calls Anthropic by default. Then add a section at the end of REVIEW.md, headed "## Week 11: tool review", with one table with the columns #, Label, Finding (file:line), Found by, Decision, Reason, numbering the findings T1, T2 and so on. Leave Decision and Reason empty. Do not change any file except REVIEW.md.
```

Triage, fix and commit as in week 6 steps 5 and 6.

**b. Docker.** Build and run your tests in the container as in week 7 step 4c (no key needed for the offline tests), and run your agent with `--env-file .env` as in week 9 step 6b. Check `docker run --rm <your image> ls -a` shows no `.env`.

**c. Push, open a pull request, read Files changed** (code, tests, the MCP server, requirements, `REVIEW.md`; no `.env` and no real key: Find `sk-ant-` and `ANTHROPIC_API_KEY=`), **merge on GitHub, then pull**, as in week 10 step 7.

The deal screener's week 11 changes are on this page (it works once week 11 is published): <https://github.com/vasuchettyphd/ai-dev-course/compare/week-10...week-11>.

## Check it worked

- Your agent answers a question by calling your tool, and prints each tool call and the cost.
- A question with a missing or bad input gets a question back, not a guess or a crash.
- Your tests pass with `.env` moved out of the folder, including one with a fake model asking for the tool and one that hits the 5-turn limit.
- `claude mcp list` shows your server, and Claude Code called your tool (screenshot).

## Troubleshooting

| What you see | What to do |
|---|---|
| The agent never calls the tool, or does sums itself | Make the tool's description say exactly what it's for, and the system prompt say "use the tool for every number". Read a real answer (step 3, "What the live runs taught"). |
| `Calling ...` with odd inputs, or an `is_error` result | That's the input check working: the model should fix the request or ask you. If it keeps sending the same bad input, make the tool's description say the expected format (for example "percentages are written as 25 for 25%"). |
| "Stopped after 5 turns without a final answer." | The model kept calling the tool. Look at the printed calls: usually the tool's error sentence doesn't tell it what to change. |
| Error 400 mentioning `tool_use_id` or `tool_result` | Each `tool_result` must carry the `id` of the `tool_use` it answers, and the results must come first in your reply. |
| Error 400 about thinking blocks | Claude's turn must go back into the conversation unchanged (`response.content`), not rebuilt by hand. |
| `claude mcp list` shows the server as failed, or `No module named 'dealscreener'` | Test the server on its own first: `python3 -m unittest tests.test_mcp_server -v` in the project folder. Then: the `-e PYTHONPATH="$PWD"` part is missing, or you ran `claude mcp add` from another folder. `claude mcp remove dealscreener -s project`, `cd` into the project folder, and add it again (step 5c). |
| `No module named 'mcp'` or `No module named 'pydantic'` | The `.venv` doesn't have it: `source .venv/bin/activate`, `python3 --version` (3.11 or newer), `pip install -r requirements.txt`. If the `.venv` was made with Python 3.10, delete only that `.venv` folder (`rm -r .venv`, in the project folder, nothing added to the command) and make it again with 3.11 or newer: for example `python3.12 -m venv .venv` (if `python3.12 --version` works), then `source .venv/bin/activate` and `pip install -r requirements.txt`. |
| `cannot import name 'FastMCP'` | Version 2.3.0 calls it `MCPServer`: `from mcp.server import MCPServer`. |
| "Pending approval" | Start `claude` in the project folder and approve the server (step 5d). |
| Claude Code asks permission to run your tool | Plain **Yes** for your own read-or-calculate tool. **No** for any tool you didn't write. |
| Anthropic errors (401, 429, credit, workspace) | See [week 9's Troubleshooting](../09-calling-a-model/README.md#troubleshooting). |
| Work was committed to `main` | Use [week 5's rescue](../05-building-with-ai/README.md#if-it-committed-to-main). |
