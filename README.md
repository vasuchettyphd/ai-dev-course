# Think It Through, Then Build It: `/grill-me` and Superpowers in Claude Code

*A hands-on guide for people who want to use Claude Code to make money or start a business, not to become software engineers.*

Claude Code will happily build you almost anything you describe. That is the problem. Describe a tool in a hurry and it builds exactly what you said, which is rarely what you meant, and you find out only after the work is done. Two free add-ins fix this from opposite ends:

- **`/grill-me`** (from Matt Pocock's `mattpocock-skills`) turns Claude into a relentless interviewer. It questions your idea until every hidden assumption is on the table, before a single thing gets built. Great for a business decision on its own, and great before you build anything.
- **Superpowers** (from Jesse Vincent's `superpowers`) is a build process. Once the plan is clear, it makes Claude work in small, tested steps and review its own work, instead of dumping a big pile of code that looks right and quietly does the wrong math.

To make this concrete, we will carry one project the whole way through: **a rental property deal screener**. You feed it a listing's numbers, it tells you the monthly cash flow, the cap rate, the cash-on-cash return, and whether the deal clears your bar. First you will use `/grill-me` to pin down what a good deal even means to you. Then you will use Superpowers to build the calculator so its numbers are actually correct, because a wrong formula here is a wrong buying decision.

You do not need to know how to code to follow along. That is the whole point.

Versions covered: `mattpocock-skills` 1.2.3 and `superpowers` 6.3.0, from the official marketplace in September 2026.

---

## 1. Before you start

**What you need:**

- Claude Code installed and working (the tool you are already reading this in).
- An empty folder to work in. Make one called `deal-screener` and open Claude Code inside it.
- Nothing else. Claude will set up whatever the project needs, including the programming language, so you do not have to.

**Install the two add-ins.** They live in Anthropic's official marketplace, so there is nothing to sign up for. From inside a Claude Code session, type:

```
/plugin install mattpocock-skills@claude-plugins-official
/plugin install superpowers@claude-plugins-official
```

Then restart the session. Superpowers only switches on in a fresh session, so close and reopen Claude Code once after installing.

**Check they loaded.** Type `/` and start typing `grill`. You should see `/grill-me` in the list. Do the same with `superpowers`.

That is the entire setup. The rest of this guide is the two tools in action.

---

## 2. `/grill-me`: the interview that will not let you hand-wave

### What it is for

`/grill-me` interviews you about a plan, a decision, or an idea until you and Claude genuinely agree on what you are doing. You do not need a finished plan to start. Producing one is the whole point of the session, and vagueness is exactly what it feeds on.

It writes no files and changes nothing. The only thing it leaves behind is a much sharper version of the idea in your own head. That makes it useful far beyond software: people point it at pricing decisions, whether to take a job, a pitch they are about to give, a property they are about to bid on.

### Two names for the same thing

You will see both `/grill-me` and `/grilling`. They run the identical interview. `/grill-me` is the one you type. `/grilling` is the engine underneath that Claude can also start on its own. For everyday use, just type `/grill-me` and forget the distinction exists.

### How it decides what to ask

Three ideas run the whole thing:

| Term | What it means |
|---|---|
| **Design tree** | Your idea, broken into decisions, and the smaller decisions that hang off each one. |
| **Frontier** | The decisions it can honestly ask about right now, because everything they depend on is already settled. |
| **Round** | One batch of questions, all from the current frontier, asked together and answered together. |

The practical effect: it does not drip one question at a time, and it does not dump fifty at once. Each round holds only questions that do not depend on each other. Your answers unlock the next layer, and the next round asks what those answers opened up. A session with forty questions usually lands in three or four rounds, not forty.

### What a round looks like

Every question comes in the same shape: a number, a short title, the question, then Claude's own recommended answer on the arrow line.

```
❓ **Q1** - **Your minimum return**: What is the lowest cash-on-cash return
   you would accept before a deal is worth your time and risk? Common bars
   for a first rental are 8% to 12%.

➡️ Start at 10%. It clears a savings account and index funds by enough to
   pay you for the hassle of being a landlord, without being so strict that
   nothing in your market qualifies.

---

❓ **Q2** - **Vacancy assumption**: Every rental sits empty sometimes. What
   share of the year should we assume it earns nothing, so the numbers are
   honest? Typical is 5% to 8%.

➡️ 8%. Better to be pessimistic. A deal that only works at 0% vacancy is
   not a deal.
```

Because the questions are numbered, you answer the whole round in one line:

> 1 yes, 10% is right. 2 make it 5%, my market is tight and units rarely sit empty.

You never have to quote the question back.

### It looks things up so you do not have to

Here is the rule that makes it trustworthy: **finding facts is Claude's job, making the calls is yours.**

If a question needs a fact it can go find, like a typical property tax rate in your state or current mortgage interest rates, Claude goes and researches it rather than making you look it up. It does not stall the whole interview to do that, it only pauses the questions that actually depend on the answer.

The judgment calls, though, are always handed to you. What return you require, how much risk you will take, which neighborhoods you would actually own in: those are yours, and a good session never quietly answers them for you. If you ever catch it deciding one of these on your behalf, say so and it will reopen the question.

### It stops and waits for your sign-off

The interview is not over when the questions run out. It is over when **you** say the two of you agree. Claude should not run off and start building until you confirm. If it jumps ahead, tell it to stop.

### Try it yourself: grill your buy box

Open Claude Code in your `deal-screener` folder and type this, in your own words:

```
/grill-me I want to define my rules for whether a rental property is a
good deal, so I can screen listings quickly. Help me pin down my criteria.
```

**Round 1** will ask the things that stand on their own: your minimum return, how you will pay for it (all cash, or a mortgage, and on what terms), what counts as an expense, how pessimistic to be about vacancy and repairs. Claude may go research typical tax and insurance rates for your area while you answer the rest.

**Round 2** exists only because of your Round 1 answers. If you said you will use a mortgage, it now asks about your down payment and interest rate. If you said you want appreciation to count, it asks how much yearly growth is fair to assume without kidding yourself.

**Round 3** is usually the short one: how to rank two deals that both pass, whether to flag deals that are close but not quite, what a "no" should tell you.

When the questions run dry, Claude lays out your finished buy box and asks you to confirm it. Notice what happened: you now have a written, defensible set of rules, and you never had to stare at a blank page. That set of rules is what you will hand to the build step next.

### Getting real value out of it

The difference between a session that sharpens your thinking and one that just agrees with you is you.

- **Push back.** The failure mode is nodding along, answering "yes, yes, yes" for forty questions, and walking away with a plan Claude wrote and you rubber-stamped. If a recommendation is wrong for you, say so and say why.
- **"I don't know" is a real answer.** Some things you genuinely cannot decide by talking, like how a property "feels" in person. Say you do not know, and treat that as a signal to go find out rather than guess.
- **Start fresh.** Run it in a new conversation, not on top of a plan you already talked Claude into. The interview is for forming the plan, not defending one.
- **Count rounds, not questions.** Forty questions over four rounds is normal. If it asks two hundred, your topic was too big; ask it to break the topic into pieces and grill them one at a time.
- **Use the strongest model you have.** This skill leans on Claude's own sense of how plans fall apart, more than most. Give it your best model for the interview.

You know it worked if you disagreed with something along the way, if a question surfaced a decision you had been making without realizing it, and if you could now defend each choice to someone who was not in the room.

### Prefer one question at a time?

Some people find a whole round at once overwhelming. If that is you, add this line to your global `CLAUDE.md` file and grilling will slow down to one question per message:

```
When grilling, ask one question at a time.
```

This is a supported setting, not a workaround.

---

## 3. Superpowers: a careful build process

### What it is

Superpowers is a set of habits that switch on automatically once installed. From the moment Claude sees you want to build something, it stops itself from diving into code. Instead it draws the plan out of you, writes it down, breaks it into small steps, builds each step, tests it, and reviews its own work before calling anything done.

There is no single command to remember. It just changes how Claude behaves. You can also invoke a specific piece by name, like `/superpowers:brainstorming`, but most of the time you simply describe what you want and it takes over.

### Why a business person should care

Left alone, an AI will write a financial calculator that looks completely correct and returns the wrong number, because a formula was subtly off. You would not notice until you had passed on a good deal or bought a bad one. Superpowers' core habit, called test-driven development, forces Claude to first write a check that says "for these inputs, the answer must be exactly this," watch it fail, then write the formula, then watch the check pass. For money math, that is the difference between a tool you can trust and a toy.

### What is inside

The build runs through these stages, in order:

| Stage | What happens |
|---|---|
| **Brainstorming** | Claude refines your idea into a clear design and gets your approval before building anything. |
| **Planning** | It breaks the approved design into small, specific steps. |
| **Building with tests** | For each step it writes the test first, then the code, so wrong answers are caught immediately. |
| **Reviewing** | It checks its own work against the plan and flags problems before you ever see them. |
| **Finishing** | It confirms everything passes and helps you wrap up cleanly. |

There is more in the box (a careful debugging process, for one), but that is the spine.

### The one rule to know: it asks before it builds

Superpowers will not write code until it has told you what it intends and you have said yes. This holds even for tiny changes. The plan it shows you might be two sentences, but the "go ahead?" never gets skipped. This is deliberate: the tasks that feel too simple to plan are exactly where wasted work comes from.

It also sizes its effort to the job. A quick question gets a quick answer. A whole new tool gets the full treatment: a few proposed approaches, a design you approve piece by piece, then the build.

### Try it yourself: build the deal screener

Still in your `deal-screener` folder, and armed with the buy box you defined in the grilling session, type:

```
Let's build the rental deal screener we just designed. I'll give it a
listing's numbers and it should tell me monthly cash flow, cap rate,
cash-on-cash return, and whether it passes my buy box.
```

Here is what you should see happen, and what to do at each point:

1. **Claude proposes a design and stops.** It will describe how the tool takes inputs and what it outputs, and ask if that is right. Read it. Correct anything that does not match your buy box. Say go.
2. **It plans, then builds in tested steps.** For the core formulas, watch it write a test first. It will state, for a specific example property, exactly what the cash-on-cash return should be, confirm the code gets that number, and only then move on. This is the part that keeps the money math honest.
3. **It reviews its own work** and reports anything questionable before handing it back.
4. **It shows you the finished tool** and how to run it.

You will end up with a working screener and, just as important, a set of tests proving its numbers are right. Change a formula later and a broken test tells you instantly.

### A note on the mockup helper

While designing something visual, Claude may offer to open a browser tab to show you layouts instead of describing them. Accept if a picture would help, decline if not. One heads-up: that helper quietly loads a small logo from the plugin author's website, which they use to count how many people use the plugin. If you would rather it did not, set `SUPERPOWERS_DISABLE_TELEMETRY=1` in your environment.

---

## 4. Using both together: the full arc

The two tools meet at one moment, the thinking that happens before building, and they handle it differently.

| | `/grill-me` | Superpowers |
|---|---|---|
| Rhythm | A whole batch of questions per round, answered by number | One question at a time, conversational |
| Good for | Any decision, including ones with no software at all | Building and fixing software |
| Ends by | Handing you a sharp plan, then stopping | Flowing straight into building the thing |

The deal screener used both in the natural order, and this is the pattern worth remembering:

1. **Think it through with `/grill-me`.** Nail down your buy box: your criteria, your assumptions, what "good" means. No code yet.
2. **Confirm you and Claude agree.** Do not skip this. It is the whole safety of the approach.
3. **Hand it to Superpowers to build.** Say something like: "We already worked out the design together. Treat that as approved and start building." Then let its tested, reviewed process turn your rules into a working tool.

One thing to watch: Superpowers likes to run its own brainstorming before building. If you already grilled the idea, just say so ("we've already designed this, go ahead and build"), and it will not interview you a second time.

And you do not always need both. Use `/grill-me` alone for a decision you are not building anything for, like whether to take on a particular investment or how to price a service. Use Superpowers alone when you already know exactly what you want built.

---

## 5. When something goes wrong

**`/grill-me` does nothing.** The full `mattpocock-skills` plugin has to be installed, not just part of it. Reinstall the whole plugin.

**It asked everything at once with no recommendations.** It did not fully start the interview engine. Ask it directly, "did you load the grilling skill?", and it usually recovers.

**It started answering its own questions.** That is a bug in that run, not how it should work. Remind it that the decisions are yours to make, and it will hand them back.

**Superpowers stopped being careful in a long session.** Rare, but if it happens, start a fresh session and it comes back.

**Superpowers feels like too much ceremony for something tiny.** That is by design; the "too simple to bother planning" jobs are where mistakes hide. If you genuinely want to skip it for one small task, say "skip brainstorming for this" and it will.

---

## 6. Where to read more

- Matt Pocock's skills, with a page explaining each one: https://github.com/mattpocock/skills
- Superpowers, and the essay behind it: https://github.com/obra/superpowers and https://blog.fsck.com/2025/10/09/superpowers/
- Claude Code plugins in general: https://code.claude.com/docs/en/plugins
