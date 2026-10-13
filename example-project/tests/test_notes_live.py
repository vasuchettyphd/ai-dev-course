"""Real calls to Google and Claude, run only on request: they need both keys. Google's free
tier costs nothing; the one Claude call costs a tiny amount of credit.

From the example-project folder, with both keys in your environment (see the README):
    RUN_LIVE_TESTS=1 python -m unittest tests.test_notes_live -v
Without RUN_LIVE_TESTS=1 and both keys, this test is skipped, so python3 -m unittest stays offline.
"""
import os
import pathlib
import tempfile
import unittest

from dealscreener import extract, notes

NOTES_FOLDER = str(pathlib.Path(__file__).parent.parent / "notes")


@unittest.skipUnless(os.environ.get("RUN_LIVE_TESTS") == "1" and os.environ.get("GEMINI_API_KEY")
                     and os.environ.get("ANTHROPIC_API_KEY"),
                     "live test: set RUN_LIVE_TESTS=1 and both keys")
class LiveNotesTest(unittest.TestCase):
    def test_riverside_dues_question_finds_the_riverside_note(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "notes-index.json")
            notes.save_index(notes.build_index(NOTES_FOLDER, notes.make_embed_client()), path)
            index = notes.load_index(path)
        self.assertEqual(index["dimensions"], notes.EMBED_DIMENSIONS)
        question = "What are the association dues like in Riverside?"
        vector = notes.embed_texts([question], notes.make_embed_client(), "RETRIEVAL_QUERY")[0]
        matches = notes.top_chunks(vector, index)
        self.assertIn("riverside-association-dues.md", [chunk.source for _, chunk in matches])
        result = notes.answer(question, matches, extract.make_client())
        self.assertNotEqual(result.text.strip(), "My notes don't say.")
        print("\nmatches: " + ", ".join(f"{c.source} part {c.number} ({s:.2f})" for s, c in matches))
        print(f"live answer: {result.input_tokens} input and {result.output_tokens} output tokens, "
              f"about ${extract.cost_usd(result.input_tokens, result.output_tokens):.5f}")


if __name__ == "__main__":
    unittest.main()
