#!/usr/bin/env bash
# Makes two identical copies of the starter project, each its own git repo:
#   <dir>/baseline  - plain Claude Code
#   <dir>/ponytail  - the same, plus the ponytail skill installed for this project only
# Usage: ./setup.sh [dir]   (default: ./practice, which git ignores)
set -euo pipefail

PONYTAIL_TAG="v5.3.2"
# The commit tag v5.3.2 points to. Pinning the commit means the file cannot change under us.
PONYTAIL_COMMIT="16352ac229eb08a9598dcae48fe9f2b342567d86"
SKILL_SHA256="9badd22a32e19cb884e46dfa8d3aae82bb81dfa5484105b8b4f0262df823a509"
SKILL_URL="https://raw.githubusercontent.com/DietrichGebert/ponytail/${PONYTAIL_COMMIT}/skills/ponytail/SKILL.md"

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
skill="$dir/ponytail/.claude/skills/ponytail/SKILL.md"
curl -fsSL "$SKILL_URL" -o "$skill"
if ! echo "$SKILL_SHA256  $skill" | sha256sum -c --status - 2>/dev/null \
   && ! echo "$SKILL_SHA256  $skill" | shasum -a 256 -c --status - 2>/dev/null; then
  rm -f "$skill"
  echo "SKILL.md checksum did not match. Not installing it." >&2
  exit 1
fi

echo "Ready:"
echo "  $dir/baseline   (no skill)"
echo "  $dir/ponytail   (ponytail ${PONYTAIL_TAG} in .claude/skills/ponytail/SKILL.md)"
