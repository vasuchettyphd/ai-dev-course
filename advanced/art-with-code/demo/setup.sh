#!/usr/bin/env bash
# Makes two empty practice folders for the with-and-without exercise:
#   <dir>/plain       - plain Claude Code, no extra skills
#   <dir>/with-skill  - the same, plus the antialgorithm skill installed for this folder only
# Usage: ./setup.sh [dir]   (default: ./practice, which git ignores)
set -euo pipefail

# The tested commit of https://github.com/mankidev/antialgorithm. Pinning it means the skill cannot change under us.
SKILL_COMMIT="766e30411195a9198afad38f3d76e08701ed4516"
SKILL_REPO="https://github.com/mankidev/antialgorithm.git"

here="$(cd "$(dirname "$0")" && pwd)"
dir="${1:-$here/practice}"

if ! command -v git >/dev/null 2>&1; then
  echo "git is not installed. Install it first (see week 3), then run this again." >&2
  exit 1
fi

if [ -e "$dir/plain" ] || [ -e "$dir/with-skill" ]; then
  echo "$dir already has plain/ or with-skill/. Delete them first: rm -rf \"$dir/plain\" \"$dir/with-skill\"" >&2
  exit 1
fi

# Download the exact commit into a temporary folder first, so a failed download leaves nothing behind.
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
if ! git -C "$tmp" init -q \
   || ! git -C "$tmp" fetch -q --depth 1 "$SKILL_REPO" "$SKILL_COMMIT" \
   || ! git -C "$tmp" -c advice.detachedHead=false checkout -q FETCH_HEAD; then
  echo "Could not download antialgorithm commit ${SKILL_COMMIT:0:7}. Check your internet connection and try again. If it keeps failing, that commit may have been removed upstream: tell your instructor." >&2
  exit 1
fi
if [ "$(git -C "$tmp" rev-parse HEAD)" != "$SKILL_COMMIT" ]; then
  echo "Downloaded the wrong antialgorithm version. Not installing it." >&2
  exit 1
fi
rm -rf "$tmp/.git" "$tmp/images"

mkdir -p "$dir/plain" "$dir/with-skill/.claude/skills"
# Project-scoped install: only Claude Code sessions started inside with-skill/ see the skill.
mv "$tmp" "$dir/with-skill/.claude/skills/antialgorithm"
trap - EXIT

echo "Ready:"
echo "  $dir/plain        (no skill)"
echo "  $dir/with-skill   (antialgorithm ${SKILL_COMMIT:0:7} in .claude/skills/antialgorithm/)"
