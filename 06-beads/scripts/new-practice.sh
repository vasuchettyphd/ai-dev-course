#!/usr/bin/env bash
# Copy the starter project into practice/<name> as its own git repo.
#   scripts/new-practice.sh <name>            # plain copy, for the plan.md-only run
#   scripts/new-practice.sh <name> --beads    # also runs bd init (needs bd on PATH)
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <name> [--beads]" >&2
  exit 1
fi

NAME="$1"
WITH_BEADS="${2:-}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$REPO_ROOT/practice/$NAME"

if [ -e "$DEST" ]; then
  echo "$DEST already exists. Pick another name or delete it first." >&2
  exit 1
fi

if [ "$WITH_BEADS" = "--beads" ] && ! command -v bd >/dev/null; then
  echo "bd is not on PATH. Run scripts/install-bd.sh, then: export PATH=\"$REPO_ROOT/bin:\$PATH\"" >&2
  exit 1
fi

mkdir -p "$REPO_ROOT/practice"
cp -R "$REPO_ROOT/starter" "$DEST"
cd "$DEST"
git init -q -b main
git add -A
git commit -q -m "Starter project"

if [ "$WITH_BEADS" = "--beads" ]; then
  bd init --non-interactive --prefix ws
fi

echo
echo "Ready: $DEST"
