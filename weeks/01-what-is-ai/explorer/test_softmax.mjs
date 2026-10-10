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
const big = softmax([1000, 999], 1);
assert.ok(Math.abs(sum(big) - 1) < 1e-9 && Number.isFinite(big[0]), "large logits do not overflow");
console.log("softmax OK");
