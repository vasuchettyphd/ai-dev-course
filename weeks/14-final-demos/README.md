# Week 14: Final demos

**Goal:** show what you built. You'll get your semester project ready on `main`, write and rehearse a 3-minute demo with a plan for when something fails in the room, write a short final write-up where every number comes from a file in your repo, and give the demo in class.

**Time:** plan for about 3 to 4 hours of your own time before demo day (an estimate): about 1 hour getting `main` ready, 1 hour on the demo and two rehearsals, and 1 to 2 hours on the write-up. **Cost:** a few Claude calls for your rehearsals, from your week 9 API credit.

**Tested with** (13 October 2026; these are the versions tested, yours may be newer):

- The deal screener's model `DEMO.md` and `FINAL.md`, with each live demo command run for real from a container, and the offline fallback run with the network switched off.
- **Being tested:** everything inside a signed-in Claude Code session, everything on GitHub, and every step on a Mac or in Windows (WSL).

## Before you start

You need:

- Weeks 3 to 13 done: your private `semester-project` with its AI feature, `REVIEW.md`, your week 12 evaluation and week 13 injection results, a `Dockerfile`, your keys in `.env` and the `Read(./.env)` deny rule.
- `gh` signed in to **your** GitHub account, and Claude Code signed in with your Claude Pro account.

**On the Gemini path** (no API credit, set up in week 9; see [week 9's Gemini page](../09-calling-a-model/gemini.md)): your rehearsals and your demo call Google's free tier, so they cost nothing; everything else is the same. A free-tier model can be busy (error 503) or you can hit a limit (error 429), so rehearse what your program says when a call fails: if it happens on demo day, that's the fallback you show.

"Your terminal" means **Terminal** on a Mac (Apple chip or Intel) and the **Ubuntu window** on Windows; the commands are the same on all three. On Windows, stay in your Ubuntu home folder (paths start `/home/<you>/`, never `C:\`). As in weeks 11 to 13, start Claude Code only in a window where no key is loaded.

### How you'll work this week

As in weeks 9 to 13: plain-English prompts, plain **Yes** for git, a branch first, a pull request last, and the key rules.

**The demo rules, new this week:**

1. **No key ever on screen.** Demo from a window where no key is loaded, with programs that read `.env` themselves (if yours can't yet, see step 2d). Never run `cat .env`, `env` or `printenv` while sharing your screen.
2. **Every number is real.** Your write-up only uses numbers that are in a file in your repo, and links to that file.
3. **Show one honest limit.** Every project has one. Saying it is worth points.
4. **Have a fallback.** If the network or the model fails in the room, you switch to your offline tests and your committed results files.

| Claude asks to | Choose |
|---|---|
| Check your project against the "ready on main" list and tell you what's missing | **Yes** |
| Draft `DEMO.md` or `FINAL.md` from your repo | **Yes**, then edit them yourself |
| Read files in `~/ai-dev-course` (the course's model `DEMO.md` and `FINAL.md`) | **Yes**: it only reads them |
| Change code, tests or results files while checking or drafting | **No**: fix things yourself, one at a time, with your own prompt |
| Read or print `.env`, or put a key in any file | **No** |
| `git add`, `git commit`, `git push` on your `final` branch, `gh pr create` | plain **Yes**, after `git status` shows no `.env` |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

## Steps

### 1. What final demos are

Each student has **3 minutes** to show their project working, then about a minute of questions. Your instructor sets the order. You hand in three things (see [the assignment](assignment.md)): the demo itself, your project as it stands on `main`, and a short write-up, `FINAL.md`.

The deal screener has a model of both. Read them now, so you know the shape you're aiming for:

- [`example-project/DEMO.md`](../../example-project/DEMO.md): a timed 3-minute script, with what to show, what to type, what to say and what to do if each step fails.
- [`example-project/FINAL.md`](../../example-project/FINAL.md): the write-up, under seven headings, with every number linked to its file.

### 2. Get your project ready on main

**a. Make the branch first.** In a **new** terminal window (no key loaded), `cd ~/semester-project`, start `claude`, and in Claude Code:

```text
Switch to main, pull the latest changes from GitHub, then create a new branch called final and switch to it.
```

Plain **Yes** to each git command. Check: "What branch am I on?" says `final`.

**b. Check the "ready on main" list.** These are the things weeks 3 to 13 asked you to have, and the project points in the rubric come from them:

| Check | From | How to check |
|---|---|---|
| Tests pass with `.env` moved out | weeks 9 to 13 | step 2c |
| `REVIEW.md` is triaged: every finding has a Decision and a Reason | weeks 6, 7, 9 to 13 | open `REVIEW.md` |
| Your week 12 evaluation results and week 13 injection results are committed | weeks 12, 13 | `ls` your results folder; open the files |
| No key anywhere in the history | week 13 step 1 | `git log --all --oneline -- .env` prints nothing; `git log --all -S'sk-ant-' --oneline` and `git log --all -S'AIza' --oneline` list no commit that adds a real key (a fake value in `.env.example` or a test is fine: `git show --stat --format=%s <id>` shows which files) |
| The README says how to run it, with exact commands | weeks 5 to 13 | read it as a stranger would |
| Your repo is private, with your instructor as a collaborator (not scored, but your instructor needs it to grade) | week 4 | on GitHub, **Settings > Collaborators** |
| Docker builds and runs your tests | week 7 | `docker build -t semester-project .`, then run your tests in the container as in week 7 step 4c |

In Claude Code:

```text
Check this project against this list and tell me what's missing, as a table with the columns Check, Status and What's missing. Don't change any file. The list: the tests pass without any API key; REVIEW.md has a Decision and a Reason for every finding; the week 12 evaluation results and week 13 injection results are committed; the README says exactly how to run the program and the tests; the Dockerfile builds and runs the tests. Never read or print .env, and don't run anything that calls a real model.
```

Then do the key checks in the table yourself, in a second terminal window, in `~/semester-project`.

**c. Run your tests offline.** In a window with no key loaded, in `~/semester-project`:

```bash
[ ! -e ~/env-aside ] && mv .env ~/env-aside && echo moved
```

If it doesn't print `moved` (for example, it says `No such file`), stop and ask your instructor. Run your tests the way your README says. Then:

```bash
[ ! -e .env ] && mv ~/env-aside .env && echo restored
ls -a
```

`ls -a` must show `.env` again.

**d. Make your program read `.env` itself.** On demo day you'll run it from a window with no key loaded, so it has to find the key on its own, as the deal screener does. If you've been loading the key with `set -a; . ./.env; set +a`, in Claude Code:

```text
Make my program read its API keys from the .env file in this folder by itself, without printing them, the way the deal screener's extract.load_env_file does in ~/ai-dev-course/example-project. A key already loaded in the environment wins. Keep every test passing and offline, write a test for it with a made-up .env in a temporary folder, never read or print my real .env, and commit.
```

If that isn't possible in time, you'll load the key once with `set -a; . ./.env; set +a` in your demo window before you share your screen (step 6), and never print it.

**e. Fix what's missing,** one thing at a time, with your own prompt for each, as in weeks 5 to 13. Commit each fix. If a feature doesn't work yet and can't be fixed in time, don't hide it: add a "Known problems" section to your README saying so, and say it in `FINAL.md`.

### 3. Write your 3-minute demo

**a. Draft it.** In Claude Code:

```text
Read example-project/DEMO.md in the course repo at ~/ai-dev-course as a model. Then write DEMO.md for my project in the same shape: a table with the columns Time, Show, Command and where to type it, Say, and If it fails, ending at 3:00 or less; then "Before you start", "If it fails" and "What to cut first if you're over time". Use only commands from my README. Show my AI feature working once, and one honest limit. No command may print a key or .env. Don't run anything that calls a real model. Then commit DEMO.md.
```

**b. Rehearse twice with a timer,** in a window set up as on the day (step 6), running the real commands. Change `DEMO.md` until it fits in 3 minutes. Cut the thing `DEMO.md` says to cut first, not the honest limit.

**c. Rehearse the fallback once.** Pretend the network failed at your AI step: switch to your offline tests and your results files, and say what the live run would have shown.

### 4. Write your write-up

**a. Draft it.** In Claude Code:

```text
Read example-project/FINAL.md in the course repo at ~/ai-dev-course as a model. Then draft FINAL.md for my project, about two pages, under exactly these seven headings: What it does and who it's for; How it's built, and which parts are AI; What I measured; What went wrong and what I changed; Risks and responsible use; What AI did and what I decided; What I'd do next. Every number must come from a file in my repo and link to that file; if a number isn't in a file, leave it out and tell me. For "Risks and responsible use", use my week 13 answers on privacy, bias, licensing and academic integrity, which I paste here: <paste your four answers>. Don't invent anything. Never read or print .env. Then commit FINAL.md.
```

**b. Make it yours.** Read it all and rewrite anything that isn't true or isn't how you'd say it. Heading 6 matters most: say plainly what Claude Code wrote, what you decided (the plan, the tests, which review findings to fix, the expected answers), and what you'd do differently.

**c. Check every number** by clicking its link.

### 5. Pull request and finish

**Push, open a pull request, read Files changed** (your fixes, `DEMO.md`, `FINAL.md`; no `.env` and no real key: use the browser's Find for `sk-ant-`, `ANTHROPIC_API_KEY=`, `AIza` and `GEMINI_API_KEY=`; only a fake value, as in `.env.example`, is allowed), as in week 10 step 7. **Merge with "Create a merge commit"**, as in weeks 12 and 13. Then, in your terminal in `~/semester-project`: `git switch main && git pull`.

### 6. On the day

- **Before your turn:** open one terminal window with **no key loaded** (`[ -z "$ANTHROPIC_API_KEY$GEMINI_API_KEY" ] && echo clear` prints `clear`), in `~/semester-project`, with your `.venv` active. If your program can't read `.env` itself (step 2d), load the key once with `set -a; . ./.env; set +a` in that window now, before you share your screen. Make the text large. Close other tabs and windows, and turn notifications off. Have `DEMO.md` open on paper or your phone, not on the shared screen.
- **During:** follow `DEMO.md`. If a step fails, say so in one sentence and switch to the fallback. Don't debug in front of the room.
- **If a key ever shows on screen:** it's leaked. Pause and delete it in the Console first (week 9 step 2f; for a Google key, week 10 step 2e): it takes about 30 seconds. Then carry on with the fallback (the live steps won't work until you make a new key), and tell your instructor afterwards.

The deal screener's week 14 changes are on this page (it works once week 14 is published): <https://github.com/vasuchettyphd/ai-dev-course/compare/week-13...week-14>.

## Check it worked

- Every row of the "ready on main" table is true on `main`.
- Your tests pass with `.env` moved out (step 2c).
- `DEMO.md` fits in 3 minutes in two timed rehearsals, and you've rehearsed the fallback once.
- `FINAL.md` has the seven headings, and every number links to a file.
- The pull request is merged with a merge commit, and you've pulled.

## Troubleshooting

| What you see | What to do |
|---|---|
| The demo runs over 3 minutes | Cut what `DEMO.md` says to cut first. Keep the AI step and the honest limit. Say less, don't talk faster. |
| No internet, or a 429, on the day | Switch to the fallback: your offline tests and your committed results files. Say what the live run would show. |
| A feature doesn't work yet | Demo what does work. Say plainly what doesn't and why, in the demo and in `FINAL.md`. |
| A key appears on screen | Pause and delete the key in the Console first (week 9 step 2f), then carry on with the fallback, and tell your instructor afterwards. |
| The AI step says there's no key | Your program doesn't read `.env` itself: step 2d, or load the key before you share your screen (step 6). |
| A number in `FINAL.md` has no file to link to | Leave it out, or run the thing again and commit the results first. |
| `docker build` fails | See [week 7's Troubleshooting](../07-running-with-docker/README.md#troubleshooting). |
| Anthropic errors (401, 429, credit, workspace) | See [week 9's Troubleshooting](../09-calling-a-model/README.md#troubleshooting). |
| Work was committed to `main` | Use [week 5's rescue](../05-building-with-ai/README.md#if-it-committed-to-main). |
