"""Compute the real model data for the Week 1 explorer page.

Re-run (needs torch + transformers, downloads Qwen/Qwen2.5-0.5B, about 1 GB):
    HF_HOME=<cache dir> <venv>/bin/python weeks/01-what-is-ai/explorer/compute.py

Versions used for the committed data.json (CPU build, Python 3.14; the
originally pinned torch 2.5.1 / transformers 4.46.3 have no Python 3.14 wheels):
    torch 2.14.1+cpu, transformers 5.19.0, tokenizers 0.23.3

The output (data.json) is committed. Students never run this script; the page
only reads data.json. Nothing in data.json is typed or edited by hand.
"""
import datetime
import json
import pathlib

import huggingface_hub
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-0.5B"
HERE = pathlib.Path(__file__).parent

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
ATTENTION_SENTENCES = [
    "The trophy didn't fit in the suitcase because it was too big.",
    "The trophy didn't fit in the suitcase because it was too small.",
]


def main():
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, attn_implementation="eager", torch_dtype=torch.float32
    )
    model.eval()
    # Resolved snapshot commit of the downloaded weights (transformers 5 no
    # longer exposes config._commit_hash).
    revision = pathlib.Path(
        huggingface_hub.try_to_load_from_cache(MODEL, "config.json")
    ).parent.name

    next_word = []
    with torch.no_grad():
        for prompt in PROMPTS:
            enc = tok(prompt, return_tensors="pt")
            logits = model(**enc).logits[0, -1].float()
            probs = torch.softmax(logits, dim=-1)
            top = torch.topk(logits, 50)
            cands = [
                {
                    "token": tok.decode([int(i)]),
                    "logit": round(float(logits[i]), 3),
                    "prob": round(float(probs[i]), 5),
                }
                for i in top.indices
            ]
            next_word.append({"prompt": prompt, "candidates": cands})

    tokens = []
    for text in TOKEN_TEXTS:
        ids = tok(text, add_special_tokens=False).input_ids
        pieces = [tok.decode([i]) for i in ids]
        assert "".join(pieces) == text, text
        tokens.append({"text": text, "pieces": pieces, "count": len(pieces)})

    attention = []
    with torch.no_grad():
        for sentence in ATTENTION_SENTENCES:
            enc = tok(sentence, return_tensors="pt")
            out = model(**enc, output_attentions=True)
            pieces = [tok.decode([int(i)]) for i in enc.input_ids[0]]
            layers = [
                [[round(v, 4) for v in row] for row in a[0].mean(dim=0).tolist()]
                for a in out.attentions
            ]
            attention.append({"sentence": sentence, "tokens": pieces, "layers": layers})

    data = {
        "model": MODEL,
        "revision": revision,
        "generated": datetime.date.today().isoformat(),
        "next_word": next_word,
        "tokens": tokens,
        "attention": attention,
    }
    (HERE / "data.json").write_text(
        json.dumps(data, ensure_ascii=True, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
