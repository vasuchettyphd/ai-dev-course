"""Check how well the listing step reads listings: run the model on the 20 cases in evals/
and count how many numbers it got right.

    python3 -m dealscreener.evaluate              # the 15 dev cases
    python3 -m dealscreener.evaluate --held-out   # the 5 held-out cases, once, after your change
    python3 -m dealscreener.evaluate --all        # all 20
    python3 -m dealscreener.evaluate --injection  # the 8 hostile listings (week 13)

Run it from the example-project folder. The scoring rule is in evals/README.md. This file uses
only Python's standard library when it loads; the anthropic package is needed only for a real
run (see extract.make_client). The tests use a fake model instead.
"""
from __future__ import annotations

import datetime
import json
import math
import os
import sys
from dataclasses import dataclass

from dealscreener import extract

# A number counts as right when it is within this many dollars of the expected answer.
TOLERANCE = 1.0

CASES_FILE = "evals/expected.json"
RESULTS_DIR = "evals/results"

# How many cases the set must have, and how many of them are held out.
CASE_COUNT = 20
HELD_OUT_COUNT = 5

# The prompt injection set (week 13): 8 hostile listings, none held out.
INJECTION_FILE = "evals/injection/expected.json"
INJECTION_COUNT = 8

# The same sentence the listing step (week 9) shows when there is no key.
NO_KEY = "No API key found. Put ANTHROPIC_API_KEY in a .env file (see the README)."

HELD_OUT_REMINDER = ("You are running the held-out cases. "
                     "Run them once, after your change, and report what you get.")

USAGE = ("Usage: python3 -m dealscreener.evaluate [--held-out | --all | --injection]\n"
         "  no flag     the 15 dev cases\n"
         "  --held-out  the 5 held-out cases (once, after your change)\n"
         "  --all       all 20 cases\n"
         "  --injection the 8 hostile listings (week 13)")

WHICH = {"": "dev", "--held-out": "held-out", "--all": "all", "--injection": "injection"}


class EvalError(Exception):
    """The cases file isn't right. The message is one plain sentence naming the case."""


@dataclass
class CaseResult:
    id: str
    category: str
    fields: dict  # field -> (expected, got, ok); empty when the case had an error
    error: str | None
    input_tokens: int
    output_tokens: int


def is_amount(value) -> bool:
    """True for a finite number of 0 or more (True and False don't count as numbers here)."""
    return (not isinstance(value, bool) and isinstance(value, (int, float))
            and math.isfinite(value) and value >= 0)


def load_cases(path=CASES_FILE, folder=None, case_count=CASE_COUNT, held_out_count=HELD_OUT_COUNT) -> list:
    """Read the cases file, check it, and add each listing's text as "text".

    Listing files are found in `folder`, which is the cases file's own folder unless given.
    The file must have exactly `case_count` cases, `held_out_count` of them held out.
    Raises EvalError, naming the case, if anything is wrong.
    """
    folder = os.path.dirname(path) if folder is None else folder
    try:
        with open(path, encoding="utf-8") as f:
            cases = json.load(f)
    except OSError:
        raise EvalError(f"The cases file {path} is missing. Run this from the example-project folder.") from None
    except ValueError:
        raise EvalError(f"The cases file {path} isn't valid JSON.") from None
    if not isinstance(cases, list) or not all(isinstance(case, dict) for case in cases):
        raise EvalError(f"The cases file {path} must be a list of cases.")
    if len(cases) != case_count:
        raise EvalError(f"The cases file {path} has {len(cases)} cases; it needs exactly {case_count}.")
    held_out = sum(1 for case in cases if case.get("held_out") is True)
    if held_out != held_out_count:
        raise EvalError(f"The cases file {path} marks {held_out} cases as held out; "
                        f"it needs exactly {held_out_count}.")
    seen = set()
    for number, case in enumerate(cases, start=1):
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise EvalError(f"Case number {number} in {path} has no id.")
        if case_id in seen:
            raise EvalError(f"{case_id}: this id is used more than once.")
        seen.add(case_id)
        if not isinstance(case.get("held_out"), bool):
            raise EvalError(f"{case_id}: held_out must be true or false.")
        if not isinstance(case.get("category"), str):
            raise EvalError(f"{case_id}: it has no category.")
        expected = case.get("expected")
        if not isinstance(expected, dict) or set(expected) != set(extract.FIELDS):
            names = sorted(expected) if isinstance(expected, dict) else []
            raise EvalError(f"{case_id}: its expected answers must be exactly {', '.join(extract.FIELDS)} "
                            f"(it has {', '.join(names) or 'none'}).")
        for field in extract.FIELDS:
            value = expected[field]
            if value is not None and not is_amount(value):
                raise EvalError(f"{case_id}: {field} is {value!r}; it must be a number of 0 or more, or null.")
        listing = os.path.join(folder, str(case.get("file", "")))
        if not case.get("file") or not os.path.isfile(listing):
            raise EvalError(f"{case_id}: its listing file {listing} is missing.")
        with open(listing, encoding="utf-8") as f:
            case["text"] = f.read()
    return cases


def field_ok(expected, got) -> bool:
    """Right when both are null, or both are numbers within TOLERANCE dollars."""
    if expected is None or got is None:
        return expected is None and got is None
    return abs(expected - got) <= TOLERANCE


def show(value) -> str:
    """A number as the listing would write it (1700, not 1700.0), or null."""
    if value is None:
        return "null"
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def run_cases(cases, extract_fn, print_fn=print) -> list:
    """Run extract_fn on every case's text and score it. A failed case is recorded with its
    error sentence, and the run carries on."""
    results = []
    for case in cases:
        try:
            extraction = extract_fn(case["text"])
        except extract.ExtractionError as error:
            results.append(CaseResult(case["id"], case["category"], {}, str(error), 0, 0))
            print_fn(f"{case['id']}  ERROR  {error}")
            continue
        except Exception as error:  # noqa: BLE001 - every failed call becomes one plain sentence
            sentence = extract.describe_error(error)
            results.append(CaseResult(case["id"], case["category"], {}, sentence, 0, 0))
            print_fn(f"{case['id']}  ERROR  {sentence}")
            continue
        fields = {}
        for field in extract.FIELDS:
            expected, got = case["expected"][field], extraction.values.get(field)
            fields[field] = (expected, got, field_ok(expected, got))
        results.append(CaseResult(case["id"], case["category"], fields, None,
                                  extraction.input_tokens, extraction.output_tokens))
        right = sum(1 for _, _, ok in fields.values() if ok)
        misses = [f"{field}: expected {show(expected)}, got {show(got)}"
                  for field, (expected, got, ok) in fields.items() if not ok]
        line = f"{case['id']}  {right}/{len(fields)}"
        if misses:
            line += "  " + "; ".join(misses)
        print_fn(line)
    return results


def summarise(results) -> dict:
    """The counts for the score lines, and what the calls cost."""
    scored = [r for r in results if r.error is None]
    input_tokens = sum(r.input_tokens for r in results)
    output_tokens = sum(r.output_tokens for r in results)
    return {
        "fields_right": sum(1 for r in scored for _, _, ok in r.fields.values() if ok),
        "fields_total": sum(len(r.fields) for r in scored),
        "cases_all_right": sum(1 for r in scored if all(ok for _, _, ok in r.fields.values())),
        "cases_scored": len(scored),
        "errors": len(results) - len(scored),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": extract.cost_usd(input_tokens, output_tokens),
    }


def score_line(summary) -> str:
    total = summary["fields_total"]
    percent = round(100 * summary["fields_right"] / total) if total else 0
    return (f"Score: {summary['fields_right']} of {total} fields right ({percent}%), "
            f"{summary['cases_all_right']} of {summary['cases_scored']} cases fully right. "
            f"Errors: {summary['errors']}.")


def cost_line(summary) -> str:
    return f"Cost: about ${summary['cost']:.4f}."


def today() -> str:
    return datetime.date.today().isoformat()


def write_results(results, summary, which, path=None) -> str:
    """Save the run as Markdown in RESULTS_DIR/<date>-<which>.md (a second run on the same
    day gets -2, then -3, and so on) and return the path. Only scores and fixed sentences go in:
    never a key or an error's own text."""
    if path is None:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        base = os.path.join(RESULTS_DIR, f"{today()}-{which}")
        path, number = base + ".md", 2
        while os.path.exists(path):
            path, number = f"{base}-{number}.md", number + 1
    misses = [(r, field, expected, got) for r in results if r.error is None
              for field, (expected, got, ok) in r.fields.items() if not ok]
    lines = [
        f"# Evaluation results: {which}",
        "",
        f"- Date: {today()}",
        f"- Model: {extract.MODEL}",
        f"- Set: {which} ({len(results)} cases)",
        f"- {score_line(summary)}",
        f"- {cost_line(summary)} ({summary['input_tokens']} input and "
        f"{summary['output_tokens']} output tokens)",
        "",
        "## Misses",
        "",
    ]
    if misses:
        lines += ["| Case | Category | Field | Expected | Got |", "|---|---|---|---|---|"]
        lines += [f"| {r.id} | {r.category} | {field} | {show(expected)} | {show(got)} |"
                  for r, field, expected, got in misses]
    else:
        lines.append("None.")
    lines += ["", "## Errors", ""]
    errors = [r for r in results if r.error is not None]
    lines += [f"- {r.id}: {r.error}" for r in errors] or ["None."]
    lines += ["", "## Every case", "", "| Case | Category | Right |", "|---|---|---|"]
    for r in results:
        right = "error" if r.error else f"{sum(1 for _, _, ok in r.fields.values() if ok)}/{len(r.fields)}"
        lines.append(f"| {r.id} | {r.category} | {right} |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def main(argv, print_fn=print, client_factory=extract.make_client) -> int:
    if len(argv) > 1 or (argv and argv[0] not in WHICH):
        print_fn(USAGE)
        return 2
    flag = argv[0] if argv else ""
    which = WHICH[flag]
    if which == "held-out":
        print_fn(HELD_OUT_REMINDER)
    extract.load_env_file()  # the API key, from a .env file in this folder, if there is one
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print_fn(NO_KEY)
        return 1
    try:
        if which == "injection":
            cases = load_cases(INJECTION_FILE, case_count=INJECTION_COUNT, held_out_count=0)
        else:
            cases = load_cases(CASES_FILE)
        client = client_factory()
    except (EvalError, extract.ExtractionError) as error:
        print_fn(str(error))
        return 1
    if which == "dev":
        cases = [case for case in cases if not case["held_out"]]
    elif which == "held-out":
        cases = [case for case in cases if case["held_out"]]
    group = f"all {len(cases)}" if which == "all" else f"the {len(cases)} {which}"
    print_fn(f"Running {group} cases with {extract.MODEL}.")
    results = run_cases(cases, lambda text: extract.extract_listing(text, client), print_fn)
    summary = summarise(results)
    print_fn(score_line(summary))
    print_fn(cost_line(summary))
    try:
        path = write_results(results, summary, which)
    except OSError:
        # For example a Docker container that can't write to evals/results (see the README).
        print_fn(f"Couldn't save the results file in {RESULTS_DIR}. The score above is still right: copy it down.")
        return 1
    print_fn(f"Saved: {path}")
    if results and summary["errors"] == len(results):
        print_fn("Every case failed, so there is no score. Read the errors above, fix the cause, and run it again.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
