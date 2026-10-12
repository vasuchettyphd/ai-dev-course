# Week 8: Debugging with AI

**Goal:** demo version 1 of your project to a classmate (the midterm check-in) and try theirs, write the bugs you find in `BUGS.md` as exact steps anyone can repeat, then fix one bug properly with Superpowers' `systematic-debugging` skill: reproduce it, narrow it down, write a test that fails because of it, and only then fix it, merged through a pull request.

**Time:** the peer demo is in class (about 5 minutes each way, plus filling in the form). Then plan for about 2 hours of your own time (an estimate) for logging and fixing one bug. **Cost:** nothing beyond your Claude plan. Nothing new to install, so the steps are **the same on a Mac (Apple chip or Intel) and on Windows (WSL)**; on Windows, everything runs in the Ubuntu window.

**Tested with** (12 October 2026; these are the versions tested, yours may be newer):

- Superpowers 6.4.1, whose `systematic-debugging` skill this week follows. Every quote from the skill below is from its `SKILL.md` in that version. Superpowers 7.0.0 came out on 10 October 2026; its `systematic-debugging` differs from 6.4.1 only in two lines of a shell example, but 7.0.0 is not tested.
- Claude Code 2.1.296 on Linux (WSL 2).
- The deal screener example's real bug (an interest rate typed as `0.07` is read as 0.07%), reproduced with Python 3.14.4, then fixed test first: before the fix, `python3 -m unittest` ran 47 tests and printed `FAILED (failures=5)`; after it, the same 47 tests passed. They also passed in a container on Docker Engine 29.8.0 with the `python:3.12-slim` image (Python 3.12.15).
- The instructor filled in the feedback form for the deal screener, acting as the classmate: [`example-project/FEEDBACK.md`](../../example-project/FEEDBACK.md). The bug it found is Bug 1 in [`example-project/BUGS.md`](../../example-project/BUGS.md).
- Being tested on real Mac and Windows laptops: the peer demo in class, everything inside a signed-in Claude Code session (starting `systematic-debugging` by name or on its own, and what it shows you), everything on GitHub, and every step on a Mac or in Windows (WSL).

## Before you start

You need:

- Weeks 5 to 7 done: version 1 of your project merged into `main` of your **private** `semester-project` repo, with `vasuchettyphd` as a collaborator, your tests passing, and your week 7 `Dockerfile` merged.
- Superpowers, installed in week 5 (in Claude Code, `/plugin` lists `superpowers`), and Docker Desktop from week 7.
- The command that runs your tests (for example `python3 -m unittest` or `npm test`), and the one that runs them in the container (week 7 step 4c).
- The course repo on your laptop, in `~/ai-dev-course` (week 6 step 3b).
- `gh` signed in to **your** GitHub account (`gh auth status` shows your username), and Claude Code signed in with your Claude Pro account.
- For class: your laptop, charged, with your program ready to run.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows, as in weeks 2 to 7. Every command below says where to type it: **in your terminal**, or **in Claude Code** (the `claude` session). On Windows, nothing this week goes in PowerShell. **In a second terminal window** means a new window, so Claude Code keeps running in the first one (week 5 shows how).

### How you'll work this week

As in weeks 5 to 7, you ask Claude Code in plain English. For each step this README shows **the prompt** to type, **what Claude Code will probably do** (its exact words will differ), and **what to check** afterwards.

The rules from weeks 5 to 7 still apply:

- Make the branch first (step 3a), before Claude writes anything. Never change `main`.
- For **git** commands, always pick plain **Yes**, never "Yes, and don't ask again" or "Yes, and switch to auto mode".
- Finish with a push and a pull request, read **Files changed**, merge on GitHub, then pull.

This week adds four debugging rules:

- **Reproduce first.** Make the bug happen on purpose before anyone changes anything.
- **A failing test before the fix.** A test that fails because of the bug, seen failing, then the fix.
- **Only the bug.** No changes unrelated to the bug, and never delete or weaken a test to make it pass.
- **Two failed attempts: stop.** Undo, and ask Claude to explain the cause before it changes anything else (step 5).

What to answer this week:

| Claude asks to | Choose |
|---|---|
| Create or edit `BUGS.md`, or add a test for the bug | **Yes** |
| Edit the code file where the bug's cause is, after it has explained the cause and you've seen the test fail | **Yes** |
| Run your tests, or run your program with the bug's input | **Yes** |
| Read-only commands: `git status`, `git log`, `git diff`, `ls` | **Yes** |
| `git add`, `git commit`, `git push` on your `fix-` branch, `gh pr create` | plain **Yes** |
| `git restore` or `git revert` that you asked for in step 5, naming only the files you expect | plain **Yes** |
| Edit a file, or part of one, that has nothing to do with the bug ("while I'm here" tidying, renaming, rewriting) | **No** |
| Delete a test, skip one, or change a test's expected answer so that it passes | **No** |
| Edit code before it has told you the cause, or before you've seen the new test fail | **No** |
| An install of any kind | **No**: nothing needs installing this week. Ask "Why do you need this?" |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

After a No, tell Claude why, for example: "Don't change that file. Only change what this bug needs."

## Steps

### 1. Debugging with AI, without the "fix it" loop

**The "fix it" loop.** Something is broken, so you type "it's broken, fix it". Claude guesses at a cause and changes some code. Now something else is broken, or the same thing is broken in a new way. "Still broken, fix it." Another guess, another change. After an hour your project has five half-fixes piled on top of each other, nobody knows what the cause was, and it's harder to fix than when you started.

The way out is to slow down at the start. Four steps, in this order:

| Step | What it means | In `systematic-debugging` |
|---|---|---|
| 1. **Reproduce** | Make the bug happen on purpose, with the exact input, every time. | Phase 1, "Root Cause Investigation": read the error, "Reproduce Consistently", and find where the wrong value first appears. |
| 2. **Narrow down** | Find exactly where and why it goes wrong, before changing anything. | The rest of Phase 1, then Phase 2, "Pattern Analysis" (find something similar that works and list every difference), and Phase 3, "Hypothesis and Testing" (write down one guess about the cause, test it with the smallest change, and say so when you don't know). |
| 3. **Test** | Write a test that fails because of the bug, and see it fail. | Phase 4, "Implementation", step 1, "Create Failing Test Case": "MUST have before fixing". |
| 4. **Fix** | One change, then every test passes. | Phase 4, steps 2 and 3, "Implement Single Fix" ("ONE change at a time", "No \"while I'm here\" improvements") and "Verify Fix". |

`systematic-debugging` is one of the Superpowers skills you installed in week 5 (<https://github.com/obra/superpowers>), so there's nothing to install. Its rule, in its own words:

```text
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

"If you haven't completed Phase 1, you cannot propose fixes." (The **root cause** is the real reason the bug happens, not just the place where you notice it.) The skill's description says to use it "when encountering any bug, test failure, or unexpected behavior, before proposing fixes", so it may start on its own when you describe a bug (being tested). This week you start it by name, to be sure (step 4a).

The skill doesn't write any files of its own. You see its work in the conversation, and in the test and the fix it makes.

### 2. Midterm peer demo, in class

> **Being tested:** The peer demo is new this term. The deal screener's form was filled in by the instructor acting as the classmate.

This is the midterm check-in. You work in pairs, about 5 minutes each: you show version 1 of your project, your classmate tries it, then you swap.

**a. Before the demo, on your own laptop.**

1. Run your program once, the way your README says (directly, or in Docker with `docker run -it --rm semester-project` from week 7), to check it starts. If it doesn't, see 2d.
2. **Hide anything private.** Your classmate sees your screen and types into your program. Close `.env` and any file with passwords, keys, tokens or personal data. Close or minimise everything except the terminal window your program runs in, including Claude Code (type `/exit`) and your browser. Turn off notifications if you can.
3. Get your copy of the form, [`feedback-form.md`](feedback-form.md), for when you try your classmate's program (2c); your classmate brings their own copy for yours. Either print it, or copy it into your own project folder. In your terminal:

   ```bash
   cp ~/ai-dev-course/weeks/08-debugging/feedback-form.md ~/semester-project/feedback-for-sam.md
   ```

   with your partner's first name instead of `sam`. This README calls that file `feedback-for-<partner>.md`. To open it, type `cd ~/semester-project`, then `open .` on a Mac or `explorer.exe .` on Windows (as in week 2), and double-click the file; pick TextEdit (Mac) or Notepad (Windows) if asked (being tested). If `cp` says `cannot stat`, type `cd ~/ai-dev-course && git pull` first.

**b. Your demo (about 5 minutes).** Say in one sentence what your program does and for whom, then run it with one normal example (your hand-worked example from week 5 is good). Then hand over the keyboard: your classmate types their own inputs, and the **odd-input list** on the form:

- blank, words instead of numbers, `0`, negative numbers, very large numbers
- decimals where whole numbers are expected, and the reverse (`0.07` where `7` is meant)
- symbols (`$`, `%`, `,`), very long text, and pressing Enter too early

Stay beside them, and only let them type into your program. Don't explain or defend while they try things: watch, and write down anything surprising. When the program stops, run it again for the next input. If your program isn't typed into (a web page, or one that reads a file), your classmate tries the same kinds of odd values in its boxes or in its input file.

**c. Your classmate's demo: you fill in the form.** Swap. Now you try your classmate's program and fill in the form for them:

- **What I tried (exact inputs):** every input, exactly as typed.
- **What worked.**
- **What broke, and exactly how:** for each problem, **what I typed**, **what I expected**, and **what happened** (copy any message word for word). "It crashed" isn't enough; "I typed `abc` for the price and it printed `ValueError: could not convert string to float` and stopped" is.
- **One suggestion.**

Leave the last line, "For the owner: bugs added to BUGS.md", for the owner. Give the owner a copy before you leave (send them the file, or let them photograph the paper), and keep yours: the form you filled in for your partner is part of your assignment. The deal screener's form is an example: [`example-project/FEEDBACK.md`](../../example-project/FEEDBACK.md).

**d. If something gets in the way.**

- **Your build is broken on the day.** Demo whatever does run, even only part of it, and show the break. The break is your first bug: write down exactly what you typed and what it printed, and it goes in `BUGS.md` (step 3).
- **Your partner is absent, or the class has an odd number.** Tell your instructor: you'll join another pair (three people, taking turns) or demo to the instructor.
- **Your partner found nothing.** Go through the odd-input list together, item by item, on every question your program asks. If still nothing breaks, the form lists everything that worked: that's a good form. Then try the odd-input list yourself after class, on parts your classmate didn't reach. A confusing message, an error screen or a wrong number all count as bugs. Still nothing? Tell your instructor.

### 3. Log the bugs in `BUGS.md`

> **Being tested:** This step needs a signed-in session and is being tested. The deal screener's `BUGS.md` is real.

**a. Start Claude Code and make the branch, before Claude writes anything.** Choose the bug you'll fix this week (the one that matters most to someone using your program), and a short name for it, such as `rate-decimal`. Your branch is `fix-` followed by that name: `fix-rate-decimal`. In your terminal:

```bash
cd ~/semester-project && claude
```

Press `Shift + Tab` until the bottom line says `manual mode on`. Then, in Claude Code:

```text
Show me git status.
```

It should say `nothing to commit, working tree clean`, or list only your `feedback-for-<partner>.md` file from step 2 (that's expected). If it lists anything else, don't go on: ask "What are these files, and where did they come from? Don't change anything.", and ask in office hours if you're not sure. Then type, with your branch's name:

```text
Switch to main and pull the latest changes from GitHub. Then make a new branch called fix-<short-name> and switch to it.
```

It will probably run `git switch main`, `git pull` and `git switch -c fix-<short-name>`. Plain **Yes**. Check: ask "What branch am I on?". (If that name is taken, add `-2`, here and everywhere this README says `fix-<short-name>`.)

**b. Reproduce each bug yourself.** Before you write a bug down, make it happen. In a **second terminal window**, in `~/semester-project`, run your program and type exactly what your classmate typed. Do you see what the form says happened? Try it three times, starting the program fresh each time: that answers "Does it happen every time?". If you can't make it happen, see Troubleshooting.

**c. Write `BUGS.md`.** Every bug uses the same template. This is the deal screener's, word for word:

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

You write `BUGS.md` from the form **your partner filled in about your project** (step 2c, their copy to you), not the one you filled in for them. In Claude Code, type this, then paste the "What broke" part of that form after it (type it in if it's on paper), and add what you saw in 3b:

```text
Make a file called BUGS.md at the top of my project. Start it with "# Bugs" and the line "Bugs found in my project, one section each, newest last." Then add one section for each bug below, numbered from 1, using exactly this template: a heading "## Bug N: <short name>", then the lines Found by, What I did (exact input), What I expected, What happened, Does it happen every time?, Status and Cause, as in the deal screener's BUGS.md. Copy the exact inputs and messages word for word. Status is Open and Cause is "(fill in once you know)" for every bug. Don't guess anything that isn't in my notes: write "Not sure" instead. Don't change any other file. Here are my notes:
```

Plain **Yes** to creating `BUGS.md`. Then read every section against your partner's form: the exact input must be exact (every number, in order, as typed). Fix anything wrong yourself, or tell Claude exactly what to change.

**The worked example: the deal screener's Bug 1.** The instructor, acting as the classmate, typed listing B with `0.07` for the interest rate, meaning 7%. Here it is in [`example-project/BUGS.md`](../../example-project/BUGS.md), as it was first written:

```markdown
## Bug 1: Interest rate typed as 0.07 is read as 0.07%

- **Found by:** the instructor, acting as a classmate, on 2026-10-12, using the odd-input list from the feedback form
- **What I did (exact input):** listing B (price 150000, rent 1700, tax 2400, insurance 1200, HOA 0, down payment 25, loan term 30, closing costs 6000), with `0.07` typed for the interest rate instead of `7`
- **What I expected:** a monthly mortgage payment of about $748.47, the 7% figure worked out by hand, or a question asking whether I meant 7%
- **What happened:** no question. It took the rate as 0.07%: monthly mortgage payment $315.80 (not $748.47), monthly cash flow $863.20 (not $430.53), cash-on-cash return 23.81% (not 11.88%). The verdict was Overall: PASS, the same as with `7`, so only the numbers show the mistake.
- **Does it happen every time?** Yes
- **Status:** Open
- **Cause:** (fill in once you know)
```

Notice the numbers: with `0.07` the mortgage was $315.80 and the cash flow $863.20, but the right answers at 7% are $748.47 and $430.53. The verdict said Overall: PASS both times, so a quick look at the last line would never show the bug. Only the numbers do.

**d. Commit.** In Claude Code:

```text
Commit BUGS.md on this branch with the message "Log bugs from the peer demo". If my feedback-for-<partner>.md file is in the folder, commit it too.
```

Plain **Yes** to `git add` and `git commit`.

### 4. Debug one bug properly

> **Being tested:** Starting the skill by name and what it shows need a signed-in session, and are being tested. The skill's words are from its `SKILL.md` (Superpowers 6.4.1). The deal screener's results below are real.

You stay on your `fix-<short-name>` branch. Keep the bottom line at `manual mode on`.

**a. Start `systematic-debugging` with the bug.** Open `BUGS.md` (as in step 2a) and copy your bug's whole section, from its `## Bug N` heading to its Cause line. In Claude Code, type this, then paste the section straight after it, before you press Enter:

```text
/superpowers:systematic-debugging Debug the bug from BUGS.md in my project that I paste below. First reproduce it and find the cause, and explain the cause to me in plain English before you change anything. Then add a test to my project's existing tests that fails because of this bug, using the exact input from BUGS.md and the answer I expected, run it, and show me it failing. Then stop. Don't change the code or fix anything yet. Don't change anything unrelated to this bug, and never delete or weaken a test. Here is the bug:
```

The command must be at the very start of the message, so the skill starts straight away. If `/superpowers:systematic-debugging` isn't in the list as you type, type `/reload-plugins` and try again, or start the prompt with `Use the superpowers systematic-debugging skill.` instead (being tested). A long paste may show as a short label such as `[Pasted text]` in the prompt box; that's normal (being tested).

The skill allows a "one-off test script if no framework", but this course wants a real test in your project's own tests: it stays in the project, and every time you run your tests it checks that this bug never comes back.

**b. What you'll see, phase by phase** (being tested; its exact words will differ). Each phase below shows what the deal screener's run found.

1. **Root Cause Investigation.** It reads your code and the error message, if there is one, and asks to run your program or your tests with the bug's input (**Yes**). It traces where the wrong value first appears. *Deal screener:* no error message, the program finished normally, so the clue was in the numbers. The typed `0.07` went through `parse_answer` in `dealscreener/__main__.py`, which accepts any percentage from 0 to 100, so it came out as 0.07%. The calculator was right; the input check was where the meaning was lost.
2. **Pattern Analysis.** It compares with something similar that works. *Deal screener:* the same listing with `7` gives $748.47, and the only difference is the typed rate. The down payment question goes through the same check, so `0.25` had the same problem.
3. **Hypothesis and Testing.** It writes down one guess, "I think X is the root cause because Y". *Deal screener:* "nothing asks whether a decimal like 0.07 meant 7%".
4. **Implementation, step 1: the failing test.** It adds a test, runs it, and shows it failing. Then it stops, because you asked it to.

If it asks to change code before it has explained the cause, choose **No** and type: "Explain the cause first, in plain English. Don't change anything yet." If it says "I don't understand" something, that's allowed: the skill tells it to say so instead of guessing. Answer its question if you can.

**c. See the test fail yourself.** In your **second terminal window**, in `~/semester-project`, run your test command (for example `python3 -m unittest`). It must **fail**. For the deal screener, before the fix:

```text
.......................................F.FF.FF.
...
FAIL: test_rate_typed_as_a_fraction_asks_and_yes_means_percent (tests.test_main.SmallPercentTest.test_rate_typed_as_a_fraction_asks_and_yes_means_percent)
...
AssertionError: 'You typed 0.07. Did you mean 7%? Type y for 7%, or n to keep 0.07%: ' not found in ['Purchase price ($): ', 'Monthly rent ($): ', 'Yearly property tax ($): ', 'Yearly insurance ($): ', 'Monthly HOA fee ($, 0 if none): ', 'Down payment (%): ', 'Interest rate (%): ', 'Loan term (years): ', 'Loan term (years): ', 'Closing costs ($): ']
...
FAIL: test_yes_and_no_ignore_case_and_spaces (tests.test_main.SmallPercentTest.test_yes_and_no_ignore_case_and_spaces)
...
First differing element 0:
'Monthly mortgage payment: $315.80'
'Monthly mortgage payment: $748.47'
...
Ran 47 tests in 0.004s

FAILED (failures=5)
```

(`...` marks lines left out.) Each `.` is a test that passed and each `F` one that failed. Read the failure: it should show **your bug**. In the deal screener's first failure, the program never asked "Did you mean 7%?" (it asked for the loan term twice, because the `y` meant for the question was read as the loan term). In the second, the wrong answer sits next to the one expected: `$315.80` where `$748.47` was expected. If it fails with an error about the test itself instead (such as `ImportError`, `NameError` or `SyntaxError`), the test is broken, not catching your bug: see Troubleshooting. Take a **screenshot** of the failing run: the assignment asks for it.

The deal screener added 8 tests (`SmallPercentTest` in [`example-project/tests/test_main.py`](../../example-project/tests/test_main.py)). Five failed before the fix. The other three passed already, on purpose: they check answers that already worked and must keep working (a real `0` or `7` isn't questioned, `n` keeps 0.07%, and running out of input stops politely). That's fine. What matters is that at least one test fails because of the bug.

Then commit the test on its own. In Claude Code:

```text
Commit only the new test on this branch with the message "Test for bug N: <short name> (fails before the fix)".
```

Plain **Yes**. Committing the test first keeps it safe if you need to undo a fix (step 5). (The deal screener put its test and fix in one commit; you commit the test first so your history shows it failing before the fix.)

**d. Make one fix.** In Claude Code:

```text
Now make one fix: the smallest change to the code that fixes the cause you found. Don't change the test, and don't change anything unrelated to this bug. Then run all my tests and show me the result.
```

**Yes** to the edit if it's in the code file where the cause is. Check each edit before you answer, against the table under "How you'll work this week": **No** to anything unrelated, and **No** to any change to a test. *Deal screener:* one change in `dealscreener/__main__.py`. A percentage between 0 and 1 now gets one follow-up question:

```text
You typed 0.07. Did you mean 7%? Type y for 7%, or n to keep 0.07%:
```

**e. Check it, on your laptop and in Docker.** In your **second terminal window**:

1. Run your test command again. **Every** test must pass, not only the new one. For the deal screener: `Ran 47 tests` and `OK`. Take a **screenshot**: the assignment asks for it.
2. Run your program and type the bug's exact input from `BUGS.md`. The bug must be gone. *Deal screener:* `0.07`, then `y`, gave a monthly mortgage payment of $748.47 and cash flow $430.53, the same as typing `7`.
3. In the container (week 7): open Docker Desktop and wait until it says it is running, then build again, so the image has the fix, and run your test command in it:

   ```bash
   docker build -t semester-project .
   docker run --rm semester-project python -m unittest
   ```

   (Use your own test command from week 7 step 4c after `docker run --rm semester-project`.) The tests must pass there too. The deal screener's 47 tests passed in its container.

If a test fails, or the bug is still there, that's a failed attempt: tell Claude what you saw ("The test still fails: <paste the last 10 lines>. Find out why before changing anything."). After **two** failed attempts, go to step 5.

When everything passes, in Claude Code:

```text
Commit the fix on this branch with the message "Fix bug N: <short name>".
```

Plain **Yes**.

### 5. When you're in the loop

You're in the "fix it" loop when a fix doesn't work, or one fix breaks something else, and Claude goes straight to another change. **After two failed attempts, stop.** Press `Esc` to stop Claude, then do three things:

**a. Undo the attempts,** with [week 3's safe undo](../03-git-and-github/README.md#8-undo-safely): `git restore` for changes not yet committed, `git revert` for commits. Your failing test is already committed (step 4c), and so is `BUGS.md`, plus your feedback file if you made one (step 3d), so **every** uncommitted change is from the fix attempts: throw them all away. In Claude Code:

```text
Stop. Two fixes haven't worked. Throw away all my uncommitted changes with git restore; the test for this bug is already committed, so it stays. If any fix attempt was committed, undo that commit with git revert, so the history keeps a record. Show me each command before you run it, and don't use reset, --force or git clean.
```

It will probably run `git restore .` (this time that's right: everything uncommitted is a failed attempt) and, for a committed attempt, `git revert <commit> --no-edit`. Plain **Yes** to those; **No** to `git clean`, `reset` or `--force`. Then ask "What does git status say?": it should say `nothing to commit, working tree clean`. If it still lists a new file an attempt made, ask Claude what it is before anything deletes it. Your test should still be there and still fail.

**b. Ask for the cause before any change.** In Claude Code:

```text
Before you change anything else, explain in plain English what you now think causes this bug, what evidence shows it, what the two attempts changed, and why they didn't work. Then tell me the one change you would make next, and why it fixes the cause rather than hiding it. Don't make it yet.
```

Read the answer. Does it make sense with what you saw? Ask about anything that doesn't. When you're happy, type "Go ahead with that one change." and check it as in step 4e.

**c. Know the skill's own limit.** `systematic-debugging` stops at three: after a failed fix, "If < 3: Return to Phase 1, re-analyze with new information", and "DON'T attempt Fix #4 without architectural discussion" (its `SKILL.md`, Phase 4). Its next step is to "Discuss with your human partner before attempting more fixes": you're the human partner, which is why you ask for the cause. This course stops you at two, because each of your attempts costs you time and Claude usage. If a third attempt fails too, stop and bring your bug, your test and the conversation to office hours.

(Claude Code also has `/rewind`, or `Esc` twice, to undo its own edits, but it doesn't undo changes made by commands, so this course uses git.)

### 6. Finish

> **Being tested:** This step needs a signed-in session and a real GitHub account, and is being tested.

**a. Push and open a pull request.** In Claude Code:

```text
Push the fix-<short-name> branch to GitHub and open a pull request into main titled "Fix bug N: <short name>".
```

It will probably run `git push -u origin fix-<short-name>` and `gh pr create ...`. Plain **Yes** to each. Copy the pull request's address: you hand it in, and it goes in `BUGS.md` next.

**b. Update the bug in `BUGS.md`, then push again.** The template's Status line says "Fixed in <commit or PR link>". Use the pull request's address: a commit's hash can change when GitHub merges. In Claude Code, with the address you copied:

```text
In BUGS.md, update the bug we just fixed: set Status to "Fixed in <the pull request's address>", and write the Cause in one or two plain sentences: what was wrong in the code, and which test now checks it. Change nothing else. Then commit BUGS.md on this branch with the message "Bug N fixed: status and cause", and push the branch to GitHub.
```

Plain **Yes** to the edit, the commit and the push. The pull request updates by itself: refresh its page to see the new commit. The other bugs stay `Open`: you only fix one this week. The deal screener's finished entry is Bug 1 in [`example-project/BUGS.md`](../../example-project/BUGS.md) (it names a commit, because the instructor's fix wasn't merged through its own pull request).

**c. Read Files changed yourself, before you merge.** Open the address and click **Files changed** (week 6 step 2). You should see:

- the test file, with your new test;
- the code file with the fix, and only the lines the fix needs;
- `BUGS.md`;
- your `feedback-for-<partner>.md`, if you saved the form as a file.

Nothing else. In particular, no test deleted, no test's expected answer changed, and no `.env`. If something is there that shouldn't be, don't merge: ask Claude what it is and why.

**d. Merge on GitHub, then pull.** On the **Conversation** tab click **Merge pull request** and **Confirm merge** (or **Squash and merge**; the exact labels are being tested), as in [week 3](../03-git-and-github/) step 7. Then, in Claude Code:

```text
Switch back to main and pull the latest changes from GitHub.
```

Check: ask "What branch am I on, and do all the tests pass?". It should say `main`, and yes. Keep your local `fix-<short-name>` branch until your assignment is graded.

The deal screener's week 8 changes are on this page (it works once week 8 is published): <https://github.com/vasuchettyphd/ai-dev-course/compare/week-07...week-08>.

### 7. Check it worked

You're done when:

- You filled in the feedback form for your partner, with exact inputs and what happened, and you have it as a file or a photo.
- `BUGS.md` on `main` has at least one bug written with the exact input, what you expected, what happened, and whether it happens every time.
- Your fix's pull request is merged, and **Files changed** shows the test, the fix and `BUGS.md`, and nothing unrelated.
- You have a screenshot of the new test failing before the fix, and one of all the tests passing after it.
- On `main`, your tests pass on your laptop and in the container (with Docker Desktop running: `docker build -t semester-project .`, then your test command in it), and the bug's exact input no longer shows the bug.
- The fixed bug's Status and Cause are filled in.

`BUGS.md` was made on your `fix-<short-name>` branch, so it reaches `main` only when the fix is merged. The [assignment](assignment.md) asks for the form, the link to `BUGS.md` (on `main` after the merge; if your fix isn't merged, its link on your `fix-<short-name>` branch), the pull request's address, two screenshots and a short reflection.

## Troubleshooting

| What you see | What to do |
|---|---|
| You can't make the bug happen (step 3b) | Ask your classmate exactly what they typed, in what order, and what was on the screen. Start the program fresh and type it again, character for character, including spaces and Enter presses. Check you're running the same version they tried (the same branch, and the container if they used it). Write down anything that was different. If it still won't happen, set "Does it happen every time?" to `Not sure`, keep the bug in `BUGS.md`, and fix a bug you can reproduce this week. |
| The bug only happens sometimes | Note every time it happens and what was different: the inputs, their order, the data file, a run in Docker or not. Ask Claude: "This bug happens only sometimes: <when it did and didn't>. Find what's different between a run that works and one that fails. Don't change any file." Fix it only once you can make it happen on purpose; until then, fix another bug. |
| Claude wants to rewrite everything, or "tidy up" other code | Choose **No**. Type: "Only change what this bug needs: the smallest change that fixes the cause you found. No improvements while you're here." The skill itself says "ONE change at a time" and "No \"while I'm here\" improvements". |
| Claude starts changing code before it explains the cause, or before the test | Choose **No**. Type: "Stop. Explain the cause in plain English first, then write a failing test. Don't change the code yet." (Step 4a.) |
| The new test passes before the fix, so it doesn't catch the bug | Don't fix anything yet. Type: "The new test passes, but the bug still happens when I type <exact input>. Change the test so it uses exactly that input and checks the answer I expected. Don't touch the code." Run it again: it must fail. Other new tests passing is fine if they check things that already worked (step 4c). |
| The test fails with an error like `ImportError`, `NameError`, `SyntaxError` or "no tests ran", not with your bug's wrong answer | The test itself is broken. Type: "The test fails with <paste the error>, not because of the bug. Fix the test so it runs and fails only because of the bug. Don't touch the code." |
| Claude changed or deleted a test, or changed an expected answer to match the wrong output | Choose **No** if it's asking. If it already happened and isn't committed: "Undo your change to <test file> with git restore. Never change or delete a test to make it pass." If it was committed: "Undo that commit with git revert." Then check your expected answer against your hand working. |
| Your partner found nothing | Go through the odd-input list together, item by item (step 2d). Then try it yourself after class on the parts they didn't reach. Still nothing? Tell your instructor. |
| Your build is broken on demo day | Demo what does run, and log the break in `BUGS.md` as your first bug (step 2d). |
| The tests pass on your laptop but not in Docker | First build again: `docker build -t semester-project .` (an old image doesn't have the fix). Still failing? Ask Claude: "My tests pass on my laptop but fail in the container with <paste the last 20 lines>. Explain why in plain English before changing anything." Common causes: a different language version in the image, or a file `.dockerignore` leaves out (week 7). |
| `/superpowers:systematic-debugging` isn't in the list | Type `/reload-plugins`, then try again. Still missing? In a second terminal window, `claude plugin list`, and check `superpowers` is there and enabled; if not, do week 5 step 2 again. |
| Two fixes haven't worked | Stop: step 5. |
| `fatal: a branch named 'fix-...' already exists` | Add `-2` to the name (step 3a), here and everywhere this README says `fix-<short-name>`. |
| It committed to `main` | Say **No** to any push of `main`, and to `reset --hard` or `--force`. Then follow [week 5's "If it committed to `main`"](../05-building-with-ai/README.md#if-it-committed-to-main), using `rescue-fix-<short-name>` as the branch name. |
