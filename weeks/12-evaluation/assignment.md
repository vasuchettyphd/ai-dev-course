# Week 12 assignment: Evaluation

## What to do

Follow the [week 12 README](README.md) on your own laptop, in your private `semester-project` repo, and collect three things.

On the Gemini path? Read [week 12 on the Gemini path](gemini.md) too: the [hand-in](gemini.md#hand-in-differences) is the same, except you copy the cost line your script prints (token counts, real cost $0 (free tier), and what it would cost on the paid tier).

**(a) Your test set.** The link to your 20 test cases, their expected answers (each with a one-line reason) and your written scoring rule, on `main` after the merge. Five cases are marked held out. Course-safe data only. In the pull request's **Commits** tab, the commit that adds them must come **before** your evaluation script (merge with "Create a merge commit" this week, so `main` keeps that order too).

**(b) Your merged evaluation script.** The address of the merged pull request from your `eval` branch. Its **Files changed** must show the script, its offline tests (a fake model, including a miss and an error), the saved results files and `REVIEW.md` with the week 12 section. **No `.env` and no real key** anywhere, including the results files.

**(c) A short report,** about one page:

1. **First score:** your two dev runs (fields or cases right, out of how many) and their cost.
2. **Three misses:** for each, the case, what was expected, what your feature gave, and why you think it happened (the model, your code, or your expected answer). If you have fewer than three, explain the ones you have and say which harder cases you'd add. List any expected answers you corrected, with the reason (or say "none").
3. **One change:** what you changed, and your new dev score.
4. **Held-out score:** the result of your one held-out run (if you ran it more than once, say so).
5. **What your score does and doesn't tell you:** in a few sentences, with your 20 cases in mind.

Never put a key, a password, a sign-in code or anything from your `.env` file in your hand-in.

## What to hand in

- One document with the link to your test set, the pull request's address and your report.

Submit it the way your course site says.

## Rubric

| Criterion | Points |
|---|---|
| Test set: 20 cases with expected answers and reasons, 5 held out, a written scoring rule, course-safe, committed before the script | 3 |
| Merged evaluation script: offline tests with a fake model, prints the score, misses and cost, saves results, no key anywhere | 3 |
| Report: two dev scores (1 point), three misses explained, or all if fewer, plus any corrections (1 point), one change with the new score and the held-out score (1 point), what the score does and doesn't tell you (1 point) | 4 |
