// node test_numbers.mjs - the next-word numbers match data.json at temperature 1.0
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
const html = readFileSync(new URL("./index.html", import.meta.url), "utf8");
const data = JSON.parse(html.match(/<script id="data" type="application\/json">(.*?)<\/script>/s)[1]);
const m = { exports: {} };
new Function("module", html.match(/<script>([\s\S]*?)<\/script>/)[1])(m);
const { nextWordDist } = m.exports;
assert.equal(typeof nextWordDist, "function", "page must export nextWordDist");
const sum = a => a.reduce((x, y) => x + y, 0);
for (const item of data.next_word) {
  const d = nextWordDist(item, 1);
  const top = d.ranked.slice(0, 10);
  top.forEach((r, i) => {
    const real = item.candidates.find(c => c.token === r.token).prob;
    assert.ok(Math.abs(r.p - real) < 0.0005, `${item.prompt} ${JSON.stringify(r.token)}: ${r.p} vs ${real}`);
  });
  const expectRest = 1 - sum(item.candidates.slice(0, 10).map(c => c.prob));
  const shownRest = 1 - sum(top.map(r => r.p));
  assert.ok(Math.abs(shownRest - expectRest) < 0.001, `${item.prompt} everything else`);
  assert.ok(Math.abs(sum(d.ranked.map(r => r.p)) + d.rest - 1) < 1e-9, "sums to 1");
  const cold = nextWordDist(item, 0.5).ranked[0].p, hot = nextWordDist(item, 2).ranked[0].p;
  assert.ok(cold > d.ranked[0].p && d.ranked[0].p > hot, "temperature sharpens/flattens top word");
}

// G6: the visible bars (top 10, the guessed word if it ranks 11-50, and "everything else")
// never add up to more than 100%.
const { nextWordBars, clearCaption, firstWordNote, guessMessage } = m.exports;
assert.equal(typeof nextWordBars, "function", "page must export nextWordBars");
for (const item of data.next_word) {
  for (const t of [0.2, 0.5, 1, 1.5, 2]) {
    const ranked = nextWordDist(item, t).ranked;
    for (const gi of [-1, 0, 9, 10, 25, 49]) {
      const bars = nextWordBars(ranked, gi);
      const total = sum(bars.rows.map(r => r.p)) + bars.rest;
      assert.ok(total <= 1 + 1e-9, `${item.prompt} t=${t} gi=${gi}: bars add to ${total}`);
      assert.ok(Math.abs(total - 1) < 1e-9, `${item.prompt} t=${t} gi=${gi}: bars should add to 100%, got ${total}`);
      assert.ok(bars.rest >= 0);
      assert.equal(bars.rows.length, gi >= 10 ? 11 : 10);
      if (gi >= 0) assert.ok(bars.rows.some(r => r.hit && r.token === ranked[gi].token));
    }
  }
}

// G3/G4: Part B caption and first-word note are built from data.json.
const paris = data.attention[2];
const cap = clearCaption(paris);
const germany = paris.next_word[0];
assert.equal(germany.token, " Germany");
const sharePct = Math.round(m.exports.focusShare(paris) * 100);
assert.equal(cap, `About ${sharePct}% of the last word's attention (setting aside the first word) goes to 'Berlin', and the model's next word here is 'Germany' (${Math.round(germany.prob * 100)}%). The attention fits the right answer, but it is not proof of why.`);
const f = paris.focus;
const full = m.exports.attnRow(paris, f.layer, f.from, true);
const note = firstWordNote(paris);
assert.equal(note, `Here the first word is 'Paris'. Tick 'Include the first word' and 'in' puts ${Math.round(full[0] * 100)}% on 'Paris' and ${Math.round(full[f.to] * 100)}% on 'Berlin'. The resting-place effect lands on whatever word comes first, so we set it aside.`);
assert.ok(note.includes("64% on 'Paris'") && note.includes("18% on 'Berlin'"), note);

// G8: a guess outside the top 50 is echoed back, with a full stop.
assert.equal(guessMessage("zebra", [], -1), "Your word \"zebra\" is not in the model's top 50.");

console.log("numbers OK");
