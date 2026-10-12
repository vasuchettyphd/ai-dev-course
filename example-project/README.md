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
| 8 onward | more of the tool, step by step, following the plan |

Each week's finished state will be marked with a **git tag** named after the week: the week 4 state will get the tag `week-04` once week 4 is published, the week 5 state will get the tag `week-05` once week 5 is published, the week 6 state will get the tag `week-06` once week 6 is published, and later weeks follow (`week-07`, ... up to `week-13`). In-class demos start from the previous week's tag. Once the tags exist, if you fall behind, open the course repo on GitHub, click the branch menu, choose the **Tags** tab and pick a week to see what "done" looked like then (the exact menu is being tested).

## What's here now (week 7)

- `README.md`: this page.
- `PLAN.md`: the plan from week 4. In week 5 the repairs reserve was decided while building: 8% of monthly rent. In week 6 the review led to one more line: the buy-box rules compare each number rounded to 2 decimals, as it is shown.
- `docs/superpowers/plans/2026-10-12-first-three-steps.md`: the instructor's task plan, written in the format Superpowers' `writing-plans` produces, from the plan's first three build steps. Compare it with your own.
- `.claude/agents/`: the three reviewer agents from week 6 (`does-it-work`, `safe-and-private` and `plain-english`). Each can only read files, never change them.
- `REVIEW.md`: the week 6 code review. Each finding has a decision (`Fix` or `Won't fix`) and a short reason; every fix is in a commit named after its number (the wording fixes share one). Find those commits on the Commits tab of the week 6 pull request on the course repo. Week 7 added a section reviewing the Dockerfile and .dockerignore (findings D1 to D4).
- `Dockerfile`: the recipe Docker follows to build an image of the program, with a plain-English note above every line.
- `.dockerignore`: the files Docker leaves out of the image, with the reason for each group.
- `dealscreener/`: the code.
  - `calculator.py` works out the monthly mortgage, cash flow, cap rate and cash-on-cash return for one listing.
  - `buybox.py` checks those numbers against the buy box and gives the reason for each pass or fail.
  - `__main__.py` is the program you run: it asks for the numbers and prints the report.
- `tests/`: the tests, written before the code. Two listings were worked out by hand first, and the tests check the code gets the same answers. Week 6 added two more hand-worked cases (a $150 HOA fee, and 10% vacancy with a 5% repairs reserve) and a few more checks, because the review found them missing.

## How to run it

You need Python 3.9 or newer (type `python3 --version` to check). Nothing else needs installing: the code uses only Python's standard library.

Open the Terminal (Mac) or, on Windows, the Ubuntu window you set up in week 2, go to the folder where you cloned the course repo, and type:

```
cd example-project
python3 -m unittest
```

The last line should say `OK`. To screen a listing yourself, type:

```
python3 -m dealscreener
```

It asks for each number in turn. Type the number and press Enter. If you type something that isn't a sensible number, it says what to type and asks again. Try listing B from the [task plan](docs/superpowers/plans/2026-10-12-first-three-steps.md) (price 150000, rent 1700, tax 2400, insurance 1200, HOA 0, down payment 25, interest rate 7, loan term 30, closing costs 6000): the monthly cash flow should be $430.53 and the deal should pass.

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

The image holds only what the program needs. `.dockerignore` leaves out git's history, the Claude Code and Superpowers settings, Python's saved bytecode (`__pycache__`), any `.env` file of secrets, key files (`.pem`, `.key`), logs and spreadsheet exports (`.csv`). It also leaves out `docs` and `REVIEW.md`: people read them, but the program doesn't need them.

The program runs inside the container as a user called `nobody`, which has no special powers, rather than as the all-powerful `root` user. That line (`USER nobody`) is optional: if your own program writes files inside `/app` and gets "Permission denied", remove that line from your Dockerfile or ask Claude.

## What the numbers mean

- **Monthly cash flow:** the rent you keep each month after vacancy, running costs and the mortgage. Below $0 means you pay in each month.
- **Cap rate:** the rent left after vacancy and running costs for a whole year, before the mortgage, as a % of the price. It compares properties as if you paid cash.
- **Cash-on-cash return:** a year of cash flow as a % of the cash you put in (down payment plus closing costs). It is the return on your own money.

## Changing the settings

The vacancy (5%) and repairs reserve (8%) are the defaults in `Assumptions` in `dealscreener/calculator.py`. The buy-box rules (at least 10% cash-on-cash, at least $100 a month cash flow) are the defaults in `BuyBox` in `dealscreener/buybox.py`. The program doesn't ask for them: to change one, edit that number in the code and run the tests again.
