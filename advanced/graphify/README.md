# Graphify: turn a project into a map Claude can query

A hands-on tour of [graphify](https://github.com/Graphify-Labs/graphify), a Claude Code skill that reads a folder of code and documents and builds a **knowledge graph**: every function, class, note and idea becomes a dot, and every "calls", "imports" or "is about" becomes a line between two dots. You will run it on the course's rental deal screener (the [example project](../../example-project/)), look at the map it draws, and then ask Claude questions that it answers from the map instead of reading every file.

Everything here was run for real on **2026-10-22** with:

- **graphify 0.9.94** (PyPI package `graphifyy`, upstream commit `c588b72`)
- **Claude Code 2.1.309**, model **Sonnet**
- uv 0.13.4, Python 3.12 (inside the demo's own environment), Ubuntu on WSL2

Output quoted below is real output from those runs. Long blocks are trimmed where you see `...`, and folder paths are shortened to where they would be on your machine.

**Time:** 20-45 minutes. **Cost:** about $0.50 of model usage to build the graph, then $0.07-0.11 per question. The whole demo cost us about $0.80. Code is read for free; only the documents cost tokens.

## The idea in one paragraph

When you ask Claude "what breaks if I change X?", it normally searches the files, reads a few, searches again, and pieces the answer together. That works, but every session starts from zero. Graphify does the reading once and saves the result as a graph in a folder called `graphify-out/`. Code is parsed by a normal program (no AI, no cost, nothing leaves your machine). Documents such as plans, notes and listings are read by Claude helpers, which pull out the ideas and how they relate. After that, Claude can run `graphify query "..."` and get back just the handful of functions, tests and notes that matter, with the file and line for each. You also get a picture of the whole project (`graph.html`) and a one-page summary (`GRAPH_REPORT.md`).

## Who made it

Graphify was started by Safi Shamsi and is now maintained by Graphify Labs. It is open source: the repository ships both an Apache 2.0 and an MIT licence file (PyPI lists Apache 2.0). You may see the old address `github.com/safishamsi/graphify`: it redirects to [github.com/Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify), which is the official repository. The Python package is called **`graphifyy`, with two y's**. Other `graphify` packages on PyPI are not from the same people, so check the spelling.

The project also sells a hosted version (Graphify Cloud). You don't need it for anything in this lesson.

## Is it a skill?

Yes, plus a command-line tool. It has two parts:

| Part | What it is | What it does |
|---|---|---|
| `graphify` CLI | A Python program | Parses code, builds the graph, answers `query`, `path` and `explain` |
| `/graphify` skill | A `SKILL.md` file for Claude Code | Tells Claude how to run the whole build, including sending documents to helper agents |

Installing it in a project also adds two small things you should know about (see [What the install changes](#what-the-install-changes)): a rule in `CLAUDE.md` that says "ask the graph first", and a hook that reminds Claude about the graph before it searches or reads files.

## Setup

You need git, [uv](https://docs.astral.sh/uv/getting-started/installation/) and [Claude Code](https://claude.com/claude-code). On Windows, use WSL. Check them:

```bash
git --version          # git version 2.x
uv --version           # uv 0.13.4 (or newer)
claude --version       # 2.1.309 (Claude Code) (or newer)
```

### Before you start: Google keys

If `GEMINI_API_KEY` or `GOOGLE_API_KEY` is set in your terminal, the `/graphify` skill is written to send your **documents** to Google Gemini for the document-reading step instead of using Claude. In our run a Gemini key was set, but the needed package wasn't installed, so Claude fell back to its own helper and said so. Check before you run anything:

```bash
env | grep -E '^(GEMINI|GOOGLE)_API_KEY='    # prints nothing if neither is set
```

If it prints a line and you don't want your documents sent to Google, run this in the same terminal before setup and before starting Claude:

```bash
unset GEMINI_API_KEY GOOGLE_API_KEY
```

`demo/setup.sh` also prints a warning with that line if either key is set. Your code is never sent to Google either way: graphify parses code on your machine. But like any Claude Code session, whatever Claude reads (code or documents) is sent to Anthropic as usual.

### The normal install (what upstream recommends)

On your own projects, upstream's two commands are:

```bash
uv tool install graphifyy      # installs the graphify command for your user
graphify install               # adds the /graphify skill to ~/.claude for every project
```

If your terminal then says `graphify: command not found`, run `uv tool update-shell` and open a new terminal.

That changes your global Claude Code setup (`~/.claude/skills/graphify/` and `~/.claude/CLAUDE.md`). For this lesson we don't do that.

### The lesson install (nothing global)

The demo script keeps everything inside this lesson's folder:

```bash
git clone https://github.com/vasuchettyphd/ai-dev-course.git
cd ai-dev-course/advanced/graphify
demo/setup.sh
```

It does three things:

1. Installs graphify 0.9.94 into `demo/.venv` (a private Python environment, nothing system-wide).
2. Copies the deal screener from `example-project/` into `demo/practice/deal-screener` and makes it its own git repository.
3. Runs `graphify install --project` there, so the skill exists in that one copy only.

It skips any `.env` files in the example project (secrets), keeping only the `.env.example` template. If you rerun it, it reuses `demo/.venv`, so you only need to delete the practice folder (see [Troubleshooting](#troubleshooting)).

Expected output (trimmed; if a Google key is set, a `WARNING` comes first):

```
==> Installing graphify 0.9.94 into .../advanced/graphify/demo/.venv
graphify 0.9.94
==> Copying the deal screener into .../advanced/graphify/demo/practice/deal-screener
==> Installing the /graphify skill into this project only
  references       ->  .claude/skills/graphify/references
  skill installed  ->  .claude/skills/graphify/SKILL.md
  CLAUDE.md        ->  created at .claude/CLAUDE.md
...
graphify section written to .../demo/practice/deal-screener/CLAUDE.md
  .claude/settings.json  ->  PreToolUse hooks registered (Bash|Grep search + Read/Glob)

Claude Code will now check the knowledge graph before answering
codebase questions and rebuild it after code changes.
...
Ready. Next:
  export PATH=".../advanced/graphify/demo/.venv/bin:$PATH"
  cd ".../advanced/graphify/demo/practice/deal-screener"
  claude
```

Run the `export` line in **every new terminal** before starting Claude, so Claude can find the `graphify` command.

The script also copies [demo/graphifyignore](demo/graphifyignore) into the project as `.graphifyignore`. It works like `.gitignore`: it tells graphify to skip the long tutorial write-ups, the eval fixtures and the Claude Code setup files. That keeps the build to 38 files and about $0.50. Without it, graphify also maps its own skill files and the reviewer agents, which is noise.

### What the install changes

Open these after setup so you know what was added:

| File | What it says |
|---|---|
| `.claude/skills/graphify/SKILL.md` | The skill itself, about 800 lines of step-by-step instructions for Claude |
| `.claude/CLAUDE.md` | "When the user types `/graphify`, use the installed graphify skill" |
| `CLAUDE.md` | "When `graphify-out/graph.json` exists, run `graphify query` before your first grep, search or file read" |
| `.claude/settings.json` | Two `PreToolUse` hooks that run `graphify hook-guard` before Claude searches or reads files. They only add a reminder; they never block anything unless you opt in to strict mode |

## Demo, step 1: build the graph

```bash
export PATH="$PWD/demo/.venv/bin:$PATH"
cd demo/practice/deal-screener
claude
```

In Claude Code, type:

```
/graphify .
```

Claude asks permission to run several `python -c` commands and to start one helper agent. Approve them. In our run it took about **2 minutes** and cost **$0.49**. What happens behind the scenes:

1. **Detect.** Graphify lists the files it will read: 25 code files and 13 documents (`PLAN.md`, `BUGS.md`, the landlord notes, the two listings, `requirements.txt`).
2. **Parse the code.** A parser (tree-sitter) reads every Python file and records functions, classes, calls and imports. No AI, no cost.
3. **Read the documents.** One helper agent reads the 13 documents and writes down the ideas in them ("Repairs reserve (8% of rent)", "Bug 1: Interest rate 0.07 read as 0.07%") and how they relate.
4. **Cluster.** Graphify groups dots that are tightly linked into "communities", and Claude gives each group a short name.
5. **Write the outputs** into `graphify-out/`.

Claude's summary at the end (trimmed):

```
Graph complete. Outputs are in .../deal-screener/graphify-out/:

- graph.html: interactive graph, open it in a browser
- GRAPH_REPORT.md: audit report
- graph.json: raw graph data

The graph has 641 nodes, 1,427 edges and 28 communities.

- Code: 25 files went through AST extraction, 588 nodes.
- Docs: 13 files went through a subagent, 34 nodes.
- Coverage: every doc was read to its last line.
- Graph health warning: 112 edges point at endpoints that aren't in the graph,
  and 21 edges were merged because they share the same two endpoints.
  The graph is still usable.

God nodes (most connected):
1. FakeClient: 38 edges
2. analyse(): 26
3. run_with(): 26
...

Suggested questions:
- Why does analyse() connect Deal Calculator to Buy Box Rules and Screening Tool Input?
...
The most interesting question is why analyse() bridges Deal Calculator,
Buy Box Rules and Screening Tool Input. Want me to trace it?
```

Your numbers will be close to these but not identical: the document reading is done by a model, so the exact ideas it pulls out vary a little between runs.

**If you don't want to run it,** open [sample-output/GRAPH_REPORT.md](sample-output/GRAPH_REPORT.md) and [sample-output/graph.html](sample-output/graph.html) from our run. (We swapped four em dashes in those two files for plain dashes to pass the course style check. Nothing else was changed.)

## Demo, step 2: look at the map

Open the picture in your browser. Use the line for your system:

```bash
explorer.exe graphify-out/graph.html     # Windows (WSL)
open graphify-out/graph.html             # macOS
xdg-open graphify-out/graph.html         # Linux
```

You need an internet connection the first time, because the page loads its drawing library (vis-network 9.1.6) from unpkg.com. Things to try:

- Each colour is a community. The legend shows the names Claude gave them, such as **Deal Calculator**, **Buy Box Rules**, **Listing Extraction** and **Docs Bugs and Notes**.
- Click a dot to see what it connects to. Click `analyse()`: it sits between the calculator, the buy-box rules and the screening tool, which is why the report calls it a "bridge".
- Search for `Repairs reserve`. You will find it twice: once from `PLAN.md` and once from `notes/repairs-reserve-rule.md`.

Then open `graphify-out/GRAPH_REPORT.md`. The first lines are worth reading closely:

```
## Corpus Check
- Corpus is ~19,679 words - fits in a single context window. You may not need a graph.

## Summary
- 641 nodes · 1427 edges · 28 communities (21 shown, 7 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.87)
- Token cost: 40,340 input · 0 output
```

Graphify is telling you, honestly, that this project is small enough that Claude could read all of it at once. Keep that in mind for step 5.

Every line in the graph is labelled:

| Label | Meaning |
|---|---|
| `EXTRACTED` | Read directly from the source, for example "`run()` calls `analyse()` on line 54" |
| `INFERRED` | Graphify or the helper agent worked it out, with a confidence score |
| `AMBIGUOUS` | The helper wasn't sure. The report lists these under "Review These" |

Our run had exactly one `AMBIGUOUS` line: it linked the condo in `listings/messy-listing.txt` to the Riverside association dues note, even though the listing never says the condo is in Riverside. That's the kind of guess you should check.

## Demo, step 3: ask the graph directly (free)

You can query the graph yourself without Claude. These commands cost nothing. Exit Claude (or open a second terminal, run the `export` line, and `cd` into `demo/practice/deal-screener`):

```bash
graphify explain "analyse()"
```

```
Node: analyse()
  ID:        dealscreener_calculator_analyse
  Source:    dealscreener/calculator.py L50
  Type:      code
  Community: Deal Calculator
  Degree:    26

Connections (26):
  <-- __main__.py [imports] [EXTRACTED] dealscreener/__main__.py:L13
  <-- tools.py [imports] [EXTRACTED] dealscreener/tools.py:L19
  ...
  <-- run() [calls] [EXTRACTED] dealscreener/__main__.py:L54
  <-- screen_listing() [calls] [EXTRACTED] dealscreener/tools.py:L129
  --> Assumptions [references] [EXTRACTED] dealscreener/calculator.py:L50
  --> Listing [references] [EXTRACTED] dealscreener/calculator.py:L50
  --> _check_inputs() [calls] [EXTRACTED] dealscreener/calculator.py:L52
  --> monthly_mortgage_payment() [calls] [EXTRACTED] dealscreener/calculator.py:L69
  ...
  ... and 6 more (--all lists all 26)
```

```bash
graphify path "parse_answer()" "analyse()"
```

```
Shortest path (2 hops):
  parse_answer() <--contains [EXTRACTED]-- __main__.py --imports [EXTRACTED]--> analyse()
```

```bash
graphify query "how is the repairs reserve used in cash flow" --budget 600
```

```
Graph: graphify-out/graph.json (641 nodes) | Traversal: BFS depth=2 | Start: ['Repairs reserve rule of thumb (8% / 10%)', 'Repairs reserve (8% of rent)', 'Cash-on-cash return', 'Monthly cash flow'] | 22 nodes found

[!] TRUNCATED: showing 18 of 22 nodes (~600-token budget). ...

NODE Repairs reserve rule of thumb (8% / 10%) [src=notes/repairs-reserve-rule.md loc=None community=Docs Bugs and Notes]
NODE Repairs reserve (8% of rent) [src=PLAN.md loc=None community=Docs Bugs and Notes]
NODE Cash-on-cash return [src=PLAN.md loc=None community=Docs Bugs and Notes]
NODE Monthly cash flow [src=PLAN.md loc=None community=Docs Bugs and Notes]
NODE Listing B decision write-up [src=notes/listing-b-write-up.md loc=None community=Docs Bugs and Notes]
...
```

Notice that every result in that last answer comes from a document, none from the code. Now try to connect a note to the code:

```bash
graphify path "Riverside condo association dues" "analyse()" --undirected
```

```
No path found between 'Riverside condo association dues' and 'analyse()'.
```

In our graph, the documents and the code are two separate islands. The helper agent found an idea called "Repairs reserve (8% of rent)" in `PLAN.md`, but nothing links it to line 63 of `calculator.py`, where the reserve is actually worked out. Keep this in mind when you read Claude's answers.

## Demo, step 4: ask Claude questions that use the graph

Start Claude again in `demo/practice/deal-screener` and ask these one at a time. Because of the rule in `CLAUDE.md`, Claude's **first** move for each question in our runs was `graphify query`, before any search or file read. Watch for it.

**Question 1:**

> How does a listing get from a text file to a pass or fail verdict? Name the functions in order.

Claude ran one `graphify query`, then read three files to confirm. Cost $0.07. Its answer (trimmed):

```
1. run() (dealscreener/__main__.py:36) is the entry point. With use_listing=True it calls listing_step() first.
2. listing_step() (__main__.py:80) reads the pasted text line by line until a line that says done.
3. extract_listing() (dealscreener/extract.py:126) sends the text to the model and asks for
   five property numbers as JSON. ... usable_number() (extract.py:157) then turns each value
   into a finite float of 0 or more, or None.
4. ask_with_default() (called from run()) asks each property question and shows the extracted number ...
5. analyse(Listing(**answers)) (dealscreener/calculator.py:50) builds a Listing and returns the results ...
6. check(results) (dealscreener/buybox.py:24) returns one RuleResult per rule ...
7. passes(rule_results) (buybox.py:32) returns all(rule.passed ...). run() prints that as
   Overall: PASS or Overall: FAIL.
```

**Question 2:**

> If I change how the repairs reserve is calculated, which functions and tests would be affected?

Claude ran two `graphify query` commands, one search and one file read. Cost $0.11. It found the formula on `calculator.py:63`, the default of 8.0 on line 28, the callers (`run()`, `screen_listing()`, the MCP server and the agent), and the tests in `test_calculator.py` and `test_tools.py` that would break. It also said honestly which files it had *not* opened:

```
I only read calculator.py. The test and caller details come from the graph and a grep,
so check test_main.py and evaluate.py before relying on them.

After you change the code, run graphify update . to refresh the graph.
```

**Question 3:**

> Which of the landlord notes in notes/ matter for the buy-box decision, and is that link in the code or only in the docs?

Claude ran one `graphify query`, then read all the notes and `buybox.py`. Cost $0.07. Its main finding was right and useful:

```
Only some of the notes affect the buy-box decision, and the link between them and the code
exists only in the docs. The code never reads the notes.
```

But it also said this, which is **wrong**:

```
riverside-association-dues.md is relevant only for Riverside condos.
calculator.py has no association-dues input at all.
```

`calculator.py` has a `monthly_hoa` field on line 16 and adds it to the operating costs on line 66. HOA fees *are* association dues. The graph doesn't link the dues note to `monthly_hoa` (the two islands again), and Claude didn't open `calculator.py` for this question. The graph narrowed where Claude looked, and the answer was only as good as that narrowing. Always check a claim like this before you act on it.

## Demo, step 5: was the graph worth it here?

We asked question 2 again in a plain copy of the project with no graph, using the same model.

| | With the graph | Without the graph |
|---|---|---|
| Tool calls | 4 (2 graph queries, 1 search, 1 read) | 9 (7 searches, 2 reads) |
| Cost | $0.11 | $0.11 |
| Found the formula, default and callers | Yes | Yes |
| Tests listed | `test_calculator.py`, `test_tools.py`; flagged `test_main.py` as unchecked | Those two, plus exact lines in `test_main.py`, `test_mcp_server.py` and `test_agent.py` |

On a project this small, the graph made Claude's search shorter but didn't make the answer better or cheaper, and the plain run actually listed more affected tests. The report warned us: "fits in a single context window. You may not need a graph." Graphify pays off on projects too big for Claude to skim: hundreds of files, or a mix of code, PDFs and meeting notes where nobody remembers how things connect. One run of each, so treat this as an anecdote, not a benchmark.

## Demo, step 6 (optional): keep the graph fresh for free

When code changes, the graph goes out of date. Updating the code part costs nothing because no AI is involved. Add a small function to `dealscreener/buybox.py`:

```python
def verdict_word(rule_results):
    """Return 'BUY' or 'PASS ON IT' for the overall verdict."""
    return "BUY" if passes(rule_results) else "PASS ON IT"
```

Then:

```bash
graphify update .
```

```
Re-extracting code files in . (no LLM needed)...
[graphify watch] 1 file(s) not classified (no supported extension or shebang), skipped: .graphifyignore
[graphify] backed up curated graph (5 files) -> 2026-10-22/
[graphify watch] Rebuilt: 643 nodes, 1430 edges, 28 communities
[graphify watch] graph.json, graph.html and GRAPH_REPORT.md updated in graphify-out
Code graph updated. For doc/paper/image changes run /graphify --update in your AI assistant.
```

It took under a second. `graphify explain "verdict_word()"` now shows the new function calling `passes()`. If you change a document instead, run `/graphify . --update` inside Claude, which re-reads only the changed documents (and costs tokens again). Undo the change with `git checkout dealscreener/buybox.py`.

## What to notice

- **Code is mapped for free and exactly.** Every `calls` and `imports` line comes with a file and line number you can check.
- **Documents cost tokens and are fuzzier.** The ideas pulled from `PLAN.md` and the notes are useful, but in our run they formed an island with almost no links into the code.
- **The labels matter.** `EXTRACTED` is a fact from the file. `INFERRED` and `AMBIGUOUS` are guesses, and the report lists them so you can review them.
- **Claude used the graph first, every time,** because of the `CLAUDE.md` rule the install added. That's the "always-on" part: you don't have to remember to ask for it.
- **The graph narrows where Claude looks.** That saves tool calls, but if the graph is missing a link, Claude can miss it too (question 3).
- **The report tells you when you don't need it.** Read the "Corpus Check" line before deciding a graph is worth building.

## Limits and caveats

- **Documents can be sent to Google.** See [Before you start: Google keys](#before-you-start-google-keys) in Setup. Unset those keys before you build a graph if you don't want that.
- **The skill may use a newer graphify than you installed.** Its first step runs `uv tool run --from graphifyy python`, which fetches the latest `graphifyy` from PyPI into uv's cache and uses that for the build. On 2026-10-22 the latest was 0.9.94, the same as our pinned version. Later, the build steps may run a newer release than the `graphify` command in `demo/.venv`.
- **If uv can't find graphify at all, the skill installs it globally.** Step 1 of the skill falls back to `uv tool install --upgrade graphifyy` (or `pip install`). The demo avoids this because `uv tool run` succeeds first, but be aware of it on other machines.
- **Results vary.** Node counts, community names and the ideas pulled from documents change a little between runs, because a model does that part.
- **Health warnings are normal.** Both of our builds reported 112 "dangling" edges (mostly calls to things outside the project, such as Python's own `math` module). The graph still works.
- **`graph.html` needs the internet** to load its drawing library, and it can get slow above a few thousand nodes. Graphify warns you above 5,000.
- **Big projects.** Above 500 files or 2 million words, the skill stops and asks you to pick a subfolder.
- **The hook runs on every search and read.** It's fast (about 0.2 seconds) and has a 10-second limit, but it does run constantly in a project where graphify is installed.
- **Not for secrets.** Graphify skips files that look sensitive and lists them, but don't point it at a folder with `.env` files or private data you wouldn't want an AI to read.

## Troubleshooting

**`graphify: command not found`** (in your terminal or in Claude's output). You forgot the `export PATH=...` line in this terminal. Run it again from `advanced/graphify`: `export PATH="$PWD/demo/.venv/bin:$PATH"`, then restart Claude.

**`/graphify` doesn't appear when you type `/`.** Claude Code was started in the wrong folder. It must be started inside `demo/practice/deal-screener`, where `.claude/skills/graphify/` lives.

**`demo/setup.sh` says the practice folder already exists.** Delete it and run setup again: `rm -rf demo/practice/deal-screener`.

**`uv is not installed`.** Install uv from [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/), open a new terminal, and run setup again.

**`ERROR: refused to shrink graphify-out/graph.json`.** You deleted files and rebuilt, so the new graph is smaller. This is a safety check. If the shrink is what you meant, run `graphify update . --force`.

**The build stops with `Graph is empty`.** Every file was ignored. Check `.graphifyignore` in the project; you may have excluded too much.

**`graph.html` opens blank.** You are offline, or something blocked unpkg.com. Use `graphify explain` and `graphify query` in the terminal instead, or read `GRAPH_REPORT.md`.

**`No path found` between two things you know are related.** The graph doesn't have that link (see step 3). Ask Claude the question anyway; it will fall back to reading files.

## Clean up

Everything the demo made is inside this lesson's folder and ignored by git. From the folder where you cloned the course:

```bash
cd ai-dev-course/advanced/graphify
rm -rf demo/practice demo/.venv
```

Graphify also leaves small caches you can delete if you want: `~/.cache/graphify/` (lock files from installing the skill) and the copy that `uv tool run` downloaded (`uv cache clean graphifyy`).

If you installed graphify the normal way on your own projects, remove it with:

```bash
graphify uninstall             # removes the skill, CLAUDE.md rules and hooks it added
graphify uninstall --purge     # same, and also deletes graphify-out/
uv tool uninstall graphifyy    # removes the graphify command
```

## Files

| Path | What it is |
|---|---|
| `README.md` | This lesson |
| `.gitignore` | Keeps `demo/.venv/`, `demo/practice/` and other generated files out of git |
| `demo/setup.sh` | Installs graphify into `demo/.venv`, copies the deal screener, installs the skill project-only |
| `demo/graphifyignore` | Copied into the practice project as `.graphifyignore` to keep the build small |
| `sample-output/GRAPH_REPORT.md` | The report from our run |
| `sample-output/graph.html` | The interactive map from our run (about 650 KB; open it in a browser) |

## Where to read more

- [graphify on GitHub](https://github.com/Graphify-Labs/graphify): the README, the skill file and the changelog
- [graphifyy on PyPI](https://pypi.org/project/graphifyy/): release history, so you can see what changed since 0.9.94
- [uv documentation](https://docs.astral.sh/uv/): how `uv venv` and `uv tool run` work
