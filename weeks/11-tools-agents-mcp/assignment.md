# Week 11 assignment: Tools, agents and MCP

## What to do

Follow the [week 11 README](README.md) on your own laptop, in your private `semester-project` repo, and collect four things.

On the Gemini path? See [week 11 on the Gemini path](gemini.md) for the small [hand-in differences](gemini.md#hand-in-differences).

**(a) Your merged tool.** The address of the merged pull request from your `tool` branch (README steps 4 to 6). Its **Files changed** must show:

- one tool that only **reads or calculates**, with a clear name and description;
- an agent loop that checks every input the model sends, returns errors to the model as text, and stops after a fixed number of turns;
- tests that use a fake model asking for the tool and pass with no key, including a bad input and hitting the turn limit;
- your MCP server and its test, and the pinned packages;
- `REVIEW.md` with the week 11 section.

**No `.env` and no real key**, anywhere in the pull request, the repo's history or `.mcp.json`.

**(b) Your MCP server, connected:** the exact `claude mcp add ...` command you ran, and a screenshot of Claude Code calling your tool (with nothing secret on screen).

**(c) One agent run's printed output** (README step 4d): the question, each `Calling ...` line, the answer and the cost line.

**(d) A short reflection,** about half a page:

1. **Tool or no tool:** when should the model call your tool, and when should it answer by itself? Give one example of each from your project.
2. **More powerful tools:** if your tool could change or delete things (send an email, delete a record, make a payment), what could go wrong, and what would you add before allowing it? Think about a wrong input, a misunderstood question, and someone trying to trick the model.

Never put a key, a password, a sign-in code or anything from your `.env` file in your hand-in.

## What to hand in

- One document with the pull request's address, the `claude mcp add` command and screenshot, the agent run's output and your reflection.

Submit it the way your course site says.

## Rubric

| Criterion | Points |
|---|---|
| Merged pull request: one read-or-calculate tool, a capped loop, checked inputs, offline tests with a fake model requesting the tool, and no key anywhere | 4 |
| MCP server connected: the `claude mcp add` command, the screenshot of Claude Code calling the tool, and one agent run's output | 3 |
| Reflection: when to call a tool (1 point), and what could go wrong with a tool that changes or deletes things (2 points) | 3 |
