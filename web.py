"""
A tiny web app that lets you watch the Wordle agent play in the browser.

Click "Solve it" and the page opens a streaming connection to /solve. The agent
starts playing on the server, and every guess it makes is pushed to the browser
the instant it happens, landing on a real Wordle board.

It reuses agent.py unchanged, except for the on_guess callback the agent already
supports. The agent has no idea it is being watched.

Run it (after activating the venv and loading your API key):
    uvicorn web:app --reload --port 8765
Then open http://localhost:8765
"""

from __future__ import annotations

import json
import queue
import threading
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse

import agent as wordle

app = FastAPI()
STATIC = Path(__file__).parent / "static"


@app.get("/")
def index() -> FileResponse:
    """Serve the single-page Wordle board."""
    return FileResponse(STATIC / "index.html")


@app.get("/solve")
def solve() -> StreamingResponse:
    """Run the agent and stream each guess to the browser as a Server-Sent Event."""
    events: queue.Queue = queue.Queue()

    def on_guess(word: str, tiles: list) -> None:
        # Called by the agent's tool on every guess. Hand it to the stream.
        events.put({"type": "guess", "word": word, "tiles": tiles})

    def play() -> None:
        try:
            # A fresh random word each game, so every click is a new puzzle.
            deps = wordle.Deps(secret=wordle.pick_secret(), on_guess=on_guess)
            result = wordle.agent.run_sync(
                "Solve the Wordle. Guess words, read the feedback, and find the secret word.",
                deps=deps,
                usage_limits=wordle.UsageLimits(request_limit=30),
            )
            events.put({
                "type": "done",
                "word": result.output.word,
                "solved": result.output.solved,
                "guesses": len(deps.guesses),
            })
        except Exception as exc:  # surface setup errors (e.g. missing API key) to the page
            events.put({"type": "error", "message": str(exc)})
        finally:
            events.put(None)  # sentinel: closes the stream

    threading.Thread(target=play, daemon=True).start()

    def stream():
        while True:
            item = events.get()
            if item is None:
                break
            yield f"data: {json.dumps(item)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
