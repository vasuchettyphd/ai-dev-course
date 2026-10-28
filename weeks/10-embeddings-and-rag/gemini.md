# Week 10 on the Gemini path

This page is for students on the **Gemini path**: you told your instructor you can't pay for API credit, and in week 9 you followed [week 9 on the Gemini path](../09-calling-a-model/gemini.md), with your Google key and the model `gemini-3.5-flash-lite` on Google's free tier.

Week 10 changes very little for you. The embeddings in the [week 10 README](README.md) already come from Google, with the same key you have. Only the **answer** step changes: your answers come from `gemini-3.5-flash-lite` instead of Claude Haiku. So you have **one key** this week, `GEMINI_API_KEY`, and no Anthropic key.

Follow the README from top to bottom, and use this page alongside it. Each section below is keyed to a README step number. Anything not listed here, do exactly as the README says.

**Cost:** $0. Embeddings and answers both run on Google's free tier. Your program still works out what each answer **would** cost on the paid tier, so you keep practising the arithmetic from week 9.

**Privacy, once more:** on the free tier, Google uses what you send to improve its products (README step 2c quotes the terms). On the Gemini path that means **everything** your program sends this week goes to Google's free tier: your documents when you build the index, and each question **plus the chunks retrieved for it** when you ask. So every document and every question must be course-safe. Week 10 already requires course-safe documents (README step 5c), so this adds nothing new: just don't type a private question either.

## Step 2: Get a Google key safely

You already did this in week 9. Skip 2a to 2f, but check the key line is still there. In your terminal, in `~/first-call`:

```bash
grep -c '^GEMINI_API_KEY=' .env
```

It prints `1`. If it prints `0`, add the line with a text editor as in README step 2d. Still read step 2c again: it's the reason for the privacy note above.

## Step 3: Your first embeddings

You already installed `google-genai` 2.30.0 in `~/first-call/.venv` in week 9, so in step 3a just run the check (the `pip install` line does no harm if you run it again):

```bash
cd ~/first-call
source .venv/bin/activate
python -c "from google import genai; print(genai.__version__)"
```

It prints `2.30.0`. Steps 3b and 3c are the same for you. Where 3c says the `set -a` line "loads both keys", for you it loads one.

## Step 4: RAG step by step, on the deal screener

The deal screener's **retrieval** half uses only Google, so it works with your key. Its **answer** half calls Claude, so it needs an Anthropic key, which you don't have. That's fine: step 4e is built for exactly this.

- **4a and 4b:** do them as written. `cp -n ~/first-call/.env .env` copies your one-key `.env`, and `index` prints `Indexed 9 chunks from 8 notes.` as in the README.
- **4c and 4d:** run both `ask` commands. You'll see `Notes that match best:` and the three matching chunks with their similarity scores, as the README describes. Then, instead of an answer, the program says why there's no answer (no Anthropic key: `No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README).`), adds `Here are the notes that match best instead.`, and prints the text of those notes. This is step 4e's "retrieval alone is useful" in action.
- **The answers:** read the ones the course recorded. README step 4c gives the instructions Claude got, word for word, and step 4d says the solar panels question got `My notes don't say.` The deal screener's [notes cost record](../../example-project/README.md#notes-cost-record) lists the course's real questions, with token counts.

Look at the printed chunks for the solar panels question: none of them mentions solar panels. A grounded model given only those chunks has nothing to answer from, which is why the recorded answer is `My notes don't say.` Your own program in step 5 will show you this for real.

## Step 5: Add RAG to your project

Steps 5a, 5c, 5e and 5f are the same for you. Two small differences in 5b and 5d:

**5b.** Your `~/semester-project/.env` already has your `GEMINI_API_KEY` line from week 9, so just check: `grep -c '^GEMINI_API_KEY=' .env` prints `1`.

**5d.** Use this planning prompt instead of the README's (replace the parts in angle brackets):

```text
/superpowers:writing-plans Write an implementation plan to add RAG to this project: answer questions about the documents in <folder> using <one sentence: what the questions are for>. Use Google's official google-genai package pinned to 2.30.0 with the model gemini-embedding-001 (task_type RETRIEVAL_DOCUMENT for the documents and RETRIEVAL_QUERY for questions, 768 dimensions), and the same package with the model gemini-3.5-flash-lite for the answers. Chunk the documents, embed each chunk once, save the embeddings in an index file, retrieve the 3 closest chunks by cosine similarity, and, in the system_instruction of the answer call, tell the model to answer only from them, name the files it used, and reply "My notes don't say." when they don't answer the question. Rules: the program reads GEMINI_API_KEY only from the environment (it may load .env when it starts), and you, Claude, must never open, read, print or log .env or the key; rebuild or refuse when the documents change after indexing; add the index file to .gitignore and .dockerignore; if the key is missing or a call fails, say what happened in one plain sentence and carry on as far as possible; if a call fails with a 429 or 503 error, say so in one plain sentence and carry on; check the answer's finish reason and say so in a plain sentence if it isn't STOP; leave out temperature; print the input tokens and output tokens of each answer call, and the cost it would have on the paid tier ($0.30 per million input, $2.50 per million output tokens, counting thinking tokens as output); tests must use a fake embedder and a fake model and never call Google, plus one live test that runs only when I set RUN_LIVE_TESTS=1; include a test for "no Google key"; update the Dockerfile and requirements; add GEMINI_API_KEY to .env.example with a fake value. I'm not a programmer, so keep each task small.
```

What changed from the README's prompt, so you can check it:

| README's prompt says | Gemini path says |
|---|---|
| "Anthropic's anthropic package with claude-haiku-5-5 for the answers" | "the same package with the model gemini-3.5-flash-lite for the answers" |
| "tell the model to answer only from them" | "in the system_instruction of the answer call, tell the model to answer only from them" |
| "reads GEMINI_API_KEY and ANTHROPIC_API_KEY only from the environment" | "reads GEMINI_API_KEY only from the environment" |
| "or the keys", "if a key is missing" | "or the key", "if the key is missing" |
| "print the cost of each Claude call" | the token counts and the paid-tier cost (the `$0.30` / `$2.50` line) |
| "never call Google or Anthropic" | "never call Google" |
| (not there) | the 429 or 503 sentence, the finish reason check, and "leave out temperature" |

`system_instruction` is where Gemini takes the instructions that stay the same for every call, like the "explain real estate terms to beginners" system prompt in week 9. The grounding rules go there, and only the question and the retrieved chunks go in the message itself.

In the package check after 5d, the one official package you need is `google-genai` (or `@google/genai` for a Node.js project, being tested). If Claude Code wants to install `anthropic`, say **No** and type: "This project uses only Google's google-genai package. Use gemini-3.5-flash-lite for the answers."

When you try it in 5e, the cost line should show tokens and a paid-tier estimate, not a real charge: your real cost is $0. The exact wording depends on what Claude Code builds.

## Steps 6 and 7: Review, run and finish

Do them as written. Two small differences:

- **6b (Docker):** the deal screener's `ask` in Docker shows the matching notes and the no-answer message, as in step 4. For your project, `--env-file .env` hands the container your one key.
- **7b (key searches):** use the browser's Find for `GEMINI_API_KEY=` (it should show only the fake value in `.env.example`) and for `AIza` (the usual start of a Google key; being tested): only fake values are allowed. You have no Anthropic key, so you can skip the `ANTHROPIC_API_KEY=` and `sk-ant-` searches. If a real key is there, don't merge: delete it first (README step 2e), then make a new one.

## Hand-in differences

The [week 10 assignment](assignment.md) is the same for you, with the same rubric and points. The only differences:

- **(a)** `.env.example` has one fake key, `GEMINI_API_KEY`, and the pinned packages are Google's only.
- **(b)** For each of your three questions, if your program prints a cost line, it shows the token counts and the paid-tier estimate; your real cost is $0.
- **(c) and (d)** are the same.

## Troubleshooting

The README's Troubleshooting table still applies to the embeddings and the index. These rows are for the Gemini answer step.

| What you see | What to do |
|---|---|
| `No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README).` from the **deal screener** | Expected on the Gemini path: the deal screener's answer half needs Claude. Read the matching notes it prints, and the recorded answers (step 4 above). |
| `ValueError: No API key was provided. Please pass a valid API key.`, or "No Google API key found", from **your** program | The key isn't loaded: `set -a; . ./.env; set +a` in the folder with `.env`, and check `grep -c '^GEMINI_API_KEY=' .env` prints `1`. |
| Your program asks for `ANTHROPIC_API_KEY` | It was built with the README's prompt, not this page's. Ask Claude Code: "Use only GEMINI_API_KEY and gemini-3.5-flash-lite for the answers. Remove the anthropic package." |
| Error 429 | You hit a free-tier limit (per minute or per day). Wait a minute and try again; a daily limit resets at midnight Pacific time. See your limits in AI Studio. |
| `503 UNAVAILABLE` and "This model is currently experiencing high demand." | Google's model is busy (the course saw this in its own test on 28 October 2026). Wait a minute and run again. Your program should treat it like any failed call: say so in one sentence and still show the retrieved chunks. |
| The answer stops mid-sentence, or the finish reason is `MAX_TOKENS` | The answer hit its token cap. Ask Claude Code to raise the cap (the course's tested Gemini programs used 1000). |
| The answer comes with Markdown, like `**bold**` | Gemini sometimes answers in Markdown. That's fine for a terminal; if it bothers you, ask for "plain text, no Markdown" in the system instruction. |
