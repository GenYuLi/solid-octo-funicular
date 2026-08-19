# tier1-brief prompt — prompt_version: 1
<!-- I5: bump on any change; cache key includes it (C5). Backend: claude -p
     from an empty dir (Q6 / I8 clean-context). -->

## Task
You turn a Tier 0 triage payload into an issue brief. Output ONLY one JSON
object conforming to brief.schema.json (v1). No prose, no fences.

## Input (from experiments/triage.py --payload)
{ issue_text, anchors, suspects (files + hits + recent_commits), archaeology
  (git log -S per anchor), commit }

## Rules (validator rejects on violation, C2)
1. Classify: bug / feature / question / config, with confidence.
2. kind=bug => at least one rank="primary" AND at least one rank="alternative"
   hypothesis (B3: 自信的錯誤假說比沒有假說更毒).
3. Every hypothesis cites evidence: spans into suspect files and/or shas from
   archaeology / recent_commits. Never cite a file or sha not present in the
   payload. Empty evidence is a schema violation.
4. kind=feature => decompose into requirements R1..Rn (<=300 chars each).
5. missing_info: list what the reporter did not provide (repro, versions,
   logs). Empty list only when genuinely complete.
6. Unsure => confidence "low". Do not omit a hypothesis to look clean.
