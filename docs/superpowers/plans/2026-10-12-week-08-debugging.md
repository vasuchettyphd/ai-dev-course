# Week 8 (Debugging with AI + midterm check-in) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 8. Students:
- demo version 1 of `semester-project` to a classmate in class (the midterm check-in), and fill in a feedback form for the classmate's project
- log the bugs found in `BUGS.md`, written as exact steps to reproduce
- debug one bug properly with Superpowers' `systematic-debugging` skill: reproduce, narrow down, a failing test, then the fix
- avoid the "fix it" loop: stop after two failed attempts, undo, and ask for the cause before any change
- merge the fix through a PR

The week also fixes a real deal screener bug the same way (tag `week-08`) and adds slides, the assignment, instructor notes with a demo script, and checklist rows.

**Architecture:**
- Same approach as weeks 2-7.
- Facts about `systematic-debugging` come from the skill's own files in Superpowers 6.4.1 (`skills/systematic-debugging/SKILL.md` and the files beside it) and the Superpowers repository, recorded on a fact sheet with paths or URLs.
- The deal screener bug is real and was confirmed on 2026-10-12: typing the interest rate as `0.07` (meaning 7%) is read as 0.07%. For listing B the mortgage comes out as $315.80 and the deal passes. It is fixed test first, and the program then asks "Did you mean 7%?".
- Anything that needs a signed-in Claude session (what `systematic-debugging` looks like live) is marked "being tested".

**Tech Stack:** Markdown, Marp (`npm run slides` in Docker), Python 3.9+ standard library for the deal screener (`python3 -m unittest`), Docker Engine for the container check, Superpowers 6.4.1.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 8 row ("Debugging with AI + midterm check-in | Reproduce, narrow down, avoid the 'fix it' loop | Demo version 1 to a classmate"). The week 8 design was approved in conversation on 2026-10-12. Decisions:
- The midterm is a peer demo in class. Pairs, about 5 minutes each: the student shows version 1, the classmate tries their own inputs (including odd ones) and fills in `feedback-form.md` (what worked, what broke and how, one suggestion). Then they swap.
- Bugs go in `BUGS.md` in `semester-project` with a fixed template: what you did (exact input), what you expected, what happened, does it happen every time.
- One bug is debugged with `systematic-debugging` on branch `fix-<short-name>`, made first.
- The deal screener fix is the `0.07` interest rate bug, fixed test first, with a filled-in example feedback form.
- Assignment: feedback form for the partner 2, `BUGS.md` 2, merged fix PR with a test that failed before the fix 4, reflection 2.

## Global Constraints

- Audience: business and non-CS students in week 8. They have Claude Code, git, `gh`, Superpowers (week 5), the week 6 reviewers in `.claude/agents/`, Docker Desktop (week 7), and a merged version 1 of private `semester-project` with tests. Plain language. Every command and prompt is shown exactly and labelled with where to type it: Terminal, the Ubuntu window, or inside Claude Code.
- Platforms: Mac (Apple chip), Mac (Intel) and Windows (WSL 2 Ubuntu). Nothing new is installed this week. Say that the steps are the same on all three, and on Windows they run in the Ubuntu window.
- Git rules from weeks 3-7:
  - make a branch before Claude changes anything
  - never change `main`
  - push and open a PR, read Files changed, merge on GitHub, then pull
  - the repo stays private
  - plain "Yes" for git prompts
  - "No" to `reset --hard`, `--force`, `git clean` and `rm -rf`
  - the week 5 rescue (`#if-it-committed-to-main`) for work committed to `main`
- Debugging rules for students:
  - reproduce before fixing
  - a test that fails because of the bug comes before the fix
  - "No" to changes unrelated to the bug, and "No" to deleting or weakening a test to make it pass
  - two failed attempts means stop: undo with week 3's safe undo, and ask Claude to explain the cause before it changes anything. Say that the skill's own limit is three failed fixes (from its `SKILL.md`), and the course uses two because a beginner's attempts cost more time.
- Peer demo privacy: classmates see only the running program and its output, not secrets such as `.env` or API keys. Students close or hide anything private before the demo.
- Every fact comes from the fact sheet with its source. Anything not observed is marked "being tested". Pin the versions tested.
- No em dashes (U+2014) or en dashes (U+2013). The rubric is a table under `## Rubric` with points in the last column, totalling 10.
- `example-project/` stays the labelled instructor example. It passes `scripts/check_course.py`, and its tests run with `python3 -m unittest` both on the host and in the container.
- Instructor-only material goes in the private repo.
- Branch `week-08-debugging` in the course repo and `week-08` in the instructor repo. The user merges. Links come first, one bare URL per line.

## Review Focus

1. **The "fix" hides the bug instead of fixing it.** For example, Claude changes the test's expected number to match the wrong output, or deletes the failing test. The README's Yes/No rules say "No" to this, and the deal screener's history shows the test failing first (the report records the failing run before the fix commit).
2. **The question "Did you mean 7%?" breaks other answers.** A real 0.5% or a 0% rate, a 0.25 down payment, an answer of `y`/`n`/blank/other text, and running out of input during the question must all behave sensibly. Task 2 has a test for each.
3. **The bug can't be reproduced**, or only happens sometimes. The README's troubleshooting says what to do (write down the exact input, try again from a fresh start, note what was different), and the `BUGS.md` template has the "does it happen every time" line.
4. **The peer demo can't happen** because a student's build is broken, the partner is absent, or the partner finds nothing. The README says what to do in each case (demo what exists and log the break as a bug; the instructor pairs you or you demo to the instructor; use the odd-input list), and so do the instructor notes.
5. **The fix only works on the student's laptop.** After the fix, the tests also run in the container from week 7. The deal screener does this for real, and the README's "check it worked" step includes it.

---

### Task 1: Fact sheet

**Files:** none in the repo. Write the report only.

- [ ] **Step 1:** Read `skills/systematic-debugging/SKILL.md` and every file beside it in Superpowers 6.4.1 (`/home/vasu/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/skills/systematic-debugging/`), and the matching files on GitHub (`obra/superpowers`). Record, with the path or URL:
  - its name and description (when it starts on its own)
  - the four phases, in the skill's own words, each with a one-line plain-English version for students
  - the "iron law" and the three-failed-fixes rule, quoted exactly
  - the red flags it lists, such as "one more fix attempt"
  - whether it requires a failing test before the fix, and which other skill it points to for that (for example test-driven development), quoted
  - how a user starts it by name inside Claude Code (the exact way skills are invoked, from the Claude Code or Superpowers docs)
  - what it produces, if anything (files, or only conversation)
- [ ] **Step 2:** Record from the Claude Code docs, with URLs, anything the README needs about undoing changes, such as checkpoints or `/rewind`, if documented. The safe undo the README uses is week 3's. Read `weeks/03-git-and-github/README.md` and record its exact section anchor and commands.
- [ ] **Step 3:** Reproduce the deal screener bug on this machine and record the output exactly:
  - `printf '150000\n1700\n2400\n1200\n0\n25\n0.07\n30\n6000\n' | python3 -m dealscreener` in `example-project/` (expected: mortgage $315.80, Overall: PASS)
  - the same with `7` for the rate (listing B as designed)
  - work out by hand what $112,500 at 7% for 30 years costs a month, and record the arithmetic
- [ ] **Step 4:** Write the report: facts, transcripts, versions (Superpowers 6.4.1, Python on this machine) and the date.

### Task 2: Deal screener bug fix (example-project)

**Files:**
- Create: `example-project/BUGS.md`, `example-project/FEEDBACK.md`
- Modify: `example-project/dealscreener/__main__.py`, `example-project/tests/test_main.py`, `example-project/README.md` (a "What's here now (week 8)" section and the week 8 row in "How it grows", tag `week-08` once published), `example-project/.dockerignore` (add `BUGS.md` and `FEEDBACK.md` to the "people read them" group)

**Interfaces (quoted by the README and slides):**
- **`BUGS.md` template,** used word for word by the README:

  ```markdown
  ## Bug N: <short name>

  - **Found by:** <who> on <date>
  - **What I did (exact input):**
  - **What I expected:**
  - **What happened:**
  - **Does it happen every time?** Yes / No / Not sure
  - **Status:** Open / Fixed in <commit or PR link>
  - **Cause:** (fill in once you know)
  ```

- **Bug 1 in the deal screener:** "Interest rate typed as 0.07 is read as 0.07%". Found by the instructor acting as the classmate, using the odd-input list. Exact input: listing B with `0.07` for the rate. Expected: a mortgage around the 7% figure from Task 1, or a question. Actual: $315.80 and Overall PASS. Every time: Yes. Cause: `parse_answer` accepts any percent from 0 to 100, so a decimal fraction is taken as a percentage. Status: Fixed, with the commit.
- **The fix in `dealscreener/__main__.py`:** for a "percent" answer greater than 0 and less than 1, `ask` asks one follow-up question before accepting it:

  ```
  You typed 0.07. Did you mean 7%? Type y for 7%, or n to keep 0.07%:
  ```

  The number shown is the typed value and the value times 100, formatted without trailing zeros (`0.07` gives `7%`, `0.065` gives `6.5%`, `0.25` gives `25%`). `y` or `yes`, any case, returns the value times 100. `n` or `no` returns the value as typed. Anything else, including blank, repeats the follow-up question. `0` and values from 1 to 100 are not asked about. End of input during the follow-up still stops with "Stopped before all the numbers were typed." and exit code 1. `parse_answer` keeps its signature and behaviour. Add a helper `confirm_small_percent(value, input_fn, print_fn) -> float`, called from `ask` when `kind == "percent"` and `0 < value < 1`.
- **`FEEDBACK.md`:** the week's `feedback-form.md` filled in for the deal screener, labelled at the top as written by the instructor acting as the classmate. "What broke" names the `0.07` input. No invented student names.

- [ ] **Step 1: Log the bug.** Write `BUGS.md` with the intro line "Bugs found in the deal screener, one section each, newest last." and Bug 1 with Status "Open" and Cause blank. Commit: `Deal screener: log the 0.07 interest rate bug`.
- [ ] **Step 2: Write the failing tests** in `tests/test_main.py`, in a new `class SmallPercentTest(unittest.TestCase)`, using `run_with`:

  ```python
  def listing_b_with_rate(*rate_answers):
      answers = list(LISTING_B)
      answers[6:7] = list(rate_answers)
      return answers


  class SmallPercentTest(unittest.TestCase):
      def test_rate_typed_as_a_fraction_asks_and_yes_means_percent(self):
          console, exit_code = run_with(listing_b_with_rate("0.07", "y"))
          self.assertEqual(exit_code, 0)
          self.assertIn("You typed 0.07. Did you mean 7%? Type y for 7%, or n to keep 0.07%: ", console.prompts)
          plain, _ = run_with(LISTING_B)
          self.assertEqual(console.output().splitlines()[-9:], plain.output().splitlines()[-9:])

      def test_no_keeps_the_small_rate(self):
          console, exit_code = run_with(listing_b_with_rate("0.07", "n"))
          self.assertEqual(exit_code, 0)
          self.assertIn("Monthly mortgage payment: $315.80", console.output())

      def test_yes_and_no_ignore_case_and_spaces(self):
          yes, _ = run_with(listing_b_with_rate("0.07", " YES "))
          plain, _ = run_with(LISTING_B)
          self.assertEqual(yes.output().splitlines()[-9:], plain.output().splitlines()[-9:])
          no, _ = run_with(listing_b_with_rate("0.07", "No"))
          self.assertIn("Monthly mortgage payment: $315.80", no.output())

      def test_other_answers_ask_the_follow_up_again(self):
          console, exit_code = run_with(listing_b_with_rate("0.07", "", "maybe", "y"))
          self.assertEqual(exit_code, 0)
          follow_up = "You typed 0.07. Did you mean 7%? Type y for 7%, or n to keep 0.07%: "
          self.assertEqual(console.prompts.count(follow_up), 3)

      def test_shows_the_number_without_extra_zeros(self):
          console, _ = run_with(listing_b_with_rate("0.065", "y"))
          self.assertIn("You typed 0.065. Did you mean 6.5%? Type y for 6.5%, or n to keep 0.065%: ", console.prompts)

      def test_zero_and_whole_percentages_are_not_questioned(self):
          for rate in ("0", "1", "7", "100"):
              console, _ = run_with(listing_b_with_rate(rate))
              self.assertFalse(any(p.startswith("You typed") for p in console.prompts), rate)

      def test_down_payment_typed_as_a_fraction_is_asked_too(self):
          answers = list(LISTING_B)
          answers[5:6] = ["0.25", "y"]
          console, exit_code = run_with(answers)
          self.assertEqual(exit_code, 0)
          self.assertIn("You typed 0.25. Did you mean 25%? Type y for 25%, or n to keep 0.25%: ", console.prompts)
          plain, _ = run_with(LISTING_B)
          self.assertEqual(console.output().splitlines()[-9:], plain.output().splitlines()[-9:])

      def test_running_out_of_input_at_the_follow_up_stops_politely(self):
          console, exit_code = run_with(LISTING_B[:6] + ["0.07"])
          self.assertEqual(exit_code, 1)
          self.assertIn("Stopped before all the numbers were typed.", console.output())
  ```

  Check `LISTING_B`'s index for the rate (index 6) and down payment (index 5) against the comment at the top of the file before relying on them. If the report's last 9 lines include anything that differs for a reason other than the rate, compare the four number lines and the Overall line instead, and say so in the report.
- [ ] **Step 3: Run them and watch them fail.** `cd example-project && python3 -m unittest tests.test_main -v`. Expected: the new tests fail (no follow-up prompt; the run reads `y` as the loan term and asks again, or similar), and every old test passes. Save the failing output in the report. Do not commit failing tests on their own; the next commit carries test and fix together, and the report is the evidence the tests failed first.
- [ ] **Step 4: Find the cause, following `systematic-debugging`'s phases.** In the report, write one short paragraph per phase for this bug: the root cause (`parse_answer` accepts 0.07 as a valid percent), the pattern (both percent questions share it), the hypothesis and how the tests check it, and the fix.
- [ ] **Step 5: Implement the fix** in `dealscreener/__main__.py`: add `confirm_small_percent` and call it from `ask`. Keep the existing style (docstrings, `input_fn`/`print_fn`). Format the numbers with `f"{x:g}"` or an equivalent that gives `0.07`, `7`, `0.065`, `6.5`, and guard against floating-point noise in `value * 100` (for example `round(value * 100, 10)`); record which you used.
- [ ] **Step 6: Run all tests.** `python3 -m unittest`. Expected: `Ran 47 tests ... OK` (39 before plus 8). Then run the original reproduction from Task 1 with `0.07` followed by `y`, and with `n`, and record both outputs.
- [ ] **Step 7: Container check.** `docker build -t dealscreener-w8 .` and `docker run --rm dealscreener-w8 python -m unittest` in `example-project/`; record `Ran 47 tests ... OK`. Check `docker run --rm dealscreener-w8 ls -a /app` has no `BUGS.md` or `FEEDBACK.md`. Remove the image afterwards with `docker image rm dealscreener-w8`.
- [ ] **Step 8: Finish the records.** In `BUGS.md`, set Bug 1's Status to "Fixed in commit `<short hash>`" (use the fix commit; a follow-up commit can fill it in) and fill in Cause. Write `FEEDBACK.md`. Update the example README and `.dockerignore`. Run `python3 scripts/check_course.py` from the repo root and check it prints OK. Check there are no dashes. Commit on `week-08-debugging`.

### Task 3: README, slides, assignment and feedback form

**Files:** `weeks/08-debugging/README.md` (replace the stub, starting from `templates/README.md`), `weeks/08-debugging/feedback-form.md`, `slides.md`, `slides.pdf`, `assignment.md`.

- [ ] **`feedback-form.md`:** a one-page form the classmate fills in during the demo: project name and owner, the classmate's name, date, "What I tried (exact inputs)", "What worked", "What broke, and exactly how (what I typed, what I expected, what happened)", "One suggestion", and a line for the owner to note which bugs went into `BUGS.md`. It also lists the **odd-input list** to try: blank, words instead of numbers, 0, negative numbers, very large numbers, decimals where whole numbers are expected and the reverse (`0.07` vs `7`), symbols (`$`, `%`, `,`), very long text, and pressing Enter too early. Students copy it into their own repo, or fill in a printed copy; say which the instructor collects (see Task 4: the form is handed in, so a file or a photo).
- [ ] **README:** follow the approved design, steps 1-7:
  1. **Debugging with AI without the "fix it" loop.** Describe the loop ("it's broken, fix it", a guess, something else breaks). The four steps: reproduce, narrow down, test, fix. Map them to `systematic-debugging`'s four phases from the fact sheet, in plain English. Say Superpowers is already installed from week 5.
  2. **Midterm peer demo, in class.** Pairs, about 5 minutes each, then swap. Before the demo: run your program once, close or hide `.env` and anything private. The classmate tries their own inputs and the odd-input list, and fills in `feedback-form.md`. What to do if your build is broken (demo what exists, the break goes in `BUGS.md`), if your partner is absent, or if your partner found nothing.
  3. **Log the bugs** in `BUGS.md` in `semester-project` with the template, word for word from Task 2. Show the deal screener's Bug 1 as the worked example (link to `example-project/BUGS.md`). Writing on `main` is not allowed, so make branch `fix-<short-name>` first and add `BUGS.md` on it.
  4. **Debug one bug properly** on branch `fix-<short-name>`:
     - the prompt that starts `systematic-debugging` with the `BUGS.md` entry pasted in, and asks for the cause first and a failing test before the fix
     - what students should see, phase by phase, marked "being tested" where a signed-in session wasn't observed
     - run the test and see it fail before any fix
     - Yes/No rules: "No" to changes unrelated to the bug, "No" to deleting or weakening a test
     - run all the tests after the fix, and in Docker (week 7)
  5. **When you're in the loop.** Two failed attempts: stop, undo with week 3's safe undo (link the anchor from the fact sheet), and ask Claude to explain the cause before changing anything. Give the exact prompt. Note the skill's own three-fix limit.
  6. **Finish:** update the bug's Status and Cause in `BUGS.md`, push and open a PR, read Files changed (the test, the fix, `BUGS.md`, nothing unrelated), merge on GitHub, then pull.
  7. **Check it worked, and troubleshooting:**
     - you can't reproduce the bug
     - the bug only happens sometimes
     - Claude wants to rewrite everything
     - the test passes before the fix (it doesn't catch the bug)
     - Claude changed or deleted a test
     - the partner found nothing
     - it works on the laptop but not in Docker
     - work committed to `main` (the week 5 rescue)

  Mark everything not observed "being tested". Give versions in "Tested with".
- [ ] **Slides:** 16-20 slides matching the README, including one with the "fix it" loop vs the four steps, one with the deal screener's Bug 1 entry, and one with its failing test then passing test. Build with `npm run slides`, restore every other week's PDF, render and look at the slides.
- [ ] **Assignment:**
  - **Hand in:**
    - the feedback form you filled in for your partner (file or photo)
    - the link to `BUGS.md` in your repo, with at least one bug written with exact reproduce steps
    - the merged fix PR URL, plus a screenshot of the test failing before the fix and passing after
    - a reflection: what your partner found that you hadn't, and how you avoided the "fix it" loop (or got out of it)
  - **Rubric:**
    - Feedback form for your partner: specific inputs and what happened. 2 points.
    - `BUGS.md` with at least one bug with exact reproduce steps. 2 points.
    - Merged fix PR with a test that failed before the fix and passes after, and nothing unrelated changed. 4 points.
    - Reflection. 2 points.
    - Total: 10 points.
- [ ] **Checks:** `python3 scripts/check_course.py` prints OK. No dashes. A prompt-and-command-to-source table in the report.

### Task 4: Instructor notes, demo script and checklist rows (private repo)

- [ ] `weeks/08-debugging/notes.md` with the four headings:
  - **Timing:** a 75-minute plan: the peer demo (pairing, two 5-minute demos plus form-filling, swap) and the debugging demo, with the rest as work time.
  - **Common problems:**
    - a student's build doesn't run on demo day
    - odd numbers of students or absent partners
    - partners who find nothing, or only say "looks good"
    - private data shown during a demo
    - the "fix it" loop
    - Claude weakening or deleting tests
    - a bug that can't be reproduced
    - the fix committed to `main`
  - **Discussion answers.**
  - **Grading guidance:** worked 10/10 and 6/10 examples that add up, how to check a fix PR for a test that failed first (the screenshot, and the test touching the bug), and how to grade a form whose partner found nothing.

  Also a **demo script:** debug the deal screener's `0.07` bug live from a scratch clone at tag `week-07`, with `systematic-debugging`, the exact prompts and commands, about 15 minutes, and a fallback to the tagged `week-08` files.
- [ ] `weeks/08-debugging/test-checklist.md`: Mac (Apple chip), Mac (Intel) and Windows rows for every README step and troubleshooting row, with identical numbering, in the same format as week 7.
- [ ] No dashes. Commit on `week-08`.

### Task 5: PRs, tag and tracking (controller)

- [ ] Push both branches and open the PRs. Links come first, and ask for a merge commit.
- [ ] After merge, tag `week-08`, close the OpenProject task, and delete the branches and the workspace.
