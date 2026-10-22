#!/usr/bin/env bash
# Set up the graphify demo without touching your global Claude Code setup.
#   1. installs graphify 0.9.94 into demo/.venv (nothing system-wide)
#   2. copies the course's example project into demo/practice/deal-screener
#   3. installs the /graphify skill into that copy only (project scope)
# Run it from anywhere:  advanced/graphify/demo/setup.sh
set -euo pipefail

GRAPHIFY_VERSION="0.9.94"
HERE="$(cd "$(dirname "$0")" && pwd)"
EXAMPLE="${EXAMPLE_PROJECT:-$HERE/../../../example-project}"
DEST="$HERE/practice/deal-screener"

if ! command -v uv >/dev/null; then
  echo "uv is not installed. Install it first: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi
if [ ! -d "$EXAMPLE/dealscreener" ]; then
  echo "Can't find the example project at $EXAMPLE" >&2
  exit 1
fi
if [ -e "$DEST" ]; then
  echo "$DEST already exists. Delete it first: rm -rf \"$DEST\"" >&2
  exit 1
fi

echo "==> Installing graphify $GRAPHIFY_VERSION into $HERE/.venv"
uv venv -q "$HERE/.venv"
VIRTUAL_ENV="$HERE/.venv" uv pip install -q "graphifyy==$GRAPHIFY_VERSION"
"$HERE/.venv/bin/graphify" --version

echo "==> Copying the deal screener into $DEST"
mkdir -p "$HERE/practice"
cp -R "$EXAMPLE" "$DEST"
rm -rf "$DEST/.venv" "$DEST/.env" "$DEST/notes-index.json" "$DEST/.mcp.json"
find "$DEST" -name __pycache__ -type d -prune -exec rm -rf {} +
cp "$HERE/graphifyignore" "$DEST/.graphifyignore"

cd "$DEST"
git init -q -b main
git add -A
git -c user.name=student -c user.email=student@example.com commit -q -m "Deal screener starting point"

echo "==> Installing the /graphify skill into this project only"
"$HERE/.venv/bin/graphify" install --project

echo
echo "Ready. Next:"
echo "  export PATH=\"$HERE/.venv/bin:\$PATH\""
echo "  cd \"$DEST\""
echo "  claude"
