#!/usr/bin/env bash
# Copies the Leaky Notes demo app into practice/leaky-notes, makes it a git
# repo, and installs the security-audit skill into THAT folder only
# (project scope: practice/leaky-notes/.claude/skills/security-audit).
# Nothing is installed globally.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRACTICE="$HERE/practice"
TARGET="$PRACTICE/leaky-notes"
SKILLS_CLI_VERSION="1.7.4"

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

# Skip the CLI's anonymous usage telemetry.
export DO_NOT_TRACK=1 DISABLE_TELEMETRY=1
npx -y "skills@$SKILLS_CLI_VERSION" add cloudflare/security-audit-skill \
  --skill security-audit -a claude-code -y --copy

# Keep the installed skill and lock file out of the audited commit.
printf '.claude/\n.agents/\nskills-lock.json\n.venv/\nnotes.db\n__pycache__/\nuploads/\navatars/\n' > .git/info/exclude

echo
echo "Installed skill files:"
ls .claude/skills/security-audit
echo
echo "Next: cd $TARGET && claude"
