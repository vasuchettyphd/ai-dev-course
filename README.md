# AI Development Course

A hands-on course at Utah Valley University on building useful tools with AI, for students with little or no coding experience. You'll learn how modern AI works, set up Claude Code, and spend the semester building a small AI-powered tool of your own: planning it, building it, reviewing it, running it, then adding AI features and measuring how well they work.

## Get the course

```bash
git clone https://github.com/vasuchettyphd/ai-dev-course.git
cd ai-dev-course
```

The material comes in 14 week folders. Follow each week's README from inside its folder. Class sessions are 2.5 hours, so some sessions cover two week folders: the schedule below says which.

## Costs

- **Claude Pro, about $20/month**, for Claude Code. Week 2 walks you through signing up.
- **About $5 of one-time API credit**, used in weeks 9-14 (and the Wordle agent session) when your own code calls a model (each call costs a fraction of a cent). Claude Pro doesn't cover this.
  If you have no way to pay for it, tell your instructor before week 9. The department may cover it; if not, you'll do weeks 9 to 14 on the **Gemini path** (Google's free tier, 18 or older; weeks 9 to 12 each have a `gemini.md` page, and weeks 13 and 14 a short note), with the same assignments and grading. In session 12, skip the Wordle agent (it needs API credit) and try two advanced topics that need no API key.

Some advanced topics need their own API key and credit, beyond the costs above; the table under Advanced topics says which. Keep API keys in a `.env` file: the course's `.gitignore` keeps `.env` files out of commits.

## Before the first class

A laptop running macOS 15 (Sequoia) or later, or Windows 10 (version 2004 or later) or Windows 11, with at least 4 GB of memory, where you can install software: you need administrator rights on both Mac and Windows. Chromebooks won't work.

The first class sets up almost everything you need for the semester, so do these three things **before** it. Each takes a few minutes, but some need waiting time you don't want to spend in class:

1. **Subscribe to Claude Pro** with your own account ([week 2, step 1](weeks/02-claude-code-setup/#1-get-claude-pro)). The free plan has no Claude Code.
2. **Windows only: install WSL** the day before class ([week 2, step 3, parts a to d](weeks/02-claude-code-setup/#3-install-on-windows-with-wsl)). It needs a restart and can take a while. Stop once you have created your Ubuntu username and password; we install Claude Code together in class.
3. **Create a GitHub account and verify your email address** ([week 3, step 1a](weeks/03-git-and-github/#1-create-a-github-account-and-keep-your-email-private)). The verification email can take a few minutes.

## Schedule

Spring 2027, Thursdays, 2.5 hours a session. Check the course site for any change to these dates.

| Session | Date | In class | Week folders |
|---|---|---|---|
| 1 | Jan 14 | What AI is, then setup: Claude Code, git and the GitHub CLI | [1. What AI is](weeks/01-what-is-ai/), [2. Setting up Claude Code](weeks/02-claude-code-setup/), [3. Git and GitHub](weeks/03-git-and-github/) steps 1 to 4 |
| 2 | Jan 21 | Your first repo and pull request, then choose and plan your project | [3. Git and GitHub](weeks/03-git-and-github/) steps 5 to 9, [4. Planning a project](weeks/04-planning/) |
| 3 | Jan 28 | Build the first version, with time in class to run the build | [5. Building with AI](weeks/05-building-with-ai/) |
| 4 | Feb 4 | Review your build with three reviewers and fix what they find | [6. Reviewing code](weeks/06-reviewing-code/) |
| 5 | Feb 11 | Run it in Docker, then the midterm peer demo | [7. Running what you build](weeks/07-running-with-docker/), [8. Debugging with AI, and midterm check-in](weeks/08-debugging/) |
| 6 | Feb 18 | Add an AI feature | [9. Calling a model from code](weeks/09-calling-a-model/) |
| 7 | Feb 25 | Search your own documents by meaning | [10. Embeddings and RAG](weeks/10-embeddings-and-rag/) |
| 8 | Mar 4 | Give your feature a tool | [11. Tools, agents and MCP](weeks/11-tools-agents-mcp/) |
| 9 | Mar 11 | Measure how well it works | [12. Evaluation](weeks/12-evaluation/) |
| | Mar 18 | No class: spring break (Mar 15 to 21) | |
| 10 | Mar 25 | Attack your own project, safely | [13. Security and responsible use](weeks/13-security-and-responsible-use/) |
| 11 | Apr 1 | Advanced: the seven add-ins tour | [Seven add-ins tour](#seven-add-ins-tour) |
| 12 | Apr 8 | Advanced: build an agent, then Beads or dbt | [Wordle agent](advanced/wordle-agent/), then [Beads](advanced/beads/) or [dbt with Postgres](advanced/dbt/) |
| 13 | Apr 15 | Catch-up and demo rehearsal | |
| 14 | Apr 22 | Final demos | [14. Final demos](weeks/14-final-demos/) |

When a session covers two week folders, finish whatever class didn't, in week order, before the next session. On top of class time, plan for about 2 to 3 hours of your own time a week, more after sessions 2 and 5.

## Your project

In week 4 you choose a small tool to build, something useful for your work, studies or a business idea. Every week after that you apply what you learned to it, and in week 14 you demo it. The class examples use a shared project, a rental property deal screener. From week 4 it will live in `example-project/`, with a git tag (`week-04` to `week-14`) marking its finished state at the end of each week.

## Grading

Weeks 1-13 each have a 10-point assignment with a rubric in that week's `assignment.md`. When a session covers two week folders, both assignments are due; the course site gives each due date. The final project in week 14 is worth 30 points. The two advanced sessions (11 and 12) share one 10-point grade: try two advanced topics, 5 points each. For each, hand in a screenshot of it working and two or three sentences on what it did well and what it got wrong. Any two count: the ones done in class are fine.

## Advanced topics

Each one stands alone. Sessions 11 and 12 teach the seven add-ins tour, the Wordle agent, Beads and dbt in class; the others are optional, for further study.

| Topic | What you learn | You need |
|---|---|---|
| [dbt with Postgres](advanced/dbt/) | Turn raw CSV data into tested tables with dbt | Docker |
| [Run an LLM locally](advanced/local-llm-docker/) | Serve an open model in Docker (needs an NVIDIA GPU) | Docker, an NVIDIA GPU with 8 GB+ VRAM, the NVIDIA Container Toolkit |
| [Jev](advanced/jev/) | Measure where a narrow classifier is reliable (week 12's case study) | Python 3, an OpenRouter API key (a full run costs a few cents) |
| [Wordle agent](advanced/wordle-agent/) | Build an agent with one tool and a validator it can't fake | Python 3.10+, an Anthropic or OpenAI API key (no cost figure given, check your provider's usage page after a game) |
| [`/grill-me` and Superpowers in depth](advanced/grill-me-superpowers/) | The full rental deal screener walkthrough | Claude Code |
| [Beads](advanced/beads/) | Keep an agent's task list across sessions (optional in week 5) | Python 3.10+, git, Claude Code (about $1-2 of model usage) |

### Seven add-ins tour

One lesson day, seven add-ins for Claude Code: five are skills, and SolidCraft and xerj are MCP servers that come with skills. Each folder has its own demo and stands alone, so do them in any order. Security audit, Anatomy and Archify need Node.js 22.20 or later, which you may not have: week 5 installs it only if Claude chose Node for your project. Check with `node --version`, and if it's missing or older, follow [week 5, step 3d](weeks/05-building-with-ai/#3-pick-your-tools) before you try one of them.

| Topic | What you learn | You need |
|---|---|---|
| [Security audit](advanced/security-audit/) | Run Cloudflare's security-audit skill on a deliberately leaky app and grade it against an answer key | git, Node 22.20+, uv or Python 3.10+, Claude Code (about $2 of model usage) |
| [Ponytail](advanced/ponytail/) | Make the agent write less code, and measure whether it did | Python 3.10+, git, curl, Claude Code (about $0.30) |
| [SolidCraft](advanced/solidcraft/) | Design a parametric 3D part by talking to a CAD app over MCP, then export STL and STEP | Linux or WSL (macOS untested), git, curl, Claude Code (about $0.35) |
| [Anatomy](advanced/anatomy/) | Explain an idea as an interactive isometric machine figure | git, Node 22.20+, Claude Code, Chrome optional (about $1.30) |
| [xerj](advanced/xerj/) | Give the agent a local search engine and memory over MCP, and compare it with plain grep | Linux, macOS or WSL, git, curl, Claude Code (under $0.50) |
| [graphify](advanced/graphify/) | Turn a project into a knowledge graph the agent can query | git, uv, Claude Code (about $0.80) |
| [Archify](advanced/archify/) | Generate architecture, sequence and workflow diagrams from code or a plain description | git, Node 22.20+, Chrome or Chromium (inside Linux on WSL), Claude Code (about $0.90) |

## History

The advanced tutorials started as separate repositories and keep their full commit history here. Run `git log --graph --oneline` to see each tutorial's original commits join the course.
