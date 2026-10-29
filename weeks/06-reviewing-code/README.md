# Week 6: Reviewing code

**Goal:** review your week 5 build with three reviewers you write yourself, each with its own focus, decide what to do about every finding, fix the most important ones test first, and read the fixes yourself on GitHub before you merge them.

**Time:** plan for about 2 hours of your own time (an estimate): the three reviewers run for a while by themselves, and each fix is built and tested one at a time. **Cost:** nothing beyond your Claude plan. Nothing new to install, so the steps are **the same on a Mac (Apple chip or Intel) and on Windows (WSL)**.

**Tested with** (12 October 2026; these are the versions tested, yours may be newer):

- Claude Code 2.1.296 on Ubuntu 24.04 Linux (in a container), without signing in to Claude.
- The deal screener example with Python 3.14.4 and Python 3.9.25 (39 tests).
- The optional `pr-review-toolkit` (step 1) at marketplace commit `f359d43b4060`.
- Tested: making a reviewer file in a project's `.claude/agents/` folder, copying the deal screener's three reviewer files, installing `pr-review-toolkit` from the terminal, and the deal screener's tests and program.
- The instructor ran the three deal screener reviewers on the week 5 code; the result is in [`example-project/REVIEW.md`](../../example-project/REVIEW.md).
- Tested on Windows (WSL, Ubuntu 26.04) with Claude Code 2.1.312 signed in (29 October 2026, on a Claude Max plan): steps 3 to 5, the fixes in step 6, and the troubleshooting rows for the reviewers.
- Being tested on real Mac laptops: every step on a Mac, everything on GitHub, and `/usage` on a Pro plan. These follow the official docs.

## Before you start

You need:

- Week 5 done: your first three build steps merged into `main` of your **private** `semester-project` repo through a pull request, with `vasuchettyphd` as a collaborator, and the tests passing.
- Your hand-worked example from week 5 (step 4d), and the address of your week 5 pull request.
- `gh` signed in to **your** GitHub account (`gh auth status` shows your username), and Claude Code signed in with your Claude Pro account.
- Time early in the week. Three reviewers use more of your Claude usage than one conversation (step 4e).

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows, as in weeks 2 to 5. Every command below says where to type it: **in your terminal**, or **in Claude Code** (the `claude` session). On Windows, nothing this week goes in PowerShell. **In a second terminal window** means a new window, so Claude Code keeps running in the first one (week 5 shows how).

### How you'll work this week

As in week 5, you ask Claude Code in plain English. For each step this README shows **the prompt** to type, **what Claude Code will probably do** (its exact words will differ), and **what to check** afterwards.

Week 5's rules still apply:

- Make the branch first (step 3a), before Claude writes anything. Never change `main`.
- For **git** commands, always pick plain **Yes**, never "Yes, and don't ask again" or "Yes, and switch to auto mode".
- Say **No** to anything that changes `main`, and to `reset --hard`, `--force`, `git clean` and `rm -rf`.
- Finish with a push and a pull request, merge on GitHub, then pull.

## Steps

### 1. Why several reviewers

Last week, Superpowers' reviewers checked each build step **against your plan**: did the code do what the task said? This week you review the whole build for the things a plan doesn't spell out: wrong answers in odd cases, private data in the wrong place, and words a user can't follow.

A publisher doesn't give a manuscript to one person and ask "is it good?". A fact checker, a lawyer and a copy editor each read it for one thing, and each finds problems the others miss. Code review works the same way. You write three **reviewer agents** (small instruction files that Claude Code runs as **subagents**, as in week 5), each with one question:

| Reviewer | Its one question |
|---|---|
| `does-it-work` | Does the code do what the plan says, and give the right answers? Are the tests strong enough? |
| `safe-and-private` | Is the project safe to share? Any passwords, keys or personal data where they shouldn't be? |
| `plain-english` | Could someone who doesn't code understand, run and trust it? |

Each reviewer **only reports**. It can read your files but has no way to change them. Every finding gets a label, **Must fix**, **Should fix** or **Nice to have**, with the file and line. Then **you** decide what to do about each one (step 5): reviewers can be wrong.

For how Superpowers' own reviewers work, see [the `/grill-me` and Superpowers tutorial](../../advanced/grill-me-superpowers/).

**The ready-made version (optional, for later).** Anthropic publishes a plugin with six reviewers, `pr-review-toolkit`: they look at code comments, test gaps, errors that fail silently, type design, general code quality, and simplifying code. Your instructor may show it in class. You don't need it this week. If you want to try it after the assignment, install it the week 5 way, in Claude Code:

```text
/plugin install pr-review-toolkit@claude-plugins-official
```

then `/reload-plugins`, and run `/pr-review-toolkit:review-pr` on a branch. Two things to know (from its own files, commit `f359d43b4060`; `claude plugin list` showed version 1.0.1 on 29 October 2026): its agent files have **no `tools` line**, so they **can** edit files, and one of them, `code-simplifier`, is designed to rewrite code. And it may print an error when it checks for an open pull request if there isn't one; that's harmless (being tested). Claude Code also has a built-in `/code-review` command. Its `--fix` option changes your files. This week you use your own three reviewers, which can't change anything.

### 2. Read a diff

> **Being tested:** "click Files changed" and the unified or split view come from GitHub's docs, <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request>. The colours and "View file" are from GitHub's screens and are being tested.

A **diff** is a list of what changed between two versions: lines added, lines removed. You don't need to be a coder to read one. You read one in step 6 before you merge your fixes, so practise now on your own week 5 pull request.

1. Open your week 5 pull request's address in your browser (the one you handed in), and click **Files changed**.
2. Each changed file has its own box, with its name at the top. Lines starting with `+` (shown in **green**) were added; lines starting with `-` (shown in **red**) were removed. Lines with neither are unchanged, shown so you can see where the change sits.
3. To switch between one column (**unified**) and old-beside-new (**split**), click the settings gear at the top of the list and choose one.
4. To see a whole file, not just the changed lines, open the `...` menu at the top right of the file's box and choose **View file**.
5. For any part you don't follow, copy the lines, then in Claude Code type (pasting the lines after the colon):

```text
Explain this change in plain English: <paste>
```

**The deal screener's fixes, as an example.** This page shows every week 6 change to the class example (the link works once week 6 is published): <https://github.com/vasuchettyphd/ai-dev-course/compare/week-05...week-06>. Find `example-project/dealscreener/buybox.py`. The fix for review finding #8 added one green line to `money()`:

```text
+    amount = round(amount, 2)  # so -0.004 shows as $0.00, not -$0.00
```

It rounds the number before choosing its sign, so a cash flow of a tiny fraction of a cent below zero prints `$0.00`, not `-$0.00`.

### 3. Make the three reviewers

> **Being tested:** Where agent files go, their format and the `tools` list come from Claude Code's docs, <https://code.claude.com/docs/en/sub-agents>. Copying the files, and everything inside a signed-in session, was tested in Windows (WSL) with Claude Code 2.1.312.

**a. Start Claude Code and make the branch, before Claude writes anything.** In your terminal:

```bash
cd ~/semester-project && claude
```

Press `Shift + Tab` until the bottom line says `manual mode on`. Then, in Claude Code:

```text
Show me git status.
```

It should say `nothing to commit, working tree clean`. If the only things listed are `__pycache__/` folders, those come from running the Python tests. They're harmless: you can go on (the `safe-and-private` reviewer will probably suggest a `.gitignore` for them). If it lists other files, don't go on: ask "What are these files, and where did they come from? Don't change anything.", and ask in office hours if you're not sure. When it's clean, type:

```text
Switch to main and pull the latest changes from GitHub. Then make a new branch called review-fixes and switch to it.
```

It will probably run `git switch main` (or `git checkout main`), `git pull` and `git switch -c review-fixes` (or `git checkout -b review-fixes`), perhaps joined into one command. Plain **Yes**. Check: ask "What branch am I on?". It should say `review-fixes`. (If that name is taken, use `review-fixes-2`, here and everywhere this README says `review-fixes`.)

**b. Copy the deal screener's three reviewers.** They are your starting point. You copy them yourself, in a **second terminal window** (as in week 5): on a Mac, click Terminal and press `Cmd + N`; on Windows, open **Ubuntu** again from the Start menu (not PowerShell). A new window starts in your home folder, `~`. First get the course repo, or update it if you already have it:

```bash
cd ~ && git clone https://github.com/vasuchettyphd/ai-dev-course.git
```

If it says `already exists`, type `cd ~/ai-dev-course && git pull` instead. (If you cloned the course repo into another folder earlier, use that folder instead of `~/ai-dev-course`, here and below.) Then copy the three files into your project:

```bash
cd ~/semester-project
mkdir -p .claude/agents
cp ~/ai-dev-course/example-project/.claude/agents/*.md .claude/agents/
ls .claude/agents
```

`ls` should list the three files: `does-it-work.md`, `plain-english.md` and `safe-and-private.md`. If `ls` shows nothing, run `git pull` in `~/ai-dev-course` and try again. A project's reviewer agents live in its `.claude/agents/` folder, and they go to GitHub with the rest of the project.

**c. Restart Claude Code.** Claude Code notices new and changed agent files by itself, but only in an `agents` folder that already existed when the session started. Yours is new, so restart once. In Claude Code (the first window), type `/exit`, then in that terminal:

```bash
claude
```

Press `Shift + Tab` until `manual mode on`, and check "What branch am I on?" still says `review-fixes`. From now on, changes to the files are picked up within a few seconds, with no restart.

**d. Make them fit your project.** The copied files were written for the deal screener, but most of each file is general. In Claude Code, type:

```text
Read PLAN.md and the three reviewer files in .claude/agents/ (does-it-work.md, safe-and-private.md and plain-english.md). They were written for another project, a rental deal screener. Adapt each one to my project: keep its one question, the line "Report only. Never change any file.", the three labels and the way each finding is written, and change the "Look for" list so it fits what PLAN.md says my project does and the data it uses. Keep the name and description lines as they are, and keep the tools line exactly as it is: tools: Read, Grep, Glob. Then show me what you changed in each file.
```

**What Claude Code will probably do:** read the four files, then ask to edit each agent file (an edit prompt; plain **Yes**, not the "don't ask again" option), and list the changes. If any prompt asks to change a `tools:` line, answer **No**. Read them. If a change doesn't fit your project, say so, for example: "In does-it-work, also check ...".

**e. Check each reviewer can only read.** This is the most important check this week. Ask "Show me the `tools:` line of each file in .claude/agents/" (or open each file; on a Mac, Finder hides folders starting with a dot). Each file starts with a block like this one, from the deal screener:

```text
---
name: does-it-work
description: Use after a build to check that the code gives the right answers and has good tests. Only reports problems; never changes files.
tools: Read, Grep, Glob
---
```

Check that the `tools:` line is there and says exactly `tools: Read, Grep, Glob`. Why it matters:

- The `tools` line is an **allowlist**: Claude Code's docs say to "use the `tools` field as an allowlist", so the reviewer can use only the tools listed. `Read` opens a file, `Grep` searches inside files, and `Glob` finds files by name. None of them can change anything.
- **No `tools` line at all** means the reviewer gets every tool, including the ones that edit and write files.
- The docs' own read-only reviewer example also lists `Bash`, which runs terminal commands. This course leaves `Bash` out: a command can still change or delete files.

If any file has no `tools` line, or lists anything else (`Edit`, `Write`, `Bash`, ...), type: "Make sure every file in .claude/agents/ has a tools line, right after the description line, that says exactly: tools: Read, Grep, Glob. Add it where it is missing. Change nothing else."

**f. Check Claude can use them.** In Claude Code, type:

```text
Which subagents can you use in this project?
```

It should name `does-it-work`, `safe-and-private` and `plain-english` (it may list built-in ones too). Two things that **don't** work for this: in Claude Code 2.1.296 and 2.1.312, `/agents` only prints "The /agents wizard has been removed." and where the files go; and `claude agents` in your terminal manages background sessions, not these files. If Claude doesn't name your reviewers, see Troubleshooting.

**g. Check a reviewer really can't edit.** In Claude Code, type:

```text
Ask the does-it-work subagent to add the word "test" to the end of README.md. Don't edit anything yourself and don't try another way. Just tell me what the subagent said.
```

It should say it can't. Its instructions say never to change a file, but the tools line from step 3e is what actually stops it, so a refusal alone doesn't prove the line is right. If an edit prompt appears anyway, choose **No**, and check step 3e again.

Optional follow-up, in Claude Code:

```text
Ask the does-it-work subagent which tools it has. Just tell me what it said.
```

It should list Read, Grep and Glob. It may also mention "deferred" tools it can't use yet; that's fine.

**h. Commit the reviewers.** In Claude Code:

```text
Commit the three files in .claude/agents/ on this branch with the message "Add three reviewer agents".
```

Plain **Yes** to `git add` and `git commit`.

### 4. Run all three

> **Being tested:** Running subagents in parallel ("in parallel using separate subagents") and how their results come back are from Claude Code's docs, <https://code.claude.com/docs/en/sub-agents>. The deal screener's review used these reviewer instructions and these combining rules. Running this one prompt was tested in a signed-in session (Windows WSL): the three reviewers ran at the same time in the background, and the whole review took under two minutes for the deal screener.

**a. Check your usage first.** In Claude Code, type `/usage` and write down what it shows. Keep these numbers; you'll compare them in step 4e, and bring them to next week's class.

**b. Run the review.** One prompt runs the three reviewers at the same time, then combines their reports into one file, `REVIEW.md`. In Claude Code, type:

```text
Run the does-it-work, safe-and-private and plain-english reviewers in parallel, as separate subagents, on this project. Then combine their reports into REVIEW.md: one table with the columns #, Label, Finding (file:line), Found by, Decision, Reason. If two or more reviewers found the same problem, list it once and put every reviewer who found it in "Found by". If they gave it different labels, keep the more serious label and say so in the Finding. Sort the rows: Must fix first, then Should fix, then Nice to have, and number them. Keep each finding's wording close to what the reviewer wrote, and keep their file and line numbers. Leave Decision and Reason empty. Do not add any finding the reviewers did not report, and do not change any file except REVIEW.md. After the table, list in a few words the areas where a reviewer said "Nothing found".
```

**c. What you'll see.** Claude starts three subagents, one per reviewer, and they read your files at the same time. Each runs in the background, and when it finishes a line like `Agent "Run safe-and-private review" finished · 12s` appears in the chat. **Wait for all three.** Then Claude writes `REVIEW.md`. This can take several minutes.

| Claude asks to | Choose |
|---|---|
| Create or edit `REVIEW.md` | **Yes** |
| Edit, create or delete **any other** file | **No**: a review changes nothing else |
| Read-only commands: `git status`, `git log`, `git diff`, `ls` | **Yes** |
| Anything that changes `main`, or `--force`, `reset --hard`, `git clean`, `rm -rf` | **No** |

After a No, type: "Don't change any file except REVIEW.md."

**d. Read `REVIEW.md`.** Open it (or ask "Show me REVIEW.md"). Check: one table with the six columns; Must fix rows first; every finding names a file and line; Decision and Reason are empty; and a short "Nothing found" list after the table. Compare with the deal screener's, [`example-project/REVIEW.md`](../../example-project/REVIEW.md): its reviewers found 13 things (1 Must fix, 5 Should fix, 7 Nice to have). Yours may find more or fewer. Then commit it, so the reviewers' own findings are saved before you add your decisions:

```text
Commit REVIEW.md on this branch with the message "Review of the week 5 build".
```

Plain **Yes**.

**e. Usage.** Type `/usage` again and compare with step 4a. Every subagent sends its own requests, which "count toward the same usage limits as your main conversation" (<https://code.claude.com/docs/en/sub-agents>), so three reviewers use more than one conversation. We have no published number for how much more: it depends on the size of your project. On a Pro plan, `/usage` shows which share of your recent usage went to subagents (press `d` or `w` for day or week). Its `Prompt cache (main)` line counts the main conversation only, not the subagents (<https://code.claude.com/docs/en/costs>), so don't judge the reviewers by it. If you hit a usage limit, wait for the reset, as in [week 5](../05-building-with-ai/) step 6.

### 5. Triage: decide on every finding

**Triage** means deciding, finding by finding, what to do. You decide, not Claude. Each finding gets a **Decision**, `Fix` or `Won't fix`, and a **Reason** of one plain sentence.

**Check each finding before you decide.** Reviewers can be wrong. In the deal screener's review, three line numbers were wrong (findings #5, #11 and #13; the corrected number is shown with the reviewer's in brackets), and finding #10 was partly wrong. To check one, type in Claude Code:

```text
Check finding #1 in REVIEW.md against the code. Is it right, and are the file and line numbers right? Explain in plain English. Don't change any file.
```

Change the number for each finding. You can also open the file yourself and look at that line.

**How to decide:**

- Every **Must fix** is `Fix`, unless the finding is wrong. Then it's `Won't fix`, and the reason gives the evidence, for example "the test in tests/test_buybox.py already checks this".
- **Should fix** and **Nice to have**: `Fix` if it's worth it this week; otherwise `Won't fix`, with a reason.
- Every `Won't fix` needs a reason. "Not important" isn't one; say **why**.
- Don't fix everything without thinking, and don't wave everything away either.

Three rows from the deal screener's `REVIEW.md` (shortened):

| # | Label | Finding | Decision | Reason |
|---|---|---|---|---|
| 1 | Must fix | README and a test say "listing B from the plan", but PLAN.md has no listings A or B | Fix | Really a wording fix: they now point at the task plan, which has the listings |
| 8 | Nice to have | A tiny negative number prints "-$0.00" | Fix | Real bug, so numbers are now rounded before formatting, with tests written first |
| 10 | Nice to have | No .gitignore in the project | Won't fix | Partly wrong: the course repo's own .gitignore already covers it |

To record your decisions, edit `REVIEW.md` yourself, or tell Claude exactly what to write, one finding at a time:

```text
In REVIEW.md, set finding #1's Decision to Fix and its Reason to "<your reason>". Don't change anything else.
```

When every finding has a Decision and a Reason, commit:

```text
Commit REVIEW.md on this branch with the message "Triage the review".
```

### 6. Fix

> **Being tested:** This step needs a signed-in session and a real GitHub account, and is being tested.

**a. One finding at a time, Must fix first.** Then Should fix, if you have time. For a finding that changes what the program **does** (a wrong answer, a missing check, a crash), fix it test first, as in week 5. In Claude Code, with the finding's number and a few words about it:

```text
Fix finding #1 in REVIEW.md, test first: write a test that fails because of this problem, run the tests and show me it fails, then change the code until all the tests pass. Change nothing else. Then commit on this branch with the message "Fix review #1: <a few words>".
```

(Your #1 may be a wording finding, as the deal screener's was; then use the wording prompt below.)

For a **wording** finding (a README sentence, a comment, a message), there's nothing to test first:

```text
Fix finding #5 in REVIEW.md. It is a wording change, so no new test: make the change, run all the tests, and commit on this branch with the message "Fix review #5: <a few words>".
```

Plain **Yes** to edits in your project, the tests and the commit. Read each change before you go on to the next finding. You can put several small wording fixes in one commit, as the deal screener did ("Fix review #1, #5, #6, #7, #13: ...").

The deal screener's only Must fix (#1) was a wording change, so #8 is its test-first example. In the deal screener, the fix for #8 started with new tests that failed (`ImportError: cannot import name 'percent'`), then the code was fixed and all 37 tests passed. For #3 and #4 the new tests passed straight away: the code was already right and only the test was missing, which is fine. You can see the deal screener's fix commits on the Commits tab of the week 6 pull request on the course repo.

**b. Run the tests and the program yourself.** In a second terminal window, `cd ~/semester-project`, then your test command from week 5 (for example `python3 -m unittest` or `npm test`). For the deal screener after its fixes:

```text
Ran 39 tests in 0.002s

OK
```

Take a **screenshot**: the assignment asks for it. Then run your program on your hand-worked example from week 5 and check it still gives the same answer. A fix must not break something else.

**c. Push and open a pull request.** In Claude Code:

```text
Push the review-fixes branch to GitHub and open a pull request into main titled "Review fixes".
```

It will probably run `git push -u origin review-fixes` and `gh pr create ...`. Plain **Yes** to each. It prints the pull request's address. Copy it: you hand it in.

**d. Read Files changed yourself, before you merge.** Open the address and click **Files changed** (step 2). You should see `REVIEW.md`, the three agent files, and the files your fixes changed (code, tests, and any README or PLAN.md you reworded): nothing else. Go file by file. For each fix, find its green and red lines and check they do what the finding asked. For any part you don't follow, use "Explain this change in plain English: <paste>" (step 2). If something is there that shouldn't be, don't merge: ask Claude what it is and why.

**e. Merge on GitHub, then pull.** On the **Conversation** tab click **Merge pull request** and **Confirm merge** (or **Squash and merge**; the exact labels are being tested), as in [week 3](../03-git-and-github/) step 7. Then, in Claude Code:

```text
Switch back to main and pull the latest changes from GitHub.
```

Check: ask "What branch am I on, and is REVIEW.md in this folder?". It should say `main`, and yes. Keep your local `review-fixes` branch until your assignment is graded.

### 7. Check it worked

You're done when:

- Your pull request's page on GitHub shows it was merged, and **Files changed** shows the three reviewer files in `.claude/agents/`, `REVIEW.md` and your fixes.
- Each reviewer file has `tools: Read, Grep, Glob`.
- Every finding in `REVIEW.md` has a Decision, and every `Won't fix` has a reason.
- Every Must fix is fixed (or is a reasoned `Won't fix` because the finding was wrong).
- On `main`, your tests pass and your program still matches your hand-worked example.

The [assignment](assignment.md) asks for the pull request's address, a screenshot and a short reflection.

## Troubleshooting

| What you see | What to do |
|---|---|
| Claude doesn't name your reviewers (step 3f) | In a second terminal window, `ls ~/semester-project/.claude/agents` must list the three files. If it does, `/exit` and start `claude` again in `~/semester-project` (step 3c): a new `agents` folder needs one restart. |
| An error when a reviewer starts, such as `Agent 'does-it-work' would be spawned with zero tools - refusing. Its tools list resolved to nothing: unrecognized [Reed].` | A tool name is misspelled. Set the line to exactly `tools: Read, Grep, Glob` (step 3e). If only one name is misspelled, there's no error: the reviewer quietly runs without that tool, so check the line anyway. |
| A reviewer asks to edit a file, or an edit prompt appears during the review for any file except `REVIEW.md` | Choose **No**. Check the `tools:` line in every reviewer file (step 3e). Then type: "Don't change any file except REVIEW.md." |
| Too many findings (say, 40) | Normal for a first review. Fix the Must fixes, triage everything, and mark most Nice to haves `Won't fix` with a reason such as "not in this version". You don't have to fix everything this week. |
| Two reviewers disagree, or give the same problem different labels | The prompt keeps the more serious label and says so. You decide (step 5): check the finding against the code, and write your reason. |
| A finding is wrong, or its line number is | It happens (the deal screener had three wrong line numbers). Mark it `Won't fix` with the evidence, or fix the right line and give the corrected number in the Reason. |
| `You've hit your session limit` or `weekly limit` | Wait for the reset, as in [week 5](../05-building-with-ai/) step 6. If the review stopped part way, run the step 4b prompt again after the reset. |
| A fix breaks a test | Don't merge. In Claude Code: "The tests fail after the fix for finding #N. Show me which test fails and why, in plain English, then fix the code, not the test." If the test's expected answer is wrong, check it against your hand working first. |
| Findings about the plan file in `docs/superpowers/plans/` | That file is Superpowers' week 5 build plan, a record of how you built it. Mark those findings `Won't fix` with the reason "build plan from week 5, not the project's code", unless they point to a real problem in the code. |
| `fatal: a branch named 'review-fixes' already exists` | Use `review-fixes-2` instead (step 3a), here and everywhere this README says `review-fixes`. |
| It committed to `main` | Say **No** to any push of `main`, and to `reset --hard` or `--force`. Then follow [week 5's "If it committed to `main`"](../05-building-with-ai/README.md#if-it-committed-to-main), using `rescue-review-fixes` as the branch name. |
| `fatal: destination path 'ai-dev-course' already exists` (step 3b) | You have it already: `cd ~/ai-dev-course && git pull`, then copy the files. |
| `cp: cannot stat ...` (step 3b) | The course repo is older than week 6, or in another folder. Run `git pull` in it, and check the path. |
