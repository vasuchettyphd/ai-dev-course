#!/usr/bin/env bash
# Copies the Leaky Notes demo app into practice/leaky-notes, makes it a git
# repo, and installs the security-audit skill into THAT folder only
# (project scope: practice/leaky-notes/.claude/skills/security-audit).
# Nothing is installed globally.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRACTICE="$HERE/practice"
TARGET="$PRACTICE/leaky-notes"

if [ -e "$TARGET" ]; then
  echo "practice/leaky-notes already exists. Run ./reset.sh first to start over." >&2
  exit 1
fi

mkdir -p "$PRACTICE"
cp -R "$HERE/leaky-notes" "$TARGET"
cd "$TARGET"
git init -q
git add .
git -c user.name="Demo Student" -c user.email="student@example.com" commit -q -m "Leaky Notes demo app (deliberately vulnerable)"
echo "Created git repo at $TARGET"

# Fetch the skill at the exact commit this lesson was tested with, then copy
# it into the project. A shallow fetch of one commit keeps the download small.
SKILL_REPO="https://github.com/cloudflare/security-audit-skill.git"
SKILL_COMMIT="c1c8a8c1471069fb0e188eeaff69b8e8db6564a8"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git -C "$TMP" init -q
git -C "$TMP" fetch -q --depth 1 "$SKILL_REPO" "$SKILL_COMMIT"
git -C "$TMP" checkout -q FETCH_HEAD
mkdir -p .claude/skills
cp -R "$TMP/skills/security-audit" .claude/skills/security-audit
echo "Installed security-audit skill at commit ${SKILL_COMMIT:0:7}"

# Keep the installed skill and runtime files out of the audited commit.
printf '.claude/\n.venv/\nnotes.db\n__pycache__/\nuploads/\navatars/\n' > .git/info/exclude

echo
echo "Installed skill files:"
ls .claude/skills/security-audit
echo
echo "Next: cd $TARGET && claude"
