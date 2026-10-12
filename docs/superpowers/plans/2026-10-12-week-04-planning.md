# Week 4 (Planning a project) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 4. Students:
- choose their semester project idea
- create a new private project repo with the instructor as collaborator
- plan the project in Claude Code plan mode
- stress-test it with `/grill-me`
- write `PLAN.md`
- merge it through a pull request

AWS AI-DLC and Superpowers are shown by the instructor in a demo and compared, and are optional for students. The week also adds `example-project/` with the deal screener's plan, plus slides, the assignment, instructor notes (including a demo script) and test checklist rows.

**Architecture:**
- Same approach as weeks 2-3.
- Every plugin, command and product fact comes from official sources (Claude Code docs, the official plugin marketplace, the plugin repositories, `awslabs/aidlc-workflows`) and is recorded on a fact sheet with its URL.
- Plugin installation is tried for real in a container where possible.
- Anything that needs a signed-in Claude session is marked "being tested" and gets rows in the instructor's checklist.

**Tech Stack:** Markdown, Marp (`npm run slides` in Docker), Docker `ubuntu:24.04`, Claude Code (native installer).

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 4 row. The week 4 design was approved in conversation on 2026-10-12. Decisions:
- Plan mode plus `/grill-me` is hands-on for students.
- AI-DLC and Superpowers are an instructor demo plus a comparison, optional for students.
- The semester project gets a new private repo (`my-first-project` stays practice), and `vasuchettyphd` is re-added as a collaborator.
- `example-project/` holds the deal screener plan, tagged `week-04` after merge.

## Global Constraints

- Audience: business and non-CS students in week 4. They can use Claude Code, git and `gh` from weeks 2-3. Plain language. Every command and prompt shown exactly, labelled with where to type it (Terminal, the Ubuntu window, or inside Claude Code).
- Platforms: Mac (Apple chip), Mac (Intel), and Windows (WSL Ubuntu). This week installs only a Claude Code plugin, which is the same inside Claude Code on every platform. Say so.
- The project repo is private. Students check for `--private` before approving, add `vasuchettyphd` as a collaborator, and always pick plain "Yes" for git prompts (from week 3).
- Project ideas must avoid sensitive personal data (health, financial account numbers, other people's private information) and anything the student isn't allowed to use. Say this plainly, because it matters again in week 13.
- Every fact comes from the fact sheet with its URL. Anything not observed is marked "being tested". Pin the plugin versions tested.
- No em dashes (U+2014). The rubric is a table under `## Rubric` with points in the last column, totalling 10.
- `example-project/` is clearly labelled as the instructor's worked example. It contains a `README.md` and `PLAN.md` only, and passes `scripts/check_course.py`.
- Instructor-only material goes in the private repo.
- Branch `week-04-planning` in the course repo and `week-04` in the instructor repo. The user merges, and links come first, one bare URL per line.

## Review Focus

1. **Plugin install command or name is wrong**, so students get stuck at the start. Exact strings come from the official marketplace and plugin docs.
2. **The student approves plan mode's proposal and Claude starts building.** Explain that approving a plan can switch modes and start work (week 2 lesson). This week the plan is not approved for building: students choose to keep planning or exit.
3. **The grilling never ends, or the student doesn't know how to stop it.** Say how to end it or move to writing the plan.
4. **The project repo is created public, or under the wrong account**, or `PLAN.md` is pushed to `main` directly. Reuse week 3's checks and the branch-and-PR loop.
5. **Over-scoped ideas.** Give a concrete "too big / just right" test with examples.

---

### Task 1: Fact sheet and dry run

**Files:** none in the repo. Write the report only.

- [ ] **Step 1: Fact sheet.** Record each fact with its URL:
  - Claude Code plan mode: how to enter it, what it does and doesn't do, what happens when a plan is approved, and how to keep planning or exit.
  - The plugin system: `/plugin`, the official marketplace name, the exact install command for `mattpocock-skills`, how to confirm it is installed, and how to update or remove it.
  - The `/grill-me` skill. Read its actual skill file in the plugin source and record:
    - what it says it does
    - how it asks questions (one at a time or in batches)
    - how it ends and what it produces
    - any companion skill such as `grill-with-docs`, if real
  - Superpowers: its install command from the official marketplace, the brainstorming and planning skills it offers, and what it produces (a spec and plan files). Read its source.
  - AWS AI-DLC from `awslabs/aidlc-workflows`:
    - what it is
    - how it is used with Claude Code (exact setup steps from its README)
    - its phases
    - what files it produces
  - The existing advanced tutorial `advanced/grill-me-superpowers/README.md`. Note what it already covers, so week 4 can link to it rather than repeat it.
- [ ] **Step 2: Dry run in a clean `ubuntu:24.04` container, as a non-root user.**
  - Install Claude Code with the native installer.
  - Try the plugin marketplace and install steps non-interactively, if the CLI supports it without signing in (for example `claude plugin marketplace add` and `claude plugin install`, only if documented). Record exactly what works and what requires signing in.
  - Clone `awslabs/aidlc-workflows` read-only and record its structure and setup instructions.
  - Never sign in and never enter credentials.
- [ ] **Step 3:** Write the facts, the transcript, the versions (Claude Code, plugin versions or commit hashes) and the date to the report.

### Task 2: README, slides, assignment and example project

**Files:**
- `weeks/04-planning/README.md` (replace the stub, starting from `templates/README.md`)
- `weeks/04-planning/slides.md` and `slides.pdf`
- `weeks/04-planning/assignment.md`
- `example-project/README.md` and `example-project/PLAN.md`

- [ ] **README:** follow the approved design, steps 1-8:
  1. Why plan first: link to `advanced/grill-me-superpowers/` for depth.
  2. Pick your idea: the checklist, a too-big vs just-right test, about 8 example ideas, and the sensitive-data rule.
  3. Make the project repo: new private repo, the `--private` check, collaborator, plain Yes for git.
  4. Plan mode.
  5. Install `mattpocock-skills` and run `/grill-me`. Explain how to stop.
  6. Write `PLAN.md` from the grilling, then branch, PR and merge (from week 3). Give `PLAN.md` a fixed outline:
     - goal
     - who it's for
     - must-haves
     - not in this version
     - data it uses
     - first three build steps
     - open questions
  7. Two other ways to plan: AI-DLC and Superpowers, as a comparison table (what it is, how it plans, what it produces, when to use it) and how to try each. Mark optional.
  8. Check it worked, and troubleshooting.

  Put "being tested" notes on everything that needs a signed-in session, unless the fact sheet observed it. In "Tested with", give the Claude Code and plugin versions and the date, and say exactly what was tested.
- [ ] **example-project:**
  - `README.md`: what the deal screener is and that this is the instructor's worked example; it grows week by week, and each week's state is a git tag.
  - `PLAN.md`: the deal screener plan in the exact outline above. Base it on the existing advanced tutorial's deal screener (its buy-box criteria and formulas), and cite that file.
- [ ] **Slides:** 16-20 slides, matching the README. Build with `npm run slides`, then restore any other week's PDF the build rewrote. Render the slides to PNG and look at them.
- [ ] **Assignment:**
  - **Hand in:**
    - the project repo URL, private with a screenshot of the Private label, and `vasuchettyphd` added
    - the merged PR URL that adds `PLAN.md`
    - the three hardest `/grill-me` questions and their answers
  - **Rubric:**
    - Repo private, with screenshot and collaborator: 3 points
    - `PLAN.md` follows the outline and is specific, merged via a PR: 4 points
    - The grilling reflection: 3 points
    - Total: 10 points
- [ ] **Checks:** `python3 scripts/check_course.py` prints OK. No em dashes. A command-to-source table in the report.

### Task 3: Instructor notes, demo script and checklist rows (private repo)

- [ ] `weeks/04-planning/notes.md`, with the four headings:
  - **Timing:** a 75-minute plan.
  - **Common problems:**
    - the plugin won't install
    - `/grill-me` not found
    - plan mode starts building
    - endless grilling
    - over-scoped ideas
    - ideas with sensitive data
    - the repo was made public or under the wrong account
  - **Discussion answers.**
  - **Grading guidance:** worked 10/10 and 6/10 examples that add up under the rubric.

  Also a **demo script** for AI-DLC and Superpowers on the deal screener. List the exact commands and prompts, what to point out, about 10 minutes each, and a fallback if the live demo fails.
- [ ] `weeks/04-planning/test-checklist.md`: Mac and Windows rows for every README step, in the same format as weeks 2-3.
- [ ] No em dashes. Commit on `week-04`.

### Task 4: PRs, tag and tracking (controller)

- [ ] Push both branches and open the PRs. Give the user the bare PR links first.
- [ ] After merge, tag the merge commit `week-04` and push the tag. Close the OpenProject task "Week 4: Planning a project".
