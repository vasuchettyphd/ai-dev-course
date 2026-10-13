# Week 12 (Evaluation) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 12. Students:
- learn why "it looked right" isn't evidence
- read the Jev case study (no key needed)
- see the deal screener's listing extraction evaluated on 20 cases with real scores
- build their own 20-case test set, with right answers decided first and 5 held out
- write and merge an evaluation script with an offline test
- report a first score, three misses, one change and the held-out score

The deal screener gets an evaluation (tag `week-12`). The week also adds slides, the assignment, instructor notes with a demo script (including an optional live Jev run on the instructor's OpenRouter key) and checklist rows.

**Architecture:**
- Same approach as weeks 9 to 11.
- **Sources:**
  - `advanced/jev/README.md` and its experiments: the numbers and quotes the course uses
  - Anthropic's evaluation docs: success criteria, building tests and grading, quoted where useful
- **Live calls:**
  - Use the workspace Anthropic key in `~/.bashrc`, loaded into one command and never printed.
  - The instructor's optional Jev demo uses `OPENROUTER_API_KEY`, which is allowed because it is Jev. The course itself makes no OpenRouter calls.
- **Who writes what:** the controller writes Tasks 3 and 4 inline, committing per section. Implementers and reviewers are subagents.

**Tech Stack:** Markdown, Marp, Python 3.10+ for the SDK (the deal screener's own logic stays 3.9+), `anthropic==1.13.0`, Docker.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 12 row: "Evaluation | Test sets, accuracy, 'it looked right' isn't evidence (Jev as the case study) | 20-case test set and a reported score". The week 12 design was approved in conversation on 2026-10-13. Decisions:
- Students read Jev; they don't run it.
- The deal screener's evaluation target is the week 9 listing extraction.
- Students build a 20-case test set for their own AI feature (week 9, 10 or 11), with right answers written first and 5 held out.

| Assignment part | Points |
|---|---|
| Test set (20 cases, expected answers, written scoring rule, course-safe) | 3 |
| Evaluation script merged with an offline test, printing score and cost | 3 |
| Report: first score, three misses explained, one change, held-out score, what the score does and doesn't tell you | 4 |

## Global Constraints

- **Audience:** business and non-CS students in week 12. They have everything from weeks 1 to 11, including the key rules, `.env`, the deny rule, the tool rules and the `example-project` setup with its `.venv` and `.env`.
  - Use plain language.
  - Every command and prompt is exact and labelled with where to type it.
- **Platforms:** Mac (Apple chip), Mac (Intel) and Windows (WSL 2 Ubuntu).
- **Evaluation honesty rules,** taught explicitly:
  - write the right answers before running anything
  - never edit the test set to raise the score
  - if an expected answer turns out wrong, fix it with a recorded reason
  - keep 5 cases held out until the one change is done
  - report misses as well as the score
  - 20 cases is small: say what the score can and can't show
- **Keys and data:**
  - The week 9 to 11 key rules apply.
  - Start Claude Code in a window with no key loaded.
  - Test sets use course-safe data only.
  - Results files hold no keys.
- **Facts:**
  - Every fact comes from the Jev README, Anthropic's pages or a live run, with its source.
  - No invented numbers.
  - Anything not observed is marked "being tested".
  - Pin versions.
- **Git rules from weeks 3 to 11:**
  - make a branch first
  - never change `main`
  - PR, read Files changed, merge, then pull
  - keep the repo private
  - answer plain "Yes" to git prompts
  - answer "No" to `reset --hard`, `--force`, `git clean` and `rm -rf`
  - use the week 5 rescue for work committed to `main`
- **Tests:** they never call the real API by default. A live run happens only on request.
- **Formatting:**
  - No em dashes (U+2014) or en dashes (U+2013).
  - The rubric is a table under `## Rubric`, totalling 10.
- **`example-project/`:**
  - It stays the labelled instructor example.
  - Its existing 184 tests stay unchanged.
  - Its offline tests run on the host (with or without SDKs) and in the container.
  - `check_course.py` reports OK.
- **Repos and branches:**
  - Instructor-only material goes in the private repo.
  - Branches: `week-12-evaluation` in the course repo, `week-12` in the instructor repo.
  - The user merges.
  - Links come first, one bare URL per line.

## Review Focus

1. **A call fails partway through the 20 cases** (429, network, no credit). The case is recorded as an error with the plain week 9 sentence. The run continues, and the report shows "errors: N", separate from misses. With no key at all, the run stops before the first case with the no-key sentence. Task 2 tests both.
2. **Expected "not stated" and the model returns a number** (it guessed), **or the reverse** (the model returned null for a stated number). Both count as misses, and the report names them as such. Task 2 tests both.
3. **Rounding.** Expected $1,700 and the model gives 1700.0, or 1699.99 from a yearly-to-monthly conversion, should count as right within the written tolerance of $1. Expected 2400 and got 2400.5 counts as right; got 2402 is a miss. Tests pin the tolerance edges.
4. **The test set file is broken or inconsistent:**
  - a listing file missing for a case
  - a duplicate id
  - a field name misspelt
  - not exactly 20 cases, or not exactly 5 held out

  The evaluator refuses to run, with a plain sentence naming the case. Tests cover each.
5. **Results and repeat runs.** Running twice can give different scores. The report says "run it twice; if the scores differ, look at the cases that changed". The results file includes the date, the model, the case set (dev, held-out or all), the score, every miss and the cost. Running the held-out set is a separate command, so it isn't run by accident.

---

### Task 1: Fact sheet

**Files:** none in the repo. Write the report only.

- [ ] **Step 1: From `advanced/jev/README.md` and `advanced/jev/experiments/`,** record exactly (with line references) the numbers the course will use:
  - the 8/8 triage
  - the 7/8 refund policy, with the 97%-confident wrong answer
  - the 300-case stress test results, including its overall accuracy and where the errors clustered
  - any calibration statement (confidence vs correctness)
  - the total cost and call counts
  - the plainest one-sentence lessons
- [ ] **Step 2: Anthropic's evaluation docs** (platform.claude.com / docs.claude.com):
  - "define success criteria" and "develop tests" (or their current names)
  - grading methods: code-based, human, model-based
  - advice on test set size and edge cases

  Quote exactly with URLs. Also reconfirm the Haiku 5.5 ID and price, and `anthropic` 1.13.0.
- [ ] **Step 3:** Record the deal screener's current extraction behaviour from `example-project/dealscreener/extract.py` and the week 9 live results:
  - what the schema asks for
  - how monthly or yearly conversions are described
  - how null is used
- [ ] **Step 4:** Write the report, with no key in it.

### Task 2: Deal screener evaluation (example-project)

**Files:**
- Create:
  - `example-project/evals/listings/case-01.txt` to `case-20.txt`
  - `example-project/evals/expected.json`
  - `example-project/evals/README.md` (the scoring rule, written before any run)
  - `example-project/dealscreener/evaluate.py`
  - `example-project/tests/test_evaluate.py`
  - `example-project/tests/test_evaluate_live.py`
  - `example-project/evals/results/` (committed results files from the live runs)
- Modify:
  - `example-project/README.md`: "What's here now (week 12)", the week 12 row, "How to evaluate the listing step", and the real scores
  - `.dockerignore`, only if needed

**The 20 cases** are made up and labelled "fictional listings written for this course example". They cover:
- 4 clean listings (all five numbers stated plainly)
- 4 messy ones: tax given monthly, insurance given monthly, "price reduced from", HOA as "association dues"
- 4 with numbers missing (expected null)
- 3 traps:
  - a yearly rent figure
  - a price range ("offers between")
  - two prices (list price vs appraisal)
- 3 with extra numbers that aren't inputs (square feet, year built, bedrooms, a phone number)
- 2 with "no HOA" stated in words

Ids run `case-01` to `case-20`. Five are marked `"held_out": true`, mixed across the categories above. `expected.json` is a list of `{"id": "case-01", "file": "listings/case-01.txt", "held_out": false, "category": "clean", "expected": {"purchase_price": 150000, "monthly_rent": 1700, "yearly_property_tax": 2400, "yearly_insurance": 1200, "monthly_hoa": 0}, "note": "why these are the right answers"}`. `null` means "not stated". Write every expected value and note **before** the first live run, and commit them in their own commit, so the history shows the answers came first.

**Interfaces (`dealscreener/evaluate.py`; standard library at import, SDK only through `extract.make_client`):**
- `TOLERANCE = 1.0`, in dollars.
- `CASES_FILE = "evals/expected.json"`, `RESULTS_DIR = "evals/results"`.
- `class EvalError(Exception)`: its message is one plain sentence naming the case.
- `load_cases(path=CASES_FILE, folder=None) -> list[dict]` validates:
  - exactly 20 cases
  - exactly 5 held out
  - unique ids
  - every file exists
  - every `expected` has exactly the five `extract.FIELDS` keys
  - values are numbers of 0 or more, or null

  Anything else raises `EvalError` (for example "case-07: its listing file evals/listings/case-07.txt is missing.").
- `field_ok(expected, got) -> bool`:
  - both None gives True
  - one None gives False
  - otherwise `abs(expected - got) <= TOLERANCE`
- `@dataclass CaseResult`:
  - `id: str`
  - `category: str`
  - `fields: dict` (field to `(expected, got, ok)`)
  - `error: str | None`
  - `input_tokens: int`
  - `output_tokens: int`
- `run_cases(cases, extract_fn, print_fn=print) -> list[CaseResult]`:
  - `extract_fn(text) -> extract.Extraction` raises on failure.
  - Errors are caught per case: the case is recorded with `error = describe_error(...)` or the `ExtractionError` sentence, and the run continues.
  - It prints one line per case: `case-01  5/5` or `case-04  4/5  monthly_rent: expected 1700, got 20400` or `case-09  ERROR  Too many requests...`.
- `summarise(results) -> dict` returns:
  - `fields_right`
  - `fields_total` (5 per case without an error)
  - `cases_all_right`
  - `cases_scored`
  - `errors`
  - `input_tokens`
  - `output_tokens`
  - `cost` (via `extract.cost_usd`)
- `write_results(results, summary, which, path=None) -> str` writes a Markdown file to `evals/results/<YYYY-MM-DD>-<which>.md`. It contains:
  - the date
  - the model
  - which set
  - the score lines
  - a table of misses
  - the errors
  - the cost

  It returns the path. There are no keys in it.
- `main(argv, print_fn=print, client_factory=extract.make_client) -> int`:
  - It runs `python3 -m dealscreener.evaluate` for the 15 dev cases, `--held-out` for the 5, or `--all`.
  - It calls `extract.load_env_file()` first.
  - With no key, it prints the week 9 no-key sentence and returns 1 before any case runs.
  - It prints `Score: N of M fields right (P%), K of C cases fully right. Errors: E.` and `Cost: about $X.`, then `Saved: <path>`.
  - It returns 0 even with misses, and 1 only for a setup problem.
  - `--held-out` prints a reminder first: "You are running the held-out cases. Run them once, after your change, and report what you get."

**Tests (`tests/test_evaluate.py`, offline):**
- `field_ok`:
  - edges at 1.0 and 1.01
  - None/None, None/number and number/None
- `load_cases`:
  - the real file passes
  - each broken variant raises with the case named: missing file, duplicate id, a misspelt field, 19 cases, 4 held out, a negative value
- `run_cases` with a fake `extract_fn` that returns scripted values per case:
  - a perfect case
  - one wrong field
  - a guess where null was expected
  - a null where a number was expected
  - an `ExtractionError`
  - an API error with `status_code` 429

  Lines are printed as specified, and the run continues after errors.
- `summarise`: the counts and cost arithmetic.
- `write_results`:
  - the file has the score, the misses table and the date
  - it contains no `sk-ant-`, written to a temp folder
- `main`:
  - no key gives the no-key sentence, returns 1, and calls `extract_fn` zero times
  - `--held-out` prints the reminder and runs only the 5
  - the default runs only the 15
  - `--all` runs 20
  - an unknown flag prints usage and returns 2

**Live test (`tests/test_evaluate_live.py`):** skipped unless `RUN_LIVE_TESTS=1` and the key is set. It runs the 15 dev cases and asserts that `fields_right / fields_total >= 0.8`. Before using this floor, check the first live score: if the real score is lower, set the floor just under it and record why.

**Steps:**
- [ ] **Step 1:** Write the 20 listings, `expected.json` and `evals/README.md` (the scoring rule). Commit them alone, before any run.
- [ ] **Step 2:** Write `tests/test_evaluate.py`, watch it fail, then write `evaluate.py` until it passes. Run the whole suite with plain `python3`. The old 184 tests stay unchanged; record the new total.
- [ ] **Step 3: Live**, in a `python:3.12-slim` container with `ANTHROPIC_API_KEY` passed by name (loaded from `~/.bashrc` for that one command, never printed):
  - run the dev set **twice**
  - then run the held-out set once
  - then `--all` once

  Record every score, miss, error and cost. Commit the results files. Write in the report which misses are the model's fault and which point to an unclear expected answer. **Do not change the expected answers after seeing results**, unless a note explains a real mistake in them, recorded in `evals/README.md` under "Corrections".
- [ ] **Step 4: Optionally, one change.** If the dev misses show a clear pattern (for example yearly rent), make one small prompt or description change in `extract.py`. Keep the week 9 tests passing. Rerun the dev set, then the held-out set once. Record before and after. If no clear pattern, skip this step and say so.
- [ ] **Step 5:** Docker:
  - build `dealscreener-w12`
  - run the offline tests in it
  - `ls -a /app` shows no `.env`
  - remove the image
- [ ] **Step 6:** Update the example README with the real scores, the misses and the cost. Run `check_course.py`, check there are no dashes, and confirm `git status` shows no `.env`. Commit early and often, with the Co-Authored-By line.

### Task 3: README, slides and assignment (controller writes, committing per section)

**Files:** `weeks/12-evaluation/README.md` (replace the stub), `slides.md`, `slides.pdf`, `assignment.md`.

- [ ] **README** follows the approved design, steps 1 to 7:
  1. **"It looked right" isn't evidence.** Cover:
     - test set
     - expected answers decided first
     - scoring rule
     - score
     - misses
     - Anthropic's quotes on success criteria and tests
  2. **Case study: Jev**, as a reading of `advanced/jev` with numbers from the fact sheet:
     - 8 easy cases looked perfect
     - the refund policy was 7/8, with a 97%-confident wrong answer
     - the 300-case results

     Three lessons:
     - errors cluster where the rules bite
     - confidence isn't correctness
     - small test sets hide things
  3. **The deal screener's evaluation,** run live: commands, real output, real scores, the misses read together, the cost.
  4. **Build your own 20-case test set** for the AI feature from week 9, 10 or 11:
     - a mix of cases
     - expected answers written first
     - 5 held out
     - course-safe data
     - a written scoring rule (exact, within a tolerance, or right category; for free text, a checklist rubric graded by a person, with model-based grading mentioned as an option from Anthropic's docs)
  5. **Write the evaluation script** on branch `eval`, using Superpowers and a prompt with these guardrails:
     - fake-model offline test
     - errors don't stop the run
     - cost printed
     - results saved
     - held-out set separate
     - no keys
  6. **Read the misses, make one change, score the held-out set once.** Cover the honesty rules and what a score of 17/20 does and doesn't tell you.
  7. **Review, PR and check it worked,** with troubleshooting:
     - scores differ between runs
     - an expected answer was wrong
     - every case errors (key)
     - 429 partway through
     - cost
     - tolerance
     - free-text grading disagreements
     - week 9's Anthropic rows
     - the week 5 rescue
- [ ] **Slides:** 16 to 20, including:
  - "it looked right"
  - the Jev numbers
  - the parts of an evaluation
  - the deal screener's real score and misses
  - held-out
  - the honesty rules
  - the assignment

  Build only this week's PDF, render it, and look at the dense slides.
- [ ] **Assignment:** hand-ins and rubric as in the spec decisions above, totalling 10.
- [ ] **Checks:** `check_course.py` OK, no dashes, and the numbers match the fact sheet and the live runs.

### Task 4: Instructor notes, demo script and checklist (private repo, controller writes)

- [ ] `weeks/12-evaluation/notes.md`:
  - **Timing:** a 75-minute plan.
  - **Demo script:**
    - the deal screener evaluation from a scratch clone at tag `week-12`, in one window with no key loaded in Claude Code's sense (the evaluator reads `.env` itself)
    - an optional live Jev run with the instructor's `OPENROUTER_API_KEY` (the Jev scripts' exact command from the README, the key never on screen, the cost from the Jev README)
  - **Common problems:**
    - students editing the test set to raise the score
    - test sets that are too easy
    - free-text features (RAG answers) needing a human rubric
    - 429 in class
    - expected answers that were wrong
    - non-Python projects
  - **Discussion answers.**
  - **Grading guidance:**
    - 10/10 and 6/10 examples that add up
    - checking the commit history shows expected answers came before results
- [ ] `weeks/12-evaluation/test-checklist.md`: three tables with identical numbering, generated from one row list, covering every README step and troubleshooting row.
- [ ] No dashes and no keys. Commit on `week-12`.

### Task 5: PRs, tag and tracking (controller)

- [ ] Key scan on both branches (`sk-ant-`, `AIza`, `sk-or-`). Only fakes are allowed.
- [ ] Push both branches and open the PRs. Links come first, and ask for a merge commit.
- [ ] After merge:
  - tag `week-12`
  - check the tag clone
  - close the OpenProject task
  - delete the branches and the workspace
