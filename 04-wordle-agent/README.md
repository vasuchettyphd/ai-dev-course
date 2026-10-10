# Build an Agent That Plays Wordle

A hands-on tutorial that builds a small agent which does something a chatbot
genuinely cannot: it solves a puzzle whose answer is **not knowable in advance**
by guessing, reading real feedback, and reasoning its way to the answer, then
refuses to claim victory until it has actually won.

The full working code is in `agent.py`. It is about 260 lines, and most of that
is the logic that gives the agent good feedback (Step 5), which turns out to be
where the real work lives.

## What the agent does

It plays Wordle. There is a secret 5-letter word it cannot see. Each turn it:

1. Guesses a word.
2. Reads the feedback (each letter comes back `correct`, `present`, or `absent`).
3. Uses that feedback to make a smarter next guess.

It repeats until every letter comes back `correct`. That is the entire job, and
you already know the game, so there is nothing abstract to picture.

## Why a plain LLM cannot do this

This is the reason Wordle is the example.

Ask ChatGPT "what is the secret word?" and it is stuck. The word is a secret. It
is not in any training data. The model can blurt out a guess with total
confidence, but it has no way to know if it is right and no way to find out.

An LLM is a brain with no senses. It can reason brilliantly, but it cannot
**look at the board.** The only way to solve a Wordle is to play it: guess, read
the real feedback, and adjust. That guess-read-adjust loop is exactly what an
agent is. The model supplies the reasoning; the loop supplies the eyes. Neither
half can win alone, and that is the whole point of this tutorial.

> The same is true of Claude's `/goal` or ChatGPT's tools. They are agents too.
> The difference here is that you are building the loop yourself, in code, wired
> to your own rules, with your own definition of what counts as winning. That is
> what you do when you are the developer instead of the end user.

## What you will build

An agent with exactly one tool, `guess(word)`, which is its only way to interact
with the puzzle. It guesses, reads feedback, and narrows in. Then comes the part
that makes it airtight: a **validator** that checks the agent's claimed answer
against the real word the instant it says it is done. If the word is wrong, the
agent is sent back to keep playing. It cannot bluff a win.

## Prerequisites

- Python 3.10 or newer
- An API key for one model provider (Anthropic or OpenAI)

## Step 0: Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # then edit .env and add your key
set -a; source .env; set +a
```

## Step 1: The secret word and the scorer

The secret word lives in your code. The agent never sees it. The `score_guess`
function is the Wordle rulebook: it compares a guess to the secret and returns
feedback. (It handles repeated letters the proper Wordle way, even though the
default word has none.)

```python
from collections import Counter

SECRET_WORD = "AGENT"
MAX_GUESSES = 6

def score_tiles(guess: str, secret: str) -> list[tuple[str, str]]:
    guess, secret = guess.upper(), secret.upper()
    result = ["absent"] * len(guess)
    remaining = Counter(secret)

    # First pass: exact matches (the green tiles).
    for i, ch in enumerate(guess):
        if i < len(secret) and ch == secret[i]:
            result[i] = "correct"
            remaining[ch] -= 1

    # Second pass: right letter, wrong spot (the yellow tiles).
    for i, ch in enumerate(guess):
        if result[i] == "correct":
            continue
        if remaining[ch] > 0:
            result[i] = "present"
            remaining[ch] -= 1

    return list(zip(guess, result))
```

It returns one `(letter, status)` pair per tile, where status is `correct`,
`present`, or `absent`. The web app in Step 9 uses those statuses to color the
board; the command line just joins them into a line of text.

You, reading this, can see the secret. The model never will. To the agent the
word is a true black box.

## Step 2: The agent's state

Tools share a small `Deps` object. Ours holds the secret, a log of every word
the agent has guessed, and an optional `on_guess` callback. The command line
leaves the callback unset; the web app in Step 9 sets it so the browser can
watch each guess as it lands. The agent never knows the difference.

```python
from dataclasses import dataclass, field
from typing import Callable, Optional

@dataclass
class Deps:
    secret: str
    guesses: list[str] = field(default_factory=list)
    on_guess: Optional[Callable[[str, list], None]] = None
```

## Step 3: The result it must return

When the agent thinks it has won, it returns a validated object, not prose.

```python
from pydantic import BaseModel, Field

class Solution(BaseModel):
    word: str = Field(description="Your final answer: the word you believe is the secret.")
    solved: bool = Field(description="True only if every letter of `word` came back 'correct'.")
    guesses_used: int = Field(description="How many guesses it took.")
```

The `solved` flag matters: it lets the agent admit defeat honestly if it runs
out of guesses, while still letting us catch any false claim of victory in
Step 6.

## Step 4: Create the agent

The system prompt teaches it the rules: it cannot see the word, its only move is
to guess, and here is what each feedback label means.

```python
from pydantic_ai import Agent

agent = Agent(
    MODEL,
    deps_type=Deps,
    output_type=Solution,
    system_prompt=(
        f"You are playing Wordle. There is a secret 5-letter English word. "
        f"You have {MAX_GUESSES} guesses. Call guess(word) with a real 5-letter "
        "word. The feedback labels each letter: 'correct' means right letter in "
        "the right spot, 'present' means the letter is in the word but in a "
        "different spot, 'absent' means the letter is not in the word at all. "
        "Use the feedback from every guess to narrow down the answer. Open with "
        "a word rich in common letters. When every letter comes back 'correct', "
        "report that word with solved=true. If you use up all your guesses "
        "without solving it, report your most likely word with solved=false."
    ),
)
```

## Step 5: The one tool, and the most important lesson

This is the agent's only way to touch the puzzle. A first version just scored
the guess and returned a line like `A=present`, leaving the model to remember
and re-combine every clue across all six turns, in its head. It played badly:
it repeated words, abandoned letters it had already confirmed, and reused
letters it knew were absent.

That was not the model being dumb. It was the tool giving terrible feedback.
**An agent is only as good as the observations and guardrails its environment
provides.** So the real work is in the tool, not the prompt. The tool does three
things a good Wordle player does automatically:

1. **Refuses repeats and rule-breaking guesses.** It replays the history to see
   what is known, and rejects any guess that drops a confirmed letter, reuses an
   absent one, or puts a letter in a ruled-out spot. This is Wordle hard mode,
   enforced by the environment so the model cannot waste a turn.
2. **Hands back a running recap** of everything known so far, so the next guess
   reasons from a clean state instead of re-deriving it.
3. **Streams the guess** to anyone watching (the web UI in Step 9).

```python
from pydantic_ai import RunContext

@agent.tool
def guess(ctx: RunContext[Deps], word: str) -> str:
    """Guess a 5-letter word and get Wordle feedback for each letter."""
    word = word.strip().upper()

    # A rejected guess is a normal game event, not a malformed call: return the
    # reason and let the agent try again. It does not count as one of the six.
    if len(word) != 5 or not word.isalpha():
        return f"{word!r} is not a 5-letter word. Guess a real 5-letter word."
    if len(ctx.deps.guesses) >= MAX_GUESSES:
        return (f"No guesses left. You used all {MAX_GUESSES} and did not solve it. "
                "Report your most likely word with solved=false.")
    if word in ctx.deps.guesses:
        return f"You already guessed {word}. Try a word you have not tried yet."

    # Enforce the rules against everything learned so far.
    greens, present, bad_pos, absent = review_constraints(ctx.deps.guesses, ctx.deps.secret)
    problem = rule_violation(word, greens, present, bad_pos, absent)
    if problem:
        recap = knowledge_summary(greens, present, bad_pos, absent, ctx.deps.guesses)
        return f"{word} wastes what you know: {problem}. {recap} Guess again."

    ctx.deps.guesses.append(word)
    tiles = score_tiles(word, ctx.deps.secret)
    feedback = " | ".join(f"{ch}={tag}" for ch, tag in tiles)
    print(f"   guess #{len(ctx.deps.guesses)}: {word}  ->  {feedback}")

    if ctx.deps.on_guess:                       # let the web UI watch (Step 9)
        ctx.deps.on_guess(word, [[ch, tag] for ch, tag in tiles])

    if word == ctx.deps.secret:
        return f"{feedback}  (every letter correct, you solved it!)"

    # Feedback plus a recap, so the next guess starts from a clean picture.
    greens, present, bad_pos, absent = review_constraints(ctx.deps.guesses, ctx.deps.secret)
    recap = knowledge_summary(greens, present, bad_pos, absent, ctx.deps.guesses)
    return f"{feedback}\nWhat you know now: {recap}"
```

The helpers `review_constraints`, `rule_violation`, and `knowledge_summary` are
plain Python (no AI) that replay the guess history into "what is known". They are
in `agent.py`; the gist is that they turn a pile of past feedback into greens,
present letters, ruled-out spots, and absent letters. With them, a clean recap
looks like:

```
Confirmed: position 4=N, position 5=T. In the word, not yet placed: A, E.
Not in the word: C, L, P, R. Already guessed: CRANE, PLANT.
```

Note we **return** rejections instead of raising an error. A broken guess is a
normal move in the game, not a crash, so the agent just reads why and guesses
again.

## Step 6: The trick - a validator the model cannot fake

Here is what separates this from a clever prompt. Right before the agent is
allowed to finish, this runs. If the agent claims it won (`solved=true`), it
checks the word against the real secret. If that claim is false, it raises
`ModelRetry` and throws the agent back into the game. (A loss, `solved=false`,
is accepted honestly.)

```python
@agent.output_validator
def cannot_fake_a_win(ctx: RunContext[Deps], result: Solution) -> Solution:
    result.word = result.word.strip().upper()
    if result.solved and result.word != ctx.deps.secret:
        raise ModelRetry(
            "You claimed solved=true, but that is not the secret word. Keep "
            "guessing; only set solved=true once every letter comes back 'correct'."
        )
    return result
```

A chatbot can *say* "the word is SLATE" with total confidence and be wrong, and
nothing stops it. This agent's *claim of victory* is checked against the truth
before it is accepted. **It is structurally impossible for it to claim a win it
did not earn.** That guarantee is the thing you get by building the agent
yourself.

## Step 7: Run the loop

A single `run_sync` runs the whole game: the model guesses, reads feedback,
guesses again, until it produces a `Solution` that passes the validator.
`UsageLimits` is a hard cap so it can never spin forever.

```python
from pydantic_ai.usage import UsageLimits

deps = Deps(secret=SECRET_WORD)
result = agent.run_sync(
    "Solve the Wordle. Guess words, read the feedback, and find the secret word.",
    deps=deps,
    usage_limits=UsageLimits(request_limit=20),
)
print(result.output.word)
```

## Step 8: Watch it play

```bash
python agent.py
```

You will see it reason its way in. Here is a real run (Claude Sonnet 4.6):

```
The agent is playing Wordle against a secret 5-letter word.

It can only learn the word by guessing and reading the feedback:

   guess #1: CRANE  ->  C=absent | R=absent | A=present | N=correct | E=present
   guess #2: PLANT  ->  P=absent | L=absent | A=present | N=correct | T=correct
   guess #3: AGENT  ->  A=correct | G=correct | E=correct | N=correct | T=correct

Solved 'AGENT' in 3 guesses.
Guesses: CRANE, PLANT, AGENT
```

Read what happened. After `CRANE`, the agent learned the word contains A, E, and
N, with N in the fourth slot, and no C or R. After `PLANT`, it learned the word
also ends in T, and still has an A somewhere other than the third slot. From
those clues it reasoned its way to `AGENT`. It never *knew* the answer. It
*figured it out* from real feedback. The exact path differs every run: in other
runs it took five or six guesses, wandering through words like SNOUT and AVANT
before landing it. That variation is the agent thinking, not a script you wrote.

## How the loop actually works

```
  goal --> [ model ] -- "guess CRANE" --> guess("CRANE")
             ^                                  |
             |                          score the guess
             |                                  v
        feedback <----------------- [ the secret word ]
             |
             '--> model: guess again, or submit the answer
                          |
                          v
                 [ validator checks the answer ] --right--> done
                          |
                       wrong / ModelRetry --> back into the game
```

The model drives the play. pydantic-ai runs the mechanics: handing the tool to
the model, running it, validating the final answer, and enforcing the guess
limit.

## Why this matters beyond a game

Wordle is a stand-in for any task where the answer can only be found by
interacting with a system you cannot predict in advance:

- Adjust a database query until it returns the rows you need.
- Tune a setting until a health check goes green.
- Try inputs until a test, a sensor, or an API responds the way you want.

In every case the pattern is identical to this tutorial: act, read reality,
adjust, and refuse to finish until an objective check confirms success. That is
the kind of agent you cannot replace with a chat window, and it is the reason to
learn to build one.

## Step 9: Watch it play in the browser

The command line is fine, but watching the agent fill in a real Wordle board is
far more convincing. We add a tiny web app, and the agent itself does not change
at all. We only use the `on_guess` callback we already built into `Deps`.

There are two new files. `web.py` is the server:

```python
# web.py (trimmed)
import json, queue, threading
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
import agent as wordle      # reuse the agent unchanged

app = FastAPI()

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.get("/solve")
def solve():
    events = queue.Queue()

    def on_guess(word, tiles):                 # the agent calls this each guess
        events.put({"type": "guess", "word": word, "tiles": tiles})

    def play():
        deps = wordle.Deps(secret=wordle.SECRET_WORD, on_guess=on_guess)
        result = wordle.agent.run_sync("Solve the Wordle.", deps=deps,
                                       usage_limits=wordle.UsageLimits(request_limit=20))
        events.put({"type": "done", "word": result.output.word,
                    "solved": result.output.solved, "guesses": len(deps.guesses)})
        events.put(None)

    threading.Thread(target=play, daemon=True).start()

    def stream():                              # push each event to the browser
        while (item := events.get()) is not None:
            yield f"data: {json.dumps(item)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
```

The idea: the agent runs in a background thread, and every time its tool calls
`on_guess`, we drop the guess onto a queue. The `/solve` endpoint drains that
queue and streams each guess to the browser using Server-Sent Events (a one-way
"server keeps pushing updates" channel). The second file, `static/index.html`,
is a Wordle board that opens `/solve`, and colors in a row each time a guess
arrives. (See the file for the full HTML and CSS.)

Run it:

```bash
uvicorn web:app --reload --port 8765
```

Then open http://localhost:8765 and click "Solve it". You will watch the agent
fill in the board live, one guess at a time, exactly as it plays on the server.
If it wins you get "Solved MONEY in 4 guesses"; if it ever runs out, you get an
honest "Did not crack it in 6 guesses".

Each game picks a fresh random word from a small list (`pick_secret` in
`agent.py`), so once a game finishes the button turns into "Next word" and you
can keep clicking to watch it play new puzzles. Set `WORDLE_SECRET` to pin one
word instead.

The point worth pausing on: `agent.py` did not change. The same agent that runs
on the command line now drives a web UI, because the agent is decoupled from how
its progress is shown. That is what makes an agent reusable inside real software.

## Ideas to extend it

- Change the secret with `WORDLE_SECRET=ROBOT python agent.py` and watch the
  agent still solve it. It never relied on knowing the word.
- Grow `WORD_LIST` (or load a real word file) so the random games have more
  variety than the starter list of thirty words.
- Validate guesses against a real dictionary so the agent cannot play made-up
  words like AHENS. (Right now the tool only enforces Wordle logic, not that a
  guess is a real word.)
- Lower `MAX_GUESSES` to 4 and see how the agent's strategy has to sharpen.
- Temporarily remove the rule enforcement and recap from Step 5, and watch the
  agent play badly again. It is the clearest way to feel how much an agent
  depends on the quality of its environment.

## File map

- `agent.py` - the complete, runnable agent (Steps 1-8)
- `web.py` - the FastAPI server for the browser demo (Step 9)
- `static/index.html` - the Wordle board the browser shows
- `requirements.txt` - dependencies
- `.env.example` - copy to `.env` and add your key
