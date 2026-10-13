# Week 11 (Tools, agents and MCP) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 11. Students:
- learn tool use, agent loops and MCP in plain words
- make a first tool call by hand
- turn it into a capped agent loop
- give their own project one safe tool, with checked inputs and offline tests, merged through a PR
- wrap the same tool as a tiny MCP server and connect it to Claude Code

The deal screener gets a calculator tool, a `dealscreener.agent` command and an MCP server (tag `week-11`). The week also adds slides, the assignment, instructor notes with a demo script, and checklist rows.

**Architecture:**
- Same approach as weeks 9-10.
- Facts come from the official sources and are recorded on a fact sheet with URLs:
  - Anthropic: tool use, the agent loop, `tool_choice`, and thinking blocks with tool results on Haiku 5.5.
  - The MCP spec site and the official MCP Python and TypeScript SDKs: package names, versions, a minimal stdio server.
  - Claude Code's MCP docs: `claude mcp add` syntax, scopes, `.mcp.json`, and how permission prompts for MCP tools work.
- Live Anthropic calls use the workspace key in `~/.bashrc`, loaded into one command only and never printed. Nothing in this week needs Google.
- Anything inside a signed-in Claude Code session (Claude Code calling the MCP tool) is marked "being tested" for the instructor's checklist. The MCP server itself is tested for real with the SDK's own client or the MCP inspector, if the fact sheet finds a non-interactive way.
- The controller writes Tasks 3 and 4 (docs) itself, committing per section, because session disconnects killed background agents in week 9. Implementers and reviewers stay subagents.

**Tech Stack:** Markdown, Marp, Python 3.10+ for the SDKs (the deal screener's own logic stays 3.9+), `anthropic==1.13.0`, the official MCP Python SDK (pinned from the fact sheet), Claude Code CLI, Docker.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 11 row: "Tools, agents and MCP | Tool use, agent loops, MCP servers | Give their feature one tool". The week 11 design was approved in conversation on 2026-10-13. Decisions:
- MCP is hands-on: students build a tiny MCP server around their one tool and connect it to Claude Code.
- The deal screener's one tool is the calculator, `screen_listing`.
- Assignment:

  | Part | Points |
  |---|---|
  | Merged PR: one tool, a capped loop, checked inputs, offline tests with a fake model that requests the tool, no keys | 4 |
  | MCP server connected to Claude Code, with a screenshot of Claude Code calling the tool and the `claude mcp` command used | 3 |
  | Reflection: when to call a tool, and what could go wrong if the tool could change or delete things | 3 |

## Global Constraints

- **Audience:** business and non-CS students in week 11, with everything from weeks 1-10:
  - the week 9 key rules, `.env`, and the `Read(./.env)` deny rule
  - `~/first-call/.venv`
  - their AI feature from week 9 and their RAG from week 10

  Use plain language. Every command and prompt is exact and says where to type it.
- **Platforms:** Mac (Apple chip), Mac (Intel) and Windows (WSL 2 Ubuntu). On Windows, Claude Code and the MCP server both run in Ubuntu.
- **Tool safety for this week:**
  - Students' tools only read or calculate: no deleting, sending, paying, posting or writing files.
  - The program checks every tool input before using it.
  - Tool errors go back to Claude as text, never a crash.
  - The agent loop has a turn cap (5 for the deal screener).
  - Each call's cost is printed.
  - MCP servers run code on the laptop, so students add only servers they wrote or trust. Say plainly that week 13 covers the risks (prompt injection, over-powerful tools).
- **Key safety (weeks 9-10 rules):** the key comes from the environment only and is never printed. The deny rule stays. Docker uses `--env-file`. The MCP server must not need or read a key: the calculator needs none.
- **Facts:** every API shape, version and command comes from the fact sheet with its URL and date. No invented numbers. Anything not observed is marked "being tested". Pin the versions used.
- **Git rules from weeks 3-10:** branch first, never change `main`, PR plus Files changed plus merge plus pull, private repo, plain "Yes", "No" to `reset --hard` / `--force` / `git clean` / `rm -rf`, and the week 5 rescue.
- **Tests:** they never call the real API by default. A live test runs only with `RUN_LIVE_TESTS=1`.
- **Formatting:** no em dashes (U+2014) or en dashes (U+2013). The rubric is a table under `## Rubric`, totalling 10.
- **`example-project/`:**
  - stays the labelled instructor example
  - passes `scripts/check_course.py`
  - its offline tests run on the host (with or without the SDKs) and in the container
  - its existing behaviour and its 133 tests are unchanged
- **Repos and merging:** instructor-only material goes in the private repo. Branches: `week-11-tools-agents-mcp` in the course repo, `week-11` in the instructor repo. The user merges. Links come first, one bare URL per line.

## Review Focus

1. **The model asks for the tool with wrong, missing or absurd inputs:** a negative price, a 250% rate, text instead of a number, missing fields, or a 0.07 interest rate. The tool checks every input with the program's existing rules and returns a plain error to the model as the tool result (`is_error`), so the model can ask the user or fix it. Task 2 tests each case.
2. **The loop never ends** (the model keeps calling the tool) **or ends without an answer.** The cap is 5 turns, and then the program prints "Stopped after 5 turns without a final answer." `stop_reason` values `max_tokens` and `refusal` get the plain week 9 sentences. Tests cover each.
3. **The user's question lacks numbers.** The model should ask for them rather than guess. The system prompt says so, and a test pins the prompt. The live check runs one question with missing numbers and records what happens.
4. **The MCP server doesn't start, or Claude Code can't find it.** Causes: the wrong path, the wrong Python (venv not used), or the package not installed. The README gives the exact `claude mcp add` command with an absolute path, plus a way to test the server on its own. Task 2 runs the server with the SDK's client, or a stdio handshake, to prove it lists and runs the tool.
5. **Keys and cost.** The tool and the MCP server need no key, and the agent prints tokens and cost per call plus a total. No key appears in the code, the logs or the MCP config (`.mcp.json` is checked).

---

### Task 1: Fact sheet and dry run

**Files:** none in the repo. Write the report only.

- [ ] **Step 1:** Record, with URL and date, quoting exactly where the course will rely on it:
  - **Anthropic tool use** (docs.claude.com / platform.claude.com):
    - the `tools` parameter and its shape: `name`, `description`, `input_schema`
    - `tool_choice` values and which current models accept which (week 9 found forced `tool`/`any` returns 400 on Sonnet and Opus 5.5)
    - the reply's `tool_use` block (`id`, `name`, `input`) and `stop_reason: "tool_use"`
    - how to send `tool_result` blocks (`tool_use_id`, `content`, `is_error`) in the next user message
    - whether the assistant turn, including any `thinking` blocks, must be sent back unchanged
    - parallel tool calls
    - strict tool use (if it exists), and whether to use it
    - Anthropic's own advice on writing tool descriptions
    - the agent-loop pattern Anthropic recommends
  - **MCP:**
    - what MCP is, in the spec site's words (modelcontextprotocol.io)
    - the official Python SDK: package name, current version, Python floor, install command
    - a minimal stdio server, e.g. `FastMCP` with `@mcp.tool()`, and how it runs
    - how to test a server without Claude Code (the SDK's client, `mcp dev` / Inspector, or similar)
    - the official TypeScript SDK package name and install command
  - **Claude Code MCP** (code.claude.com/docs):
    - the exact `claude mcp add` syntax for a local stdio server
    - scopes (local, project, user) and `.mcp.json`
    - `claude mcp list`, `claude mcp get` and `claude mcp remove`
    - how tools appear (names like `mcp__server__tool`) and how permission prompts and the `/mcp` command work
    - the documented security warnings about third-party MCP servers, quoted
  - **Anthropic reconfirm:** Haiku 5.5's ID and price, and `anthropic` 1.13.0, are still current.
- [ ] **Step 2: Dry run in `python:3.12-slim` as a non-root user:**
  - install the MCP SDK (pinned) and `anthropic==1.13.0`
  - write the minimal server from the docs and start it
  - test it without Claude Code, using the documented client or a stdio handshake
  - record the transcript
  - check whether `claude mcp add` can run without signing in: install Claude Code in the container if the docs allow, run `claude mcp add --scope project ...`, and record what `.mcp.json` contains
- [ ] **Step 3: Live, with the Anthropic key loaded into one command and never printed.** Make one tool call on `claude-haiku-5-5` with a toy tool, with `tool_choice` auto, then send back the tool result and record:
  - both replies' block types, `stop_reason` and usage
  - whether a `thinking` block appears
  - what happens if the thinking blocks are left out of the history
- [ ] **Step 4:** Write the report. Never write a key.

### Task 2: Deal screener tool, agent and MCP server (example-project)

**Files:**
- Create:
  - `example-project/dealscreener/tools.py`: the `screen_listing` tool, standard library only
  - `example-project/dealscreener/agent.py`: the agent loop and the command
  - `example-project/dealscreener/mcp_server.py`: the MCP server; it imports the SDK at the top, so it is not imported by tests that run without the SDK
  - `example-project/tests/test_tools.py`
  - `example-project/tests/test_agent.py`
  - `example-project/tests/test_mcp_server.py`, skipped if the MCP SDK isn't installed
  - `example-project/tests/test_agent_live.py`
- Modify:
  - `example-project/requirements.txt`: add the MCP SDK, pinned
  - `example-project/README.md`: "What's here now (week 11)", the week 11 row, "How to ask the agent", "How to use the MCP server in Claude Code", and the cost record

**Interfaces:**
- **`dealscreener/tools.py`:**
  - `TOOL_NAME = "screen_listing"`
  - `FIELDS`: the nine `Listing` fields in order
  - `TOOL_SCHEMA`: `{"name": TOOL_NAME, "description": <plain description, say "percentages are written as 25 for 25%">, "input_schema": {"type": "object", "properties": {<each field: number or integer, with a description>}, "required": FIELDS, "additionalProperties": False}}`
  - `class ToolInputError(Exception)`: its message is a plain sentence naming the field.
  - `check_input(raw: dict) -> Listing`:
    - The input must be a dict with every field present.
    - Unknown fields raise "Unknown field: <name>."
    - Each value must be an int or float, not a bool or str, and finite. The value then goes through the same rules as `__main__.parse_answer` for its kind (price, dollars, percent, years), reusing that function on `str(value)`.
    - A percent between 0 and 1 raises "interest_rate_pct is 0.07: percentages are written as 7 for 7%. Ask the user which they meant." (the week 8 lesson, applied to the tool).
    - Problems raise `ToolInputError`.
  - `screen_listing(raw: dict) -> dict` returns `{"monthly_mortgage": float, "monthly_cash_flow": float, "cap_rate_pct": float, "cash_on_cash_pct": float, "rules": [{"passed": bool, "reason": str}], "overall": "PASS" | "FAIL"}`, rounded to 2 decimals. It uses `calculator.analyse` and `buybox.check` / `buybox.passes`. A `ValueError` from `analyse` (for example, no cash invested) becomes `ToolInputError` with its message.
- **`dealscreener/agent.py`:**
  - `MAX_TURNS = 5`
  - `SYSTEM_PROMPT`, pinned by a test, contains:
    - "Use the screen_listing tool for every number you report; never work numbers out yourself."
    - "If the question is missing any of the nine numbers, ask the user for them and do not call the tool."
    - "Explain the result in plain English for a beginner."
  - `run_agent(question: str, client, print_fn=print) -> AgentResult` with `AgentResult(text: str | None, turns: int, input_tokens: int, output_tokens: int, tool_calls: int)`:
    - Each turn calls `client.messages.create(model=extract.MODEL, max_tokens=2000, system=SYSTEM_PROMPT, tools=[tools.TOOL_SCHEMA], messages=history)`, with no `tool_choice` (auto) and no `temperature`.
    - It appends the assistant `content` to the history unchanged.
    - For every `tool_use` block, it prints `Calling screen_listing with <the input as compact JSON>`, runs `tools.screen_listing`, and returns a `tool_result`:
      - `content` is the JSON text of the result, or the `ToolInputError` sentence with `is_error: True`
      - `tool_use_id` matches the block
      - unknown tool names get `is_error` "Unknown tool."
    - It stops when `stop_reason` is `end_turn` and returns the text blocks joined.
    - `stop_reason` of `max_tokens` or `refusal` raises `extract.ExtractionError` with the week 9 sentences.
    - After `MAX_TURNS` without `end_turn`, it returns `text=None`.
    - Tokens are summed across turns.
  - `main(argv, print_fn=print, client_factory=extract.make_client) -> int`:
    - Usage: `python3 -m dealscreener.agent "your question"`. `extract.load_env_file()` runs first.
    - It prints the tool calls and the answer, then `Used <in> input and <out> output tokens on Claude in <turns> turns, about $<cost:.5f>.`
    - With `text=None` it prints "Stopped after 5 turns without a final answer." and returns 1.
    - A missing key or API errors print the plain week 9 sentences and return 1.
    - No question prints the usage text and returns 2.
- **`dealscreener/mcp_server.py`:**
  - the fact sheet's minimal pattern (for example `FastMCP("dealscreener")`)
  - one tool, `screen_listing`, with the same parameters and description, calling `tools.screen_listing` and returning its dict; a `ToolInputError` comes back as the SDK's error result
  - run with `python -m dealscreener.mcp_server` over stdio
  - needs no key and reads no `.env`

**Tests:**
- **`tests/test_tools.py`, offline:**
  - listing B through `screen_listing` gives a monthly cash flow of 430.53 and PASS (the same as the existing program)
  - listing A gives FAIL
  - each bad input raises `ToolInputError` with the field named: missing field, unknown field, string, bool, negative, NaN, a rate of 250, 30.5 years, a price of 0, and `interest_rate_pct` 0.07
  - zero cash invested (0% down and $0 closing) gives the calculator's sentence
  - `TOOL_SCHEMA` has the nine fields, all required, and `additionalProperties` set to False
- **`tests/test_agent.py`, offline:** a fake client returns scripted replies, each a `SimpleNamespace` with `content` (`thinking`, `tool_use` and `text` blocks), `stop_reason` and `usage`. It records the kwargs of each call. Cases:
  - one tool call then the answer: the second call's last message is a user message with a `tool_result` whose `tool_use_id` matches and whose content holds 430.53; the assistant turn, including its `thinking` block, is in the history unchanged; tokens are summed; `tool_calls == 1`
  - bad tool input: the `tool_result` has `is_error` True and the field sentence; the loop continues
  - an unknown tool name gives `is_error` "Unknown tool."
  - two `tool_use` blocks in one reply both get results, in one user message
  - the cap: a model that always calls the tool stops after 5 turns with `text=None`, and `main` returns 1 with the "Stopped after 5 turns" sentence
  - `max_tokens` and `refusal` give the plain sentences
  - each call sends `tools=[TOOL_SCHEMA]` and has no `tool_choice` or `temperature`
  - `SYSTEM_PROMPT` contains the three pinned sentences
  - `main` without a key gives the week 9 no-key sentence and returns 1; without a question it returns 2; the cost line has the right arithmetic
- **`tests/test_mcp_server.py`:** skipped if the MCP SDK can't be imported. It lists the server's tools and calls `screen_listing` with listing B, through the SDK's in-memory or stdio client from the fact sheet. The result holds 430.53. A bad input comes back as an error result.
- **`tests/test_agent_live.py`:** skipped unless `RUN_LIVE_TESTS=1` and the key is set. It runs listing B's question and asserts at least one tool call and "430.53" in the answer.

**Steps:**
- [ ] **Step 1:** Write `tests/test_tools.py`, watch it fail, then write `tools.py` until it passes.
- [ ] **Step 2:** Write `tests/test_agent.py`, watch it fail, then write `agent.py` until it passes. The whole suite passes with plain `python3` and no SDKs. Record the new total; the old 133 must be unchanged.
- [ ] **Step 3:** Pin the MCP SDK in `requirements.txt`. Write `mcp_server.py` and `tests/test_mcp_server.py`, and run them in a `python:3.12-slim` container with the requirements installed.
- [ ] **Step 4: Live**, in the container, with `ANTHROPIC_API_KEY` passed by name (loaded from `~/.bashrc` for that one command, never printed). Record each output, the turns, tokens and cost in the report:
  - listing B's full question
  - a question with missing numbers, which should ask for them
  - a question with "7 percent" phrased as "0.07", which should ask or correct
  - the live test
- [ ] **Step 5:** Check `claude mcp add` the way the fact sheet allows (in a container with Claude Code installed, not signed in). If it works, record the exact command and the resulting `.mcp.json`. Mark anything unobserved "being tested".
- [ ] **Step 6:** Docker:
  - build `dealscreener-w11`
  - run the offline tests in it, and the MCP test
  - run `ls -a /app`: no `.env`
  - remove the image
- [ ] **Step 7:** Update the example README, using the real numbers from Step 4. Run `check_course.py`, check there are no dashes, and check `git status` shows no `.env`. Commit early and often, with the Co-Authored-By line.

### Task 3: README, slides and assignment (controller writes, committing per section)

**Files:** `weeks/11-tools-agents-mcp/README.md` (replace the stub), `slides.md`, `slides.pdf`, `assignment.md`.

- [ ] **README:** follow the approved design, steps 1-7:
  1. **Tools, agents and MCP in plain words.** Include the request, tool call, result and answer cycle as a short numbered list.
  2. **The first tool call by hand,** in `~/first-call`:
     - a `cat > tool_call.py <<'EOF'` script with one toy tool
     - the real two-call output, with tokens
  3. **The agent loop:**
     - the loop and its cap
     - checking inputs, with errors returned as `tool_result` text
     - "let code do the maths"
     - the deal screener's agent, run live, with real output
  4. **One tool in `semester-project`:**
     - branch `tool` first
     - what makes a safe first tool: read or calculate only, with a good and bad examples table
     - the Superpowers prompt with the guardrails
     - Yes and No rules, including "No" to any tool that deletes, sends, pays or writes
  5. **Make it an MCP server:**
     - the SDK install
     - the server file
     - testing it on its own
     - `claude mcp add` with the exact syntax and scope from the fact sheet
     - `/mcp` in Claude Code
     - asking a question that uses it, and approving the tool call
     - the trust rule, with the Claude Code docs' warning quoted
     - Node.js: the TypeScript SDK package
  6. **Review, Docker and PR:**
     - `safe-and-private` covering the tool's inputs, the MCP server and `.mcp.json`
     - Files changed shows no key
     - merge, then pull
  7. **Check it worked, and troubleshooting:**
     - the tool is never called
     - wrong inputs and `is_error`
     - the turn cap is hit
     - a 400 about `tool_use` / `tool_result` ids
     - a 400 about thinking blocks (if the fact sheet shows one)
     - the MCP server isn't listed or failed to start (path, venv, package)
     - the permission prompt for the MCP tool
     - removing a server with `claude mcp remove`
     - week 9's Anthropic rows (linked)
     - the week 5 rescue
- [ ] **Slides:** 16-20 slides, including:
  - the four-step tool cycle
  - a `tool_use` block and a `tool_result` block, shown side by side
  - the capped loop
  - "let code do the maths"
  - the deal screener's agent output
  - the tool safety table
  - MCP in one picture, in words: Claude Code, MCP, your server, your function
  - `claude mcp add`
  - the assignment

  Build only this week's PDF. Render it and look at the densest slides.
- [ ] **Assignment:**
  - **Hand in:**
    - the merged PR
    - the `claude mcp ...` command used, and a screenshot of Claude Code calling the tool, with nothing secret on screen
    - one agent run's printed output, with tool calls and cost
    - the reflection
  - **Rubric:**

    | Part | Points |
    |---|---|
    | Merged PR: one read-or-calculate tool, capped loop, checked inputs, offline tests with a fake model requesting the tool, no keys | 4 |
    | MCP server connected, with screenshot, command and agent-run output | 3 |
    | Reflection: when to call a tool vs answer (1 point), what could go wrong with a tool that changes or deletes things (2 points) | 3 |
    | Total | 10 |
- [ ] **Checks:** `check_course.py` OK, no dashes, and quotes match the fact sheet.

### Task 4: Instructor notes, demo script and checklist (private repo, controller writes)

- [ ] `weeks/11-tools-agents-mcp/notes.md`:
  - **Timing:** 75 minutes.
  - **Demo script:**
    - the deal screener agent and its MCP server in Claude Code, from a scratch clone at tag `week-11`
    - the key never on screen
    - the deny rule
    - removing the MCP server afterwards
  - **Common problems:**
    - the tool never called
    - inputs as strings
    - the cap hit
    - id mismatches
    - the MCP server not starting (path, venv)
    - Windows paths in WSL
    - permission prompts
    - a student wanting a tool that sends email or deletes things
    - non-Python projects
  - **Discussion answers.**
  - **Grading guidance:**
    - 10/10 and 6/10 examples that add up
    - how to check the PR: the tool only reads or calculates, the cap exists, the inputs are checked, the tests are offline, and there are no keys in `.mcp.json`
- [ ] `weeks/11-tools-agents-mcp/test-checklist.md`: three tables with identical numbering, generated from one row list, covering every README step and troubleshooting row. Include rows for `claude mcp add` and Claude Code calling the tool in a signed-in session.
- [ ] No dashes and no keys. Commit on `week-11`.

### Task 5: PRs, tag and tracking (controller)

- [ ] Run the key scan on both branches (`sk-ant-`, `AIza`). Only fakes are allowed.
- [ ] Push both branches and open the PRs. Links come first, and ask for a merge commit.
- [ ] After merge:
  - tag `week-11`
  - check the tag clone
  - close the OpenProject task
  - delete the branches and the workspace
