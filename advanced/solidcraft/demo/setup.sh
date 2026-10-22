#!/usr/bin/env bash
# Set up the SolidCraft demo, without installing anything system-wide.
#
# 1. Downloads the pinned SolidCraft release (the solidcraft-cli program) into ./bin
#    and checks it against the release's SHA256SUMS.txt before unpacking it.
# 2. Makes a practice folder (./practice) with:
#      .claude/skills/solidcraft-*   the four upstream agent skills, from the same release tag
#      .mcp.json                     tells Claude Code how to start the SolidCraft MCP server
#      out/                          where Claude saves exports and pictures
#
# Run it from anywhere: demo/setup.sh   (run it again to start the practice folder fresh)
# Optional: SOLIDCRAFT_BIN_DIR and SOLIDCRAFT_PRACTICE move the two folders somewhere else.
set -euo pipefail

VERSION="0.19.0"
REPO="tangency-labs/solidcraft"
BASE="https://github.com/$REPO/releases/download/v$VERSION"
DEMO_DIR="$(cd "$(dirname "$0")" && pwd)"
BIN_DIR="${SOLIDCRAFT_BIN_DIR:-$DEMO_DIR/bin}"
PRACTICE="${SOLIDCRAFT_PRACTICE:-$DEMO_DIR/practice}"

case "$(uname -s)-$(uname -m)" in
  Linux-x86_64)            ASSET="solidcraft-$VERSION-linux-x86_64.tar.gz" ;;
  Linux-aarch64|Linux-arm64) ASSET="solidcraft-$VERSION-linux-aarch64.tar.gz" ;;
  Darwin-*)                ASSET="solidcraft-cli-$VERSION-macos-universal.zip" ;;
  *) echo "Unsupported system: $(uname -s) $(uname -m). On Windows, use WSL." >&2; exit 1 ;;
esac

for tool in curl git; do
  command -v "$tool" >/dev/null || { echo "Please install $tool first." >&2; exit 1; }
done

if [ -x "$BIN_DIR/solidcraft-cli" ] && "$BIN_DIR/solidcraft-cli" --version | grep -q " $VERSION\$"; then
  echo "solidcraft-cli $VERSION is already in $BIN_DIR"
else
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  echo "Downloading $ASSET (about 60 MB) ..."
  curl -fsSL -o "$TMP/$ASSET" "$BASE/$ASSET"
  curl -fsSL -o "$TMP/SHA256SUMS.txt" "$BASE/SHA256SUMS.txt"

  echo "Checking the download against SHA256SUMS.txt ..."
  EXPECTED="$(awk -v f="$ASSET" '$2 == f {print $1}' "$TMP/SHA256SUMS.txt")"
  if command -v sha256sum >/dev/null; then
    ACTUAL="$(sha256sum "$TMP/$ASSET" | awk '{print $1}')"
  else
    ACTUAL="$(shasum -a 256 "$TMP/$ASSET" | awk '{print $1}')"
  fi
  if [ -z "$EXPECTED" ] || [ "$EXPECTED" != "$ACTUAL" ]; then
    echo "Checksum mismatch for $ASSET - not installing." >&2
    exit 1
  fi
  echo "Checksum OK."

  mkdir -p "$TMP/x" "$BIN_DIR"
  case "$ASSET" in
    *.tar.gz) tar -xzf "$TMP/$ASSET" -C "$TMP/x" ;;
    *.zip)    (cd "$TMP/x" && unzip -q "$TMP/$ASSET") ;;
  esac
  # The CLI is the only program the demo needs (the desktop app is optional).
  find "$TMP/x" -type f -name solidcraft-cli -exec cp {} "$BIN_DIR/" \;
  chmod +x "$BIN_DIR/solidcraft-cli"
  if [ "$(uname -s)" = Darwin ]; then
    # The download isn't signed yet; clear the quarantine flag so macOS will run it.
    xattr -d com.apple.quarantine "$BIN_DIR/solidcraft-cli" 2>/dev/null || true
  fi
fi
"$BIN_DIR/solidcraft-cli" --version

echo "Making a fresh practice folder in $PRACTICE ..."
rm -rf "$PRACTICE"
mkdir -p "$PRACTICE/.claude/skills" "$PRACTICE/out"

SRC="$(mktemp -d)"
git clone -q --depth 1 --branch "v$VERSION" "https://github.com/$REPO" "$SRC/solidcraft" 2>/dev/null
cp -R "$SRC/solidcraft/skills/"solidcraft-* "$PRACTICE/.claude/skills/"
rm -rf "$SRC"

cat > "$PRACTICE/.mcp.json" <<EOF
{
  "mcpServers": {
    "solidcraft": {
      "command": "$BIN_DIR/solidcraft-cli",
      "args": ["mcp", "--allow-path", "$PRACTICE/out"]
    }
  }
}
EOF

echo
echo "Skills installed for this folder only:"
ls "$PRACTICE/.claude/skills"
echo
echo "Ready. Next:"
echo "  cd $PRACTICE"
echo "  claude"
