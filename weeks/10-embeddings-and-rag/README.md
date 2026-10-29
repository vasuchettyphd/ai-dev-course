# Week 10: Embeddings and RAG

**Goal:** make your program find information by **meaning**, not just matching words, and answer questions from **your own documents**, naming which documents it used. You'll get a Google AI key safely, turn sentences into embeddings and compare them, see each step of RAG on the deal screener's notes, and add RAG over your own course-safe documents to your project, merged through a pull request.

**Time:** about 20 minutes before class to get the Google key (step 2), then plan for about 2 to 3 hours of your own time (an estimate). **Cost:** Google's pricing page lists embeddings as "Free of charge" on the free tier, so the course expects no Google charge for this week's use (the pricing page lists `gemini-embedding-001` input as "Free of charge" on the free tier, checked 29 October 2026); step 2c explains the catch: what you send may be read to improve Google's products. The answers come from Claude Haiku, paid from your week 9 API credit: a fraction of a cent per question.

**Tested with** (13 October 2026; these are the versions tested, yours may be newer):

- Google's official Python package `google-genai` 2.30.0 (released 13 October 2026; it needs Python 3.10 or newer) and the embedding model `gemini-embedding-001`, plus `anthropic` 1.13.0 and `claude-haiku-5-5` from week 9, in a container with Python 3.12.
- Real calls on 13 October 2026, from a container: `embed.py` below, and the deal screener's `notes` command (index, three questions, its live test). The scores, answers and costs shown below are from those runs; yours will differ a little. Google's responses carried no token counts.
- **Being tested:** every step in Google AI Studio, whether your school Google account can use AI Studio, everything on GitHub, and every step on a Mac. Windows (WSL), 29 October 2026: steps 3, 4 and 6b, the Troubleshooting messages, and steps 5 and 6a in a signed-in Claude Code session (2.1.312) were run and matched this page.

## Before you start

You need:

- Week 9 done: your AI feature merged into `main` of your **private** `semester-project`, your Anthropic key in `~/semester-project/.env`, the `Read(./.env)` deny rule in `.claude/settings.json`, and `~/first-call/.venv` from week 9 step 3.
- A Google account that can use Google AI Studio (step 2a explains which). Google's terms say "You must be 18 years of age or older to use the APIs."
- On the **Gemini path** (you got your Google key in week 9 instead of buying API credit)? You have one key, not two, and only the answer step changes: follow [week 10 on the Gemini path](gemini.md) alongside this page.
- A few **course-safe documents** for your project (step 5c says what that means).
- `gh` signed in to **your** GitHub account, and Claude Code signed in with your Claude Pro account.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows. Every command below says where to type it. On Windows, nothing this week goes in PowerShell.

### How you'll work this week

The same as week 9: you ask Claude Code in plain English, and this page shows the prompt, what Claude Code will probably do, and what to check. The git rules still apply (branch first, never change `main`, plain **Yes** for git commands, finish with a pull request).

**The key rules from week 9 now cover two keys**, `ANTHROPIC_API_KEY` and `GEMINI_API_KEY`:

1. **You** put each key in `.env` with a text editor. Never paste a key into Claude Code, a chat, a screenshot, a commit or a pull request.
2. `git check-ignore .env` must print `.env` before you commit.
3. Your program reads keys from the environment and never prints them.
4. Docker gets them when the container starts (`--env-file .env`), never in the image.
5. Claude Code is blocked from reading `.env` by your week 9 deny rule. Keep it.
6. If a key leaks, **delete it first** (Anthropic: week 9 step 2f; Google: step 2e below), then clean up.

**And one new rule, about your documents:** only send documents you'd be happy for a stranger to read (step 2c explains why).

| Claude asks to | Choose |
|---|---|
| Create or edit your code, tests and a `docs/` or `notes/` folder of course-safe documents on your `rag` branch | **Yes** |
| `pip install` the packages in your project's `.venv`, or `npm install` for Node.js, after you check they're the official ones (step 5) | **Yes** |
| Put a key in any file, print `.env`, or run code that prints the environment | **No**. Type: "Never read or print .env. Read the keys from the environment." |
| Add documents with personal, customer or confidential information | **No** |
| Tests that call Google or Anthropic every time they run | **No**. Type: "Tests must use a fake embedder and a fake model. Make the live test run only when I ask for it." |
| Commit the saved index file | **No**: it holds your documents' full text (step 5d) |
| `git add`, `git commit`, `git push` on your `rag` branch, `gh pr create` | plain **Yes**, after `git status` shows no `.env` |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

At the end of the build, Superpowers may ask to `rm -rf` its own scratch folder (`.superpowers/sdd/...`). Answering **No** is safe: the folder is ignored by git and can stay.

## Steps

### 1. Search by meaning

Say your notes say "the association dues are $240 a month", and you search for "HOA fees". A **keyword search** finds nothing: none of those words are in the note. A person sees at once that it's the same thing (an HOA, a homeowners association, charges dues).

An **embedding** lets a program see that too. An embedding model turns a piece of text into a long list of numbers (`gemini-embedding-001` gives 3,072 of them by default; this course keeps 768). Texts that **mean** similar things get similar lists of numbers, even when they use different words. Then "find notes about HOA fees" becomes "find the notes whose numbers are closest to the question's numbers".

"Closest" is measured with **cosine similarity**: a score from -1 to 1, where 1 means "pointing the same way". Google's embeddings guide says cosine similarity "is a good distance metric because it focuses on direction rather than magnitude" (<https://ai.google.dev/gemini-api/docs/embeddings>). You don't need the maths: the score is just "how alike are these two meanings?".

**RAG** (retrieval-augmented generation) puts this together with week 9:

1. **Chunk:** split your documents into small pieces.
2. **Index:** turn every piece into an embedding **once**, and save them all in a file.
3. **Retrieve:** turn the question into an embedding and pick the few pieces closest to it.
4. **Answer:** give only those pieces to Claude and ask it to answer **from them**, naming the documents it used, and to say so when they don't contain the answer.

The model answers from your documents instead of from memory, and you can check its answer against the named documents.

### 2. Get a Google key safely (before class)

> **Being tested:** the AI Studio steps below follow Google's pages, read on 13 October 2026. The screens may look a little different.

**a. Which Google account.** Google's page for school and work accounts says: "All Google Workspace users have access to AI Studio by default." But a school's administrator can switch it off, and "Users under the age of 18 are restricted from using AI Studio with their Google Workspace for Education accounts. This is true even when the AI Studio setting is on." (<https://ai.google.dev/gemini-api/docs/workspace>). So:

- Try your **UVU** Google account first. Whether UVU has AI Studio switched on is **being tested: check with your instructor**.
- If you see "We are sorry, but you do not have access to Google AI Studio. Please contact your Organization Administrator for access.", use a **personal** Google account instead (you must be 18 or older).

**b. Create the key.** Go to Google AI Studio's API keys page (<https://aistudio.google.com/apikey>, being tested; Google's key page is <https://ai.google.dev/gemini-api/docs/api-key>), sign in, and click **Create API key**. Copy it (Google keys usually start with `AIza`, being tested). Don't paste it anywhere except your `.env` file, next.

**c. Know what the free tier does with what you send.** The free tier should cost you nothing (being tested), but Google's terms (<https://ai.google.dev/gemini-api/terms>, read 13 October 2026) say:

> "When you use Unpaid Services, including, for example, Google AI Studio and the unpaid quota on Gemini API, Google uses the content you submit to the Services and any generated responses to provide, improve, and develop Google products and services and machine learning technologies, including Google's enterprise features, products, and services, consistent with our Privacy Policy."
>
> "To help with quality and improve our products, human reviewers may read, annotate, and process your API input and output."
>
> "Do not submit sensitive, confidential, or personal information to the Unpaid Services."

On the paid tier (a Google Cloud project with billing switched on) Google says it "doesn't use your prompts ... or responses to improve our products". Your program's calls to the Gemini API count as paid only when they go through a Google Cloud project with billing switched on (Google's terms), and this course doesn't use billing, so **your calls are on the free tier**. **Treat everything you send to Google as something a stranger might read**: that's why your documents must be course-safe (step 5c).

**d. Save it in `.env`.** Add a second line to your `.env` files, with a text editor, exactly as in week 9 step 2d (no spaces, no quote marks):

```text
GEMINI_API_KEY=AIza...your Google key...
```

Do it in `~/first-call/.env` now, and later in `~/semester-project/.env` (step 5b). Check the line without showing the key: `grep -c '^GEMINI_API_KEY=' .env` prints `1`.

Use the name `GEMINI_API_KEY`, and **don't** also set `GOOGLE_API_KEY`: Google's library reads both, and "If both are set, `GOOGLE_API_KEY` takes precedence" (<https://ai.google.dev/gemini-api/docs/api-key>), which leads to confusing "wrong key" errors.

**e. Restrict it, and if it leaks, delete it.** Google: "Adding restrictions to your API keys minimizes the potential damage if a key is compromised." (<https://ai.google.dev/gemini-api/docs/api-key>): so if your key's settings in AI Studio offer a way to limit it to the Gemini API, use it (being tested). If a Google key leaks, on the same API keys page delete the key first, then create a new one and put it in `.env`. Google's own advice: "Never check API keys into source control systems like Git."

**f. Limits.** On the free tier, Google limits how many requests you can make per minute and per day; Google says "View your active rate limits in AI Studio" (<https://ai.google.dev/gemini-api/docs/rate-limits>). If you hit one, you'll see error 429: wait and try again. The daily count resets at midnight Pacific time. The free tier needs no billing account, so it shouldn't be able to charge you (being tested): **don't add billing** for this course.

### 3. Your first embeddings

You'll use the scratch folder and virtual environment from week 9 (`~/first-call`), so nothing here can end up in your project.

**a. Install Google's package.** In your terminal:

```bash
cd ~/first-call
source .venv/bin/activate
pip install google-genai==2.30.0
python -c "from google import genai; print(genai.__version__)"
```

The last line prints `2.30.0`. (`google-genai` is Google's official package, from <https://github.com/googleapis/python-genai>. It needs Python 3.10 or newer, like week 9's.)

**b. Write the program.** In your terminal, in `~/first-call`, paste this whole block and press Enter. It creates `embed.py`:

```bash
cat > embed.py <<'EOF'
import math
from google import genai
from google.genai import types

client = genai.Client()  # reads GEMINI_API_KEY from the environment

sentences = [
    "The association dues on the Riverside condo are $240 a month.",
    "How much are the HOA fees?",
    "The contractor prefers a text message to a phone call.",
]

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=sentences,
    config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY", output_dimensionality=768),
)
vectors = [embedding.values for embedding in result.embeddings]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


print("Numbers in each embedding:", len(vectors[0]))
print("Dues note vs HOA question:      ", round(cosine(vectors[0], vectors[1]), 3))
print("Dues note vs contractor note:   ", round(cosine(vectors[0], vectors[2]), 3))
print("HOA question vs contractor note:", round(cosine(vectors[1], vectors[2]), 3))
EOF
```

Three things to notice: there's no key in it (the package reads `GEMINI_API_KEY` itself); `output_dimensionality=768` keeps 768 numbers instead of 3,072; and `task_type="SEMANTIC_SIMILARITY"` tells the model what you'll use the embeddings for (Google's list of task types is at <https://ai.google.dev/api/embeddings>).

**c. Run it.** In your terminal, in `~/first-call`, with `(.venv)` showing:

```bash
set -a; . ./.env; set +a
python embed.py
```

The first line loads both keys from `.env` into this window, as in week 9. You should see `Numbers in each embedding: 768`, then three scores. The course's run:

```text
Numbers in each embedding: 768
Dues note vs HOA question:       0.817
Dues note vs contractor note:    0.681
HOA question vs contractor note: 0.653
```

The dues note and the HOA question should score **higher** than either does with the contractor note, although they share no important words. That's search by meaning.

If you see `ValueError` mentioning an API key, the key isn't loaded: run the `set -a` line again in `~/first-call`. Google's newer model, `gemini-embedding-2`, works a little differently (it has no `task_type`); this course uses `gemini-embedding-001`, whose announced shutdown date is 14 May 2028 (<https://ai.google.dev/gemini-api/docs/deprecations>).

### 4. RAG step by step, on the deal screener

The deal screener now has a `notes/` folder: 8 short notes an investor might keep, made up for this course (no real people or addresses). One is about Riverside's "association dues" and never says "HOA"; one is about a contractor's phone habits and has nothing to do with money. You'll watch each RAG step on them.

**a. Get the course files and set up.** In your terminal:

```bash
cd ~/ai-dev-course
git pull
cd example-project
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`python3 --version` must show 3.10 or newer, as in week 9 step 3a. If `python3 -m venv .venv` fails with "ensurepip is not available", do the fix in [week 9 step 3b](../09-calling-a-model/README.md#3-your-first-call) (`sudo apt install python3-venv`, then `rm -r .venv`) and run it again. Then copy your keys file in, without opening it: `cp -n ~/first-call/.env .env` (newer Ubuntu prints `cp: warning: behavior of -n is non-portable ...`: that's harmless). Check git ignores it: `git check-ignore .env` prints `.env`. Then check the Google line is in it: `grep -c '^GEMINI_API_KEY=' .env` prints `1`. If it prints `0` (an older `.env` from week 9 was already there, so `cp -n` left it alone), add the `GEMINI_API_KEY=` line to this `.env` with a text editor, as in step 2d.

**b. Chunk and index.** In the same window:

```bash
set -a; . ./.env; set +a
python3 -m dealscreener.notes index
```

It splits each note into chunks of up to 800 characters (most notes are one chunk; the listing B write-up is two), turns every chunk into an embedding with Google, and saves them all in `notes-index.json`. It prints `Indexed 9 chunks from 8 notes.` (about a second in the course's run). That file holds the full text of your notes, so git and Docker both ignore it. You only rebuild it when the notes change: if you edit a note and ask again, the program says `Your notes changed since the index was built. Run: python3 -m dealscreener.notes index`.

**c. Retrieve and answer.** Ask:

```bash
python3 -m dealscreener.notes ask "What are the HOA fees like in Riverside?"
```

The program turns your question into an embedding, picks the 3 closest chunks, and prints them with their similarity scores, under `Notes that match best:`. In the course's run the Riverside "association dues" note came first, with similarity 0.73; the next two scored 0.55. Then it sends **only those 3 chunks** to Claude Haiku with these instructions (the program's `SYSTEM_PROMPT`, word for word):

```text
You answer questions about a property investor's own notes. Answer only from the notes below. Do not use anything else you know. After your answer, list the file names you used, after the word Sources:. If the notes do not answer the question, reply exactly: My notes don't say.
```

and prints the answer, its `Sources:` line, and what the Claude call cost.

**d. Ask something the notes don't cover.**

```bash
python3 -m dealscreener.notes ask "What did I note about solar panels?"
```

Retrieval still finds the 3 "closest" chunks (something is always closest), but none of them mentions solar panels, so the answer should be `My notes don't say.`, and in the course's run it was (the three "closest" chunks scored only 0.62 to 0.64). That's **grounding**: without the rule, a model would happily answer from general knowledge, sounding just as sure, and you couldn't tell which answers came from your notes.

**e. Without a Claude key.** If the Anthropic key is missing or the call fails, `ask` still prints the matching notes and says why there's no answer: retrieval alone is useful.

### 5. Add RAG to your project

> Tested in a signed-in Claude Code session (2.1.312, Sonnet) in Windows (WSL) on 29 October 2026: the plan took about 4 minutes, and the build took about 26 minutes and about 90 Yes answers. Claude Code never opened `.env`. The deal screener's version was built and tested offline on 13 October 2026.

**a. Make the branch first.** Open a **new** terminal window (no keys loaded in it), `cd ~/semester-project`, start `claude`, and in Claude Code:

```text
Switch to main, pull the latest changes from GitHub, then create a new branch called rag and switch to it.
```

Plain **Yes** to each git command. Check: "What branch am I on?" says `rag`.

**b. Check the safety setup from week 9.** In a second terminal window, in `~/semester-project`:

```bash
git check-ignore .env
grep -c 'Read(./.env)' .claude/settings.json
```

The first prints `.env`; the second prints `1`. If either doesn't, redo week 9 step 5b before going on. Then add your Google key line to `~/semester-project/.env` with a text editor (step 2d), and check: `grep -c '^GEMINI_API_KEY=' .env` prints `1`.

**c. Pick course-safe documents.** RAG is only as good, and as safe, as the documents you give it. Choose 5 to 15 short text or Markdown files that fit your project, and put them in a folder such as `docs/` or `notes/`.

| Good | Not allowed |
|---|---|
| Notes, guides or FAQs **you wrote** for your project | Anything with names, emails, phone numbers or addresses of real people |
| Public material you're allowed to copy (with its source written at the top) | Customer, employer or client documents |
| Made-up example documents, labelled as made up, like the deal screener's notes | Anything confidential, or anything you'd mind a stranger reading (step 2c) |

**d. Plan and build it, with the guardrails in the prompt.** In Claude Code (replace the parts in angle brackets):

```text
/superpowers:writing-plans Write an implementation plan to add RAG to this project: answer questions about the documents in <folder> using <one sentence: what the questions are for>. Use Google's official google-genai package pinned to 2.30.0 with the model gemini-embedding-001 (task_type RETRIEVAL_DOCUMENT for the documents and RETRIEVAL_QUERY for questions, 768 dimensions), and Anthropic's anthropic package with claude-haiku-5-5 for the answers. Chunk the documents, embed each chunk once, save the embeddings in an index file, retrieve the 3 closest chunks by cosine similarity, print the file name and similarity score of each of the 3 retrieved chunks before the answer, then tell the model to answer only from them, name the files it used after the word Sources:, and reply "My notes don't say." when they don't answer the question. Rules: the program reads GEMINI_API_KEY and ANTHROPIC_API_KEY only from the environment (it may load .env when it starts), and you, Claude, must never open, read, print or log .env or the keys; rebuild or refuse when the documents change after indexing; add the index file to .gitignore and .dockerignore; if a key is missing or a call fails, say what happened in one plain sentence and carry on as far as possible; print the cost of each Claude call; tests must use a fake embedder and a fake model and never call Google or Anthropic, plus one live test that runs only when I set RUN_LIVE_TESTS=1; include a test for "no Google key"; update the Dockerfile and requirements; add GEMINI_API_KEY to .env.example with a fake value. I'm not a programmer, so keep each task small.
```

Then build it as in week 9:

```text
/superpowers:subagent-driven-development Execute the plan docs/superpowers/plans/<your-plan-file>.md.
```

Answer as in the table at the top. The official packages are `google-genai` (Google) and `anthropic` (Anthropic). For a Node.js project, Google's package is `@google/genai` (Google lists it at <https://ai.google.dev/gemini-api/docs/libraries>; on npm its source is github.com/googleapis/js-genai) and Anthropic's is `@anthropic-ai/sdk`. Any other name: ask "Is this the official package?" before answering Yes.

**e. Try it.** In your second terminal window (not the Claude Code one), in `~/semester-project`: activate `.venv` if it has one, load the keys with `set -a; . ./.env; set +a`, build the index, and ask your program three questions the way its README says, including **one your documents can't answer**. Write down, for each: the question, the documents it retrieved, and the answer. Take a screenshot of the index being built (check nothing secret is on screen). You hand these in.

**f. Run the tests.** In Claude Code: "Run all the tests." They must pass. To be sure they don't use your keys, run them once more yourself with `.env` moved out of the folder, as in week 9 steps 5e and 5f (move it out, run the tests, move it back, and check `ls -a` shows `.env` again).

**The deal screener's version:** `python3 -m dealscreener.notes index` and `python3 -m dealscreener.notes ask "..."`, in [`dealscreener/notes.py`](../../example-project/dealscreener/notes.py), with offline tests in [`tests/test_notes.py`](../../example-project/tests/test_notes.py). See [its README](../../example-project/README.md#how-to-ask-your-notes).

### 6. Review and run

**a. Review it with `safe-and-private`.** In Claude Code:

```text
Run the safe-and-private reviewer as a subagent on the files changed on this branch compared with main (git diff main --name-only), and on .gitignore, .dockerignore and the Dockerfile. Focus on: an API key in any file tracked by git (search with git grep only, never grep -r, and never open .env); whether .env or the index file could be committed or copied into the Docker image; whether a key could ever be printed or logged; whether any test calls Google or Anthropic by default; whether any document in the documents folder holds personal or confidential information. Then add a section at the end of REVIEW.md, headed "## Week 10: RAG review", with one table with the columns #, Label, Finding (file:line), Found by, Decision, Reason, numbering the findings R1, R2 and so on. Leave Decision and Reason empty. Do not change any file except REVIEW.md.
```

**Yes** to editing `REVIEW.md` only. Triage, fix and commit as in week 6 steps 5 and 6.

**b. Run it in Docker.** Your week 9 Dockerfile installs your requirements, and `--env-file .env` hands both keys to the container. The index lives on your laptop, so share just the documents folder (read-only) and the index file with the container. For the deal screener, in `~/ai-dev-course/example-project`, after `docker build -t dealscreener .` and `touch notes-index.json` (once, so Docker shares a file, not a folder):

```bash
docker run --rm --env-file .env --user "$(id -u):$(id -g)" -v "$PWD/notes:/app/notes:ro" -v "$PWD/notes-index.json:/app/notes-index.json" dealscreener python -m dealscreener.notes index
docker run --rm --env-file .env --user "$(id -u):$(id -g)" -v "$PWD/notes:/app/notes:ro" -v "$PWD/notes-index.json:/app/notes-index.json" dealscreener python -m dealscreener.notes ask "What are the association dues like in Riverside?"
```

(`--user "$(id -u):$(id -g)"` lets the container write the index file as you; tested on Windows (WSL), being tested on a Mac.) Ask Claude Code for the same two commands for your project, with your folder and index file names. Check the image holds neither: `docker run --rm <your image> ls -a` shows no `.env` and no index file.

### 7. Finish

**a. Push and open a pull request.** In Claude Code:

```text
Push the rag branch to GitHub and open a pull request into main titled "Add RAG over my documents".
```

Plain **Yes**, after `git status` shows no `.env` and no index file.

**b. Read Files changed yourself.** You should see your code and tests, the documents folder (course-safe documents only), the requirements and Dockerfile, `.env.example` with **fake** keys, `.gitignore` and `.dockerignore` listing the index file, your README and `REVIEW.md`. **No `.env`, no real key, no index file.** Use the browser's Find for `ANTHROPIC_API_KEY=` and `GEMINI_API_KEY=` (each should show only the fake value in `.env.example`), and for `sk-ant-` and `AIza` (the usual starts of the two kinds of key; being tested for Google): only fake values are allowed. If a real key is there, don't merge: delete it first (week 9 step 2f, or step 2e here).

**c. Merge on GitHub, then pull,** as in week 9. Check: "What branch am I on, and do all the tests pass?" says `main`, and yes.

The deal screener's week 10 changes are on this page (it works once week 10 is published): <https://github.com/vasuchettyphd/ai-dev-course/compare/week-09...week-10>.

## Check it worked

- `git check-ignore .env` and `git check-ignore <your index file>` both print the file name, and GitHub shows neither in your pull request.
- Your program answers a question from your documents and names the files it used.
- A question your documents can't answer gets "My notes don't say." (or your program's version of it).
- All tests pass with `.env` moved out of the folder.
- You have three questions written down, each with the retrieved documents and the answer.

## Troubleshooting

| What you see | What to do |
|---|---|
| `ValueError` mentioning an API key, or "No Google API key found" | The Google key isn't loaded: `set -a; . ./.env; set +a` in the folder with `.env`, and check `grep -c '^GEMINI_API_KEY=' .env` prints `1`. |
| "We are sorry, but you do not have access to Google AI Studio..." | Your school account can't use AI Studio. Use a personal Google account (18 or older), and tell your instructor. |
| AI Studio says it isn't available in your country, or asks you to verify your age | Google's limits (<https://ai.google.dev/gemini-api/docs/available-regions>). Use a personal account that meets them, or ask your instructor. |
| `API key not valid`, error 400, 401 or 403, or "The Google API key was not accepted" | The key is wrong, deleted, or has quote marks or spaces: check the `.env` line, or make a new key (step 2b). |
| "Using GOOGLE_API_KEY" in a warning | You also set `GOOGLE_API_KEY`, which wins: remove it (step 2d). |
| Error 429, or "Too many requests for the free tier" | You hit a free-tier limit. Wait a minute (or until the next day for a daily limit) and try again; see your limits in AI Studio. |
| "Google couldn't read the request." (error 400) | Google rejected the request. Check the package version (`google-genai==2.30.0`), the model name (`gemini-embedding-001`), and that your documents aren't empty; if it continues, ask your instructor. |
| "Couldn't reach Google. Check your internet connection." | Check your internet connection, then try again. |
| "Google's service is busy or having a problem. Try again later." | Wait a few minutes and try again. |
| "Couldn't save the index file ..." | The program can't write in that folder (in Docker, check the `--user` part and that you ran `touch notes-index.json` first). |
| Error 404, or "The embedding model name wasn't found" | Check the model name: `gemini-embedding-001`. |
| `ModuleNotFoundError: No module named 'google'` | The `.venv` isn't active, or `google-genai` isn't installed in it: `source .venv/bin/activate`, then `pip install -r requirements.txt`. |
| "Your notes changed since the index was built" | Rebuild the index (`index`), then ask again. |
| "No index yet" | Build it first (`index`). |
| "My notes don't say." when you know they do | The right chunk wasn't retrieved, or was cut in half: ask with words closer to the document's, or try bigger chunks; check which chunks it printed. |
| The answer cites the wrong document | Look at the retrieved chunks: two documents may say similar things. Make the documents more distinct, or ask a more specific question. |
| "The notes folder has no notes in it", or "No notes folder found" | Check the folder name and that it has `.md` or `.txt` files. |
| "Skipped <name>: not plain text." | That file isn't plain text (a Word file or PDF, say): save it as `.txt` or `.md`. |
| "Couldn't read <name>." | Your laptop won't let the program open that file: check its permissions. |
| The index file shows in `git status` | Add it to `.gitignore` before committing (step 5d's prompt asks for this). |
| An Anthropic error (401, 429, credit, workspace) | See [week 9's Troubleshooting](../09-calling-a-model/README.md#troubleshooting). |
| A key was pasted into a chat or committed | Delete it first (step 2e for Google, week 9 step 2f for Anthropic), then make a new one. |
| Work was committed to `main` | Use [week 5's rescue](../05-building-with-ai/README.md#if-it-committed-to-main). |
