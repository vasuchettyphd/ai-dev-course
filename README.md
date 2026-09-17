# Stop Building the Wrong Thing: `/grilling` and Superpowers in Claude Code

Two of the most useful additions to Claude Code are not features of Claude Code itself. They are plugins from the official marketplace, written by working engineers, that change *how* Claude approaches a task before it writes a line of code.

- **`/grill-me`** (from Matt Pocock's `mattpocock-skills`) turns Claude into a relentless interviewer that stress-tests your plan until nothing is left silently assumed. Under the hood it runs the `grilling` skill, the reusable interview engine that several of Matt's other skills also call.
- **Superpowers** (from Jesse Vincent's `superpowers`) is a complete development methodology: brainstorm, spec, plan, then implement with subagents, test-driven development, and built-in code review.

Both attack the same failure mode: the agent confidently builds something you did not ask for. This tutorial covers what each one does, how to install it, what a session looks like, and how to use them together.

Versions covered: `mattpocock-skills` 1.2.3 and `superpowers` 6.3.0, as pinned in the official marketplace in September 2026.

---

## 1. Installation

Both plugins live in Anthropic's official marketplace, so there is nothing to add first. From inside a Claude Code session:

```
/plugin install mattpocock-skills@claude-plugins-official
/plugin install superpowers@claude-plugins-official
```

Or from your shell:

```bash
claude plugins install mattpocock-skills
claude plugins install superpowers
```

Restart the session afterwards. Superpowers relies on a session-start hook, so it only takes effect in a fresh session.

To confirm they loaded, type `/` and start typing `grill` or `superpowers`. You should see entries like `/grilling`, `/grill-me`, `/grill-with-docs`, and `/superpowers:brainstorming`.

**One-time repo setup for Matt Pocock's skills.** The engineering skills in that bundle (tickets, triage, specs) want to know your issue tracker and where docs live. Run this once per repo:

```
/setup-matt-pocock-skills
```

`/grilling` itself works without it, but `/grill-with-docs` writes `CONTEXT.md` and ADRs, so it helps to have the doc location settled.

---

## 2. `/grill-me`: the interview that will not let you hand-wave

### Two names, one skill

You will see both `/grill-me` and `/grilling` in the plugin, and it helps to know how they relate before you type either.

- **`grilling`** is the engine. It holds the whole interview technique, and it is *model-invoked*: Claude can reach for it on its own when a task fits, and other skills (`grill-me`, `grill-with-docs`, `triage`, `wayfinder`) call it rather than inventing their own interview.
- **`grill-me`** is the front door. Its entire body is one line: run the `grilling` skill. It is *user-invoked only*, so it never fires by itself. You type it when you want the interview and nothing else.

In practice, type `/grill-me`. Typing `/grilling` directly gives you the identical session, and the distinction only matters if you are building your own skill that needs an interview, in which case you call `grilling` from it.

### What it does

`/grill-me` interviews you about a plan, decision, or idea until you and Claude share the same understanding. You do not need a worked-out plan to start. Producing one is what the session is for, and vagueness is the thing it eats. It models the subject as a **design tree**: every decision branches into the smaller decisions that hang off it. The interview walks that tree until every branch is visited.

Three ideas carry the whole skill:

| Term | Meaning |
|---|---|
| **Design tree** | The decisions in your plan, and the decisions that depend on them. |
| **Frontier** | The decisions whose prerequisites are already settled. These are the only questions Claude can honestly ask right now. |
| **Round** | One full frontier, asked in one message and answered in one reply. |

The important consequence: Claude does not ask one question at a time, and it does not dump everything at once. Each round contains only questions that are independent of each other. Your answers settle those decisions, which unblocks the next layer, and the next round asks what that unlocked. Thirteen questions typically land in about three rounds rather than thirteen.

### The question format

Every question in a round arrives in a fixed shape:

```
❓ **Q1** - **Storage backend**: Where should rate-limit counters live? Options:
   (a) in-process memory, (b) Redis, (c) the existing Postgres database.

➡️ Redis. You already run it for sessions, and in-process memory breaks
   as soon as you have two API replicas.

---

❓ **Q2** - **Limit scope**: Should limits apply per API key, per user, or per IP?

➡️ Per API key. IPs are shared behind corporate NATs and users can hold
   several keys.
```

The `➡️` line is Claude's recommended answer. Because each question is numbered, you answer the whole round by number:

> 1 yes. 2 per user, not per key, because our keys are per-integration and one customer can have dozens of them.

You do not need to quote the questions back.

### Facts versus decisions

This is the rule that makes the skill trustworthy. **Finding facts is Claude's job. Making decisions is yours.**

If a question needs a fact from the environment (what database you already use, whether a module exists, what a config value is), Claude dispatches a subagent to look it up rather than asking you. It does not block on that lookup: only the questions downstream of it wait, and the rest of the frontier is asked immediately.

Decisions, on the other hand, are always put to you. An agent running `/grilling` that answers its own decisions has broken the skill. If you see that happen, say so, and it will reopen the branch.

### The confirmation gate

The session is not over when Claude runs out of questions. It is over when **you** confirm the understanding is shared. Claude must not start building until you say so. If it does start building on its own, tell it to stop, and consider adding a line to your `CLAUDE.md` such as "Do not implement without permission."

### Walkthrough

Start with a rough idea:

```
/grill-me I want to add rate limiting to our public API.
```

**Round 1** asks the questions that have no prerequisites: what you are protecting against, which storage to use, what the limit is keyed on, what happens when a client exceeds it. Claude may spin up a subagent to read your middleware stack while you answer.

**Round 2** only exists because of your Round 1 answers. If you chose per-user limits, it now asks how unauthenticated requests are treated. If you chose Redis, it asks about failure behavior when Redis is down. Nothing in Round 2 could have been asked before Round 1 was settled.

**Round 3** is usually short: response headers, whether to expose limits in the docs, rollout order.

When the frontier is empty, Claude summarizes the design tree and asks you to confirm. Only then does implementation begin.

### Which entry point to use

`/grilling` is a **primitive**. Other skills call it, and it has two user-facing front doors:

| Situation | Use |
|---|---|
| You want the plain interview, no files written | `/grilling` or `/grill-me` (identical, but `/grill-me` never triggers on its own) |
| You are in a repo and want a paper trail | `/grill-with-docs` writes `CONTEXT.md` (a project glossary) and ADRs as you go |
| The effort is too big for one session | `/wayfinder` maps it as decision tickets and grills each one |
| The question is about look and feel | `/prototype` builds a throwaway version instead of talking |

`/grill-with-docs` is Matt Pocock's most recommended skill. The `CONTEXT.md` it builds gives you and the agent a shared vocabulary, which makes every later session shorter and every later prompt more precise.

### Getting the most out of `/grill-me`

`/grill-me` is **stateless**. It writes no files and leaves no workspace behind. The only output is a sharper version of the idea in your own head, which is exactly what makes it portable: no repo, no setup, and no assumption that the subject is software. People point it at product directions, business calls, talk outlines, and pieces of writing.

A few habits make the difference between a session that produces decisions and one that produces confident nonsense.

- **Start it in a fresh conversation.** Do not run it on top of a plan an agent already wrote. The interview is for forming the plan, not defending one.
- **Leave plan mode off.** Plan mode primes Claude to rush toward producing a plan, which is the opposite of staying in inquiry.
- **Own the scope.** The skill asks the questions, but you steer. The failure mode is passivity: answering "agreed, agreed, agreed" for forty questions and coming out with a plan Claude wrote and you nodded at. It feels productive because it was long. Push back on questions pitched beneath the fidelity you need, and say when the scope drifts.
- **"I don't know" is a real answer.** Say it and mean it. A question you cannot answer by talking is usually a sign to prototype rather than guess.
- **Recognise the ungrillable question.** "One long form or three pages?" and "how should this interaction feel?" need something to react to. Talking through them is where sessions balloon. Stop, build the throwaway version with `/prototype`, look at it, then come back and answer in one line.
- **Count rounds, not questions.** Forty-six questions across four rounds is an ordinary session. Two hundred questions means the scope was too large. Ask Claude to break the work up, then grill each piece.
- **Use your best model.** Grilling leans on the model's own sense of how systems break, more than most skills do. Implementation tolerates a cheaper model; the interview does not.
- **Do not start a fresh session before the spec.** The value of the session is the context you just built. If the idea turns out to be software, hand the same conversation straight to `/to-spec`.

You know it worked if you disagreed with something along the way, if you ended up somewhere you did not expect because a question surfaced a decision you had been making implicitly, and if you could defend each choice to someone who was not there.

### Tuning it

- **Prefer one question at a time?** Add `When grilling, ask one question at a time.` to your global `CLAUDE.md`. This is a supported opt-out, not a hack.
- **Want fewer questions?** There is no cap, deliberately. Tell it to wrap up, or accept the plan where it stands. If sessions run very long, the scope is probably too big: split the work and grill the pieces.
- **The recommendation contradicts the question?** This happens. Answer the recommendation and say so.

### It is working if

- A round arrives as a numbered list with a `➡️` recommendation under each question.
- Nothing in a round depends on another question in the same round.
- Later rounds ask things the first round could not have asked.
- Claude looks up facts itself instead of asking you.
- It stops at the end and waits for your confirmation.

---

## 3. Superpowers: a methodology, not a command

### What it is

Superpowers is a set of composable skills plus a session-start hook that makes sure Claude actually uses them. Once installed, you do not have to type anything special. From the moment Claude sees you are building something, it steps back and asks what you are really trying to do, gets a spec out of you, writes an implementation plan, and then executes it with subagents, test-driven development, and code review.

There is no single `/superpowers` command. There are three ways it shows up:

1. **Automatically.** The `using-superpowers` skill is injected at session start (and again after `/clear` and context compaction). It instructs Claude to check for an applicable skill before any response, including clarifying questions. "Let's build X" triggers brainstorming. "Fix this bug" triggers systematic debugging.
2. **By name.** Every skill is callable as `/superpowers:<skill>`, for example `/superpowers:brainstorming` or `/superpowers:writing-plans`.
3. **By asking.** "Use the systematic-debugging skill on this" works too.

### The skills

**The main workflow, in order:**

| Step | Skill | What it does |
|---|---|---|
| 1 | `brainstorming` | Refines a rough idea through questions, proposes approaches, presents the design in sections for approval, saves a spec. |
| 2 | `using-git-worktrees` | Creates an isolated workspace on a new branch with a clean test baseline. |
| 3 | `writing-plans` | Breaks the spec into tasks of 2 to 5 minutes each, with exact file paths, code, and verification steps. |
| 4 | `subagent-driven-development` or `executing-plans` | Runs a fresh subagent per task with two-stage review (spec compliance, then code quality), or executes in batches with human checkpoints. |
| 5 | `test-driven-development` | Enforces red, green, refactor. Code written before its test gets deleted. |
| 6 | `requesting-code-review` | Reviews against the plan and reports issues by severity. Critical issues block progress. |
| 7 | `finishing-a-development-branch` | Verifies tests, offers merge, PR, keep, or discard, and cleans up the worktree. |

**Supporting skills:** `systematic-debugging` (four-phase root-cause process), `verification-before-completion` (prove it is fixed before saying so), `dispatching-parallel-agents`, `receiving-code-review`, and `writing-skills` for authoring your own.

### Brainstorming in detail

Brainstorming is the skill you will meet most often, and it is the closest cousin to `/grilling`. Two things define it.

**The hard gate.** Claude may not write code, scaffold anything, or invoke an implementation skill until it has told you what it intends and you have approved it. This applies to every task, including a one-line config change. The design may be two sentences in chat, but the approval is never skipped.

**Three paths.** Before its first question, Claude classifies the request out loud so you can override it:

| Path | When | Output |
|---|---|---|
| **Spike** | A feasibility question ("can we...?") | An answer and a recommendation. Anything built is labeled throwaway. |
| **Bounded** | A well-scoped change to a flow that already exists in the repo | Clarifying questions, then a short design in chat, then approval, then implementation with no plan document. |
| **Architectural** | New projects, new subsystems, interface changes | Questions one at a time, 2 to 3 proposed approaches, a sectioned design approved section by section, a written spec at `docs/superpowers/specs/`, then `writing-plans`. |

When in doubt, it takes the heavier path. If hidden complexity appears mid-task, the path upgrades. Nothing downgrades.

### Walkthrough

```
Let's add rate limiting to our public API.
```

With Superpowers installed, Claude announces "Using brainstorming to..." and classifies the request. A new middleware layer touching every route is architectural, so it explores the repo, then asks questions **one at a time**, preferring multiple choice. After it understands purpose, constraints, and success criteria, it proposes two or three approaches with a recommendation and YAGNI applied ruthlessly.

Then it presents the design in sections (architecture, components, data flow, error handling, testing) and asks after each one whether it looks right. Once you approve, it writes the spec to `docs/superpowers/specs/2026-09-17-rate-limiting-design.md`, self-reviews it for placeholders and contradictions, commits it, and asks you to review the file.

When you say go, it invokes `writing-plans`, and from there `subagent-driven-development` runs each task in a fresh subagent with TDD and two-stage review. It is normal for Claude to work for an hour or two without leaving the plan.

### The visual companion

During architectural brainstorming, if a question would be clearer shown than described (a layout, a diagram, a side-by-side), Claude offers to open a browser tab with mockups. It only offers when a visual question actually arises, and you can decline. Note that the companion loads a logo from the author's website that carries the plugin version, which they use as a usage counter. Set `SUPERPOWERS_DISABLE_TELEMETRY=1` to switch that off.

---

## 4. Using them together

The two overlap on exactly one step: the interview before building. They disagree on how to run it.

| | `/grill-me` | Superpowers `brainstorming` |
|---|---|---|
| Question rhythm | Whole frontier per round, answered by number | One question at a time |
| Recommendations | Always, on a `➡️` line | Conversational, for approaches rather than each question |
| Output | Shared understanding, plus `CONTEXT.md` and ADRs with `/grill-with-docs` | A spec file, then a plan, then execution |
| Scope | Any plan, decision, or idea, including non-code | Software features and bugs |
| After the interview | Stops. What happens next is up to you | Flows straight into planning and subagent execution |

A workflow that plays to both strengths:

1. **Think with `/grill-me` or `/grill-with-docs`.** Rounds are faster for thinking through a design with many independent decisions. Use `/grill-with-docs` when you are in the repo, since you get a growing `CONTEXT.md` glossary as a side effect. Use `/grill-me` when you are not.
2. **Confirm the shared understanding.** Do not skip the gate.
3. **Hand off to Superpowers for execution.** Tell Claude "We've already grilled this. Treat the agreed design as the approved brainstorm and go to writing-plans." Then `/superpowers:writing-plans` followed by `/superpowers:subagent-driven-development` carries it through with TDD and review.

One caution: Superpowers' session-start hook tells Claude it *must* brainstorm before creative work. If you have already grilled, say so explicitly, or you will get interviewed twice. User instructions take precedence over skills, so a single sentence is enough.

Use `/grill-me` alone for anything that is not code: a hiring plan, a talk outline, an architecture decision you are not implementing today. Use Superpowers alone when the task is a well-understood feature and you want the whole pipeline with minimal ceremony.

---

## 5. Troubleshooting

**`/grill-me` does nothing.** It is a one-line skill whose body is "run `/grilling`", so the `grilling` skill must be installed too. Installing the whole plugin avoids this.

**`/grill-with-docs` asked everything at once with no recommendations.** It did not actually load `grilling`. This is a known rough edge: a skill that names another skill does not always cause it to load. Ask "did you load the grilling and domain-modeling skills?" and it usually recovers.

**Grilling answered its own questions.** That is a bug in the run, not the design. It happens most when another skill runs grilling inside a "resolve this ticket" frame. Tell it the decisions are yours.

**Superpowers skills stopped triggering after a long session.** The bootstrap is re-injected after compaction in Claude Code, so this should be rare. If it happens, run `/clear` or start a fresh session.

**Superpowers is too heavy for a trivial change.** It is meant to be. The brainstorming skill's own anti-pattern table argues that "too simple to need approval" is exactly where wasted work comes from. If you truly want it off for one task, say "skip brainstorming for this" and it will comply.

---

## 6. Where to read more

- Matt Pocock's skills: https://github.com/mattpocock/skills (the `docs/` folder has a page per skill)
- Superpowers: https://github.com/obra/superpowers and the launch post at https://blog.fsck.com/2025/10/09/superpowers/
- Claude Code plugins: https://code.claude.com/docs/en/plugins
