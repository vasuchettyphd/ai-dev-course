# Week 5: Building with AI

**Goal:** build the first three steps of your `PLAN.md` with Claude Code and the Superpowers plugin: in small steps, each one tested first and reviewed before the next starts, on a branch, and merged through a pull request.

**Time:** plan for about 2 hours of your own time (an estimate), spread over more than one day: the build runs for a while by itself, and it can pause at a usage limit (step 6). **Start early in the week.** **Cost:** nothing beyond your Claude plan. Superpowers is free, and so are Python and Node.js.

**Tested with:** Claude Code 2.1.296, `superpowers` 6.4.1 and Python 3.12.3, on Ubuntu 24.04 Linux (in a container), 12 October 2026. The newest installers on the official sites that day were Python 3.15.0 (python.org) and Node.js 24.21.0 LTS (nodejs.org). These are the versions tested; yours may be newer. We tested, without signing in to Claude: installing Claude Code, installing and listing Superpowers from the terminal, reading the Superpowers instructions this week uses, installing Python with `apt` and running a test with it, and the deal screener example's tests and program (with Python 3.9 and newer). Everything inside a signed-in Claude Code session (the `/plugin` screen, choosing tools, writing the plan, the build, usage limits, finishing), everything on GitHub, installing Node.js, and every step on a Mac or in Windows (WSL) follow the official docs and are being tested on real Mac and Windows laptops.

## Before you start

You need:

- Week 4 done: your **private** `semester-project` repo on GitHub, with `vasuchettyphd` added, and `PLAN.md` merged into `main` through a pull request. Its "First three build steps" section is what you build this week.
- `gh` signed in to **your** GitHub account (in your terminal, `gh auth status` shows your username), and the branch, pull request and merge loop from [week 3](../03-git-and-github/) step 7.
- Claude Code signed in with your Claude Pro account (week 2).
- Time early in the week. The build uses a lot of your Claude usage (step 6), so don't leave it for the night before.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows, as in weeks 2 to 4. Every command below says where to type it: **in your terminal**, or **in Claude Code** (the `claude` session). On Windows, nothing this week goes in PowerShell.

Some steps say **in a second terminal window**: that means a new window, so Claude Code keeps running in the first one. On a Mac, click Terminal and press `Cmd + N`. On Windows, open **Ubuntu** again from the Start menu (don't type `wsl` in PowerShell). Then type `cd ~/semester-project` in the new window before anything else.

### How you'll work this week

As in weeks 3 and 4, you ask Claude Code in plain English. For each step this README shows **the prompt** to type, **what Claude Code will probably do** (its exact words will differ), and **what to check** afterwards.

Two rules for the prompts Claude Code shows you:

- For **git** commands, always pick plain **Yes**, never "Yes, and don't ask again" or "Yes, and switch to auto mode", so you see every commit and push.
- For **install** commands, read the command first (step 3 shows how), then pick plain **Yes** or **No**.

## Steps

### 1. What building with AI means

Last week you decided **what** to build. This week Claude builds it, and your job changes: you don't write the code, but you decide what gets built, you read what Claude asks to do, and you check that the result is right.

Asked to "build my project", Claude Code will happily write a big pile of code that looks right and quietly does the wrong math. Superpowers, the plugin you tried in week 4 (<https://github.com/obra/superpowers>), makes it work the careful way instead:

- **Small steps.** One build step at a time, never the whole project at once.
- **Tests first.** A **test** is a tiny program that checks the code's answer against an answer worked out by hand, for example "for this listing, the monthly cash flow must be $430.53". Claude writes the test, runs it and watches it **fail** (there's no code yet), then writes just enough code to make it **pass**. Superpowers' rule, in its own words: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST".
- **A review after every step.** A second Claude, which didn't write the code, checks each step against the plan before the next one starts. If it finds a problem, the step is fixed and checked again.

You use five parts of Superpowers (its **skills**) this week. Superpowers starts most of them for you.

| Skill | What it does | Step |
|---|---|---|
| `writing-plans` | Turns your first three build steps into a detailed plan file: tasks, tests and files | 4 |
| `subagent-driven-development` | Builds the plan task by task, with a fresh Claude (a **subagent**) for each task and another for each review | 5 |
| `test-driven-development` | The tests-first rule each task follows | 5 |
| `using-git-worktrees` | Offers to build in a separate folder; this week you say No (step 5) | 5 |
| `finishing-a-development-branch` | Runs the tests and offers to push and open a pull request | 7 |

For much more on how Superpowers works, read [the `/grill-me` and Superpowers tutorial](../../advanced/grill-me-superpowers/) (written for an earlier version; where it says to restart the session after installing, use `/reload-plugins` instead). Optional extra: [Beads](../../advanced/beads/) is a different way to keep an AI's task list between sessions; you don't need it this week.

### 2. Install Superpowers again

> **Being tested:** Installing from the terminal is from our test (without signing in). The `/plugin` screen needs a signed-in session and is being tested.

At the end of week 4 you removed Superpowers. Install it again, the same way. It's the same on Mac and Windows.

**a. Start Claude Code in your project.** In your terminal:

```bash
cd ~/semester-project && claude
```

Check the bottom line, and press `Shift + Tab` until it says `manual mode on`.

**b. Install it.** In Claude Code, type:

```text
/plugin install superpowers@claude-plugins-official
```

It opens the plugin's details. Choose **Install for you (user scope)**, not project scope. If the summary says `Run /reload-plugins to apply.`, type:

```text
/reload-plugins
```

**Or from your terminal** (open a second terminal window, or type `/exit` first):

```bash
claude plugin install superpowers@claude-plugins-official
```

In our test it ended with `Successfully installed plugin: superpowers@claude-plugins-official (scope: user)`. If it says the plugin was **not found in marketplace**, add Anthropic's official marketplace first (in a second terminal window, `claude plugin marketplace add anthropics/claude-plugins-official`), then run the install again. If you installed from the terminal while Claude Code was open, type `/reload-plugins` in Claude Code.

**c. Check it's installed.** In Claude Code, type `/plugin` and look for `superpowers` among your installed plugins (the exact screen is being tested; press `Esc` to close it). Or, in a second terminal window, type `claude plugin list`. In our test it showed:

```text
Installed plugins:
  superpowers@claude-plugins-official
    Version: 6.4.1
    Scope: user
    Status: enabled
```

Your version number may be higher. Superpowers stays installed from now on: you use it again in later weeks.

**d. Start a branch, before Claude writes anything.** You build on a branch, never on `main`, and you make the branch now, before step 3, so nothing Claude writes this week can land on `main`. First check that nothing is waiting to be saved. In Claude Code, type:

```text
Show me git status.
```

It should say `nothing to commit, working tree clean`. If it lists files, don't go on: ask "What are these files, and where did they come from? Don't change anything.", and ask in office hours if you're not sure. When it's clean, type:

```text
Switch to main and pull the latest changes from GitHub. Then make a new branch called build-first-steps and switch to it.
```

It will probably run `git switch main`, `git pull` and `git switch -c build-first-steps`. Plain **Yes**. Check: ask "What branch am I on?". It should say `build-first-steps`. (If it says a branch with that name already exists, use `build-first-steps-2` instead, here and everywhere this README says `build-first-steps`.)

### 3. Pick your tools

Your plan says **what** to build, but not which programming language and tools to build it with. Let Claude recommend them, with guardrails: it must run on a Mac and in WSL, and it must explain every install before it runs.

**a. Ask for a recommendation.** In Claude Code (still in `~/semester-project`, on `build-first-steps`, `manual mode on`), type this, with your own laptop in the brackets:

```text
Read PLAN.md. Recommend the simplest programming language and tools for building its first three build steps. I'm not a programmer. It must run on a Mac and on Windows in WSL (Ubuntu), and my laptop is [a Mac with an Apple chip / an Intel Mac / Windows with WSL Ubuntu]. Prefer what's already installed, as few installs as possible, and tests I can run with one command. Check what's already installed first. Before you run any install command, explain in one or two sentences what it installs and why, and wait for me to say go. Don't create or change any files yet.
```

**What Claude Code will probably do:** run a few checks such as `python3 --version` or `node --version` (plain **Yes**: they only print a version), then recommend a language. For a small tool that you type numbers or text into, that's usually **Python** (its tests come built in) or **Node.js** (JavaScript). If it recommends anything else, ask: "Can I do this with Python or Node.js instead?" Those two are the ones this README has official install links for.

If Superpowers starts **brainstorming** (asking design questions one at a time), see Troubleshooting: your design is already in `PLAN.md`.

**b. How to read an install prompt.** When Claude wants to run a command, Claude Code stops and shows it, then asks `Do you want to proceed?` with choices like **Yes**, **Yes, and don't ask again for: ...** and **No**. Before you choose, check three things:

1. **Did Claude explain it first?** If an install appears that it didn't explain, choose **No** and type: "Explain this command first: what does it install, and why?"
2. **Is it for your laptop?** Mac commands and Ubuntu commands look different (table below).
3. **Is it on the "say No" list?**

| Your laptop | Install commands that are fine | Say **No** to |
|---|---|---|
| Mac with an Apple chip | `brew install ...` (you installed Homebrew in week 3), or a `.pkg` installer you download yourself from the official links below | `apt`, `apt-get`, `winget`, `choco`, anything with `.exe` or `.msi` |
| Intel Mac | a `.pkg` installer you download yourself from the official links below | `brew` (no Homebrew on an Intel Mac in this course), `apt`, `apt-get`, `winget`, `choco`, `.exe`, `.msi` |
| Windows (WSL) | `sudo apt install ...`, and the Node.js commands below | `brew`, `winget`, `choco`, PowerShell commands, anything with `.exe`, `.msi` or `.pkg` |

Also say **No** to anything with `--force`, `rm -rf`, `--break-system-packages` or `sudo pip`, to any `curl ... | bash` (the one exception is the Node.js line in step 3d, on Windows only, which you type yourself), and to anything you don't understand. Saying No is always safe: Claude stops and asks what to do instead. Choose plain **Yes** for installs, never "don't ask again".

**On Windows (WSL), commands that start with `sudo`** ask for the Ubuntu password you made in week 2 (typing it shows nothing; that's normal). Run them **yourself, in a second Ubuntu window**, so the password goes to Ubuntu and never to Claude: when Claude asks to run one, choose **No**, type "I'll run that myself", copy the command into the second window, and tell Claude when it's done (being tested). **On a Mac,** the `.pkg` installers below ask for your Mac password in their own window. **Never type a password into Claude Code.**

**c. Install Python, if you need it.** Check first: in a second terminal window, type `python3 --version`.

- **Mac (Apple chip or Intel):** if it prints `Python 3.9` or any higher number, you already have it: it came with Apple's Command Line Tools in week 3. If it's lower, or a window offers to install the Command Line Tools, get the installer from python.org's Mac page, <https://www.python.org/downloads/macos/>: under "Latest Python 3 Release" (Python 3.15.0 when we checked), download the **macOS installer** (`python-3.15.0-macos11.pkg`; your number may be higher). The same installer works on Apple chip and Intel Macs; Python's docs say it "runs natively on all Macs (Apple Silicon and Intel)" (<https://docs.python.org/3/using/mac.html>). Double-click it in **Downloads** and follow the steps. Then come back as in "After an install" below, and type `python3 --version` (being tested). On an Apple chip Mac, Homebrew's Python is fine too; use a `.venv` for packages.
- **Windows (WSL):** if it prints a version, you have it. If it says `command not found`, type this yourself in the second **Ubuntu window**:

  ```bash
  sudo apt update && sudo apt install -y python3 python3-venv
  ```

  In our test (Ubuntu 24.04) this installed Python 3.12.3, and `python3 --version` then printed `Python 3.12.3`. If Python is there but Claude's plan needs extra Python packages, also install `python3-venv` this way (being tested on real WSL).

**Extra Python packages.** If the plan needs packages from outside Python (installed with `pip`), ask Claude to put them in a **virtual environment** in your project: "Use a virtual environment in .venv for any Python packages." In WSL (Ubuntu 24.04) and with Homebrew's Python on a Mac, plain `pip install` outside one is blocked (an `externally-managed-environment` error), so say **No** to `--break-system-packages`. In WSL, a virtual environment needs `python3-venv` (above). Being tested. The deal screener needs no extra packages at all.

**d. Install Node.js, if Claude chose it.** The official page is <https://nodejs.org/en/download> (Node.js 24.21.0 was the LTS, "long-term support", version when we checked; pick the LTS one). Being tested:

- **Mac (Apple chip or Intel):** on that page, download the **macOS Installer** (`.pkg`), double-click it in **Downloads** and follow the steps. Then come back as in "After an install" below.
- **Windows (WSL):** nodejs.org's Linux instructions use **nvm**, a Node.js version manager. Type these three lines yourself in a second **Ubuntu window**, one at a time, exactly as shown (they come from nodejs.org's own download instructions). The first line is this course's one exception to "say No to `curl ... | bash`": only on Windows (WSL), only this line, and you type it yourself:

  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
  \. "$HOME/.nvm/nvm.sh"
  nvm install 24
  ```

  Then come back as in "After an install" below.

**After an install,** your terminal has to be closed and opened again before it finds the new tool, and closing it also closes Claude Code. So:

1. In Claude Code, type `/exit`.
2. Close the window: on a Mac, quit Terminal (`Cmd + Q`); on Windows, close every Ubuntu window. Then open it again.
3. Type `cd ~/semester-project && claude`, and press `Shift + Tab` until the bottom line says `manual mode on`.
4. Tell Claude: "We chose [Python / Node.js]. It's installed. We're on the build-first-steps branch."

**e. Check what was installed.** In a second terminal window, type the line for your language:

```bash
python3 --version
```

```bash
node --version && npm --version
```

Each prints a version number. `command not found`? Do "After an install" (step 3d) and try once more; then see Troubleshooting. Tell Claude what they printed, for example: "Python 3.12.3 is installed now."

### 4. Plan the first three steps

> **Being tested:** This step needs a signed-in session and is being tested. What the plan contains comes from the `writing-plans` skill's own instructions (Superpowers 6.4.1).

**a. Keep tool folders out of git.** Some tools make big folders inside your project (`.venv/` for a Python virtual environment, `node_modules/` for Node.js, `__pycache__/` for Python's own scratch files, `.claude/worktrees/` for the extra folders Claude Code can make). They must never go to GitHub. Still on `build-first-steps`, in Claude Code, type:

```text
Add .venv/, node_modules/, __pycache__/ and .claude/worktrees/ to .gitignore (create it if it doesn't exist), and commit .gitignore on this branch.
```

It edits or creates `.gitignore` (an edit prompt) and commits it. Plain **Yes**.

**b. Ask for the plan.** In Claude Code, type:

```text
/superpowers:writing-plans Write an implementation plan for only the first three build steps in PLAN.md (the section "First three build steps"), one task per step, nothing else. Use the language and tools we just chose. Build each task test first, with tests I can run with one command, and include at least one example worked out by hand. I'm not a programmer, so keep each task small.
```

If `/superpowers:writing-plans` isn't in the list as you type, type `/reload-plugins` and try again, or start the prompt with `Use the superpowers writing-plans skill to` instead (being tested).

**What Claude Code will probably do:** say "I'm using the writing-plans skill to create the implementation plan.", read `PLAN.md`, then create one file (an edit prompt; plain **Yes**). The plan is saved in your project at:

```text
docs/superpowers/plans/YYYY-MM-DD-<name>.md
```

with today's date and a short name, for example `docs/superpowers/plans/2026-10-12-first-three-steps.md`.

**c. Read the plan.** Open it (or ask "Show me the plan file"). It starts with a **Goal**, an **Architecture** (how the pieces fit), a **Tech Stack** (your language and tools) and the **Spec** (your `PLAN.md`), then **Global Constraints** and a **Review Focus** (the risky cases the reviewers must check). Then come the tasks, `### Task 1:` and so on. Each task lists:

- **Files:** what it creates or changes, with the test file marked **Test:**.
- **Steps,** as checkboxes, always in this order: write the failing test, run it and see it fail, write the code, run it and see it pass, commit.

Check:

- There are **exactly three tasks**, one for each of your three build steps. More than three? See Troubleshooting before you go on.
- Every task **writes its test first**.
- The tests include an example **worked out by hand**, with the expected answer written in the plan.
- It doesn't add things from your "Not in this version" list.

To change something, tell Claude, for example: "Task 2 should also ...". It updates the plan.

**d. Work out your own example by hand.** Pick one example input of your own (not the plan's) and work out the answer yourself, on paper, in a spreadsheet or with a calculator. Keep it: in step 7 you run the finished program on it and compare, and the assignment asks for both side by side.

**e. The deal screener's plan, as an example.** The instructor's plan for the class example is [`example-project/docs/superpowers/plans/2026-10-12-first-three-steps.md`](../../example-project/docs/superpowers/plans/2026-10-12-first-three-steps.md). It's long (about 800 lines) because it holds every test and every line of code. Look at:

- the **Hand-worked listings** table near the top: two listings worked out by hand. Listing B's monthly cash flow is $430.53 and it passes the buy box; listing A fails on cash-on-cash return (5.744%, under the 10% rule).
- **Task 2: The buy-box check.** Step 1 writes `tests/test_buybox.py`, with tests such as `test_listing_a_fails_on_cash_on_cash_only`. Step 2 runs `python3 -m unittest` and expects it to **fail** with `ModuleNotFoundError: No module named 'dealscreener.buybox'`, because the code doesn't exist yet. Step 3 writes `dealscreener/buybox.py`. Step 4 runs the tests again and expects `Ran 21 tests` and `OK`. Step 5 commits.

Yours will be shorter or longer, in your own language; the shape is the same.

**f. Answer the handoff question.** When the plan is done, Claude asks something like: "Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Please review the plan. Which execution approach would you prefer?", with two choices:

| Choice | What it means |
|---|---|
| **Subagent-driven** | A fresh Claude builds each task, a fresh reviewer checks it before the next one starts, then the whole branch is reviewed at the end. Most thorough, uses more of your usage. |
| **Native** (also called "inline") | Claude builds every task itself in this session, with one review of the whole branch at the end. Cheaper and faster, no review after each task. |

It recommends one. **Choose Subagent-driven**, even if it recommends Native: the review after every step is what you're here to see. Only answer once you've read the plan and changed what you wanted. First type `/usage` and write down what it shows (step 6a). You need this 'before' number for the assignment. Then reply:

```text
Subagent-driven. Before you start building, commit the plan file on this branch if it isn't committed yet.
```

### 5. Build with `subagent-driven-development`

> **Being tested:** The build needs a signed-in session and is being tested. How it works comes from the `subagent-driven-development` skill's own instructions (Superpowers 6.4.1).

Your answer starts the build. Keep the bottom line at `manual mode on`.

**a. The worktree question: say No.** First, Superpowers may ask: "Would you like me to set up an isolated worktree? It protects your current branch from changes." A **worktree** is a second copy of your project in another folder, with its own branch. You don't need one: your `build-first-steps` branch already protects `main`. Reply:

```text
No. Work here, on the build-first-steps branch.
```

Superpowers then builds in your `~/semester-project` folder. If a worktree gets made anyway, see "If a worktree was made" below.

**b. What you'll see, task by task.** Before Task 1 it may run the tests once; with no tests yet it may ask whether to go on: answer Yes (being tested). The build runs **without stopping between tasks**. Claude writes at most a short line between actions, so you mostly see a stream of subagents starting and finishing, short status lines, and prompts for you to answer. For each task:

1. **An implementer** (a fresh Claude that sees only that task) writes the test, runs it and sees it **fail**, writes the code, runs the test and sees it **pass**, then commits. It reports back with a status: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT` or `BLOCKED`.
2. **A reviewer** (another fresh Claude) checks the work against the plan and for quality, and sorts what it finds as Critical, Important or Minor.
3. **Fixes,** if the reviewer found anything Critical or Important: the implementer fixes it and the reviewer checks again. This can repeat, up to 5 rounds per task. Minor findings are noted for later, not fixed now.

After the last task, one more reviewer checks the whole branch, there may be one more fix, and Claude lists the decisions it made on its own, under "Rulings I made". **Note one review finding and what changed because of it**: the assignment asks for one. Then it moves on to finishing (step 7).

The skill only stops to ask you for four reasons: something that can't be undone or deletes things, something security-sensitive, something that reaches outside your project (such as a push, a merge or publishing), or a plan so broken that any next step would be a guess. Everything else it decides and writes down.

**c. The ledger.** Superpowers keeps a progress file, the **ledger**, so a build can carry on after it stops. It's in your project folder at:

```text
.superpowers/sdd/<your-plan-file's-name>/progress.md
```

Its first line is `# SDD ledger`, followed by the plan's path, and it gets a line such as `Task 1: complete` as each task finishes. The folder also holds each task's brief and report. Git ignores it, so it doesn't appear in `git status` and never goes to GitHub. To check progress, ask "Show me the ledger", or open the file. Superpowers may ask to delete the folder when the build finishes (you can say No). Never ask Claude to "clean" untracked files (`git clean`) in the middle of a build: that deletes the ledger.

**d. Which prompts to say Yes or No to.** Read each one.

| Claude asks to | Choose |
|---|---|
| Create or edit files inside your project folder | **Yes** |
| Run the tests (for example `python3 -m unittest` or `npm test`) | **Yes** |
| `git add` or `git commit` on `build-first-steps` | plain **Yes** |
| An install it explained in step 3 | plain **Yes**, except a `sudo` command on Windows: **No**, and run it yourself (step 3b) |
| An install it didn't explain | **No**, then "Explain this command first" |
| Anything that **changes** `main` (`git switch main`, `git checkout main`, `git merge` into main, `git push origin main`, `git branch -f main`) | **No** |
| Read-only git commands that only mention `main` (`git diff`, `git log`, `git merge-base`, `git status`) | **Yes** |
| `git push` during the build | **No**: you push in step 7 |
| `--force`, `reset --hard`, `git clean`, `rm -rf` | **No** |
| At the very end, Claude may ask to delete `.superpowers/sdd/...` with `rm -rf` | **No** is fine. That folder is git-ignored and harmless. Type `Carry on without deleting it.` |
| Change files outside your project folder | **No** |

You ask Claude to switch to `main` only after the merge, in step 7d. After a No, Claude stops and asks what to do instead. Tell it, or type "Carry on with the plan without that."

**e. How to stop safely.** The safest moment is just after a task finishes (the ledger gets a `Task N: complete` line). Then press `Esc` to stop Claude, and type `/exit`. Everything finished so far is committed on your branch. If you have to stop in the middle of a task, press `Esc` anyway: that task may be redone when you carry on. Its files may not be committed yet. Ask "Show me git status" to see them, and leave them where they are: never `git clean`, `git restore` or `reset` them. When you carry on, Claude picks them up.

**To carry on later** (being tested): in your terminal, `cd ~/semester-project && claude`, press `Shift + Tab` until `manual mode on`, check "What branch am I on?" says `build-first-steps`, then type this, with your plan file's name:

```text
/superpowers:subagent-driven-development Continue the plan from the ledger. The plan is docs/superpowers/plans/<your-plan-file>.md.
```

It reads the ledger, skips the tasks marked complete, and carries on from the first one that isn't. If it asks the worktree question again, answer No again (step 5a).

**If a worktree was made** (being tested; from Claude Code's docs, <https://code.claude.com/docs/en/worktrees>): if you said Yes to the worktree question, your build happens in another folder, so your files seem to "disappear" from `~/semester-project`. They haven't.

- Claude Code's own worktrees are in `.claude/worktrees/<name>/` inside your project, on a branch called `worktree-<name>`. They start from `main` on GitHub. If Superpowers made the worktree itself, it's in `.worktrees/` instead.
- To list them, type `git worktree list` in a second terminal window, in `~/semester-project`.
- When you `/exit`, Claude Code may ask whether to keep or remove the worktree. Choose **Keep**. Removing it deletes the folder, its branch and all the work in it.
- To go back to it, type the command Claude Code prints when you exit, which looks like `claude --worktree <name> --resume`.
- The worktree started from GitHub's `main`, so it may not have your plan file or `.gitignore`. Before step 7, type in Claude Code: `Merge the build-first-steps branch into this branch.` Plain Yes. In step 7d, check Files changed shows the plan file (being tested).
- The ledger and the build are in the worktree folder, so carry on from there. Your pull request in step 7 comes from the worktree's branch. If anything is unclear, ask in office hours before you delete anything.

### 6. Usage limits

> **Being tested:** Usage limits need a signed-in session. The messages below are from Claude Code's docs, <https://code.claude.com/docs/en/errors>, and are being tested.

Your Claude Pro plan has a **five-hour session limit** and a **weekly limit**, and Claude and Claude Code share them: chatting on claude.ai uses the same allowance (Claude's help article, <https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan>). Anthropic doesn't publish a fixed number of messages, so this README doesn't give one.

**Subagent-driven building uses more, honestly.** Every subagent sends its own requests, and Claude Code's docs say they "count toward the same usage limits as your main conversation" (<https://code.claude.com/docs/en/sub-agents>). A build with an implementer and a reviewer for every task, plus fixes and a final review, uses more than one ordinary conversation. Nobody publishes how much more; it depends on your plan's size.

**a. Check your usage.** In Claude Code, type:

```text
/usage
```

On a Pro plan it shows your plan's usage bars, when they reset, and which share went to skills, subagents and plugins (<https://code.claude.com/docs/en/costs>). Press `d` or `w` to switch between day and week. (Claude's help article names `/status` for the same check; Claude Code's docs name `/usage`. Use whichever your version shows.) Check it before you start the build, and again after: the assignment asks roughly how much of your usage the build took.

**b. What happens at the limit.** You'll see warnings as you get close. At the limit, Claude Code shows a message like `You've hit your session limit · resets 3:45pm` (or `weekly limit`, with a day), and stops sending requests until that time. Switching models doesn't help: the limits cover all models.

**c. Wait for the reset, then carry on.** You don't need to buy anything.

- **Leave Claude Code open,** and it carries on by itself after the reset. It shows something like `Continuing automatically at 3:45pm · esc to cancel`. Keep your laptop awake; if it slept a long time, it shows "Press enter to continue". It can still stop at a permission prompt while you're away, so check on it.
- **If you closed Claude Code,** come back after the reset time, and carry on with the prompt from step 5e (`Continue the plan from the ledger`).
- If auto-continue stops after several limits in a row, carry on from the ledger after the reset (step 5e).

**d. Start early in the week.** A big build can use up a five-hour session, and a heavy day can eat into your weekly limit too. Starting early leaves time to wait for a reset and still finish.

### 7. Finish

> **Being tested:** This step needs a signed-in session and a real GitHub account, and is being tested. The menu below is from the `finishing-a-development-branch` skill's own instructions.

When the build is done, Superpowers moves on to `finishing-a-development-branch` by itself. It runs all the tests first and only goes on if they pass. Then it asks something like:

```text
Implementation complete. What would you like to do?
1. Merge back to main locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
Which option?
```

**Don't answer yet.** First check the work yourself.

**a. Run the tests yourself.** Open a second terminal window. Type `cd ~/semester-project`, then the test command from your plan's **Tech Stack** (for example `python3 -m unittest` or `npm test`). For the deal screener, in our test:

```text
Ran 32 tests in 0.002s

OK
```

Yours will say something like "all passed", in your language's words. Take a **screenshot**: the assignment asks for it.

**b. Run your program on your own example.** Still in your second terminal window, start your program the way the plan or Claude says (for the deal screener, `python3 -m dealscreener`). Type in your example from step 4d, and compare its answer with the one you worked out by hand. They should match (to the cent, for money). Take a **screenshot** of the program's answer with your hand-worked answer beside it.

Don't match? Don't answer the menu. Tell Claude: "For this input [your input], I worked out [your answer] by hand, but the program says [its answer]. Find out which is right before changing anything." Sometimes the hand working is the one that's wrong.

For the deal screener, listing B (price 150000, rent 1700, tax 2400, insurance 1200, HOA 0, down payment 25, interest rate 7, loan term 30, closing costs 6000) gives the hand-worked answer in the program:

```text
Monthly mortgage payment: $748.47
Monthly cash flow: $430.53
Cap rate: 9.43%
Cash-on-cash return: 11.88%

PASS  Cash-on-cash return 11.88% is at least 10.00%
PASS  Monthly cash flow $430.53 is at least $100.00

Overall: PASS
```

**c. Choose push and pull request.** Back in Claude Code, answer the menu:

```text
2
```

**Never choose 1** (that merges into `main` on your laptop, skipping the pull request). It will probably run `git push -u origin build-first-steps` and `gh pr create ...`. Plain **Yes** to each. It prints the pull request's address. Copy it: you hand it in. If it asks "This branch split from main - is that correct?", answer yes. The menu has no "throw it away" choice, and you don't need one.

If the menu never appeared (for example, you stopped and came back), type `/superpowers:finishing-a-development-branch` in Claude Code.

**d. Merge on GitHub, then pull.** As in [week 3](../03-git-and-github/) step 7: open the PR's address and read **Files changed**. You should see only your plan file, `.gitignore`, your code and your tests. If you see a `.venv/`, `node_modules/` or `__pycache__/` folder, don't merge: ask Claude "Remove .venv, node_modules and __pycache__ from git (keep them on my laptop), make sure .gitignore lists them, commit and push." Then on the **Conversation** tab click **Merge pull request** and **Confirm merge** (or "Squash and merge"; the exact label is being tested). Then, in Claude Code:

```text
Switch back to main and pull the latest changes from GitHub.
```

Check: ask "Is my plan file in this folder, and what branch am I on?". The plan file and your code should be there, on `main`.

Your laptop still has the `build-first-steps` branch. That's harmless: keep it until your assignment is graded. If Claude or GitHub offers to delete a branch or a worktree, answer **No** on your laptop. (Deleting the branch on GitHub after the merge, as in week 3, is fine.)

### 8. Check it worked

You're done when:

- Your pull request's page on GitHub shows it was merged, and **Files changed** shows the plan file under `docs/superpowers/plans/`, `.gitignore` (if step 4a changed it), your code and your tests, and no tool folders.
- On `main`, in your terminal in `~/semester-project`, your tests pass.
- Your program gives the same answer as your hand-worked example.
- You've noted one review finding and what changed, and roughly how much of your usage the build took (from `/usage`).

The [assignment](assignment.md) asks for the PR's address, two screenshots and a short reflection.

## Troubleshooting

| What you see | What to do |
|---|---|
| The tests fail (in step 7, or Claude says they do) | Don't merge. In Claude Code: "The tests fail. Show me which test fails and why, in plain English, then fix the code, not the test." If a test's expected answer is wrong, check it against your hand working first. |
| An install command for the wrong laptop (`apt` on a Mac, `brew` on an Intel Mac or in WSL, `winget`, `.exe` or PowerShell on Windows) | Choose **No**. Type: "That's not for my laptop. I'm on [a Mac with an Apple chip / an Intel Mac / Windows with WSL Ubuntu]. Use the official installer for it, and explain it first." |
| `python3: command not found` or `node: command not found` | Do "After an install" (step 3d): `/exit`, close and reopen your terminal, start Claude Code again, then try again. On Windows, check you're in the **Ubuntu window**, not PowerShell. Still missing? Do step 3c or 3d again. |
| `command not found` for something Claude installed | Do "After an install" (step 3d). If you used a virtual environment, ask Claude: "How do I run the tests and the program with the virtual environment?" |
| `error: externally-managed-environment` | Choose **No** to `--break-system-packages`. Ask Claude: "Use a virtual environment in .venv instead." In WSL, install `python3-venv` first (step 3c). |
| (being tested) Superpowers starts brainstorming, asking design questions one at a time | Type: "Skip brainstorming: PLAN.md is the design. Use writing-plans for its first three build steps." |
| `/superpowers:...` isn't in the list | Type `/reload-plugins`, then try again. Still missing? In a second terminal window, `claude plugin list`, and check `superpowers` is there and enabled; if not, do step 2 again. |
| `You've hit your session limit` or `weekly limit` | Normal. Wait for the reset time it shows (step 6). Leave Claude Code open, or come back later and carry on (step 5e). If you hit the weekly limit with days to go, tell your instructor. |
| A task goes round and round in review and fix rounds | Up to 5 rounds per task is normal; after that Claude decides and writes down a ruling. If it seems stuck, press `Esc` and ask: "Summarise in plain English what's still failing and why." Check `/usage`. Ask in office hours if it's still stuck. |
| (being tested) A worktree folder appeared, or "my files disappeared" | They're in a worktree, on another branch (step 5, "If a worktree was made"). In a second terminal window, `git worktree list` shows where. When you exit, choose **Keep**, never remove. Don't delete any folder yourself. |
| Claude asks to keep or remove a worktree | Choose **Keep**. |
| It committed to `main` | Say **No** to any push of `main`, and to `reset --hard` or `--force`. Then follow "If it committed to `main`" below. |
| `fatal: a branch named 'build-first-steps' already exists` | Use `build-first-steps-2` instead (step 2d), here and everywhere this README says `build-first-steps`. |
| The plan has more than three tasks | Before you choose Subagent-driven, type: "Rewrite the plan with exactly three tasks, one for each of the first three build steps in PLAN.md. Leave everything else out." Then read it again (step 4c). |
| The program's answer doesn't match your hand-worked answer | See step 7b. Check your hand working too. |

### If it committed to `main`

> **Being tested** with real students. The git commands were tested in a scratch repository on Linux, 12 October 2026.

If Claude committed your work on `main` instead of your branch, you move the work to a new branch yourself. Type these commands **yourself, in a second terminal window** (Terminal on a Mac, a second Ubuntu window on Windows), one at a time, and check each result before the next.

```bash
cd ~/semester-project
git fetch
```

`git fetch` gets GitHub's latest state without changing your files. It may print nothing.

```bash
git log --oneline origin/main..main
```

This lists the commits that are only on your laptop's `main`, one per line, such as `a1b2c3d Add the calculator`. **If it prints nothing,** type `git status`. If it lists your files, they are not committed yet: run only `git switch -c rescue-first-steps` (it carries them) and skip `git branch -f`. If it is clean too, stop and ask in office hours.

```bash
git switch -c rescue-first-steps
```

This makes a new branch at the same commit and moves you onto it, carrying any unsaved changes with you. Nothing is lost. It prints `Switched to a new branch 'rescue-first-steps'`.

```bash
git log --oneline origin/main..rescue-first-steps
```

This must list **the same commits** as before. If it doesn't, stop and ask in office hours.

```bash
git branch -f main origin/main
```

This moves only the `main` label back to match GitHub. Your files and the new branch are untouched. In our test it printed `branch 'main' set up to track 'origin/main'.` This is **the one exception** to "never change `main`", and only now, because your work is safe on `rescue-first-steps`. Never use `reset --hard` or `--force`, and never push `main`.

Then, in Claude Code, type:

```text
Work on the rescue-first-steps branch from now on.
```

From here, read `rescue-first-steps` wherever this README says `build-first-steps`, and carry on (step 5e) or finish (step 7).
