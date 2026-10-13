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
| 10 onward | more of the tool, step by step, following the plan |

Each week's finished state is marked with a **git tag** named after the week: `week-04` to `week-08` exist now, the week 9 state will get the tag `week-09` once week 9 is published, and later weeks follow (`week-10`, ... up to `week-13`). In-class demos start from the previous week's tag. If you fall behind, open the course repo on GitHub, click the branch menu, choose the **Tags** tab and pick a week to see what "done" looked like then (the exact menu is being tested).

## What's here now (week 9)

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

You need Python 3.9 or newer (type `python3 --version` to check). Nothing else needs installing: the code uses only Python's standard library. (The optional listing step from week 9 needs more: see [How to use the listing step](#how-to-use-the-listing-step).)

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

The image holds only what the program needs. `.dockerignore` leaves out git's history, the Claude Code and Superpowers settings, Python's saved bytecode (`__pycache__`), any `.env` file of secrets, key files (`.pem`, `.key`), logs and spreadsheet exports (`.csv`). It also leaves out `docs`, `REVIEW.md`, `BUGS.md` and `FEEDBACK.md`: people read them, but the program doesn't need them.

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

## What the numbers mean

- **Monthly cash flow:** the rent you keep each month after vacancy, running costs and the mortgage. Below $0 means you pay in each month.
- **Cap rate:** the rent left after vacancy and running costs for a whole year, before the mortgage, as a % of the price. It compares properties as if you paid cash.
- **Cash-on-cash return:** a year of cash flow as a % of the cash you put in (down payment plus closing costs). It is the return on your own money.

## Changing the settings

The vacancy (5%) and repairs reserve (8%) are the defaults in `Assumptions` in `dealscreener/calculator.py`. The buy-box rules (at least 10% cash-on-cash, at least $100 a month cash flow) are the defaults in `BuyBox` in `dealscreener/buybox.py`. The program doesn't ask for them: to change one, edit that number in the code and run the tests again.
