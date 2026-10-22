#!/usr/bin/env bash
# Makes two identical copies of the starter project, each its own git repo:
#   <dir>/baseline  - plain Claude Code
#   <dir>/ponytail  - the same, plus the ponytail skill installed for this project only
# Usage: ./setup.sh [dir]   (default: ./practice, which git ignores)
set -euo pipefail

PONYTAIL_TAG="v5.3.2"
SKILL_URL="https://raw.githubusercontent.com/DietrichGebert/ponytail/${PONYTAIL_TAG}/skills/ponytail/SKILL.md"

here="$(cd "$(dirname "$0")" && pwd)"
dir="${1:-$here/practice}"

if [ -e "$dir/baseline" ] || [ -e "$dir/ponytail" ]; then
  echo "$dir already has baseline/ or ponytail/. Delete them first: rm -rf \"$dir\"" >&2
  exit 1
fi

for arm in baseline ponytail; do
  mkdir -p "$dir/$arm"
  cp "$here"/starter/*.py "$here"/starter/*.csv "$dir/$arm/"
  printf '__pycache__/\n' > "$dir/$arm/.gitignore"
  git -C "$dir/$arm" init -q
  git -C "$dir/$arm" add -A
  git -C "$dir/$arm" -c user.name=student -c user.email=student@example.com commit -qm "starter"
done

# Project-scoped install: only Claude Code sessions started inside ponytail/ see the skill.
mkdir -p "$dir/ponytail/.claude/skills/ponytail"
curl -fsSL "$SKILL_URL" -o "$dir/ponytail/.claude/skills/ponytail/SKILL.md"

echo "Ready:"
echo "  $dir/baseline   (no skill)"
echo "  $dir/ponytail   (ponytail ${PONYTAIL_TAG} in .claude/skills/ponytail/SKILL.md)"
