# AI Development Course: design

Date: 2026-10-10. Status: approved 2026-10-10.

## Goal

Turn `ai-dev-course` from six standalone advanced tutorials into a full 14-week course for a class at Utah Valley University. It starts from the basics (what AI is, setting up Claude Code, git) and ends with students demoing a small AI-powered tool they built themselves. The six existing tutorials become optional advanced topics for after the core course.

**Success looks like this:** a student with no coding background can follow the weeks in order, using only the repo and a Claude Pro plan, and finish with a working, containerized, evaluated project of their own.

## Audience and constraints

- **Students:** business and other non-CS majors, with little or no coding. They want to build useful tools, not become software engineers. All material uses plain language and shows every command.
- **Format:** a semester of weekly sessions. 14 teaching weeks, plus one buffer week in a roughly 15-week UVU semester. Amended 2026-10-24, see "Session schedule" below.
- **Student cost:** each student buys Claude Pro (about $20/month), which covers Claude Code. Weeks 9-11 call a model from the student's own code, which Pro does not cover, so students also need about $5 of one-time API credit. The syllabus states both costs up front.
- **Platforms:** macOS and Windows (via WSL). Steps that can only be tested on WSL are marked "untested on native Windows" until someone confirms them.
- **Visibility:** the course repo is public. Instructor notes and answer keys go in a separate private repo.
- **Style:** no em dashes anywhere. Each tutorial pins the tool versions it was tested on.

## Course schedule

| Wk | Topic | In class | On their own project |
|---|---|---|---|
| 1 | What AI is | Probability and next-token prediction, tokens, embeddings, attention (*Attention Is All You Need*, explained intuitively), training vs. using a model, why models make things up | List 3 problems from their work or life that AI might help with |
| 2 | Setting up Claude Code | Install on Mac or Windows (WSL), sign in, first session, CLAUDE.md, what costs money | Working setup; ask Claude to explain a file |
| 3 | Git and GitHub | Repos, commits, branches, PRs, using git through Claude Code | Create their project repo |
| 4 | Planning | Plan mode with `/grill-me`, AWS AI-DLC (`awslabs/aidlc-workflows`) and Superpowers, compared on the deal screener | Choose an idea, get grilled on it, write the plan |
| 5 | Building with AI | Building with Superpowers (decided in week 4): small steps, tests first | First working version |
| 6 | Reviewing code | Several reviewers with different focuses; reading a diff without being a coder | Review their own build and fix what's found |
| 7 | Running what you build | Docker: why "works on my machine" isn't enough, running the app in a container | Containerize their project |
| 8 | Debugging with AI + midterm check-in | Reproduce, narrow down, avoid the "fix it" loop | Demo version 1 to a classmate |
| 9 | Calling a model from code | API keys, tokens, cost, temperature, structured output, choosing a model | Add one AI feature |
| 10 | Embeddings and RAG | Search by meaning, chunking, retrieval, grounded answers | Add RAG over their own documents |
| 11 | Tools, agents and MCP | Tool use, agent loops, MCP servers | Give their feature one tool |
| 12 | Evaluation | Test sets, accuracy, "it looked right" isn't evidence (Jev as the case study) | 20-case test set and a reported score |
| 13 | Security and responsible use | Leaked keys, prompt injection, privacy, bias, licensing, academic integrity | Security review of their project |
| 14 | Final demos | Presentations | Demo and a short write-up |

**Advanced topics** come after the core weeks and are optional extra credit or further study: dbt, running a local LLM in Docker, Jev, the Wordle agent, `/grill-me` and Superpowers in depth, and Beads. Week 12 uses Jev as its case study, and Beads is offered as an optional extra in week 5.

## Session schedule (amended 2026-10-24)

The class meets on Thursdays in Spring 2027, 2.5 hours a session, twice the 75 minutes the weeks were written for. The 14 week folders stay as they are (folder names, example-project tags and links don't change); the root README maps them to 14 sessions:

- Session 1 does week 1 (shortened) and nearly all the setup: week 2 and week 3 steps 1 to 4. Pro, WSL and a GitHub account are done before it.
- Session 2 is week 3 steps 5 to 9 and week 4. Session 5 is week 7 and the in-class part of week 8 (the peer demo). Weeks 6 and 7 are not paired, because week 7's review needs week 6's reviewers on `main`.
- Weeks 5, 6 and 9 to 13 each keep a session to themselves, and use the extra time as supervised work time.
- Session 11 is the seven add-ins tour; session 12 is the Wordle agent, then Beads or dbt. Together they are one 10-point grade: 5 points for each of two advanced topics tried.
- One buffer session (catch-up and rehearsal) comes before demo day. Spring break (Mar 15 to 21) has no class.

Session-by-session timing is in the instructor repo's `sessions.md`.

## Repository layout

```
ai-dev-course/                       public
  README.md                          syllabus: schedule, costs, setup before week 1, grading
  package.json                       Marp CLI; `npm run slides` builds every slides.md to PDF
  weeks/
    01-what-is-ai/
      README.md                      hands-on tutorial
      slides.md                      Marp deck
      assignment.md                  project task, hand-in, rubric
    02-claude-code-setup/
    03-git-and-github/
    04-planning/
    05-building-with-ai/
    06-reviewing-code/
    07-running-with-docker/
    08-debugging/
    09-calling-a-model/
    10-embeddings-and-rag/
    11-tools-agents-mcp/
    12-evaluation/
    13-security-and-responsible-use/
    14-final-demos/
  advanced/
    dbt/  local-llm-docker/  jev/  wordle-agent/  grill-me-superpowers/  beads/
  example-project/                   rental deal screener, git-tagged week-04 ... week-13
  docs/superpowers/specs/            this file

ai-dev-course-instructor/            private
  README.md
  weeks/<same names>/notes.md        timing, common problems, answers, grading guidance
```

## What each week contains

- **README.md:** the hands-on tutorial. Sections: goal, before you start, steps, check it worked, troubleshooting. Every command is shown with its expected output, and those outputs come from real runs. The README lists the tool versions it was tested with.
- **slides.md:** a Marp deck of 15-25 slides for the lecture part (concepts and diagrams). For hands-on steps it points to the README instead of repeating them.
- **assignment.md:** the task for the student's own project, what to hand in, and a rubric of 3-4 criteria on a 10-point scale. Week 14 has a larger final-project rubric.
- **Instructor notes:** in the private repo, not the public one. They cover session timing, likely student problems (especially on Windows), discussion answers and grading guidance.

## Example project

`example-project/` holds the rental deal screener from the existing `/grill-me` and Superpowers tutorial. It is built up week by week, with a git tag for each week's finished state (`week-04` through `week-13`). In-class demos start from the previous week's tag. Students who fall behind can see what "done" looks like for any week.

## Build sequence

1. **Restructure PR (no new content):**
   - Move the six tutorials to `advanced/<name>/` with `git mv`, so their history follows them.
   - Fix the clone paths in their READMEs.
   - Add `weeks/01-...` through `weeks/14-...`, each with a stub README showing its title and "coming soon".
   - Add the Marp setup.
   - Rewrite the root README as the syllabus.
   - Create the private instructor repo with matching empty week folders.
2. **One PR per week, in teaching order (1 to 14).** Each contains that week's README, slides and assignment, the matching instructor notes in the private repo, and from week 4 onward the `example-project` changes and tag.
3. Each week gets its own OpenProject task under "Tutorials and Teaching" (project id 4), closed when its PR merges.

## Verification for every week

- **Run it for real:** every README command is run on a clean setup, and its output quoted. Windows-only steps are marked "untested on native Windows" unless someone confirms them on native Windows.
- **Slides build:** `npm run slides` builds the deck to PDF without errors.
- **Rubric fit:** the rubric matches what the assignment asks for.
- **Style:** no em dashes, and plain language suited to non-coders.
- **Week 1 fact-check:** week 1 has no commands to run, so it gets a fact-check pass instead. Probability examples are computed, and claims about the attention paper are checked against the paper itself.
- **Review:** three reviewers with identical briefs review each week, and their findings are consolidated before merge.

## Out of scope

Recorded videos, LMS (Canvas) export, translations, and fine-tuning or training models (mentioned in week 9 as an option students rarely need, not taught).
