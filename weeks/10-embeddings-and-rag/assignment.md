# Week 10 assignment: Embeddings and RAG

## What to do

Follow the [week 10 README](README.md) on your own laptop, in your private `semester-project` repo, and collect four things.

On the Gemini path? Use [week 10 on the Gemini path](gemini.md) too: the [hand-in](gemini.md#hand-in-differences) is the same, with one key instead of two.

**(a) Your merged RAG feature.** The address of the merged pull request from your `rag` branch (README steps 5 to 7). Its **Files changed** must show:

- the code that chunks your documents, builds and saves the index, retrieves the closest chunks and asks for a grounded answer that names its sources;
- tests that use a fake embedder and a fake model and pass with no keys, including a test for "no Google key";
- your documents folder, with **course-safe documents only** (README step 5c);
- the index file listed in `.gitignore` and `.dockerignore`, and **not** committed;
- `.env.example` with fake keys, and the pinned packages;
- `REVIEW.md` with the week 10 section.

**No `.env`, no real key and no index file**, anywhere in the pull request or the repo's history.

**(b) Three questions** (README step 5e), each with the documents your program retrieved and its answer. At least one must be a question your documents **can't** answer, showing your program saying so.

**(c) A screenshot** of your index being built (with nothing secret on screen).

**(d) A short reflection,** about half a page:

1. **Chunk size:** one answer that was wrong, weak or "doesn't say" when it should have known. Why did that happen (look at the chunks it retrieved), and what did you change, or what would you change?
2. **Grounding:** how does your program stop the model from answering from general knowledge, and how would a user of your program check an answer?

Never put a key, a password, a sign-in code or anything from your `.env` file in your hand-in.

## What to hand in

- One document with the pull request's address, the three questions with their retrieved documents and answers, the screenshot and your reflection.

Submit it the way your course site says.

## Rubric

| Criterion | Points |
|---|---|
| Merged RAG pull request: fake embedder and fake model in the tests, a "no Google key" test, course-safe documents, and no key, `.env` or index file anywhere | 4 |
| Three questions with the retrieved documents and the answers, including one the documents can't answer, plus the index screenshot | 3 |
| Reflection: chunk size (2 points) and grounding (1 point) | 3 |
