# Output contract (G1–G5 seed — style spec lives in style.toml, obey it)

## Docs (G2)
- Decision-record format: context (<=3 lines), decision (1 line),
  consequences, rejected alternatives (1 line each + why). Hard cap 80 lines.
- Answer first: if I stop reading after 90 seconds I must already have the
  conclusion. Details go to an appendix file I opt into.
- Never restate my requirements back to me. Prose hard-wrap 100 cols; no wide
  markdown tables — use lists.

## Code (G1, G3)
- One logical change per commit; message states intent (why). Cap ~300
  changed lines per commit. Bigger task => STOP, propose a split plan first.
- Estimated > ~150 lines => work as a series: after each logical unit, stop,
  show the diff, wait.
- No drive-by changes outside task scope; note follow-ups as TODOs.
- YAGNI: exactly what was asked. No speculative abstraction or extra knobs.
- Prefer boring: flat descriptive functions over clever hierarchies; greppable
  names; local reasoning. Intent goes in doc comments (they get
  consistency-checked against the code, A10).
- Never weaken a test assertion to make it pass. Flag the conflict instead.
- Branch naming carries the issue ref: fix/ISSUE-123-short-desc (Q2).

## Every substantial reply (G5)
- End with `NEXT — needed from you:` listing REAL decisions only, max 3.
- No decision pending => `NEXT: nothing — proceeding with <X>; say stop to stop.`
- Never manufacture a confirmation round.
