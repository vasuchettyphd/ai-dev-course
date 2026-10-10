# weeks/01-what-is-ai/explorer/test_page.py
"""python3 test_page.py - the page embeds exactly data.json and makes no network requests."""
import json, pathlib, re, unittest

HERE = pathlib.Path(__file__).parent
HTML = (HERE / "index.html").read_text(encoding="utf-8")


class Page(unittest.TestCase):
    def test_embedded_data_matches(self):
        m = re.search(r'<script id="data" type="application/json">(.*?)</script>', HTML, re.S)
        self.assertIsNotNone(m)
        self.assertEqual(json.loads(m.group(1)), json.loads((HERE / "data.json").read_text(encoding="utf-8")))

    def test_embedded_data_is_ascii(self):
        m = re.search(r'<script id="data" type="application/json">(.*?)</script>', HTML, re.S)
        self.assertTrue(m.group(1).isascii())

    def test_no_network(self):
        page = re.sub(r'<script id="data" type="application/json">.*?</script>', "", HTML, flags=re.S)
        for pattern in (r"https?://", r"\bfetch\(", r"XMLHttpRequest", r"<link[^>]+href=", r"<script[^>]+src="):
            self.assertIsNone(re.search(pattern, page), pattern)

    def test_no_literal_em_dash(self):
        self.assertNotIn(chr(0x2014), HTML)

    def test_has_three_activities(self):
        for anchor in ('id="next-word"', 'id="tokens"', 'id="attention"'):
            self.assertIn(anchor, HTML)

    def test_mobile_viewport(self):
        self.assertIn('name="viewport"', HTML)
        self.assertRegex(HTML, r"@media\s*\(max-width:\s*600px\)")

    def test_attention_wording(self):
        self.assertIn("Include the first word", HTML)
        self.assertIn("it is not a readable explanation", HTML)

    def test_attention_sentences_embedded(self):
        data = json.loads((HERE / "data.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["attention"]), 3)
        self.assertIn("Paris is in France and Berlin is in", [a["sentence"] for a in data["attention"]])


if __name__ == "__main__":
    unittest.main()
