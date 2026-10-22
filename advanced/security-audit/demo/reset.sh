#!/usr/bin/env bash
# Deletes the practice copy and any audit output so you can run the demo again.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rm -rf "$HERE/practice" "$HERE/audit-output"
echo "Removed practice/ and audit-output/"
