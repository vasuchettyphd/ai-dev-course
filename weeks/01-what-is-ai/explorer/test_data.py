# weeks/01-what-is-ai/explorer/test_data.py
"""Checks data.json is well formed. Stdlib only: python3 test_data.py"""
import json, math, pathlib, unittest

HERE = pathlib.Path(__file__).parent
DATA = json.loads((HERE / "data.json").read_text(encoding="utf-8"))


class DataShape(unittest.TestCase):
    def test_header(self):
        self.assertEqual(DATA["model"], "Qwen/Qwen2.5-0.5B")
        self.assertRegex(DATA["revision"], r"^[0-9a-f]{40}$")

    def test_next_word(self):
        self.assertGreaterEqual(len(DATA["next_word"]), 6)
        for item in DATA["next_word"]:
            c = item["candidates"]
            self.assertEqual(len(c), 50)
            logits = [x["logit"] for x in c]
            self.assertEqual(logits, sorted(logits, reverse=True))
            self.assertLessEqual(sum(x["prob"] for x in c), 1.0 + 1e-6)
            self.assertTrue(all(0 < x["prob"] < 1 for x in c))

    def test_tokens(self):
        self.assertGreaterEqual(len(DATA["tokens"]), 8)
        for item in DATA["tokens"]:
            self.assertEqual("".join(item["pieces"]), item["text"])
            self.assertEqual(item["count"], len(item["pieces"]))

    def test_attention(self):
        self.assertEqual(len(DATA["attention"]), 2)
        for item in DATA["attention"]:
            n = len(item["tokens"])
            self.assertGreater(len(item["layers"]), 1)
            for layer in item["layers"]:
                self.assertEqual(len(layer), n)
                for i, row in enumerate(layer):
                    self.assertEqual(len(row), n)
                    self.assertTrue(math.isclose(sum(row), 1.0, abs_tol=0.01))
                    self.assertTrue(all(v == 0 for v in row[i + 1:]))  # causal: no looking ahead


if __name__ == "__main__":
    unittest.main()
