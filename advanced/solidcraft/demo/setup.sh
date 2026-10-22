#!/usr/bin/env bash
# Set up the SolidCraft demo, without installing anything system-wide.
#
# 1. Downloads the pinned SolidCraft release (the solidcraft-cli program) into ./bin
#    and checks its SHA-256 against the value pinned below (and the release's
#    SHA256SUMS.txt) before unpacking it.
# 2. Makes a practice folder (./practice) with:
#      .claude/skills/solidcraft-*   the four upstream agent skills, from the same release tag
#      .mcp.json                     tells Claude Code how to start the SolidCraft MCP server
#      out/                          where Claude saves exports and pictures
#
# Run it from anywhere: demo/setup.sh   (run it again to start the practice folder fresh)
# Optional: SOLIDCRAFT_BIN_DIR and SOLIDCRAFT_PRACTICE move the two folders somewhere else.
# Safety: the script only ever deletes a practice folder that it made itself (it leaves
# a .solidcraft-practice marker file inside). Any other existing folder is left alone.
set -euo pipefail

VERSION="0.19.0"
REPO="tangency-labs/solidcraft"
BASE="https://github.com/$REPO/releases/download/v$VERSION"
DEMO_DIR="$(cd "$(dirname "$0")" && pwd)"
BIN_DIR="${SOLIDCRAFT_BIN_DIR:-$DEMO_DIR/bin}"
PRACTICE="${SOLIDCRAFT_PRACTICE:-$DEMO_DIR/practice}"
MARKER=".solidcraft-practice"

# Temporary folders, removed when the script ends (even if it fails).
TMP=""
SRC=""
cleanup() { rm -rf "$TMP" "$SRC"; }
trap cleanup EXIT

case "$(uname -s)-$(uname -m)" in
  # SHA256 values copied from the v0.19.0 release, checked against a fresh download.
  Linux-x86_64)
    ASSET="solidcraft-$VERSION-linux-x86_64.tar.gz"
    SHA256="1e3650237a617667f557a16e865bbf544b20ece1dec39f7c380239d7058d632d" ;;
  Linux-aarch64|Linux-arm64)
    ASSET="solidcraft-$VERSION-linux-aarch64.tar.gz"
    SHA256="109a495c3a6049edd790304f5bd6abbd0abd79063120adf3847ca9c305f375c6" ;;
  Darwin-*)
    ASSET="solidcraft-cli-$VERSION-macos-universal.zip"
    SHA256="e9ec50c3a838336feeffd7028dc2594fef791cdfee3ccbf5cbf235f78ba88245" ;;
  *) echo "Unsupported system: $(uname -s) $(uname -m). On Windows, use WSL." >&2; exit 1 ;;
esac

for tool in curl git; do
  command -v "$tool" >/dev/null || { echo "Please install $tool first." >&2; exit 1; }
done

if [ -x "$BIN_DIR/solidcraft-cli" ] && "$BIN_DIR/solidcraft-cli" --version | grep -q " $VERSION\$"; then
  echo "solidcraft-cli $VERSION is already in $BIN_DIR"
else
  TMP="$(mktemp -d)"
  echo "Downloading $ASSET (about 60 MB) ..."
  curl -fsSL -o "$TMP/$ASSET" "$BASE/$ASSET"
  curl -fsSL -o "$TMP/SHA256SUMS.txt" "$BASE/SHA256SUMS.txt"

  echo "Checking the download's SHA-256 checksum ..."
  LISTED="$(awk -v f="$ASSET" '$2 == f {print $1}' "$TMP/SHA256SUMS.txt" | head -n 1)"
  if command -v sha256sum >/dev/null; then
    ACTUAL="$(sha256sum "$TMP/$ASSET" | awk '{print $1}')"
  else
    ACTUAL="$(shasum -a 256 "$TMP/$ASSET" | awk '{print $1}')"
  fi
  # Must match the value pinned in this script AND the release's own list.
  if [ "$ACTUAL" != "$SHA256" ] || [ "$LISTED" != "$SHA256" ]; then
    echo "Checksum mismatch for $ASSET - not installing." >&2
    echo "  expected (pinned): $SHA256" >&2
    echo "  SHA256SUMS.txt:    ${LISTED:-not listed}" >&2
    echo "  downloaded file:   $ACTUAL" >&2
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

if [ -e "$PRACTICE" ] && [ ! -f "$PRACTICE/$MARKER" ]; then
  echo "$PRACTICE already exists, and this script did not make it, so it will not touch it." >&2
  echo "To start fresh, look inside it, delete it yourself if you don't need it, and run demo/setup.sh again." >&2
  echo "Or pick another folder: SOLIDCRAFT_PRACTICE=/some/new/folder demo/setup.sh" >&2
  exit 1
fi

# Fetch the four skills before touching the practice folder, so a failed
# download leaves the old one as it was.
SRC="$(mktemp -d)"
git -c advice.detachedHead=false clone -q --depth 1 --branch "v$VERSION" "https://github.com/$REPO" "$SRC/solidcraft"

echo "Making a fresh practice folder in $PRACTICE ..."
rm -rf "$PRACTICE"   # safe: it is either missing or has our marker file
mkdir -p "$PRACTICE/.claude/skills" "$PRACTICE/out"
echo "Made by advanced/solidcraft/demo/setup.sh. Running setup.sh again deletes this folder." > "$PRACTICE/$MARKER"
cp -R "$SRC/solidcraft/skills/"solidcraft-* "$PRACTICE/.claude/skills/"

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
