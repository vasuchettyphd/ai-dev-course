---
marp: true
paginate: true
title: Week 4 - Planning a project
style: |
  section { font-size: 28px; }
  table { font-size: 22px; }
  pre { font-size: 20px; }
  .small { font-size: 20px; color: #555; }
---

# Week 4: Planning a project

AI Development Course

<p class="small">Tested with Claude Code 2.1.296, mattpocock-skills 1.2.3, superpowers 6.4.1 and AI-DLC 2.11.0 on Ubuntu Linux (in a container), 12 October 2026, without signing in. Everything inside a signed-in session, on GitHub, or on a Mac or in Windows (WSL) is being tested on real Mac and Windows laptops.</p>

---

## Today

- Why plan first
- Pick your idea: the too-big test, and keeping sensitive data out
- Your project repo, private
- Plan mode, then `/grill-me`
- `PLAN.md`, through a pull request
- Two other ways to plan (demo): Superpowers and AWS AI-DLC
- The assignment, and next week

---

## Why plan first

Claude Code builds exactly what you said, which is rarely what you meant.

| Layer | What it does | You get |
|---|---|---|
| **Plan mode** | Reads and thinks; can't change files | A first draft, on screen |
| **`/grill-me`** | Questions your plan, round by round | Sharper decisions |
| **`PLAN.md`** | The decisions, in a fixed outline, merged by PR | The plan, saved in your repo |

---

## Pick your idea

A good idea:

- does **one job** for **one kind of person** (you count)
- fits in one sentence: "It takes ___ and gives me ___"
- uses data you can **type in, make up, or are allowed to use**
- has **3 to 5 must-haves**
- can be shown working in **3 minutes** in week 14

Bonus: a part where AI could help later (summarise, sort, draft).

---

## The too-big test

Too big if it's "a platform", needs several kinds of users or logins, takes payments, copies live data from websites, or uses other people's private data.

| Too big | Just right |
|---|---|
| An app that runs my whole small business | Weekly sales spreadsheet in, one-page summary out |
| A tutor and student marketplace | A study planner for my exam dates |
| An AI financial adviser | A budget checker with my own limits (no bank connection) |
| A real estate investing platform | A rental deal screener for one listing (class example) |

---

## Example ideas, about the right size

1. Rental deal screener (the class example, in `example-project/`)
2. Freelance quote calculator
3. Club event budget planner
4. Sales summary from a spreadsheet export
5. Job application tracker with follow-up drafts
6. Product description writer for a small shop
7. Café reorder checker
8. Customer feedback sorter (public or made-up reviews)

---

## Keep sensitive personal data out

Never in your project:

- health or medical information
- account, card or ID numbers
- other people's private information: customers, employees, classmates' grades
- passwords, keys, sign-in codes
- anything you aren't allowed to use

Use **made-up**, **public**, or your own non-sensitive data. (Again in week 13.)

---

## Your project repo (being tested)

In your terminal:

```bash
cd ~ && mkdir semester-project && cd semester-project && claude
```

`Shift + Tab` until `manual mode on`. Then ask Claude Code to create `README.md` with your idea, commit it, and:

```bash
gh repo create semester-project --private --source=. --remote=origin --push
```

**Before you say Yes, look for `--private`.** Plain **Yes** for git, always.

Check github.com: **your** username, and the **Private** label.

---

## Invite your instructor (being tested)

On github.com, as in week 3:

1. Your repo, then **Settings**
2. **Collaborators**, then **Add people**
3. Type `vasuchettyphd`, select it
4. **Add vasuchettyphd to semester-project**

**Don't make the repo public.** The invitation is how your instructor gets in.

---

## Plan mode (being tested)

`Shift + Tab` until the bottom line says `plan mode on`:

```text
auto mode on -> manual mode on -> accept edits on -> plan mode on
```

Or type `/plan` before one prompt.

```text
I want to build this for my semester project: "...". I'm not a
programmer, and I have about eight weeks. Don't build anything yet.
Propose a plan: who it's for, the 3 to 5 must-haves, what to leave
out, what data it uses, and the first three build steps.
```

---

## Don't approve it for building

Claude shows the plan and asks how to proceed. Labels vary:

| Choice | Means |
|---|---|
| "Yes, and use auto mode" / "Yes, auto-accept edits" | **start building** |
| "Yes, manually approve edits" | **start building** |
| **"No, keep planning"** | stay in plan mode, tell Claude what to change |

This week: **No, keep planning**. Happy with it? Then `Shift + Tab` until `manual mode on`.

<p class="small">Claude Code keeps its own copy in ~/.claude/plans/. Your PLAN.md goes in your repo (step 6).</p>

---

## Install `/grill-me` (mattpocock-skills) (being tested)

In Claude Code:

```text
/plugin install mattpocock-skills@claude-plugins-official
```

Choose **Install for you (user scope)**. Asked to? `/reload-plugins`.

Or in your terminal (from our test):

```text
$ claude plugin install mattpocock-skills@claude-plugins-official
✔ Successfully installed plugin: mattpocock-skills@claude-plugins-official (scope: user)
```

"Not found in marketplace"? Add the official marketplace first (README, step 5a).

Check: type `/grill` and look for `/grill-me`.

---

## Get grilled (being tested)

```text
/grill-me Grill me on the plan you just proposed for my semester project.
```

Not in the list? `/mattpocock-skills:grill-me`

- **Rounds** of **numbered questions**, each with a **recommended answer**
- Reply by number: `1 yes. 2 no, only me. 3 I don't know yet.`
- Facts are Claude's job; **decisions are yours**. Push back.
- It writes **no files**. An edit prompt? Say **No**.

Note your **three hardest questions** and your answers.

---

## How it ends

It ends when nothing is left open, and **you** confirm you agree:

```text
Yes, we agree.
```

Out of time, or going in circles?

```text
Stop grilling, summarise the decisions so far
```

Anything undecided goes under **Open questions**.

Stopping before it ends (end of class)? Copy the summary into your note. Next time: `claude` in `~/semester-project`, `/grill-me`, paste it, add `Carry on grilling me from here.`

---

## `PLAN.md`: the fixed outline

```text
# Plan: <your project's name>
## Goal
## Who it's for
## Must-haves
## Not in this version
## Data it uses
## First three build steps
## Open questions
```

Be specific. "Easy to use" is vague. "Shows the week's total sales in dollars, and the top 3 products" is specific.

Worked example: `example-project/PLAN.md` (the deal screener).

---

## Branch, pull request, merge (being tested)

```text
Make a new branch called add-plan. On it, write PLAN.md from our
grilling session, with exactly these seven headings, in order: ...
Use my answers. Be specific. Show it to me before you commit.
```

Then: commit, push, `gh pr create` ("Add project plan").

On GitHub: **Files changed**, then **Merge pull request**, then **Confirm merge**.

Back in Claude Code: "Switch back to main and pull the latest changes from GitHub."

---

## Two other ways to plan (demo, optional)

| | Plan mode + /grill-me | Superpowers | AWS AI-DLC |
|---|---|---|---|
| How it plans | Draft, then rounds of numbered questions | One question at a time, 2-3 approaches, approve section by section | Phases, one stage at a time, approval gates |
| Produces | Nothing; you ask for `PLAN.md` | Design and plan files in `docs/superpowers/` | Records in `aidlc/`, ~40 skills in `.claude/` |
| Use it for | Deciding what to build | Building in small, tested steps | Team software projects |

**Next week you build with Superpowers.**

---

<style scoped>section { font-size: 23px; }</style>

## Trying them yourself (optional)

Only **after your `PLAN.md` PR is merged**, in a **throwaway folder**:

```bash
mkdir -p ~/planning-sandbox && cd ~/planning-sandbox && git init && claude
```

**Superpowers:** `/plugin install superpowers@claude-plugins-official`, then `/superpowers:brainstorming ...`. User scope means it's on in **every** folder, so remove it afterwards, in your terminal: `claude plugin uninstall superpowers@claude-plugins-official` (or `/plugin uninstall superpowers@claude-plugins-official` in Claude Code, being tested). If Claude Code is open, type `/reload-plugins`.

**AI-DLC** (Windows: the Ubuntu window). It gives Claude a very broad edit permission (exact reach being tested). Use its own folder:

```bash
mkdir -p ~/aidlc-sandbox && cd ~/aidlc-sandbox && git init
curl -fsSL https://github.com/awslabs/aidlc-workflows/releases/latest/download/install.sh | sh
aidlc config --harness claude && aidlc doctor
```

<p class="small">Then /aidlc ... in Claude Code. Runs are being tested.</p>

---

## Assignment

One document with:

- Your **private** project repo's address, a screenshot showing **Private**, `vasuchettyphd` added
- The address of the **merged** PR that adds `PLAN.md`
- Your **three hardest `/grill-me` questions**, your answers, and how one changed your plan

| Criterion | Points |
|---|---|
| Repo private (screenshot) and collaborator added | 3 |
| `PLAN.md`: outline (1), specific and no sensitive data (1), merged by PR (2) | 4 |
| Three grilling questions, answers, and what changed | 3 |

---

## Next week: Building with AI

You build the **first steps of your `PLAN.md`**, with Superpowers.

Bring:

- your merged `PLAN.md`
- your open questions, answered if you can
