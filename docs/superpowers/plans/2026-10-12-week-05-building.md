# Week 5 (Building with AI) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 5. Students:
- install Superpowers in `semester-project`
- let Claude suggest the language and tools for their project, and approve every install themselves
- turn the first three build steps of `PLAN.md` into a Superpowers task plan with tests first (`writing-plans`)
- build it with `subagent-driven-development`
- run the tests and the program themselves
- merge the work through a pull request

The week also builds the deal screener's first three steps in `example-project/` (Python, standard library only, tagged `week-05`), plus slides, the assignment, instructor notes with a demo script, and test checklist rows.

**Architecture:**
- Same approach as weeks 2-4.
- Every Superpowers, Claude Code and install fact comes from official sources and is recorded on a fact sheet with its URL. Sources: Superpowers 6.4.1 skill files, code.claude.com docs, support.claude.com for usage limits, python.org, nodejs.org and Ubuntu docs.
- The Superpowers install and skill files are inspected for real in a container.
- The deal screener's code and tests are run for real.
- Anything that needs a signed-in session is marked "being tested" and gets rows in the instructor's checklist.

**Tech Stack:** Markdown, Marp (`npm run slides` in Docker), Docker `ubuntu:24.04`, Claude Code (native installer), Superpowers 6.4.1, Python 3.9+ with only the standard library (`unittest`) for the example project.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 5 row ("Building with Superpowers (decided in week 4): small steps, tests first"). The week 5 design was approved in conversation on 2026-10-12. Decisions:
- **Each student's stack:** each student lets Claude suggest the language and tools for their own project, with guardrails: they must run on Mac and in WSL, every install step is explained first, and students read each install prompt.
- **The build flow:** students use the full Superpowers chain, `writing-plans` then `subagent-driven-development`.
- **Usage limits:** because the full chain uses Claude Pro usage quickly, the week teaches `/usage`, starting early, and resuming from the Superpowers ledger after a limit.
- **The example project:** the deal screener's steps 1-3 are built in Python and tagged `week-05`.
- **Beads:** offered as an optional extra.

## Global Constraints

- Audience: business and non-CS students in week 5. They have Claude Code, git, `gh`, plan mode, `/grill-me` and a merged `PLAN.md` in a private `semester-project` repo. Plain language. Every command and prompt is shown exactly and labelled with where to type it: Terminal, the Ubuntu window, or inside Claude Code.
- Platforms: Mac (Apple chip), Mac (Intel) and Windows (WSL Ubuntu). Each install path covers all three, and Windows commands run in the Ubuntu window, never PowerShell. Intel Macs can't use Homebrew (week 3), so Intel paths use official installers.
- Students choose their own stack. Don't teach one language. Teach how to ask for a suggestion that runs on Mac and WSL, how to read an install prompt, and how to check what was installed. Give official install links for the two most likely picks, Python and Node.js, for all three platforms.
- Claude Pro usage: no invented limit numbers. Cite https://support.claude.com pages and `/usage` from the fact sheet. Say plainly that subagent-driven development uses more usage than working in one session.
- Repo rules from weeks 3-4 still apply: work on a branch, merge through a PR on GitHub, then pull. Nothing is pushed straight to `main`. The repo stays private. Plain "Yes" for git prompts. Never paste secrets.
- Every fact comes from the fact sheet with its URL. Anything not observed is marked "being tested". Pin the versions tested.
- No em dashes (U+2014) or en dashes (U+2013). The rubric is a table under `## Rubric` with points in the last column, totalling 10.
- `example-project/` stays the clearly labelled instructor example. Its Python code needs only the standard library and Python 3.9 or newer, because a Mac's Xcode command-line tools Python is 3.9. Tests use `unittest` and run with `python3 -m unittest`. It passes `scripts/check_course.py`.
- Instructor-only material goes in the private repo.
- Branch `week-05-building` in the course repo and `week-05` in the instructor repo. The user merges. Links come first, one bare URL per line.

## Review Focus

1. **The student approves an install they don't understand, or one that needs `sudo` in a way that breaks WSL** (for example a Mac-only command in WSL). The README says what a safe install prompt looks like, when to say No, and to ask "Is this for Mac or Linux?". Troubleshooting covers "command not found" after an install.
2. **The usage limit is hit in the middle of a task.** The student loses track and restarts from scratch, or tries to buy more usage. The README explains `/usage`, waiting for the reset, and resuming with the ledger. The deal screener demo records roughly how much usage the build took, if it can be observed (otherwise "being tested").
3. **Work lands on `main` or in a worktree folder the student can't find.** The README explains where Superpowers puts the work (from the fact sheet: branch or worktree), how to find it, and the finish step that pushes and opens the PR. Troubleshooting covers "my files disappeared" and "it committed to main".
4. **Tests pass but the program is wrong, or there are no real tests.** Students must run the program themselves with their own example and compare it with a hand-worked answer. The deal screener shows this with a listing worked out by hand.
5. **Bad input in the example program** (letters, a negative price, zero interest, zero cash invested). The program re-asks or explains, and never crashes with a traceback. Task 2's tests pin each case.

---

### Task 1: Fact sheet and dry run

**Files:** none in the repo. Write the report only.

- [ ] **Step 1: Fact sheet.** Record each fact with its URL or file path.
  - **Superpowers 6.4.1** (`~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/skills/`). Read these skills and record what each one does, what it asks the user, what files it writes and where, and how it ends:
    - `writing-plans`: where the plan is saved, its header, and the handoff question that offers Subagent-driven or Native
    - `subagent-driven-development`: the ledger path and whether it is git-ignored (read `scripts/sdd-workspace`), what the user sees per task, fix rounds, the final review, and how to resume after stopping
    - `using-git-worktrees`: whether a worktree is created, where it goes, and how to find it
    - `test-driven-development`
    - `finishing-a-development-branch`: the options it offers (merge locally, push and PR, keep, discard) and which one students should choose
  - **Claude Code docs:**
    - subagents and what they cost, from the costs page and the sub-agents page
    - `/usage`
    - what happens at a usage limit, and when it resets (Claude Code docs and support.claude.com "usage limits" articles for Pro)
    - permission prompts for installs
    - the `/plugin` list
  - **Install docs for the likely stacks, on all three platforms:**
    - Python: does macOS have `python3` after week 3's Xcode command-line tools, and which version? Record the python.org installer for Mac (works on Apple chip and Intel), and Ubuntu's `python3` and `python3-venv` packages.
    - Node.js: the nodejs.org installer for Mac (Apple chip and Intel), and Ubuntu, using the official NodeSource or nvm instructions from nodejs.org's download page.
  - **`advanced/beads/README.md`:** note what it covers, so week 5 can link to it as optional.
- [ ] **Step 2: Dry run in a clean `ubuntu:24.04` container, as a non-root user.**
  - Install Claude Code with the native installer.
  - Run `claude plugin marketplace add anthropics/claude-plugins-official`, then `claude plugin install superpowers@claude-plugins-official`, and record the output.
  - List the installed skill folders.
  - Copy `example-project/` in once Task 2 exists, or check with a hello-world `unittest` file now. Check `python3 --version` and `python3 -m unittest` with no extra packages, and record whether `python3` is preinstalled in `ubuntu:24.04`. If it isn't, record the `apt` command.
  - Never sign in and never enter credentials.
- [ ] **Step 3:** Write the facts, the transcript, the versions and the date to the report.

### Task 2: Deal screener steps 1-3 (example-project)

**Files:**
- Create: `example-project/docs/superpowers/plans/2026-10-12-first-three-steps.md`. This is the Superpowers-format task plan a student would get from `writing-plans`, written from `example-project/PLAN.md`'s first three build steps. Students see it as the example of what `writing-plans` produces.
- Create: `example-project/dealscreener/__init__.py`, `calculator.py`, `buybox.py`, `__main__.py`
- Create: `example-project/tests/__init__.py`, `test_calculator.py`, `test_buybox.py`, `test_main.py`
- Modify: `example-project/PLAN.md`. Answer the repairs reserve open question: 8% of monthly rent, decided while building. Move it out of open questions and into the assumptions.
- Modify: `example-project/README.md`. Add the week 5 state: how to run the tests and the program, and that the tag `week-05` will be added once week 5 is published.

**Interfaces (produced, used by the README and the slides):**
- `dealscreener.calculator`:
  - `Listing` (frozen dataclass). All fields are floats except `loan_term_years: int`, and percentages are written as 25 for 25%. Fields: `purchase_price`, `monthly_rent`, `yearly_property_tax`, `yearly_insurance`, `monthly_hoa`, `down_payment_pct`, `interest_rate_pct`, `loan_term_years`, `closing_costs`.
  - `Assumptions(vacancy_pct=5.0, repairs_reserve_pct=8.0)`.
  - `Results(monthly_mortgage, monthly_cash_flow, cap_rate_pct, cash_on_cash_pct)`.
  - `monthly_mortgage_payment(principal, annual_rate_pct, years) -> float`.
  - `analyse(listing, assumptions=Assumptions()) -> Results`. Raises `ValueError` with a plain-English message for:
    - a purchase price that is 0 or less
    - a negative amount
    - a percentage outside 0-100
    - a loan term below 1
    - zero cash invested (down payment amount plus closing costs is 0)
- `dealscreener.buybox`:
  - `BuyBox(min_cash_on_cash_pct=10.0, min_monthly_cash_flow=100.0)`.
  - `RuleResult(name, value, threshold, passed, reason)`.
  - `check(results, buy_box=BuyBox()) -> list` of two `RuleResult`s, cash-on-cash first.
  - `passes(rule_results) -> bool`.
  - Comparisons are "at least", so a value equal to the threshold passes. Compare `round(value, 6) >= threshold`.
  - Reason texts:
    - `"Cash-on-cash return 5.74% is below 10.00% by 4.26 points"` and `"Cash-on-cash return 11.88% is at least 10.00%"`
    - `"Monthly cash flow $268.05 is at least $100.00"` and `"Monthly cash flow $50.00 is below $100.00 by $50.00"`
- `dealscreener.__main__`:
  - `run(input_fn=input, print_fn=print) -> int`. It asks for each `Listing` field in order, with plain prompts such as `"Purchase price ($): "`, and re-asks with a short message on non-numbers, negatives or out-of-range percentages.
  - It prints the three numbers, each rule's pass or fail with its reason, and a final `PASS` or `FAIL` line.
  - It returns 0. `python3 -m dealscreener`, run inside `example-project/`, calls it.
  - It never shows a traceback for bad input.
  - `analyse`'s `ValueError` for zero cash invested is printed as a message, and the program asks again from the down payment onward.

**Hand-checked test listings.** Use the same assumptions for both: vacancy 5% and repairs 8%. Values were worked out by hand in the plan and confirmed with a one-line Python check. Use `assertAlmostEqual(..., delta=0.01)` for dollar amounts and `delta=0.001` for percentages.

| Field | Listing A | Listing B |
|---|---|---|
| Price | 200000 | 150000 |
| Rent | 1800 | 1700 |
| Tax | 2400 | 2400 |
| Insurance | 1200 | 1200 |
| HOA | 0 | 0 |
| Down | 25% | 25% |
| Rate | 7% | 7% |
| Term | 30 years | 30 years |
| Closing | 6000 | 6000 |
| **Mortgage** | **997.95** | **748.47** |
| **Cash flow** | **268.05** | **430.53** |
| **Cap rate** | **7.596%** | **9.432%** |
| **Cash-on-cash** | **5.744%** | **11.877%** |
| **Buy box** | **FAIL** on cash-on-cash, cash flow passes | **PASS** |

- [ ] **Step 1:** Write the student-visible plan file (`docs/superpowers/plans/2026-10-12-first-three-steps.md` inside `example-project/`).
  - Use the `writing-plans` header format.
  - Make three tasks, matching the three build steps, each with tests first.
  - Use the interfaces and test listings above.
- [ ] **Step 2: Calculator, test first.** Write `tests/test_calculator.py` and run `python3 -m unittest` in `example-project/` to see it fail. Then write `calculator.py` until it passes. The tests cover:
  - Listings A and B.
  - Zero interest: `monthly_mortgage_payment(120000, 0, 10) == 1000.00`.
  - 0% down with closing costs 6000, which works.
  - 0% down with 0 closing costs, which raises `ValueError` mentioning "cash invested".
  - A negative rent, which raises.
  - A down payment of 120%, which raises.
  - A purchase price of 0, which raises.
- [ ] **Step 3: Buy box, test first.** Write `tests/test_buybox.py` covering:
  - A fails on cash-on-cash only, and its reason text is exactly as above.
  - B passes.
  - Exactly 10.0% passes.
  - Exactly $100.00 passes.
  - A cash flow of 50 fails, with the reason text above.
  - A negative cash flow fails.

  See it fail, then implement it.
- [ ] **Step 4: Runner, test first.** Write `tests/test_main.py` with a fake `input_fn` fed from a list and a `print_fn` that collects output. It covers:
  - Listing B's numbers give output containing `PASS` and `430.53`.
  - `"abc"`, then `"-5"`, then `"150000"` for the price re-asks twice, then continues, with no traceback.
  - A down payment of `"0"` with closing costs `"0"` prints the cash-invested message and re-asks.

  See it fail, then implement it.
- [ ] **Step 5:** Run `python3 -m unittest` and check all tests pass. Then run `printf '150000\n1700\n2400\n1200\n0\n25\n7\n30\n6000\n' | python3 -m dealscreener` and paste the output into the report.
- [ ] **Step 6:** Update `PLAN.md` (repairs 8%) and `example-project/README.md` (week 5 state, how to run). Run `python3 scripts/check_course.py` and check it prints OK. Check there are no em or en dashes, and that `__pycache__` is not committed (it is in `.gitignore`).
- [ ] **Step 7:** Commit on `week-05-building`.

### Task 3: README, slides and assignment

**Files:** `weeks/05-building-with-ai/README.md` (replace the stub, starting from `templates/README.md`), `slides.md`, `slides.pdf`, `assignment.md`.

- [ ] **README:** follow the approved design, steps 1-8:
  1. **What building with AI means:** small steps, tests first, and a review after every step. Link `advanced/grill-me-superpowers/` for depth, and `advanced/beads/` as an optional extra.
  2. **Install Superpowers in `semester-project`:** the week 4 command, `/reload-plugins`, and checking it in `/plugin`.
  3. **Pick your tools:**
     - the exact prompt asking for a stack that runs on Mac and in WSL, with each install step explained before it runs
     - how to read an install prompt, and when to say No
     - official install links for Python and Node.js on Mac (Apple chip), Mac (Intel) and Windows (WSL)
     - how to check what was installed (`--version`)
  4. **Plan the first three steps:**
     - the `writing-plans` prompt, which uses `PLAN.md`'s first three build steps
     - where the plan file is saved
     - reading it: tasks, tests first, files
     - at the handoff question, choose Subagent-driven
     - the deal screener's plan file as the example
  5. **Build with `subagent-driven-development`:**
     - what students see per task (implementer, then reviewer, then fixes)
     - the ledger, and where it lives
     - which prompts to say Yes or No to
     - how to stop safely
     - worktree or branch behaviour, from the fact sheet
  6. **Usage limits:**
     - `/usage`
     - what happens at the limit
     - wait for the reset, then resume ("Continue the plan from the ledger")
     - start early in the week
     - the honest note that subagents use more
  7. **Finish:**
     - run the tests yourself
     - run the program with your own example and compare it with a hand-worked answer
     - `finishing-a-development-branch`: choose push and PR
     - merge on GitHub, then pull
  8. **Check it worked, and troubleshooting:**
     - tests fail
     - an install meant for the wrong platform
     - "command not found"
     - a usage limit
     - a long review loop
     - a worktree folder, or "my files disappeared"
     - it committed to `main`
     - the plan has more than three steps

  Put "being tested" notes on everything that needs a signed-in session, unless the fact sheet observed it. In "Tested with", give the versions and the date.
- [ ] **Slides:** 16-20 slides matching the README, including a slide that walks through the deal screener's plan file and the test-first loop. Build with `npm run slides`, restore every other week's PDF the build rewrote, render to PNG and look at them.
- [ ] **Assignment:**
  - **Hand in:**
    - the merged PR URL containing the plan file and the first three steps
    - a screenshot of the tests passing
    - a screenshot of the program running on their own example, with the hand-worked answer beside it
    - a reflection (one review finding and what changed; roughly how much of their usage the build took)
  - **Rubric:**
    - Merged PR with the plan file and the three steps built on a branch: 4 points (plan file 1, three steps working 2, merged through a PR 1)
    - Tests run and pass, and the program checked against a hand-worked example: 3 points
    - Reflection: 3 points
    - Total: 10 points
- [ ] **Checks:** `python3 scripts/check_course.py` prints OK. No em or en dashes. A command-to-source table in the report.

### Task 4: Instructor notes, demo script and checklist rows (private repo)

- [ ] `weeks/05-building-with-ai/notes.md` with the four headings:
  - **Timing:** a 75-minute plan. Students start the build in class and finish at home.
  - **Common problems:**
    - wrong-platform installs
    - usage limits
    - a long review loop
    - worktree confusion
    - work on `main`
    - plans with too many steps
    - a project whose stack won't run in WSL
    - students who skipped week 4's `PLAN.md`
  - **Discussion answers.**
  - **Grading guidance:** worked 10/10 and 6/10 examples that add up under the rubric, and how to grade a project in any language (read the tests, run them, run the program).

  Also a **demo script:** build deal screener step 1 live with `writing-plans` and `subagent-driven-development`, in a fresh copy of the week 4 state (`git checkout week-04` in a scratch clone). List the exact prompts, what to point out, and about 20 minutes. The fallback is to show the tagged `week-05` code and the plan file.
- [ ] `weeks/05-building-with-ai/test-checklist.md`: Mac and Windows rows for every README step, including troubleshooting, in the same format as weeks 2-4.
- [ ] No em or en dashes. Commit on `week-05`.

### Task 5: PRs, tag and tracking (controller)

- [ ] Push both branches and open the PRs. Give the user the bare PR links first.
- [ ] After merge, tag the course repo's merge commit `week-05` and push the tag. Close the OpenProject task "Week 5: Building with AI".
