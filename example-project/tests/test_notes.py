"""Tests for asking the investor notes. Fake embeddings and a fake model: no network, no keys."""
import json
import math
import os
import pathlib
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from dealscreener import extract, notes
from tests.test_extract import FakeAPIError, FakeClient

NOTES_FOLDER = pathlib.Path(__file__).parent.parent / "notes"

# A fake embedder: each vector counts concept words, so "association dues" and "HOA" land together.
CONCEPTS = [("hoa", "association dues", "dues"), ("tax", "assessment"), ("insurance", "premium"),
            ("phone", "call", "text message"), ("repair", "reserve", "maintenance")]


def fake_vector(text):
    t = text.lower()
    return [float(sum(t.count(w) for w in group)) for group in CONCEPTS]


class FakeEmbedClient:
    """Stands in for genai.Client(): the same shape, client.models.embed_content(...), which
    returns an object whose .embeddings[i].values is the vector for the i-th text."""

    def __init__(self, error=None):
        self.calls, self.error = [], error
        self.models = self

    def embed_content(self, model, contents, config):
        self.calls.append({"model": model, "contents": list(contents), "config": config})
        if self.error:
            raise self.error
        # Like Google, give vectors of the size asked for: the concept counts, then zeros.
        size = config["output_dimensionality"]
        return SimpleNamespace(embeddings=[
            SimpleNamespace(values=(fake_vector(t) + [0.0] * size)[:size]) for t in contents])


class FakeGoogleError(Exception):
    """Like google.genai.errors.APIError: carries the HTTP status in .code."""

    def __init__(self, code, message="error"):
        super().__init__(message)
        self.code = code


class ConnectError(Exception):
    """Named like the connection errors of httpx, the library google-genai uses."""


class ReadTimeout(Exception):
    """Named like httpx's error when Google doesn't answer in time."""


def answer_reply(text="Dues are $240 a month.\n\nSources: riverside-association-dues.md",
                 thinking=True, stop_reason="end_turn", input_tokens=700, output_tokens=40):
    blocks = [SimpleNamespace(type="text", text=text)]
    if thinking:
        blocks.insert(0, SimpleNamespace(type="thinking", thinking=""))
    return SimpleNamespace(content=blocks, stop_reason=stop_reason,
                           usage=SimpleNamespace(input_tokens=input_tokens, output_tokens=output_tokens))


def write(folder, name, content):
    path = os.path.join(folder, name)
    mode = "wb" if isinstance(content, bytes) else "w"
    with open(path, mode, **({} if mode == "wb" else {"encoding": "utf-8"})) as handle:
        handle.write(content)
    return path


class ChunkTextTest(unittest.TestCase):
    def test_chunk_joins_short_paragraphs_up_to_the_limit(self):
        text = "a" * 30 + "\n\n" + "b" * 30 + "\n\n" + "c" * 30
        chunks = notes.chunk_text(text, "n.md", max_chars=70)
        # 30 + 2 + 30 = 62 fits; adding the third would make 94, so it starts a new chunk.
        self.assertEqual([c.text for c in chunks], ["a" * 30 + "\n\n" + "b" * 30, "c" * 30])

    def test_chunk_splits_a_long_paragraph_at_a_space(self):
        text = "word " * 40  # 200 characters, one paragraph
        chunks = notes.chunk_text(text, "n.md", max_chars=52)
        for chunk in chunks:
            self.assertLessEqual(len(chunk.text), 52)
            self.assertFalse(chunk.text.startswith(" ") or chunk.text.endswith(" "))
            self.assertNotIn("wor ", chunk.text + " ")  # never cut inside a word
        self.assertEqual(" ".join(c.text for c in chunks), " ".join(["word"] * 40))

    def test_chunk_numbers_start_at_one_per_file(self):
        first = notes.chunk_text("x " * 100, "a.md", max_chars=60)
        second = notes.chunk_text("y " * 100, "b.md", max_chars=60)
        self.assertEqual([c.number for c in first], list(range(1, len(first) + 1)))
        self.assertEqual(second[0].number, 1)
        self.assertEqual({c.source for c in second}, {"b.md"})

    def test_windows_line_endings_and_extra_blank_lines_still_split_paragraphs(self):
        text = "a" * 30 + "\r\n\r\n" + "b" * 30 + "\n\n\n \n" + "c" * 30
        chunks = notes.chunk_text(text, "n.md", max_chars=40)
        self.assertEqual([c.text for c in chunks], ["a" * 30, "b" * 30, "c" * 30])

    def test_whitespace_only_text_gives_no_chunks(self):
        self.assertEqual(notes.chunk_text("  \n\n \t\n", "a.md"), [])

    def test_the_long_course_note_splits_into_two_chunks(self):
        text = (NOTES_FOLDER / "listing-b-write-up.md").read_text(encoding="utf-8")
        self.assertGreater(len(text), notes.CHUNK_CHARS)
        self.assertEqual(len(notes.chunk_text(text, "listing-b-write-up.md")), 2)


class LoadNotesTest(unittest.TestCase):
    def test_load_notes_reads_md_and_txt_in_order(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "b.txt", "Bee note.")
            write(folder, "a.md", "Ay note.")
            write(folder, "c.csv", "not,a,note")
            write(folder, "empty.md", "")
            chunks, fingerprints, skipped = notes.load_notes(folder)
        self.assertEqual([(c.source, c.number, c.text) for c in chunks],
                         [("a.md", 1, "Ay note."), ("b.txt", 1, "Bee note.")])
        self.assertEqual(set(fingerprints), {"a.md", "b.txt", "empty.md"})
        self.assertTrue(all(len(v) == 64 for v in fingerprints.values()))
        self.assertEqual(skipped, [])

    def test_capital_letter_endings_are_read_too(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "A.MD", "Capital md.")
            write(folder, "B.TXT", "Capital txt.")
            chunks, fingerprints, _ = notes.load_notes(folder)
        self.assertEqual([c.source for c in chunks], ["A.MD", "B.TXT"])
        self.assertEqual(set(fingerprints), {"A.MD", "B.TXT"})

    def test_non_utf8_file_is_skipped_with_a_message(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "good.md", "A good note.")
            write(folder, "photo.txt", b"\xff\xd8\xff\xe0 binary")
            chunks, _, skipped = notes.load_notes(folder)
        self.assertEqual([c.source for c in chunks], ["good.md"])
        self.assertEqual(skipped, ["Skipped photo.txt: not plain text."])

    def test_missing_folder_says_so(self):
        with tempfile.TemporaryDirectory() as folder:
            missing = os.path.join(folder, "nope")
            with self.assertRaises(notes.NotesError) as caught:
                notes.load_notes(missing)
        self.assertEqual(str(caught.exception), f"No notes folder found at {missing}.")

    def test_empty_folder_says_so(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "blank.md", "   \n")
            with self.assertRaises(notes.NotesError) as caught:
                notes.load_notes(folder)
        self.assertEqual(str(caught.exception), "The notes folder has no notes in it.")


class SimilarityTest(unittest.TestCase):
    def test_cosine_of_identical_is_one_and_zero_vector_is_zero(self):
        self.assertAlmostEqual(notes.cosine([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0)
        self.assertAlmostEqual(notes.cosine([1.0, 0.0], [0.0, 1.0]), 0.0)
        self.assertAlmostEqual(notes.cosine([1.0, 0.0], [-1.0, 0.0]), -1.0)
        self.assertEqual(notes.cosine([0.0, 0.0], [1.0, 2.0]), 0.0)
        self.assertEqual(notes.cosine([1.0, 2.0], [0.0, 0.0]), 0.0)

    def test_association_dues_note_matches_an_hoa_question(self):
        index = notes.build_index(str(NOTES_FOLDER), FakeEmbedClient())
        question = notes.embed_texts(["What are the HOA fees like in Riverside?"],
                                     FakeEmbedClient(), "RETRIEVAL_QUERY")[0]
        matches = notes.top_chunks(question, index)
        self.assertEqual(matches[0][1].source, "riverside-association-dues.md")
        # The note never says "HOA": the match comes from meaning, not the same word.
        self.assertNotIn("hoa", matches[0][1].text.lower())

    def test_top_chunks_keeps_index_order_for_ties(self):
        index = {"chunks": [{"source": s, "number": 1, "text": s, "vector": v} for s, v in
                            [("a.md", [1.0, 0.0]), ("b.md", [0.0, 1.0]), ("c.md", [1.0, 0.0])]]}
        matches = notes.top_chunks([1.0, 0.0], index, k=3)
        self.assertEqual([c.source for _, c in matches], ["a.md", "c.md", "b.md"])
        self.assertEqual(len(notes.top_chunks([1.0, 0.0], index, k=2)), 2)


class EmbedTextsTest(unittest.TestCase):
    def test_embed_texts_batches_and_keeps_order(self):
        texts = [f"repair {'tax ' * i}" for i in range(25)]
        client = FakeEmbedClient()
        with mock.patch.object(notes, "BATCH_SIZE", 10):
            vectors = notes.embed_texts(texts, client, "RETRIEVAL_DOCUMENT")
        self.assertEqual([len(c["contents"]) for c in client.calls], [10, 10, 5])
        self.assertEqual([t for c in client.calls for t in c["contents"]], texts)
        self.assertEqual(len(vectors), 25)
        self.assertEqual({len(v) for v in vectors}, {notes.EMBED_DIMENSIONS})
        for text, vector in zip(texts, vectors):
            expected = fake_vector(text)
            length = math.sqrt(sum(x * x for x in expected))
            for got, want in zip(vector, expected):
                self.assertAlmostEqual(got, want / length)  # in order, and scaled to length 1

    def test_document_and_query_task_types_are_sent(self):
        client = FakeEmbedClient()
        notes.embed_texts(["a note"], client, "RETRIEVAL_DOCUMENT")
        notes.embed_texts(["a question"], client, "RETRIEVAL_QUERY")
        self.assertEqual([c["config"]["task_type"] for c in client.calls],
                         ["RETRIEVAL_DOCUMENT", "RETRIEVAL_QUERY"])
        for call in client.calls:
            self.assertEqual(call["model"], "gemini-embedding-001")
            self.assertEqual(call["config"]["output_dimensionality"], 768)
        self.assertEqual((notes.EMBED_MODEL, notes.EMBED_DIMENSIONS, notes.BATCH_SIZE),
                         ("gemini-embedding-001", 768, 100))

    def test_wrong_number_of_vectors_back_is_an_error(self):
        client = FakeEmbedClient()
        client.embed_content = lambda **kwargs: SimpleNamespace(
            embeddings=[SimpleNamespace(values=[1.0, 0.0])])
        with self.assertRaises(notes.NotesError):
            notes.embed_texts(["one", "two"], client, "RETRIEVAL_DOCUMENT")


class IndexTest(unittest.TestCase):
    def test_build_save_load_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "dues.md", "The association dues are $240.")
            write(folder, "calls.md", "Text message the painter, don't call.")
            index = notes.build_index(folder, FakeEmbedClient())
            path = os.path.join(folder, "notes-index.json")
            notes.save_index(index, path)
            loaded = notes.load_index(path)
        self.assertEqual(loaded, index)
        self.assertEqual(loaded["model"], notes.EMBED_MODEL)
        self.assertEqual(loaded["dimensions"], notes.EMBED_DIMENSIONS)
        self.assertEqual(set(loaded["fingerprints"]), {"dues.md", "calls.md"})
        self.assertEqual([(c["source"], c["number"]) for c in loaded["chunks"]],
                         [("calls.md", 1), ("dues.md", 1)])
        self.assertEqual(set(loaded["chunks"][0]), {"source", "number", "text", "vector"})

    def test_build_index_embeds_documents_once_each(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "a.md", "One.")
            write(folder, "b.md", "Two.")
            client = FakeEmbedClient()
            notes.build_index(folder, client)
        self.assertEqual([c["config"]["task_type"] for c in client.calls], ["RETRIEVAL_DOCUMENT"])
        self.assertEqual(client.calls[0]["contents"], ["One.", "Two."])

    def test_index_is_stale_after_add_edit_or_delete(self):
        stale = ("Your notes changed since the index was built. "
                 "Run: python3 -m dealscreener.notes index")
        for change in ("add", "edit", "delete"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as folder:
                write(folder, "a.md", "First note.")
                write(folder, "b.md", "Second note.")
                index = notes.build_index(folder, FakeEmbedClient())
                notes.check_fresh(index, folder)  # unchanged: no error
                if change == "add":
                    write(folder, "c.md", "A new note.")
                elif change == "edit":
                    write(folder, "a.md", "First note, edited.")
                else:
                    os.remove(os.path.join(folder, "b.md"))
                with self.assertRaises(notes.NotesError) as caught:
                    notes.check_fresh(index, folder)
                self.assertEqual(str(caught.exception), stale)

    def test_index_from_another_model_size_or_shape_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "a.md", "First note.")
            index = notes.build_index(folder, FakeEmbedClient())
            broken = [dict(index, model="another-model"), dict(index, dimensions=3072),
                      {key: value for key, value in index.items() if key != "fingerprints"},
                      {"chunks": index["chunks"]}]
            for bad in broken:
                with self.subTest(keys=sorted(bad)), self.assertRaises(notes.NotesError) as caught:
                    notes.check_fresh(bad, folder)
                self.assertTrue(str(caught.exception).endswith("Run: python3 -m dealscreener.notes index"))

    def test_missing_index_says_run_index(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(notes.NotesError) as caught:
                notes.load_index(os.path.join(folder, "notes-index.json"))
        self.assertEqual(str(caught.exception), "No index yet. Run: python3 -m dealscreener.notes index")

    def test_index_that_cant_be_saved_says_so(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "no-such-folder", "notes-index.json")
            with self.assertRaises(notes.NotesError) as caught:
                notes.save_index({"chunks": []}, path)
        self.assertEqual(str(caught.exception), f"Couldn't save the index file {path}.")

    def test_unreadable_index_says_run_index(self):
        with tempfile.TemporaryDirectory() as folder:
            path = write(folder, "notes-index.json", "{not json")
            with self.assertRaises(notes.NotesError) as caught:
                notes.load_index(path)
        self.assertIn("Run: python3 -m dealscreener.notes index", str(caught.exception))


MATCHES = [(0.91, notes.Chunk("riverside-association-dues.md", 1, "Dues are $240 a month.")),
           (0.40, notes.Chunk("listing-b-write-up.md", 2, "The deal passed."))]


class AnswerTest(unittest.TestCase):
    def test_answer_prompt_pins_grounding_rules(self):
        for sentence in ("Answer only from the notes below.",
                         "After your answer, list the file names you used, after the word Sources:.",
                         "If the notes do not answer the question, reply exactly: My notes don't say."):
            self.assertIn(sentence, notes.SYSTEM_PROMPT)
        client = FakeClient(answer_reply())
        notes.answer("What are the dues?", MATCHES, client)
        self.assertEqual(len(client.calls), 1)
        call = client.calls[0]
        self.assertEqual(call["model"], extract.MODEL)
        self.assertEqual(call["max_tokens"], 1000)
        self.assertEqual(call["system"], notes.SYSTEM_PROMPT)
        content = call["messages"][0]["content"]
        self.assertEqual(call["messages"][0]["role"], "user")
        first = content.index("[riverside-association-dues.md part 1]")
        second = content.index("[listing-b-write-up.md part 2]")
        self.assertLess(first, content.index("Dues are $240 a month."))
        self.assertLess(first, second)
        self.assertLess(second, content.index("What are the dues?"))
        for name in ("temperature", "tools", "output_config"):
            self.assertNotIn(name, call)

    def test_answer_reads_text_blocks_after_thinking(self):
        result = notes.answer("Q?", MATCHES, FakeClient(answer_reply(thinking=True)))
        self.assertEqual(result.text, "Dues are $240 a month.\n\nSources: riverside-association-dues.md")
        self.assertEqual((result.input_tokens, result.output_tokens), (700, 40))
        plain = notes.answer("Q?", MATCHES, FakeClient(answer_reply("My notes don't say.", thinking=False)))
        self.assertEqual(plain.text, "My notes don't say.")

    def test_answer_cut_off_and_refusal_are_errors(self):
        for stop_reason, sentence in (("max_tokens", "The answer was cut off before it finished."),
                                      ("refusal", "The model declined to answer.")):
            with self.subTest(stop_reason=stop_reason):
                with self.assertRaises(notes.NotesError) as caught:
                    notes.answer("Q?", MATCHES, FakeClient(answer_reply(stop_reason=stop_reason)))
                self.assertEqual(str(caught.exception), sentence)


class KeysAndErrorsTest(unittest.TestCase):
    def test_no_google_key_says_how_to_add_one(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(notes.NotesError) as caught:
                notes.make_embed_client()
        self.assertEqual(str(caught.exception),
                         "No Google API key found. Put GEMINI_API_KEY in a .env file (see the README).")

    def test_missing_google_package_says_how_to_install_it(self):
        # None in sys.modules makes "from google import genai" fail, as if it weren't installed.
        with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "test-key-not-real"}), \
                mock.patch.dict("sys.modules", {"google": None, "google.genai": None}):
            with self.assertRaises(notes.NotesError) as caught:
                notes.make_embed_client()
        self.assertEqual(str(caught.exception),
                         "The google-genai package isn't installed (pip install -r requirements.txt).")

    def test_google_errors_get_fixed_sentences_without_the_key(self):
        key = "AIzaSy-secret-key-in-the-error"
        key_sentence = ("The Google API key was not accepted, or isn't allowed to do that. "
                        "Check GEMINI_API_KEY in your .env file.")
        cases = [
            (FakeGoogleError(400, f"bad request for {key}"), "Google couldn't read the request."),
            (FakeGoogleError(400, f"API key not valid. Please pass a valid API key. {key}"), key_sentence),
            (FakeGoogleError(401, key), key_sentence),
            (FakeGoogleError(403, key), key_sentence),
            (FakeGoogleError(404, key), "The embedding model name wasn't found."),
            (FakeGoogleError(429, key), "Too many requests for the free tier right now. Wait a minute and try again."),
            (FakeGoogleError(500, key), "Google's service is busy or having a problem. Try again later."),
            (FakeGoogleError(503, key), "Google's service is busy or having a problem. Try again later."),
            (FakeGoogleError(418, key), "The call to Google failed."),
            (OSError(f"connection failed {key}"), "Couldn't reach Google. Check your internet connection."),
            (ConnectError(f"no route {key}"), "Couldn't reach Google. Check your internet connection."),
            (ReadTimeout(f"slow {key}"), "Couldn't reach Google. Check your internet connection."),
            (FakeGoogleError("UNAVAILABLE", key), "The call to Google failed."),
            (FakeGoogleError(7, key), "The call to Google failed."),
            (ValueError(key), "The call to Google failed."),
        ]
        for error, sentence in cases:
            with self.subTest(error=repr(error)):
                message = notes.describe_google_error(error)
                self.assertEqual(message, sentence)
                self.assertNotIn(key, message)


class FakeConsole:
    def __init__(self):
        self.lines = []

    def print(self, text=""):
        self.lines.append(str(text))

    def output(self):
        return "\n".join(self.lines)


def no_input(prompt=""):
    raise AssertionError("the notes command should never ask for typing")


class MainTest(unittest.TestCase):
    """The command, run in a temporary folder with the course notes copied in."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.notes_dir = os.path.join(self.folder.name, "notes")
        os.mkdir(self.notes_dir)
        for path in sorted(NOTES_FOLDER.glob("*.md")):
            write(self.notes_dir, path.name, path.read_text(encoding="utf-8"))
        self.index_file = os.path.join(self.folder.name, "notes-index.json")
        for patch in (mock.patch.object(notes, "NOTES_DIR", self.notes_dir),
                      mock.patch.object(notes, "INDEX_FILE", self.index_file),
                      mock.patch.object(notes.extract, "load_env_file")):
            patch.start()
            self.addCleanup(patch.stop)
        self.embed_client = FakeEmbedClient()

    def run_main(self, argv, claude=None, embed_factory=None, claude_factory=None):
        console = FakeConsole()
        code = notes.main(argv, input_fn=no_input, print_fn=console.print,
                          embed_factory=embed_factory or (lambda: self.embed_client),
                          claude_factory=claude_factory or (lambda: claude))
        return code, console.output()

    def test_main_index_prints_count(self):
        write(self.notes_dir, "scan.txt", b"\xff\xfe binary")
        code, output = self.run_main(["index"])
        self.assertEqual(code, 0)
        self.assertIn("Skipped scan.txt: not plain text.", output)
        self.assertTrue(output.endswith("Indexed 9 chunks from 8 notes."), output)
        with open(self.index_file, encoding="utf-8") as handle:
            self.assertEqual(len(json.load(handle)["chunks"]), 9)

    def test_main_ask_prints_matches_answer_and_cost(self):
        self.run_main(["index"])
        claude = FakeClient(answer_reply(input_tokens=700, output_tokens=40))
        code, output = self.run_main(["ask", "What are the HOA fees like in Riverside?"], claude=claude)
        self.assertEqual(code, 0)
        lines = output.splitlines()
        start = lines.index("Notes that match best:")
        self.assertRegex(lines[start + 1], r"^  riverside-association-dues\.md part 1 \(similarity 0\.\d\d\)$")
        self.assertEqual(len([line for line in lines if " (similarity " in line]), notes.TOP_K)
        self.assertIn("Sources: riverside-association-dues.md", output)
        self.assertTrue(output.endswith(
            "Used 700 input and 40 output tokens on Claude, about $0.00009."), output)
        self.assertEqual(self.embed_client.calls[-1]["config"]["task_type"], "RETRIEVAL_QUERY")
        self.assertIn("[riverside-association-dues.md part 1]", claude.calls[0]["messages"][0]["content"])

    def test_main_ask_without_claude_key_still_prints_matches(self):
        self.run_main(["index"])

        def no_key():
            raise extract.ExtractionError(
                "No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README).")

        failures = [(no_key, "No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README)."),
                    (lambda: FakeClient(error=FakeAPIError(401, "sk-ant-secret")),
                     "The API key was not accepted. Check the key in your .env file."),
                    (lambda: FakeClient(answer_reply(stop_reason="refusal")), "The model declined to answer.")]
        for factory, sentence in failures:
            with self.subTest(sentence=sentence):
                code, output = self.run_main(["ask", "What are the HOA fees like in Riverside?"],
                                             claude_factory=factory)
                self.assertEqual(code, 0)
                self.assertIn("  riverside-association-dues.md part 1 (similarity", output)
                self.assertIn(sentence + " Here are the notes that match best instead.", output)
                self.assertIn("$240 a month", output)  # the matching note's own text
                self.assertNotIn("sk-ant-secret", output)
                self.assertNotIn("Used ", output)

    def test_main_ask_with_stale_index_refuses(self):
        self.run_main(["index"])
        write(self.notes_dir, "new-note.md", "A note added after the index was built.")
        calls_before = len(self.embed_client.calls)
        code, output = self.run_main(["ask", "Anything?"], claude=FakeClient(answer_reply()))
        self.assertEqual(code, 1)
        self.assertEqual(output, "Your notes changed since the index was built. "
                                 "Run: python3 -m dealscreener.notes index")
        self.assertEqual(len(self.embed_client.calls), calls_before)  # no call was made

    def test_main_ask_with_no_index_and_google_failures_return_1(self):
        code, output = self.run_main(["ask", "Anything?"])
        self.assertEqual((code, output), (1, "No index yet. Run: python3 -m dealscreener.notes index"))

        def no_google_key():
            raise notes.NotesError("No Google API key found. Put GEMINI_API_KEY in a .env file (see the README).")

        code, output = self.run_main(["index"], embed_factory=no_google_key)
        self.assertEqual(code, 1)
        self.assertIn("No Google API key found.", output)
        failing = FakeEmbedClient(error=FakeGoogleError(429, "AIza-secret"))
        code, output = self.run_main(["index"], embed_factory=lambda: failing)
        self.assertEqual(code, 1)
        self.assertEqual(output, "Too many requests for the free tier right now. Wait a minute and try again.")
        self.assertFalse(os.path.exists(self.index_file))

    def test_a_mistake_in_the_program_is_not_blamed_on_google(self):
        broken = FakeEmbedClient(error=ValueError("a bug in our own code"))
        with self.assertRaises(ValueError):
            self.run_main(["index"], embed_factory=lambda: broken)
        offline = FakeEmbedClient(error=ConnectError("no network"))
        code, output = self.run_main(["index"], embed_factory=lambda: offline)
        self.assertEqual((code, output), (1, "Couldn't reach Google. Check your internet connection."))

    def test_a_mistake_in_the_program_while_asking_is_not_blamed_on_google(self):
        self.run_main(["index"])
        broken = FakeEmbedClient(error=ValueError("a bug in our own code"))
        with self.assertRaises(ValueError):
            self.run_main(["ask", "dues?"], embed_factory=lambda: broken)

    def test_a_file_error_is_not_called_a_connection_error(self):
        self.assertFalse(notes.is_connection_error(PermissionError(13, "Permission denied", "notes/a.md")))
        self.assertFalse(notes.is_connection_error(FileNotFoundError(2, "No such file", "notes-index.json")))

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root can read any file")
    def test_an_unreadable_note_says_which_file(self):
        path = os.path.join(self.notes_dir, "locked.md")
        pathlib.Path(path).write_text("secret dues", encoding="utf-8")
        os.chmod(path, 0)
        self.addCleanup(os.chmod, path, 0o644)
        with self.assertRaises(notes.NotesError) as caught:
            notes.load_notes(self.notes_dir)
        self.assertEqual(str(caught.exception), "Couldn't read locked.md.")

    def test_main_usage_errors_return_2(self):
        for argv in ([], ["ask"], ["ask", "   "], ["search", "dues"]):
            with self.subTest(argv=argv):
                code, output = self.run_main(argv)
                self.assertEqual(code, 2)
                self.assertIn("python3 -m dealscreener.notes index", output)
                self.assertIn('python3 -m dealscreener.notes ask "your question"', output)
        self.assertEqual(self.embed_client.calls, [])


if __name__ == "__main__":
    unittest.main()
