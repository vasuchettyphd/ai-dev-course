# Week 4: Planning a project

**Goal:** choose the small tool you'll build this term, give it its own private GitHub repo, plan it with Claude Code's plan mode, have the plan questioned hard with `/grill-me`, and save the result as `PLAN.md` through a pull request.

**Time:** plan for about 90 minutes (an estimate); the grilling can take longer if your idea is big. **Cost:** nothing beyond your Claude plan. The add-in you install is free.

**Tested with:** Claude Code 2.1.296, `mattpocock-skills` 1.2.3, `superpowers` 6.4.1 and AI-DLC 2.11.0, on Ubuntu 24.04 Linux (in a container), 12 October 2026. These are the versions tested; the official add-in marketplace updates itself, so yours may be newer. We tested, without signing in to Claude: installing Claude Code, adding Anthropic's official add-in marketplace, installing, listing, updating and removing the add-ins from the terminal, reading the `/grill-me` and Superpowers instructions inside them, and installing and setting up AI-DLC. Everything inside a signed-in Claude Code session (plan mode, the `/plugin` screen, running `/grill-me`, writing `PLAN.md`, Superpowers and AI-DLC runs), everything on GitHub, and every step on a Mac follow the official docs and are being tested on real Mac and Windows laptops.

## Before you start

You need:

- Week 3 done: git set up with your private `noreply` email, `gh` signed in to **your** GitHub account (in your terminal, `gh auth status` shows your username), and the branch, pull request and merge loop from [week 3](../03-git-and-github/) step 7.
- Claude Code signed in with your Claude Pro account (week 2).
- Two or three rough ideas for a tool you'd find useful. Step 2 helps you pick one.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows, as in weeks 2 and 3. Every command below says where to type it: **in your terminal**, or **in Claude Code** (the `claude` session, which looks the same on every laptop). On Windows, nothing this week goes in PowerShell.

### How you'll work this week

As in week 3, you ask Claude Code in plain English. For each step this README shows **the prompt** to type, **what Claude Code will probably do** (its exact words will differ), and **what to check** afterwards. For git commands, always pick plain **Yes**, never "Yes, and don't ask again" or "Yes, and switch to auto mode", so you see every push.

## Steps

### 1. Why plan first

Claude Code will build almost anything you describe. That's the problem: describe a tool in a hurry and it builds exactly what you said, which is rarely what you meant, and you find out only after the work is done. Twenty minutes of planning saves hours of building the wrong thing.

This week you plan in three layers:

| Layer | What it does | What you get |
|---|---|---|
| **Plan mode** | Claude Code reads and thinks, but can't change files. It proposes a plan. | A first draft of the plan, on screen |
| **`/grill-me`** | Claude questions your plan, round by round, until every hidden assumption is decided | Sharper decisions, in your head and on screen |
| **`PLAN.md`** | Claude writes the decisions into a file with a fixed outline, and you merge it through a pull request | The plan, saved in your project repo |

Next week, [Building with AI](../05-building-with-ai/), you build the first steps of `PLAN.md`.

For much more on `/grill-me` (how it chooses its questions, and how to get real value out of it), read [the `/grill-me` and Superpowers tutorial](../../advanced/grill-me-superpowers/): a longer walkthrough, written for an earlier version. Where it says to restart the session after installing, use `/reload-plugins` instead.

### 2. Pick your idea

Your project is a **small tool**: something useful for your work, studies or a business idea, which you build up week by week and demo in week 14. Later weeks add AI to it (calling a model in week 9, searching your own documents in week 10), so an idea with a part where AI could help (summarising, sorting, drafting, answering questions) is a good sign.

**The checklist.** A good idea:

- does **one job** for **one kind of person** (you count),
- fits in one sentence: "It takes ___ and gives me ___",
- works with data you can **type in, make up, or are allowed to use** (a small spreadsheet is plenty),
- has **3 to 5 must-haves**, not 20,
- could be shown working in **3 minutes** at the week 14 demo.

**The too-big test.** If your idea has any of these, it's too big for this term. Cut it down to the smallest useful piece.

- It's "a platform", "an app like Uber for ..." or "an all-in-one ..."
- It needs several kinds of users (buyers and sellers, students and tutors), sign-ups or logins
- It takes payments, or needs a phone app store
- It needs live data from websites you'd have to copy automatically, or other people's private data
- You can't say who would use it first

| Too big | Just right |
|---|---|
| An app that runs my whole small business | A tool that turns my weekly sales spreadsheet into a one-page summary |
| A marketplace that matches tutors and students | A study planner that spreads my revision over the days before each exam |
| An AI financial adviser | A budget checker that flags spending categories over my own monthly limits (typed in, no bank connection) |
| A social network for student clubs | An event budget planner for one club's events |
| A real estate investing platform | A rental deal screener that says whether one listing meets my rules (the class example) |

**Example ideas** that are about the right size:

1. **Rental deal screener:** type in a listing's numbers, get cash flow and returns, and a pass or fail against your rules. This is the class example: see [`example-project/`](../../example-project/).
2. **Freelance quote calculator:** hours, materials and your margin in; a price and a short quote out.
3. **Club event budget planner:** a list of costs and expected attendance in; a ticket price that breaks even.
4. **Sales summary:** a spreadsheet export (made up, or your own that you're allowed to use) in; the week's totals and top products out.
5. **Job application tracker:** the roles you've applied for in; which ones need a follow-up this week, with a draft note.
6. **Product description writer:** a few facts about a product in; a short shop description in your brand's voice.
7. **Café reorder checker:** stock counts and usual weekly use in; what to reorder and how much.
8. **Customer feedback sorter:** public or made-up reviews in; the main themes and an example of each.

**Keep sensitive personal data out.** Your project must not use:

- health or medical information,
- financial account, card or ID numbers (Social Security numbers, passport numbers, bank details),
- other people's private information: customer lists, employee records, classmates' grades, private messages,
- passwords, keys or sign-in codes,
- anything your employer, school or anyone else hasn't allowed you to use.

Use made-up data, public data, or your own non-sensitive data instead. A budget checker with made-up amounts is fine; one connected to your real bank account isn't. This matters again in week 13, Security and responsible use.

Write your idea down in one sentence before you go on. You'll type it in step 4.

### 3. Make your project repo (private)

> **Being tested:** This step needs a real GitHub account and is being tested. If something looks different, tell your instructor.

Your project gets its **own new private repo**. `my-first-project` from week 3 stays as your practice repo.

**a. Make the folder and start Claude Code.** In your terminal, type:

```bash
cd ~ && mkdir semester-project && cd semester-project && claude
```

Claude Code may ask whether you trust the files in this folder. It's your own new, empty folder, so say yes. Then check the bottom line, and press `Shift + Tab` until it says `manual mode on`.

**b. The prompt.** In Claude Code, type this, with your own one-sentence idea in place of the example:

```text
Create README.md with the title "Semester project" and this one-sentence description of my idea: "A tool that turns my weekly sales spreadsheet into a one-page summary." Make this folder a git repository with the branch name main, and commit README.md with the message "Start project". Then use gh to create a new PRIVATE GitHub repository called semester-project from this folder, with the remote named origin, and push the main branch. It must be private.
```

**What Claude Code will probably do:**

- create `README.md` (an edit prompt)
- run `git init -b main` (or `git init` then `git branch -M main`), `git add` and `git commit -m "Start project"`
- run a command like this one:

```bash
gh repo create semester-project --private --source=. --remote=origin --push
```

Read each prompt and choose plain **Yes**. **Before you say Yes to `gh repo create`, look for `--private`** in the command. If you see `--public`, or no `--private`, choose **No** and tell it: "It must be private."

**c. What to check.** Claude Code should show the new repo's address, like `https://github.com/yourusername/semester-project`. Open it in your browser. You should see `README.md`, **your** username in the address, and a **Private** label next to the repo's name. If it's public or under someone else's account, stop and see the troubleshooting table.

**d. Add your instructor as a collaborator,** exactly as in [week 3](../03-git-and-github/) step 9. On github.com:

1. Open your repo's main page (`https://github.com/yourusername/semester-project`).
2. Click **Settings** (if you don't see it, it's in the **...** "More" menu).
3. In the "Access" section of the sidebar, click **Collaborators**.
4. Click **Add people**.
5. Type `vasuchettyphd` and select it from the matches.
6. Click **Add vasuchettyphd to semester-project**.

The **Collaborators** list should now show `vasuchettyphd` as a pending invitation (being tested). Don't make the repo public so your instructor can see it: the invitation is how they get in.

### 4. Plan in plan mode

> **Being tested:** Plan mode needs a signed-in session, so the exact screens are being tested. The behaviour below is from Claude Code's docs, <https://code.claude.com/docs/en/permission-modes>.

In **plan mode**, Claude Code reads files and thinks, then proposes a plan. It doesn't edit your files until you approve the plan. The docs: "Plan mode tells Claude to research and propose changes without making them."

**a. Switch to plan mode.** Still in Claude Code in `semester-project`, press `Shift + Tab` and watch the bottom line. Keep pressing until it says `plan mode on` (from manual mode it's two presses; from auto mode, three). The order, from week 2:

```text
auto mode on  ->  manual mode on  ->  accept edits on  ->  plan mode on  ->  back to auto
```

(Or skip the key presses: type `/plan` followed by your prompt, and that one prompt runs in plan mode.)

**b. The prompt.** In Claude Code, type this, with your own idea:

```text
I want to build this for my semester project: "A tool that turns my weekly sales spreadsheet into a one-page summary." I'm not a programmer, and I have about eight weeks to build it, a few hours a week. Don't build anything yet. Propose a plan: who it's for, the 3 to 5 must-haves, what to leave out of the first version, what data it uses, and the first three build steps. Keep it small, and point out anything that looks too big.
```

**What Claude Code will probably do:** read the folder, maybe ask you a question or two, then show a plan and ask how to proceed.

**c. Don't approve it for building.** The docs list approve options such as "Yes, and use auto mode" (or "Yes, auto-accept edits"), "Yes, manually approve edits", and "No, keep planning"; your labels may differ. The approve options mean "start building now": the docs say "approving a plan exits plan mode ... so Claude starts editing". You're not building this week. So:

- To change something: choose **No, keep planning**, and tell Claude what to change. It updates the plan.
- When the plan looks reasonable: choose **No, keep planning**, then press `Shift + Tab` to leave plan mode without approving. Keep pressing until the bottom line says `manual mode on`.

Optional: press `Ctrl + G` while the plan is shown to open it in a text editor and change it yourself.

Claude Code keeps its own copy of plans in a hidden folder on your laptop (`~/.claude/plans/`). That copy isn't part of your project, which is why you write `PLAN.md` in step 6.

### 5. Install `/grill-me` and get grilled

> **Being tested:** Installing from the terminal is from our test (without signing in). The `/plugin` screen and running `/grill-me` need a signed-in session and are being tested.

`/grill-me` comes in **`mattpocock-skills`**, a free add-in (a **plugin**) by Matt Pocock, from Anthropic's official marketplace (<https://github.com/mattpocock/skills>). You install it once, and it works in every folder. It's the same on Mac and Windows: you type it inside Claude Code.

**a. Install it.** In Claude Code, type:

```text
/plugin install mattpocock-skills@claude-plugins-official
```

This doesn't install straight away: it opens the plugin's details so you can choose where it applies. Choose **Install for you (user scope)**. Don't choose project scope: that changes settings inside your project repo. If the summary says `Run /reload-plugins to apply.`, type:

```text
/reload-plugins
```

**Or from your terminal** (open a second terminal window, or type `/exit` first):

```bash
claude plugin install mattpocock-skills@claude-plugins-official
```

In our test it printed:

```text
Installing plugin "mattpocock-skills@claude-plugins-official"...✔ Successfully installed plugin: mattpocock-skills@claude-plugins-official (scope: user)
```

If it says the plugin was **not found in marketplace**, add Anthropic's official marketplace first, then run the install again. In your terminal:

```bash
claude plugin marketplace add anthropics/claude-plugins-official
```

In our test it ended with `✔ Successfully added marketplace: claude-plugins-official (declared in user settings)`. (Inside Claude Code, the same thing is `/plugin marketplace add anthropics/claude-plugins-official`.) If you installed from the terminal while Claude Code was open, type `/reload-plugins` in Claude Code.

**b. Check it's installed.** In Claude Code, type `/grill` and look at the list that appears: you should see `/grill-me`. Or, in your terminal, type `claude plugin list`. In our test:

```text
Installed plugins:

  ❯ mattpocock-skills@claude-plugins-official
    Version: 1.2.3
    Scope: user
    Status: ✔ enabled
```

Your version number may be higher.

**c. Start the grilling.** Make sure the bottom line says `manual mode on`. In Claude Code, type:

```text
/grill-me Grill me on the plan you just proposed for my semester project. I'm not a programmer and I have about eight weeks to build it.
```

If `/grill-me` isn't in the list, type `/mattpocock-skills:grill-me` instead (being tested). If you closed Claude Code since step 4, put your one-sentence idea in place of "the plan you just proposed".

**What it does** (from the skill's own instructions, at <https://github.com/mattpocock/skills>):

- It asks in **rounds**. Each round is a batch of **numbered questions**, and each question comes with Claude's **recommended answer**. Your answers unlock the next round.
- **Reply by number**, in one message. For example: `1 yes. 2 no, only me for the first version. 3 I don't know yet, put it in open questions.`
- **Facts are Claude's job, decisions are yours.** It may look something up before asking (if it asks to search the web or read a file, plain **Yes** is fine). What your tool does, who it's for and what to leave out are your calls. Push back when a recommendation is wrong for you.
- **It changes no files.** If it asks to edit or create a file during the grilling, choose **No**.

**As you go, copy the three questions you find hardest, and your answers, into a note.** The assignment asks for them.

**d. How it ends.** It finishes when there are no open questions left, and it asks you to confirm that you both agree. Read its summary, correct anything that's wrong, then say so, for example: `Yes, we agree.`

**To stop early** (you're out of time, or it's going round in circles), type:

```text
Stop grilling, summarise the decisions so far
```

Anything not decided goes under "Open questions" in your plan.

### 6. Write `PLAN.md` and merge it through a pull request

> **Being tested:** This step needs a signed-in session and a real GitHub account, and is being tested.

`/grill-me` writes no file, so now you ask Claude to write the decisions down. Every `PLAN.md` in this course uses the same outline:

```text
# Plan: <your project's name>
## Goal
## Who it's for
## Must-haves
## Not in this version
## Data it uses
## First three build steps
## Open questions
```

See the instructor's worked example: [`example-project/PLAN.md`](../../example-project/PLAN.md).

**a. Write it on a branch.** Check the bottom line says `manual mode on`. In Claude Code, type:

```text
Make a new branch called add-plan. On it, write PLAN.md from our grilling session, with a title line "# Plan: <my project's name>" and exactly these seven headings, in this order: Goal, Who it's for, Must-haves, Not in this version, Data it uses, First three build steps, Open questions. Use my answers, not your own ideas. Be specific: numbers, names and examples. Keep it to about one page. Show it to me before you commit.
```

**What Claude Code will probably do:** `git switch -c add-plan`, then create `PLAN.md` (an edit prompt). Choose plain **Yes**.

**b. Read it, and make it specific.** Open `PLAN.md` (or ask "Show me PLAN.md"). Check:

- Every heading is there, in order.
- It says what **you** decided. If something's wrong, tell Claude: "Change the must-haves: ..."
- It's specific. "Must-have: easy to use" is vague. "Must-have: shows the week's total sales in dollars, and the top 3 products" is specific.
- No sensitive personal data (step 2): no real customer names, account numbers or passwords.

**c. Commit, push and open the pull request.** In Claude Code, type:

```text
Commit PLAN.md on the add-plan branch, push the branch to GitHub, and open a pull request titled "Add project plan" with a short description of what the plan covers.
```

It will probably run `git add PLAN.md`, `git commit`, `git push -u origin add-plan` and `gh pr create ...`. Plain **Yes** to each. It prints the pull request's address. Copy it: you hand it in.

**d. Merge on GitHub, then pull.** As in [week 3](../03-git-and-github/) step 7: open the PR's address, read **Files changed**, then on the **Conversation** tab click **Merge pull request** and **Confirm merge** (or "Squash and merge"). Then, in Claude Code:

```text
Switch back to main and pull the latest changes from GitHub.
```

Check: ask "Is PLAN.md in this folder, and what branch am I on?". `PLAN.md` should be there, on `main`.

### 7. Two other ways to plan (optional)

You don't need either of these for the assignment. Your instructor demonstrates both in class on the deal screener. They're here so you can compare.

| | Plan mode + `/grill-me` (this week) | Superpowers | AWS AI-DLC |
|---|---|---|---|
| **What it is** | A Claude Code mode plus a free plugin (`mattpocock-skills`) | A free plugin (`superpowers`, by Jesse Vincent) that gives Claude a careful build process | A free, open-source workflow from AWS (`awslabs/aidlc-workflows`) that runs inside Claude Code and other AI tools |
| **How it plans** | Plan mode drafts a plan; `/grill-me` asks rounds of numbered questions with recommended answers | Brainstorming asks one question at a time, proposes 2 or 3 approaches, then gets your approval section by section | Runs through phases (Initialization, Ideation, Inception, Construction, Operation), one stage at a time, and stops for your approval at each gate |
| **What it produces** | Nothing by itself; you ask for `PLAN.md` | A design file and a step-by-step build plan, saved under `docs/superpowers/` and committed to git | A folder of records for each stage under `aidlc/`, plus a `.claude/` folder with about 40 AI-DLC skills |
| **When to use it** | Any idea, even with no software at all. Best for deciding what to build | When you're ready to build software and want it built in small, tested steps | Team software projects that want a full, documented process |

Both Superpowers and AI-DLC are made for building software, and both write many files. **If you try either, use a throwaway folder, never your project repo this week**, and only after your `PLAN.md` pull request is merged.

**Next week you build with Superpowers**, so you'll install it then anyway.

#### Try Superpowers

> **Being tested:** Running Superpowers needs a signed-in session and is being tested.

**Try it only after your `PLAN.md` pull request is merged.** A plugin installed "for you" (user scope) is switched on in **every** folder, including `semester-project`, and Superpowers' brainstorming can start by itself whenever you ask Claude to build or change something. So try it, then remove it until next week (see the end of this part).

**a. Make a throwaway folder and start Claude Code there.** In your terminal:

```bash
mkdir -p ~/planning-sandbox && cd ~/planning-sandbox && git init && claude
```

**b. Install it,** the same way as `mattpocock-skills` (choose **Install for you (user scope)**, then `/reload-plugins` if asked). In Claude Code:

```text
/plugin install superpowers@claude-plugins-official
```

**c. Try it.** In Claude Code, type:

```text
/superpowers:brainstorming I want to plan a tool that turns my weekly sales spreadsheet into a one-page summary.
```

It asks one question at a time, then writes a design file to `docs/superpowers/specs/` and asks you to review it. Source: <https://github.com/obra/superpowers>. The [advanced tutorial](../../advanced/grill-me-superpowers/) shows a full run.

**d. Remove it when you're done.** In Claude Code, type `/plugin uninstall superpowers@claude-plugins-official` (it opens the plugin screen; choose to uninstall it there, being tested), or in your terminal:

```bash
claude plugin uninstall superpowers@claude-plugins-official
```

In our test it printed `✔ Successfully uninstalled plugin: superpowers (scope: user)`. If Claude Code is open, type `/reload-plugins`. You install it again next week.

#### Try AI-DLC

> **Being tested:** Installing and setting up AI-DLC is from our test, on Linux. Running `/aidlc` needs a signed-in session and is being tested. Source: <https://github.com/awslabs/aidlc-workflows>.

AI-DLC also gives Claude Code permission to edit any file in the folder without asking. That's another reason to keep it in a throwaway folder.

**a. Install it.** In your terminal (on Windows, in the **Ubuntu window**, never PowerShell), paste this line from AI-DLC's README:

```bash
curl -fsSL https://github.com/awslabs/aidlc-workflows/releases/latest/download/install.sh | sh
```

In our test it ended with:

```text
PASS installed AI-DLC 2.11.0 with all harness runtimes
Next: aidlc config
```

**b. Set it up in a throwaway folder.** In your terminal, make the folder (if you haven't already) and set AI-DLC up in it:

```bash
mkdir -p ~/planning-sandbox && cd ~/planning-sandbox && git init
aidlc config --harness claude && aidlc doctor
```

`aidlc config` writes its files (`aidlc/` and `.claude/`) into this folder.

In our test, `aidlc config` printed `configured /home/student/proj for Claude Code 2.11.0; next: open Claude Code in this project ...` and `aidlc doctor` ended with:

```text
0 problems, 4 warnings.
Warnings are advisory - if everything works, ignore them.
```

**c. Run it.** Start Claude Code in that folder (`claude`; if it was already open there, type `/exit` and start it again). Then, in Claude Code:

```text
/aidlc Plan a tool that turns my weekly sales spreadsheet into a one-page summary
```

It works through its stages and stops at each approval gate for you to approve, revise or skip.

### 8. Check it worked

You're done when:

- `https://github.com/yourusername/semester-project` exists and is marked **Private**, under **your** username.
- In the repo's **Settings > Collaborators**, `vasuchettyphd` is listed. (Exactly how a pending invitation looks is being tested.)
- Your "Add project plan" pull request's page on GitHub shows it was merged. (The exact label is being tested.)
- `PLAN.md` is on `main`, on GitHub and in `~/semester-project` on your laptop, with all seven headings, in order.
- You've noted the three hardest `/grill-me` questions and your answers.

The [assignment](assignment.md) asks for the repo's address, a screenshot, the merged PR's address and your three hardest questions.

## Troubleshooting

| What you see | What to do |
|---|---|
| `/grill-me` isn't in the list when you type `/grill` | Type `/reload-plugins`, then try again. Still missing? Type `/mattpocock-skills:grill-me`. Still missing? In your terminal, type `claude plugin list` and check `mattpocock-skills` is there and enabled; if not, do step 5a again. |
| `Plugin "mattpocock-skills" not found in marketplace "claude-plugins-official"` | Add the official marketplace first: in your terminal, `claude plugin marketplace add anthropics/claude-plugins-official`, then install again (step 5a). |
| (being tested) The `/plugin` screen asks where to install | Choose **Install for you (user scope)**, not project scope. |
| (being tested) In plan mode, Claude asks to edit or create a file in your project folder | Choose **No**. Check the bottom line says `plan mode on`. Plan mode shouldn't edit files until you approve a plan. |
| You approved the plan by mistake, and Claude is building | Press `Esc` to stop it. Choose **No** to any edit prompt. Then ask: "What files did you create or change? Don't change anything else." If it made changes you don't want, ask in office hours before you delete anything. |
| The grilling goes on and on | Type `Stop grilling, summarise the decisions so far`. If it keeps opening new topics round after round, your idea is probably too big: go back to the too-big test in step 2. |
| (being tested) It answers its own questions, or decides for you | Tell it: "The decisions are mine. Ask me, with your recommendation." |
| Claude asks to edit a file during the grilling | Choose **No**. `/grill-me` writes no files. You write `PLAN.md` in step 6. |
| `gh repo create` shows `--public`, or no `--private` | Choose **No** and say: "It must be private." |
| The repo is public | (being tested) On github.com, open the repo, then **Settings**. In the **Danger Zone** at the bottom, click **Change visibility**, choose private, and follow the confirmation steps until you click **Make this repository private**. |
| The repo is under the wrong GitHub account | (being tested) Type `/exit`, then in your terminal `gh auth logout`. Sign out of github.com in your browser (or use a private window) and sign in with your own account. Then `gh auth login` (week 3 step 4), start `claude` in `~/semester-project` again, and ask it to create the repo again. Tell your instructor about the repo on the wrong account. |
| (being tested) `gh repo create` says the name already exists | You already have a repo called `semester-project`. Open `https://github.com/yourusername/semester-project` and check it's **Private**. Then ask Claude Code: "Connect this folder to my existing private GitHub repository semester-project as origin and push main, instead of creating a new one. Don't force-push." Say **No** to any prompt with `--force`. |
| `PLAN.md` was committed on `main`, not on `add-plan` | Don't undo it, and say **No** to `reset --hard` or `--force`. Ask Claude Code to push `main`. Then make your next change to `PLAN.md` (for example, answer one open question) on a new branch and through a pull request, as in step 6, and hand in that PR. |
| `PLAN.md` has headings missing or in a different order | Ask Claude Code: "Rewrite PLAN.md with exactly these seven headings, in this order: ..." and paste the outline from step 6. |
| `! [rejected]        main -> main (fetch first)` | You merged on GitHub and didn't pull. Ask Claude Code: "Pull the latest changes from GitHub as a merge (git pull --no-rebase --no-edit), then push again. Don't reset or force-push." |
| (being tested) `aidlc: command not found` | Close your terminal and open it again, then try again. On Windows, check you're in the **Ubuntu window**, not PowerShell. |
| You tried Superpowers or AI-DLC in your project repo, or Superpowers started brainstorming there (new files under `docs/superpowers/`) | Ask Claude Code: "Show me git status." Don't commit those files. Ask in office hours how to remove them safely. To stop Superpowers starting by itself this week, remove it (step 7, Try Superpowers, part d). |
