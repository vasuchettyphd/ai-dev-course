# Week 11: Tools, agents and MCP

**Goal:** let a model **use your code** instead of guessing. You'll make a first tool call by hand, turn it into a small **agent** (a loop that keeps going until it has an answer, with a limit), give your project one safe tool, and then package that tool as an **MCP server** so Claude Code itself can use it, merged through a pull request.

**Time:** plan for about 2 to 3 hours of your own time after class (an estimate). **Cost:** a few Claude calls, from your week 9 API credit: the deal screener's agent run cost about $0.0008 (step 3). Nothing new to pay for.

**Tested with** (13 October 2026; these are the versions tested, yours may be newer):

- `anthropic` 1.13.0 and `claude-haiku-5-5`, with real calls from a container (the outputs below are from those runs).
- The official MCP Python package `mcp` 2.3.0, in a container with Python 3.12, and Claude Code 2.1.296's `claude mcp add`, `list`, `get` and `remove` commands (not signed in).
- The deal screener's new tool, agent and MCP server, with 181 tests.
- **Being tested:** everything inside a signed-in Claude Code session (approving your MCP server, the `/mcp` screen, the permission prompt and Claude Code actually calling your tool), everything on GitHub, and every step on a Mac or in Windows (WSL).

## Before you start

You need:

- Weeks 9 and 10 done: your Anthropic key in `.env`, the `Read(./.env)` deny rule in `.claude/settings.json`, and `~/first-call/.venv` (week 9 step 3).
- **Python 3.11 or newer** for the MCP part (step 5): `python3 --version`. Ubuntu 24.04 has 3.12; on a Mac, the python.org installer from week 9 step 3a is newer than that.
- `gh` signed in to **your** GitHub account, and Claude Code signed in with your Claude Pro account.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows. Claude Code and your MCP server both run there; on Windows, nothing this week goes in PowerShell.

### How you'll work this week

As in weeks 9 and 10: plain-English prompts, plain **Yes** for git, a branch first, a pull request last, and the key rules (your key only in `.env`, never printed, never in a chat).

**The tool rules, new this week:**

1. **Your first tool only reads or calculates.** No deleting, sending, paying, posting or writing files. (Week 13 is planned to cover what can go wrong when tools can do more.)
2. **Your program checks every input** the model sends to the tool, the same way it checks a person's input.
3. **Errors go back to the model as text**, so it can fix its request or ask the user, instead of your program crashing.
4. **The loop has a limit** (5 turns for the deal screener), so it can't run forever or run up costs.
5. **Only add MCP servers you wrote or trust.** An MCP server is a program that runs on your laptop.

| Claude asks to | Choose |
|---|---|
| Create or edit your code and tests on your `tool` branch | **Yes** |
| A tool that reads or calculates | **Yes** |
| A tool that deletes, sends, pays, posts or writes files | **No**. Type: "This week the tool may only read or calculate." |
| `pip install` the official packages in your project's `.venv` (step 4) | **Yes** |
| `claude mcp add ...` for **your own** server (step 5) | **Yes** |
| Add an MCP server you didn't write, or one from a website or a chat | **No** |
| Read or print `.env`, or put a key in any file, including `.mcp.json` | **No** |
| `git add`, `git commit`, `git push` on your `tool` branch, `gh pr create` | plain **Yes**, after `git status` shows no `.env` |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

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

Two details matter. Claude's turn goes back into the conversation **unchanged** (`first.content`): Anthropic's docs say any thinking in it must be passed back "complete and unmodified". And in your reply, the `tool_result` comes first.
