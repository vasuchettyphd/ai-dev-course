# Week 6 assignment: Reviewing code

## What to do

Follow the [week 6 README](README.md) on your own laptop, in your private `semester-project` repo, then collect three things.

**(a) Your merged fix pull request.** The address of the merged pull request on `semester-project` from your `review-fixes` branch (README steps 3 to 6). Its **Files changed** must show:

- your three reviewer files in `.claude/agents/`, each with `tools: Read, Grep, Glob` and its own focus (does it work, safe and private, plain English);
- `REVIEW.md`, with a Decision (`Fix` or `Won't fix`) and a Reason for every finding;
- the fixes: every Must fix done (or a reasoned `Won't fix` because the finding was wrong), each in a commit whose message starts `Fix review` (several small fixes may share one commit).

The repo stays **private**, with `vasuchettyphd` as a collaborator, so your instructor can open it.

**(b) A screenshot of the tests passing after the fixes.** Your terminal after you ran the tests yourself (README step 6b), showing the command and the result.

**(c) A short reflection,** about half a page:

1. **The most useful reviewer:** which of your three reviewers found the most useful thing, what it was, and what you did about it.
2. **One finding you disagreed with:** quote or describe it, and say why you disagreed, with the evidence you checked (README step 5). If you agreed with every finding, pick the one you came closest to marking `Won't fix`, and say why you fixed it in the end.

Never put a password, a sign-in code or a token in your hand-in.

## What to hand in

- One document with the pull request's address, the screenshot and your reflection.

Submit it the way your course site says.

## Rubric

| Criterion | Points |
|---|---|
| The three reviewer files: each read-only (`tools: Read, Grep, Glob`) and each with a clear focus of its own | 2 |
| `REVIEW.md`: every finding triaged as `Fix` or `Won't fix`, and every `Won't fix` with a real reason | 3 |
| Merged fix pull request: the Must fixes done, and the tests passing after the fixes (screenshot) | 3 |
| Reflection: the most useful reviewer (1 point), and one finding you disagreed with and why (1 point) | 2 |
