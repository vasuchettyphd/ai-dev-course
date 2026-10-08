# Beads: a task tracker your coding agent can't forget

A hands-on tutorial for [beads](https://github.com/gastownhall/beads) (`bd`), Steve Yegge's issue tracker for AI coding agents. You will build a small Python CLI with Claude Code, kill the session halfway, and watch a fresh session pick up exactly where the last one stopped.

Everything here was run for real against **beads v1.3.1** and Claude Code 2.1 (Sonnet) on 2026-10-08. The results quoted below come from those runs. Beads changes quickly, so the install script pins that version.

**Time:** about 60-90 minutes. **Cost:** roughly $0.15-0.20 of model usage per agent session, about $1-2 for everything.

## The idea in one paragraph

Coding agents forget everything when a session ends or the context window is compacted. The usual fix is a file on disk the agent re-reads, like a `PLAN.md` with checkboxes. Beads replaces the *checklist* part of that file with a small database: each task is an issue, tasks depend on each other, and `bd ready` tells the agent which tasks are unblocked right now. A Claude Code hook loads that state into every new session automatically.

## plan.md and beads do different jobs

| | `PLAN.md` | Beads |
|---|---|---|
| **Job** | The initial plan: what we're building and why | The living state: what's done, what's next, what's blocked |
| **Changes** | Rarely, when the design changes | Constantly, every time a task is claimed or closed |
| **Who edits it** | You, or the agent while planning | The agent, only through `bd` commands |
| **Answers** | "What is the design?" | "What should I do next?" |

The natural workflow is to write `PLAN.md` first, convert its task list into beads, and then let the agent work from beads. The plan stays as the design document.

### The trade-off

You could skip beads and have the agent tick boxes in `PLAN.md`. That costs nothing to set up, but:

- **The file only grows.** The agent re-reads all of it every session. `bd ready` returns only the tasks that matter now.
- **Markdown drifts.** Agents forget to tick boxes, reword tasks or leave stale notes. Beads changes state only through commands (`claim`, `close`), so it stays consistent.
- **Dependencies are prose.** In markdown, the agent works out what's blocked by reading. Beads calculates it.
- **Several agents clash.** Two agents editing one file will collide. A beads claim is atomic: the second agent is refused.

Against that, beads adds:

- a 150 MB binary
- a Dolt database
- version pinning
- agent instruction files for half a dozen tools

On a small project you may not notice any benefit (see the results below).

## What we found

We ran the same two sessions on the same 12-task project, once with beads and once with `PLAN.md` alone. Session 1 was "implement two tasks". Session 2 was a fresh session told only "Continue where the last session left off. Do one task."

| | Beads | PLAN.md only |
|---|---|---|
| Session 2 picked the right next task | Yes (task 2) | Yes (task 2) |
| How it worked out where it was | Its first command was `bd ready` | 7 tool calls (`git diff`, reading code, re-reading `PLAN.md`) before writing any code |
| Did it record progress anywhere? | Yes, closed issues with a reason | No. It never ticked anything in `PLAN.md`; progress existed only in the code |
| Session 2 cost | $0.18 | $0.16 |

**Takeaway:** on a project this small, both approaches resume correctly and cost about the same. The difference is *how* they know. Beads reads the state directly. The plain agent reconstructs it from the code each time, which gets harder and less reliable as the project grows. That's what Exercise 5 tests.

This is one run of each, so it's an anecdote, not a benchmark.

## Setup

You need git, Python 3.10+, and [Claude Code](https://claude.com/claude-code). On Windows, use WSL.

```bash
git clone https://github.com/vasuchettyphd/beads-tutorial.git
cd beads-tutorial
scripts/install-bd.sh                 # downloads bd v1.3.1 into ./bin, verifies its checksum
export PATH="$PWD/bin:$PATH"          # run this in every new terminal
bd version                            # bd version 1.3.1 (...)
```

Nothing is installed system-wide. Practice projects go in `practice/`, which git ignores.

## Exercise 1: beads by hand (no agent)

Learn the five commands an agent will use. Make a scratch project:

```bash
scripts/new-practice.sh ex1 --beads
cd practice/ex1
```

`bd init` created `.beads/` (the database) and committed it to git. It also wrote instruction files for several agents: `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, `.agents/skills/beads/`, `.codex/`, `.cursor/`. Open `.claude/settings.json`: it's a single `SessionStart` hook that runs `bd prime --hook-json`. That hook is the whole trick behind Exercise 3.

Create an epic with three tasks, then chain them:

```bash
E=$(bd q "Make tea" -t epic)
A=$(bd q "Boil water"   --parent $E)
B=$(bd q "Steep tea"    --parent $E)
C=$(bd q "Add milk"     --parent $E)
bd dep add $B $A            # B depends on A
bd dep add $C $B            # C depends on B
bd ready                    # only "Boil water" (and the epic) are ready
bd blocked                  # the other two, and what blocks them
```

Do the work the way an agent would:

```bash
bd update $A --claim        # marks it in progress and assigns it to you
bd close $A --reason "kettle done"
bd ready                    # now "Steep tea" is ready
bd show $C                  # details, parent, what it depends on
```

**Check yourself:** what does `bd ready` show after you close `$B`? (Answer: "Add milk", plus the epic, which stays ready until you close it.)

`bd ready` also prints a tip about installing the beads plugin or running `bd setup claude`. You can ignore it: `bd init` already set up Claude Code.

## Exercise 2: turn PLAN.md into beads

Make the real practice project and read its plan:

```bash
cd ../..                          # back to the tutorial root
scripts/new-practice.sh build --beads
cd practice/build
cat PLAN.md
```

`PLAN.md` describes `wordstats`, a word-statistics CLI, as 12 tasks with a dependency column. Start Claude Code (`claude`) in this folder and ask:

> Read PLAN.md and create a beads epic with one child issue per task. Add the dependencies from the table with `bd dep add`. Don't write any code yet. Finish by running `bd ready`.

Check its work:

```bash
bd list --all       # 1 epic + 12 tasks
bd ready            # tasks 1 and 3, plus the epic
bd blocked          # 10 blocked tasks
```

If it went wrong, or you want to skip ahead, rebuild the folder and run the seeding script instead:

```bash
cd ../.. && rm -rf practice/build
scripts/new-practice.sh build --beads
cd practice/build
../../scripts/seed-beads.sh
```

**Note:** `bd create -f file.md` can batch-create issues from markdown headings. We tried it, but in v1.3.1 its dependency field didn't link issues by title. That's why the agent (or the script) adds dependencies one by one.

## Exercise 3: kill the session, and see what survives

This is the point of the tutorial.

1. In Claude Code, in `practice/build`:

   > Implement the project in PLAN.md. Work through the beads issues. Complete exactly two tasks, then stop and say which issue IDs you closed.

   In our run it closed tasks 1 and 3 (the only two that were ready), with tests, in about 5 turns.

2. Quit Claude Code completely (`/exit`). In a terminal, run `bd list --all`: two tasks show as closed.

3. Start a **new** session and say only:

   > Continue where the last session left off. Do one task, then stop.

Watch what happens:

- The `SessionStart` hook runs `bd prime`, which loads the workflow rules and current state into the new session.
- The agent's first command is `bd ready`. In our run it was `bd list --status=in_progress; bd ready`.
- It claims the next unblocked task (task 2), implements it, runs the tests and runs `bd close`.

Try `/clear` mid-session too: the hook runs again and the agent recovers the same way.

**Discuss:** where did the agent's knowledge of "what's next" come from? Not from its memory, and not from reading the code.

## Exercise 4: two agents, one task list

Open two terminals in `practice/build`, both with `bd` on the PATH. Pick an open task ID from `bd ready` (something like `ws-xxx.4`). In each terminal, pretend to be a different agent:

```bash
# terminal 1
bd --actor agent-a update <id> --claim     # ✓ Updated issue
# terminal 2, same id
bd --actor agent-b update <id> --claim     # Error updating <id>: issue already claimed by agent-a
```

The second claim is refused (exit code 1), so two agents can't end up on the same task. `bd show <id>` also shows a **lease** ("expires in 4 mins"). If an agent dies mid-task, `bd reclaim` returns stale claims to the ready list.

Release it afterwards with `bd --actor agent-a unclaim <id>`.

Stretch goal: run two Claude Code sessions in separate terminals, both told "work through the ready beads issues, one at a time". Check that they never pick the same task. Give each session its own git worktree so their code changes don't collide.

## Exercise 5: the experiment

Does beads beat a plain plan once the project is long enough for it to matter? Run both conditions on the same project:

```bash
cd ../..                                       # back to the tutorial root
scripts/new-practice.sh arm-beads --beads
(cd practice/arm-beads && ../../scripts/seed-beads.sh)
scripts/new-practice.sh arm-plain              # no beads; agent tracks progress however it likes
```

Run each condition's sessions from inside its own folder (`practice/arm-beads` or `practice/arm-plain`).

For each condition, do several short sessions until all 12 tasks are done. Start every session fresh with the same prompt: "Continue where the last session left off. Do two tasks, then stop." For the plain condition, start the very first session with "Implement the project in PLAN.md. Do two tasks, then stop."

Fill in [`experiment/scorecard.md`](experiment/scorecard.md) after each session. The things to record:

- Did it pick a task that was actually ready?
- Did it redo or skip anything?
- Did the tests pass?
- What did it cost? Use `/cost` in Claude Code, or the session summary.

**Predictions to test:**

1. Both conditions do fine for the first few sessions.
2. The plain condition spends more of each session working out where it is, and that overhead grows.
3. Mistakes (skipping a task, building one twice, starting something blocked) show up in the plain condition first.

If your data says otherwise, that's a result too.

## Caveats

- **It's opinionated.** `bd prime` tells the agent to use beads for all task tracking, and not to use its built-in todo list, markdown TODOs or `MEMORY.md` files. That's deliberate, but it can conflict with your own setup: for example, a planning workflow that writes checkbox plans, or Claude Code's auto-memory.
- **`bd init` touches a lot.** It writes integration files for Claude Code, Codex and Cursor, and commits to git. `bd init --skip-agents` followed by `bd setup claude` installs only the Claude Code pieces (the hook in `.claude/settings.json` and a section in `CLAUDE.md`). `bd init --stealth` keeps beads files out of git entirely.
- **Pin your version.** The project moves fast (over 11,000 commits). Syncing between machines needs matching `bd` versions, and upgrades involve export, install and migrate steps.
- **Dolt is under the hood.** It's embedded by default, so there's no server to run. But the database is binary, and `.beads/issues.jsonl` is only an export, not a backup.
- **It hasn't been proven.** It's very popular (about 28,000 stars), but nobody has published a careful comparison against a well-kept plan file. That's why Exercise 5 exists.

## Cleanup

```bash
rm -rf practice bin
```

Beads installed nothing outside this folder. The only global change is whatever Claude Code itself saved.

## Files

| Path | What it is |
|---|---|
| `scripts/install-bd.sh` | Downloads pinned bd v1.3.1 into `./bin`, checks its checksum |
| `scripts/new-practice.sh` | Copies `starter/` into `practice/<name>` as a git repo, optionally with `bd init` |
| `scripts/seed-beads.sh` | Loads the 12 PLAN.md tasks and their dependencies into beads |
| `starter/` | The `wordstats` project: `PLAN.md`, a stub package, one placeholder test, `sample.txt` |
| `experiment/scorecard.md` | The table for Exercise 5 |
