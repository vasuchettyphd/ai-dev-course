"""Pick the clear attention example for the Week 1 explorer, transparently.

Re-run (same environment as compute.py):
    HF_HOME=<cache dir> <venv>/bin/python weeks/01-what-is-ai/explorer/choose_example.py

Each candidate names a source token and an earlier target token. For every
layer we take the head-averaged attention row of the source token, drop column
0 (the first token, an attention sink that soaks up weight), renormalise the
rest to sum 1, and read off the target's share. A sentence's score is its best
layer's share; the margin is that share minus the next-highest non-first token
in the same layer. The winner is the highest score with a positive margin.
Every candidate is written to choose_example_results.json (committed).
Same package versions as compute.py.
"""
import json
import pathlib

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-0.5B"
HERE = pathlib.Path(__file__).parent

# (sentence, source piece, which source occurrence, target piece, which target occurrence)
CANDIDATES = [
    ("Maria paid the bill because she", " she", "last", " Maria", "first"),
    ("The keys were on the table, so I picked up the", " the", "last", " keys", "first"),
    ("Apples are red and bananas are yellow, so a banana is", " is", "last", " yellow", "first"),
    ("My sister Anna loves jazz. Every Friday, Anna", " Anna", "last", " Anna", "first"),
    ("Paris is in France and Berlin is in", " in", "last", " Berlin", "first"),
    ("The password is tulip. Later, I typed the password: tulip", "ip", "last", "ip", "first"),  # " tulip" is two tokens (" tul", "ip"); use the final piece of each
]


def find(pieces, wanted, which):
    """Index of a piece matching `wanted` (exact, else ignoring spaces)."""
    for exact in (True, False):
        hits = [i for i, p in enumerate(pieces)
                if (p == wanted if exact else p.strip() == wanted.strip())]
        if hits:
            return hits[-1] if which == "last" else hits[0]
    raise ValueError(f"{wanted!r} not in {pieces}")


def renorm_row(row):
    """Drop column 0 and renormalise the rest of the row to sum 1."""
    rest = row[1:]
    total = sum(rest)
    return [v / total for v in rest] if total > 0 else rest


def head_avg_layers(tok, model, sentence):
    enc = tok(sentence, return_tensors="pt")
    with torch.no_grad():
        out = model(**enc, output_attentions=True)
    pieces = [tok.decode([int(i)]) for i in enc.input_ids[0]]
    return pieces, [a[0].mean(dim=0).tolist() for a in out.attentions]


def best_share(layers, src, tgt):
    """Best layer for target share (target must not be column 0)."""
    best = None
    for L, mat in enumerate(layers):
        shares = renorm_row(mat[src][: src + 1])  # index k here is token k+1
        share = shares[tgt - 1]
        others = [v for k, v in enumerate(shares) if k != tgt - 1]
        margin = share - max(others) if others else share
        if best is None or share > best["share"]:
            best = {"layer": L, "share": share, "margin": margin}
    return best


def main():
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, attn_implementation="eager", dtype=torch.float32)
    model.eval()
    rows = []
    for sentence, sp, sw, tp, tw in CANDIDATES:
        pieces, layers = head_avg_layers(tok, model, sentence)
        src, tgt = find(pieces, sp, sw), find(pieces, tp, tw)
        row = {"sentence": sentence, "tokens": pieces, "source_index": src,
               "target_index": tgt, "source": pieces[src], "target": pieces[tgt]}
        if tgt == 0 or tgt >= src:
            row.update(layer=None, share=None, margin=None,
                       note="target is the first token (excluded as attention sink) or not before the source")
        else:
            b = best_share(layers, src, tgt)
            row.update(layer=b["layer"], share=round(b["share"], 4),
                       margin=round(b["margin"], 4), note="")
        rows.append(row)
    ok = [r for r in rows if r["share"] is not None and r["margin"] > 0]
    winner = max(ok, key=lambda r: r["share"]) if ok else None
    result = {"model": MODEL, "candidates": rows, "winner": winner}
    (HERE / "choose_example_results.json").write_text(
        json.dumps(result, ensure_ascii=True, indent=1) + "\n", encoding="utf-8")
    for r in rows:
        print(r["sentence"], r["layer"], r["share"], r["margin"])
    print("winner:", winner and winner["sentence"])


if __name__ == "__main__":
    main()
