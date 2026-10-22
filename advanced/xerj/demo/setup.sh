#!/usr/bin/env bash
# Download the pinned xerj release into ./bin and check its SHA-256 against
# a value written into this script (so a swapped release file is caught too).
# Nothing is installed system-wide. Run from anywhere: paths are relative to this script.
set -euo pipefail

VERSION="1.0.0-rc.98"
DEMO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$DEMO/bin"

case "$(uname -s)-$(uname -m)" in
  Linux-x86_64)
    TARGET="x86_64-unknown-linux-gnu"
    EXPECTED="cd983afbea1d8a54c8762950f064a1d47ba9a06027aa9f8d8c295c803e565ff2" ;;
  Linux-aarch64)
    TARGET="aarch64-unknown-linux-gnu"
    EXPECTED="5bcb82bdc2f92075b6712081ec973a9a317c35411f1e58712f9fefb098c2d04b" ;;
  Darwin-x86_64)
    TARGET="x86_64-apple-darwin"
    EXPECTED="783032546338e8eb4b04817064f5cee66d6a4797247043a42b33898782085146" ;;
  Darwin-arm64)
    TARGET="aarch64-apple-darwin"
    EXPECTED="6373d6a0caaad282a627b2a896c5d708d47c7ead055663c9accf153e6348ea0d" ;;
  *) echo "Unsupported platform $(uname -s)-$(uname -m). On Windows, use WSL." >&2; exit 1 ;;
esac

if [ -x "$BIN/xerj" ] && "$BIN/xerj" --version 2>/dev/null | grep -q "$VERSION"; then
  echo "xerj $VERSION already in $BIN"
  exit 0
fi

FILE="xerj-$VERSION-$TARGET.tar.gz"
URL="https://github.com/xerj-org/xerj/releases/download/v$VERSION/$FILE"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading $FILE ..."
curl -fsSL -o "$TMP/$FILE" "$URL"

if command -v sha256sum >/dev/null; then
  ACTUAL="$(sha256sum "$TMP/$FILE" | awk '{print $1}')"
else
  ACTUAL="$(shasum -a 256 "$TMP/$FILE" | awk '{print $1}')"
fi
if [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "Checksum mismatch: expected $EXPECTED, got $ACTUAL" >&2
  exit 1
fi
echo "Checksum OK"

tar xzf "$TMP/$FILE" -C "$TMP"
mkdir -p "$BIN"
cp "$TMP/xerj-$VERSION-$TARGET/xerj" "$BIN/xerj"
chmod +x "$BIN/xerj"
"$BIN/xerj" --version
