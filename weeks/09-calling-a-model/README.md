# Week 9: Calling a model from code

**Goal:** make your own program call an AI model. You'll get an API key and keep it safe, make a first call and work out what it cost, learn the settings that make a model's answers dependable, and add one AI feature to your project that still works when there's no key, merged through a pull request.

**Time:** about 30 minutes before class to set up your account and key (step 2), then plan for about 2 to 3 hours of your own time (an estimate) for the rest. **Cost:** API credit, separate from Claude Pro. The syllabus budgets about $5 for weeks 9 to 11; this week's calls cost a fraction of a cent each (step 1 shows how to work it out). Set a spend limit before your first call (step 2c).

**Tested with** (12 October 2026; these are the versions tested, yours may be newer):

- The official Python package `anthropic` 1.13.0 (released 9 October 2026; it needs Python 3.10 or newer), installed in a virtual environment with Python 3.12.3 on Ubuntu 24.04 Linux (in a container).
- The model `claude-haiku-5-5` (Claude Haiku 5.5), at $0.10 per million input tokens and $0.50 per million output tokens (<https://platform.claude.com/docs/en/about-claude/pricing>, read 12 October 2026). Model names and prices change: check that page on the day you start.
- The deal screener example's new "paste the listing" step and its 90 offline tests, with Python 3.14.4 and, in a container, Python 3.12.
- **Being tested:** every real call to the model. No call had been made when this page was written, so the replies, token counts and costs you'll see below are marked "being tested" (the cost arithmetic itself is exact). Also being tested: every step in the Claude Console, everything inside a signed-in Claude Code session, everything on GitHub, and every step on a Mac or in Windows (WSL).

## Before you start

You need:

- Weeks 5 to 8 done: version 1 of your project merged into `main` of your **private** `semester-project` repo, with `vasuchettyphd` as a collaborator, your tests passing, and your week 7 `Dockerfile` merged.
- Superpowers (week 5), your week 6 reviewers in `.claude/agents/`, and Docker Desktop (week 7).
- Python 3.10 or newer for step 3 (step 3a shows how to check). On a Mac, Apple's own Python is often 3.9, which is too old for the `anthropic` package.
- A way to pay for API credit (step 2b). If you can't, tell your instructor **before** class.
- `gh` signed in to **your** GitHub account, and Claude Code signed in with your Claude Pro account.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows, as in weeks 2 to 8. Every command below says where to type it: **in your terminal**, **in Claude Code**, or **in a text editor**. On Windows, nothing this week goes in PowerShell.

### How you'll work this week

As in weeks 5 to 8, you ask Claude Code in plain English, and this README shows **the prompt**, **what Claude Code will probably do**, and **what to check**. The git rules still apply: make the branch first (step 5a), never change `main`, plain **Yes** for git commands, and finish with a pull request.

This week adds **the key rules**. Read them now; every step depends on them.

> **The key rules**
>
> 1. **You** put your key in a file called `.env`, with a text editor (step 2d). Never paste a key into Claude Code, a chat, an email, a screenshot, a commit or a pull request.
> 2. Before your first commit in a folder that has a `.env`, check git ignores it: `git check-ignore .env` must print `.env`.
> 3. Your program reads the key from the environment and never prints it, not even in an error message.
> 4. Docker gets the key when the container starts (`--env-file .env`). The key never goes into the image.
> 5. Set a monthly **spend limit** before your first call (step 2c).
> 6. If a key leaks, **delete it in the Console first** (step 2f), then clean up.

What to answer this week:

| Claude asks to | Choose |
|---|---|
| Create or edit your project's code and tests on your `ai-feature` branch | **Yes** |
| Create `.env.example` (a sample file with a fake key in it) | **Yes** |
| Read `.env`, print it, `cat .env`, or put your key in any file | **No**. Type: "Never read or print .env. Read the key from the environment." |
| Write the key, or anything starting `sk-ant-`, into your code | **No** |
| A test that calls the real API every time the tests run | **No**. Type: "Tests must use a fake model. Make the live test run only when I ask for it." |
| `pip install` inside your project's `.venv`, or `npm install` for a Node.js project | **Yes**, after you check the package name is the official one (step 5) |
| Run your tests, or `git status`, `git log`, `git diff` | **Yes** |
| `git add`, `git commit`, `git push` on your `ai-feature` branch, `gh pr create` | plain **Yes**, after `git status` shows no `.env` |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

## Steps

### 1. What changes this week

Until now, Claude Code wrote code for you. This week **your own program** sends text to a model and gets an answer back. That's an **API call** (API: a way for one program to ask another for something), and it's paid for separately. Anthropic says so in plain words: "A paid Claude subscription enhances your chat experience, and the Claude API is billed separately." (<https://support.claude.com/en/articles/9876003>). So Claude Pro pays for Claude Code; the calls your program makes are paid from **API credit** that you buy in the **Claude Console**, Anthropic's site for developers.

You pay per **token**. A token is a piece of text, often part of a word. Every call has:

- **input tokens**: everything you send (your instructions and the text);
- **output tokens**: everything the model writes back.

Prices are per **million** tokens (MTok), and output costs more than input. For `claude-haiku-5-5`, the model this week uses: **$0.10 per million input tokens and $0.50 per million output tokens**.

**A worked example** (example numbers, to show the arithmetic): a call that used 500 input tokens and 200 output tokens costs

```text
500 x $0.10 / 1,000,000  =  $0.00005
200 x $0.50 / 1,000,000  =  $0.00010
total                    =  $0.00015
```

That's fifteen thousandths of a cent. Calls are cheap; mistakes like a loop that calls the model thousands of times are not. That's why you set a spend limit.

Every reply tells you exactly how many tokens it used, so you never have to guess (step 3d).

### 2. Get a key safely (before class)

> **Being tested:** the Console steps below follow Anthropic's pages, read on 12 October 2026. The Console's buttons may look a little different.

**a. Make a Console account.** Go to <https://platform.claude.com> and sign in, or create an account if you don't have one yet. This is a different account from your Claude Pro subscription, even if you use the same email. Anthropic's steps then ask you to fill in some information about your organization and use case: a student project is fine.

**b. Buy a small amount of credit.** Anthropic's steps: "Navigate to Settings > Billing", click **Buy credits**, then "Enter the amount of credits you want to purchase and confirm." Buy the smallest amount the Console offers (it shows the minimum when you click **Buy credits**); the syllabus budgets about $5 for weeks 9 to 11. Leave **auto-reload** off: it "purchases additional credits automatically when your balance falls below a threshold you set". When your credit runs out, your calls simply stop working until you add more.

**c. Set a monthly spend limit.** Still in **Settings > Billing** (<https://platform.claude.com/settings/billing>), in **Spend limits**, click **Set limit** (or **Adjust limit**) and enter a small number, such as your credit amount. If your program ever reaches it, Anthropic refuses further calls until the limit resets or you raise it.

**d. Create a key and save it in `.env`.**

1. In the Console, open **Settings > API keys** (<https://platform.claude.com/settings/keys>) and click **Create key**. Name it `semester-project`, and choose an expiration such as **30 days** (Anthropic: "Expiration limits the lifetime of a leaked credential"). Set **Linked account** to yourself.
2. The Console "shows the full key, which starts with `sk-ant-`, only once". Click its copy button. Don't paste it anywhere except step 4 below.
3. In your terminal, make a scratch folder for step 3 and open a new `.env` file in a text editor:

   - **Mac:** `mkdir -p ~/first-call && cd ~/first-call && touch .env && open -e .env` opens it in TextEdit. If TextEdit shows a formatting bar, choose **Format > Make Plain Text** first.
   - **Windows (Ubuntu window):** `mkdir -p ~/first-call && cd ~/first-call && nano .env` opens the `nano` editor in the window.

4. Type this one line, and paste your key after the `=`, with **no spaces and no quote marks**:

   ```text
   ANTHROPIC_API_KEY=sk-ant-...your key...
   ```

   Save and close: in TextEdit, **File > Save** then quit; in `nano`, press `Ctrl+O`, `Enter`, then `Ctrl+X`. (No quote marks, because Docker's `--env-file` in step 6 would keep them as part of the key, and Anthropic would then reject it.)
5. Check the file has exactly one line, without showing the key: in your terminal, in `~/first-call`, `wc -l .env` should print `1 .env`. Don't `cat` the file in class: anyone behind you can read your screen.

The key is like a password to your credit. If you lose it, you can't see it again: delete it and create a new one.

**e. Check git would ignore it.** `~/first-call` isn't a git folder, so there's nothing to check yet. You'll do this in your project in step 5b, before any commit.

**f. If a key leaks.** Pasted it into a chat, showed it on screen, committed it, or pushed it? **First**, in the Console, **Settings > API keys**, find the key and **Delete** it (Anthropic: "disable or delete any key you suspect has leaked"; **Disable** can be undone, **Delete** can't, and a leaked key should never come back). Then create a new key and put it in `.env`. Only then clean up the place it leaked: tell your instructor if it was committed or pushed, so you can fix the history together. Deleting the old key first matters more than cleaning up, because a pushed key can be copied within minutes.
