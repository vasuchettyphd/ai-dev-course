# Week 3: Git and GitHub

**Goal:** save versions of your work with git, keep a private copy of it on GitHub, make a change through a pull request, and undo a change safely, all by asking Claude Code in plain English.

**Time:** plan for about 90 minutes (an estimate); installing Homebrew on a Mac can make it longer. **Cost:** nothing beyond your Claude plan. A GitHub account is free.

**Tested with:** git 2.43.0 and GitHub CLI (`gh`) 2.102.0 on Ubuntu 24.04 Linux (in a container), 12 October 2026. We tested installing git and `gh`, and every git step that runs on your own computer, using a stand-in for GitHub: creating a repository, saving snapshots, a branch, comparing versions, discarding a change, reverting a commit and a rejected push. Everything that needs a real GitHub account, and every step on a Mac, follows GitHub's, Homebrew's and Apple's docs and is being tested on real Mac and Windows laptops. The git steps and the `gh auth login` questions were also tested in Ubuntu on WSL 2 (Windows) with git 2.53.0 and `gh` 2.102.0, 29 October 2026, again with a stand-in for GitHub.

## Before you start

You need:

- Week 2 done: Claude Code installed and signed in, and your practice folder `~/my-first-project` with `hello.md` and `CLAUDE.md` in it. If you don't have the folder, make it: in your terminal, type `cd ~` then `mkdir my-first-project`. Then, in your terminal, type `cd ~/my-first-project && claude`, and ask Claude Code: "Create hello.md with three tips for using Claude Code, and a short CLAUDE.md describing this folder." Approve the two new files, then type `/exit` to leave Claude Code.
- On a Mac: **macOS 15 (Sequoia) or later** (Apple menu > About This Mac), and an **administrator** account on the Mac. If your Mac is older, or it's a work or school Mac where you aren't an administrator, tell your instructor now: the course's Mac steps need both.
- An email address you can open now, to create a GitHub account.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows, as in week 2. Every command below says where to type it. On Windows, nothing this week goes in PowerShell.

### What git and GitHub are

**Git** saves **snapshots** of the files in a folder. Each snapshot is called a **commit**: a picture of what all your files looked like at that moment, with a short message saying what changed and why. The list of commits is your project's **history**, and you can always go back to an earlier one.

A folder that git looks after is a **repository**, or **repo** for short.

A **branch** is a safe draft. You make a branch, try a change on it, and your main version (the branch called `main`) stays exactly as it was. If you like the draft, you bring it into `main`. If you don't, you throw the draft away and nothing is lost.

**GitHub** (github.com) is a website that keeps an online copy of your repo. It's your backup, and the place where others can see your work if you let them. Your repos this term are **private**: only you, and the people you invite, can see them. Your business ideas stay yours.

A **pull request** (PR) is how a change on a branch asks to join `main` on GitHub. It means "review before it becomes official": you, or a teammate, read exactly what changed, then click a button to **merge** it.

### Why this matters with AI

Claude Code changes real files on your laptop. Usually that's what you want. Sometimes it changes something you didn't expect, or a good idea turns out badly. Git is your **undo button**: commit before you ask for a big change, and you can always get back to that snapshot.

| Word | Plain meaning |
|---|---|
| repository (repo) | a folder whose history git keeps |
| commit | a saved snapshot, with a message |
| history | the list of snapshots, newest first |
| branch | a safe draft; `main` is the official version |
| push | send your new commits up to GitHub |
| pull | bring new commits down from GitHub |
| pull request (PR) | a request to bring a branch into `main`, reviewed first |
| merge | bring the branch's changes into `main` |

### How you'll work this week

You don't need to memorise git commands. You ask Claude Code in plain English, and it runs the commands for you. For each step, this README shows:

1. **The prompt** to type into Claude Code.
2. **What Claude Code will probably do:** the commands it's likely to run, and the permission prompts it may show. Its exact words and order may differ; the commands should be similar.
3. **What to check** afterwards.

Claude Code runs read-only git commands, such as `git status`, `git log` and `git diff`, without asking. Commands that change something, such as `git add`, `git commit`, `git push`, `git restore` and `git revert`, will show a permission prompt. Read each one before you say Yes. Use **manual mode** (`Shift + Tab` until the bottom line says `manual mode on`) so you see every step.

## Steps

### 1. Create a GitHub account and keep your email private

> **Being tested:** These steps need a real GitHub account and are being tested. If something looks different, tell your instructor.

**a. Sign up.** In your web browser, go to <https://github.com/signup> and follow the prompts. Pick a username you're happy for an employer to see. GitHub asks you to verify your email address; do it, because some basic GitHub tasks don't work without it.

**b. Keep your email private.** Every commit records a name and an email. If you push commits with your personal email, that email becomes visible to anyone who can see the repo. GitHub gives you a private stand-in address instead. On github.com:

1. Click your profile picture (upper right), then **Settings**.
2. In the "Access" section of the sidebar, click **Emails**.
3. Tick **Keep my email addresses private**.
4. Also tick **Block command line pushes that expose my email**.

Near the "Keep my email addresses private" setting, GitHub shows your private address. It looks like `12345678+yourusername@users.noreply.github.com` (a number, a plus sign, your username). Copy it; you need it in step 2. (Exactly where GitHub shows it is being tested.) If you can't find it, look on the same **Emails** page for text ending in `users.noreply.github.com` and copy all of it exactly, including the number. Still can't find it? Ask in office hours.

**Optional:** students can apply for the free GitHub Student Developer Pack at <https://github.com/settings/education/benefits>. You don't need it for this course.

### 2. Check git, and tell it who you are

**On a Mac.** In **Terminal**, type:

```bash
git --version
```

> **Being tested:** On any Mac (Apple chip or Intel) without Apple's developer tools, the first `git --version` may open a window asking to install the "command line developer tools". Click Install, wait for it to finish, then type `git --version` again.

**On Windows.** In the **Ubuntu window**, type:

```bash
git --version
```

You should see a version number. In our test:

```text
git version 2.43.0
```

Any version is fine. If instead the Ubuntu window says git is not found (in our test: `git: command not found`), install it, then try `git --version` again:

```bash
sudo apt update && sudo apt install -y git
```

It asks for your Ubuntu password from week 2. Typing it shows nothing; that's normal.

**Tell git who you are.** Git won't save a snapshot until it knows your name and email. In your terminal, type these two lines. Use your own name, and the private `noreply` address you copied in step 1:

```bash
git config --global user.name "Your Name"
git config --global user.email "12345678+yourusername@users.noreply.github.com"
```

They print nothing. To check, type:

```bash
git config --global user.email
```

It should print your `noreply` address.

### 3. Install the GitHub CLI (`gh`)

`gh` is GitHub's own command-line tool. Claude Code uses it to create your GitHub repo and open pull requests, and you use it to sign in to GitHub from the terminal.

#### On a Mac: first, check your chip

Click the Apple menu, then **About This Mac**.

- If it shows **Chip** followed by a name such as `Apple M1`, your Mac has an **Apple chip**. Follow "On a Mac with an Apple chip" below.
- If it shows **Processor** followed by an **Intel** name, it's an **Intel Mac**. Skip Homebrew and follow "On an Intel Mac" below.

(Apple's own page explains this: <https://support.apple.com/en-us/116943>.)

#### On a Mac with an Apple chip: with Homebrew

> **Being tested:** These steps are being tested on a real Mac laptop. If something looks different, tell your instructor.

**Homebrew** is a free installer for Mac tools. It supports macOS 15 (Sequoia) and later, on Macs with Apple chips.

You need an **administrator** account on the Mac. The installer uses `sudo` (a command that asks for administrator rights), so it asks for your Mac login password, and it stops if your account isn't an administrator. If it's a work or school Mac where you aren't an administrator, ask in office hours.

**a. Install Homebrew.** If you already use Homebrew, skip to step c. Otherwise, in **Terminal**, paste this line exactly (from <https://brew.sh>) and press Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- It explains what it will do, then pauses. Press **Return** to continue.
- It asks for your Mac login password. Typing it shows nothing; that's normal.
- It can take several minutes.

**b. Run the "Next steps" lines.** At the end, the installer prints **Next steps** with one or more lines to run. Copy and run **exactly the lines it prints**, in Terminal.

Then close Terminal (`Cmd + Q`), open it again, and check:

```bash
brew --version
```

It should print `Homebrew` followed by a version number (being tested). Still `command not found`? Come to office hours.

**c. Install `gh`.** In **Terminal**, type:

```bash
brew install gh
```

#### On an Intel Mac: GitHub's installer

> **Being tested:** These Intel Mac steps are being tested. If something looks different, tell your instructor.

Homebrew's installer only works on Macs with Apple chips, so on an Intel Mac you install `gh` with GitHub's own installer instead.

**a. Download it.** In your web browser, open GitHub's official release page for `gh`: <https://github.com/cli/cli/releases/latest>. Scroll down to **Assets** and click the file whose name ends in `_macOS_universal.pkg`. When we checked (release 2.102.0) it was called `gh_2.102.0_macOS_universal.pkg`; your number may be higher.

**b. Open it.** In **Finder**, open your **Downloads** folder and double-click the file. macOS will probably block it, because GitHub doesn't sign this installer at the moment. GitHub's install page (<https://github.com/cli/cli/blob/trunk/docs/install_macos.md>) says: "As of May 29th, Mac OS installer .pkg are unsigned with efforts prioritized in cli/cli#9139 to support signing them." Close the warning, but don't delete the file.

**c. Allow it, this once.** Click the Apple menu, then **System Settings**, then **Privacy & Security** in the sidebar. Scroll down to **Security** and click **Open Anyway** (Apple says the button is there for about an hour after you tried to open the file). Enter your Mac login password if asked. The installer opens; follow its steps to the end.

This is the one exception in this course. It's safe here because the file comes from GitHub's own release page, and GitHub's own docs say it isn't signed. Apple warns that overriding security settings "is the most common way that a Mac gets infected with malware", so **never** click Open Anyway for other downloads, for files from emails or chat messages, or for websites you don't know.

**d. Check it.** Close Terminal (`Cmd + Q`), open it again, and do "Check it worked" below.

#### On Windows: in the Ubuntu window

On Windows you install `gh` inside Ubuntu (WSL), with GitHub's official steps. Type it in the **Ubuntu window**, never in PowerShell.

**a. Install `gh`.** In the **Ubuntu window**, paste this whole block (`Ctrl + Shift + V` or right-click) and press Enter. It comes from GitHub's install page, <https://github.com/cli/cli/blob/trunk/docs/install_linux.md>:

```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
	&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
	&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& sudo mkdir -p -m 755 /etc/apt/sources.list.d \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y
```

It asks for your Ubuntu password. Lots of text scrolls past; near the end, look for a line like `Setting up gh (2.102.0) ...` (your number may be higher).

If the paste stops partway (for example after the password, or with an error), paste the whole block again. If that still fails, paste it one line at a time.

#### Check it worked (Mac and Windows)

In your terminal, type:

```bash
gh --version
```

You should see two lines like these. Your numbers will probably be higher; any version is fine:

```text
gh version 2.102.0 (2026-09-30)
https://github.com/cli/cli/releases/tag/v2.102.0
```

### 4. Sign in to GitHub with `gh`

> **Being tested:** Signing in needs a real GitHub account, so the browser sign-in is being tested. The questions below were checked on Windows (WSL) with `gh` 2.102.0. If something looks different, tell your instructor.

In your terminal, type:

```bash
gh auth login
```

It asks a few questions. Use the arrow keys and Enter, and choose:

| It asks about | Choose |
|---|---|
| where you use GitHub | **GitHub.com** |
| your preferred protocol for Git operations | **HTTPS** |
| whether to authenticate Git with your GitHub credentials | **Y** (yes) |
| how to authenticate | **Login with a web browser** |

(If `gh` has been set up before, it may skip the question about authenticating Git.)

Then it shows a **one-time code** and asks you to press Enter to open github.com in your browser. Press Enter, sign in to GitHub in the browser if asked, type the code, and approve.

- **On Windows (WSL):** the browser may not open by itself (it did not on our Ubuntu 26.04 test). `gh` copies the code to your Windows clipboard and may print `! Failed opening a web browser at https://github.com/login/device`. If no browser opens, that's fine: go to <https://github.com/login/device> in your normal Windows browser and paste (or type) the code there.
- **On Windows (WSL), being tested:** `gh` may say it saved your sign-in in a plain-text file, because Ubuntu here has no credential store. That's expected here; carry on.
- Never create, copy or paste a "personal access token" for this course. The browser sign-in is all you need.

**Check who you're signed in as.** In your terminal, type:

```bash
gh auth status
```

It should show that you're logged in to github.com, with **your** GitHub username, in a line like `✓ Logged in to github.com account yourusername`. (The rest of that line after a browser sign-in is being tested.) If you're not signed in, you'll see:

```text
You are not logged into any GitHub hosts. To log in, run: gh auth login
```

If it shows someone else's username (for example on a shared laptop), type `gh auth logout`. Before signing in again, sign out of github.com in your browser (or use a private window), then sign in there with your own account. Then type `gh auth login` again.

### 5. Make `my-first-project` a git repository

> **Being tested:** Claude Code's prompts below were checked on Windows (WSL); the Mac check is still being done. The git output below is from our test.

**a. Start Claude Code in your folder.** In your terminal, type:

```bash
cd ~/my-first-project && claude
```

Check the bottom line, and press `Shift + Tab` until it says `manual mode on`.

**b. The prompt.** Type this into Claude Code and press Enter:

```text
Make this folder a git repository with the branch name main. Then save a first snapshot (a commit) of all the files, with the message "First snapshot". Explain each command before you run it.
```

**What Claude Code will probably do:**

- run `git init -b main`, or `git init` followed by `git branch -M main` (both give you a branch called `main`)
- run `git add` to choose the files for the snapshot, then `git commit -m "First snapshot"`

Each of these shows a permission prompt. Read it: the command should start with `git`, and it should stay in your `my-first-project` folder. Choose **Yes**.

Claude Code may also add a line like `Co-Authored-By: Claude ...` to each commit message. That's normal: it records that Claude helped.

For git commands, always pick plain **Yes**. Never pick "Yes, and don't ask again" or "Yes, and switch to auto mode" for git, so you see every push. (Claude Code's permissions page, <https://code.claude.com/docs/en/permissions>, lists these options; "don't ask again" for a command is saved for this repo for good.)

Why `main`: plain `git init` names the first branch `master` and prints a long `hint:` about branch names. GitHub calls its main branch `main`, so you want `main` from the start.

**c. What to check.** Ask Claude Code:

```text
Show me the git history and the current branch.
```

It will probably run `git log` (maybe `git log --oneline`) and `git branch --show-current`, and may describe the history in its own words instead of showing the raw lines. You should see one commit in the history: a code, then your message. The code is different for everyone. In our test, a first commit looked like this:

```text
74659dd Add README
```

(From our test; yours says `First snapshot`.)

and the branch:

```text
main
```

**d. A second snapshot.** Ask:

```text
Add a fourth tip to hello.md, then commit it with a short message that says what changed.
```

Approve the edit and the commit. Then ask "Show me the git history" again. Now there are two lines, newest first. That list is your history: two snapshots you can always go back to.

**Good habit:** before you ask Claude Code for a big change, ask it to commit first. Then your undo button is ready.

### 6. Put it on GitHub, as a private repo

> **Being tested:** This step needs a real GitHub account and is being tested. If something looks different, tell your instructor.

**a. The prompt.** In Claude Code, type:

```text
Use gh to create a new PRIVATE GitHub repository called my-first-project from this folder, with the remote named origin, and push the main branch. It must be private.
```

**What Claude Code will probably do:** run a command like this one, and show you a permission prompt for it:

```bash
gh repo create my-first-project --private --source=. --remote=origin --push
```

**Before you say Yes, look for `--private`** in the command. If you see `--public`, or no `--private`, choose **No** and tell it: "It must be private." This one check is what keeps your work from going public by mistake.

When it finishes, Claude Code should show the new repo's address, like `https://github.com/yourusername/my-first-project`.

**b. What to check.** Open that address in your browser. You should see your files (`hello.md`, `CLAUDE.md`) and a **Private** label next to the repo's name. (The label's exact look is being tested.) If it isn't private, fix it now: see "The repo is public" in the troubleshooting table.

### 7. Change something through a pull request

> **Being tested:** This step needs a real GitHub account and is being tested. If something looks different, tell your instructor.

This is the loop you'll use all term: **branch, change, push, pull request, merge, pull.**

**a. Make a change on a branch, and open a PR.** In Claude Code, type:

```text
Make a new branch called add-goals. On it, create goals.md with three goals I have for this course, commit it, push the branch to GitHub, and open a pull request with a clear title and a short description of what changed and why.
```

**What Claude Code will probably do:**

- `git switch -c add-goals` (makes the branch and moves onto it; in our test, with a branch called `feature-intro`, it printed `Switched to a new branch 'feature-intro'`)
- create `goals.md` (an edit prompt), then `git add` and `git commit`
- `git push -u origin add-goals` (sends the branch to GitHub)
- `gh pr create --title "..." --body "..."` (opens the pull request)

It may ask you what your three goals are; tell it. When `gh pr create` works, it prints the pull request's address. Copy it: you hand it in.

**b. Review and merge on GitHub.** Open the PR's address in your browser.

1. Read the title and description. Click **Files changed** to see exactly what's different. This is the "review before it becomes official" part.
2. Go back to the **Conversation** tab. At the bottom of it, click **Merge pull request**, then **Confirm merge**. (Depending on the repo's settings the button may say "Squash and merge" instead; that's fine too.)
3. GitHub offers **Delete branch**. You can click it: the draft's work is now in `main`.

**c. Pull the merged result back to your laptop.** The merge happened on GitHub, so your laptop doesn't have it yet. In Claude Code, type:

```text
Switch back to main and pull the latest changes from GitHub.
```

It will probably run `git switch main` then `git pull`. Then check: ask "Is goals.md in this folder, and what does the history look like now?". `goals.md` should be there, on `main`.

**Rule of thumb: pull after you merge.** If you forget and commit on `main`, GitHub will refuse your next push with `rejected ... (fetch first)`. The fix is this prompt:

```text
Pull the latest changes from GitHub as a merge (git pull --no-rebase --no-edit), then push again. Don't reset or force-push.
```

In our test (against a stand-in for GitHub), `git pull --no-rebase --no-edit` printed `Merge made by the 'ort' strategy.` and the push that followed worked.

### 8. Undo safely

Two kinds of undo, and Claude Code should use exactly these:

| You want to | Ask for | What it does |
|---|---|---|
| throw away a change you haven't committed yet | `git restore` | puts the file back to the last snapshot. **That change is gone for good.** |
| undo a change you already committed (and maybe pushed) | `git revert` | makes a new commit that does the opposite. History keeps both, so nothing is lost. |

**Never let it use `git reset --hard` or `git push --force` on work you've pushed.** Those can delete history. If a permission prompt shows either one, choose **No** and ask for `git revert` instead.

**a. Discard an uncommitted change.** In Claude Code, type:

```text
Add a line saying "Oops, a mistake" to the end of hello.md. Don't commit it.
```

Approve the edit. Then ask "What does git status say?". It should say `hello.md` is modified. In our test, `git status` looked like this:

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

(Yours says `hello.md`.) Now type:

```text
Throw away my uncommitted change to hello.md with git restore.
```

It will probably run `git restore hello.md`. Check the command names `hello.md` only; if you see `.` or `git clean`, choose **No**. Otherwise approve it. `git restore` asks no question and has no undo, so only use it on changes you really don't want. Ask "What does git status say?" again. In our test:

```text
On branch main
nothing to commit, working tree clean
```

**b. Revert a commit.**

> **Being tested:** This part pushes to GitHub, so it is being tested. The revert itself is from our test.

First make a small commit to undo. In Claude Code, type:

```text
Add a line saying "This line will be undone" to hello.md, commit it, and push main to GitHub.
```

Approve the edit, the commit and the push. Now undo it:

```text
Undo my last commit with git revert, so the history keeps a record. Don't use reset. Then push main to GitHub.
```

It will probably run `git revert HEAD --no-edit` (or `git revert --no-commit HEAD` followed by a `git commit`), then `git push`. In our test, a revert printed:

```text
[main 9fe6f0b] Revert "Add intro line"
 Date: Mon Oct 12 13:17:27 2026 +0000
 1 file changed, 1 deletion(-)
```

**What to check:** ask "Show me the git history". The newest line starts with `Revert "`, and the commit it undid is still listed below it. In our test:

```text
9fe6f0b Revert "Add intro line"
2be7a5d Add intro line
74659dd Add README
```

The line is gone from `hello.md`, and the history shows both what you did and that you undid it.

### 9. Add your instructor as a collaborator

> **Being tested:** This step needs a real GitHub account and is being tested. If something looks different, tell your instructor.

Your repo is private, so your instructor can't see it until you invite them. Do this on github.com, in your browser:

1. Open your repo's main page (`https://github.com/yourusername/my-first-project`).
2. Click **Settings** (if you don't see it, it's in the **...** "More" menu).
3. In the "Access" section of the sidebar, click **Collaborators**.
4. Click **Add people**.
5. Type `vasuchettyphd` and select it from the matches.
6. Click **Add vasuchettyphd to my-first-project**.

Check it worked: the **Collaborators** list should now show `vasuchettyphd` as a pending invitation (being tested). If you misspelled the name, remove that entry and add `vasuchettyphd` again.

GitHub emails your instructor an invitation. Once they accept it, they can see your repo. You don't need to do anything else. Don't change the repo to public so your instructor can see it: the invitation is how they get in.

## Check it worked

You're done when:

- `gh auth status` in your terminal shows you're signed in with your own GitHub username. Type `/exit` to leave Claude Code first (or open a new terminal).
- Your repo `https://github.com/yourusername/my-first-project` exists and is marked **Private**.
- Your `add-goals` pull request's page on GitHub shows it was merged. (The exact label is being tested.)
- `goals.md` is in `~/my-first-project` on your laptop, on the `main` branch.
- The history (ask Claude Code "Show me the git history") includes a line starting with `Revert "`.
- In your repo's **Settings > Collaborators**, `vasuchettyphd` is listed. (Exactly how a pending invitation looks is being tested.)

The [assignment](assignment.md) asks for the repo's address, the merged PR's address and a short reflection. Next week, [Planning a project](../04-planning/), you choose the tool you'll build this term. Next week you'll make a new private repo for your project the same way (steps 6 and 9). `my-first-project` stays as your practice repo.

## Troubleshooting

| What you see | What to do |
|---|---|
| `Author identity unknown` and `*** Please tell me who you are.` | Git doesn't know your name and email yet. Do "Tell git who you are" in step 2, then ask Claude Code to commit again. |
| `fatal: not a git repository (or any of the parent directories): .git` | You're not inside a repo. In your terminal, `cd ~/my-first-project`, start `claude` there, and do step 5 if you haven't. |
| The branch is called `master`, not `main` (for example `git switch main` says `fatal: invalid reference: main`) | Ask Claude Code: "Rename this branch to main with `git branch -M main`." Do this before you push to GitHub. |
| `fatal: No configured push destination.` | This folder isn't connected to GitHub yet. Do step 6. |
| `! [rejected]        main -> main (fetch first)` with `Updates were rejected because the remote contains work that you do not have locally` | GitHub has commits your laptop doesn't, usually because you merged a PR. Ask Claude Code: "Pull the latest changes from GitHub as a merge (git pull --no-rebase --no-edit), then push again. Don't reset or force-push." Say **No** to any prompt that contains `--force` or `reset --hard`. |
| `Need to specify how to reconcile divergent branches` | Same cause and same fix. Ask Claude Code: "Pull the latest changes from GitHub as a merge (git pull --no-rebase --no-edit), then push again. Don't reset or force-push." |
| The repo is public | (being tested) On github.com, open the repo, then **Settings**. In the **Danger Zone** at the bottom, click **Change visibility**, choose private, and follow the confirmation steps until you click **Make this repository private**. |
| `gh auth status` shows the wrong username | (being tested) Type `gh auth logout` and answer the questions it asks (which account, and to confirm). Before signing in again, sign out of github.com in your browser (or use a private window), then sign in there with your own account. Then type `gh auth login`. |
| `You are not logged into any GitHub hosts. To log in, run: gh auth login` | Do step 4. |
| A push is refused with a message about exposing your private email | (being tested) Your commits use your personal email. Do step 1b and "Tell git who you are" in step 2 with your `noreply` address, then ask Claude Code: "Change the author email on my commits that are not on GitHub yet to my noreply address, without losing any files. Don't force-push and don't use reset --hard." Say **No** to any prompt that contains `--force` or `reset --hard`. If you're unsure, stop and ask in office hours. |
| `! Failed opening a web browser at https://github.com/login/device` during `gh auth login` (WSL) | Expected in WSL. The code is already on your clipboard. Open <https://github.com/login/device> in your Windows browser and paste the code. |
| (being tested) `gh repo create` says the repository name already exists (for example after a first try that failed) | The repo was already made on GitHub. First open `https://github.com/yourusername/my-first-project` in your browser and check it says **Private** (if not, see "The repo is public"). Then ask Claude Code: "Connect this folder to my existing private GitHub repository my-first-project as origin and push main, instead of creating a new one. Don't force-push." Say **No** to any prompt that contains `--force`. Or choose a new name. |
| `gh: command not found` (or `brew: command not found` on a Mac) | Apple-chip Mac: run the "Next steps" lines the Homebrew installer printed (step 3b), close and reopen Terminal, then `brew --version`; still not found? Come to office hours. Intel Mac: close and reopen Terminal; still not found? Come to office hours. Windows: make sure you're in the **Ubuntu** window, not PowerShell, then redo step 3. |
| (being tested) A Mac window asks to install "command line developer tools" (on any Mac, for example on your first `git --version`) | Click Install, wait for it to finish, then run the command again. |
| (being tested) A Mac warning says the `gh` installer can't be opened (Intel Mac) | Expected: GitHub doesn't sign it. Do step 3 "On an Intel Mac", part c (**Open Anyway** in **Privacy & Security**). Only for this file from GitHub's release page. |
| (being tested) `CONFLICT` or `Automatic merge failed` | Ask Claude Code to explain the conflict and show both versions before changing anything. Don't reset. If you're unsure, stop and ask in office hours. |
| Claude Code wants to run `git reset --hard` or `git push --force` | Choose **No**. Ask it to undo with `git revert` instead (step 8). |
| You merged on GitHub but `goals.md` isn't on your laptop | You haven't pulled. Ask Claude Code: "Switch to main and pull the latest changes from GitHub." |
| Typing your password shows nothing | That's normal in the terminal. Type it carefully and press Enter. |
