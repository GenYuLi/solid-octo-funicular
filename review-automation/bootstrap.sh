#!/usr/bin/env bash
# One-shot repo bootstrap. Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")"
[ -d .git ] || git init -q -b main
git add -A
git commit -q -m "v0 spec package (requirements v0.7)" 2>/dev/null \
  || echo "nothing new to commit"
echo "repo ready: $(pwd)"
echo "next: open a Claude Code session here — NOW.md has the task queue."
