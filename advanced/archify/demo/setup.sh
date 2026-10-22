#!/usr/bin/env bash
# Make a practice copy of the course's deal screener and install Archify into it.
#   demo/setup.sh                # practice copy goes in demo/practice/deal-screener
#   demo/setup.sh <folder>       # or anywhere you like
# Archify is installed for this one project only (.claude/skills/archify),
# not for your whole computer. Nothing outside the practice folder changes.
set -euo pipefail

# The Archify commit this lesson was tested with (release 3.2.0 plus fixes).
ARCHIFY_REPO="https://github.com/tt-a1i/archify.git"
ARCHIFY_COMMIT="25cf37080fc8b1dbe758a4efc3935b55f3327083"
SKILLS_CLI="skills@1.7.4"

DEMO_DIR="$(cd "$(dirname "$0")" && pwd)"
COURSE_ROOT="$(cd "$DEMO_DIR/../../.." && pwd)"
SOURCE="$COURSE_ROOT/example-project"
DEST="${1:-$DEMO_DIR/practice/deal-screener}"

if [ ! -d "$SOURCE/dealscreener" ]; then
  echo "Can't find the deal screener at $SOURCE" >&2
  exit 1
fi
if [ -e "$DEST" ]; then
  echo "$DEST already exists. Delete it first (rm -rf \"$DEST\") or pick another folder." >&2
  exit 1
fi
command -v node >/dev/null || { echo "Node.js 22.20 or later is needed (node --version)." >&2; exit 1; }
if ! node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>22||(a===22&&b>=20)?0:1)'; then
  echo "Node $(node --version) found. The skills installer needs Node.js 22.20 or later." >&2
  exit 1
fi
command -v git >/dev/null || { echo "git is needed." >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "1/4 Copying the deal screener to $DEST"
mkdir -p "$DEST"
# Copy everything except secrets (.env files) and caches, then put back the
# harmless .env.example template.
tar -C "$SOURCE" --exclude='.env*' --exclude='__pycache__' --exclude='.venv' -cf - . | tar -C "$DEST" -xf -
if [ -f "$SOURCE/.env.example" ]; then cp "$SOURCE/.env.example" "$DEST/.env.example"; fi

echo "2/4 Making it a git repo (Archify cites code by commit)"
cd "$DEST"
git init -q
git add -A
git -c user.name="Archify Demo" -c user.email="demo@example.com" commit -q -m "Deal screener snapshot for the Archify demo"
# Archify only attaches source citations when the repo has a remote address.
# example.com is reserved for examples; nothing is ever pushed to it.
git remote add origin https://example.com/deal-screener.git

echo "3/4 Downloading the tested Archify version (only its skill folder, about 18 MB)"
git -C "$TMP" init -q upstream
git -C "$TMP/upstream" remote add origin "$ARCHIFY_REPO"
git -C "$TMP/upstream" fetch -q --depth 1 --filter=blob:none origin "$ARCHIFY_COMMIT"
git -C "$TMP/upstream" sparse-checkout set --no-cone /archify/
git -C "$TMP/upstream" checkout -q FETCH_HEAD

echo "4/4 Installing the archify skill into this project only"
DO_NOT_TRACK=1 npx -y "$SKILLS_CLI" add "$TMP/upstream" --skill archify --agent claude-code --copy -y >/dev/null
# Keep the installed skill out of git status, so the repo stays "clean".
printf '.claude/skills/\nskills-lock.json\n.archify/\n' >> .git/info/exclude
node .claude/skills/archify/bin/archify.mjs doctor | tail -1

echo
echo "Done. Next:"
echo "  cd \"$DEST\""
echo "  export ARCHIFY_UPDATE_CHECK_DISABLED=1   # optional: skip Archify's daily update check"
echo "  claude"
