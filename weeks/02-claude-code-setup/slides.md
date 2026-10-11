---
marp: true
paginate: true
title: Week 2 - Setting up Claude Code
style: |
  section { font-size: 28px; }
  table { font-size: 22px; }
  pre { font-size: 20px; }
  .small { font-size: 20px; color: #555; }
---

# Week 2: Setting up Claude Code

AI Development Course

<p class="small">Install and first screens tested with Claude Code 2.1.296 on Ubuntu Linux (in a container), 10 October 2026, up to the sign-in screen. Everything after sign-in follows Anthropic's docs and is being tested on real Mac and Windows laptops.</p>

---

## Today

- What Claude Code is, and what it costs
- Installing it: Mac, and Windows with WSL
- Live demo: install, first session, a permission prompt
- Permission modes: how much it asks you
- CLAUDE.md: standing instructions
- Staying safe
- The assignment, and next week

---

## What Claude Code is

**claude.ai chat:** talks to you in a web page.

**Claude Code:** works with **files in a folder on your computer**.

- You ask in plain English: "Create a file with three tips"
- It reads, creates and changes files in that folder
- It can stop and ask first: **"May I do this?"** You decide.

---

## What it costs

- Claude Code needs a paid plan. **The free plan has no Claude Code.**
- **Claude Pro**, about $20/month, includes Claude Code
- Usage limits depend on your plan: <https://claude.com/pricing>
- Check what you've used: type `/usage` in Claude Code

---

## The terminal in 2 minutes

A window where you **type** commands and press **Enter**.

| You type | It means |
|---|---|
| `~` | your home folder |
| `cd ~` | go into a folder (here, home) |
| `mkdir my-first-project` | make a new folder |

Paste: `Cmd + V` on a Mac; `Ctrl + Shift + V` or right-click in Ubuntu.

---

## Two install paths

| Mac | Windows |
|---|---|
| Open **Terminal** (`Cmd + Space`, "Terminal") | **PowerShell** as administrator: `wsl --install` |
| | Restart, create Ubuntu username + password |
| In Terminal: the install line | In the **Ubuntu** window: the same install line |

After that, every step is the same.

<p class="small">Needs macOS 13+, or Windows 10 version 2004 (build 19041)+ or Windows 11, and 4 GB RAM.</p>

---

## Where you type matters

| Window | How you can tell | Used for |
|---|---|---|
| Terminal (Mac) | opened from Spotlight | everything |
| PowerShell | line starts with `PS C:\` | only `wsl --install` and WSL fixes |
| Ubuntu | not `PS`; line ends with `$` | everything else on Windows |

The install line belongs in **Ubuntu**, not PowerShell.

---

## Live demo: install

In Terminal (Mac) or the Ubuntu window (Windows):

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Look for: `✔ Claude Code successfully installed!`

Open a **new** terminal, then:

```bash
claude --version
```

```text
2.1.296 (Claude Code)
```

<p class="small">Your number will be higher. "command not found"? See the PATH fix in the README.</p>

---

## Windows tips

- Typing a password shows **nothing**. That's normal.
- See your Ubuntu files in File Explorer:

```bash
explorer.exe .
```

- `Exec format error`? You're on WSL 1. In PowerShell:

```powershell
wsl -l -v
wsl --set-version Ubuntu 2
```

<p class="small">Use the name you saw in <code>wsl -l -v</code> instead of Ubuntu if it differs.</p>

---

## Live demo: first session

```bash
cd ~
mkdir my-first-project && cd my-first-project && claude
```

1. Pick a theme (any), press Enter
2. "Select login method": **1. Claude account with subscription**
3. Sign in in the browser
4. `Login successful`, press Enter

---

## Signing in on WSL

The browser didn't open?

- Press **`c`** to copy the sign-in link, paste it into your browser

The browser shows a code?

- Paste it at **`Paste code here if prompted >`**, press Enter

You only sign in once per laptop.

---

## Read the bottom line

The bottom of the screen shows the **permission mode**.

Recent versions often start in **auto**: fewer questions.

For today: press **`Shift + Tab`** until it says `manual mode on`.

```text
auto -> manual -> accept edits -> plan -> auto
```

---

## Live demo: a permission prompt

```text
Create a file called hello.md with three tips for
staying organised, then explain what you did
```

| Choice | Means |
|---|---|
| **Yes** | do this once, ask next time |
| **Yes, and don't ask again for ...** | stop asking about this kind of action |
| **No** | don't; tell it what to do instead |

---

## When to say No

- You don't understand what it wants to do
- It wants to delete or change files you didn't mention
- It wants to work outside your project folder
- Anything with passwords, keys or money

You can always say No, then ask **"What would that do?"**

---

## Permission modes

| Bottom line | Without asking, it... |
|---|---|
| `manual mode on` | only reads. Asks before every change and most commands. |
| `accept edits on` | reads and edits files, and creates, moves or deletes files in this folder. Asks for the rest. |
| `plan mode on` | only reads and plans, changes nothing |
| `auto mode on` | does most things, with safety checks |

While learning: **manual**. You see every change first.

---

## CLAUDE.md: standing instructions

Each session starts fresh. CLAUDE.md is a note it reads **every time**.

1. Type `/init` to create one
2. Add three preferences:
   - Explain things in plain English
   - Ask before deleting files
   - Keep answers short
3. `/exit`, start `claude` again, see the difference

---

## Safety

- **Never paste** passwords, API keys or other people's private data
- **Read every prompt** before saying yes
- Work in a **project folder**, not your whole laptop
- `Esc` stops it. `/exit` leaves.

---

## Assignment

One document with:

- Screenshot: `claude --version`
- Screenshot: a permission prompt in your first session
- Your CLAUDE.md with three preferences
- One paragraph: which prompt, what you chose, and why

| Criterion | Points |
|---|---|
| Installed and running, both screenshots | 4 |
| CLAUDE.md with three meaningful preferences | 3 |
| Permission paragraph shows understanding | 3 |

---

## Next week: Git and GitHub

Claude Code changes real files.

Next week you learn to **save versions** of your work, so you can always undo a change.
