# Week 12: Evaluation

**Goal:** find out how well your AI feature really works, with evidence instead of impressions. You'll read how the course measured another model (Jev), watch the deal screener's listing step get scored on 20 test cases, build your own 20-case test set with the right answers written first, write a script that scores your feature, and report what the score does and doesn't tell you, merged through a pull request.

**Time:** plan for about 2 to 3 hours of your own time after class (an estimate); writing good test cases takes longer than people expect. **Cost:** one Claude call per case per run, so about 50 calls for your own runs (an estimate: three dev runs and one held-out run), plus about 15 for the deal screener in step 3, from your week 9 API credit: running the deal screener's 20 cases once cost under a cent (step 3).

**Tested with** (13 October 2026; these are the versions tested, yours may be newer):

- `anthropic` 1.13.0 and `claude-haiku-5-5`, with real evaluation runs from a container (the scores below are from those runs).
- The deal screener's new evaluation and its tests.
- Windows (WSL), 29 October 2026: the deal screener's runs (dev 75 of 75 twice, held out 25 of 25, Docker with `--user`) and steps 4 to 7a in a signed-in Claude Code session. **Being tested:** everything on GitHub, and every step on a Mac.

## Before you start

You need:

- Weeks 9 to 11 done: an AI feature in your `semester-project` (week 9, 10 or 11), your keys in `.env`, the `Read(./.env)` deny rule, and the course repo's `example-project` set up with its `.venv` and `.env` (week 10 step 4a).
- `gh` signed in to **your** GitHub account, and Claude Code signed in with your Claude Pro account.

On the **Gemini path** (no paid API credit, set up in week 9)? Almost everything is the same: read [week 12 on the Gemini path](gemini.md) first for the few differences.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows. As in week 11, start Claude Code only in a window where no key is loaded. The commands are the same on a Mac with an Apple chip, an Intel Mac and Windows; on Windows, stay in your Ubuntu home folder (paths start `/home/<you>/`, never `C:\`).

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
| Run the evaluation against the real model | **No**: you run it yourself in a second window (step 6), never the Claude Code one |
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

**Errors cluster where the rules bite.** The author then generated 300 cases from a harder four-step refund policy (300 cases from 36 distinct customer messages, one run, with the messages and the right answers written by the author). Asked directly, Jev got 211 of 300 right (70%); with the facts prepared for it first, 236 of 300 (79%); and a hybrid, where code applied the rules and Jev only read the message, got 300 of 300 (the Jev README warns not to over-read this: the 300 cases came from 36 distinct messages, Jev read all 36 right, and plain code did the rest). But for cases within 3 days of a refund window's edge, Jev alone got only 63 of 129 right (49%). The largest single group of its misses (30 of 89) was defective items 366 to 400 days old, which the policy said to deny (counted from the run's saved results, [`refund_stress_test_seed7.json`](../../advanced/jev/experiments/results/refund_stress_test_seed7.json); the Jev README sums this up as "a defective item a few days past 365 being refunded anyway").

**Confidence isn't correctness.** When the prepared answers were kept only if Jev was at least 90% confident, 174 of 179 were right (97%): better, but 5 confident wrong answers remained.

What that means for you: a feature that looks perfect on a few easy cases can be wrong exactly where it matters, while sounding just as sure. Only a test set with hard cases, scored by a rule you wrote first, shows that.

### 3. The deal screener's evaluation

The deal screener's listing step (week 9) reads a pasted listing and pulls out five numbers. Its evaluation is in [`example-project/evals/`](../../example-project/evals/):

- 20 made-up listings: clean ones, messy ones (monthly tax, "association dues"), ones with numbers missing, traps (a yearly rent, a price range, two prices), ones full of extra numbers that aren't inputs, and ones saying "no HOA" in words;
- `expected.json`: the right five numbers for each, with a note on why, and `null` where the listing doesn't say;
- the scoring rule in [`evals/README.md`](../../example-project/evals/README.md): a number is right if it's within $1 of the expected one; `null` is right only if the model also says "not stated"; a guess where the listing gives nothing is a miss.

All of that was committed **before** the first run (look at the commit history: the commit "Week 12: 20 evaluation listings, expected answers and scoring rule, written before any run" comes before the evaluator and every results file). Five of the cases are held out.

**a. Run it.** Type in: the Terminal on a Mac (Apple chip or Intel), or the Ubuntu window on Windows; in `~/ai-dev-course/example-project`, with `(.venv)` showing and **no** `set -a` line (the evaluator reads your key from this folder's `.env` itself and never prints it). Don't run it in a window running Claude Code.

```bash
git pull
python3 -m dealscreener.evaluate
```

It runs the 15 practice ("dev") cases, prints one line per case (`case-01  5/5`, or the fields it missed), then the score and the cost, and saves the results in `evals/results/`. `--held-out` runs the 5 held-out cases and first reminds you to run them only once; `--all` runs all 20. The results files it saves in your course folder are just for you: `git status` shows them, and you can delete them by name when you're done. To run it in Docker instead, use the command in the [example README's evaluation section](../../example-project/README.md#how-to-evaluate-the-listing-step) (it needs the `--user` and `-v` parts to save results).

**b. The course's results** (13 October 2026, Claude Haiku 5.5):

| Run | Score | Cases fully right | Cost |
|---|---|---|---|
| Dev, first run | 75 of 75 fields (100%) | 15 of 15 | about $0.0017 |
| Dev, second run | 75 of 75 fields (100%) | 15 of 15 | about $0.0016 |
| Held out, run on its own once | 24 of 25 fields (96%) | 4 of 5 | about $0.0005 |
| All 20 | 100 of 100 fields (100%) | 20 of 20 | about $0.0023 |

The `--all` run includes the 5 held-out cases, so they ran a second time; that is how the flip below showed up. In your own work, run `--held-out` once and leave `--all` until your report is written.

**c. Read the miss.** Case 14 says "The seller will consider offers between $180,000 and $195,000." There's no single asking price, so the written answer is `null`. In the held-out run the model answered 187500, the middle of the range: a guess. In the `--all` run, on the very same listing, it answered `null`. **The same input got two different answers in two runs.** That's why you run an evaluation more than once, and why one good run proves little.

**d. What these 20 cases show, and what they don't.** They show no big failure: monthly tax, yearly rent, a quarterly HOA, "no HOA" in words, missing and extra numbers were all read right. They don't show a precise accuracy rate: 19 of 20 against 20 of 20 is one case. And a perfect dev score suggests the set may be **too easy** for this model: harder cases (two rents, a weekly figure, a typo in a number) would teach more. The [example README](../../example-project/README.md) explains why no change was made: the dev cases had no misses, and changing the program because of a held-out case would spoil the held-out set.

### 4. Build your own test set

> Steps 4 to 7a were tested in a signed-in session on Windows (WSL) on 29 October 2026; the GitHub part of 7b and the Mac are being tested. The deal screener's version was built and run on 13 October 2026.

**a. Make the branch first.** In a **new** terminal window (no key loaded), `cd ~/semester-project`, start `claude`, and in Claude Code:

```text
Switch to main, pull the latest changes from GitHub, then create a new branch called eval and switch to it.
```

Plain **Yes** to each git command. Check: "What branch am I on?" says `eval`.

**b. Check the safety setup from week 9.** In a second terminal window, in `~/semester-project`:

```bash
git check-ignore .env
grep -c 'Read(./.env)' .claude/settings.json
```

The first prints `.env`; the second prints `1`. If either doesn't, redo week 9 step 5b before going on.

**c. Pick what to evaluate:** your week 9 AI feature, your week 10 RAG, or your week 11 tool. It needs an answer you can check.

**d. Write 20 cases.** Course-safe data only (week 10 step 5c). Mix them:

| Kind | How many | Example |
|---|---|---|
| Clean, easy | 4 or 5 | the input your feature was built for |
| Messy | 4 or 5 | typos, odd wording, extra detail |
| Missing or impossible | 3 or 4 | the right answer is "not stated", "I don't know" or "ask the user" |
| Traps | 3 or 4 | the thing that would fool a careless reader (two dates, a yearly figure, a negation) |
| Edge cases | 2 or 3 | right at a limit, very long, or empty |

**e. Write the right answers first,** for every case, with one line saying why. Mark 5 cases as **held out**, mixed across the kinds.

**f. Write your scoring rule** in one short paragraph, before any run:

- **numbers:** right if within a tolerance you choose (say why);
- **categories or labels:** right if exactly equal;
- **free text** (a RAG answer, a summary): a short checklist per case ("names the right document", "says the price", "doesn't invent a number"), graded by you. Anthropic's guide lists three ways to grade: code ("Fastest and most reliable"), a person ("Avoid if possible", because it's slow), or another model ("Test to ensure reliability first, then scale"). For 20 cases, code or you is fine.

**g. Commit them alone, first.** In Claude Code:

```text
Commit only the test cases, the expected answers and the scoring rule, with the message "Week 12 test set and scoring rule, written before any run". Don't write any other code yet.
```

### 5. Write the evaluation script

In Claude Code (replace the parts in angle brackets):

```text
/superpowers:writing-plans Write an implementation plan for an evaluation script for <my feature>: read the test cases and expected answers I just committed, run my feature on each case, score each answer with my scoring rule in <file>, and print one line per case, the score, the misses and the cost. Rules: never change the test cases or the expected answers; run the 15 dev cases by default and the 5 held-out cases only with --held-out (print a reminder to run them once); if a call fails, record that case as an error with a plain sentence and carry on; stop before the first case if there's no API key; save each run's results (date, model, score, misses, cost) to its own new file in evals/results/, never a key; read the key only from the environment and never read or print .env; include offline tests with a fake model, including a miss, an error and the held-out flag, and never call the real API in the tests. I'm not a programmer, so keep each task small.
```

Then build it with `/superpowers:subagent-driven-development` as in weeks 9 to 11. Answer as in the table at the top. At the end it may ask to `rm -rf` its own scratch folder (`.superpowers/sdd/...`): answer No as the table says; the folder is git-ignored and can stay.

### 6. Run it, read the misses, make one change, test the held-out cases

Type in: a second terminal window, **never** the one running Claude Code, in `~/semester-project`, with your project's `.venv` active. Load your key the way your feature's README says: for most of you that's `set -a; . ./.env; set +a`, as in week 9 (skip it if your program reads `.env` itself, as the deal screener does). Never print the key.

1. **Run the dev cases twice.** Write down both scores. If they differ, look at the cases that changed: that's the model answering differently, not your code.
2. **Read every miss.** For each one, decide: is it the model's mistake, or was **your expected answer** wrong? If yours was wrong, fix it and write the reason in your scoring rule file under "Corrections" (never quietly).
3. **Make one change** that should fix a pattern in the misses (a clearer prompt, a schema description, a check in your code). Run the dev cases again.
4. **Run the held-out cases, once.** That score is your honest estimate, because those cases didn't shape your change.

**Commit as you go.** After each run and after your change, in Claude Code:

```text
Commit the new results files, and my change if there is one, with a message saying which run or change this was. Don't change the test cases or the expected answers, except a correction I've recorded under "Corrections".
```

Plain **Yes**, after `git status` shows no `.env`.

**Run your tests offline once:** with `.env` moved out of the folder, as in week 9 steps 5e and 5f (in a window with no key loaded); they must all pass.

Write down: the two dev scores, three misses and why (if you have fewer than three, all of them, and the harder cases you'd add), any corrections with their reasons, your change, the new dev score, and the held-out score. You hand these in.

When you read your scores, remember what 20 cases can show (step 1): a pattern of misses, yes; a precise rate, no. With 20 cases, 17 against 18 is one case.

### 7. Review and finish

**a. Review it with `safe-and-private`.** In Claude Code:

```text
Run the safe-and-private reviewer as a subagent on the files changed on this branch compared with main (git diff main --name-only). Focus on: whether an API key could be printed, logged or saved in any file, including the results files (search tracked files with git grep only, never open .env); whether any test data isn't course-safe; whether any test calls the real API by default; whether any expected answer changed after a results file without a reason under "Corrections". Then add a section at the end of REVIEW.md, headed "## Week 12: evaluation review", with one table with the columns #, Label, Finding (file:line), Found by, Decision, Reason, numbering the findings E1, E2 and so on. Leave Decision and Reason empty. Do not change any file except REVIEW.md.
```

Triage, fix and commit as in week 6 steps 5 and 6.

**b. Push, open a pull request, read Files changed** (the test cases and expected answers, the scoring rule, the script and its tests, the results files, `REVIEW.md`; no `.env` and no real key: use the browser's Find for `sk-ant-` and `ANTHROPIC_API_KEY=`, including in the results files), as in week 10 step 7. In the pull request's **Commits** tab, the test set commit must come before the script. **This week, merge with "Create a merge commit"**, not "Squash and merge": a squash would fold the test set and the script into one commit on `main`, and the order is what assignment part (a) checks. Then pull.

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
| `No API key found ...` before any case runs | The key isn't loaded: check it's in the project's `.env` (and loaded, if your program needs `set -a`), as in week 9. |
| Every case says ERROR, then "Every case failed" | The key was found but refused, or there's no credit: read the first ERROR sentence, then see week 9's Troubleshooting. |
| ERROR on some cases partway through (429) | Too many calls too quickly: wait a minute and run again. The run carries on past errors, and the score counts only the cases that ran. |
| The run costs more than you expected | Each case is one call. Check the `Cost:` line after each run, and your spend limit (week 9 step 2c). |
| A score of 100% | Your test set may be too easy: add harder cases (keep the 20 by swapping, and write the new answers first). |
| Free-text answers are hard to score | Use a short checklist per case and grade by hand; write the checklist before you run. |
| Numbers that should match are scored as misses | Check your tolerance: rounding (1699.99 vs 1700) needs a small tolerance, written into your rule. |
| The results file wasn't saved | The folder may not be writable (in Docker, use the `--user` and `-v` parts from the deal screener's README); the score printed on screen is still right. |
| Anthropic errors (401, 429, credit, workspace) | See [week 9's Troubleshooting](../09-calling-a-model/README.md#troubleshooting). |
| Work was committed to `main` | Use [week 5's rescue](../05-building-with-ai/README.md#if-it-committed-to-main). |
