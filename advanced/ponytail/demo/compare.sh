#!/usr/bin/env bash
# Compares what the two runs changed: lines added and removed, whether the
# tests pass, and what the new command prints.
# Usage: ./compare.sh [dir] [tracker args...]
#   dir            same dir you gave setup.sh (default: ./practice)
#   tracker args   a command to try in both copies (default: by-category --month 2026-09)
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
dir="${1:-$here/practice}"
shift || true
try=("$@")
[ ${#try[@]} -eq 0 ] && try=(by-category --month 2026-09)

for arm in baseline ponytail; do
  repo="$dir/$arm"
  echo "=================== $arm ==================="
  git -C "$repo" add -A -N -- . ':!.claude'       # count brand-new files too
  echo "--- lines changed (git diff --stat) ---"
  git -C "$repo" diff --stat -- . ':!.claude'
  echo "--- file sizes now (starter: tracker.py 57, test_tracker.py 26) ---"
  (cd "$repo" && wc -l ./*.py)
  echo "--- tests ---"
  (cd "$repo" && python3 -m unittest 2>&1 | tail -n 3)
  echo "--- python3 tracker.py ${try[*]} ---"
  (cd "$repo" && python3 tracker.py "${try[@]}" 2>&1) || true
  echo
done
