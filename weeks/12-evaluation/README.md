# Week 12: Evaluation

**Goal:** find out how well your AI feature really works, with evidence instead of impressions. You'll read how the course measured another model (Jev), watch the deal screener's listing step get scored on 20 test cases, build your own 20-case test set with the right answers written first, write a script that scores your feature, and report what the score does and doesn't tell you, merged through a pull request.

**Time:** plan for about 2 to 3 hours of your own time after class (an estimate); writing good test cases takes longer than people expect. **Cost:** a few Claude calls from your week 9 API credit: running the deal screener's 20 cases once cost under a cent (step 3).

**Tested with** (13 October 2026; these are the versions tested, yours may be newer):

- `anthropic` 1.13.0 and `claude-haiku-5-5`, with real evaluation runs from a container (the scores below are from those runs).
- The deal screener's new evaluation and its tests.
- **Being tested:** everything inside a signed-in Claude Code session, everything on GitHub, and every step on a Mac or in Windows (WSL).

## Before you start

You need:

- Weeks 9 to 11 done: an AI feature in your `semester-project` (week 9, 10 or 11), your keys in `.env`, the `Read(./.env)` deny rule, and the course repo's `example-project` set up with its `.venv` and `.env` (week 10 step 4a).
- `gh` signed in to **your** GitHub account, and Claude Code signed in with your Claude Pro account.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows. As in week 11, start Claude Code only in a window where no key is loaded.

### How you'll work this week

As in weeks 9 to 11: plain-English prompts, plain **Yes** for git, a branch first, a pull request last, and the key rules.

**The evaluation honesty rules, new this week:**

1. **Write the right answers before you run anything.** Commit them first, so your history shows it.
2. **Never change the test set to make the score go up.** If a right answer turns out to be wrong, fix it, and write down why.
3. **Keep 5 cases aside** (the **held-out** cases) and run them only once, after you've made your one change.
4. **Report the misses, not just the score.**
5. **Say what your score can't show.** Twenty cases is a small sample.

| Claude asks to | Choose |
|---|---|
| Create your test cases, expected answers and scoring rule on your `eval` branch | **Yes** |
| Change an expected answer **after** a run | **No**, unless you agree it was a real mistake: then ask it to record the reason |
| Write the evaluation script and its tests | **Yes** |
| Run the evaluation against the real model | **Yes**, in a window you choose: it costs a little credit |
| Read or print `.env`, or put a key in any file (including a results file) | **No** |
| `git add`, `git commit`, `git push` on your `eval` branch, `gh pr create` | plain **Yes**, after `git status` shows no `.env` |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

## Steps

### 1. "It looked right" isn't evidence

You've tried your AI feature a few times and the answers looked good. That tells you less than it feels like. You probably tried easy cases, you remember the hits better than the misses, and you can't compare one version with the next.

An **evaluation** fixes that. It has four parts:

1. A **test set**: a fixed list of cases, including hard ones.
2. **Expected answers**, decided **before** you run anything, so the model's answer can't sway you.
3. A **scoring rule** that says exactly what counts as right (an exact match, a number within a tolerance, the right category).
4. A **score**, and the list of **misses**, which is where the learning is.

Anthropic's guide (<https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>, read 13 October 2026) says a good success criterion is "Specific: Clearly define what you want to achieve" and "Measurable: Use quantitative metrics or well-defined qualitative scales." It also says to "factor in edge cases", such as "Irrelevant or nonexistent input data" and "Ambiguous test cases where even humans would find it hard to reach an assessment consensus".

**About the size.** Anthropic's guide gives no minimum number of cases; its own examples use from 50 to 10,000, and it says "Prioritize volume over quality: More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals." This week does the opposite on purpose: 20 cases, each with an answer you wrote and can check yourself. Twenty cases can show **big failures and patterns** ("it always gets yearly rent wrong"). They can't give a precise rate: each case is 5% of the score, so 17 out of 20 against 18 out of 20 is one case, which could be luck.

### 2. Case study: Jev

The course's advanced tutorial [Jev](../../advanced/jev/README.md) measured a model (TypeSafe's Jev 1.13) with about 1,130 real calls, costing "a few cents" in total. Read its README; you don't need to run it. Three lessons from it:

**Small, easy tests look perfect.** On 8 easy support tickets, Jev picked the right team 8 times out of 8, all at confidence 1.00. On a refund policy with 8 cases it got 7 right, and the miss was a $100 refund requested on day 31: it answered "send to a manager" when the rule said deny, and it was 97% confident.

**Errors cluster where the rules bite.** The author then generated 300 cases from a harder four-step refund policy (300 cases from 36 distinct customer messages, one run, with the messages and the right answers written by the author). Asked directly, Jev got 211 of 300 right (70%); with the facts prepared for it first, 236 of 300 (79%); and a hybrid, where code applied the rules and Jev only read the message, got 300 of 300. But for cases within 3 days of a refund window's edge, Jev alone got only 63 of 129 right (49%). The largest single group of its misses (30 of 89) was defective items 366 to 400 days old, which the policy said to deny.

**Confidence isn't correctness.** When the prepared answers were kept only if Jev was at least 90% confident, 174 of 179 were right (97%): better, but 5 confident wrong answers remained.

What that means for you: a feature that looks perfect on a few easy cases can be wrong exactly where it matters, while sounding just as sure. Only a test set with hard cases, scored by a rule you wrote first, shows that.

### 3. The deal screener's evaluation

The deal screener's listing step (week 9) reads a pasted listing and pulls out five numbers. Its evaluation is in [`example-project/evals/`](../../example-project/evals/):

- 20 made-up listings: clean ones, messy ones (monthly tax, "association dues"), ones with numbers missing, traps (a yearly rent, a price range, two prices), ones full of extra numbers that aren't inputs, and ones saying "no HOA" in words;
- `expected.json`: the right five numbers for each, with a note on why, and `null` where the listing doesn't say;
- the scoring rule in [`evals/README.md`](../../example-project/evals/README.md): a number is right if it's within $1 of the expected one; `null` is right only if the model also says "not stated"; a guess where the listing gives nothing is a miss.

All of that was committed **before** the first run (look at the commit history: the commit "Week 12: 20 evaluation listings, expected answers and scoring rule, written before any run" comes before the evaluator and every results file). Five of the cases are held out.

**a. Run it.** In your terminal, in `~/ai-dev-course/example-project`, with `(.venv)` showing (the evaluator reads your key from this folder's `.env` itself):

```bash
git pull
python3 -m dealscreener.evaluate
```

It runs the 15 practice ("dev") cases, prints one line per case (`case-01  5/5`, or the fields it missed), then the score and the cost, and saves the results in `evals/results/`. `--held-out` runs the 5 held-out cases and first reminds you to run them only once; `--all` runs all 20.

**b. The course's results** (13 October 2026, Claude Haiku 5.5):

| Run | Score | Cases fully right | Cost |
|---|---|---|---|
| Dev, first run | 75 of 75 fields (100%) | 15 of 15 | about $0.0017 |
| Dev, second run | 75 of 75 fields (100%) | 15 of 15 | about $0.0016 |
| Held out, run on its own once | 24 of 25 fields (96%) | 4 of 5 | about $0.0005 |
| All 20 | 100 of 100 fields (100%) | 20 of 20 | about $0.0023 |

The `--all` run includes the 5 held-out cases, so the course ran them a second time to show you the flip below. In your own work, run `--held-out` once and leave `--all` until your report is written.

**c. Read the miss.** Case 14 says "The seller will consider offers between $180,000 and $195,000." There's no single asking price, so the written answer is `null`. In the held-out run the model answered 187500, the middle of the range: a guess. In the `--all` run, on the very same listing, it answered `null`. **The same input got two different answers in two runs.** That's why you run an evaluation more than once, and why one good run proves little.

**d. What these 20 cases show, and what they don't.** They show no big failure: monthly tax, yearly rent, a quarterly HOA, "no HOA" in words, missing and extra numbers were all read right. They don't show a precise accuracy rate: 19 of 20 against 20 of 20 is one case. And a perfect dev score suggests the set may be **too easy** for this model: harder cases (two rents, a weekly figure, a typo in a number) would teach more. The example README explains why no change was made: the dev cases had no misses, and changing the program because of a held-out case would spoil the held-out set.

### 4. Build your own test set

> **Being tested:** steps 4 to 7 need a signed-in session and are being tested. The deal screener's version was built and run on 13 October 2026.

**a. Make the branch first.** In a **new** terminal window (no key loaded), `cd ~/semester-project`, start `claude`, and in Claude Code:

```text
Switch to main, pull the latest changes from GitHub, then create a new branch called eval and switch to it.
```

**b. Pick what to evaluate:** your week 9 AI feature, your week 10 RAG, or your week 11 tool. It needs an answer you can check.

**c. Write 20 cases.** Course-safe data only (week 10 step 5c). Mix them:

| Kind | How many | Example |
|---|---|---|
| Clean, easy | 4 or 5 | the input your feature was built for |
| Messy | 4 or 5 | typos, odd wording, extra detail |
| Missing or impossible | 3 or 4 | the right answer is "not stated", "I don't know" or "ask the user" |
| Traps | 3 or 4 | the thing that would fool a careless reader (two dates, a yearly figure, a negation) |
| Edge cases | 2 or 3 | right at a limit, very long, or empty |

**d. Write the right answers first,** for every case, with one line saying why. Mark 5 cases as **held out**, mixed across the kinds.

**e. Write your scoring rule** in one short paragraph, before any run:

- **numbers:** right if within a tolerance you choose (say why);
- **categories or labels:** right if exactly equal;
- **free text** (a RAG answer, a summary): a short checklist per case ("names the right document", "says the price", "doesn't invent a number"), graded by you. Anthropic's guide lists three ways to grade: code ("Fastest and most reliable"), a person ("Avoid if possible", because it's slow), or another model ("Test to ensure reliability first then scale"). For 20 cases, code or you is fine.

**f. Commit them alone, first.** In Claude Code:

```text
Commit only the test cases, the expected answers and the scoring rule, with the message "Week 12 test set and scoring rule, written before any run". Don't write any other code yet.
```

### 5. Write the evaluation script

In Claude Code (replace the parts in angle brackets):

```text
/superpowers:writing-plans Write an implementation plan for an evaluation script for <my feature>: read the test cases and expected answers I just committed, run my feature on each case, score each answer with my scoring rule in <file>, and print one line per case, the score, the misses and the cost. Rules: never change the test cases or the expected answers; run the 15 dev cases by default and the 5 held-out cases only with --held-out (print a reminder to run them once); if a call fails, record that case as an error with a plain sentence and carry on; stop before the first case if there's no API key; save each run's results (date, model, score, misses, cost) to a file, never a key; read the key only from the environment and never read or print .env; include offline tests with a fake model, including a miss, an error and the held-out flag, and never call the real API in the tests. I'm not a programmer, so keep each task small.
```

Then build it with `/superpowers:subagent-driven-development` as in weeks 9 to 11. Answer as in the table at the top.

### 6. Run it, read the misses, make one change, test the held-out cases

In a second terminal window (not the Claude Code one), with your project's `.venv` active and your key available the way your project loads it:

1. **Run the dev cases twice.** Write down both scores. If they differ, look at the cases that changed: that's the model answering differently, not your code.
2. **Read every miss.** For each one, decide: is it the model's mistake, or was **your expected answer** wrong? If yours was wrong, fix it and write the reason in your scoring rule file under "Corrections" (never quietly).
3. **Make one change** that should fix a pattern in the misses (a clearer prompt, a schema description, a check in your code). Run the dev cases again.
4. **Run the held-out cases, once.** That score is your honest estimate, because those cases didn't shape your change.

Write down: the first dev score, three misses and why, your change, the new dev score, and the held-out score. You hand these in.

### 7. Review and finish

**a. Review it** with `safe-and-private`, as in weeks 9 to 11, focused on: keys in any file or results file (search tracked files with `git grep` only), test data that isn't course-safe, and tests that call the real API by default. Add a "## Week 12: evaluation review" section to `REVIEW.md` and triage it.

**b. Push, open a pull request, read Files changed** (the test cases and expected answers, the scoring rule, the script and its tests, the results files, `REVIEW.md`; no `.env`, no real key), **merge on GitHub, then pull.** In the pull request's Commits tab, the test set commit should come before the script.

The deal screener's week 12 changes are on this page (it works once week 12 is published): <https://github.com/vasuchettyphd/ai-dev-course/compare/week-11...week-12>.

## Check it worked

- Your test set (20 cases, 5 held out) and scoring rule were committed before your first run.
- Your script runs the dev cases, prints the score, the misses and the cost, and saves a results file without any key in it.
- Your tests pass with `.env` moved out of the folder.
- You have: two dev scores, three misses explained, one change, and one held-out score.

## Troubleshooting

| What you see | What to do |
|---|---|
| The dev score changes between runs | Normal: the model doesn't answer the same way every time. Look at the cases that changed, and report both scores. |
| An expected answer turns out to be wrong | Fix it, and record the reason under "Corrections" in your scoring rule file. Never change answers just to raise the score. |
| Every case says ERROR | Usually the key: the first line says so. Check the key is in the project's `.env`, as in week 9. |
| ERROR on some cases partway through (429) | Too many calls too quickly: wait a minute and run again. The run carries on past errors, and the score counts only the cases that ran. |
| A score of 100% | Your test set may be too easy: add harder cases (keep the 20 by swapping, and write the new answers first). |
| Free-text answers are hard to score | Use a short checklist per case and grade by hand; write the checklist before you run. |
| Numbers that should match are scored as misses | Check your tolerance: rounding (1699.99 vs 1700) needs a small tolerance, written into your rule. |
| The results file wasn't saved | The folder may not be writable (in Docker, use the `--user` and `-v` parts from the deal screener's README); the score printed on screen is still right. |
| Anthropic errors (401, 429, credit, workspace) | See [week 9's Troubleshooting](../09-calling-a-model/README.md#troubleshooting). |
| Work was committed to `main` | Use [week 5's rescue](../05-building-with-ai/README.md#if-it-committed-to-main). |
