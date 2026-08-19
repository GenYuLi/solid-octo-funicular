# tier1-dossier prompt — prompt_version: 1
<!-- I5: bump prompt_version on ANY change here; LLM cache key includes it (C5). -->
<!-- Backend: claude -p (Q6 decision), run from an EMPTY temp dir so no project
     context leaks in (I8 clean-context note applies to the S3 editor, but a
     clean cwd also keeps this call reproducible). -->

## System / task
You map an issue's requirements to a code diff. Output ONLY one JSON object
conforming to claims.schema.json (v1). No prose, no markdown fences.

## Inputs supplied by the deterministic layer (Tier 0)
- ISSUE: raw issue text (may be empty => output requirements: [] and only
  risk / scope_creep / test_weakening claims).
- DIFF: hunks, each pre-annotated with { hunk_id, file, line range,
  enclosing symbol }.
- CONTEXT: one-hop caller/callee signatures for touched symbols (A2).

## Rules (violations are validator rejects, C2)
1. Split ISSUE into requirements R1..Rn, each <= 300 chars, verbatim-faithful.
2. For each requirement: either >=1 `req_impl` claim with spans into DIFF,
   or exactly one `gap` claim (spans MUST be empty).
3. Every hunk not supporting any requirement => one `scope_creep` claim.
4. Tag risks from the fixed vocabulary only: unsafe, lock_atomic, error_path,
   api_surface, serde_config, duplication (A4).
5. Assertions deleted or loosened alongside changes to the code they test
   => `test_weakening` claim (A5).
6. spans must cite files and line ranges that exist in DIFF or CONTEXT.
   Never invent paths. Never include code bodies in `text` (C3).
7. Unsure => confidence "low". Do not omit a claim to look clean.
