#!/usr/bin/env bash
# Sends the same feature request to both copies, headless, one after the other.
# The ponytail copy gets the request with "/ponytail " in front, which loads the skill.
# Usage: ./run-both.sh [dir] [request-file]
#   dir           same dir you gave setup.sh (default: ./practice)
#   request-file  default: requests/1-by-category.txt
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
request="$(cat "${2:-$here/requests/1-by-category.txt}")"
# Absolute path, because run() cds into each copy before writing its result file.
dir="$(cd "${1:-$here/practice}" && pwd)"

# --setting-sources project: ignore your own plugins and hooks, so the only
# difference between the two runs is the ponytail skill.
run() {
  (cd "$dir/$1" && claude -p "$2" \
    --model sonnet \
    --permission-mode acceptEdits \
    --allowedTools "Bash(python3:*)" \
    --setting-sources project \
    --output-format json > "$dir/$1.result.json")
  python3 - "$dir/$1.result.json" "$1" <<'PY'
import json, sys
r = json.load(open(sys.argv[1]))
print(f"{sys.argv[2]}: ${r['total_cost_usd']:.2f}, {r['num_turns']} turns, {r['duration_ms'] / 1000:.0f}s")
PY
}

run baseline "$request"
run ponytail "/ponytail $request"
