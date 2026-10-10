# AI Development Course

Six hands-on tutorials on building with data and AI tools, collected for a class at Utah Valley University. Each one lives in its own folder, has its own README, and can be done on its own. The order below goes from data plumbing, to running and calling models, to building an agent, to working with an AI coding assistant.

## Get the code

```bash
git clone https://github.com/vasuchettyphd/ai-dev-course.git
cd ai-dev-course
```

Then `cd` into a tutorial folder and follow its README. Every command in a tutorial is run from inside that tutorial's folder.

## The tutorials

| # | Tutorial | What you learn | You need |
|---|---|---|---|
| 1 | [dbt with Postgres](01-dbt/) | Turn raw CSV data into tested, documented tables with dbt | Docker |
| 2 | [Run an LLM locally](02-local-llm-docker/) | Serve an open model behind an HTTP endpoint and call it from Jupyter, all in Docker Compose | Docker, an NVIDIA GPU with 8 GB+ VRAM, the NVIDIA Container Toolkit |
| 3 | [Jev: what it's good at and what it isn't](03-jev/) | Measure where a narrow classifier model is reliable, and keep exact rules in code | Python 3, an OpenRouter key (a full run costs a few cents) |
| 4 | [Build an agent that plays Wordle](04-wordle-agent/) | Give a model one tool, real feedback and a validator it cannot fake | Python 3.10+, an Anthropic or OpenAI key |
| 5 | [`/grill-me` and Superpowers](05-grill-me-superpowers/) | Plan with Claude Code before building, then build in small, tested steps | Claude Code |
| 6 | [Beads](06-beads/) | Keep an AI coding agent's task list alive across sessions | Python 3.10+, git, Claude Code (about $1-2 of model usage) |

Tutorial 2 is the only one that needs a GPU. If you don't have one, read it for the architecture and move on.

## API keys and cost

Tutorials 3, 4 and 6 call paid model APIs, and tutorials 5 and 6 need Claude Code, which requires a paid Claude plan or API credit. Tutorials 3 and 6 say roughly what a run costs (a few cents and about $1-2). Tutorial 4 doesn't give a figure, so check your provider's usage page after your first game. Keep keys in environment variables or a local `.env` file. The course's `.gitignore` excludes `.env` files in every folder, so a key never ends up in a commit.

## History

Each tutorial started as its own repository and was merged in here with git subtree, which keeps its full commit history. Run `git log --graph --oneline` to see each tutorial's commits join the course.
