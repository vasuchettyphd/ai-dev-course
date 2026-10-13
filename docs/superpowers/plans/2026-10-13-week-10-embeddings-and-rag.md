# Week 10 (Embeddings and RAG) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 10. Students learn what an embedding is and why meaning search beats keyword search. They get a Google AI Studio (Gemini API) key safely, make a first embedding and compare similarities, and then build RAG step by step (chunk, index, retrieve, grounded answer with sources). Finally they add RAG over their own course-safe documents to `semester-project`, with offline tests and a working fallback, merged through a PR. The deal screener gets investor notes and a `notes` command (tag `week-10`). The week also adds slides, the assignment, instructor notes with a demo script, and checklist rows.

**Architecture:**
- Same approach as week 9.
- Facts come from Google's official Gemini API docs and Anthropic's docs, and are recorded on a fact sheet with URLs:
  - Google: embeddings guide, the `google-genai` Python SDK, models and prices, free-tier rate limits, the AI Studio key steps, API key safety, the Gemini API terms (free vs paid data use), available regions, and Workspace for Education access.
  - Anthropic, from week 9: the answer step with Haiku.
- Live calls use the user's `GEMINI_API_KEY` and `ANTHROPIC_API_KEY` from `~/.bashrc`. Each key is loaded into one command only and never printed.
- The deal screener's new module is standard library at import time and imports both SDKs lazily. Its tests use fake embeddings and a fake model.

**Tech Stack:** Markdown, Marp, Python 3.10+ for the SDKs (the deal screener's own logic stays 3.9+), `google-genai` (pinned), `anthropic==1.13.0`, Docker.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 10 row ("Embeddings and RAG | Search by meaning, chunking, retrieval, grounded answers | Add RAG over their own documents"). The week 10 design was approved in conversation on 2026-10-13. Decisions:
- Embeddings come from Google (Gemini API, AI Studio key). The user believes UVU students have free access; the fact sheet checks this, and anything unconfirmed is marked "check before class".
- Answers come from Claude Haiku 5.5, as in week 9.
- Deal screener documents: about 8 fictional investor notes written for the course.
- Assignment: merged RAG PR with offline tests, a no-key test, no keys and no private documents (4); three questions with retrieved sources and answers, including one the documents can't answer (3); reflection on chunk size and grounding (3).

**Refinement made while planning:** the deal screener's commands are `python3 -m dealscreener.notes index` and `python3 -m dealscreener.notes ask "..."`, not a `--ask` flag. This leaves `__main__.py` and its 92 tests untouched.

## Global Constraints

- **Audience and context:** business and non-CS students in week 10, with everything from weeks 1-9, including the week 9 key rules, `.env`, the `Read(./.env)` deny rule and `~/first-call/.venv`. Their projects may not be Python. Use plain language. Every command and prompt is exact and says where to type it.
- **Platforms:** Mac (Apple chip), Mac (Intel) and Windows (WSL 2 Ubuntu).
- **Key safety (week 9 rules, now for two keys):**
  - Students type keys into `.env` with a text editor and never paste them into a chat.
  - Check `git check-ignore .env`.
  - The deny rule stays.
  - Programs read keys only from the environment and never print them.
  - Docker gets keys with `--env-file .env`.
  - If a key leaks, revoke it first. Google's revoke steps come from the fact sheet.
  - Set spend or usage limits where Google offers them.
- **Privacy:**
  - Students send only course-safe documents (their own writing, public material, or the course's fictional notes), never personal, customer or confidential data.
  - Say exactly what Google's terms say about data sent on the free tier versus the paid tier (quoted, from the fact sheet).
  - The saved index contains the documents' text. It follows the same rule, and the README says whether to commit it.
- **Cost:**
  - Every price, free-tier limit and model ID comes from Google's or Anthropic's pages on the fact sheet, with the date it was read.
  - No invented numbers.
  - Embedding the documents happens once (the index file). Each question is one small embedding plus one Haiku call.
- **Git rules from weeks 3-9:**
  - Branch first, and never change `main`.
  - Open a PR, read Files changed, merge, then pull.
  - The repo stays private.
  - Answer plain "Yes" to git commands.
  - Answer "No" to `reset --hard`, `--force`, `git clean` and `rm -rf`.
  - Use the week 5 rescue for work committed to `main`.
- **Testing and verification:**
  - Tests never call the real APIs by default. A live test runs only with `RUN_LIVE_TESTS=1`.
  - Everything not observed is marked "being tested". Pin the versions used.
- **Formatting and repo rules:**
  - No em dashes (U+2014) or en dashes (U+2013).
  - The rubric is a table under `## Rubric`, totalling 10.
  - `example-project/` stays the labelled instructor example. It passes `scripts/check_course.py`, and its offline tests run on the host (with or without the SDKs) and in the container.
  - Instructor-only material goes in the private repo.
- **Branches:** `week-10-embeddings-and-rag` in the course repo and `week-10` in the instructor repo. The user merges. Links come first, one bare URL per line.
- **Session disconnects:** the controller writes the docs tasks (3 and 4) itself, committing per section. Disconnects killed background agents three times in week 9. Reviews stay with subagents.

## Review Focus

1. **The index goes stale.** If a note is edited, added or deleted after `index`, `ask` would use old text. The index stores each file's SHA-256, and `ask` refuses with "Your notes changed since the index was built. Run: python3 -m dealscreener.notes index" (Task 2 tests add, edit and delete).
2. **The notes don't contain the answer.** The model is told to answer only from the given notes, to name the files it used, and to say exactly "My notes don't say." otherwise. The prompt's text is pinned by a test. A live check in Task 2 asks one unanswerable question, and the README shows it.
3. **Keys are missing or calls fail.**
   - With no Google key, `index` and `ask` say so in one sentence.
   - With no Anthropic key, `ask` still prints the best-matching notes ("Here are the notes that match best:") without an answer.
   - Google and Anthropic errors (bad key, rate limit, quota, network) become fixed plain sentences that never echo the error text.
   - Task 2 tests each case.
4. **The documents are awkward.**
   - A missing or empty `notes/` folder gets a plain message.
   - A non-UTF-8 or non-text file is skipped with a note.
   - A very long note is split into several chunks.
   - Blank-only files are skipped.
   - Tests cover each case.
5. **Cost or size surprises.**
   - Embeddings are sent in batches no bigger than the API's limit (from the fact sheet).
   - The index stores vectors at the dimension the fact sheet chooses.
   - Each command prints the tokens and estimated cost it used, or "free tier" where Google gives no per-call price.
   - `notes-index.json` is ignored by git and by Docker.

---

### Task 1: Fact sheet and dry run

**Files:** none in the repo. Write the report only.

- [ ] **Step 1:** Record, with URL and date, from Google's official pages (ai.google.dev, cloud.google.com, policies.google.com, support.google.com), and quote exactly:
  - **Getting a key:**
    - the AI Studio key steps
    - whether a Google Workspace for Education account (a school account like UVU's) can use AI Studio or the Gemini API, and what blocks it (admin settings, age rules)
    - regions where it's available
    - how to restrict, delete or rotate a key
  - **Money and terms:**
    - the free tier's limits for the embedding model (requests per minute, per day, tokens)
    - paid prices for the embedding model, and whether embedding inputs are billed by token or character
    - how to set a budget or spend cap, if one exists
    - the Gemini API terms on how free-tier and paid-tier data is used, quoted exactly
  - **The `google-genai` SDK:**
    - package name, current version, minimum Python and install command
    - the environment variable it reads (`GEMINI_API_KEY` and/or `GOOGLE_API_KEY`, and which wins)
    - the exact `embed_content` call shape: model ID, `contents` as a list, `config` with `task_type` (`RETRIEVAL_DOCUMENT` / `RETRIEVAL_QUERY`) and `output_dimensionality`
    - the response shape (`embeddings[i].values`), and whether token counts come back
    - the maximum texts per request and tokens per text
    - the error classes and their attributes (status code, message), and what happens with no key
  - **The model:** the current embedding model ID (expected `gemini-embedding-001`), its default and allowed dimensions, and Google's advice on normalising vectors when the dimension is reduced.
  - **Explaining it to students:** Google's own plain explanation of embeddings and of cosine similarity, if there is one, for the README to quote.
  - **Anthropic:** reuse week 9's facts (Haiku 5.5 ID and prices, SDK 1.13.0, no `temperature`, blocks by type, `stop_reason`). Confirm nothing changed since 12 October 2026.
- [ ] **Step 2: Dry run in a clean `python:3.12-slim` container, as a non-root user:**
  - `pip install google-genai==<current>`
  - import it and print the version
  - run the minimal embedding example with no key and record the exact error
- [ ] **Step 3: Live check.** Load `GEMINI_API_KEY` for one command only, with `eval "$(grep '^export GEMINI_API_KEY=' ~/.bashrc | tail -1)"`, and pass it into the container by name with `-e GEMINI_API_KEY`. Never print it. Record:
  - **The two-sentence comparison:** embed two similar sentences and one unrelated sentence, and record the dimensions and three cosine similarities.
  - **Response metadata:** whether any token count or billing information comes back.
  - **Batches:** one batch of 10 texts.
  - **A bad key:** one call with `GEMINI_API_KEY=invalid`. Record the error class, status and message.
  - **If the key isn't in `~/.bashrc`:** mark every live item "being tested" and tell the controller.
- [ ] **Step 4:** Write the report: facts, transcripts, versions and the date. Never write a key.

### Task 2: Deal screener investor notes and the `notes` command (example-project)

**Files:**
- Create:
  - `example-project/notes/` (8 notes, `.md`)
  - `example-project/dealscreener/notes.py`
  - `example-project/tests/test_notes.py`
  - `example-project/tests/test_notes_live.py`
- Modify:
  - `example-project/requirements.txt` (add `google-genai==<pinned>`)
  - `example-project/.env.example` (add `GEMINI_API_KEY=put-your-key-here`)
  - `example-project/.dockerignore` (`notes-index.json`)
  - course `.gitignore` (`notes-index.json`)
  - `example-project/README.md`:
    - a "What's here now (week 10)" section
    - the week 10 row in "How it grows"
    - "How to ask your notes", with the Google key setup, `index`, `ask` and Docker
    - the cost record

**The notes:**
- About 8 short notes, each 3 to 12 lines, clearly labelled "Fictional notes written for this course example; no real people or addresses."
- Cover these topics:
  - Riverside HOA fees, using the words "association dues" and never "HOA"
  - the university district
  - a rule of thumb for repairs reserves
  - a past deal write-up (listing B)
  - lender notes on down payments
  - a property tax reassessment note
  - an insurance quote note
  - a note with nothing about money (a contractor's phone etiquette), as a distractor
- One note must be long enough, over the chunk size, to split into two chunks.

**Interfaces (`dealscreener/notes.py`; standard library at import time, SDKs imported inside functions):**
- `@dataclass(frozen=True) class Chunk: source: str; number: int; text: str`
- `CHUNK_CHARS = 800`; `TOP_K = 3`; `EMBED_MODEL = "<fact sheet ID>"`; `EMBED_DIMENSIONS = <fact sheet choice, e.g. 768>`; `BATCH_SIZE = <fact sheet max, at most 100>`; `INDEX_FILE = "notes-index.json"`; `NOTES_DIR = "notes"`
- `class NotesError(Exception)`: its message is one plain sentence.
- `chunk_text(text: str, source: str, max_chars: int = CHUNK_CHARS) -> list[Chunk]`:
  - Split on blank lines into paragraphs.
  - Join consecutive paragraphs while the total stays at or under `max_chars`.
  - A single paragraph longer than `max_chars` is cut at the last space before the limit.
  - Chunks are numbered from 1 per file.
  - Whitespace-only text gives `[]`.
- `load_notes(folder: str = NOTES_DIR) -> tuple[list[Chunk], dict, list[str]]` returns (chunks, fingerprints by filename of SHA-256 hex, skipped messages).
  - It reads `*.md` and `*.txt` in sorted order.
  - A file that isn't UTF-8 is skipped with "Skipped <name>: not plain text."
  - Empty files are skipped silently.
  - A missing folder raises `NotesError("No notes folder found at <folder>.")`.
  - No chunks at all raises `NotesError("The notes folder has no notes in it.")`.
- `cosine(a: list[float], b: list[float]) -> float` returns 0.0 when either vector is all zeros.
- `embed_texts(texts: list[str], client, task_type: str) -> list[list[float]]`:
  - Sends batches of at most `BATCH_SIZE`.
  - Uses the fact sheet's exact call shape, with `task_type` and `EMBED_DIMENSIONS`.
  - Returns vectors in input order.
- `build_index(folder, embed_client) -> dict` returns `{"model": EMBED_MODEL, "dimensions": n, "fingerprints": {...}, "chunks": [{"source", "number", "text", "vector"}]}`. Embeddings use `RETRIEVAL_DOCUMENT`.
- `save_index(index, path=INDEX_FILE)` and `load_index(path=INDEX_FILE) -> dict`.
  - A missing index raises `NotesError("No index yet. Run: python3 -m dealscreener.notes index")`.
- `check_fresh(index, folder) -> None` raises `NotesError("Your notes changed since the index was built. Run: python3 -m dealscreener.notes index")` if the fingerprints differ (added, edited or deleted file).
- `top_chunks(question_vector, index, k=TOP_K) -> list[tuple[float, Chunk]]`, highest score first. Ties keep index order.
- `SYSTEM_PROMPT` (pinned by a test) contains:
  - "Answer only from the notes below."
  - "After your answer, list the file names you used, after the word Sources:."
  - "If the notes do not answer the question, reply exactly: My notes don't say."
- `answer(question, matches, claude_client) -> Answer` with `Answer(text: str, input_tokens: int, output_tokens: int)`:
  - Makes one Haiku call: `model=extract.MODEL`, `max_tokens=1000`, `system=SYSTEM_PROMPT`.
  - The user message holds the numbered notes, each headed `[<source> part <number>]`, then the question.
  - Text is taken from text blocks by type.
  - `stop_reason` `max_tokens` raises "The answer was cut off before it finished."; `refusal` raises "The model declined to answer."
- `make_embed_client()`:
  - Raises `NotesError("No Google API key found. Put GEMINI_API_KEY in a .env file (see the README).")` if the variable from the fact sheet is unset.
  - Raises "The google-genai package isn't installed (pip install -r requirements.txt)." if the package can't be imported.
- `describe_google_error(error) -> str`: fixed sentences only, chosen by the status attribute from the fact sheet:
  - 400: "Google couldn't read the request."
  - 401 or 403: "The Google API key was not accepted, or isn't allowed to do that. Check GEMINI_API_KEY in your .env file."
  - 404: "The embedding model name wasn't found."
  - 429: "Too many requests for the free tier right now. Wait a minute and try again."
  - 5xx: "Google's service is busy or having a problem. Try again later."
  - no status: "Couldn't reach Google. Check your internet connection."
- `main(argv, input_fn=input, print_fn=print, embed_factory=make_embed_client, claude_factory=extract.make_client) -> int`, run with `python3 -m dealscreener.notes ...`. It calls `extract.load_env_file()` first.
  - **`index`:**
    - loads the notes, prints each skipped message, embeds, saves
    - prints "Indexed N chunks from M notes." and returns 0
  - **`ask "<question>"`:**
    - loads the index and checks it's fresh, then embeds the question with `RETRIEVAL_QUERY`
    - prints "Notes that match best:" and one line per match, `  <source> part <n> (similarity 0.xx)`
    - asks Haiku and prints the answer
    - prints "Used <in> input and <out> output tokens on Claude, about $<cost:.5f>."
    - returns 0
  - **Failures:**
    - If the Claude factory or call fails, it prints the plain sentence plus " Here are the notes that match best instead." after the match list, and returns 0.
    - A `NotesError` or Google failure prints its sentence and returns 1.
    - No subcommand, or `ask` with no question, prints usage and returns 2.

**Tests (`tests/test_notes.py`, offline):**

```python
"""Tests for asking the investor notes. Fake embeddings and a fake model: no network, no keys."""
import os, tempfile, unittest
from types import SimpleNamespace
from dealscreener import notes

# A fake embedder: each vector counts concept words, so "association dues" and "HOA" land together.
CONCEPTS = [("hoa", "association dues", "dues"), ("tax", "assessment"), ("insurance", "premium"),
            ("phone", "call", "text message"), ("repair", "reserve", "maintenance")]

def fake_vector(text):
    t = text.lower()
    return [float(sum(t.count(w) for w in group)) for group in CONCEPTS]

class FakeEmbedClient:
    def __init__(self, error=None): self.calls, self.error = [], error
    def embed(self, texts, task_type):            # the shape notes.embed_texts uses via an adapter
        self.calls.append((list(texts), task_type))
        if self.error: raise self.error
        return [fake_vector(t) for t in texts]
```

Task 2's implementer adapts `FakeEmbedClient` to the real call shape from the fact sheet, for example by giving it `.models.embed_content(...)` returning objects with `.embeddings[i].values`. Tests must exercise `embed_texts` through that same shape, not a shortcut. Test list (each its own method):
- **Chunking (`chunk_text`):**
  - `test_chunk_joins_short_paragraphs_up_to_the_limit`
  - `test_chunk_splits_a_long_paragraph_at_a_space`
  - `test_chunk_numbers_start_at_one_per_file`
  - `test_whitespace_only_text_gives_no_chunks`
- **Loading notes (`load_notes`):**
  - `test_load_notes_reads_md_and_txt_in_order`
  - `test_non_utf8_file_is_skipped_with_a_message`
  - `test_missing_folder_says_so`
  - `test_empty_folder_says_so`
- **Similarity:**
  - `test_cosine_of_identical_is_one_and_zero_vector_is_zero`
  - `test_association_dues_note_matches_an_hoa_question` (the meaning-search point)
- **Embedding calls:**
  - `test_embed_texts_batches_and_keeps_order` (25 texts with `BATCH_SIZE` patched to 10 gives 3 calls, in order)
  - `test_document_and_query_task_types_are_sent`
- **Building and loading the index:**
  - `test_build_save_load_round_trip`
  - `test_index_is_stale_after_add_edit_or_delete`
  - `test_missing_index_says_run_index`
- **Answering:**
  - `test_answer_prompt_pins_grounding_rules`
  - `test_answer_reads_text_blocks_after_thinking`
  - `test_answer_cut_off_and_refusal_are_errors`
- **Keys, clients and errors:**
  - `test_no_google_key_says_how_to_add_one`
  - `test_missing_google_package_says_how_to_install_it`
  - `test_google_errors_get_fixed_sentences_without_the_key`, with statuses 400, 401, 403, 404, 429, 500, 503 and none, and a key string inside the error text that must not appear
- **The command:**
  - `test_main_index_prints_count`
  - `test_main_ask_prints_matches_answer_and_cost`
  - `test_main_ask_without_claude_key_still_prints_matches`
  - `test_main_ask_with_stale_index_refuses`
  - `test_main_usage_errors_return_2`

**Live test (`tests/test_notes_live.py`):** skipped unless `RUN_LIVE_TESTS=1` and both keys are set. It builds the index from `notes/` into a temp file and asks "What are the association dues like in Riverside?". The Riverside note must be among the matches, and the answer must not be "My notes don't say.".

- [ ] **Step 1:** Write `notes/`, update `requirements.txt` and `.env.example`, and add `notes-index.json` to the course `.gitignore` and `example-project/.dockerignore`.
- [ ] **Step 2:** Write `tests/test_notes.py` and watch it fail (no module).
- [ ] **Step 3:** Write `dealscreener/notes.py` until the tests pass with plain `python3` and no SDKs installed. Run the whole suite: all 92 old tests still pass, and record the new total.
- [ ] **Step 4: Live**, in a `python:3.12-slim` container with `pip install -r requirements.txt`, both keys passed by name with `-e` (loaded from `~/.bashrc` for that one command), and nothing printed:
  - run `index` and record the chunk count and time
  - ask three questions, recording matches, answer, tokens and cost: the Riverside association dues question, "What repairs reserve did I use for listing B?", and "What did I note about solar panels?" (expect "My notes don't say.")
  - run the live test
  - record whether Google returns token counts (for the cost line)
- [ ] **Step 5: Docker:**
  - build `dealscreener-w10`
  - run the offline tests in the container
  - run `ls -a /app` and check there is no `.env` or `notes-index.json`
  - run `docker run --rm -e GEMINI_API_KEY -e ANTHROPIC_API_KEY -v "$PWD/notes-index.json:/app/notes-index.json:ro" ...`, or build the index inside the container first, whichever the README will teach (record the choice)
  - remove the image
- [ ] **Step 6:** Update the example README (real numbers from step 4), run `check_course.py`, check there are no dashes, check `git status` shows no `.env` or index, and commit.

### Task 3: README, slides and assignment (controller writes, committing per section)

**Files:** `weeks/10-embeddings-and-rag/README.md` (replace the stub), `slides.md`, `slides.pdf`, `assignment.md`.

- [ ] **README:** follow the approved design, steps 1-7:
  1. **Search by meaning:**
     - what an embedding is, in plain words
     - keyword versus meaning search, using the deal screener's "association dues" note
     - cosine similarity in one paragraph
  2. **Get a Google key safely (before class):**
     - the AI Studio steps
     - school account versus personal account, saying exactly what the fact sheet found and marking the rest "check with your instructor"
     - the free-tier limits and the data-use terms, quoted
     - `GEMINI_API_KEY=` in `.env`, with no quotes
     - the week 9 deny rule covers it
     - restricting and deleting the key
  3. **First embedding**, in `~/first-call` (week 9's venv):
     - `pip install google-genai==<pinned>`
     - a `cat > embed.py <<'EOF'` script that embeds three sentences and prints the dimensions and the three similarities
     - the real output
  4. **RAG step by step, using the deal screener:**
     - chunk, index, retrieve, then a grounded answer with sources
     - "My notes don't say." on the solar panels question
     - what goes wrong without grounding, in one paragraph
  5. **Add RAG to `semester-project`:**
     - branch `rag` first
     - pick course-safe documents (a list of good and bad examples)
     - the Superpowers prompt with guardrails: both keys from the environment only; a `Read(./.env)` deny rule check; fake embeddings and a fake model in tests; a live test only on request; a no-key test; the index ignored by git if the documents aren't public; cost or usage printed; the Dockerfile installs packages
     - Yes and No rules
     - Node.js students: the official Google JavaScript SDK name from the fact sheet
  6. **Review and run:**
     - `safe-and-private`, focused on keys, documents and the index
     - Docker with `--env-file .env`
     - PR, Files changed (no `.env`, no index unless public), merge, pull
  7. **Check it worked, and troubleshooting:**
     - Google 400, 401/403, 404 and 429 (free tier), the "not available in your region" message, and a school account blocked from AI Studio
     - no Google key
     - `ModuleNotFoundError: google`
     - a stale index
     - "My notes don't say." when they do (chunk size, wording)
     - the wrong note cited
     - an empty notes folder
     - a non-text file skipped
     - committing the index by mistake
     - week 9's Anthropic rows (link them)
     - the week 5 rescue
- [ ] **Slides:** 16-20 slides, including keyword versus meaning search, the "numbers for meaning" picture in plain words (a table of 3 sentences and their similarities), the RAG pipeline (chunk, embed, store, retrieve, answer), the grounding prompt, the "My notes don't say." example, and the assignment. Build only this week's PDF with `sh scripts/build-slides.sh weeks/10-embeddings-and-rag/slides.md`. Render the PNGs into the session scratchpad and look at the densest slides.
- [ ] **Assignment:**
  - **Hand in:**
    - the merged PR
    - three questions, each with its retrieved sources and the answer (one the documents can't answer)
    - a screenshot of the index being built
    - a reflection on chunk size and grounding: one answer that was wrong or weak, why, and what changed
  - **Rubric:**
    - PR with offline tests (fake embeddings and fake model), a no-key test, no key and no private documents or index: 4 points
    - three questions with sources and answers, including the unanswerable one: 3 points
    - reflection: 3 points
    - Total: 10 points
- [ ] **Checks:** `check_course.py` prints OK, no dashes, and every quote matches the fact sheet.

### Task 4: Instructor notes, demo script and checklist (private repo, controller writes)

- [ ] `weeks/10-embeddings-and-rag/notes.md`:
  - **Timing:** 75 minutes, with key setup before class. The pre-class email covers the Google key, the school versus personal account question, and the privacy rule.
  - **Demo script:**
    - add notes RAG live from a scratch clone at tag `week-09`
    - keys never on screen, a deny rule in the clone
    - a fallback clone at `week-10`
  - **Common problems:**
    - UVU account blocked from AI Studio (marked "check before class": record what you find)
    - region messages
    - free-tier 429 in a full classroom
    - students sending private documents
    - a committed index
    - a stale index
    - two keys mixed up
    - non-Python projects
  - **Discussion answers.**
  - **Grading guidance:** 10/10 and 6/10 examples that add up, and how to check a PR for keys, private documents and a committed index.
- [ ] `weeks/10-embeddings-and-rag/test-checklist.md`:
  - three tables with identical numbering, generated from one row list
  - every README step and troubleshooting row
  - a row that records what a real UVU student account shows in AI Studio
- [ ] No dashes and no keys. Commit on `week-10`.

### Task 5: PRs, tag and tracking (controller)

- [ ] Scan both branches for key-like strings: `sk-ant-` and Google key prefixes from the fact sheet (for example `AIza`). Only fakes are allowed.
- [ ] Push both branches and open the PRs. Links come first, and ask for a merge commit.
- [ ] After merge:
  - tag `week-10`
  - check the demo fallback clone
  - close the OpenProject task
  - delete the branches and the workspace
