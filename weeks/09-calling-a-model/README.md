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

### 3. Your first call

You'll do this in the scratch folder `~/first-call` from step 2d, not in your project, so nothing here can end up in a commit.

**a. Check your Python.** In your terminal, type `python3 --version`. The `anthropic` package needs **Python 3.10 or newer**.

- **Mac:** if it prints `Python 3.9` (Apple's own Python, from week 3) or lower, install a newer one from python.org exactly as in [week 5 step 3c](../05-building-with-ai/README.md#3-pick-your-tools), then close and reopen Terminal and check again (being tested). On an Apple chip Mac, `brew install python` works too.
- **Windows (Ubuntu window):** Ubuntu 24.04 comes with Python 3.12, which is fine.

**b. Make a virtual environment and install the package.** A **virtual environment** (a `.venv` folder) is a private box of Python packages for one folder, so installing a package can't break anything else on your laptop. In your terminal:

```bash
cd ~/first-call
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic==1.13.0
```

The `source` line **activates** the environment: your prompt now starts with `(.venv)`. You need to activate it again in every new terminal window (`cd ~/first-call` then `source .venv/bin/activate`). The `==1.13.0` pins the version the course tested.

The last line should end with `Successfully installed ... anthropic-1.13.0 ...` (seen in the course's test). Check:

```bash
python -c "import anthropic; print(anthropic.__version__)"
```

It prints `1.13.0`.

**On Windows (Ubuntu), if `python3 -m venv .venv` fails** with a message starting "The virtual environment was not created successfully because ensurepip is not available", Ubuntu is missing one package. The failed attempt also leaves a broken `.venv` folder behind. In the Ubuntu window:

```bash
sudo apt update
sudo apt install python3-venv
rm -r .venv
```

`sudo` asks for your Ubuntu password (nothing shows as you type). The `rm -r .venv` deletes **only** the broken `.venv` folder you just made, in `~/first-call`: type it exactly, with nothing added. Then run the four lines above again.

**c. Write the first program.** In your terminal, in `~/first-call`, paste this whole block and press Enter. It creates a file called `first_call.py` (the lines between `<<'EOF'` and `EOF` go into the file):

```bash
cat > first_call.py <<'EOF'
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "In one sentence, what is a cap rate in real estate?"}
    ],
)

for block in message.content:
    if block.type == "text":
        print(block.text)

print()
print("Stopped because:", message.stop_reason)
print("Input tokens:", message.usage.input_tokens)
print("Output tokens:", message.usage.output_tokens)
cost = (message.usage.input_tokens * 0.10 + message.usage.output_tokens * 0.50) / 1_000_000
print(f"Cost: about ${cost:.6f}")
EOF
```

It's Anthropic's own first example (<https://platform.claude.com/docs/en/get-started>) with three changes: the cheaper `claude-haiku-5-5` model, a real-estate question, and the lines at the end that show the tokens and the cost. Notice what the program does **not** contain: your key. The package reads it from the environment, from a variable called `ANTHROPIC_API_KEY` (Anthropic: "The client SDK reads `ANTHROPIC_API_KEY` automatically").

Why the `for block in message.content` loop? A reply is a list of **blocks**. Haiku 5.5 sometimes "thinks" first, and its thinking comes back as a block of its own before the answer, so the program picks out the `text` blocks instead of assuming the first block is the answer. Anthropic: "Select content blocks by their `type` field rather than by position."

**d. Run it.** In your terminal, in `~/first-call`, with `(.venv)` showing:

```bash
set -a; . ./.env; set +a
python first_call.py
```

The first line loads the key from `.env` into this terminal window, without showing it. It lasts until you close the window; in a new window, run it again. You should see a one-sentence answer, then lines like these (being tested; your numbers will differ):

```text
Stopped because: end_turn
Input tokens: ...
Output tokens: ...
Cost: about $0.000...
```

`end_turn` means the model finished its answer. Check the cost by hand with step 1's arithmetic, and check it against the Console's **Usage** page (<https://platform.claude.com/usage>) later: the Console may take a while to update.

If you see `TypeError: "Could not resolve authentication method...`, the key isn't loaded: run the `set -a` line again, in `~/first-call`. Other errors: see Troubleshooting.

### 4. The settings that matter

Each change below is a small edit to `first_call.py`. Make it in a text editor (`open -e first_call.py` on a Mac, `nano first_call.py` in Ubuntu), or paste a new version with `cat > first_call.py <<'EOF'` as above.

**a. The same question, three times.** Run the program three times in a row:

```bash
for i in 1 2 3; do python first_call.py; done
```

Compare the three answers. They'll probably be worded differently (being tested): a model picks its words with some randomness. Older models let you turn that randomness down with a setting called **temperature**. The current models don't: on Haiku 5.5, "If a request includes `temperature`, it must be `1`", and Sonnet 5.5 and Opus 5.5 also reject any other value (<https://platform.claude.com/docs/en/about-claude/models/migration-guide>). The Python package doesn't even accept it: adding `temperature=0` gives `TypeError: ... got an unexpected keyword argument 'temperature'` before anything is sent. And Anthropic notes that "`temperature = 0` ... never guaranteed identical outputs" even on older models. So you can't make a model give the same words every time. Instead, you make its answers **dependable** with the four settings below, and you **check** the answer in your code.

**b. A system prompt.** The `system` setting holds instructions that apply to the whole conversation (Anthropic: "Use the top-level `system` field for instructions that apply from the start"). Add this line just below `max_tokens=1000,`:

```python
    system="You explain real estate terms to beginners. Answer in one short sentence, with no jargon.",
```

Run it a few times. The answers keep their wording differences, but they all follow the rules. A specific prompt (exactly what to do, how long, in what form) is your strongest control.

**c. `max_tokens`.** This caps how many output tokens the model may write, so it caps the cost of one call. Change `max_tokens=1000` to `max_tokens=20` and run it. The answer is probably cut off, and `Stopped because:` shows `max_tokens` (being tested). Thinking counts toward this cap too ("Thinking tokens count toward `max_tokens`"), so a very small number can stop the model before it writes any text at all. Your program must check `stop_reason` and not trust a cut-off answer. Put it back to `1000`.

**d. Structured output: answers your program can read.** A sentence is fine for a person, but a program needs the answer in a fixed shape. **Structured output** makes the model answer in JSON (a standard text format for data, like `{"price": 150000}`) that follows a **schema**: a description of exactly which fields you want. Paste this into your terminal, in `~/first-call`, to create `structured.py`:

```bash
cat > structured.py <<'EOF'
import json
import anthropic

client = anthropic.Anthropic()

schema = {
    "type": "object",
    "properties": {
        "price": {"type": ["number", "null"], "description": "Asking price in dollars"},
        "bedrooms": {"type": ["number", "null"], "description": "Number of bedrooms"},
    },
    "required": ["price", "bedrooms"],
    "additionalProperties": False,
}

message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1000,
    system="Pull numbers out of real estate listings. Use null for any number the listing does not state.",
    messages=[{"role": "user", "content": "Cozy 3 bed, 2 bath bungalow, now $189,000."}],
    output_config={"format": {"type": "json_schema", "schema": schema}},
)

if message.stop_reason != "end_turn":
    print("No usable answer. Stopped because:", message.stop_reason)
else:
    text = next(block.text for block in message.content if block.type == "text")
    answer = json.loads(text)
    print(answer)
    print("Input tokens:", message.usage.input_tokens, "Output tokens:", message.usage.output_tokens)
EOF
python structured.py
```

You should see something like `{'price': 189000, 'bedrooms': 3}` (being tested). The `output_config` part is Anthropic's **structured outputs** feature (<https://platform.claude.com/docs/en/build-with-claude/structured-outputs>). `null` lets the model say "the listing doesn't say" instead of guessing. Structured output fixes the **shape** of the answer, not whether it's **right**: a model can still misread a number, so your program checks the values, and a person confirms anything that matters.

**e. Choosing a model.** Anthropic's three current families (<https://platform.claude.com/docs/en/about-claude/models/overview>, prices from <https://platform.claude.com/docs/en/about-claude/pricing>, both read 12 October 2026):

| Model | ID to use in code | Price per million tokens (input / output) | Speed | Good for |
|---|---|---|---|---|
| Claude Haiku 5.5 | `claude-haiku-5-5` | $0.10 / $0.50 | fastest | high-volume tasks "such as classification, extraction, and routing" |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | $2 / $10 | fast | harder writing and reasoning |
| Claude Opus 5.5 | `claude-opus-5-5` | $4 / $20 | moderate | the hardest tasks; Anthropic's default suggestion |

Anthropic's own advice for keeping costs down: "1. Begin implementation with Claude Haiku 5.5. 2. Test your use case thoroughly. 3. Evaluate if performance meets your requirements. 4. Upgrade only if necessary for specific capability gaps." (<https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>). That's what this course does. To try another model, change only the `model=` line; the same call costs 20 times more on Sonnet 5.5 and 40 times more on Opus 5.5.

You may hear of **fine-tuning**: training a model further on your own examples. This course doesn't cover it, and projects like yours don't need it: a clear prompt, structured output and checks in your code go a long way.

### 5. Add one AI feature to your project

> **Being tested:** this step needs a signed-in session and is being tested. The deal screener's version of it was built and tested offline on 12 October 2026 (see "The deal screener's version" below).

**a. Make the branch first.** In your terminal, `cd ~/semester-project`, then start `claude`. In Claude Code:

```text
Switch to main, pull the latest changes from GitHub, then create a new branch called ai-feature and switch to it.
```

Plain **Yes** to each git command. Check: ask "What branch am I on?". It should say `ai-feature`.

**b. Check git ignores `.env`, then copy your key in.** In a second terminal window:

```bash
cd ~/semester-project
git check-ignore .env
```

It should print `.env`. If it prints nothing, **stop**: in Claude Code, type "Add .env and .venv to .gitignore and commit only .gitignore on this branch.", plain **Yes**, and run `git check-ignore .env` again until it prints `.env`. Only then copy the key file from step 2, without opening it:

```bash
cp ~/first-call/.env ~/semester-project/.env
git status
```

`git status` must **not** list `.env`. (If it does, don't commit anything: ask your instructor.)

**c. Pick one small feature.** One call to the model, one clear job, and the program still works without it. Ideas for business projects:

- **Pull fields out of pasted text**: an invoice, an email, a job ad or a listing becomes the numbers or fields your program already uses (the deal screener does this).
- **Sort something into categories**: customer comments into "praise / complaint / question", or expenses into your budget's categories.
- **Write a short plain-English summary** of a result your program already works out, such as one sentence explaining a verdict.

Pick the one that fits your project, and keep it to one call.

**d. Plan and build it with Superpowers, with the guardrails in the prompt.** In Claude Code (replace the part in angle brackets):

```text
/superpowers:writing-plans Write an implementation plan to add one AI feature to this project: <one sentence: what the feature does>. Use Anthropic's official package for this project's language, pinned to an exact version, with the model claude-haiku-5-5 and structured output (output_config with a JSON schema) if the answer must be read by the program. Rules: read the key only from the ANTHROPIC_API_KEY environment variable, loaded from .env, and never read, print or log .env or the key; never write a key in any file; the program must still work when there is no key, no internet or the call fails, saying what happened in one plain sentence and carrying on without the feature; check stop_reason and check every value the model returns before using it; print the input tokens, output tokens and cost of each call; tests must use a fake model and never call the real API, plus one live test that runs only when I set RUN_LIVE_TESTS=1; include a test for "no key"; update the Dockerfile so it installs the package; add a .env.example with a fake key and say in the README how to set up .env. I'm not a programmer, so keep each task small.
```

Then build it as in [week 5 step 5](../05-building-with-ai/README.md#5-build-with-subagent-driven-development):

```text
/superpowers:subagent-driven-development Execute the plan docs/superpowers/plans/<your-plan-file>.md.
```

Answer as in the table at the top. Watch especially for:

- **No** to anything that reads or prints `.env`. Type: "Never read or print .env. Read the key from the environment."
- **No** to a key, or anything starting `sk-ant-`, in a file. `.env.example` may only hold a fake one like `put-your-key-here`.
- **No** to a test that calls the real API whenever the tests run.
- For a package install: Python's official package is `anthropic`; for a Node.js project it's `@anthropic-ai/sdk` (Anthropic's other official packages are listed at <https://platform.claude.com/docs/en/cli-sdks-libraries/overview>). Any other name: ask "Is this Anthropic's official package?" before answering Yes.

**e. Try it.** When the build is done, in your terminal, in `~/semester-project`: activate the project's `.venv` if it has one (`source .venv/bin/activate`), load the key with `set -a; . ./.env; set +a`, and run your program the way its README says. Then try it **without** a key: open a new terminal window (the key is only loaded in the old one), `cd ~/semester-project`, and run it again. It must say there's no key and carry on. Take a screenshot of each run for your assignment: check no key is visible in them first.

**f. Run the tests, then the live test once.** In Claude Code: "Run all the tests." They must pass with no key loaded. Then, in your terminal with the key loaded, run the live test once, the way Claude set it up (for a Python project, something like `RUN_LIVE_TESTS=1 python -m unittest`). Write down the tokens and cost each real call printed: you need three for your assignment's cost log.

**The deal screener's version** (being tested live; built and tested offline). It got an optional "paste the listing" step: `python3 -m dealscreener --listing` asks you to paste a listing's text, sends it to `claude-haiku-5-5` with a schema for the five property numbers, then shows each number for you to confirm:

```text
Purchase price ($) [from the listing: 150000]:
```

Press Enter to keep the number, or type the right one. Numbers the listing doesn't state are asked normally, the loan questions are always yours, and the maths is unchanged. With no key, it says `No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README). For now, type the numbers yourself.` and carries on. Its 90 tests never touch the network. See [`example-project/README.md`](../../example-project/README.md) and [`dealscreener/extract.py`](../../example-project/dealscreener/extract.py).

### 6. Review and run

**a. Review it with `safe-and-private`.** As in week 7 step 5, run only that reviewer, on what changed. In Claude Code:

```text
Run the safe-and-private reviewer as a subagent on the files changed on this branch compared with main (git diff main --name-only), and on .gitignore, .dockerignore and the Dockerfile. Focus on: an API key or anything starting sk-ant- in any file; whether .env could be committed or copied into the Docker image; whether the key could ever be printed or logged, including in error messages; whether any test calls the real API by default. Do not read .env itself. Then add a section at the end of REVIEW.md, headed "## Week 9: AI feature review", with one table with the columns #, Label, Finding (file:line), Found by, Decision, Reason, numbering the findings A1, A2 and so on. Leave Decision and Reason empty. Do not change any file except REVIEW.md.
```

**Yes** to editing `REVIEW.md` only. Triage the findings as in week 6 step 5 (every Must fix is `Fix`), fix them, and commit.

**b. Run it in Docker, with the key given at run time.** In your terminal, in `~/semester-project`:

```bash
docker build -t semester-project .
docker run --rm semester-project ls -a
```

The list must **not** include `.env` (your week 7 `.dockerignore` keeps it out). Then run your program with the key:

```bash
docker run -it --rm --env-file .env semester-project
```

`--env-file .env` hands the key to this one container while it runs; it never goes into the image. For the deal screener the command is `docker run -it --rm --env-file .env dealscreener python -m dealscreener --listing` (being tested). Run your tests in the container as in week 7 step 4c, without `--env-file`: they must pass with no key.

### 7. Finish

**a. Push and open a pull request.** In Claude Code:

```text
Push the ai-feature branch to GitHub and open a pull request into main titled "Add one AI feature: <short name>".
```

Plain **Yes** to each, after `git status` shows no `.env`.

**b. Read Files changed yourself.** Open the pull request and click **Files changed**. You should see your code and tests, the package list (`requirements.txt` or `package.json`), the Dockerfile, `.env.example` with a **fake** key, your README and `REVIEW.md`. **No `.env`, and no real key anywhere**: use the browser's Find (`Cmd+F` or `Ctrl+F`) for `sk-ant-` on the page; the only hit allowed is a fake one. If a real key is there, don't merge: go to step 2f now.

**c. Merge on GitHub, then pull,** as in week 8 step 6d. In Claude Code: "Switch back to main and pull the latest changes from GitHub." Check: ask "What branch am I on, and do all the tests pass?" It should say `main`, and yes.

The deal screener's week 9 changes are on this page (it works once week 9 is published): <https://github.com/vasuchettyphd/ai-dev-course/compare/week-08...week-09>.

## Check it worked

- `git check-ignore .env` prints `.env` in `~/semester-project`, and GitHub shows no `.env` and no real key in your pull request.
- Your feature works with the key loaded, and without a key it says so in one sentence and carries on.
- All your tests pass with no key loaded (they use a fake model).
- You have three real calls written down: input tokens, output tokens, and the cost you worked out from them.
- The Console's **Usage** page shows roughly the same spend, and your spend limit is set.

## Troubleshooting

| What you see | What to do |
|---|---|
| `TypeError: "Could not resolve authentication method...` | The key isn't loaded. In the same terminal window, in the folder with `.env`, run `set -a; . ./.env; set +a`, then try again. |
| `No API key found` (the deal screener, or your own program's message) | Same as above: load the key in this window. In Docker, add `--env-file .env`. |
| `ModuleNotFoundError: No module named 'anthropic'` | The `.venv` isn't active: `source .venv/bin/activate` (your prompt shows `(.venv)`), then try again. In a new folder, install it first (step 3b). |
| `python3 -m venv .venv` fails with "ensurepip is not available" (Ubuntu) | Step 3b: `sudo apt install python3-venv`, delete only the broken `.venv` folder with `rm -r .venv`, try again. |
| `pip install anthropic==1.13.0` says no matching version, or it needs Python 3.10 | Your Python is too old: step 3a. |
| `TypeError: ... unexpected keyword argument 'temperature'` | Current models and the package don't take `temperature`: remove that line (step 4a). |
| Error 401, or "The API key was not accepted" | The key is wrong, expired, deleted, or has quote marks or spaces around it. Check `.env` is exactly `ANTHROPIC_API_KEY=sk-ant-...` on one line, or make a new key (step 2d). |
| Error 403 | This key isn't allowed to do that. Make a new key linked to yourself (step 2d). |
| Error 404, or "The model name wasn't found" | Check the model name exactly: `claude-haiku-5-5`. Names change: check the models page. |
| Error 429, or "Too many requests" | You (or your whole class, on one network) sent too many calls too fast, or hit your plan's cap. Wait a minute and try again. If it continues, check the Console's **Rate limits** page. |
| "You have reached your specified API usage limits", or "Your monthly spend limit has been reached" | Your spend limit worked. Raise it a little in **Settings > Billing**, or wait until it resets. |
| Calls stop working and your credit balance is $0, or "Your API credit has run out" | Buy a little more credit (step 2b). |
| Error 529, or "busy or having a problem" | Anthropic is overloaded. Wait a few minutes and try again. |
| `Stopped because: max_tokens`, and the answer is cut off or missing | Raise `max_tokens` (1000 is a good start), and make your program check `stop_reason`. |
| The model's numbers or fields are wrong | That's why your program checks them and a person confirms what matters. Make the prompt and the schema's descriptions more specific, then try again. |
| You pasted a key into Claude Code, a chat or a screenshot, or committed it | Step 2f, now: delete the key in the Console first, then make a new one. |
| A bigger bill than expected | Check the Console's **Usage** page, look for a loop that calls the model, and lower your spend limit (step 2c). |
| `.env` shows in `git status` | Don't commit. Step 5b: add `.env` to `.gitignore` first. |
| Work was committed to `main` | Use [week 5's rescue](../05-building-with-ai/README.md#if-it-committed-to-main). |
