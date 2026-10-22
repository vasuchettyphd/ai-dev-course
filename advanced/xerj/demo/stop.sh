#!/usr/bin/env bash
# Stop the xerj node started by start.sh. Add --clean to also delete the index and the binary.
set -euo pipefail

DEMO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$DEMO/xerj.pid" ]; then
  PID="$(cat "$DEMO/xerj.pid")"
  if kill "$PID" 2>/dev/null; then
    # Wait for it to finish flushing its data before anything is deleted.
    for _ in $(seq 1 30); do
      kill -0 "$PID" 2>/dev/null || break
      sleep 0.5
    done
    echo "Stopped xerj (pid $PID)"
  else
    echo "xerj (pid $PID) was not running"
  fi
  rm -f "$DEMO/xerj.pid"
else
  echo "No xerj.pid found; nothing to stop"
fi

if [ "${1:-}" = "--clean" ]; then
  rm -rf "$DEMO/bin" "$DEMO/.xerj-data" "$DEMO/.xerj-state" "$DEMO/playground" "$DEMO/xerj.log"
  echo "Removed bin/, .xerj-data/, .xerj-state/, playground/ and xerj.log"
fi
