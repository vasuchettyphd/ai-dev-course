#!/usr/bin/env bash
# Makes two empty practice folders for the with-and-without exercise:
#   <dir>/plain       - plain Claude Code, no extra skills
#   <dir>/with-skill  - the same, plus the antialgorithm skill installed for this folder only
# Usage: ./setup.sh [dir]   (default: ./practice, which git ignores)
set -euo pipefail

# The tested commit of https://github.com/mankidev/antialgorithm. Pinning it means the skill cannot change under us.
SKILL_COMMIT="766e30411195a9198afad38f3d76e08701ed4516"

here="$(cd "$(dirname "$0")" && pwd)"
dir="${1:-$here/practice}"

if [ -e "$dir/plain" ] || [ -e "$dir/with-skill" ]; then
  echo "$dir already has plain/ or with-skill/. Delete them first: rm -rf \"$dir\"" >&2
  exit 1
fi

mkdir -p "$dir/plain" "$dir/with-skill/.claude/skills"

# Project-scoped install: only Claude Code sessions started inside with-skill/ see the skill.
skill="$dir/with-skill/.claude/skills/antialgorithm"
git clone -q https://github.com/mankidev/antialgorithm.git "$skill"
git -C "$skill" -c advice.detachedHead=false checkout -q "$SKILL_COMMIT"
rm -rf "$skill/.git" "$skill/images"

echo "Ready:"
echo "  $dir/plain        (no skill)"
echo "  $dir/with-skill   (antialgorithm ${SKILL_COMMIT:0:7} in .claude/skills/antialgorithm/)"
