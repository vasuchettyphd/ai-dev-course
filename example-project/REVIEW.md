# Review of week 5 build

The instructor's worked example for week 6. Three reviewer agents read the deal screener as it was at the end of week 5 and reported problems. They did not change any file. This page collects what they found, and the Decision and Reason columns record what was done about each one. Every `Fix` is in a commit named after its number, for example `Fix review #3: ...` (the wording fixes #1, #5, #6, #7 and #13 share one commit). Those commits are listed on the Commits tab of the week 6 pull request on the course repo.

## How this was made

- **Reviewers:** the three agent files in [`.claude/agents/`](.claude/agents/): `does-it-work` (right answers and tests), `safe-and-private` (secrets, personal data, unsafe setup) and `plain-english` (clear names, messages and instructions). The agent files can only read files (`tools: Read, Grep, Glob`).
- **Code reviewed:** `example-project/` at the git tag `week-05` (PLAN.md, dealscreener/, tests/, README.md).
- **Date:** 2026-10-12.
- **Line numbers** point at the week 5 code (tag `week-05`); where a reviewer's number was wrong, the corrected one is shown with the reviewer's in brackets.

Each reviewer's instructions (the files in `.claude/agents/`) were run as a separate subagent on the week 5 code (tag `week-05`), and their reports were combined using the rules in the prompt students type in step 4b:

> Run the does-it-work, safe-and-private and plain-english reviewers in parallel, as separate subagents, on this project. Then combine their reports into REVIEW.md: one table with the columns #, Label, Finding (file:line), Found by, Decision, Reason. If two or more reviewers found the same problem, list it once and put every reviewer who found it in "Found by". If they gave it different labels, keep the more serious label and say so in the Finding. Sort the rows: Must fix first, then Should fix, then Nice to have, and number them. Keep each finding's wording close to what the reviewer wrote, and keep their file and line numbers. Leave Decision and Reason empty. Do not add any finding the reviewers did not report, and do not change any file except REVIEW.md. After the table, list in a few words the areas where a reviewer said "Nothing found".

The Decision and Reason columns were filled in afterwards, by a person checking each finding against the week 5 code. `Fix` means it was fixed on this branch; `Won't fix` means it was left as it is, for the reason given.

## Findings

| # | Label | Finding (file:line) | Found by | Decision | Reason |
|---|-------|---------------------|----------|----------|--------|
| 1 | Must fix | README.md:56 and tests/test_calculator.py:13 say "listing B from the plan" / "Listing A from the plan", but PLAN.md has no listings A or B (they are only in docs/superpowers/plans/2026-10-12-first-three-steps.md). A reader looking in PLAN.md won't find them. Fix: point to the docs/ file, or add the two listings to PLAN.md. | plain-english | Fix | Really a wording fix: the README and the test now point at the docs/ task plan, which has the listings and their hand working, rather than copying them into PLAN.md, where two copies could drift apart. |
| 2 | Should fix | dealscreener/buybox.py:43-45, 50-51, 61-62 vs PLAN.md:26: the rules compare at 2 decimals, so 9.996% passes a "10% minimum" (tests/test_buybox.py:56 locks it in). The comment explains it as a choice, but PLAN.md says "at least 10%" and was never updated, so plan and program disagree on edge cases. Fix: decide on purpose and add the rounding rule to PLAN.md, or drop the rounding. (plain-english said Should fix, does-it-work said Nice to have.) | does-it-work, plain-english | Fix | The rounding is on purpose, so pass or fail always matches the 2 decimals shown; PLAN.md must-have 4 now says so (so 9.996% passes, 9.994% fails), and the code is unchanged. |
| 3 | Should fix | tests/test_calculator.py:12-48: both hand-worked listings have HOA = 0, so the HOA term (dealscreener/calculator.py:66) is never tested. Fix: a third hand-worked listing with HOA above 0 (for example $150). | does-it-work | Fix | Added listing A with a $150 HOA, worked out by hand first ($118.05 a month, exactly $150 less); the test passed at once because the code was already right, and failed when the HOA was removed from the code on purpose. |
| 4 | Should fix | tests/test_calculator.py:29: vacancy and repairs reserve are only tested at 5% and 8%; a non-default pair is a stronger check. Fix: one test with, for example, 10% vacancy and 5% repairs. | does-it-work | Fix | Added listing A with 10% vacancy and 5% repairs, worked out by hand first; the test passed at once because the code was already right, and failed when the repairs reserve was fixed at 8% in the code on purpose. |
| 5 | Should fix | README.md:31 (reviewer said :87) says the plan's "open question about the repairs reserve was answered", but PLAN.md's open questions (51-56) don't include it and PLAN.md:16 just says "decided in week 5". Fix: reword to match PLAN.md. | plain-english | Fix | Correct: PLAN.md never listed the repairs reserve as an open question. The README now says the 8% was decided in week 5, as PLAN.md does. |
| 6 | Should fix | dealscreener/__main__.py:52-55 prints "Cap rate" and "Cash-on-cash return" with no explanation; a first-time investor who doesn't code may not know them. Fix: a short hint line, or explain both in the README. | plain-english | Fix | Explained both numbers in the README, so the program's output, and the plan that shows it, stay the same. |
| 7 | Nice to have | dealscreener/calculator.py:27-28 and dealscreener/buybox.py:11-12: PLAN.md calls vacancy, repairs reserve and the buy-box limits "Assumptions I set once" and "my buy-box settings" (PLAN.md:42), but they are fixed defaults, so changing a rule means editing code, and the README doesn't say so. Fix: a README line saying where the settings live, or a small settings step. | does-it-work, plain-english | Fix | Correct and cheap: the README now says where the settings live and that changing one means editing the code. A settings step is not in this version. |
| 8 | Nice to have | dealscreener/__main__.py:53-54 prints unrounded cash flow and cap rate; a tiny negative number prints "-$0.00". Fix: round before formatting. | does-it-work | Fix | Real bug: -0.004 printed as "-$0.00" (and "-0.00%"), so numbers are now rounded before formatting, with tests written first. |
| 9 | Nice to have | dealscreener/calculator.py:99-100: no test that a vacancy or repairs reserve above 100 raises an error. | does-it-work | Fix | Added tests that a vacancy or repairs reserve over 100% is refused; they passed at once because the check was already there, and failed when it was removed on purpose. |
| 10 | Nice to have | Project root has no .gitignore. Running the tests or the program creates `__pycache__/`, and any future .env, logs or data exports would be unprotected, so generated files or a real listing export or key could be committed by accident. Fix: add a .gitignore with `__pycache__/`, `*.pyc`, `.env`, `*.log`, `*.csv`, `.venv/`. | safe-and-private | Won't fix | Partly wrong: the course repo's own .gitignore already covers `__pycache__/` and `.env`, and this version writes no files; your own project repo does need one (week 5, step 4a). |
| 11 | Nice to have | dealscreener/__main__.py:14-16, dealscreener/buybox.py:32 (reviewer said :137): the answer "kinds" ("price", "percent", "years", "dollars") are cryptic, and `passes` is vague. Fix: better names (for example `deal_passes`, `answer_type`). | plain-english | Won't fix | The names are explained in the comment where they are used (__main__.py:14-16) and renaming changes no behaviour, and renaming `passes` would make the code and the week 5 plan disagree. |
| 12 | Nice to have | dealscreener/calculator.py:45: the expm1/log1p comment is too technical; only the "tiny rate" reason matters. Fix: shorten it. | plain-english | Won't fix | It is one short line, and its second half ("so a tiny rate can't round it to 0") already says why in plain words; the maths itself is the standard loan formula. |
| 13 | Nice to have | README.md:26, 43 (reviewer said :82, 99): "The exact menu is being tested" is unclear, and "The Ubuntu window (Windows)" assumes a setup. Fix: reword. | plain-english | Fix | Partly: the Ubuntu window now says where it was set up (week 2), but the menu note keeps "(being tested)", the phrase the whole course uses for steps not yet checked on real screens. |

## What the reviewers found nothing wrong with

- **The math** (does-it-work): the three numbers match the PLAN.md formulas for both example listings, reworked by hand (the reviewer could not run the tests).
- **Bad inputs** (does-it-work): zero, negative, blank, text, nan, inf, huge and over-100% answers are all handled.
- **Secrets** (safe-and-private): no passwords, keys or tokens.
- **Personal data** (safe-and-private): tests use made-up numbers, and the program never asks for names, addresses or accounts.
- **Data saved or sent** (safe-and-private): no file writing, network or logging; it only prints to the screen.
- **Unsafe installs or commands** (safe-and-private): standard Python only, and the README's commands are safe.
- **Files that should not be in the repo** (safe-and-private): none, apart from the missing .gitignore (finding 10).
- **Error messages** (plain-english): nothing found.
- **Test names and comments** (plain-english): nothing found.

## Week 7: Dockerfile review

The `safe-and-private` reviewer's instructions (in [`.claude/agents/`](.claude/agents/)) were run as a separate subagent on `Dockerfile` and `.dockerignore` as they were in the first week 7 commit, on 2026-10-12; line numbers point at that version. The findings are numbered D1 to D4 so they don't clash with the week 6 numbers, and the fixes are in a commit named `Fix review D1, D2: ...`.

| # | Label | Finding (file:line) | Found by | Decision | Reason |
|---|-------|---------------------|----------|----------|--------|
| D1 | Nice to have | .dockerignore:15-17: the secret patterns cover only `.env` and `.env.*`, so `*.pem`, `*.key`, `*.csv` and `*.log` files would be copied by `COPY . .` (Dockerfile:12) if someone added them. Fix: add `**/*.pem`, `**/*.key`, `**/*.csv`, `**/*.log`. | safe-and-private | Fix | Cheap insurance: key files and logs can hold secrets or private details, and PLAN.md says this version reads no CSV file, so none belongs in the image. |
| D2 | Nice to have | .dockerignore:7-8: `.venv` and `venv` match only at the top folder, unlike the `**/` patterns. Fix: `**/.venv`, `**/venv`. | safe-and-private | Fix | Correct: a bare name only matches at the top folder, so these now use `**/` like the other patterns. |
| D3 | Nice to have | Dockerfile:3: pinned to a tag, not a digest, so the image can change on rebuild. Fix: optionally pin `@sha256:...`. | safe-and-private | Won't fix | A digest pin stops security patches arriving and is hard for students to read; the `3.12-slim` tag is the course's pin, as the Dockerfile comment says. |
| D4 | Nice to have | .dockerignore:24-25: PLAN.md and README.md are still copied; harmless. Fix: none needed. | safe-and-private | Won't fix | The reviewer itself says harmless: PLAN.md and README.md hold no private data and help anyone who opens the image. |

What the reviewer found nothing wrong with: secrets, personal data, data sent, unsafe installs and files that should not be in the repo. It noted the official `python:3.12-slim` image (Dockerfile:3), no `pip install`, the program running as `nobody` (Dockerfile:15), and that `.git`, `.claude`, `.superpowers`, `docs`, `REVIEW.md`, `__pycache__` and `.env` files are left out.
