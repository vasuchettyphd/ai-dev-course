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
