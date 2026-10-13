"""Ask Claude about a listing in plain English; Claude uses the calculator as a tool (week 11).

  python3 -m dealscreener.agent "your question"

How it works (the agent loop): the question goes to Claude Haiku together with the
screen_listing tool's description. If Claude wants numbers, it replies with a tool call;
this program runs the tool (the deal screener's own calculator) and sends the result back.
That repeats until Claude gives its final answer, or until MAX_TURNS calls, whichever
comes first. Claude never works the numbers out itself: every number comes from the tool.

This file uses only Python's standard library when it loads. The anthropic package is
needed only for a real call (see extract.make_client). The tests use a fake client.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass

from dealscreener import extract, tools

# The most calls to Claude for one question. The docs set no limit: 5 is the course's own
# safety rule, so a confused model can't run up a bill by calling the tool forever.
MAX_TURNS = 5

USAGE = 'Usage: python3 -m dealscreener.agent "your question"'

SYSTEM_PROMPT = (
    "You help a beginner property investor screen rental listings. "
    "Use the screen_listing tool for every number you report; never work numbers out yourself. "
    "If the question is missing any of the nine numbers, ask the user for them and do not call the tool. "
    "If the tool returns an error, fix the input if the user's question makes the right number clear; "
    "otherwise ask the user. "
    "Explain the result in plain English for a beginner."
)


@dataclass
class AgentResult:
    text: str | None  # the final answer, or None if MAX_TURNS ran out first
    turns: int  # calls to Claude
    input_tokens: int  # summed over every call
    output_tokens: int
    tool_calls: int


def run_agent(question: str, client, print_fn=print) -> AgentResult:
    """Run the agent loop for one question. Raises extract.ExtractionError with a plain
    sentence if Claude's answer was cut off or declined."""
    history = [{"role": "user", "content": question}]
    input_tokens = output_tokens = tool_calls = 0
    for turn in range(1, MAX_TURNS + 1):
        response = client.messages.create(
            model=extract.MODEL,
            max_tokens=extract.MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=[tools.TOOL_SCHEMA],
            messages=history,
        )
        input_tokens += response.usage.input_tokens
        output_tokens += response.usage.output_tokens
        if response.stop_reason == "max_tokens":
            raise extract.ExtractionError("The model's answer was cut off before it finished.")
        if response.stop_reason == "refusal":
            raise extract.ExtractionError("The model declined to answer.")
        # The whole reply goes back unchanged, thinking blocks included: the docs say they
        # must be passed back "complete and unmodified" when tools are used.
        history.append({"role": "assistant", "content": response.content})
        calls = [block for block in response.content if getattr(block, "type", None) == "tool_use"]
        if response.stop_reason != "tool_use" or not calls:
            # The final answer. A reply can start with a thinking block: pick text blocks by type.
            texts = [block.text for block in response.content if getattr(block, "type", None) == "text"]
            answer = "\n".join(texts).strip()
            if not answer:
                raise extract.ExtractionError("The model's answer had no text in it.")
            return AgentResult(answer, turn, input_tokens, output_tokens, tool_calls)
        # One tool_result for every tool call, all in one user message, in the same order.
        results = []
        for block in calls:
            tool_calls += 1
            print_fn(f"Calling {block.name} with {json.dumps(block.input, separators=(',', ':'))}")
            results.append(run_tool(block))
        history.append({"role": "user", "content": results})
    return AgentResult(None, MAX_TURNS, input_tokens, output_tokens, tool_calls)


def run_tool(block) -> dict:
    """Run one tool call and return its tool_result block. A problem goes back to Claude as
    a sentence with is_error set, so it can fix the input or ask the user."""
    if block.name != tools.TOOL_NAME:
        return {"type": "tool_result", "tool_use_id": block.id, "content": "Unknown tool.", "is_error": True}
    try:
        result = tools.screen_listing(block.input)
    except tools.ToolInputError as problem:
        return {"type": "tool_result", "tool_use_id": block.id, "content": str(problem), "is_error": True}
    return {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)}


def main(argv, print_fn=print, client_factory=extract.make_client) -> int:
    """Answer one question. Returns 0 when it worked, 1 when it couldn't, 2 for a usage mistake."""
    extract.load_env_file()  # the API key, from a .env file in this folder, if there is one
    question = " ".join(argv).strip()
    if not question:
        print_fn(USAGE)
        return 2
    try:
        result = run_agent(question, client_factory(), print_fn)
    except extract.ExtractionError as problem:  # no key, no package, cut off or declined
        print_fn(str(problem))
        return 1
    except Exception as error:  # any failed call: a plain sentence, never a traceback or the key
        print_fn(extract.describe_error(error))
        return 1
    print_fn("")
    if result.text is None:
        print_fn(f"Stopped after {MAX_TURNS} turns without a final answer.")
    else:
        print_fn(result.text)
    print_fn("")
    cost = extract.cost_usd(result.input_tokens, result.output_tokens)
    print_fn(f"Used {result.input_tokens} input and {result.output_tokens} output tokens "
             f"on Claude in {result.turns} {'turn' if result.turns == 1 else 'turns'}, about ${cost:.5f}.")
    return 1 if result.text is None else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
