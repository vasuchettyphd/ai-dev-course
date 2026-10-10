# weeks/01-what-is-ai/explorer/test_data.py
"""Checks data.json is well formed. Stdlib only: python3 test_data.py"""
import datetime, json, math, pathlib, unittest

HERE = pathlib.Path(__file__).parent
RAW = (HERE / "data.json").read_text(encoding="utf-8")
DATA = json.loads(RAW)
CHOICE = json.loads((HERE / "choose_example_results.json").read_text(encoding="utf-8"))

PROMPTS = [
    "The best way to start a small business is to",
    "Our quarterly sales were up, so the board decided to",
    "The customer was angry because the package",
    "The capital of France is",
    "Two plus two equals",
    "Once upon a time, there was a",
]
TOKEN_TEXTS = [
    "The best way to start a small business is to",
    "Revenue grew 12.5% to $3,450,000 in Q3.",
    "Contact me at jane.doe@example.com",
    "strawberry",
    "Strawberry STRAWBERRY strawberries",
    "El cliente quiere un reembolso.",
    "antidisestablishmentarianism",
    "I can't believe it's not butter!",
]
TROPHY = [
    "The trophy didn't fit in the suitcase because it was too big.",
    "The trophy didn't fit in the suitcase because it was too small.",
]


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
        self.assertEqual(len(DATA["attention"]), 3)
        for item in DATA["attention"]:
            n = len(item["tokens"])
            self.assertGreater(len(item["layers"]), 1)
            for layer in item["layers"]:
                self.assertEqual(len(layer), n)
                for i, row in enumerate(layer):
                    self.assertEqual(len(row), n)
                    self.assertTrue(math.isclose(sum(row), 1.0, abs_tol=0.01))
                    self.assertTrue(all(v == 0 for v in row[i + 1:]))  # causal: no looking ahead

    def test_exact_inputs(self):
        self.assertEqual([x["prompt"] for x in DATA["next_word"]], PROMPTS)
        self.assertEqual([x["text"] for x in DATA["tokens"]], TOKEN_TEXTS)
        sents = [x["sentence"] for x in DATA["attention"]]
        self.assertEqual(sents[:2], TROPHY)
        self.assertEqual(len(sents), 3)
        self.assertEqual(sents[2], CHOICE["winner"]["sentence"])

    def test_next_word_extra(self):
        sums = []
        for item in DATA["next_word"]:
            c = item["candidates"]
            probs = [x["prob"] for x in c]
            self.assertEqual(probs, sorted(probs, reverse=True))
            self.assertEqual(len({x["token"] for x in c}), 50)
            sums.append(sum(probs))
        self.assertTrue(any(v < 0.999 for v in sums))

    def test_generated_is_iso_date(self):
        datetime.date.fromisoformat(DATA["generated"])

    def test_attention_extra(self):
        for item in DATA["attention"]:
            self.assertEqual("".join(item["tokens"]), item["sentence"])
            self.assertEqual(len(item["layers"]), 24)
            f = item["focus"]
            n = len(item["tokens"])
            self.assertTrue(0 <= f["to"] < f["from"] < n)
            self.assertTrue(0 <= f["layer"] < len(item["layers"]))
            self.assertTrue(f["label"].strip())
        big, small = DATA["attention"][0], DATA["attention"][1]
        self.assertEqual(big["tokens"][big["focus"]["from"]], " big")
        self.assertEqual(small["tokens"][small["focus"]["from"]], " small")
        for a in (big, small):
            self.assertEqual(a["tokens"][a["focus"]["to"]], " trophy")
        win = CHOICE["winner"]
        ex = DATA["attention"][2]
        self.assertEqual(ex["focus"]["from"], win["source_index"])
        self.assertEqual(ex["focus"]["to"], win["target_index"])
        self.assertEqual(ex["focus"]["layer"], win["layer"])
        # the two trophy sentences share every token before the last word, so rows 0..11 match
        for lb, ls in zip(big["layers"], small["layers"]):
            self.assertEqual(lb[:12], ls[:12])

    def test_ascii_only(self):
        self.assertTrue(RAW.isascii())


if __name__ == "__main__":
    unittest.main()
