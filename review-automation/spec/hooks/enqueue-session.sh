#!/usr/bin/env bash
# L1: SessionEnd hook - enqueue job spec and exit. <1s, no LLM, no network.
# Atomic write: tmp + rename (I1). Not applicable (no repo / unborn branch) => silent no-op.
# Deps: git, python3 (both base Fedora). Deliberately NO jq.
set -euo pipefail

QUEUE="${REVIEW_QUEUE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/review-queue}"
repo=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
branch=$(git -C "$repo" rev-parse --abbrev-ref HEAD 2>/dev/null) || exit 0
[ "$branch" = "HEAD" ] && exit 0   # detached head: nothing to dossier

# Q2 decision: issue ref from branch naming, e.g. fix/ISSUE-123-desc or feat/456-desc
issue=$(grep -oE '[A-Za-z]+-[0-9]+|/[0-9]+' <<< "$branch" | head -1 | tr -d '/' || true)

mkdir -p "$QUEUE"
ts=$(date -u +%Y%m%dT%H%M%SZ)
tmp=$(mktemp "$QUEUE/.tmp.XXXXXX")
python3 - "$repo" "$branch" "${issue:-}" "${CLAUDE_SESSION_ID:-}" > "$tmp" << 'PY'
import json, sys, datetime
repo, branch, issue, sid = sys.argv[1:5]
spec = {"version": 1, "type": "dossier", "repo": repo, "branch": branch,
        "issue_refs": [issue] if issue else [],
        "trigger": "session_end",
        "created_at": datetime.datetime.now(datetime.timezone.utc)
                      .strftime("%Y-%m-%dT%H:%M:%SZ")}
if sid:
    spec["session_id"] = sid
print(json.dumps(spec))
PY
mv -f "$tmp" "$QUEUE/dossier-${branch//\//_}-${ts}.json"
