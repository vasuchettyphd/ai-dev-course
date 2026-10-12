# Week 6 (Reviewing code) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 6. Students:
- learn to read a diff on GitHub without being a coder
- write three reviewer agents with different focuses
- run all three on their week 5 build
- consolidate and triage the findings in `REVIEW.md`
- fix the Must fixes test first, and merge the fixes through a PR whose diff they read themselves

The week also gives the deal screener three real reviewers, a real `REVIEW.md` and the fixes (tag `week-06`), plus slides, the assignment, instructor notes with a demo script, and test checklist rows.

**Architecture:**
- Same approach as weeks 2-5.
- Facts about agent files (`.claude/agents/`, frontmatter fields, the `tools` allow-list, `/agents`, running agents in parallel) come from code.claude.com docs. Facts about `pr-review-toolkit` come from its source in the official marketplace. All of them are recorded on a fact sheet with URLs.
- The deal screener's reviews are real: the controller runs the three reviewer files' prompts as subagents on the week 5 code, and the output becomes `REVIEW.md`.
- Anything needing a signed-in student session is marked "being tested".

**Tech Stack:** Markdown, Marp (`npm run slides` in Docker), Claude Code 2.1.296+, Python 3.9+ standard library (`unittest`) for the deal screener.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 6 row ("Several reviewers with different focuses; reading a diff without being a coder | Review their own build and fix what's found"). The week 6 design was approved in conversation on 2026-10-12. Decisions:
- Students write their own three reviewer agents:
  - **Does it work?**
  - **Is it safe and private?**
  - **Can a non-coder follow it?**
- Each reviewer reports only. It never edits, and labels every finding *Must fix*, *Should fix* or *Nice to have*, with the file and line.
- All three run on the week 5 code. The findings are merged into `REVIEW.md` with who found what. The student triages each finding as Fix or Won't fix, giving a reason for each Won't fix, then fixes the Must fixes test first on branch `review-fixes` and merges through a PR.
- Anthropic's `pr-review-toolkit` is shown by the instructor as the ready-made version.
- Assignment: reviewer files 2, `REVIEW.md` with triage 3, merged fix PR with tests passing 3, reflection 2.

## Global Constraints

- Audience: business and non-CS students in week 6. They have Claude Code, git, `gh`, Superpowers and a week 5 build merged on `main` of private `semester-project`. Plain language. Every command and prompt is shown exactly and labelled with where to type it: Terminal, the Ubuntu window, or inside Claude Code.
- Platforms: Mac (Apple chip), Mac (Intel) and Windows (WSL Ubuntu). This week installs nothing new except the optional `pr-review-toolkit` demo, so the steps are the same on every platform. Say so.
- Reviewer agents must not be able to change files. Their `tools` list contains only read tools, from the fact sheet. Students check this before running them.
- Git rules from weeks 3-5 still apply:
  - make a branch (`review-fixes`) before Claude writes anything
  - never change `main`
  - finish with push and a PR, merge on GitHub, then pull
  - the repo stays private
  - plain "Yes" for git prompts
  - "No" to `reset --hard`, `--force`, `git clean` and `rm -rf`
- Claude Pro usage: three reviewers use more usage than one. No invented numbers. Point to `/usage`.
- Every fact comes from the fact sheet with its URL. Anything not observed is marked "being tested". Pin the versions tested.
- No em dashes (U+2014) or en dashes (U+2013). The rubric is a table under `## Rubric` with points in the last column, totalling 10.
- `example-project/` stays the labelled instructor example: Python 3.9+, standard library only, `python3 -m unittest`. It passes `scripts/check_course.py`. Its reviewer files live in `example-project/.claude/agents/`.
- Instructor-only material goes in the private repo.
- Branch `week-06-reviewing` in the course repo and `week-06` in the instructor repo. The user merges. Links come first, one bare URL per line.

## Review Focus

1. **A reviewer agent edits files.** Its tools list is missing, so it inherits all tools, or it includes Edit, Write or Bash. The README makes students check `tools:` and say No to any edit prompt during the review. The deal screener's agent files show the read-only list.
2. **Students accept every finding, or reject every finding, without thinking.** `REVIEW.md` requires a Fix or Won't fix decision and a reason for each Won't fix. The deal screener's `REVIEW.md` has at least one reasoned Won't fix, and at least one Must fix fixed test first.
3. **Too many findings, or duplicates across reviewers.** The consolidation prompt merges duplicates, keeps who found what, and sorts by label. Troubleshooting covers "40 findings": fix the Must fixes, triage the rest, and leave Nice to have.
4. **A fix breaks something else.** Students run all the tests and the program again after the fixes, and compare with their hand-worked example from week 5. The deal screener's fix commits keep all earlier tests passing.
5. **Students can't read the diff.** Step 2 teaches green and red lines, file by file, and asking Claude "explain this change in plain English". Students read their own fix PR's Files changed before merging, and the assignment reflection asks about it.

---

### Task 1: Fact sheet

**Files:** none in the repo. Write the report only.

- [ ] **Step 1:** Record each fact with its URL or file path.
  - **Claude Code sub-agents docs** (https://code.claude.com/docs/en/sub-agents and related pages):
    - where project agent files live (`.claude/agents/`) and the file format: frontmatter `name`, `description`, `tools`, `model`, any others, then the system prompt body
    - what happens when `tools` is omitted (does the agent inherit all tools?)
    - the exact names of the read-only tools (Read, Grep, Glob)
    - whether Bash can be left out
    - how `/agents` lists agents, and whether new files need a restart or reload
    - how to ask Claude to run several agents in parallel, and whether that is documented
    - how agents report back
    - whether subagents cost usage like the main session (costs page)
  - **GitHub docs:** reading a PR's **Files changed** (split and unified views, green and red lines, viewing a whole file, leaving a comment on a line).
  - **`pr-review-toolkit`** (`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/pr-review-toolkit/`): read the README, `commands/review-pr.md` and the agent files. Record:
    - the install command
    - the exact command and its arguments
    - the six agents and their focuses
    - their `tools` lists
    - whether it needs an open PR or `gh`
  - **The built-in review commands** in Claude Code 2.1.296 (`/review`, `/security-review` or whatever the commands doc lists): one line each, for comparison only.
- [ ] **Step 2: Container check** (not signed in, as in earlier weeks).
  - Install Claude Code 2.1.296 in `ubuntu:24.04` as a non-root user.
  - Create `.claude/agents/test-reviewer.md` with read-only tools in a git repo.
  - Record what `claude agents` or `claude --help` shows about agents, if anything works without signing in.
  - Install `pr-review-toolkit` via `claude plugin install pr-review-toolkit@claude-plugins-official` (after `claude plugin marketplace add anthropics/claude-plugins-official`) and record the output.
  - Never sign in.
- [ ] **Step 3:** Write the report: facts, transcript, versions and date.

### Task 2: Deal screener reviewer agents and the real review (example-project)

**Files:**
- Create: `example-project/.claude/agents/does-it-work.md`, `safe-and-private.md`, `plain-english.md`
- Create: `example-project/REVIEW.md` (raw findings section, filled from the real review run)

**Interfaces (produced, quoted by the README and slides):**
- Each agent file has frontmatter `name` (`does-it-work`, `safe-and-private` or `plain-english`), a one-line `description`, and `tools` set to the read-only list from the fact sheet. No Edit, Write or Bash.
- The body is a plain-English system prompt of 15-25 lines. It covers:
  - the agent's focus, with 4-6 concrete things to look for, written for any project and not just Python
  - "Report only. Never change any file."
  - read `PLAN.md` first
  - label every finding `Must fix`, `Should fix` or `Nice to have`
  - give the file and line, what is wrong, why it matters and a suggested fix
  - say "Nothing found" if nothing is found
  - keep it under 300 words
- `REVIEW.md` sections:
  - `# Review of week 5 build`
  - `## How this was made` (three reviewers, the date, and the prompt used)
  - `## Findings`: a table with columns #, Label, Finding (file:line), Found by, Decision, Reason. The Decision and Reason columns are left empty in Task 2.

- [ ] **Step 1:** Write the three agent files. Run `python3 scripts/check_course.py` and check it prints OK.
- [ ] **Step 2 (controller):** The controller runs each agent file's body as a read-only subagent prompt over `example-project/` at tag `week-05`. Pass it the agent file text plus "Review the code in example-project/ (PLAN.md, dealscreener/, tests/, README.md)". Save each raw output to the SDD workspace.
- [ ] **Step 3:** Consolidate the three raw outputs into `REVIEW.md` using the student consolidation prompt the README will give:
  - merge duplicates, keeping all finders in "Found by"
  - sort Must fix, then Should fix, then Nice to have
  - number the findings
  - keep each finding's wording close to the reviewer's
  - invent nothing
- [ ] **Step 4:** Commit on `week-06-reviewing`.

### Task 3: Triage and fixes (example-project)

**Files:**
- Modify: `example-project/REVIEW.md` (fill in Decision and Reason)
- Modify: `example-project/dealscreener/*.py` and `tests/*.py` as the Must fixes require
- Modify: `example-project/README.md` (week 6 state; tag `week-06` once published)

- [ ] **Step 1: Triage.** Mark every finding `Fix` or `Won't fix`.
  - Every Must fix is `Fix`, unless the finding is wrong. A wrong finding is `Won't fix`, with the evidence. For example, "the test at tests/test_buybox.py:40 already covers this".
  - At least one finding overall must be a reasoned `Won't fix`. If every finding is truly worth fixing, mark a Nice to have `Won't fix` with a scope reason ("not in this version, see PLAN.md").
  - Reasons are one plain sentence.
- [ ] **Step 2: Fix each `Fix` finding test first, one at a time.**
  - For a behaviour finding: write the failing test, run `python3 -m unittest` and see it fail, fix it, see all tests pass, then commit with the finding number in the message (`Fix review #3: ...`).
  - For a wording or comment finding: edit it, run the tests, then commit.
  - Run on Python 3.9 too (`docker run --rm -v "$PWD":/w -w /w python:3.9-slim python -m unittest`, from `example-project/`).
- [ ] **Step 3:** Run listings A and B through `python3 -m dealscreener`. Their outputs must be unchanged, unless a finding changed them, in which case `REVIEW.md` says why. Check that `example-project/docs/superpowers/plans/2026-10-12-first-three-steps.md` still matches the code. If the code changed, add a one-line note at the top of the plan saying week 6 review fixes changed X, rather than rewriting the plan.
- [ ] **Step 4:** Update `example-project/README.md` with the week 6 state. Run `python3 scripts/check_course.py` and check it prints OK. Check there are no dashes and that `__pycache__` is not committed. Commit.

### Task 4: README, slides and assignment

**Files:** `weeks/06-reviewing-code/README.md` (replace the stub, starting from `templates/README.md`), `slides.md`, `slides.pdf`, `assignment.md`.

- [ ] **README:** follow the approved design, steps 1-7:
  1. **Why several reviewers.** Link `advanced/` where relevant, and mention `pr-review-toolkit` as the ready-made version.
  2. **Read a diff.** Use the deal screener's week 6 fix PR on GitHub, or the student's own week 5 PR. Cover green and red lines, viewing a file, and the prompt "Explain this change in plain English: <paste>".
  3. **Make the three agents:**
     - start Claude Code in `~/semester-project` on a new branch `review-fixes`, made first (week 5 rules)
     - the prompt to create the three files, copying the deal screener's files as the starting point
     - check `tools:` is read-only
     - check `/agents` lists them, following the fact sheet's reload rule
  4. **Run all three:**
     - the exact prompt to run the three reviewers in parallel on the project and write their consolidated findings to `REVIEW.md`, using the consolidation rules from Task 2
     - what students see
     - say No to any edit prompt during the review
     - the usage note
  5. **Triage:** Fix or Won't fix for each finding, a reason for each Won't fix, and that reviewers can be wrong. The deal screener's `REVIEW.md` is the example.
  6. **Fix:**
     - one finding at a time, test first where it changes behaviour (the prompt)
     - run the tests and the program
     - push and open a PR
     - read its Files changed yourself before merging
     - merge on GitHub, then pull
  7. **Check it worked, and troubleshooting:**
     - agents don't appear
     - a reviewer edits or asks to edit
     - too many findings
     - reviewers disagree
     - a usage limit
     - a fix breaks a test
     - findings about week 5 code that belongs to Superpowers' plan file
     - work on `main` (point to week 5's rescue)
- [ ] **Slides:** 16-20 slides matching the README, including one slide showing a deal screener agent file and one showing three rows of its `REVIEW.md`. Build with `npm run slides`, restore every other week's PDF, render and look at the slides.
- [ ] **Assignment:**
  - **Hand in:**
    - the merged fix PR URL, with the three agent files and `REVIEW.md` in it
    - a screenshot of the tests passing after the fixes
    - a reflection: which reviewer found the most useful thing, and one finding you disagreed with and why
  - **Rubric:**
    - The three reviewer files, read-only and each with a clear focus: 2 points
    - `REVIEW.md` with every finding triaged and every Won't fix reasoned: 3 points
    - Merged fix PR with the Must fixes done and tests passing: 3 points
    - Reflection: 2 points
    - Total: 10 points
- [ ] **Checks:** `python3 scripts/check_course.py` prints OK. No dashes. A command-to-source table in the report.

### Task 5: Instructor notes, demo script and checklist rows (private repo)

- [ ] `weeks/06-reviewing-code/notes.md` with the four headings:
  - **Timing:** a 75-minute plan.
  - **Common problems:**
    - agents not found
    - an agent edits
    - findings overload
    - students who accept everything
    - wrong findings
    - usage
    - students whose week 5 build is unfinished (review what exists)
  - **Discussion answers.**
  - **Grading guidance:** worked 10/10 and 6/10 examples that add up, and what a good Won't fix reason looks like.

  Also a **demo script:**
  - run the three deal screener reviewers live on a scratch clone at tag `week-05`, about 15 minutes
  - compare with the committed `REVIEW.md`
  - then a 5-minute `pr-review-toolkit` showing, from the fact sheet
  - a fallback
- [ ] `weeks/06-reviewing-code/test-checklist.md`: Mac and Windows rows for every README step and troubleshooting row, in the week 5 format, with identical numbering.
- [ ] No dashes. Commit on `week-06`.

### Task 6: PRs, tag and tracking (controller)

- [ ] Push both branches and open the PRs. Links come first.
- [ ] After merge, tag `week-06`, close the OpenProject task, and delete the branches and the workspace.
