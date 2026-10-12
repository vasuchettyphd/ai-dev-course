# Review of week 5 build

The instructor's worked example for week 6. Three reviewer agents read the deal screener as it was at the end of week 5 and reported problems. They did not change any file. This page collects what they found, and the Decision and Reason columns record what was done about each one. Every `Fix` has its own commit on the branch, named after its number (for example `Fix review #3: ...`).

## How this was made

- **Reviewers:** the three agent files in [`.claude/agents/`](.claude/agents/): `does-it-work` (right answers and tests), `safe-and-private` (secrets, personal data, unsafe setup) and `plain-english` (clear names, messages and instructions). Each one can only read files (`tools: Read, Grep, Glob`).
- **Code reviewed:** `example-project/` at the git tag `week-05` (PLAN.md, dealscreener/, tests/, README.md).
- **Date:** 2026-10-12.
- **Line numbers** point at the week 5 code (tag `week-05`); where a reviewer's number was wrong, the corrected one is shown with the reviewer's in brackets.

One prompt, typed into Claude Code, ran the three reviewers and combined their reports:

> Run the does-it-work, safe-and-private and plain-english reviewers in parallel, as separate subagents, on this project. Then combine their reports into REVIEW.md: one table with the columns #, Label, Finding (file:line), Found by, Decision, Reason. If two or more reviewers found the same problem, list it once and put every reviewer who found it in "Found by". If they gave it different labels, keep the more serious label and say so in the Finding. Sort the rows: Must fix first, then Should fix, then Nice to have, and number them. Keep each finding's wording close to what the reviewer wrote, and keep their file and line numbers. Leave Decision and Reason empty. Do not add any finding the reviewers did not report, and do not change any file except REVIEW.md. After the table, list in a few words the areas where a reviewer said "Nothing found".

The Decision and Reason columns were filled in afterwards, by a person checking each finding against the week 5 code. `Fix` means it was fixed on this branch; `Won't fix` means it was left as it is, for the reason given.

## Findings

| # | Label | Finding (file:line) | Found by | Decision | Reason |
|---|-------|---------------------|----------|----------|--------|
| 1 | Must fix | README.md:56 and tests/test_calculator.py:13 say "listing B from the plan" / "Listing A from the plan", but PLAN.md has no listings A or B (they are only in docs/superpowers/plans/2026-10-12-first-three-steps.md). A reader looking in PLAN.md won't find them. Fix: point to the docs/ file, or add the two listings to PLAN.md. | plain-english | Fix | Correct: the listings and their hand working are only in the docs/ plan. Really a wording fix, so the README and the test now point at that file; copying the listings into PLAN.md would give two copies to keep in step. |
| 2 | Should fix | dealscreener/buybox.py:43-45, 50-51, 61-62 vs PLAN.md:26: the rules compare at 2 decimals, so 9.996% passes a "10% minimum" (tests/test_buybox.py:56 locks it in). The comment explains it as a choice, but PLAN.md says "at least 10%" and was never updated, so plan and program disagree on edge cases. Fix: decide on purpose and add the rounding rule to PLAN.md, or drop the rounding. (plain-english said Should fix, does-it-work said Nice to have.) | does-it-work, plain-english | Fix | The rounding is on purpose (the reason line shows 2 decimals, so pass or fail must match what it shows); PLAN.md now says so, and the code is unchanged. |
| 3 | Should fix | tests/test_calculator.py:12-48: both hand-worked listings have HOA = 0, so the HOA term (dealscreener/calculator.py:66) is never tested. Fix: a third hand-worked listing with HOA above 0 (for example $150). | does-it-work | Fix | Correct: HOA was 0 in every test. Added listing A with a $150 HOA, worked out by hand first: cash flow drops by exactly $150, to $118.05. |
| 4 | Should fix | tests/test_calculator.py:29: vacancy and repairs reserve are only tested at 5% and 8%; a non-default pair is a stronger check. Fix: one test with, for example, 10% vacancy and 5% repairs. | does-it-work | Fix | Correct: only the default 5% and 8% were tested. Added listing A with 10% vacancy and 5% repairs, worked out by hand first. |
| 5 | Should fix | README.md:31 (reviewer said :87) says the plan's "open question about the repairs reserve was answered", but PLAN.md's open questions (51-56) don't include it and PLAN.md:16 just says "decided in week 5". Fix: reword to match PLAN.md. | plain-english | Fix | Correct: PLAN.md never listed the repairs reserve as an open question. The README now says the 8% was decided in week 5, as PLAN.md does. |
| 6 | Should fix | dealscreener/__main__.py:52-55 prints "Cap rate" and "Cash-on-cash return" with no explanation; a first-time investor who doesn't code may not know them. Fix: a short hint line, or explain both in the README. | plain-english | Fix | Fair for a first-time investor. Explained both in the README rather than in the program, so the program's output (and the plan that shows it) stays the same. |
| 7 | Nice to have | dealscreener/calculator.py:27-28 and dealscreener/buybox.py:11-12: PLAN.md calls vacancy, repairs reserve and the buy-box limits "Assumptions I set once" and "my buy-box settings" (PLAN.md:42), but they are fixed defaults, so changing a rule means editing code, and the README doesn't say so. Fix: a README line saying where the settings live, or a small settings step. | does-it-work, plain-english | Fix | Correct and cheap: the README now says where the settings live and that changing one means editing the code. A settings step is not in this version. |
| 8 | Nice to have | dealscreener/__main__.py:53-54 prints unrounded cash flow and cap rate; a tiny negative number prints "-$0.00". Fix: round before formatting. | does-it-work | Fix | Real bug: a cash flow of -$0.004 printed as "-$0.00" and a tiny negative percentage as "-0.00%". Now rounded before formatting, test first. |
| 9 | Nice to have | dealscreener/calculator.py:99-100: no test that a vacancy or repairs reserve above 100 raises an error. | does-it-work | Fix | Cheap and useful: added tests that a vacancy or repairs reserve over 100% is refused. They passed at once, because the check was already there. |
| 10 | Nice to have | Project root has no .gitignore. Running the tests or the program creates `__pycache__/`, and any future .env, logs or data exports would be unprotected, so generated files or a real listing export or key could be committed by accident. Fix: add a .gitignore with `__pycache__/`, `*.pyc`, `.env`, `*.log`, `*.csv`, `.venv/`. | safe-and-private | Won't fix | Partly wrong: the course repo's own .gitignore already covers `__pycache__/` and `.env`, and this version writes no logs or CSV files (PLAN.md, "Not in this version"). Your own project repo does need one (week 5, step 4a). |
| 11 | Nice to have | dealscreener/__main__.py:14-16, dealscreener/buybox.py:32 (reviewer said :137): the answer "kinds" ("price", "percent", "years", "dollars") are cryptic, and `passes` is vague. Fix: better names (for example `deal_passes`, `answer_type`). | plain-english | Won't fix | The kinds are explained in the comment right above them (__main__.py:14-16), `passes(rule_results)` reads plainly where it is used, and renaming would make the code and the week 5 plan disagree. |
| 12 | Nice to have | dealscreener/calculator.py:45: the expm1/log1p comment is too technical; only the "tiny rate" reason matters. Fix: shorten it. | plain-english | Won't fix | The comment is one line, and its formula is what a reader checks against the standard loan payment; its reason ("so a tiny rate can't round it to 0") is already plain. |
| 13 | Nice to have | README.md:26, 43 (reviewer said :82, 99): "The exact menu is being tested" is unclear, and "The Ubuntu window (Windows)" assumes a setup. Fix: reword. | plain-english | Fix | Fair: both phrases are now plainer, and the Ubuntu window says where it was set up (week 2). |

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
