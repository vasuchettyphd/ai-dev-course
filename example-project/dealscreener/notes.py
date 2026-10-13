"""Ask questions of your own investor notes (week 10).

  python3 -m dealscreener.notes index              reads notes/ and saves notes-index.json
  python3 -m dealscreener.notes ask "your question"  finds the best notes and asks Claude

How it works: each note is cut into chunks, and Google's embedding model turns each chunk
into a list of numbers (a vector) that stands for its meaning. A question gets a vector too,
and the chunks whose vectors point the most the same way (cosine similarity) are the best
matches. Claude Haiku then answers from those chunks only, and names the files it used.

This file uses only Python's standard library when it loads. The google-genai and anthropic
packages are needed only for real calls, so they are imported inside the functions that
make the clients. The tests use fake clients, so they run with no packages, keys or internet.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
from dataclasses import dataclass

from dealscreener import extract

# Chunks of at most this many characters: small enough that a match points at one idea.
CHUNK_CHARS = 800
# How many of the best-matching chunks go to Claude.
TOP_K = 3
# Google's text embedding model. It takes a task type (a note being stored, or a question
# being asked) and can return a shorter vector. From
# https://ai.google.dev/gemini-api/docs/embeddings (read 2026-10-13); Google lists its
# shutdown date as 14 May 2028 (https://ai.google.dev/gemini-api/docs/deprecations).
EMBED_MODEL = "gemini-embedding-001"
# 768 numbers per vector, one of the sizes Google recommends. This model doesn't scale a
# shorter vector to length 1 itself, so embed_texts does it.
EMBED_DIMENSIONS = 768
# Texts per request. Google doesn't publish a maximum, so the course keeps it at 100.
BATCH_SIZE = 100
INDEX_FILE = "notes-index.json"
NOTES_DIR = "notes"

USAGE = ("Usage:\n"
         "  python3 -m dealscreener.notes index\n"
         "  python3 -m dealscreener.notes ask \"your question\"")

RUN_INDEX = "Run: python3 -m dealscreener.notes index"

SYSTEM_PROMPT = (
    "You answer questions about a property investor's own notes. "
    "Answer only from the notes below. Do not use anything else you know. "
    "After your answer, list the file names you used, after the word Sources:. "
    "If the notes do not answer the question, reply exactly: My notes don't say."
)

# Claude's answer is short, so 1000 tokens leaves room for any thinking first.
ANSWER_MAX_TOKENS = 1000


class NotesError(Exception):
    """Something the user can fix. The message is one plain sentence."""


@dataclass(frozen=True)
class Chunk:
    source: str  # the note's file name, like "riverside-association-dues.md"
    number: int  # its place in that file, starting at 1
    text: str


@dataclass
class Answer:
    text: str
    input_tokens: int
    output_tokens: int


def chunk_text(text: str, source: str, max_chars: int = CHUNK_CHARS) -> list[Chunk]:
    """Cut one note into chunks of at most max_chars characters, keeping paragraphs whole
    where it can."""
    pieces = []
    text = text.replace("\r\n", "\n").replace("\r", "\n")  # Windows line endings
    for paragraph in re.split(r"\n(?:[ \t]*\n)+", text):  # one or more blank lines
        paragraph = paragraph.strip()
        while len(paragraph) > max_chars:  # too long on its own: cut at the last space
            cut = paragraph.rfind(" ", 0, max_chars + 1)
            if cut <= 0:
                cut = max_chars  # one very long word: cut it where the limit falls
            pieces.append(paragraph[:cut].rstrip())
            paragraph = paragraph[cut:].strip()
        if paragraph:
            pieces.append(paragraph)
    texts = []
    for piece in pieces:  # join neighbours while they still fit
        if texts and len(texts[-1]) + 2 + len(piece) <= max_chars:
            texts[-1] = texts[-1] + "\n\n" + piece
        else:
            texts.append(piece)
    return [Chunk(source, number, chunk) for number, chunk in enumerate(texts, start=1)]


def load_notes(folder: str = NOTES_DIR) -> tuple[list[Chunk], dict, list[str]]:
    """Read every .md and .txt file in the folder, in name order.

    Returns the chunks, a fingerprint (SHA-256) of each file so a changed note can be
    spotted later, and a message for each file that was skipped.
    """
    if not os.path.isdir(folder):
        raise NotesError(f"No notes folder found at {folder}.")
    chunks, fingerprints, skipped = [], {}, []
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if not name.lower().endswith((".md", ".txt")) or not os.path.isfile(path):
            continue
        with open(path, "rb") as note_file:
            data = note_file.read()
        fingerprints[name] = hashlib.sha256(data).hexdigest()
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            skipped.append(f"Skipped {name}: not plain text.")
            continue
        chunks.extend(chunk_text(text, name))  # an empty file gives no chunks, silently
    if not chunks:
        raise NotesError("The notes folder has no notes in it.")
    return chunks, fingerprints, skipped


def cosine(a: list[float], b: list[float]) -> float:
    """How much two vectors point the same way: 1 the same, 0 unrelated, -1 opposite."""
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(x * x for x in b))
    if length_a == 0 or length_b == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (length_a * length_b)


def normalise(vector: list[float]) -> list[float]:
    """The same vector scaled to length 1 (a vector of zeros stays as it is)."""
    length = math.sqrt(sum(x * x for x in vector))
    return [x / length for x in vector] if length else list(vector)


def embed_texts(texts: list[str], client, task_type: str) -> list[list[float]]:
    """Ask Google for one vector per text, BATCH_SIZE texts per request, in the same order.

    task_type is "RETRIEVAL_DOCUMENT" for notes being stored and "RETRIEVAL_QUERY" for a
    question. The config is a plain dict, which the google-genai library accepts in place
    of types.EmbedContentConfig, so this file needn't import the library.
    """
    vectors = []
    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start:start + BATCH_SIZE]
        result = client.models.embed_content(
            model=EMBED_MODEL,
            contents=batch,
            config={"task_type": task_type, "output_dimensionality": EMBED_DIMENSIONS},
        )
        if len(result.embeddings) != len(batch):
            raise NotesError("Google sent back the wrong number of embeddings.")
        vectors.extend(normalise(list(embedding.values)) for embedding in result.embeddings)
    return vectors


def build_index(folder, embed_client) -> dict:
    """Read the notes, embed every chunk, and return the index (not yet saved)."""
    chunks, fingerprints, _ = load_notes(folder)
    vectors = embed_texts([chunk.text for chunk in chunks], embed_client, "RETRIEVAL_DOCUMENT")
    return {
        "model": EMBED_MODEL,
        "dimensions": len(vectors[0]),
        "fingerprints": fingerprints,
        "chunks": [{"source": chunk.source, "number": chunk.number, "text": chunk.text,
                    "vector": vector} for chunk, vector in zip(chunks, vectors)],
    }


def save_index(index: dict, path: str = INDEX_FILE) -> None:
    try:
        with open(path, "w", encoding="utf-8") as index_file:
            json.dump(index, index_file)
    except OSError:  # for example a folder you can't write to, such as /app in the container
        raise NotesError(f"Couldn't save the index file {path}.") from None


def load_index(path: str = INDEX_FILE) -> dict:
    try:
        with open(path, encoding="utf-8") as index_file:
            index = json.load(index_file)
    except FileNotFoundError:
        raise NotesError(f"No index yet. {RUN_INDEX}") from None
    except (OSError, ValueError):
        raise NotesError(f"The index file can't be read. {RUN_INDEX}") from None
    if not isinstance(index, dict) or not isinstance(index.get("chunks"), list):
        raise NotesError(f"The index file can't be read. {RUN_INDEX}")
    return index


def check_fresh(index: dict, folder) -> None:
    """Stop if a note was added, edited or deleted since the index was built."""
    if index.get("model") != EMBED_MODEL or index.get("dimensions") != EMBED_DIMENSIONS \
            or not isinstance(index.get("fingerprints"), dict):
        raise NotesError(f"The index was built differently from what this program uses. {RUN_INDEX}")
    _, fingerprints, _ = load_notes(folder)
    if fingerprints != index["fingerprints"]:
        raise NotesError(f"Your notes changed since the index was built. {RUN_INDEX}")


def top_chunks(question_vector, index, k: int = TOP_K) -> list[tuple[float, Chunk]]:
    """The k chunks most like the question, best first. Equal scores keep the index order."""
    scored = [(cosine(question_vector, item["vector"]),
               Chunk(item["source"], item["number"], item["text"])) for item in index["chunks"]]
    scored.sort(key=lambda pair: -pair[0])  # sort keeps the earlier one first on a tie
    return scored[:k]


def answer(question: str, matches, claude_client) -> Answer:
    """One call to Claude Haiku, with the matching notes and the question."""
    notes_text = "\n\n".join(f"[{chunk.source} part {chunk.number}]\n{chunk.text}"
                             for _, chunk in matches)
    message = claude_client.messages.create(
        model=extract.MODEL,
        max_tokens=ANSWER_MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user",
                   "content": f"My notes:\n\n{notes_text}\n\nMy question: {question}"}],
    )
    if message.stop_reason == "max_tokens":
        raise NotesError("The answer was cut off before it finished.")
    if message.stop_reason == "refusal":
        raise NotesError("The model declined to answer.")
    # The reply can start with a thinking block: pick the answer by its type, not its place.
    texts = [block.text for block in message.content if getattr(block, "type", None) == "text"]
    if not texts:
        raise NotesError("The model's answer had no text in it.")
    return Answer("\n".join(texts).strip(), message.usage.input_tokens, message.usage.output_tokens)


def make_embed_client():
    """Return a Google client, or raise NotesError saying what is missing."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:  # checked here, because genai.Client() with no key stops with its own error
        raise NotesError("No Google API key found. Put GEMINI_API_KEY in a .env file (see the README).")
    try:
        from google import genai
    except ImportError:
        raise NotesError("The google-genai package isn't installed (pip install -r requirements.txt).") from None
    # Passing the key by hand means a GOOGLE_API_KEY set elsewhere can't take its place.
    return genai.Client(api_key=key)


def http_status(error):
    """The HTTP status a failed Google call carries in .code (google-genai's errors keep it
    there), or None if there isn't one."""
    code = getattr(error, "code", None)
    if isinstance(code, int) and not isinstance(code, bool) and 100 <= code <= 599:
        return code
    return None


def is_connection_error(error) -> bool:
    """True for a call that never reached Google: no internet, or no answer in time.
    The library's own connection errors are named like ConnectError or ReadTimeout."""
    name = type(error).__name__
    return isinstance(error, (OSError, ConnectionError, TimeoutError)) or \
        "Connect" in name or "Timeout" in name


def is_google_failure(error) -> bool:
    """A failed Google call (an HTTP error or a connection problem), as opposed to a
    mistake in this program, which should show up as one."""
    return http_status(error) is not None or is_connection_error(error)


def describe_google_error(error) -> str:
    """One plain sentence for a failed Google call. Fixed sentences only: never the error's
    own text, which could hold details we don't want on screen."""
    code = http_status(error)
    if code is None:
        if is_connection_error(error):
            return "Couldn't reach Google. Check your internet connection."
        return "The call to Google failed."
    # A wrong key comes back as 400 with "API key not valid" (seen on 13 October 2026).
    if code in (401, 403) or (code == 400 and "api key not valid" in str(error).lower()):
        return ("The Google API key was not accepted, or isn't allowed to do that. "
                "Check GEMINI_API_KEY in your .env file.")
    if code >= 500:
        return "Google's service is busy or having a problem. Try again later."
    messages = {
        400: "Google couldn't read the request.",
        404: "The embedding model name wasn't found.",
        429: "Too many requests for the free tier right now. Wait a minute and try again.",
    }
    return messages.get(code, "The call to Google failed.")


def main(argv, input_fn=input, print_fn=print, embed_factory=make_embed_client,
         claude_factory=extract.make_client) -> int:
    """Run one command. Returns 0 when it worked, 1 when it couldn't, 2 for a usage mistake.
    (input_fn is unused for now: the question comes from the command line.)"""
    extract.load_env_file()  # the API keys, from a .env file in this folder, if there is one
    command = argv[0] if argv else None
    question = " ".join(argv[1:]).strip()
    if command not in ("index", "ask") or (command == "ask" and not question):
        print_fn(USAGE)
        return 2
    if command == "index":
        return run_index(print_fn, embed_factory)
    return run_ask(question, print_fn, embed_factory, claude_factory)


def run_index(print_fn, embed_factory) -> int:
    try:
        chunks, _, skipped = load_notes(NOTES_DIR)
        for message in skipped:
            print_fn(message)
        index = build_index(NOTES_DIR, embed_factory())
        save_index(index, INDEX_FILE)
    except NotesError as problem:
        print_fn(str(problem))
        return 1
    except Exception as error:  # a failed Google call: a plain sentence, never the key
        if not is_google_failure(error):
            raise  # a mistake in this program: show it, don't blame Google
        print_fn(describe_google_error(error))
        return 1
    note_count = len({chunk.source for chunk in chunks})
    print_fn(f"Indexed {len(index['chunks'])} chunks from {note_count} notes.")
    return 0


def run_ask(question, print_fn, embed_factory, claude_factory) -> int:
    try:
        index = load_index(INDEX_FILE)
        check_fresh(index, NOTES_DIR)
        question_vector = embed_texts([question], embed_factory(), "RETRIEVAL_QUERY")[0]
    except NotesError as problem:
        print_fn(str(problem))
        return 1
    except Exception as error:
        if not is_google_failure(error):
            raise
        print_fn(describe_google_error(error))
        return 1
    matches = top_chunks(question_vector, index)
    print_fn("Notes that match best:")
    for score, chunk in matches:
        print_fn(f"  {chunk.source} part {chunk.number} (similarity {score:.2f})")
    try:
        result = answer(question, matches, claude_factory())
    except (NotesError, extract.ExtractionError) as problem:
        return show_notes_instead(str(problem), matches, print_fn)
    except Exception as error:  # a failed Claude call: the week 9 sentences
        return show_notes_instead(extract.describe_error(error), matches, print_fn)
    print_fn("")
    print_fn(result.text)
    print_fn("")
    cost = extract.cost_usd(result.input_tokens, result.output_tokens)
    print_fn(f"Used {result.input_tokens} input and {result.output_tokens} output tokens "
             f"on Claude, about ${cost:.5f}.")
    return 0


def show_notes_instead(sentence, matches, print_fn) -> int:
    """Claude couldn't answer: say why, then show the matching notes themselves."""
    print_fn(f"{sentence} Here are the notes that match best instead.")
    for _, chunk in matches:
        print_fn("")
        print_fn(f"[{chunk.source} part {chunk.number}]")
        print_fn(chunk.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
