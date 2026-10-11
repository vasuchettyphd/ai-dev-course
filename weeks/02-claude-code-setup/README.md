# Week 2: Setting up Claude Code

**Goal:** install Claude Code on your own laptop, run your first session, approve (or refuse) its requests with confidence, and give it a CLAUDE.md file with your own preferences.

**Time:** about 90 minutes, plus a restart on Windows. **Cost:** a Claude Pro subscription, about $20/month (see step 1).

**Tested with:** Claude Code 2.1.296, 10 October 2026, on Ubuntu Linux (the same system Windows students use inside WSL). The Mac and Windows steps are being tested on real laptops.

## Before you start

You need:

- A laptop with **macOS 13 or later**, or **Windows 10 version 2004 (build 19041) or later**, or **Windows 11**. To check: on a Mac, Apple menu > About This Mac; on Windows, press `Win + R`, type `winver` and press Enter.
- At least **4 GB of memory (RAM)** and an internet connection.
- About 90 minutes where you can restart your laptop (Windows).

Nothing from week 1 is needed. This is your first time in a terminal, and that's fine: every command is below, exactly as you type it, with what you should see.

### What Claude Code is

In week 1 you used AI in a web page. Claude Code is different in one important way: it works with **files in a folder on your computer**. You ask it, in plain English, to create, read or change files, and it does the work there. Before it acts, it can stop and ask you: "May I do this?". You decide.

That's the difference from the claude.ai chat website. The chat can only talk to you; Claude Code can actually change things on your laptop. That's what makes it useful for the rest of the course, and why this week spends time on saying yes and no.

Claude Code needs a paid Claude plan. **The free claude.ai plan does not include Claude Code.**

### The terminal in 2 minutes

A **terminal** is a window where you type commands instead of clicking. You type a line, press **Enter**, and the computer answers with text.

- **Open it on a Mac:** press `Cmd + Space` to open Spotlight, type `Terminal`, press Enter.
- **Open it on Windows:** you'll use the **Ubuntu** window, which you install in step 3.
- **Paste a command:** `Cmd + V` on a Mac. In the Ubuntu window, `Ctrl + Shift + V` or a right-click.
- **You can't click around** in the terminal. Use the arrow keys.

Three things you'll type this week:

| You type | It means |
|---|---|
| `~` | Your **home folder**, the folder that belongs to you. |
| `cd ~` | "Change directory": go into a folder, here your home folder. |
| `mkdir my-first-project` | "Make directory": create a new, empty folder called `my-first-project`. |

**Where to type matters.** Each command below says where it goes: **in Terminal** (Mac), **in PowerShell** (Windows, only for setting up WSL) or **in the Ubuntu window** (Windows, everything else).

## Steps

### 1. Get Claude Pro

Go to <https://claude.com/pricing> and subscribe to **Pro** with your own account. The course's main page lists it at about $20/month.

What it covers: Pro includes Claude Code, so you don't pay anything extra for this week or for the building weeks. Your usage has limits that depend on your plan; the pricing page explains them, and step 6 shows you how to check how much you've used.

Remember the email you sign up with. You'll sign in with it in step 4.

### 2. Install on a Mac

> **Being tested:** These steps are being tested on a real Mac laptop. If something looks different, tell your instructor.

Windows students: skip to step 3.

**a. Open Terminal.** Press `Cmd + Space`, type `Terminal`, press Enter. A window with a blinking cursor appears.

**b. Install.** In Terminal, paste this line and press Enter:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Leave the window open and wait; it can take a minute or two. When it finishes, look for this line:

```text
✔ Claude Code successfully installed!
```

Above or below it you may also see a "Setup notes" warning that `~/.local/bin` is not in your PATH. If you do, that's fine for now; step c deals with it. (In our test the installer printed its messages twice. That's harmless.)

If a window pops up asking to install Apple's "command line developer tools", click Install, wait for it to finish, then run the install line again.

**c. Check it worked.** Close Terminal completely (`Cmd + Q`), open it again, then in Terminal type:

```bash
claude --version
```

You should see a version number followed by `(Claude Code)`. In our test it was:

```text
2.1.296 (Claude Code)
```

Your number will probably be higher, because Claude Code updates itself. Any number is fine.

If instead you see `zsh: command not found: claude`, run these two lines in Terminal, then try `claude --version` again:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Mac students: go to step 4.

### 3. Install on Windows (with WSL)

> **Being tested:** These steps are being tested on a real Windows laptop. If something looks different, tell your instructor.

On Windows you'll run Claude Code inside **WSL**, the Windows Subsystem for Linux. It's a small Linux computer built into Windows, and it opens as a window called **Ubuntu**. Once it's set up, your steps are the same as a Mac student's.

**a. Open PowerShell as administrator.** Click Start, type `PowerShell`, right-click **Windows PowerShell** and choose **Run as administrator**. Click Yes if Windows asks for permission. The line where you type starts with `PS C:\`; that `PS` tells you you're in PowerShell.

**b. Install WSL.** In PowerShell, type:

```powershell
wsl --install
```

This turns on WSL and installs Ubuntu. It can take several minutes. If you see a help text instead of an install, WSL is already there: skip to step d.

**c. Restart your computer** when it finishes.

**d. Create your Ubuntu user.** After the restart an Ubuntu window opens by itself (if it doesn't, click Start and type `Ubuntu`). Wait while it finishes setting up. Then it asks you to create a **username** and a **password**:

- The username: short, lowercase, no spaces, for example your first name.
- The password: **typing it shows nothing at all**, not even dots. That's normal. Type it and press Enter, then type it again when asked.

Write the password down somewhere safe. Ubuntu asks for it when you install things. This password is only for Ubuntu on your laptop; it's not your Claude or Windows password.

From now on, open Ubuntu from the Start menu (type `Ubuntu`) whenever this course says "the Ubuntu window". Its lines end with a `$` and don't start with `PS`.

**e. Install Claude Code.** In the **Ubuntu window** (not PowerShell), paste this line (`Ctrl + Shift + V` or right-click) and press Enter:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Wait. When it finishes, look for:

```text
✔ Claude Code successfully installed!
```

You may also see a "Setup notes" warning that `~/.local/bin` is not in your PATH; step f deals with it. In our test the messages printed twice, which is harmless.

If you see `curl: command not found` instead, run this in the Ubuntu window, then run the install line again:

```bash
sudo apt update && sudo apt install -y curl
```

`sudo` means "do this as the administrator", so it asks for the Ubuntu password you created in step d. Again, typing shows nothing. Type it and press Enter.

**f. Check it worked.** Close the Ubuntu window, open a new one from the Start menu, then in the Ubuntu window type:

```bash
claude --version
```

You should see a version number followed by `(Claude Code)`. In our test:

```text
2.1.296 (Claude Code)
```

Your number will probably be higher; any number is fine.

If you see `bash: claude: command not found`, run this in the Ubuntu window, then try `claude --version` again:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

If you see `cannot execute binary file: Exec format error`, your Ubuntu is running on the older WSL 1. See the troubleshooting table at the bottom.

**g. See your Ubuntu files in File Explorer.** In the Ubuntu window, type:

```bash
explorer.exe .
```

The dot means "the folder I'm in now". A normal File Explorer window opens on that folder, so you can see and open the files Claude Code creates. You'll use this in step 4.

### 4. Your first session

> **Being tested:** The screens after sign-in are being tested on real Mac and Windows laptops. If something looks different, tell your instructor.

From here on, Mac and Windows are the same. "Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows.

**a. Make a practice folder and start Claude Code.** In your terminal, type these two lines:

```bash
cd ~
mkdir my-first-project && cd my-first-project && claude
```

This goes to your home folder, makes a new folder called `my-first-project`, goes into it and starts Claude Code. Always start Claude Code inside a folder made for the job, so it works there and not across your whole laptop.

**b. Pick a theme.** The first screen says "Welcome to Claude Code" and "Choose the text style that looks best with your terminal". Any choice is fine. Use the arrow keys if you like, then press Enter. (You can change it later with `/theme`.)

**c. Choose how to sign in.** The next screen says "Select login method:". Choose:

```text
1. Claude account with subscription · Pro, Max, Team, or Enterprise
```

It's already highlighted, so press Enter.

**d. Sign in in the browser.** The terminal shows "Opening browser to sign in…" and a browser tab should open. Sign in with your Claude Pro account and approve.

- **The browser didn't open?** (Common on Windows/WSL.) The terminal shows "Browser didn't open? Use the url below to sign in (c to copy)". Press `c` to copy the link, paste it into your browser's address bar and sign in there.
- **The browser shows a code instead of finishing?** Copy the code, go back to your terminal, paste it at `Paste code here if prompted >` and press Enter.

When it works, the terminal shows `Login successful`. Press Enter. You only need to sign in once on this laptop.

**e. Trust the folder.** Claude Code may ask whether you trust the files in this folder. It's your own new, empty practice folder, so say yes. (For a folder someone else gave you, think first.)

**f. Look at the bottom of the screen.** You now see the Claude Code prompt, where you type. At the bottom, a short line shows the **permission mode**, for example `auto mode on`. Read what yours says; don't assume. Recent versions often start in **auto** mode, which asks you fewer questions.

**g. Switch to manual mode.** For this exercise you want Claude Code to ask before every change. Press `Shift + Tab` and watch the bottom line change. Keep pressing until it says `manual mode on`. The order is:

```text
auto mode on  ->  manual mode on  ->  accept edits on  ->  plan mode on  ->  back to auto
```

(If your session started in manual mode, you're already there. If auto mode isn't available to you, the cycle simply skips it.)

**h. Ask for something.** Type this and press Enter:

```text
Create a file called hello.md with three tips for staying organised, then explain what you did
```

**i. Meet a permission prompt.** Before creating the file, Claude Code stops and asks you to approve. You'll see what it wants to do, then a question with choices like these:

| Choice | What it means |
|---|---|
| **Yes** | Do this one thing. It will ask again next time. |
| **Yes, and don't ask again for ...** | Do this, and stop asking about this kind of action. For file edits this lasts until you end the session; for some commands it is saved for this folder. |
| **No** | Don't do it. Claude Code stops and you can tell it what to do differently. |

A fourth choice, "Yes, and switch to auto mode", may also appear.

Use the arrow keys to pick **Yes** and press Enter. Note what the prompt showed you; the assignment asks about it. Claude Code creates `hello.md` and explains what it did.

**When to say No:** say No whenever you don't understand what it wants to do, when it wants to delete or change files you didn't ask about, when it wants to work outside your project folder, or when anything involves passwords, keys or money. You can always say No and ask "What would that do?" first.

**j. See the file.** Open a second terminal window (on a Mac, `Cmd + N` in Terminal; on Windows, open Ubuntu again from the Start menu) and type `cd ~/my-first-project`. Then type `open .` on a Mac (a Finder window opens) or `explorer.exe .` on Windows (a File Explorer window opens). Double-click `hello.md` to read it.

#### The permission modes

| Bottom line shows | Mode | What Claude Code does without asking |
|---|---|---|
| `manual mode on` | Manual | Only reads files. Asks before every change or command. |
| `accept edits on` | Accept edits | Reads, edits files and runs simple file commands (like making folders). Asks for the rest. |
| `plan mode on` | Plan | Only reads and plans. It won't change anything until you approve its plan. |
| `auto mode on` | Auto | Most things, with automatic safety checks in the background. Asks least often. |

Press `Shift + Tab` at any time to switch. While you're learning, **manual** is the safest choice: you see every change before it happens.

### 5. CLAUDE.md: your standing instructions

Every Claude Code session starts fresh: it doesn't remember your last conversation. **CLAUDE.md** is a plain text file where you write instructions that it reads at the start of every session in that folder. Think of it as a note you leave for a new assistant each morning.

Where it lives:

- `CLAUDE.md` in your project folder (here, `~/my-first-project/CLAUDE.md`): instructions for this project.
- `~/.claude/CLAUDE.md`: personal preferences for all your projects. You don't need this one yet.

**a. Create it with `/init`.** In your Claude Code session, type:

```text
/init
```

Claude Code looks at what's in the folder and creates a starting `CLAUDE.md`. It may ask permission to create the file; read the prompt and say Yes.

**b. Add three personal preferences.** Type this (change the three preferences to your own if you like) and press Enter:

```text
Add a section called "My preferences" to CLAUDE.md with these three rules: Explain things in plain English. Ask before deleting files. Keep answers short.
```

Approve the edit when asked. Good preferences are specific and about how you want to work. Other ideas: "Use US spelling", "Give me one step at a time", "Tell me what a command does before you run it".

**c. Leave and start again.** Type `/exit` to leave Claude Code. Then, in your terminal, start a new session in the same folder:

```bash
claude
```

**d. See the effect.** Ask:

```text
Explain what a CSV file is
```

The answer should follow your preferences: plain English and short. You can also ask "What preferences do you have for working with me?" and it should list your three. Leave with `/exit`.

### 6. Cost and safety

**Cost.** Claude Pro covers Claude Code. To see how much of your plan you've used, type this inside a Claude Code session:

```text
/usage
```

It shows your plan's usage bars. Limits depend on your plan; see <https://claude.com/pricing>. If you hit a limit, Claude Code tells you. Starting a fresh conversation with `/clear` between unrelated tasks helps your usage go further.

**Safety.** Claude Code can change real files on your laptop, so:

- **Never paste passwords, API keys or other people's private data** into Claude Code, or into any AI tool. If a task seems to need one, stop and ask your instructor.
- **Read every permission prompt before saying yes.** If you're not sure, choose No and ask what it would do.
- **Work in a project folder**, not your whole home folder or Desktop.
- **To leave**, type `/exit` (or press `Ctrl + D` twice). To stop Claude Code in the middle of something, press `Esc`.

## Check it worked

You're done when:

- `claude --version` in your terminal prints a version number followed by `(Claude Code)`.
- Typing `claude` in `~/my-first-project` starts a session, signed in with your Pro account.
- `~/my-first-project/CLAUDE.md` exists and has your three preferences.

The [assignment](assignment.md) asks for screenshots of the first two and the text of the third. Next week, [Git and GitHub](../03-git-and-github/), you'll learn to save versions of your work so you can always undo a change.

## Troubleshooting

| What you see | What to do |
|---|---|
| `zsh: command not found: claude` (Mac) or `bash: claude: command not found` (Ubuntu) after installing | Close the terminal and open a new one, then try again. Still there? Mac: run `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc` then `source ~/.zshrc`. Ubuntu: run `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc`. Then `claude --version` again. |
| An error after pasting `curl -fsSL https://claude.ai/install.sh \| bash` on Windows, and the line starts with `PS C:\` | You're in PowerShell, not Ubuntu. Close it, open **Ubuntu** from the Start menu, and paste the line there. PowerShell is only for `wsl --install` and the WSL fixes below. |
| `wsl --install` fails, or mentions virtualization | Virtualization is turned off in your laptop's settings (BIOS or UEFI). See Microsoft's guide at <https://learn.microsoft.com/en-us/windows/wsl/troubleshooting> and come to office hours; we'll do it together. |
| `cannot execute binary file: Exec format error` when you run `claude` in Ubuntu | You're on WSL 1. In **PowerShell**, run `wsl -l -v` to see your Ubuntu's name (for example `Ubuntu`) and its VERSION. Then run `wsl --set-version Ubuntu 2`, using the name you saw. Open a new Ubuntu window and try `claude` again. |
| `curl: command not found` in Ubuntu | In the Ubuntu window run `sudo apt update && sudo apt install -y curl`, type your Ubuntu password (it shows nothing), then run the install line again. |
| The browser doesn't open when you sign in (WSL) | Press `c` in the terminal to copy the sign-in link, paste it into your browser, and sign in there. |
| You signed in, but the terminal never says `Login successful` | The browser should show a code. Copy it and paste it at `Paste code here if prompted >` in the terminal, then press Enter. If pasting does nothing, try right-click to paste. |
| A message about your plan, or the sign-in won't accept your account | Claude Code needs a paid plan; the free plan has no Claude Code. Subscribe to Pro at <https://claude.com/pricing>, then type `/login` in Claude Code to sign in again. |
| A Mac window asks to install "command line developer tools" | Click Install and wait for it to finish, then run the install line again. |
| Typing your password shows nothing | That's normal in the terminal. Type it carefully and press Enter. |
| You never see a permission prompt | You're probably in auto or accept edits mode. Look at the bottom line and press `Shift + Tab` until it says `manual mode on`, then ask again. |
