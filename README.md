# AI Development Course

A 14-week, hands-on course at Utah Valley University on building useful tools with AI, for students with little or no coding experience. You'll learn how modern AI works, set up Claude Code, and spend the semester building a small AI-powered tool of your own: planning it, building it, reviewing it, running it, then adding AI features and measuring how well they work.

## Get the course

    git clone https://github.com/vasuchettyphd/ai-dev-course.git
    cd ai-dev-course

Each week lives in its own folder. Follow that week's README from inside the folder.

## Costs

- **Claude Pro, about $20/month**, for Claude Code. Week 2 walks you through signing up.
- **About $5 of one-time API credit**, used in weeks 9-11 when your own code calls a model. Claude Pro doesn't cover this.

## Before week 1

A laptop running macOS, or Windows 10/11 (we'll set up WSL together in week 2). Nothing else needs installing yet.

## Schedule

| Week | Topic |
|---|---|
| 1 | [What AI is](weeks/01-what-is-ai/) |
| 2 | [Setting up Claude Code](weeks/02-claude-code-setup/) |
| 3 | [Git and GitHub](weeks/03-git-and-github/) |
| 4 | [Planning a project](weeks/04-planning/) |
| 5 | [Building with AI](weeks/05-building-with-ai/) |
| 6 | [Reviewing code](weeks/06-reviewing-code/) |
| 7 | [Running what you build](weeks/07-running-with-docker/) |
| 8 | [Debugging with AI, and midterm check-in](weeks/08-debugging/) |
| 9 | [Calling a model from code](weeks/09-calling-a-model/) |
| 10 | [Embeddings and RAG](weeks/10-embeddings-and-rag/) |
| 11 | [Tools, agents and MCP](weeks/11-tools-agents-mcp/) |
| 12 | [Evaluation](weeks/12-evaluation/) |
| 13 | [Security and responsible use](weeks/13-security-and-responsible-use/) |
| 14 | [Final demos](weeks/14-final-demos/) |

## Your project

In week 4 you choose a small tool to build, something useful for your work, studies or a business idea. Every week after that you apply what you learned to it, and in week 14 you demo it. The class examples use a shared project, a rental property deal screener, and its state at the end of each week is tagged in `example-project/`.

## Grading

Weeks 1-13 each have a 10-point assignment with a rubric in that week's `assignment.md`. The final project in week 14 is worth 30 points.

## Advanced topics

Optional, for after the core course or for extra credit. Each one stands alone.

| Topic | What you learn |
|---|---|
| [dbt with Postgres](advanced/dbt/) | Turn raw CSV data into tested tables with dbt |
| [Run an LLM locally](advanced/local-llm-docker/) | Serve an open model in Docker (needs an NVIDIA GPU) |
| [Jev](advanced/jev/) | Measure where a narrow classifier is reliable (week 12's case study) |
| [Wordle agent](advanced/wordle-agent/) | Build an agent with one tool and a validator it can't fake |
| [`/grill-me` and Superpowers in depth](advanced/grill-me-superpowers/) | The full rental deal screener walkthrough |
| [Beads](advanced/beads/) | Keep an agent's task list across sessions (optional in week 5) |

## History

The advanced tutorials started as separate repositories and keep their full commit history here. Run `git log --graph --oneline` to see each tutorial's original commits join the course.
