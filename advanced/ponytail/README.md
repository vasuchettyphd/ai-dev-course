# Ponytail: make Claude Code write less code

A hands-on tour of [ponytail](https://github.com/DietrichGebert/ponytail), a free add-on for Claude Code by Dietrich Gebert (MIT license). It tells the agent to act like a lazy senior developer: reuse what the project already has, reach for the standard library before writing anything new, and skip features nobody asked for. You will give the same feature request to two identical copies of a small project, one with ponytail and one without, and count the difference.

Everything here was run for real on 2026-10-22 with **ponytail v5.3.2**, Claude Code 2.1.309 (Sonnet), Python 3.14, git 2.53 and Node 22 on Linux (WSL). The numbers and output quoted below come from those runs. Do not confuse it with `mikrammullah/PonyTail` on GitHub, which is an unrelated project.

**Time:** about 30-40 minutes. **Cost:** each headless run costs about $0.05-0.11 of model usage. Both rounds of the demo (4 runs) come to roughly $0.30. Our full test, 3 repeats of each round, cost about $1.

## The idea in one paragraph

Ask an AI agent for a feature and it tends to over-deliver: an extra helper function here, a config option there, three extra tests, a docstring explaining it all. Each piece looks reasonable, but every line is something you have to read, trust and maintain. Ponytail is one instruction file (a "skill") that puts a checklist in front of the agent before it writes: *Does this need to exist? Is it already in this codebase? Does the standard library do it? Can it be one line?* Only then does it write the minimum code that works. It is not allowed to cut corners on safety: input validation, error handling that prevents data loss, security and anything you explicitly asked for stay in. It also ends every reply with a line or two about what it skipped, so you know what you did not get.

## What we found

Same starter project, same request, same model, run 3 times each. "Lines added" is the `git diff --stat` total, tests included.

| Request | | Without ponytail | With ponytail |
|---|---|---|---|
| **1. Precise:** "add a `by-category` command with an optional `--month`" | Lines added | 50, 48, 51 (avg 50) | 43, 50, 48 (avg 47) |
| | Cost per run | $0.05-0.06 | $0.08-0.11 |
| | Turns | 6-8 | 12-17 |
| **2. Vague:** "I keep overspending. Add budgets so it warns me when I go over." | Lines added | 54, 48, 64 (avg 55) | 35, 41, 42 (avg 39) |
| | Cost per run | $0.07-0.11 | $0.05-0.09 |
| | Turns | 11-21 | 6-8 |

All 12 runs worked: the tests passed and the new command printed the right totals.

**Takeaway:** when the request is precise and the project is small and tidy, ponytail barely changes the code (about 6% fewer lines) and actually costs more, because its "read everything the change touches first" rule makes the agent look around before it writes. When the request is vague, the difference is clear: about 29% fewer lines, fewer turns and lower cost, every time. Ponytail earns its keep where there is room to over-build. The upstream README claims about half the code on its own 39-task benchmark; on this tiny project we saw much less. Three runs per arm is an anecdote, not a benchmark.

## How it is installed normally (read this, then use the demo's project-only install)

Upstream ponytail is a **Claude Code plugin**, not just a skill. The recommended install is two separate prompts inside Claude Code:

```
/plugin marketplace add DietrichGebert/ponytail
```
```
/plugin install ponytail@ponytail
```

Restart Claude Code afterwards. You need Node.js on your PATH, because the plugin runs small Node scripts ("hooks") at set moments. We read all of them before running anything. Here is what the plugin adds on top of the skill file:

- **Always on.** A `SessionStart` hook loads the ponytail rules into every session automatically, and a `SubagentStart` hook passes them on to any helper agents Claude spawns. You do not have to type anything.
- **Level switching.** A `UserPromptSubmit` hook watches for `/ponytail lite`, `/ponytail full` (default), `/ponytail ultra`, and `/ponytail off`, `stop ponytail` or `normal mode` to switch it off.
- **Five extra skills:** `/ponytail-review` (review a change), `/ponytail-audit` (review a whole repo), `/ponytail-debt` (list the `shortcut:` comments it left), `/ponytail-gain` and `/ponytail-help`.
- **Small files outside the project:** a mode flag in `~/.claude/.ponytail-active` and `~/.claude/ponytail-modes/`, and, if you have no status line yet, a copy of its status-line script in `~/.claude/` plus a hint that makes Claude *offer* to add a status line to your `~/.claude/settings.json`. You can say no.
- **"The band"** (new in 5.3): a panel above the prompt showing cost, tokens and tests for the current task. It also writes a per-project CSV and a local `board.html` in `~/.config/ponytail/band/`. Nothing leaves your machine unless you fill in the optional webhook URL in the plugin settings, which is empty by default.

Nothing in the hooks looked suspicious: no downloads, no network calls unless you set the webhook, and the only files written are the ones listed above. Upstream also offers `npx skills add DietrichGebert/ponytail` (the skills CLI), which copies the skills into your project without the hooks. We did not test that route.

**For this demo we skip the plugin** and copy only the main skill file, `SKILL.md`, into one project folder. That keeps the experiment clean (only one copy has ponytail) and leaves your global Claude Code setup untouched. The trade-off: without the hooks it is not always on, so we type `/ponytail` in front of the request to switch it on.

## Setup

You need git, Python 3.10 or newer, curl, and [Claude Code](https://claude.com/claude-code) logged in. On Windows, use WSL.

```bash
git clone https://github.com/vasuchettyphd/ai-dev-course.git
cd ai-dev-course/advanced/ponytail/demo
./setup.sh
```

Expected output (your path will differ):

```
Ready:
  /home/you/ai-dev-course/advanced/ponytail/demo/practice/baseline   (no skill)
  /home/you/ai-dev-course/advanced/ponytail/demo/practice/ponytail   (ponytail v5.3.2 in .claude/skills/ponytail/SKILL.md)
```

`setup.sh` made two identical copies of the starter project in `practice/` (which git ignores), turned each into its own git repo so we can measure changes with `git diff`, and downloaded ponytail's `SKILL.md` (pinned to v5.3.2) into `practice/ponytail/.claude/skills/ponytail/`. A skill in a project's `.claude/skills/` folder is only visible to Claude Code sessions started in that folder.

### The starter project

`demo/starter/` is a 57-line expense tracker, `tracker.py`, with a CSV of 12 expenses and 3 tests. It already has the helpers a good solution should reuse: `load_expenses()` reads the CSV, and `format_money()` prints dollars.

```bash
cd practice/baseline
python3 tracker.py total          # Total: $2,235.05
python3 -m unittest               # Ran 3 tests ... OK
cd ../..
```

### Read the skill before you use it

Always read third-party instructions before you hand them to your agent:

```bash
cat practice/ponytail/.claude/skills/ponytail/SKILL.md
```

It is about 50 lines of plain English. The core is a six-step ladder ("Does it need to exist? Already in this codebase? Standard library? Installed dependency? One line? Otherwise the minimum code that works") and a "Never cut" list.

## Demo round 1: a precise request

The request is in `requests/1-by-category.txt`:

> Add a `by-category` command to tracker.py. It prints how much was spent in each category, biggest first. It takes an optional --month YYYY-MM so I can see just one month. Add tests to test_tracker.py and run them when you are done.

Run it against both copies. The script runs Claude Code headless (`claude -p`) in each folder, one after the other. The ponytail copy gets `/ponytail ` in front of the same request.

```bash
./run-both.sh
```

Expected output, after about a minute (your numbers will vary a little):

```
baseline: $0.06, 8 turns, 20s
ponytail: $0.08, 13 turns, 25s
```

Two flags in `run-both.sh` are worth knowing. `--permission-mode acceptEdits` lets Claude edit files without asking, which is fine in a throwaway practice copy. `--setting-sources project` makes Claude ignore your own plugins and hooks for this run, so ponytail is the only difference between the two copies.

**Prefer to watch it work?** Open Claude Code yourself instead: `cd practice/baseline && claude`, paste the request, then quit; then `cd ../ponytail && claude`, type `/ponytail` followed by a space and the same request. The results are the same kind of thing, just interactive.

Now compare:

```bash
./compare.sh
```

Real output from our run (trimmed to the interesting lines; the full version is in [sample-output/by-category-compare.txt](sample-output/by-category-compare.txt)):

```
=================== baseline ===================
 test_tracker.py | 28 +++++++++++++++++++++++++++-
 tracker.py      | 24 +++++++++++++++++++++++-
 2 files changed, 50 insertions(+), 2 deletions(-)
Ran 7 tests in 0.003s
OK
--- python3 tracker.py by-category --month 2026-09 ---
rent            $950.00
groceries       $164.15
eating out       $50.50
transport         $5.50

=================== ponytail ===================
 test_tracker.py | 23 ++++++++++++++++++++++-
 tracker.py      | 22 +++++++++++++++++++++-
 2 files changed, 43 insertions(+), 2 deletions(-)
Ran 6 tests in 0.003s
OK
--- python3 tracker.py by-category --month 2026-09 ---
rent            $950.00
groceries       $164.15
eating out       $50.50
transport         $5.50
```

Look at the code each one wrote:

```bash
git -C practice/baseline diff tracker.py
git -C practice/ponytail diff tracker.py
```

In our run the two solutions were nearly the same shape. Both reused `format_money()`, both added one function and one subcommand. The ponytail version used `collections.defaultdict` from the standard library and a 2-line month check where the baseline wrote 4. That is the whole difference (see `sample-output/by-category-baseline.diff` and `by-category-ponytail.diff`). Sonnet already writes fairly lean code for a clear, small request.

## Demo round 2: a vague request

Vague requests are where agents over-build. Reset the copies and try this one, from `requests/2-budgets.txt`:

> I keep overspending. Add budgets to this tracker so it warns me when I go over.

```bash
rm -rf practice
./setup.sh
./run-both.sh practice requests/2-budgets.txt
./compare.sh practice budget
```

(The last argument tells `compare.sh` which command to try. Both agents named it `budget` in all our runs, but check the reply if yours picked another name.)

Our run:

```
baseline: $0.07, 11 turns, 26s
ponytail: $0.05, 7 turns, 16s
```

```
=================== baseline ===================
 budgets.csv     |  4 ++++
 test_tracker.py | 14 ++++++++++++++
 tracker.py      | 36 ++++++++++++++++++++++++++++++++++++
 3 files changed, 54 insertions(+)
Ran 5 tests in 0.001s
OK
--- python3 tracker.py budget ---
WARNING 2026-09 eating out: $50.50 spent, $10.50 over the $40.00 budget

=================== ponytail ===================
 budgets.csv     |  5 +++++
 test_tracker.py |  9 +++++++++
 tracker.py      | 21 +++++++++++++++++++++
 3 files changed, 35 insertions(+)
Ran 4 tests in 0.001s
OK
--- python3 tracker.py budget ---
OVER BUDGET 2026-09 eating out: $50.50 of $40.00 (+$10.50)
OVER BUDGET 2026-09 groceries: $164.15 of $150.00 (+$14.15)
OVER BUDGET 2026-10 transport: $45.00 of $40.00 (+$5.00)
```

(Different warnings only because each agent invented different placeholder limits in `budgets.csv`.)

Both picked the same design: a `budgets.csv` file of monthly limits and a `budget` command. The baseline split the work into three new functions (`load_budgets`, `over_budget`, `cmd_budget`) and added a paragraph to the docstring. Ponytail put it in one 15-line function. The full diffs and both replies are in [sample-output/](sample-output/).

Read the end of each reply (`python3 -c 'import json;print(json.load(open("practice/ponytail.result.json"))["result"])'`, and the same for `baseline`). Ponytail's reply finished with a **Skipped** list:

```
**Skipped:**
- The warning only shows when you run `budget`, not when you add an expense. This tracker has no add command yet.
- Categories missing from `budgets.csv` are ignored, with no warning.
- A malformed budgets file raises a plain Python error.
```

## What to notice

- **Fewer lines is not automatically better.** Ponytail's budget code is shorter, but the baseline's separate `over_budget()` function is easier to test on its own. Judge readability yourself: which diff would you rather maintain?
- **The "Skipped" lines are the most useful part.** They tell you, in plain words, what you did not get. A vague request gets the smallest version that does the core job, and you decide whether you need more.
- **It does not skip tests.** Every ponytail run added at least one test for its new logic. The skill says "lazy code without its check is unfinished."
- **Precise requests leave little room to save.** If you already ask for exactly what you want, ponytail mostly adds reading time.
- **It reused the existing helpers in every run**, but so did the baseline. On a messier, bigger codebase the "already in this codebase?" step matters more.

## Try this

1. Run round 2 again with `/ponytail ultra` instead of `/ponytail` (edit the last line of `run-both.sh`, or do it interactively). Ultra is allowed to push back on parts of your request before building.
2. Write your own vague request (for example, "make this tracker easier to use") into a text file, reset the copies (`rm -rf practice && ./setup.sh`) and run `./run-both.sh practice your-request.txt`. Bigger, vaguer asks should show a bigger gap.
3. Run the same round twice without changing anything. How much do the line counts move on their own? That noise is why one run proves nothing.

## Limits and caveats

- **Results vary run to run.** In round 1, one ponytail run added *more* lines than its baseline (50 vs 48). Always repeat before drawing conclusions.
- **The project-only install is not the full plugin.** Without the hooks, ponytail is off until you type `/ponytail`, and the extra skills (`/ponytail-review`, `/ponytail-audit`, and so on) and the band are not there. The rules themselves are identical.
- **Headless runs skip the band.** It only shows in the interactive terminal or desktop app (Claude Code 2.1.290 or later).
- **It can cost more.** In round 1 ponytail took about twice as many turns because it reads more before writing.
- **Placeholder data.** On the vague request both agents invented budget limits. Ponytail's reply said so; check the baseline's reply too.

## Troubleshooting

**`./setup.sh` says the folder already has baseline/ or ponytail/.** Run `rm -rf practice` and try again.

**`curl: (22) The requested URL returned error: 404`.** GitHub could not find the pinned file. Check you can open https://github.com/DietrichGebert/ponytail/blob/v5.3.2/skills/ponytail/SKILL.md in a browser.

**`run-both.sh` stops with an error from `claude`.** Make sure `claude -p "say hi"` works on its own first (you need to be logged in).

**The ponytail reply has no "Skipped" or "Not checked" line.** The skill may not have loaded. Check the file exists at `practice/ponytail/.claude/skills/ponytail/SKILL.md` and that the prompt starts with `/ponytail`.

**`compare.sh` says `invalid choice: 'budget'`.** The agent named the command something else. Read its reply, then run `./compare.sh practice <that-name>`.

**With the full plugin: `node: command not found` on every prompt.** The hooks need Node.js on your PATH. The skill still works without it.

## Clean up

For the demo, delete the practice copies. Nothing else was installed:

```bash
rm -rf practice
```

If you installed the full plugin, upstream says to run its clean-up script **before** removing the plugin, because the script lives inside the plugin. It removes the mode flags, `~/.config/ponytail/config.json`, the status-line script copy and any `statusLine` entry it added (only if that entry points at ponytail's own script). From a fresh clone of the repo:

```bash
git clone --branch v5.3.2 https://github.com/DietrichGebert/ponytail.git /tmp/ponytail-src
node /tmp/ponytail-src/scripts/uninstall.js
rm -rf /tmp/ponytail-src
```

Then, inside Claude Code:

```
/plugin remove ponytail
/plugin marketplace remove ponytail
```

The band's task history in `~/.config/ponytail/band/` is not removed by the script. Delete that folder by hand if you used the band.

## Files in this folder

| Path | What it is |
|---|---|
| `demo/starter/` | The 57-line expense tracker, its CSV and 3 tests |
| `demo/setup.sh` | Makes the two practice copies and downloads the skill into one |
| `demo/run-both.sh` | Sends one request to both copies with `claude -p` |
| `demo/compare.sh` | Line counts, test results and a sample command for both copies |
| `demo/requests/` | The two feature requests |
| `sample-output/` | Real diffs, replies and `compare.sh` output from our runs |

## Where to read more

- Ponytail: https://github.com/DietrichGebert/ponytail (its `benchmarks/` folder has the upstream numbers)
- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code plugins: https://code.claude.com/docs/en/plugins
