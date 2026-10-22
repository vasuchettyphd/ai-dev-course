#!/usr/bin/env bash
# Make a practice copy of the course's deal screener and install Archify into it.
#   demo/setup.sh                # practice copy goes in demo/practice/deal-screener
#   demo/setup.sh <folder>       # or anywhere you like
# Archify is installed for this one project only (.claude/skills/archify),
# not for your whole computer. Nothing outside the practice folder changes.
set -euo pipefail

ARCHIFY_REF="tt-a1i/archify"
SKILLS_CLI="skills@1.7.0"

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
command -v node >/dev/null || { echo "Node.js 18 or newer is needed (node --version)." >&2; exit 1; }
command -v git  >/dev/null || { echo "git is needed." >&2; exit 1; }

echo "1/3 Copying the deal screener to $DEST"
mkdir -p "$DEST"
# Copy everything except secrets and caches.
tar -C "$SOURCE" --exclude='.env' --exclude='__pycache__' --exclude='.venv' -cf - . | tar -C "$DEST" -xf -

echo "2/3 Making it a git repo (Archify cites code by commit)"
cd "$DEST"
git init -q
git add -A
git -c user.name="Archify Demo" -c user.email="demo@example.com" commit -q -m "Deal screener snapshot for the Archify demo"
# Archify only attaches source citations when the repo has a remote address.
# This one is a placeholder name, not a real repo; nothing is ever pushed to it.
git remote add origin https://github.com/example/deal-screener.git

echo "3/3 Installing the archify skill into this project only"
DO_NOT_TRACK=1 npx -y "$SKILLS_CLI" add "$ARCHIFY_REF" --skill archify --agent claude-code --copy -y >/dev/null
# Keep the installed skill out of git status, so the repo stays "clean".
printf '.claude/skills/\nskills-lock.json\n.archify/\n' >> .git/info/exclude
node .claude/skills/archify/bin/archify.mjs doctor | tail -1

echo
echo "Done. Next:"
echo "  cd \"$DEST\""
echo "  claude"
