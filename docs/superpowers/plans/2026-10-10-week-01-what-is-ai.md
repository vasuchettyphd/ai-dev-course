# Week 1 (What AI is) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 1 of the course. It has three parts: a self-contained browser "explorer" page with real model numbers (next-word guessing, tokens, attention), the week's README, slides and assignment, and private instructor notes. The explorer is served by GitHub Pages.

**Architecture:**
- **Data:** a one-off Python script (`compute.py`) runs a small open model locally. It writes `data.json` containing next-word logits, tokenizations and attention weights.
- **Explorer page:** `index.html` is a single self-contained page (inline CSS and JS, no external requests) with `data.json`'s content embedded. It works from GitHub Pages and from a local `file://` open.
- **Embed check:** a stdlib-only Python test checks that the data is well formed and that the embedded copy matches `data.json`.
- **Text:** prose content follows the course templates and passes `scripts/check_course.py`.

**Tech Stack:**
- Python 3 with `torch` and `transformers`. These are only used to compute the data, in a throwaway venv outside the repo.
- Model: `Qwen/Qwen2.5-0.5B` (Apache 2.0).
- Plain HTML, CSS and JS.
- Marp, run through `npm run slides` in Docker.
- GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md` (week 1 row). The week 1 design was approved in conversation on 2026-10-10. Its decisions are copied into Global Constraints below.

## Global Constraints

- Audience: business and non-CS university students, in week 1, with nothing installed. Everything students do this week happens in a web browser. No terminal, no code.
- Teaching approach: hands-on intuition. *Attention Is All You Need* (Vaswani et al., 2017, arXiv 1706.03762) is explained with pictures and plain words, never read line by line, and never shown as equations.
- Every number shown on the explorer page comes from `weeks/01-what-is-ai/explorer/data.json`, produced by `weeks/01-what-is-ai/explorer/compute.py`. Nothing is hand-typed or invented.
- Model: `Qwen/Qwen2.5-0.5B`, revision pinned to the commit hash `compute.py` records in `data.json`.
- The explorer page makes no network requests: no CDNs, fonts or analytics. It must work when opened as a local file.
- No em dashes (U+2014) in any file. Plain language. Every claim about the paper is checked against the paper.
- Week 1 assignment rubric: a table under `## Rubric`, points in the last column, totalling 10.
- The large dependencies (torch, model weights) go in a venv and cache outside the repo, under the session scratchpad. Only `compute.py`, `data.json`, `index.html` and tests are committed.
- Instructor-only material (discussion answers, grading guidance) goes only in the private repo `~/claude/ai-dev-course-instructor`.
- Branch `week-01-what-is-ai` in `~/claude/ai-dev-course`. Never commit to `main`. The user merges PRs in the GitHub UI.

## Review Focus

1. **Temperature math looks wrong.** A student drags the temperature slider, and the top word's probability should rise as temperature falls and flatten as it rises. Task 2 adds a test of the page's softmax function (run with Node) for T=0.5 vs T=1 vs T=2 on fixed logits.
2. **Probabilities shown don't add up.** Only the top 10 words are listed, so the page must say "other words" for the remainder, and the shown numbers must sum to at most 100%. Task 1's data test checks that the top-k probabilities sum to at most 1. Task 2's page shows an "everything else" row.
3. **Attention picture over-claims.** "The model knows *it* means the trophy" isn't something attention weights prove. The README and slides must say attention shows where the model looked, not proof of understanding. Task 3's review checklist includes this exact wording check.
4. **Page breaks on a phone or as a local file.** Students open it on phones and laptops. Task 2 tests `file://` loading (no fetch of data.json, data embedded) and uses a single-column layout under 600px.
5. **Token examples misrepresent tokenization.** Token boundaries shown must be the model's real ones, including leading-space markers. Task 1 stores the token strings exactly as the tokenizer decodes each id, and Task 2 renders spaces visibly (as `·`).

---

### Task 1: Compute the data

**Files:**
- Create: `weeks/01-what-is-ai/explorer/compute.py`
- Create: `weeks/01-what-is-ai/explorer/data.json` (generated)
- Create: `weeks/01-what-is-ai/explorer/test_data.py`

**Interfaces:**
- Produces: `data.json` with this exact top-level shape, which Tasks 2-3 consume:

```json
{
  "model": "Qwen/Qwen2.5-0.5B",
  "revision": "<commit hash>",
  "generated": "<ISO date>",
  "next_word": [
    {"prompt": "...", "candidates": [{"token": " grow", "logit": 17.2, "prob": 0.081}]}
  ],
  "tokens": [
    {"text": "...", "pieces": [" The", " best"], "count": 2}
  ],
  "attention": [
    {"sentence": "...", "tokens": ["The", " trophy"], "layers": [[[0.1, 0.9], [0.4, 0.6]]]}
  ]
}
```

- `next_word[].candidates`: the top 50 by logit, sorted descending. `prob` is softmax at temperature 1 over the **full vocabulary**, not just the top 50.
- `attention[].layers[L][i][j]`: the attention from token i to token j in layer L, averaged over that layer's heads, rounded to 4 decimals. Every layer is included.

- [ ] **Step 1: Make the throwaway environment (outside the repo)**

```bash
SP=/tmp/claude-1000/-home-vasu/15717341-d1c6-466d-9e1a-15ef7796f57e/scratchpad
python3 -m venv $SP/w1venv
$SP/w1venv/bin/pip install --quiet "torch==2.5.1" --index-url https://download.pytorch.org/whl/cpu
$SP/w1venv/bin/pip install --quiet "transformers==4.46.3"
```
Expected: both install without error. If the pinned versions are unavailable for this Python (3.14), use the nearest available CPU builds and record the versions you used in the report and in `compute.py`'s docstring.

- [ ] **Step 2: Write the data test first**

```python
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
```

Run: `cd weeks/01-what-is-ai/explorer && python3 test_data.py`
Expected: an ERROR because `data.json` does not exist (FileNotFoundError at import).

- [ ] **Step 3: Write compute.py**

Inputs to use verbatim:
- `PROMPTS` (next word):
  - "The best way to start a small business is to"
  - "Our quarterly sales were up, so the board decided to"
  - "The customer was angry because the package"
  - "The capital of France is"
  - "Two plus two equals"
  - "Once upon a time, there was a"
- `TOKEN_TEXTS`:
  - "The best way to start a small business is to"
  - "Revenue grew 12.5% to $3,450,000 in Q3."
  - "Contact me at jane.doe@example.com"
  - "strawberry"
  - "Strawberry STRAWBERRY strawberries"
  - "El cliente quiere un reembolso."
  - "antidisestablishmentarianism"
  - "I can't believe it's not butter!"
- `ATTENTION_SENTENCES`:
  - "The trophy didn't fit in the suitcase because it was too big."
  - "The trophy didn't fit in the suitcase because it was too small."

Required behaviour:
- Load the tokenizer and the model with `attn_implementation="eager"` (needed to return attention weights) and `torch_dtype=torch.float32`, in eval mode under `torch.no_grad()`. Record `model.config._commit_hash` (or the resolved snapshot hash) as `revision`.
- **Next word:** take the logits at the last position, `probs = softmax(logits)` over the full vocabulary, then `topk(50)`. Each candidate's `token` is `tokenizer.decode([id])`. Round logits to 3 decimals and probs to 5.
- **Tokens:** use `ids = tokenizer(text, add_special_tokens=False).input_ids`. Pieces are `[tokenizer.decode([i]) for i in ids]`. Assert `"".join(pieces) == text`. If the assert fails for a text, replace that text with a nearby sentence and record the change in the report.
- **Attention:** call `model(**enc, output_attentions=True)`. For each layer, take the mean over heads of `attentions[L][0]`. Tokens are the decoded pieces. Round values to 4 decimals.
- Write `data.json` with `ensure_ascii=True, indent=1`. Real model tokens can include characters such as the em dash; ASCII escapes (`\u2014`) keep the literal character out of every file while the page still shows the real token. Set `generated` to today's date.
- Add a module docstring stating how to re-run it, the exact package versions used, and that the output is committed so students never run it.

- [ ] **Step 4: Run it and the test**

```bash
HF_HOME=$SP/hf $SP/w1venv/bin/python weeks/01-what-is-ai/explorer/compute.py
cd weeks/01-what-is-ai/explorer && python3 test_data.py
```
Expected: `data.json` is written (under 1.5 MB) and the test prints `OK`. Report the top 5 candidates for each prompt, so the reviewers and the page author can see the real numbers.

- [ ] **Step 5: Commit**

```bash
git add weeks/01-what-is-ai/explorer/compute.py weeks/01-what-is-ai/explorer/data.json weeks/01-what-is-ai/explorer/test_data.py
git commit -m "Week 1: compute real next-word, token and attention data from Qwen2.5-0.5B"
```

### Task 2: The explorer page

**Files:**
- Create: `weeks/01-what-is-ai/explorer/index.template.html` (hand-written page with a `__DATA__` placeholder)
- Create: `weeks/01-what-is-ai/explorer/index.html` (built by build_page.py; never edit by hand)
- Create: `weeks/01-what-is-ai/explorer/build_page.py` (embeds data.json into index.html)
- Create: `weeks/01-what-is-ai/explorer/test_page.py`
- Create: `weeks/01-what-is-ai/explorer/test_softmax.mjs`
- Create: `.nojekyll` (repo root, so GitHub Pages serves files as they are)

**Interfaces:**
- Consumes: `data.json` (shape above).
- Produces: `index.html`. It contains `<script id="data" type="application/json">` with the exact JSON of data.json, and a global `softmax(logits, temperature)` function returning an array of probabilities. The function is exported for Node through `if (typeof module !== "undefined") module.exports = { softmax }`.

- [ ] **Step 1: Write the tests first**

```python
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

    def test_no_network(self):
        page = re.sub(r'<script id="data" type="application/json">.*?</script>', "", HTML, flags=re.S)
        for pattern in (r"https?://", r"\bfetch\(", r"XMLHttpRequest", r"<link[^>]+href=", r"<script[^>]+src="):
            self.assertIsNone(re.search(pattern, page), pattern)

    def test_no_literal_em_dash(self):
        self.assertNotIn("\u2014", HTML)

    def test_has_three_activities(self):
        for anchor in ('id="next-word"', 'id="tokens"', 'id="attention"'):
            self.assertIn(anchor, HTML)

    def test_mobile_viewport(self):
        self.assertIn('name="viewport"', HTML)
        self.assertRegex(HTML, r"@media\s*\(max-width:\s*600px\)")


if __name__ == "__main__":
    unittest.main()
```

```js
// weeks/01-what-is-ai/explorer/test_softmax.mjs  -  node test_softmax.mjs
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
const html = readFileSync(new URL("./index.html", import.meta.url), "utf8");
const src = html.match(/\/\/ BEGIN softmax([\s\S]*?)\/\/ END softmax/)[1];
const softmax = new Function(src + "; return softmax;")();
const logits = [3, 2, 1, 0];
const p1 = softmax(logits, 1), pCold = softmax(logits, 0.5), pHot = softmax(logits, 2);
const sum = a => a.reduce((x, y) => x + y, 0);
for (const p of [p1, pCold, pHot]) assert.ok(Math.abs(sum(p) - 1) < 1e-9);
assert.ok(pCold[0] > p1[0] && p1[0] > pHot[0], "lower temperature sharpens the top choice");
assert.ok(Math.abs(p1[0] - Math.exp(3) / (Math.exp(3) + Math.exp(2) + Math.exp(1) + 1)) < 1e-12);
console.log("softmax OK");
```

Run both. Expected: both fail because `index.html` does not exist.

- [ ] **Step 2: Build the page**

Write `index.template.html` by hand, with the placeholder line `<script id="data" type="application/json">__DATA__</script>`. Then write `build_page.py`, which replaces `__DATA__` with the compact JSON of data.json (`separators=(",",":")`, `ensure_ascii=True`) and escapes `</` as `<\/` so the data cannot close the tag. It writes the result to `index.html`.

Page requirements:
- **Title and intro:** "What AI is: an explorer". One short paragraph: "Everything on this page comes from a real AI model (Qwen2.5-0.5B, a small open model). Nothing here is made up."
- **Section `#next-word`:**
  - A prompt picker with the 6 prompts and a text box: "Type the word you think comes next".
  - A **Reveal** button shows the top 10 candidates as horizontal bars with percentages, plus an "everything else" row of 100% minus the shown total, computed at the current temperature.
  - The student's guess is highlighted if it is among the 50 candidates. Otherwise the page shows "Not in the model's top 50".
  - The temperature slider runs from 0.2 to 2.0 in steps of 0.1, defaulting to 1.0. It recomputes from the stored logits with the `softmax` function, normalising over the 50 stored candidates. A one-line note says the page re-spreads probability over the top 50 words only, so the numbers are close to the model's but not exact at other temperatures.
  - Spaces in tokens are shown as `·`.
- **Section `#tokens`:**
  - Each text is shown as coloured chips, one per piece, with spaces as `·`, plus "N tokens".
  - Caption: "Models read tokens, not letters or words. That's why counting the r's in strawberry can trip them up."
- **Section `#attention`:**
  - A toggle switches between the two sentences.
  - Clicking a token shades every earlier token by its attention weight, using the selected layer. A layer slider runs from 1 to N and defaults to the layer where "it" has the highest weight on "trophy" in the "big" sentence; `build_page.py` computes this and writes it into the page as a constant.
  - Caption: "Attention shows where the model looked when reading each word. It is not proof that the model understands the sentence."
- **Layout and accessibility:** semantic HTML, keyboard-usable controls, and colours with contrast of at least 4.5:1. Single column under 600px, readable without horizontal scrolling. No external fonts.
- **softmax:** wrap the function in `// BEGIN softmax` and `// END softmax` comments. Subtract the maximum before exponentiating so large logits don't overflow.

- [ ] **Step 3: Build and run the tests**

```bash
cd weeks/01-what-is-ai/explorer && python3 build_page.py && python3 test_page.py && node test_softmax.mjs && python3 test_data.py
cd ../../.. && touch .nojekyll && python3 scripts/check_course.py
```
Expected: all tests `OK`, `softmax OK`, and the checker prints `OK`. The week README still has its stub marker until Task 3, so the checker does not yet require slides or an assignment.

- [ ] **Step 4: Look at it**

Open `index.html` in a headless browser if one is available. If not, render it with the Marp Docker image's Chromium:

```bash
docker run --rm --entrypoint "" -v "$PWD":/w -w /w marpteam/marp-cli:v4.1.2 sh -c 'chromium-browser --headless --no-sandbox --screenshot=/w/shot.png --window-size=1200,2400 file:///w/weeks/01-what-is-ai/explorer/index.html'
```
If that image has no chromium binary at that name, find it with `ls /usr/bin | grep -i chrom` inside the image. Take a 1200px screenshot and a 390px one. Read both images and fix anything broken. Do not commit the screenshots.

- [ ] **Step 5: Commit**

```bash
git add .nojekyll weeks/01-what-is-ai/explorer/
git commit -m "Week 1: self-contained explorer page for next words, tokens and attention"
```

### Task 3: README, slides and assignment

**Files:**
- Modify: `weeks/01-what-is-ai/README.md` (replace the stub, starting from `templates/README.md`)
- Create: `weeks/01-what-is-ai/slides.md`, `weeks/01-what-is-ai/slides.pdf` (built)
- Create: `weeks/01-what-is-ai/assignment.md`

**Interfaces:**
- Consumes: the explorer URL `https://vasuchettyphd.github.io/ai-dev-course/weeks/01-what-is-ai/explorer/` (live after Task 5), the relative link `explorer/index.html` for the repo copy, and the real numbers in `data.json`. Quote these exactly: no rounding beyond one decimal place in percentages.

- [ ] **Step 1: Fact-check sheet first**

Read the paper's abstract and introduction at https://arxiv.org/abs/1706.03762. Write the facts you will use, each with where it is in the paper, into the task report:
- title, year and venue
- number of authors, and that they were at Google Brain and Google Research
- the core claim: attention alone, without recurrence or convolutions
- the original task (machine translation)
- that it introduced the Transformer architecture

Use only facts on this sheet. Every number in the README or slides about the explorer must be copied from `data.json`.

- [ ] **Step 2: README.md**

Use the template's sections. Required content:
- **Header:** Goal, Time (about 75 minutes), Cost ("nothing beyond your browser"), and Tested with (the model name and revision, and the date).
- **Steps** (each step is a short explanation followed by an explorer activity):
  1. **AI as next-word prediction.** Explain probability as "how likely, out of 100 tries". Activity: guess the next word for 3 prompts. Discussion question: "Why might the model pick a likely word that's false?"
  2. **Temperature.** Activity: slide it, and watch the choices sharpen and spread.
  3. **Tokens.** Activity: find the most surprising token split. Cover why the strawberry question trips models up, and what this means for cost (pricing is per token).
  4. **Attention and *Attention Is All You Need*.** Explain in plain words, using only the fact-check sheet. Activity: the trophy and suitcase pair. Include the sentence "Attention shows where the model looked, not proof that it understood."
  5. **Training vs. using a model.** Training is reading huge amounts of text to tune the numbers. Using the model is predicting one token at a time. Cover why the model doesn't "look things up" unless given tools, which week 11 teaches.
  6. **Why models make things up.** Tie this back to step 1. Preview week 12, evaluation.
- **Check it worked:** a list of 3 things the student can now explain.
- **Troubleshooting:** the page won't load (use the repo copy `explorer/index.html` and download it), and the page looks wrong on a phone (rotate it, or use a laptop).
- **Remove** the `Status: coming soon` line.

- [ ] **Step 3: slides.md, then build the PDF**

Start from `templates/slides.md` and write 18-24 slides, in this order: title; agenda; probability with a dice or weather example; next-word prediction; live demo cue (explorer next word); temperature; tokens; live demo cue (tokens); the 2017 paper (title, year, one-sentence idea); before vs. after attention (one picture made of Marp text boxes or an ASCII diagram, no external images); attention demo cue; what attention is not; training vs. using; why models make things up; what is coming in weeks 2-14; this week's assignment. Every fact comes from the fact-check sheet or `data.json`.

Run: `npm run slides`
Expected: `weeks/01-what-is-ai/slides.pdf` is produced.

- [ ] **Step 4: assignment.md**

From `templates/assignment.md`:
- **What to do:**
  - (a) List 3 problems from their work, studies or life where AI might help. Tag each "good fit" or "poor fit" for a next-word predictor, with one sentence why.
  - (b) Write one paragraph on the most surprising thing they saw in the explorer, quoting a number from it.
- **What to hand in:** one document, about one page long.
- **Rubric** under `## Rubric`:
  - Three problems, each tagged with a reason: 4 points
  - Reasons show understanding of next-word prediction: 3 points
  - Reflection quotes a real number from the explorer and explains it: 3 points
  - Total: 10 points

- [ ] **Step 5: Check and commit**

Run: `python3 scripts/check_course.py`
Expected: `OK`.

Run: `grep -c "proof that it understood" weeks/01-what-is-ai/README.md`
Expected: 1.

```bash
git add weeks/01-what-is-ai/README.md weeks/01-what-is-ai/slides.md weeks/01-what-is-ai/slides.pdf weeks/01-what-is-ai/assignment.md
git commit -m "Week 1: tutorial, slides and assignment"
```

### Task 4: Instructor notes (private repo)

**Files:**
- Modify: `~/claude/ai-dev-course-instructor/weeks/01-what-is-ai/notes.md` (on new branch `week-01`)

- [ ] **Step 1: Write the notes**

Fill the four headings and remove `Status: not written yet`.
- **Timing:** a 75-minute session plan with minute marks.
- **Common problems:** the misconceptions "it looks things up", "it understands", "temperature is randomness I can turn off for truth" and "more tokens means smarter", each with a one-line correction. Also the problem of the page not loading on campus wifi (it is a local file, so download the repo copy).
- **Discussion answers:** answers to every discussion question in the README, citing the actual explorer numbers.
- **Grading guidance:** an example of a 10/10 and a 6/10 submission for the rubric, and how to score a "good fit" tag with a weak reason.

No em dashes.

- [ ] **Step 2: Commit on the branch**

```bash
cd ~/claude/ai-dev-course-instructor && git checkout -b week-01 && git add weeks/01-what-is-ai/notes.md && git commit -m "Week 1 instructor notes"
```

### Task 5: GitHub Pages and PRs (controller)

- [ ] **Step 1:** Push `week-01-what-is-ai`. Open the PR with the `github:gh-create-pr` skill, and ask the user to merge it.
- [ ] **Step 2:** After the merge, enable GitHub Pages: `POST /repos/vasuchettyphd/ai-dev-course/pages` with `{"source":{"branch":"main","path":"/"}}`. This is the step the user approved in the week 1 design.
- [ ] **Step 3:** Poll `GET /repos/vasuchettyphd/ai-dev-course/pages/builds/latest` until its status is `built`. Then `curl -sI https://vasuchettyphd.github.io/ai-dev-course/weeks/01-what-is-ai/explorer/` should return HTTP 200.
- [ ] **Step 4:** Push `week-01` in the instructor repo, open its PR and ask the user to merge. Create and close the OpenProject task "Week 1: What AI is" in project 4.
