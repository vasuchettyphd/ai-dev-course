#!/usr/bin/env bash
# Start a local xerj node, index a folder, and write playground/.mcp.json for Claude Code.
# Usage: ./start.sh [folder-to-index]   (default: the course's weeks/ folder)
set -euo pipefail

DEMO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XERJ="$DEMO/bin/xerj"
PORT="${XERJ_DEMO_PORT:-19273}"
URL="http://127.0.0.1:$PORT"
CORPUS="$(cd "${1:-$DEMO/../../../weeks}" && pwd)"
PREFIX="course"

# Never let xerj or an agent send field reports from this demo.
export XERJ_DISABLE_FEEDBACK=true

[ -x "$XERJ" ] || { echo "Run ./setup.sh first." >&2; exit 1; }

if curl -fsS "$URL" >/dev/null 2>&1; then
  echo "A node is already answering on $URL"
else
  # xerj claims PORT, PORT+1 and PORT+2.
  for p in "$PORT" $((PORT + 1)) $((PORT + 2)); do
    if (ss -ltn 2>/dev/null || netstat -an 2>/dev/null) | grep -q "[:.]$p "; then
      echo "Port $p is busy. Pick another with: XERJ_DEMO_PORT=<port> ./start.sh" >&2
      exit 1
    fi
  done
  echo "Starting xerj on $URL (no auth, loopback only) ..."
  nohup "$XERJ" --insecure --port "$PORT" --data-dir "$DEMO/.xerj-data" \
    > "$DEMO/xerj.log" 2>&1 &
  echo $! > "$DEMO/xerj.pid"
  for _ in $(seq 1 60); do
    curl -fsS "$URL" >/dev/null 2>&1 && break
    sleep 1
  done
  curl -fsS "$URL" >/dev/null || { echo "xerj did not start; see $DEMO/xerj.log" >&2; exit 1; }
fi

echo "Indexing $CORPUS as prefix '$PREFIX' ..."
"$XERJ" autoindex "$CORPUS" --url "$URL" --prefix "$PREFIX" \
  --state-dir "$DEMO/.xerj-state" --replace-prefix

mkdir -p "$DEMO/playground"
cat > "$DEMO/playground/.mcp.json" <<EOF
{
  "mcpServers": {
    "xerj": {
      "command": "$XERJ",
      "args": ["mcp"],
      "env": { "XERJ_URL": "$URL", "XERJ_DISABLE_FEEDBACK": "true" }
    }
  }
}
EOF
echo "Wrote $DEMO/playground/.mcp.json"
echo "Next: cd $DEMO/playground && claude"
