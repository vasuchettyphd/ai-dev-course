# Week 14 (Final demos) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 14. Students:
- get their semester project "ready on main" against a checklist drawn from weeks 3 to 13
- write and rehearse a 3-minute demo script (`DEMO.md`) with a fallback for when the network or the model fails
- write a short final write-up (`FINAL.md`) where every number comes from a file in their repo
- give the demo in class

The deal screener gets a model `DEMO.md` and `FINAL.md` (tag `week-14`), with no code change. The week also adds slides, the 30-point assignment, instructor notes (demo-day running order, grading sheet) and checklist rows.

**Architecture:**
- Same approach as weeks 9 to 13.
- **Sources:** the repo itself (results files, `BUGS.md`, `REVIEW.md`, the example README) for every number in `FINAL.md`; live runs of each `DEMO.md` command in a container.
- **Live calls:** the workspace Anthropic key in `~/.bashrc`, loaded into one command and never printed; the Google key the same way for the notes command only if `DEMO.md` uses it. No OpenRouter calls.
- **Who writes what:** the controller writes Tasks 3 and 4 inline, committing per section. Implementers and reviewers are subagents.

**Tech Stack:** Markdown, Marp, Python 3.10+ (3.11+ for the agent's `mcp` extra), `anthropic==1.13.0`, Docker.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 14 row: "Final demos | Presentations | Demo and a short write-up", and "Week 14 has a larger final-project rubric" (30 points; `scripts/check_course.py` enforces 30). Week 4 promised a demo "shown working in **3 minutes**". The week 14 design was approved in conversation on 2026-10-13. Decisions:

| Assignment part | Points | Split |
|---|---|---|
| Demo | 10 | works, or the fallback is used well (4); the AI feature shown (2); one honest limit (2); within 3 minutes (2) |
| Project on main | 10 | tests pass offline (2); `REVIEW.md` triaged (2); evaluation and injection results committed (2); no key anywhere in the history (2); README says how to run it and Docker runs it (2) |
| Write-up | 10 | the seven headings present and specific (4); every number traceable to a file in the repo (3); "what AI did and what I decided" honest and specific (3) |

`FINAL.md` headings (students and the deal screener use the same seven):
1. What it does and who it's for
2. How it's built, and which parts are AI
3. What I measured
4. What went wrong and what I changed
5. Risks and responsible use
6. What AI did and what I decided
7. What I'd do next

## Global Constraints

- **Audience:** business and non-CS students in week 14. They have everything from weeks 1 to 13: key rules, `.env`, the deny rule, evaluation and security habits, Docker, PRs with merge commits.
  - Use plain language.
  - Every command and prompt is exact and labelled with where to type it.
- **Platforms:** Mac (Apple chip), Mac (Intel) and Windows (WSL 2 Ubuntu).
- **Demo safety:** no key on screen ever: demo from a window where no key is loaded or from a program that reads `.env` itself; never `cat .env`, `env`, `printenv`; close other tabs and notifications; a key that appears on screen is treated as leaked (week 9 step 2f, delete first).
- **Honesty:** the write-up reports real numbers from the repo, misses as well as scores, and what AI did; a demo that fails live is not penalised if the fallback is used well and the failure is explained.
- **Facts:** no invented numbers; every number in `FINAL.md` links to its source file; anything not observed is marked "being tested". Pin versions.
- **Git rules from weeks 3 to 13:** branch first, never change `main`, PR, read Files changed, merge with "Create a merge commit", then pull. Plain "Yes" to git prompts; "No" to `reset --hard`, `--force`, `git clean` and `rm -rf`. Week 5 rescue for work committed to `main`.
- **Tests:** they never call the real API by default.
- **Formatting:** no em dashes (U+2014) or en dashes (U+2013). The rubric is a table under `## Rubric`, totalling **30**.
- **`example-project/`:** no code change; the existing 236 tests stay unchanged and pass; `check_course.py` reports OK.
- **Repos and branches:** instructor-only material goes in the private repo. Branches: `week-14-final-demos` in the course repo, `week-14` in the instructor repo. The user merges. Links come first, one bare URL per line.

## Review Focus

1. **The live demo fails in the room** (no internet, a 429, an expired key, a slow call). `DEMO.md` has a fallback at every live step: the committed results files and the offline tests, which need no key and no network. Task 2 runs the fallback commands with the network off (`docker run --network none`) and records that they work.
2. **A key appears on screen.** No `DEMO.md` command prints a key or the environment; the README's "on the day" section and the notes say what to do if one appears (delete it first, then carry on with the fallback).
3. **The demo runs over 3 minutes.** `DEMO.md` gives a time for each step summing to 3:00 or less, and says what to cut first. Task 2 times one read-through with the real command output and records the total.
4. **A number in the write-up has no source.** Every number in the deal screener's `FINAL.md` links to a file in the repo; a reviewer checks each one. The student prompt for drafting `FINAL.md` forbids numbers that aren't in a file.
5. **A student's feature doesn't work yet.** The README's troubleshooting says to demo what does work, say plainly what doesn't, and use the fallback; the rubric's "works, or the fallback is used well" point allows it.

---

### Task 1: Repo fact sheet

**Files:** none in the repo. Write the report only (in the SDD workspace).

- [ ] **Step 1:** From `example-project/` on this branch, record with file paths and line numbers every number the model `FINAL.md` may use:
  - week 8: the `0.07` bug (`BUGS.md`, `FEEDBACK.md`)
  - week 6 and 7: `REVIEW.md` finding counts and decisions
  - week 9: the listing step's model, price and a call's cost (example README)
  - week 10: the notes command (model names, the free-tier caveat)
  - week 11: the agent's listing B answer ($430.53), turns and cost
  - week 12: every evaluation results file (`evals/results/2026-10-13-*.md`): scores, case 14, costs
  - week 13: the injection results (before 39/40, after 40/40, dev 75/75), `inj-07`, total cost
  - the current test count (`python3 -m unittest` with plain `python3`: expect 236, 9 skipped)
- [ ] **Step 2:** Record the exact commands that run each feature (example README sections), which need a key, which need the network, and which work offline.
- [ ] **Step 3:** Record what weeks 3 to 13 asked students to have on `main` (one line each, with the week and step), as the source for the "ready on main" checklist.
- [ ] **Step 4:** Write the report, with no key in it.

### Task 2: Model DEMO.md and FINAL.md (example-project)

**Files:**
- Create: `example-project/DEMO.md`, `example-project/FINAL.md`
- Modify: `example-project/README.md`: "What's here now (week 14)" and the week 14 row in "How it grows"; nothing else

**`DEMO.md`:** a timed 3-minute script, one table row per step with: the time (cumulative, ending at 3:00 or less), what to show, the exact command and where to type it, what to say (one or two plain sentences), and the fallback if it fails. Steps:
1. 0:00 the problem in one sentence (who it's for)
2. one listing through the listing step (`python3 -m dealscreener --listing`, pasting `listings/listing-b.txt`), confirming the numbers, the verdict
3. the agent answering one question (week 11)
4. the evaluation: show the committed week 12 results file and the week 13 before and after (no live run in the demo; say why)
5. one honest limit: case 14's price range answered two ways
6. close: what AI did and what you decided, in one sentence

Plus: "Before you start" (window with no key loaded; `.env` in place; terminal font large; notifications off), "If it fails" (the offline fallback: `python3 -m unittest` and the results files, no key and no network), and "What to cut first if you're over time".

**`FINAL.md`:** about two pages under the seven headings, using only numbers from Task 1's fact sheet, each linked to its file. "What AI did and what I decided" is written as the instructor building the example with Claude Code, honestly.

**Steps:**
- [ ] **Step 1:** Draft `DEMO.md`.
- [ ] **Step 2: Live**, in a `python:3.12-slim` container (Python 3.12 for the agent) with `ANTHROPIC_API_KEY` passed by name (loaded from `~/.bashrc` for that one command, never printed): run each live `DEMO.md` command once (the listing step with listing B piped in, the agent question). Record the real output and cost; put the real output in `DEMO.md` where it says "you'll see".
- [ ] **Step 3: Offline fallback:** run `python3 -m unittest` and `cat` the results files named in `DEMO.md` inside `docker run --network none` with no key. Record that they work.
- [ ] **Step 4:** Time one read-through: the times in `DEMO.md` must add to 3:00 or less with the real output; record the total in the report.
- [ ] **Step 5:** Write `FINAL.md`. Check every number against its linked file.
- [ ] **Step 6:** Update the example README's week 14 parts. Run the test suite (236, 9 skipped, unchanged), `check_course.py` (OK), check for dashes and that `git status` shows no `.env`. Commit early and often, with the Co-Authored-By line.

### Task 3: README, slides and assignment (controller writes, committing per section)

**Files:** `weeks/14-final-demos/README.md` (replace the stub), `slides.md`, `slides.pdf`, `assignment.md`.

- [ ] **README:**
  1. **What final demos are:** 3 minutes each plus about a minute of questions; the order is set by your instructor; what you hand in.
  2. **Get your project ready on main:** branch `final`; the "ready on main" checklist from Task 1 Step 3 (tests pass with `.env` moved out using the guarded commands, `REVIEW.md` triaged, evaluation and injection results committed, no key in the history (week 13 step 1), Docker builds and runs the tests, the README says how to run it); a Claude Code prompt to check each item and list what's missing without fixing anything on its own; fix, PR, merge commit.
  3. **Write your 3-minute demo:** `DEMO.md`, modelled on the deal screener's; a prompt to draft it from their repo; rehearse twice with a timer; the fallback.
  4. **Write your write-up:** `FINAL.md` with the seven headings; a prompt to draft it from their own repo where every number must come from a file and be linked, and nothing is invented; then they edit it themselves, especially heading 6.
  5. **On the day:** what to have open, a key-free window, notifications off, the fallback, what to do if a key shows on screen.
  6. **Check it worked** and **Troubleshooting:** over time; no internet or 429 on the day; a feature that doesn't work yet; a key on screen; Docker won't build; the week 9 Anthropic rows; the week 5 rescue.
- [ ] **Slides:** 14 to 18, covering each README section, the deal screener's `DEMO.md` timing, `FINAL.md`'s headings, and the 30-point rubric. Build only this week's PDF, render it, and look at the dense slides.
- [ ] **Assignment:** hand-ins and the 30-point rubric as in the table above.
- [ ] **Checks:** `check_course.py` OK (rubric 30), no dashes, numbers match the fact sheet and the example files.

### Task 4: Instructor notes, grading sheet and checklist (private repo, controller writes)

- [ ] `weeks/14-final-demos/notes.md`:
  - **Timing:** a 75-minute demo day (about 15 demos at 4 minutes plus changeover; the instructor sets the split if the class is larger), and what to do before class (order, a shared timer, a fallback laptop).
  - **Your own demo:** the deal screener's `DEMO.md` from a scratch clone at tag `week-14`, keys cleared from the projector window, as the opening example (optional, 3 minutes).
  - **Grading sheet:** one row per student with the 30-point split; how to grade a demo that fails live; how to check "no key in the history" quickly.
  - **Common problems:** over time, a live failure, a key on screen, a write-up with invented numbers, a write-up that hides what AI did, a student absent on the day (a recorded demo, your call).
  - **Worked examples:** 30/30 and 18/30 that add up.
- [ ] `weeks/14-final-demos/test-checklist.md`: three tables with identical numbering, generated from one row list, covering every README step and troubleshooting row; every `.env` move guarded.
- [ ] No dashes and no keys. Commit on `week-14`.

### Task 5: PRs, tag and tracking (controller)

- [ ] Key scan on both branches (`sk-ant-`, `AIza`, `sk-or-`). Only fakes are allowed.
- [ ] Push both branches and open the PRs. Links come first, and ask for a merge commit.
- [ ] After merge: tag `week-14`, check the tag clone, close the OpenProject task, delete the branches and the workspace.
