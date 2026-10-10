#!/usr/bin/env bash
# Load the 12 tasks from starter/PLAN.md into beads, with their dependencies.
# Run it inside a practice project made with: scripts/new-practice.sh <name> --beads
# This is the fallback for Exercise 2. The exercise asks the agent to do it first.
set -euo pipefail

command -v bd >/dev/null || { echo "bd is not on PATH. Run scripts/install-bd.sh first." >&2; exit 1; }
[ -d .beads ] || { echo "No .beads/ here. Run this inside a practice project after bd init." >&2; exit 1; }

EPIC=$(bd q "Build wordstats (see PLAN.md)" -t epic -p 1)

T1=$(bd q "1. CLI skeleton with argparse"                 --parent "$EPIC" -p 1)
T2=$(bd q "2. Read files as UTF-8; missing file exits 2"  --parent "$EPIC" -p 1)
T3=$(bd q "3. Tokenizer"                                  --parent "$EPIC" -p 1)
T4=$(bd q "4. Basic counts: lines, words, characters"     --parent "$EPIC" -p 1)
T5=$(bd q "5. --top N most common words"                  --parent "$EPIC" -p 2)
T6=$(bd q "6. --no-stopwords"                             --parent "$EPIC" -p 2)
T7=$(bd q "7. Table output (default)"                     --parent "$EPIC" -p 2)
T8=$(bd q "8. --json output"                              --parent "$EPIC" -p 2)
T9=$(bd q "9. Several files plus TOTAL section"           --parent "$EPIC" -p 2)
T10=$(bd q "10. Read stdin when the file name is -"       --parent "$EPIC" -p 2)
T11=$(bd q "11. --min-length N"                           --parent "$EPIC" -p 3)
T12=$(bd q "12. README with usage examples"               --parent "$EPIC" -p 3)

# bd dep add <issue> <depends-on>
bd dep add "$T2" "$T1"
bd dep add "$T4" "$T2";  bd dep add "$T4" "$T3"
bd dep add "$T5" "$T4"
bd dep add "$T6" "$T3"
bd dep add "$T7" "$T4"
bd dep add "$T8" "$T4"
bd dep add "$T9" "$T7"
bd dep add "$T10" "$T2"
bd dep add "$T11" "$T3"
for T in "$T5" "$T6" "$T8" "$T9" "$T10" "$T11"; do bd dep add "$T12" "$T"; done

echo
bd ready
