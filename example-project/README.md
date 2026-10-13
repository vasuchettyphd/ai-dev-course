# Example project: rental deal screener

**This is the instructor's worked example, not a project for you to copy.** It shows what each week's work looks like on one real project, so you can compare it with your own.

## What it is

A small tool for someone thinking about buying their first rental property. You type in one listing's numbers (price, rent, costs, loan terms), and it tells you:

- the monthly cash flow,
- the cap rate,
- the cash-on-cash return,
- whether the deal passes your own rules (your "buy box"), and if not, why not.

The idea comes from the [`/grill-me` and Superpowers tutorial](../advanced/grill-me-superpowers/), which grills the buy box and then builds the calculator.

## How it grows

The class builds this project up week by week, alongside your own:

| Week | What gets added |
|---|---|
| 4 | [`PLAN.md`](PLAN.md): the plan, in the course's fixed outline |
| 5 | the first three build steps: the calculator, the buy-box check and a program you run, each built test first from a [Superpowers plan](docs/superpowers/plans/2026-10-12-first-three-steps.md) |
| 6 | a code review: three reviewer agents in [`.claude/agents/`](.claude/agents/), their findings and the decision on each in [`REVIEW.md`](REVIEW.md), and the fix commits, each named after its finding's number |
| 7 | a [`Dockerfile`](Dockerfile) and [`.dockerignore`](.dockerignore), so the program and its tests run the same way inside a Docker container |
| 8 | a real bug fixed test first: a classmate's feedback form found it ([`FEEDBACK.md`](FEEDBACK.md) is the instructor's example), [`BUGS.md`](BUGS.md) logs it, and one commit carries the failing test and the fix |
| 9 | an optional "paste the listing" step: a model (Claude Haiku 5.5, through the Anthropic API) reads a pasted listing and offers its numbers, which you confirm or replace; tests use a fake model, so they need no key and cost nothing |
| 10 | investor notes you can ask questions of: `python3 -m dealscreener.notes index` turns each note into an embedding (Google's `gemini-embedding-001`), and `ask` finds the notes closest in meaning to your question and has Claude Haiku answer from those notes only, naming its sources; tests use fake embeddings and a fake model, so they need no keys and cost nothing |
| 11 | tools, an agent and MCP: the calculator becomes a tool (`screen_listing`) that Claude can call; `python3 -m dealscreener.agent "your question"` runs an agent loop (Claude asks for the tool, the program runs it and sends the result back, at most 5 calls to Claude), and `python -m dealscreener.mcp_server` offers the same tool to Claude Code as an MCP server; tests use a fake model, so they need no key and cost nothing |
| 12 onward | more of the tool, step by step, following the plan |

Each week's finished state is marked with a **git tag** named after the week: `week-04` to `week-09` exist now, the week 10 state will get the tag `week-10` once week 10 is published, and later weeks follow (`week-10`, ... up to `week-13`). In-class demos start from the previous week's tag. If you fall behind, open the course repo on GitHub, click the branch menu, choose the **Tags** tab and pick a week to see what "done" looked like then (the exact menu is being tested).

## What's here now (week 11)

Everything from week 10 (listed below), plus:

- `dealscreener/tools.py`: the `screen_listing` tool. `TOOL_SCHEMA` is what Claude is told about it: its name, a plain description (it says percentages are written as 25 for 25%, and that 5% vacancy and 8% repairs are already allowed for), and the nine numbers it needs, each with a type and a description, all required, nothing else allowed. `screen_listing` checks every number with the same rules as the program's questions, runs the calculator and the buy box, and returns the four results (rounded to cents), each rule's reason, and `PASS` or `FAIL`. A wrong number raises `ToolInputError` with one sentence naming the field, for example `interest_rate_pct is 250: it must be a percentage from 0 to 100.` A rate between 0 and 1 is refused with `interest_rate_pct is 0.07: percentages are written as 7 for 7%. Ask the user which they meant.` (the week 8 bug, now for the tool). The tool only calculates: it reads no files, writes nothing and sends nothing.
- `dealscreener/agent.py`: the agent command, `python3 -m dealscreener.agent "your question"`. It sends the question and the tool's description to Claude Haiku 5.5. When Claude asks for the tool, the program prints `Calling screen_listing with` and the numbers, runs the tool, and sends the result back (or the error sentence, marked as an error, so Claude can fix it or ask you). It stops at Claude's final answer, or after 5 calls to Claude (the course's own limit, so a confused model can't run up a bill), and prints what all the calls cost together. The instructions tell Claude to use the tool for every number, to give the tool's numbers exactly, to ask for any of the nine numbers the question leaves out instead of guessing, and to explain the result for a beginner.
- `dealscreener/mcp_server.py`: the same tool as an MCP server, for Claude Code (see [How to use the MCP server in Claude Code](#how-to-use-the-mcp-server-in-claude-code)). It needs no key and reads no `.env` file.
- `tests/test_tools.py` (25 tests) and `tests/test_agent.py` (20 tests): a fake client plays Claude from a script of replies, so they run with plain `python3`, no key, no internet and no packages. They cover listing B (cash flow 430.53, `PASS`), listing A (`FAIL`), every kind of wrong input, a tool call and its result going back with the matching id, Claude's whole reply (including its thinking) going back unchanged, two tool calls in one reply, an unknown tool, the 5-call limit, a cut-off answer, a refusal, the cost line and the error sentences.
- `tests/test_mcp_server.py` (5 tests): starts the real MCP server and talks to it the way Claude Code would, with the MCP package's own client. Skipped when the `mcp` package isn't installed.
- `tests/test_agent_live.py`: one real run, skipped unless you ask for it (see [How to ask the agent](#how-to-ask-the-agent)).
- `requirements.txt`: adds `mcp[cli]`, the official MCP package, pinned to the version the course tested (2.3.0). It needs Python 3.11 or newer; on an older Python, pip skips it and installs the rest.

## What week 10 added

Everything from week 9 (listed below), plus:

- `notes/`: eight short investor notes, each marked "Fictional notes written for this course example; no real people or addresses." They cover the Riverside association dues, the university district, a rule of thumb for the repairs reserve, the write-up of listing B, a lender's notes on down payments, property tax after a sale, an insurance quote, and one note with nothing about money (how a contractor likes to be called), there to show that a note unrelated to a money question should score low against it. The Riverside note says "association dues" and never "HOA", so asking about HOA fees shows that the search goes by meaning, not by the same words. `listing-b-write-up.md` is longer than one chunk (800 characters), so it is split into two parts.
- `dealscreener/notes.py`: the notes command, `python3 -m dealscreener.notes`.
  - `index` reads every `.md` and `.txt` file in `notes/`, cuts each into chunks of at most 800 characters (whole paragraphs where it can), and asks Google's embedding model for one embedding per chunk: a list of 768 numbers that stands for the chunk's meaning. It saves the chunks, their embeddings and a fingerprint of each file in `notes-index.json`.
  - `ask "your question"` gets an embedding for the question, compares it with every chunk's embedding (cosine similarity), prints the three best matches with their scores, and sends just those three chunks and the question to Claude Haiku 5.5. The instructions tell Claude to answer only from those notes, to list the file names it used after the word `Sources:`, and to reply exactly `My notes don't say.` when the notes don't answer the question. It prints the answer and what the Claude call cost.
  - If you add, change or delete a note after indexing, `ask` stops and tells you to run `index` again, so answers never come from old notes. If the Claude call fails (for example, no Anthropic key), `ask` still prints the matching notes themselves. Each kind of failed Google call (no key, a key that isn't accepted, too many requests, no internet) becomes one plain sentence, and neither key is ever printed.
- `tests/test_notes.py`: 40 tests for `notes.py`. A fake embedder stands in for Google: it counts words for a few ideas, so "association dues" and "HOA" count as the same idea, and a fake client stands in for Claude. They run with plain `python3`, no keys, no internet and no packages. They cover chunking, reading the notes folder (including a file that isn't text), search by meaning, sending the notes in batches, spotting changed notes, the answer instructions, a cut-off answer and a refusal, every error sentence (with a key hidden in the error, which must never show), and the command itself.
- `tests/test_notes_live.py`: one real run, skipped unless you ask for it (see [How to ask your notes](#how-to-ask-your-notes)).
- `requirements.txt`: adds `google-genai`, Google's official library, pinned to the version the course tested (2.30.0).
- `.env.example`: adds a `GEMINI_API_KEY` line.
- `.dockerignore` and the course `.gitignore`: both leave out `notes-index.json`, because it holds the full text of your notes.

## What week 9 added

Everything from week 8 (listed below), plus:

- `dealscreener/extract.py`: the listing step's model call. It sends the pasted listing to Claude Haiku 5.5 (`claude-haiku-5-5`) in one call and asks for the five property numbers in a fixed JSON shape (Anthropic calls this "structured outputs"). Each number comes back, or `null` when the listing doesn't say. The code then checks every number itself: anything that isn't a number of 0 or more is dropped and asked for normally. It also turns each kind of failed call (no key, wrong key, no credit, no internet, too many requests) into one plain sentence, and works out what the call cost from its token counts and the published price. It never prints the key.
- `dealscreener/__main__.py`: `python3 -m dealscreener --listing` turns the step on. Without `--listing` the program behaves exactly as in week 8.
- `listings/`: two listings to paste. `listing-b.txt` is listing B written as a real listing (with extra numbers that aren't inputs, like bedrooms and the year built). `messy-listing.txt` is harder on purpose: a "price reduced from" figure, the property tax given per month instead of per year, the HOA fee per month, and no insurance figure at all.
- `requirements.txt`: the one package the listing step needs, `anthropic`, pinned to the version the course tested (1.13.0).
- `.env.example`: what your `.env` file should look like, with a made-up value. Your real key goes in `.env`, which git and Docker both ignore.
- `tests/test_extract.py`: tests for `extract.py`. A fake client stands in for Anthropic, so they run with plain `python3`, no key, no internet and no `anthropic` package. They include a reply that was cut off, a refusal, an answer that isn't JSON, odd values (text, negative, missing) and every error sentence, and they check that the key never appears in a message.
- `tests/test_main.py`: a new `ListingStepTest` class, with the same fake client: accepting a number with Enter, typing over it, a missing number asked normally, a listing number that fails the usual checks, skipping with `done`, a paste that is too long, and each kind of failure falling back to typing the numbers.
- `tests/test_live.py`: one real call, skipped unless you ask for it (see [How to use the listing step](#how-to-use-the-listing-step)).
- `Dockerfile`: now installs `requirements.txt` before copying the code.

## What was here in week 8

- `README.md`: this page.
- `PLAN.md`: the plan from week 4. In week 5 the repairs reserve was decided while building: 8% of monthly rent. In week 6 the review led to one more line: the buy-box rules compare each number rounded to 2 decimals, as it is shown.
- `docs/superpowers/plans/2026-10-12-first-three-steps.md`: the instructor's task plan, written in the format Superpowers' `writing-plans` produces, from the plan's first three build steps. Compare it with your own.
- `.claude/agents/`: the three reviewer agents from week 6 (`does-it-work`, `safe-and-private` and `plain-english`). Each can only read files, never change them.
- `REVIEW.md`: the week 6 code review. Each finding has a decision (`Fix` or `Won't fix`) and a short reason; every fix is in a commit named after its number (the wording fixes share one). Find those commits on the Commits tab of the week 6 pull request on the course repo. Week 7 added a section reviewing the Dockerfile and .dockerignore (findings D1 to D4).
- `Dockerfile`: the recipe Docker follows to build an image of the program, with a plain-English note above every line.
- `.dockerignore`: the files Docker leaves out of the image, with the reason for each group.
- `FEEDBACK.md`: the week 8 feedback form, filled in for this project by the instructor acting as the classmate. It lists the inputs tried (including the odd-input list), what worked, and what broke: an interest rate typed as `0.07`.
- `BUGS.md`: the bug list, one section each, newest last. Bug 1 is the `0.07` interest rate, now fixed. Each bug uses this template:

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
- `dealscreener/`: the code.
  - `calculator.py` works out the monthly mortgage, cash flow, cap rate and cash-on-cash return for one listing.
  - `buybox.py` checks those numbers against the buy box and gives the reason for each pass or fail.
  - `__main__.py` is the program you run: it asks for the numbers and prints the report. Week 8 added one follow-up question for a percentage typed as a decimal (bug 1).
- `tests/`: the tests, written before the code. Two listings were worked out by hand first, and the tests check the code gets the same answers. Week 6 added two more hand-worked cases (a $150 HOA fee, and 10% vacancy with a 5% repairs reserve) and a few more checks, because the review found them missing. Week 8 added the `SmallPercentTest` tests for bug 1, written before the fix: five of them failed until the fix went in, and three check answers that already worked and must keep working.

## How to run it

You need Python 3.9 or newer (type `python3 --version` to check). Nothing else needs installing: the code uses only Python's standard library. (The optional listing step from week 9, the notes command from week 10 and the agent and MCP server from week 11 need more: see [How to use the listing step](#how-to-use-the-listing-step), [How to ask your notes](#how-to-ask-your-notes), [How to ask the agent](#how-to-ask-the-agent) and [How to use the MCP server in Claude Code](#how-to-use-the-mcp-server-in-claude-code).)

Open the Terminal (Mac) or, on Windows, the Ubuntu window you set up in week 2, go to the folder where you cloned the course repo, and type:

```
cd example-project
python3 -m unittest
```

The last line should say `OK`. To screen a listing yourself, type:

```
python3 -m dealscreener
```

It asks for each number in turn. Type the number and press Enter. If you type something that isn't a sensible number, it says what to type and asks again. Try listing B from the [task plan](docs/superpowers/plans/2026-10-12-first-three-steps.md) (price 150000, rent 1700, tax 2400, insurance 1200, HOA 0, down payment 25, interest rate 7, loan term 30, closing costs 6000): the monthly cash flow should be $430.53 and the deal should pass. If you type a percentage as a decimal, like `0.07` for the interest rate, it asks whether you meant 7%: type `y` for 7% or `n` to keep 0.07%.

## How to run with Docker

From week 7 you can also run the program inside a Docker container, so it behaves the same on every computer. You need Docker Desktop installed and running (see the [week 7 page](../weeks/07-running-with-docker/README.md)). Python doesn't need to be installed for this: the image brings its own (Python 3.12).

First build the image, starting in the course repo folder.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
cd example-project
docker build -t dealscreener .
```

This builds an image called `dealscreener` from the `Dockerfile` in this folder (the final `.` means "this folder"). The first build downloads the official Python image, so it takes longer; later builds are quick.

Next, run the tests inside the container.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
docker run --rm dealscreener python -m unittest
```

The last line should say `OK`, just as on your own computer. Then screen a listing.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
docker run -it --rm dealscreener
```

It asks for each number in turn, the same as `python3 -m dealscreener`. `-it` lets you type into the program (`-i` keeps your typing connected to the program, `-t` makes it act like a terminal); `--rm` deletes the stopped container when the program ends, so they don't pile up. If you leave out `-it`, the program can't read what you type: it prints `Stopped before all the numbers were typed.` and stops.

The image holds only what the program needs. `.dockerignore` leaves out git's history, the Claude Code and Superpowers settings, Python's saved bytecode (`__pycache__`), any `.env` file of secrets, key files (`.pem`, `.key`), logs, spreadsheet exports (`.csv`) and, from week 10, the notes index (`notes-index.json`). It also leaves out `docs`, `REVIEW.md`, `BUGS.md` and `FEEDBACK.md`: people read them, but the program doesn't need them.

The program runs inside the container as a user called `nobody`, which has no special powers, rather than as the all-powerful `root` user. That line (`USER nobody`) is optional: if your own program writes files inside `/app` and gets "Permission denied", remove that line from your Dockerfile or ask Claude.

## How to use the listing step

From week 9 the program can read a pasted listing for you. It sends the text to a model (Claude Haiku 5.5) through the Anthropic API, then shows each number it found at the usual question. Press Enter to keep a number, or type the right one. Questions the listing didn't answer, and the loan questions, are asked as usual. Every call costs a little API credit (see the [cost record](#cost-record)), and the program never calls the model unless you add `--listing`.

You need three things: an API key with credit on it, a `.env` file holding the key, and the `anthropic` package. The [week 9 page](../weeks/09-calling-a-model/README.md) (published with this week) walks through each step; in short:

- **Key:** in the Anthropic Console, go to Settings > API keys (https://platform.claude.com/settings/keys) and click **Create key**. Choose a **workspace** for it (a key not tied to a workspace was refused with "This API key is not scoped to a workspace"). The Console shows the key, which starts with `sk-ant-`, only once, so put it straight into `.env` (step 1 below).
- **Spend limit, before your first call:** in Settings > Billing (https://platform.claude.com/settings/billing), set a monthly spend limit in the "Spend limits" section, so a mistake can't cost more than you chose.
- **Safety:** the key goes only in `.env`, typed with a text editor. Never in Claude Code, a chat, a screenshot, a commit or a pull request.

**1. Put your key in `.env`, with a text editor.** Never paste your key into Claude Code, a chat, a screenshot, a commit or a pull request. In the `example-project` folder, make a copy of `.env.example` called `.env`.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
cp .env.example .env
```

Open `.env` in a text editor (not in Claude Code), replace `put-your-key-here` with your key, and save. Write the key with no quote marks around it, like `ANTHROPIC_API_KEY=sk-ant-...`: `docker run --env-file` keeps quote marks as part of the key, and Anthropic then rejects it. Then check git ignores `.env`.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
git check-ignore .env
```

It should print `.env`. If it prints nothing, stop: don't commit anything until `.env` is in your `.gitignore`. If a key is ever shared by mistake, revoke it in the Anthropic Console first, then make a new one.

**2. Install the package in a virtual environment.** A virtual environment (a `.venv` folder) keeps this project's packages separate from the rest of your computer. The `anthropic` package needs Python 3.10 or newer: type `python3 --version`, and if it shows 3.9, use Docker instead (step 4).

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`source .venv/bin/activate` switches this window to the virtual environment: your prompt starts with `(.venv)`. In a new window, type it again before running the program. On Windows, if `python3 -m venv .venv` says `ensurepip is not available` and suggests `apt install python3.12-venv`, type `sudo apt install python3-venv`, delete the broken `.venv` folder it left behind (`rm -r .venv`), and run the three lines again. `rm -r .venv` deletes only that broken `.venv` folder you just made, by name, and nothing else: never add `-f` or any other folder or file to it.

**3. Run it with `--listing`.**

Type in: the Terminal on a Mac, or the Ubuntu window on Windows (with `(.venv)` showing).

```
python3 -m dealscreener --listing
```

Paste the listing, then type `done` on a line by itself and press Enter. (Type `done` straight away to skip the step.) Try `listings/listing-b.txt`: in the course's run every number matched listing B, so pressing Enter five times and typing the loan details (25, 7, 30, 6000) gave a cash flow of $430.53. Then try `listings/messy-listing.txt` and check what the model made of the monthly tax and the missing insurance before you press Enter. In the course's run it turned the $200 a month tax into 2400 a year, left the insurance out (so you're asked for it), ignored the old "reduced from" price, and found the $185 HOA. The model can be wrong: you are the one who confirms each number.

If something goes wrong (no key, a key that isn't accepted, no credit, no internet), the program says so in one sentence, adds "For now, type the numbers yourself.", and asks the questions as usual. The tests never call the model: `python3 -m unittest` stays free and works without a key. The one real-call test runs only on request.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows (with `(.venv)` showing).

```
set -a; . ./.env; set +a
RUN_LIVE_TESTS=1 python -m unittest tests.test_live -v
```

The first line loads the key from `.env` into this window without showing it.

**4. With Docker.** The image installs `requirements.txt` itself, so you only need Docker Desktop. Build the image again (week 7's `docker build -t dealscreener .`), then give the container your key when it starts, never inside the image.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
docker run -it --rm --env-file .env dealscreener python -m dealscreener --listing
```

`--env-file .env` hands the key to this one container while it runs. `.dockerignore` keeps `.env` out of the image, so the image never holds your key.

### Cost record

What each real call cost, from the token counts the program prints and Haiku 5.5's published price: $0.10 per million input tokens and $0.50 per million output tokens (for prompts up to 100,000 tokens; [Anthropic's pricing page](https://platform.claude.com/docs/en/about-claude/pricing), read on 2026-10-12).

| Call | Input tokens | Output tokens | Cost |
|---|---|---|---|
| `listing-b.txt` | 887 | 65 | 887 x $0.10 / 1,000,000 + 65 x $0.50 / 1,000,000 = about $0.00012 |
| `messy-listing.txt`, first run | 823 | 174 | about $0.00017 |
| `messy-listing.txt`, second run | 823 | 146 | about $0.00016 |

These ran on 12 October 2026. The same listing can use a different number of output tokens each time.

## How to ask your notes

From week 10 you can ask questions of your own investor notes in plain English. The notes are the files in `notes/`. You build an index once, then ask as many questions as you like.

**How it finds the right notes.** An embedding is a list of numbers that stands for the meaning of a piece of text: two texts about the same idea get lists that point in nearly the same direction, even when they use different words. The program compares them with cosine similarity, a score from -1 to 1 where higher means closer in meaning. Google's [embeddings page](https://ai.google.dev/gemini-api/docs/embeddings) (read 2026-10-13) puts it this way: "Cosine similarity is a good distance metric because it focuses on direction rather than magnitude." The program uses `gemini-embedding-001`, which Google supports until 14 May 2028 ([deprecations page](https://ai.google.dev/gemini-api/docs/deprecations)). Google's newer model, `gemini-embedding-2`, also takes images, video, audio and PDFs ([its model page](https://ai.google.dev/gemini-api/docs/models/gemini-embedding-2), read 2026-10-13), but it is called differently, so the course stays with 001 for now.

**What it costs.**

- Google: on the free tier, no charge for this course's use (being tested for `gemini-embedding-001`: Google's [pricing page](https://ai.google.dev/gemini-api/docs/pricing), read 2026-10-13, lists only the newer `gemini-embedding-2`, whose free tier says "Free of charge"). The notes are embedded once, when you run `index`. Each question is one more small embedding. Google doesn't publish its free-tier limits for embeddings; you can see yours in Google AI Studio.
- Claude: each question is one Haiku 5.5 call, at the same price as the listing step (see the [cost record](#cost-record)). The program prints what each call cost.

**What Google does with your text on the free tier.** From the [Gemini API terms](https://ai.google.dev/gemini-api/terms) (read 2026-10-13), for the free ("Unpaid") services:

> To help with quality and improve our products, human reviewers may read, annotate, and process your API input and output.

> Do not submit sensitive, confidential, or personal information to the Unpaid Services.

On the paid tier Google says it doesn't use your prompts or responses to improve its products. Treat your use as unpaid, and only index notes you'd be happy for a stranger to read: these fictional notes, public material or your own non-private writing. Never index real tenants' details, customer data or anything confidential. (Calls to the Gemini API count as paid only through a Google Cloud project with billing switched on, so without billing they are on the free tier.)

You need two keys now: the Anthropic key from week 9 and a Google key. The [week 10 page](../weeks/10-embeddings-and-rag/README.md) (published with this week) walks through getting the Google key; in short:

- **Google key:** sign in to Google AI Studio and create an API key, as Google's [API key page](https://ai.google.dev/gemini-api/docs/api-key) describes (read 2026-10-13). You must be 18 or older. A school Google account works only if your school hasn't turned AI Studio off (check with your instructor); a personal Google account is the fallback. Google's API key page also says: "Adding restrictions to your API keys minimizes the potential damage if a key is compromised." Look at your key's settings in AI Studio for a restriction to the Gemini API (the exact screens are being tested).
- **Safety:** both keys go only in `.env`, typed with a text editor. Never in Claude Code, a chat, a screenshot, a commit or a pull request. If a key is ever shared by mistake, delete it first (in AI Studio for the Google key, in the Anthropic Console for the other), then make a new one.

**1. Add the Google key to `.env`, with a text editor.** If you made `.env` in week 9, open it in a text editor (not in Claude Code) and add a new line `GEMINI_API_KEY=` followed by your key, with no quote marks. If you don't have a `.env` yet, copy `.env.example` first (`cp .env.example .env`, in the Terminal on a Mac or the Ubuntu window on Windows), then replace each `put-your-key-here`. Use the name `GEMINI_API_KEY` only: don't also set `GOOGLE_API_KEY`, which Google's library would read in its place. Then check git still ignores `.env`.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
git check-ignore .env
```

It should print `.env`. If it prints nothing, stop and fix that first (see step 1 of [How to use the listing step](#how-to-use-the-listing-step)).

**2. Install the new package.** `requirements.txt` now lists `google-genai` too, which needs Python 3.10 or newer like `anthropic`. Switch to the virtual environment from week 9 and install again.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
source .venv/bin/activate
pip install -r requirements.txt
```

(No `.venv` yet? Make one first with `python3 -m venv .venv`, as in [How to use the listing step](#how-to-use-the-listing-step). On Python 3.9, use Docker instead: step 6.)

**3. Build the index.**

Type in: the Terminal on a Mac, or the Ubuntu window on Windows (with `(.venv)` showing).

```
python3 -m dealscreener.notes index
```

It should print `Indexed 9 chunks from 8 notes.` (8 notes, and the listing B write-up counts twice because it is split in two). In the course's run it took about a second. This saves `notes-index.json` in this folder. **Don't commit it:** it holds the full text of every note, so it follows the same privacy rule as the notes themselves. The course's `.gitignore` already leaves it out; for your own project, add `notes-index.json` to your `.gitignore`.

**4. Ask a question.**

Type in: the Terminal on a Mac, or the Ubuntu window on Windows (with `(.venv)` showing).

```
python3 -m dealscreener.notes ask "What are the association dues like in Riverside?"
```

It prints `Notes that match best:` and the three best notes with their similarity scores, then Claude's answer with a `Sources:` line, then what the Claude call cost. In the course's run of the live test with this question, the first match was `  riverside-association-dues.md part 1 (similarity 0.77)`, and the call used 725 input and 296 output tokens, about $0.00022. Then try:

- `"What repairs reserve did I use for listing B?"`: the answer should be 8% of the rent, from `listing-b-write-up.md`.
- `"What did I note about solar panels?"`: no note mentions solar panels, so the answer should be exactly `My notes don't say.` The matches are still printed, but they are only the closest of a poor set.
- `"What are the HOA fees like in Riverside?"`: the Riverside note never says "HOA", yet it should still match, because the search goes by meaning.

If you add, change or delete a note, `ask` says `Your notes changed since the index was built. Run: python3 -m dealscreener.notes index`. Run `index` again, then ask again.

If something goes wrong with Google (no key, a key that isn't accepted, too many requests, no internet), the program says so in one sentence and stops. If only the Claude call fails, it says why, adds "Here are the notes that match best instead.", and prints those notes. The tests never call Google or Claude: `python3 -m unittest` stays free and works without keys.

**5. The live test (optional).** One real run: it builds the index into a temporary folder, asks the Riverside question, and checks that the Riverside note is among the matches and that the answer isn't `My notes don't say.`

Type in: the Terminal on a Mac, or the Ubuntu window on Windows (with `(.venv)` showing).

```
set -a; . ./.env; set +a
RUN_LIVE_TESTS=1 python3 -m unittest tests.test_notes_live -v
```

The first line copies both keys from `.env` into this window, without showing them, so the test can use them: `set -a` marks every setting read next for passing on to programs, `. ./.env` reads the file, and `set +a` turns the marking off again. The keys stay in this window only until you close it.

**6. With Docker.** Build the image again (`docker build -t dealscreener .`, as in [How to run with Docker](#how-to-run-with-docker)). The image never holds your keys or the index: `.dockerignore` leaves out `.env` and `notes-index.json`. So each command below hands the container your keys, your notes folder and the index file while it runs. First make an empty index file, once, so Docker has a file to connect (without it, Docker would make a folder of that name instead).

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
touch notes-index.json
```

Then build the index and ask a question.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
docker run --rm --env-file .env --user "$(id -u):$(id -g)" -v "$PWD/notes:/app/notes:ro" -v "$PWD/notes-index.json:/app/notes-index.json" dealscreener python -m dealscreener.notes index
docker run --rm --env-file .env --user "$(id -u):$(id -g)" -v "$PWD/notes:/app/notes:ro" -v "$PWD/notes-index.json:/app/notes-index.json" dealscreener python -m dealscreener.notes ask "What are the association dues like in Riverside?"
```

- `--env-file .env` hands both keys to this one container while it runs.
- `-v "$PWD/notes:/app/notes:ro"` lets the container read your current `notes` folder in place of the copy inside the image (`$PWD` means "the folder you're in"; `:ro` means read only, so the container can't change your notes). Nothing else from this folder goes in.
- `-v "$PWD/notes-index.json:/app/notes-index.json"` connects that one file, so `index` saves the index into your folder and `ask` reads it from there. Without it, `index` can't save: the program runs as the `nobody` user, which can't write inside the image, and it says `Couldn't save the index file notes-index.json.`
- `--user "$(id -u):$(id -g)"` runs the program as you, so it is allowed to write to your index file.

The course checked both commands in the container with a made-up key: the folders connected, the made-up key was refused with the plain sentence, and a stand-in index was saved to the file and read back. The `--user` part was checked on Windows (WSL) only and is being tested on a Mac; the run with real keys is being tested too.

### Notes cost record

What the course's real runs cost, on 13 October 2026 (Claude at $0.10 / $0.50 per million input / output tokens).

| Run | Google (embeddings) | Claude input tokens | Claude output tokens | Claude cost |
|---|---|---|---|---|
| `index` (9 chunks) | 9 embeddings, no token count returned | none | none | none |
| `What are the HOA fees like in Riverside?` | 1 embedding | 585 | 268 | about $0.00019 |
| `What repairs reserve did I use for listing B?` | 1 embedding | 739 | 276 | about $0.00021 |
| `What did I note about solar panels?` (answer: `My notes don't say.`) | 1 embedding | 620 | 151 | about $0.00014 |

Google's embedding responses reported no token counts, so the program prints only Claude's cost.

## How to ask the agent

From week 11 you can ask about a listing in plain English, and Claude works out the answer with the deal screener's own calculator. Claude doesn't do the sums itself: it asks for the `screen_listing` tool, the program runs the tool on your computer and sends the result back, and Claude explains it. This back and forth is the **agent loop**. The program allows at most 5 calls to Claude per question. Anthropic's documentation sets no limit: 5 is the course's own safety rule.

You need the same things as the listing step: an Anthropic key in `.env`, and the packages from `requirements.txt` in a virtual environment (see steps 1 and 2 of [How to use the listing step](#how-to-use-the-listing-step)). The agent needs Python 3.10 or newer, like `anthropic`.

**1. Ask a question with all nine numbers.**

Type in: the Terminal on a Mac, or the Ubuntu window on Windows (with `(.venv)` showing).

```
python3 -m dealscreener.agent "Should I buy this rental? The price is \$150,000 and the rent is \$1,700 a month. Property tax is \$2,400 a year, insurance is \$1,200 a year and there is no HOA fee. I'd put 25% down on a 30-year loan at 7% interest, with \$6,000 in closing costs."
```

The `\` before each `$` stops the Terminal reading `$150` as a setting of its own. In the course's run it printed the tool call first:

```
Calling screen_listing with {"purchase_price":150000,"monthly_rent":1700,"yearly_property_tax":2400,"yearly_insurance":1200,"monthly_hoa":0,"down_payment_pct":25,"interest_rate_pct":7,"loan_term_years":30,"closing_costs":6000}
```

Then Claude's answer: the listing passes, with a monthly mortgage of $748.47, a monthly cash flow of $430.53, a cap rate of 9.43% and a cash-on-cash return of 11.88%, each explained in a sentence, the two buy-box rules, and what to check before buying (the real rent, the property's condition, the actual tax and insurance quotes). Last came the cost:

```
Used 3072 input and 988 output tokens on Claude in 2 turns, about $0.00080.
```

Two turns means two calls to Claude: one that asked for the tool, and one that answered with the tool's result. Claude's wording is different every time; the numbers come from the tool, so they are the same every time.

**2. Leave numbers out.** Try `python3 -m dealscreener.agent "Should I buy a rental priced at \$150,000 that rents for \$1,700 a month?"`. In the course's run Claude didn't call the tool: it listed the seven missing numbers (tax, insurance, HOA, down payment, rate, loan term, closing costs) and asked for them. That took 1 turn: 1215 input and 378 output tokens, about $0.00031. The agent answers one question and stops, so ask again with all nine numbers.

**3. Write the rate as a decimal.** Try the question from step 1 with `an interest rate of 0.07` in place of `7% interest`. In the course's run Claude sent 7 to the tool and said "I read your 0.07 interest rate as 7%." If Claude ever sends 0.07, the tool refuses it with `interest_rate_pct is 0.07: percentages are written as 7 for 7%. Ask the user which they meant.`, and Claude gets that sentence back as an error to act on. Either way, read the numbers in the `Calling screen_listing with` line: they are the ones the answer is based on.

If something goes wrong (no key, a key that isn't accepted, no credit, no internet), the program says so in one sentence and stops, the same sentences as the listing step. If Claude's answer is cut off or declined, it prints that sentence and what the calls so far cost. If Claude hasn't answered after 5 calls, it prints `Stopped after 5 turns without a final answer.` and what those calls cost. The tests never call Claude: `python3 -m unittest` stays free and works without a key.

**4. The live test (optional).** One real run of the question from step 1: it checks that Claude called the tool at least once and that the answer contains 430.53.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows (with `(.venv)` showing).

```
set -a; . ./.env; set +a
RUN_LIVE_TESTS=1 python3 -m unittest tests.test_agent_live -v
```

**5. With Docker.** Build the image again (`docker build -t dealscreener .`), then hand the container your key while it runs.

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
docker run --rm --env-file .env dealscreener python -m dealscreener.agent "Should I buy a rental priced at \$150,000 that rents for \$1,700 a month?"
```

### Agent cost record

What the course's runs of the final code cost, on 13 October 2026 (Claude Haiku 5.5 at $0.10 / $0.50 per million input / output tokens). Every call sends the whole conversation so far, plus the tool's description, so a two-turn question costs more than twice a one-call question.

| Question | Turns | Tool calls | Input tokens | Output tokens | Cost |
|---|---|---|---|---|---|
| Listing B, all nine numbers | 2 | 1 | 3072 | 988 | 3072 x $0.10 / 1,000,000 + 988 x $0.50 / 1,000,000 = about $0.00080 |
| Price and rent only | 1 | 0 | 1215 | 378 | about $0.00031 |
| Listing B with the rate as 0.07 | 2 | 1 | 3168 | 1056 | about $0.00084 |
| Live test, three runs | 2 each | 1 each | 3072, 3072, 3068 | 977, 867, 1018 | about $0.0007 to $0.0008 each |

**Two fixes the live runs led to.** In the first run Claude told the user the calculator leaves out vacancy and repairs, which is wrong (it allows 5% and 8% of the rent): the tool's description now says so. In the second run Claude rounded the cash flow to "about $431" and worked out a yearly figure itself, so the instructions now say to give the tool's numbers exactly, to the cent, and to do no sums of its own. The tests pin both. Reading the real answers, not only the tests, is what found them.

## How to use the MCP server in Claude Code

MCP (Model Context Protocol) is a standard way to connect AI apps to tools: the [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro) (read 2026-10-13) calls it "like a USB-C port for AI applications". `dealscreener/mcp_server.py` offers the `screen_listing` tool to any MCP app. Here the app is Claude Code: once it is connected, you can ask Claude Code to screen a listing and it calls your tool. The server needs no key and reads no `.env` file.

**An MCP server runs code on your computer.** Claude Code's [MCP page](https://code.claude.com/docs/en/mcp) (read 2026-10-13) says: "Verify you trust each server before connecting it. Servers that fetch external content can expose you to prompt injection risk." Add only servers you wrote yourself, like this one, or ones from a source you trust. Week 13 covers the risks in more depth.

You need Python 3.11 or newer for the `mcp` package (type `python3 --version` to check) and Claude Code from week 2. A virtual environment keeps the Python it was made with: if you made `.venv` with Python 3.10, `pip install -r requirements.txt` skips the MCP package and the steps below don't work. Then delete that `.venv` (`rm -r .venv`, which removes only that folder) and make it again with Python 3.11 or newer (for example `python3.12 -m venv .venv`, if `python3.12 --version` works), then activate it and install again. On Windows, do every step in the Ubuntu window: Claude Code and the server both run in Ubuntu.

**1. Install the package and test the server on its own.** In the `example-project` folder, with the virtual environment from week 9:

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
source .venv/bin/activate
pip install -r requirements.txt
python3 -m unittest tests.test_mcp_server -v
```

The tests start the server and talk to it with the MCP package's own client: they list its one tool, screen listing B (cash flow 430.53), check that a wrong number comes back as an error, and start it from another folder the way Claude Code may. All five should say `ok`. If they say `skipped`, the `mcp` package isn't installed in this window: check that `(.venv)` is showing and that `python3 --version` is 3.11 or newer.

You can also start the server by hand with `python -m dealscreener.mcp_server`, but it prints nothing: it waits silently for an app to connect. Press Ctrl+C to stop it.

**2. Add it to Claude Code.** Still in the `example-project` folder:

Type in: the Terminal on a Mac, or the Ubuntu window on Windows (with `(.venv)` showing).

```
claude mcp add dealscreener --scope project -e PYTHONPATH="$PWD" -- "$PWD/.venv/bin/python" -m dealscreener.mcp_server
```

- `dealscreener` is the name Claude Code shows for the server.
- `--scope project` saves it in a file called `.mcp.json` in this folder, for this project only.
- `-e PYTHONPATH="$PWD"` tells Python where the `dealscreener` folder is. `-m dealscreener.mcp_server` only finds it from inside `example-project`, and Claude Code may start the server from another folder; in the course's check, starting it from another folder without this setting failed with `No module named 'dealscreener'`, and with it the server started and screened listing B. Put the name `dealscreener` before `-e`, as shown.
- Everything after `--` is the command Claude Code runs to start the server. Claude Code stores it exactly as typed, so it uses the full path to the virtual environment's Python (`$PWD` means "the folder you're in"). With plain `python`, Claude Code would start a Python without the `mcp` package, and the server would fail.

In the course's check (Claude Code 2.1.296, in a test container, not signed in) it printed:

```
Added stdio MCP server dealscreener with command: /home/student/example-project/.venv/bin/python -m dealscreener.mcp_server to project config
File modified: /home/student/example-project/.mcp.json
```

and `.mcp.json` held this (your path will be your own folder):

```
{
  "mcpServers": {
    "dealscreener": {
      "type": "stdio",
      "command": "/home/student/example-project/.venv/bin/python",
      "args": [
        "-m",
        "dealscreener.mcp_server"
      ],
      "env": {
        "PYTHONPATH": "/home/student/example-project"
      }
    }
  }
}
```

No key is in it, and none is needed: the only setting is the folder. This example doesn't commit its `.mcp.json`, because the path belongs to one computer.

**3. Check it.**

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
claude mcp list
```

In the course's check it showed ``dealscreener: /home/student/example-project/.venv/bin/python -m dealscreener.mcp_server - ⏸ Pending approval (run `claude` to approve)``. For your safety, Claude Code asks you to approve a project's servers before it uses them. `claude mcp get dealscreener` shows the details.

**4. Approve it and ask.** Start Claude Code in the `example-project` folder (type `claude`), approve the `dealscreener` server when it asks, and ask, for example: "Use the screen_listing tool to screen this listing: price 150000, rent 1700 a month, tax 2400 a year, insurance 1200 a year, no HOA, 25% down, 7% interest, 30 years, closing costs 6000." Claude Code should ask your permission to run the tool (the permission prompt is being tested), then answer with a cash flow of $430.53 and `PASS`. The approval screen and the name Claude Code shows for the tool (perhaps `mcp__dealscreener__screen_listing`) are being tested in a signed-in session, and so is the `/mcp` screen inside Claude Code, which the docs say shows each server's status.

**How the MCP tool differs from the agent's.** The MCP package builds the tool's input schema from the function's parameters, so it is a little stricter in places and looser in one: `loan_term_years` must be a whole number like `30`, not `30.0`, and an unknown extra field isn't turned away with `Unknown field:` the way the agent's tool does it. The numbers and the error sentences are the same. If you copy the pattern for your own server: a problem raised as `ToolError` (from `mcp.server.mcpserver.exceptions`) reaches Claude as your own sentence, while any other error reaches it only as `Error executing tool screen_listing`.

**5. Remove it** when you no longer want it:

Type in: the Terminal on a Mac, or the Ubuntu window on Windows.

```
claude mcp remove dealscreener --scope project
```

In the course's check this left `.mcp.json` with an empty list of servers.

## What the numbers mean

- **Monthly cash flow:** the rent you keep each month after vacancy, running costs and the mortgage. Below $0 means you pay in each month.
- **Cap rate:** the rent left after vacancy and running costs for a whole year, before the mortgage, as a % of the price. It compares properties as if you paid cash.
- **Cash-on-cash return:** a year of cash flow as a % of the cash you put in (down payment plus closing costs). It is the return on your own money.

## Changing the settings

The vacancy (5%) and repairs reserve (8%) are the defaults in `Assumptions` in `dealscreener/calculator.py`. The buy-box rules (at least 10% cash-on-cash, at least $100 a month cash flow) are the defaults in `BuyBox` in `dealscreener/buybox.py`. The program doesn't ask for them: to change one, edit that number in the code and run the tests again.
