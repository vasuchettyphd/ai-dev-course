# Week 14 assignment: Final demos

## What to do

Follow the [week 14 README](README.md) on your own laptop, in your private `semester-project` repo. This is the final project, worth 30 points: your demo, your project as it stands on `main`, and your write-up.

**(a) Your demo.** In class, in the order your instructor sets: 3 minutes, following your `DEMO.md`, then about a minute of questions. Show your AI feature working once (or your fallback, if the network or the model fails in the room), and say one honest limit of your project. No key on screen.

**(b) Your project on main.** The address of the merged pull request from your `final` branch (merged with "Create a merge commit"), and `main` as it stands after it. Your instructor checks it against the README's "ready on main" table:

1. The tests pass with `.env` moved out.
2. `REVIEW.md` has a Decision and a Reason for every finding.
3. Your week 12 evaluation results and week 13 injection results are committed.
4. No key anywhere in the history.
5. The README says exactly how to run it, and `docker build` builds it and runs the tests.

**(c) Your write-up.** `FINAL.md` on `main`, about two pages, under these seven headings:

1. What it does and who it's for
2. How it's built, and which parts are AI
3. What I measured
4. What went wrong and what I changed
5. Risks and responsible use
6. What AI did and what I decided
7. What I'd do next

Every number links to the file in your repo it comes from. Never put a key, a password, a sign-in code or anything from your `.env` file in your hand-in.

## What to hand in

- On the day: your demo.
- Before the deadline your course site gives: one document with the pull request's address and the link to `FINAL.md` on `main`.

Submit it the way your course site says.

## Rubric

| Criterion | Points |
|---|---|
| Demo: works, or the fallback is used well and the failure explained (4 points); the AI feature shown (2 points); one honest limit said (2 points); within 3 minutes (2 points) | 10 |
| Project on main: tests pass with `.env` moved out (2 points); `REVIEW.md` triaged (2 points); week 12 and 13 results committed (2 points); no key anywhere in the history (2 points); the README says how to run it and Docker builds it and runs the tests (2 points) | 10 |
| Write-up: the seven headings present and specific to your project (4 points); every number traceable to a file in your repo (3 points); "What AI did and what I decided" honest and specific (3 points) | 10 |
