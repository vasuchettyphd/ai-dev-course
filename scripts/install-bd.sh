#!/usr/bin/env bash
# Install the pinned beads (bd) release into ./bin of this repo.
# Nothing is installed system-wide. The download is checked against the
# release's checksums.txt before anything is extracted.
set -euo pipefail

VERSION="1.3.1"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="$REPO_ROOT/bin"

case "$(uname -s)" in
  Linux)  OS=linux ;;
  Darwin) OS=darwin ;;
  *) echo "Unsupported OS: $(uname -s). On Windows, use WSL." >&2; exit 1 ;;
esac

case "$(uname -m)" in
  x86_64|amd64) ARCH=amd64 ;;
  arm64|aarch64) ARCH=arm64 ;;
  *) echo "Unsupported CPU: $(uname -m)" >&2; exit 1 ;;
esac

ASSET="beads_${VERSION}_${OS}_${ARCH}.tar.gz"
BASE="https://github.com/gastownhall/beads/releases/download/v${VERSION}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading $ASSET ..."
curl -fsSL -o "$TMP/$ASSET" "$BASE/$ASSET"
curl -fsSL -o "$TMP/checksums.txt" "$BASE/checksums.txt"

echo "Verifying checksum ..."
EXPECTED="$(grep " $ASSET\$" "$TMP/checksums.txt" | awk '{print $1}')"
if command -v sha256sum >/dev/null; then
  ACTUAL="$(sha256sum "$TMP/$ASSET" | awk '{print $1}')"
else
  ACTUAL="$(shasum -a 256 "$TMP/$ASSET" | awk '{print $1}')"
fi
if [ -z "$EXPECTED" ] || [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "Checksum mismatch for $ASSET. Not installing." >&2
  exit 1
fi

mkdir -p "$BIN_DIR"
tar -xzf "$TMP/$ASSET" -C "$TMP" bd
mv -f "$TMP/bd" "$BIN_DIR/bd"
chmod +x "$BIN_DIR/bd"

echo
"$BIN_DIR/bd" version
echo
echo "Installed to $BIN_DIR/bd. Add it to your PATH for this shell:"
echo "  export PATH=\"$BIN_DIR:\$PATH\""
