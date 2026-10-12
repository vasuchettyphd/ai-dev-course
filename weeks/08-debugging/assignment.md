# Week 8 assignment: Debugging with AI

## What to do

Take part in the peer demo in class, then follow the [week 8 README](README.md) on your own laptop, in your private `semester-project` repo, and collect four things.

**(a) The feedback form you filled in for your partner** (README step 2c). Either the file, `feedback-for-<partner>.md` in your repo (hand in its link on `main` after the merge, or on your `fix-<short-name>` branch if it isn't merged), or a clear photo of the printed form. It lists the exact inputs you tried on your partner's program, what worked, and, for anything that broke, what you typed, what you expected and what happened. If your partner's program never broke, the form says which inputs you tried, including the odd-input list.

**(b) The link to `BUGS.md` in your repo** (README step 3). You make it on your `fix-<short-name>` branch, so it reaches `main` when your fix is merged: hand in its link on `main` after the merge. If your fix isn't merged, hand in its link on your `fix-<short-name>` branch. It has at least one bug written with the course's template, including the exact input someone else could type to see the bug, what you expected, what happened, and whether it happens every time.

**(c) Your merged fix.** The address of the merged pull request from your `fix-<short-name>` branch (README steps 4 to 6), plus two screenshots:

- your new test **failing** before the fix (README step 4c), showing the command and the failure;
- **all** your tests **passing** after the fix (README step 4e).

Its **Files changed** must show the new test, the fix and `BUGS.md` (with that bug's Status and Cause filled in), and nothing unrelated: no deleted or weakened test, no "while I'm here" changes, no `.env` file. (Your `feedback-for-<partner>.md` may be there too.) The repo stays **private**, with `vasuchettyphd` as a collaborator, so your instructor can open it.

**(d) A short reflection,** about half a page:

1. **What your partner found:** one thing your partner found, or tried, that you hadn't, and why you think you'd missed it.
2. **The "fix it" loop:** how you avoided it, or how you got out of it. Say what Claude told you the cause was before it changed anything, and whether your first fix worked. If you hit two failed attempts, say what the undo and the explanation (README step 5) showed you.

Never put a password, a sign-in code, a token or anything from your `.env` file in your hand-in.

## What to hand in

- One document with the feedback form (its link, or the photo), the link to `BUGS.md`, the pull request's address, the two screenshots and your reflection.

Submit it the way your course site says.

## Rubric

| Criterion | Points |
|---|---|
| Feedback form for your partner: specific inputs, and exactly what happened | 2 |
| `BUGS.md` with at least one bug written with exact steps to reproduce it | 2 |
| Merged fix pull request: a test that failed before the fix (screenshot) and passes after it (screenshot), and nothing unrelated changed | 4 |
| Reflection: what your partner found that you hadn't (1 point), and how you avoided the "fix it" loop or got out of it (1 point) | 2 |
