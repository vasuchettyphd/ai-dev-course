"""
Wordle-Solving Agent, built with pydantic-ai.

The agent plays Wordle. There is a secret 5-letter word it cannot see. It
guesses a word, reads the correct / present / absent feedback, and reasons its
way to the answer, the same way a person would.

A plain LLM cannot do this. It does not know the secret word, and no amount of
thinking reveals it. The only path to the answer is to guess, read real
feedback, and use it. That guess-read-adjust loop is what makes this an agent.

The detail that makes it airtight: when the agent claims it solved the puzzle,
an output validator checks the word against the real answer. It cannot claim a
win it did not earn.

Run it:
    python agent.py
"""

from __future__ import annotations

import os
import random
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable, Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.usage import UsageLimits

MODEL = os.environ.get("AGENT_MODEL", "anthropic:claude-sonnet-4-6")

# The secret word lives here. The agent NEVER sees it. Its only way to learn
# anything about it is to guess and read the feedback. Change it with the
# WORDLE_SECRET env var to prove the agent never relied on knowing it.
SECRET_WORD = os.environ.get("WORDLE_SECRET", "AGENT").upper()
MAX_GUESSES = 6

# A pool of common 5-letter words, so each new game can use a fresh secret.
WORD_LIST = [
    "AGENT", "CRANE", "PLANT", "ROBOT", "HOUSE", "LIGHT", "BRAIN", "STORM",
    "MONEY", "PIANO", "BREAD", "CLOUD", "FROST", "GRAPE", "JUDGE", "KNIFE",
    "LEMON", "MARCH", "OCEAN", "PRIDE", "RIVER", "SNAKE", "TIGER", "VOICE",
    "WHALE", "YACHT", "ZEBRA", "FLAME", "GHOST", "MUSIC",
]


def pick_secret() -> str:
    """Choose a secret word. WORDLE_SECRET pins it; otherwise pick at random."""
    forced = os.environ.get("WORDLE_SECRET")
    return forced.upper() if forced else random.choice(WORD_LIST)


def score_tiles(guess: str, secret: str) -> list[tuple[str, str]]:
    """Score a guess into (letter, status) tiles, using the standard Wordle rules."""
    guess, secret = guess.upper(), secret.upper()
    result = ["absent"] * len(guess)
    remaining = Counter(secret)

    # First pass: exact matches (the green tiles).
    for i, ch in enumerate(guess):
        if i < len(secret) and ch == secret[i]:
            result[i] = "correct"
            remaining[ch] -= 1

    # Second pass: right letter, wrong spot (the yellow tiles), if copies remain.
    for i, ch in enumerate(guess):
        if result[i] == "correct":
            continue
        if remaining[ch] > 0:
            result[i] = "present"
            remaining[ch] -= 1

    return list(zip(guess, result))


def score_guess(guess: str, secret: str) -> str:
    """Return Wordle feedback for one guess as a readable line of text."""
    return " | ".join(f"{ch}={tag}" for ch, tag in score_tiles(guess, secret))


def review_constraints(guesses: list[str], secret: str):
    """Replay every past guess to work out what is now known about the word.

    Returns four things:
      greens     {position index: letter}   confirmed letters in confirmed spots
      present    {letters}                   letters known to be in the word
      bad_pos    {letter: {indices}}         spots a letter is known NOT to be in
      absent     {letters}                   letters known to be absent entirely
    This is the agent's memory, computed for it instead of left in its head.
    """
    greens: dict[int, str] = {}
    present: set[str] = set()
    bad_pos: dict[str, set[int]] = {}
    seen_absent: set[str] = set()
    for word in guesses:
        for i, (ch, tag) in enumerate(score_tiles(word, secret)):
            if tag == "correct":
                greens[i] = ch
                present.add(ch)
            elif tag == "present":
                present.add(ch)
                bad_pos.setdefault(ch, set()).add(i)
            else:
                seen_absent.add(ch)
    absent = {ch for ch in seen_absent if ch not in present}
    return greens, present, bad_pos, absent


def rule_violation(word: str, greens, present, bad_pos, absent) -> str | None:
    """Return a reason the guess wastes known information, or None if it is sound.

    This is Wordle 'hard mode' plus one extra rule (do not reuse absent letters).
    It forces the agent to actually use what it has learned.
    """
    for i, ch in greens.items():
        if word[i] != ch:
            return (
                f"position {i + 1} is already known to be {ch}, "
                f"but your guess has {word[i]} there"
            )
    for ch in sorted(present):
        if ch not in word:
            return f"{ch} is in the word, so your guess must include it"
    for ch, indices in bad_pos.items():
        for i in indices:
            if word[i] == ch:
                return f"{ch} is in the word but not at position {i + 1}; put it somewhere else"
    for ch in sorted(absent):
        if ch in word:
            return f"{ch} is not in the word, so do not use it"
    return None


def knowledge_summary(greens, present, bad_pos, absent, guesses) -> str:
    """A short, plain-language recap of the state, returned to the agent each turn."""
    parts = []
    if greens:
        placed = ", ".join(f"position {i + 1}={ch}" for i, ch in sorted(greens.items()))
        parts.append(f"Confirmed: {placed}.")
    unplaced = sorted(present - set(greens.values()))
    if unplaced:
        parts.append(f"In the word, not yet placed: {', '.join(unplaced)}.")
    if absent:
        parts.append(f"Not in the word: {', '.join(sorted(absent))}.")
    if guesses:
        parts.append(f"Already guessed: {', '.join(guesses)}.")
    return " ".join(parts) if parts else "Nothing known yet."


@dataclass
class Deps:
    """State shared with the tool. `guesses` records every word the agent tried.

    `on_guess` is an optional callback. The command line leaves it None, but the
    web app sets it so the browser can watch each guess land in real time. The
    agent has no idea anyone is watching: a clean way to decouple the agent from
    how its progress is displayed.
    """

    secret: str
    guesses: list[str] = field(default_factory=list)
    on_guess: Optional[Callable[[str, list], None]] = None


class Solution(BaseModel):
    """What the agent hands back when the game is over, win or lose."""

    word: str = Field(description="Your final answer: the word you believe is the secret.")
    solved: bool = Field(description="True only if every letter of `word` came back 'correct'.")
    guesses_used: int = Field(description="How many guesses it took.")


agent = Agent(
    MODEL,
    deps_type=Deps,
    output_type=Solution,
    retries=3,  # headroom for the output validator to bounce a false win claim
    system_prompt=(
        f"You are playing Wordle. There is a secret 5-letter English word. "
        f"You have {MAX_GUESSES} guesses. Call guess(word) with a real 5-letter "
        "word. The feedback labels each letter: 'correct' means right letter in "
        "the right spot, 'present' means the letter is in the word but in a "
        "different spot, 'absent' means the letter is not in the word at all. "
        "After each guess you get a recap of everything known so far. Every new "
        "guess must respect it: keep every 'correct' letter in its position, "
        "include every letter known to be in the word, do not place a letter in "
        "a spot already ruled out, and never reuse a letter known to be absent. "
        "Open with a word rich in common letters. When every letter comes back "
        "'correct', report that word with solved=true. If you use up all your "
        "guesses without solving it, report your most likely word with solved=false."
    ),
)


@agent.tool
def guess(ctx: RunContext[Deps], word: str) -> str:
    """Guess a 5-letter word and get Wordle feedback for each letter."""
    word = word.strip().upper()

    # These are not malformed calls to "retry", they are normal game situations.
    # We return the reason as feedback and let the agent simply guess again. A
    # rejected guess does not count as one of the six.
    if len(word) != 5 or not word.isalpha():
        return f"{word!r} is not a 5-letter word. Guess a real 5-letter word."
    if len(ctx.deps.guesses) >= MAX_GUESSES:
        return (
            f"No guesses left. You used all {MAX_GUESSES} and did not solve it. "
            "Report your most likely word with solved=false."
        )
    if word in ctx.deps.guesses:
        return f"You already guessed {word}. Try a word you have not tried yet."

    # Enforce the rules against everything learned so far, so the agent cannot
    # throw away a confirmed letter or reuse one it knows is absent.
    greens, present, bad_pos, absent = review_constraints(ctx.deps.guesses, ctx.deps.secret)
    problem = rule_violation(word, greens, present, bad_pos, absent)
    if problem:
        recap = knowledge_summary(greens, present, bad_pos, absent, ctx.deps.guesses)
        return f"{word} wastes what you know: {problem}. {recap} Guess again."

    ctx.deps.guesses.append(word)
    tiles = score_tiles(word, ctx.deps.secret)
    feedback = " | ".join(f"{ch}={tag}" for ch, tag in tiles)
    print(f"   guess #{len(ctx.deps.guesses)}: {word}  ->  {feedback}")

    # Let anyone who is watching (the web UI) see this guess as it happens.
    if ctx.deps.on_guess:
        ctx.deps.on_guess(word, [[ch, tag] for ch, tag in tiles])

    if word == ctx.deps.secret:
        return f"{feedback}  (every letter correct, you solved it!)"

    # Hand back the feedback plus a running recap, so the next guess reasons
    # from a clean, accumulated picture instead of re-deriving it every turn.
    greens, present, bad_pos, absent = review_constraints(ctx.deps.guesses, ctx.deps.secret)
    recap = knowledge_summary(greens, present, bad_pos, absent, ctx.deps.guesses)
    return f"{feedback}\nWhat you know now: {recap}"


@agent.output_validator
def cannot_fake_a_win(ctx: RunContext[Deps], result: Solution) -> Solution:
    """The agent may admit defeat, but it cannot claim a win it did not earn.

    If it reports solved=true, we check the word against the real secret. If it
    does not match, we raise ModelRetry and send it back to keep guessing. A
    loss (solved=false) is accepted as-is. This is the check the model cannot
    talk its way around.
    """
    result.word = result.word.strip().upper()
    if result.solved and result.word != ctx.deps.secret:
        raise ModelRetry(
            "You claimed solved=true, but that is not the secret word. Keep "
            "guessing; only set solved=true once every letter comes back 'correct'."
        )
    return result


def main() -> None:
    deps = Deps(secret=SECRET_WORD)
    print("The agent is playing Wordle against a secret 5-letter word.\n")
    print("It can only learn the word by guessing and reading the feedback:\n")

    # request_limit is a hard cap so the loop can never run away.
    result = agent.run_sync(
        "Solve the Wordle. Guess words, read the feedback, and find the secret word.",
        deps=deps,
        usage_limits=UsageLimits(request_limit=30),
    )
    sol = result.output

    if sol.solved:
        print(f"\nSolved '{sol.word}' in {len(deps.guesses)} guesses.")
    else:
        print(f"\nDid not crack it in {MAX_GUESSES} guesses. Best guess: '{sol.word}'.")
    print(f"Guesses: {', '.join(deps.guesses)}")


if __name__ == "__main__":
    main()
