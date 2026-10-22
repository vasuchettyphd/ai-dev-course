#!/usr/bin/env bash
# Runs prove_bugs.py against practice/leaky-notes. Uses uv if you have it,
# otherwise a throwaway virtual environment in practice/.venv.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$HERE/practice/leaky-notes"
VENV="$HERE/practice/.venv"

if [ ! -d "$TARGET" ]; then
  echo "Run ./setup.sh first." >&2
  exit 1
fi

export PYTHONDONTWRITEBYTECODE=1

if command -v uv >/dev/null 2>&1; then
  exec uv run --quiet --no-project --with-requirements "$TARGET/requirements.txt" \
    python "$HERE/prove_bugs.py" "$TARGET"
fi

if [ ! -x "$VENV/bin/python" ]; then
  if ! python3 -m venv "$VENV"; then
    rm -rf "$VENV"
    echo "python3 -m venv failed. Install uv (https://docs.astral.sh/uv/) or python3-venv and retry." >&2
    exit 1
  fi
  "$VENV/bin/pip" install -q -r "$TARGET/requirements.txt"
fi
"$VENV/bin/python" "$HERE/prove_bugs.py" "$TARGET"
