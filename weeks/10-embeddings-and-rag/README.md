# Week 10: Embeddings and RAG

**Goal:** make your program find information by **meaning**, not just matching words, and answer questions from **your own documents**, naming which documents it used. You'll get a Google AI key safely, turn sentences into embeddings and compare them, see each step of RAG on the deal screener's notes, and add RAG over your own course-safe documents to your project, merged through a pull request.

**Time:** about 20 minutes before class to get the Google key (step 2), then plan for about 2 to 3 hours of your own time (an estimate). **Cost:** Google's embeddings are free of charge on the free tier (step 2 explains the catch: what you send may be read to improve Google's products). The answers come from Claude Haiku, paid from your week 9 API credit: a fraction of a cent per question.

**Tested with** (13 October 2026; these are the versions tested, yours may be newer):

- Google's official Python package `google-genai` 2.30.0 (released 13 October 2026; it needs Python 3.10 or newer) and the embedding model `gemini-embedding-001`, plus `anthropic` 1.13.0 and `claude-haiku-5-5` from week 9, in a container with Python 3.12.
- The deal screener example's new `notes` command and its offline tests.
- **Being tested:** every real call to Google (no Google key had been used when this page was written), every step in Google AI Studio, whether your school Google account can use AI Studio, everything inside a signed-in Claude Code session, everything on GitHub, and every step on a Mac or in Windows (WSL).

## Before you start

You need:

- Week 9 done: your AI feature merged into `main` of your **private** `semester-project`, your Anthropic key in `~/semester-project/.env`, the `Read(./.env)` deny rule in `.claude/settings.json`, and `~/first-call/.venv` from week 9 step 3.
- A Google account that can use Google AI Studio (step 2a explains which). Google's terms say "You must be 18 years of age or older to use the APIs."
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
| Commit the saved index file, if your documents aren't public | **No**: it holds their full text (step 5d) |
| `git add`, `git commit`, `git push` on your `rag` branch, `gh pr create` | plain **Yes**, after `git status` shows no `.env` |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

## Steps

### 1. Search by meaning

Say your notes say "the association dues are $185 a month", and you search for "HOA fees". A **keyword search** finds nothing: none of those words are in the note. A person sees at once that it's the same thing (an HOA, a homeowners association, charges dues).

An **embedding** lets a program see that too. An embedding model turns a piece of text into a long list of numbers (`gemini-embedding-001` gives 3,072 of them by default; this course keeps 768). Texts that **mean** similar things get similar lists of numbers, even when they use different words. Then "find notes about HOA fees" becomes "find the notes whose numbers are closest to the question's numbers".

"Closest" is measured with **cosine similarity**: a score from -1 to 1, where 1 means "pointing the same way". Google's embeddings guide: "Cosine similarity is a good distance metric because it focuses on direction rather than magnitude." (<https://ai.google.dev/gemini-api/docs/embeddings>). You don't need the maths: the score is just "how alike are these two meanings?".

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

**b. Create the key.** Go to Google AI Studio's API keys page (<https://aistudio.google.com/apikey>), sign in, and click **Create API key**. Copy it (Google keys usually start with `AIza`, being tested). Don't paste it anywhere except your `.env` file, next.

**c. Know what the free tier does with what you send.** The free tier costs nothing, but Google's terms (<https://ai.google.dev/gemini-api/terms>, read 13 October 2026) say:

> "When you use Unpaid Services, including, for example, Google AI Studio and the unpaid quota on Gemini API, Google uses the content you submit to the Services and any generated responses to provide, improve, and develop Google products and services and machine learning technologies, including Google's enterprise features, products, and services, consistent with our Privacy Policy."
>
> "To help with quality and improve our products, human reviewers may read, annotate, and process your API input and output."
>
> "Do not submit sensitive, confidential, or personal information to the Unpaid Services."

On the paid tier (a Google Cloud project with billing switched on) Google says it "doesn't use your prompts ... or responses to improve our products". This course uses the free tier, so **treat everything you send to Google as something a stranger might read**: that's why your documents must be course-safe (step 5c).

**d. Save it in `.env`.** Add a second line to your `.env` files, with a text editor, exactly as in week 9 step 2d (no spaces, no quote marks):

```text
GEMINI_API_KEY=AIza...your Google key...
```

Do it in `~/first-call/.env` now, and later in `~/semester-project/.env` (step 5b). Check the line without showing the key: `grep -c '^GEMINI_API_KEY=' .env` prints `1`.

Use the name `GEMINI_API_KEY`, and **don't** also set `GOOGLE_API_KEY`: Google's library reads both, and "If both are set, `GOOGLE_API_KEY` takes precedence" (<https://ai.google.dev/gemini-api/docs/api-key>), which leads to confusing "wrong key" errors.

**e. If a Google key leaks.** On the same API keys page in AI Studio, delete the key first, then create a new one and put it in `.env`. Google's own advice: "Never check API keys into source control systems like Git."

**f. Limits.** On the free tier, Google limits how many requests you can make per minute and per day; Google says "View your active rate limits in AI Studio" (<https://ai.google.dev/gemini-api/docs/rate-limits>). If you hit one, you'll see error 429: wait and try again. The daily count resets at midnight Pacific time.

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
    "The association dues on the Riverside condo are $185 a month.",
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

The first line loads both keys from `.env` into this window, as in week 9. You should see `Numbers in each embedding: 768`, then three scores (being tested: your numbers will be close to these). The dues note and the HOA question should score **higher** than either does with the contractor note, although they share no important words. That's search by meaning.

If you see `ValueError` mentioning an API key, the key isn't loaded: run the `set -a` line again in `~/first-call`. Google's newer model, `gemini-embedding-2`, works a little differently (it has no `task_type`); this course uses `gemini-embedding-001`, which Google supports until at least May 2028 (<https://ai.google.dev/gemini-api/docs/deprecations>).

### 4. RAG step by step, on the deal screener

The deal screener now has a `notes/` folder: 8 short notes an investor might keep, made up for this course (no real people or addresses). One is about Riverside's "association dues" and never says "HOA"; one is about a contractor's phone habits and has nothing to do with money. You'll watch each RAG step on them.

**a. Get the course files and set up.** In your terminal:

```bash
cd ~/ai-dev-course
git pull
cd example-project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then copy your keys file in, without opening it: `cp -n ~/first-call/.env .env`. Check git ignores it: `git check-ignore .env` prints `.env`.

**b. Chunk and index.** In the same window:

```bash
set -a; . ./.env; set +a
python3 -m dealscreener.notes index
```

It splits each note into chunks of up to 800 characters (most notes are one chunk; the listing B write-up is two), turns every chunk into an embedding with Google, and saves them all in `notes-index.json`. It prints `Indexed 9 chunks from 8 notes.` (being tested). That file holds the full text of your notes, so git and Docker both ignore it. You only rebuild it when the notes change: if you edit a note and ask again, the program says `Your notes changed since the index was built. Run: python3 -m dealscreener.notes index`.

**c. Retrieve and answer.** Ask:

```bash
python3 -m dealscreener.notes ask "What are the HOA fees like in Riverside?"
```

The program turns your question into an embedding, picks the 3 closest chunks, and prints them with their similarity scores, under `Notes that match best:`. The Riverside "association dues" note should be first (being tested). Then it sends **only those 3 chunks** to Claude Haiku with these rules (the program's `SYSTEM_PROMPT`):

```text
Answer only from the notes below.
After your answer, list the file names you used, after the word Sources:.
If the notes do not answer the question, reply exactly: My notes don't say.
```

and prints the answer, its `Sources:` line, and what the Claude call cost.

**d. Ask something the notes don't cover.**

```bash
python3 -m dealscreener.notes ask "What did I note about solar panels?"
```

Retrieval still finds the 3 "closest" chunks (something is always closest), but none of them mentions solar panels, so the answer should be `My notes don't say.` (being tested). That's **grounding**: without the rule, a model would happily answer from general knowledge, sounding just as sure, and you couldn't tell which answers came from your notes.

**e. Without a Claude key.** If the Anthropic key is missing or the call fails, `ask` still prints the matching notes and says why there's no answer: retrieval alone is useful.
