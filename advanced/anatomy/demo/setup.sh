#!/usr/bin/env bash
# Make a practice project with the Anatomy skill installed for that project only.
# Usage: demo/setup.sh [folder]   (default: advanced/anatomy/practice/skill-figure)
# Set ANATOMY_REF=main to try the newest upstream version instead of the tested one.
set -euo pipefail

TESTED_COMMIT="1482e8469b0a9e0d8cc18ea2740a01423d29ae80"
REF="${ANATOMY_REF:-$TESTED_COMMIT}"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON="$(dirname "$HERE")"
TARGET="${1:-$LESSON/practice/skill-figure}"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing: $1. $2" >&2; exit 1; }; }
need node "Install Node.js 22 LTS from https://nodejs.org"
need git "Install git from https://git-scm.com"

if ! node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>20||(a===20&&b>=10)?0:1)'; then
  echo "Node $(node --version) found. Anatomy needs Node 20.10 or later." >&2
  exit 1
fi

if [ -e "$TARGET" ]; then
  echo "$TARGET already exists. Delete it first, or pass another folder name." >&2
  exit 1
fi

mkdir -p "$TARGET"
cd "$TARGET"
git init -q
cp "$HERE/brief.md" brief.md

# Project install: the skill lands in ./.claude/skills/anatomy, nowhere else.
git clone -q https://github.com/wheresryan22/anatomy.git .claude/skills/anatomy
git -C .claude/skills/anatomy checkout -q "$REF"
echo "anatomy at $(git -C .claude/skills/anatomy rev-parse --short HEAD)"

echo
echo "Ready: $TARGET"
echo "Skill installed at: $TARGET/.claude/skills/anatomy/SKILL.md"
echo "Next: cd \"$TARGET\" && claude"
