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
console.log("numbers OK");
