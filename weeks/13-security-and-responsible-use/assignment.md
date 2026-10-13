# Week 13 assignment: Security and responsible use

## What to do

Follow the [week 13 README](README.md) on your own laptop, in your private `semester-project` repo, and collect three things.

**(a) Your injection test and defence.** The address of the merged pull request from your `security` branch. Its **Files changed** must show your 5 hostile cases with their expected answers, the `--injection` option and its offline tests, your one defence and its tests, and the results files. In its **Commits** tab, the hostile cases commit must come **before** the defence (merge with "Create a merge commit"). **No `.env` and no real key** anywhere, including the results files. In your report, give:

1. The "before" score, and which attacks worked.
2. The "after" score.
3. Your normal dev score after the defence (from your week 12 cases, or the normal cases from the README's Troubleshooting row).

**(b) Your security review.** The link to `REVIEW.md` on `main`, with a triaged "## Week 13: security review" section: the reviewer's findings and your own step 1 rows (the `.env` history check, the two key searches and the deny rule), each with a decision and a reason.

**(c) Your responsible-use answers,** a few sentences each, about **your** project (README step 6):

1. **Privacy:** what data your feature sends, to which company, and whether any of it could be about a real person.
2. **Bias:** whether your feature makes or suggests a decision about people; if so, who it could treat unfairly and what you'd check or leave out.
3. **Licensing:** which packages and documents your project uses, under what licences, and which parts you wrote yourself.
4. **Academic integrity:** how you used AI in your project, how your commits and `REVIEW.md` show it, and what you decided yourself.

Never put a key, a password, a sign-in code or anything from your `.env` file in your hand-in. If step 1 found a real key, say so and say that you deleted it; don't include the key.

## What to hand in

- One document with the pull request's address, your three scores and which attacks worked, the link to `REVIEW.md`, and your four answers.

Submit it the way your course site says.

## Rubric

| Criterion | Points |
|---|---|
| Injection test and defence: 5 hostile cases with expected answers committed before the defence (1 point), the before and after scores with the attacks that worked (1 point), one defence with tests (1 point), the normal dev cases re-run after the defence, merged, no key anywhere (1 point) | 4 |
| Security review: a "## Week 13: security review" section in `REVIEW.md` with the reviewer's findings and your step 1 checks, each triaged with a decision and a reason | 3 |
| Responsible-use answers: privacy, bias, licensing and academic integrity, each specific to your project (3 points for all four specific; 2 for three; 1 for one or two) | 3 |
