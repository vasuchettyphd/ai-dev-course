# Archify: turn a project, or an idea, into a diagram you can click

A hands-on tutorial for [Archify](https://github.com/tt-a1i/archify), a free Claude Code skill by the developer **tt-a1i** (MIT licence). You describe a system or point Claude at a folder of code, and Archify produces a single `.html` file: an interactive diagram with a light and dark theme, several visual styles, and export to PNG, JPEG, SVG and a short motion clip.

You will draw three diagrams:

1. an **architecture diagram** of the course's rental deal screener, drawn by reading its code,
2. a **sequence diagram** of one thing a user does in it (paste a listing, get PASS or FAIL),
3. a **workflow diagram** of a made-up student startup, drawn from a plain-English description, with no code at all.

Everything here was run for real on **2026-10-22** with:

| Tool | Version |
|---|---|
| Archify skill | 3.2.0 (upstream commit `25cf370`) |
| `skills` installer | 1.7.4 (run with `npx`, nothing installed) |
| Claude Code | 2.1.309, model Sonnet |
| Node.js | 22.23.3 (the `skills` installer needs 22.20 or later) |
| Browser for the automated check | Chromium (Playwright build 1248) |

`demo/setup.sh` installs exactly that tested commit, `25cf370`, so you get the same Archify we used. The upstream install command under [The normal way](#the-normal-way-for-your-own-projects) installs the newest version instead, which may be newer than 3.2.0. The replies quoted below are the real ones from those runs. Your diagram will not be identical: Claude decides the layout and the wording each time.

**Time:** about 30-40 minutes. **Cost:** the three diagrams cost $0.90 of Sonnet usage in our runs ($0.44, $0.26 and $0.20). Redoing one costs about the same again. See [What it cost](#what-it-cost).

## The idea in one paragraph

Claude is good at reading code and explaining it, but a wall of text is a poor way to see how the parts of a program fit together. Archify gives Claude a fixed recipe for diagrams. Claude writes a small JSON file that lists the boxes, the arrows and (for code) the exact file and lines each box came from. Archify's own program, which runs on your computer with Node.js, then turns that JSON into a polished HTML page and checks it: does the JSON follow the rules, are the cited lines real, does the page render in a real browser without text overlapping or spilling off the screen. Claude only hands you the diagram once those checks pass. The result opens in any browser, works offline and can be emailed as one file.

## What it is, exactly

Archify is a real Claude Code **skill**: a folder with a `SKILL.md` file of instructions for Claude, plus the Node.js programs those instructions tell Claude to run. It is not an app you open and not an MCP server. Once it is installed, you just ask Claude for a diagram ("Use Archify to ...") and the skill takes over.

It draws ten kinds of diagram:

| Type | Good for |
|---|---|
| architecture | what a system is made of and what talks to what |
| workflow | step-by-step processes, approval gates, branches |
| sequence | the back-and-forth of one action, in time order |
| dataflow | where data (or money, or documents) goes |
| lifecycle | the states something moves through (an order, an application) |
| erd | database tables and how they link |
| class, tree, timeline, waterfall | code types, hierarchies, events over time, where the time went |

It can also make a one-page "explainer" (an answer laid out as a page), which this tutorial does not cover.

## Before you start

You need:

- Claude Code, working.
- **Node.js 22.20 or later.** Check with `node --version`. The `skills` installer refuses older versions. If it's missing, install the LTS version from [nodejs.org](https://nodejs.org).
- **git.** Check with `git --version`.
- **Google Chrome, Chromium or Microsoft Edge.** Archify's last check opens your diagram in a hidden browser window. Without one the diagram is still made, but the check fails (see [Troubleshooting](#troubleshooting)). On WSL, a Windows browser does not count: Chrome must be installed inside Linux.

On Windows, use WSL.

## Setup

### The normal way (for your own projects)

Upstream's install command puts Archify into your user-wide skills folder, so it works in every project:

```bash
npx -y skills@1.7.4 add tt-a1i/archify --skill archify -g
```

Drop the `-g` to install it into the current project only (`.claude/skills/archify/`). Then start a new Claude Code session so it picks up the skill.

### The course way (for this tutorial)

So that nothing changes outside this tutorial, the setup script makes a practice copy of the course's deal screener and installs Archify into **that copy only**:

```bash
git clone https://github.com/vasuchettyphd/ai-dev-course.git
cd ai-dev-course/advanced/archify
demo/setup.sh
```

Expected output (about 15 seconds; `/...` stands for wherever you cloned the course):

```
1/4 Copying the deal screener to /.../advanced/archify/demo/practice/deal-screener
2/4 Making it a git repo (Archify cites code by commit)
3/4 Downloading the tested Archify version (only its skill folder, about 18 MB)
4/4 Installing the archify skill into this project only
Archify is ready.

Done. Next:
  cd "/.../advanced/archify/demo/practice/deal-screener"
  export ARCHIFY_UPDATE_CHECK_DISABLED=1   # optional: skip Archify's daily update check
  claude
```

What the script did:

- copied `example-project/` (the deal screener the course builds week by week) into `demo/practice/deal-screener`, leaving out `.env` files with secrets but keeping the `.env.example` template,
- made it a git repo with one commit, because Archify pins every citation to a commit,
- gave it a **placeholder** remote address, `https://example.com/deal-screener.git` (`example.com` is reserved for examples). Archify only attaches source citations when a repo has a remote. Nothing is ever pushed there.
- downloaded only the `archify/` skill folder from upstream commit `25cf370`, the one we tested (not the whole 900 MB repo),
- ran `npx skills@1.7.4 add` on that folder without `-g`, so the skill landed in `demo/practice/deal-screener/.claude/skills/archify/`,
- ran Archify's own health check, `doctor`, whose last line is `Archify is ready.`

`demo/practice/` is ignored by git, so you can't commit it by mistake.

**Optional: turn off the update check.** Once a day Archify fetches a small file from `tt-a1i.github.io` to see if a newer version exists (see [Limits and caveats](#limits-and-caveats)). We turned it off for our runs. To do the same, run this in the terminal where you will start `claude`:

```bash
export ARCHIFY_UPDATE_CHECK_DISABLED=1
```

Want to see the full health check? From the practice folder:

```bash
node .claude/skills/archify/bin/archify.mjs doctor
```

```
[ok] Node.js v22.23.3 (requires >=18)
[ok] Core template
[ok] Example renderer
...
[ok] architecture renderer, schema, and example
[ok] workflow renderer, schema, and example
[ok] sequence renderer, schema, and example
...
[ok] Explainer runtime and reader assets

Archify is ready.
```

## Step 1: an architecture diagram of the deal screener

Go into the practice copy and start Claude Code:

```bash
cd demo/practice/deal-screener
claude
```

Type:

```
Use Archify to draw an architecture diagram of this repository, the rental deal screener. Show the main parts: the program you run, the calculator, the buy-box check, the optional Claude listing step, the agent, the MCP server and the notes search. Cite the source lines for each part. The git remote is a placeholder, so use local-only source links.
```

Claude will ask permission to run `node` and `git` commands and to write files. Say yes. Behind the scenes it:

1. reads Archify's instructions and an example,
2. runs `git rev-parse HEAD` to pin the commit,
3. reads the deal screener's code, writing down file names and line numbers as it goes,
4. writes `candidate.json` in a new folder under `.archify/`,
5. runs Archify's `finalize` command, which checks the JSON, builds the HTML, checks the citations against the commit, and opens the page in a hidden browser to check the layout.

In our run this took 2 minutes and 25 turns. Claude's reply:

```
Here is the diagram: Rental Deal Screener architecture
(/.../deal-screener/.archify/architecture-deal-screener-20261022-120000/deal-screener.html).
The automated checks passed. I didn't look at it myself.

The core path (program → calculator → buy-box check) needs no network. The listing
step, agent and notes search are the optional parts that call Claude. The agent and
the MCP server share one `screen_listing` tool, and that tool calls the same
calculator and buy-box check.

- Source links: Each part cites its source lines on its node. I pinned commit
  `8661edc` and set `link_mode: "local-only"`, so the placeholder GitHub remote
  isn't linked.
- Entry points: The agent, notes search and MCP server each start from their own
  command, not from the main program. I left out `evaluate.py`.
- Where the files are: The candidate JSON and receipts are in the same `.archify/`
  folder as the HTML.
- Stray folder: My first attempt ran from the wrong directory and left a failed
  receipt in `dealscreener/.archify/`. It's safe to delete.
```

Open the HTML file it names in your browser. On WSL, from the practice folder: `explorer.exe .archify` and double-click the file. Or open [`sample-output/1-architecture-deal-screener.html`](sample-output/1-architecture-deal-screener.html), which is the file from this run.

Our diagram has 13 boxes and 14 arrows: Investor → Program you run → Calculator → Buy-box check along the top; the optional Listing step and Claude API down the left; the agent, the `screen_listing` tool, the MCP server and the Claude Code app that starts it on the right; notes search, Google embeddings and the notes files at the bottom.

**Try the controls** at the top right of the page:

- the sun/moon switch flips between light and dark (keyboard: `T`),
- **Classic** opens the visual styles: Classic, Signal Flow, Blueprint, Editorial (keyboard: `S` cycles them),
- **Still / Live** turns the moving dots on the arrows on and off,
- **Export** saves a PNG, JPEG or SVG (light, dark or auto), copies a PNG to the clipboard, or records a 6-second motion clip,
- **ROUTE** at the bottom right traces the path between two boxes, and **LENS** picks one kind of box from the legend (Backend, Database, Cloud...) and highlights every arrow that touches it.

**Check the citations.** Open [`sample-output/1-architecture-deal-screener.json`](sample-output/1-architecture-deal-screener.json), the JSON Claude wrote. Every box from the code has a `sources` list, for example:

```json
{ "id": "tools", "label": "screen_listing tool", ...
  "sources": [ { "path": "dealscreener/tools.py", "line": 70, "end_line": 82 },
               { "path": "dealscreener/tools.py", "line": 125, "end_line": 140 } ] }
```

Line 125 of `example-project/dealscreener/tools.py` is `def screen_listing(raw: dict) -> dict:`. Archify checked every one of these ranges against the committed file before it let Claude hand over the diagram.

## Step 2: a sequence diagram of one user action

An architecture diagram shows the parts. A sequence diagram shows what happens, in order, when someone does one thing. Still in the same Claude Code session (or a new one), type:

```
Use Archify to draw a sequence diagram of one user action in this repo: running 'python3 -m dealscreener --listing', pasting a listing, letting Claude read its numbers, confirming them, and getting the PASS or FAIL verdict. Trace it from the code and cite the source lines. The git remote is a placeholder, so use local-only source links.
```

In our run: 1 minute, 14 turns. Claude's reply:

```
Created dealscreener --listing: pasted listing to PASS/FAIL
(/.../deal-screener/.archify/sequence-listing-verdict-20261022-120000/listing-verdict.html).

The model is only used to read the five property numbers. It is called once and
never retried (`extract.py:126-134`). The loan questions, the math and the PASS or
FAIL verdict never go through it. Overall is PASS only if both buy-box rules pass
(`buybox.py:32-34`).

- Source links: They are local-only and pinned to commit `8661edc`, since the remote
  is a placeholder. Each participant carries its file and line ranges, and the cards
  repeat the key ones.
- Left out of the main flow:
  - an empty, oversized or failed listing read, after which you type every number
    yourself;
  - the loop that re-asks the loan questions when cash invested is $0.

  Both appear in a card.
- Checks: Automated checks passed. I haven't looked at the rendered page.
```

The diagram ([`sample-output/2-sequence-listing-verdict.html`](sample-output/2-sequence-listing-verdict.html)) has six columns, User, `__main__`, `extract`, Claude Haiku 5.5, `calculator` and `buybox`, and 17 arrows between them, grouped into "Paste and read", "Confirm" and "Verdict".

Check one of its claims yourself. Lines 32-34 of `example-project/dealscreener/buybox.py`:

```python
def passes(rule_results: list) -> bool:
    """A deal passes only if every rule passes."""
    return all(rule.passed for rule in rule_results)
```

## Step 3: a diagram from an idea, with no code

Archify does not need a repo. [`demo/startup-idea.md`](demo/startup-idea.md) describes **ShelfSwap**, a made-up app for UVU students to sell used textbooks to each other, in eight plain-English steps. Type:

```
Use Archify to draw a workflow diagram of the startup idea described in ../../startup-idea.md. It has nothing to do with the code in this folder, so don't read the repo. Show the approval gates and the 7-day refund branch.
```

Claude will ask permission to read a file outside the project folder. Say yes. (Or paste the eight steps straight into the prompt instead of the file name.)

In our run: 1 minute, 12 turns. Claude's reply:

```
Created ShelfSwap workflow
(/.../deal-screener/.archify/workflow-shelfswap-20261022-120000/shelfswap-workflow.html).

- Approval gates: Gate 1 is the seller accepting or editing the 40% price before the
  listing goes live. Gate 2 is the buyer's hand-off scan, which has to happen before
  the seller is paid.
- Refund branch: If nobody confirms within 7 days, the held funds go back to the
  buyer in full and the listing goes live again.

Automated checks passed; I haven't looked at the diagram visually.
```

Our diagram puts each step in a lane for who does it: Seller, Buyer, the ShelfSwap app, and a separate dashed "Held money" lane where the money waits until the hand-off scan, then goes either to "Pay seller, minus 10% fee" or to "Full refund" and back to "Listing live".

We kept only the JSON for this one, [`sample-output/3-workflow-shelfswap.json`](sample-output/3-workflow-shelfswap.json), because each HTML file is about 0.8 MB and mostly the same viewer code. To turn it into the diagram on your own computer, with no Claude and no cost, run this from `demo/practice/deal-screener`:

```bash
node .claude/skills/archify/bin/archify.mjs render workflow ../../../sample-output/3-workflow-shelfswap.json ../3-workflow-shelfswap.html
```

It prints the path of the new file, `demo/practice/3-workflow-shelfswap.html`. Open it in your browser. (This works for Step 3 because that diagram cites no code. Steps 1 and 2 cite our exact commit, which your copy doesn't have, so their HTML files are kept in `sample-output/`.)

Now do it for **your** idea. Edit `demo/startup-idea.md` (or write your own steps in the prompt) and ask for whichever type fits: a workflow for "how it works", a sequence for "what happens when a customer pays", a lifecycle for "the states an order goes through". This is a quick way to get a picture for a pitch slide, and to spot steps you haven't decided yet: if Claude asks you a question, that is a gap in your plan.

## What to notice

- **Claude wrote JSON, not a picture.** The boxes, arrows and citations live in a small JSON file (4-6 KB). Archify's program draws it. That is why the layouts look consistent and why the checks can be strict.
- **The checks are real, but they are not your eyes.** Every reply said some version of "automated checks passed, not visually reviewed". The checks catch broken JSON, made-up line numbers, overlapping text and labels too small to read. They can't tell whether the diagram tells the right story. That's your job.
- **Reading code is where it shines.** Both code diagrams said true things we could check line by line, and both said what they left out (`evaluate.py`, the error paths). A plain "explain this repo" answer rarely tells you what it skipped.
- **The diagram is only as current as the commit.** Citations are pinned to one commit. Change the code and the old diagram still points at the old lines.
- **Iterate in plain English.** Upstream suggests follow-ups like "Add authentication", "Highlight the cache-miss path" or "Switch to the light theme". Each follow-up is another paid turn.

## What it cost

| Run | Turns | Time | Cost (Sonnet) |
|---|---|---|---|
| Step 1, architecture, with citations | 25 | 2 min | $0.44 |
| Step 2, sequence | 14 | 1 min | $0.26 |
| Step 3, workflow from the description | 12 | 1 min | $0.20 |
| **The three steps** | | | **$0.90** |

While writing this tutorial we also ran Step 1 twice more while working out the setup ($0.34 and $0.36), so the whole session cost about $1.60. On a Claude subscription these come out of your usage allowance instead.

## Limits and caveats

- **Citations need a git repo with a commit and a remote.** Our first try had no remote, and Claude said: "Archify only attaches per-part source links when the repo has a git remote. This one has none, so every part shows its file path in its label." That is why `setup.sh` adds a placeholder remote. On your own project, once it's on GitHub, Archify can link each box to the real file on GitHub.
- **Uncommitted changes are not evidence.** Archify checks citations against the committed files. Commit first, then diagram.
- **Each diagram file is about 0.8 MB**, because the whole viewer is built into it. That is what makes it work offline as a single file.
- **It checks for updates.** Once a day, `finalize` fetches a small file from `tt-a1i.github.io` to see if a newer Archify exists, and Claude may mention it. It never updates itself. Turn this off with `export ARCHIFY_UPDATE_CHECK_DISABLED=1` before starting `claude` (see [Setup](#setup)).
- **The "explainer" offer edits a global file if you say yes.** After making an explainer page, the skill may offer to make pages proactively from now on. If you accept, it adds a line to `~/.claude/CLAUDE.md`, which affects every project. Delete that line to undo it.
- **The installer reports installs.** The `skills` installer sends an anonymous install event unless `DO_NOT_TRACK=1` is set. `setup.sh` sets it. The installer also showed a third-party safety summary: "Gen: Safe, Socket: 1 alert, Snyk: Low Risk" ([details](https://skills.sh/tt-a1i/archify)).
- **We read the code before running it.** The skill's programs start a hidden browser for the check and run read-only `git` commands to verify citations. Apart from the update check, they only go online if you ask for a company logo and give a web address for it, and the optional live preview runs a small web server on your own computer only (`127.0.0.1`). We found nothing that sends your code anywhere. The skill runs with Claude Code's permissions, though, so treat it like any other software you install.
- **Don't clone the upstream repo to look at it.** It is about 900 MB (videos, a website, galleries). Read it on GitHub instead. `setup.sh` downloads only the `archify/` skill folder (18 MB) from the tested commit, which took a few seconds for us.
- **The sample HTML files were edited once.** Archify's built-in viewer code contains the long dash character in its code comments, which this course's checker forbids. We replaced those characters with a hyphen in `sample-output/*.html`. We also set the placeholder remote in `sample-output/` to `example.com/deal-screener.git` to match `setup.sh`. The diagrams render the same, and Archify's `check` command still passes on them.

## Troubleshooting

**The reply says "the final browser-rendering check failed" with `write EPIPE`.** Archify could not start a working browser. The diagram file was still written; only the last check failed. This is what happened on our first try, on WSL with no Chrome inside Linux. Fixes:

- Install Chrome inside Linux or WSL: `wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo apt install ./google-chrome-stable_current_amd64.deb`
- Or point Archify at a browser you already have: `export ARCHIFY_CHROME=/path/to/chrome`, then start `claude` from that same terminal.

Then ask Claude to "run Archify's finalize again on that diagram".

**Claude answers in text and makes no diagram.** Start the prompt with "Use Archify to ...". If it still doesn't, type `/` in Claude Code and look for `archify`. If it's missing, you started `claude` in a different folder from the one the skill was installed in, or before the install finished. Quit and start it again in `demo/practice/deal-screener`.

**`demo/setup.sh` says the folder already exists.** You ran it before. Delete the old copy with `rm -rf demo/practice` and run it again.

**`npx: command not found` or `Node.js 22.20 or later is needed`.** Install Node.js 22 LTS or newer from [nodejs.org](https://nodejs.org), open a new terminal and check `node --version`.

**Claude left a `.archify` folder somewhere odd**, such as `dealscreener/.archify/` in our Step 1. It's a failed attempt. Delete it.

**The folder name has a strange time in it**, like `-120000`. Claude picks that timestamp itself. It doesn't matter.

## Clean up

Delete the practice copy, which also removes the skill installed inside it. From the `advanced/archify` folder (if you are still in `demo/practice/deal-screener`, run `cd ../../..` first):

```bash
rm -rf demo/practice
```

If you installed Archify for your whole account with `-g`, remove it with:

```bash
npx -y skills@1.7.4 remove archify -g
```

Without `-g`, run the same command inside the project to remove a project-only install. If you had turned on the explainer mode, also delete its `[archify explainer: ...]` line from `~/.claude/CLAUDE.md`.

## Files

| Path | What it is |
|---|---|
| `.gitignore` | Keeps `demo/practice/` and Archify's working files out of git |
| `demo/setup.sh` | Copies the deal screener to `demo/practice/deal-screener`, makes it a git repo, installs the tested Archify commit into it only |
| `demo/startup-idea.md` | ShelfSwap, the made-up startup for Step 3 |
| `sample-output/1-architecture-deal-screener.html` and `.json` | Step 1's diagram, and the JSON Claude wrote for it |
| `sample-output/2-sequence-listing-verdict.html` and `.json` | Step 2's diagram and JSON |
| `sample-output/3-workflow-shelfswap.json` | Step 3's JSON (render it to HTML with the command in Step 3) |

## Where to read more

- Archify on GitHub: https://github.com/tt-a1i/archify
- Live examples: https://archify.si/gallery.html
- Claude Code skills in general: https://code.claude.com/docs/en/skills
