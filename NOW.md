# NOW — review-automation

## Blocked on (you)
- [ ] 協作模式 — 本 repo 的 task 0–3 由 Claude Code 實作、你審(CLAUDE.md 合約生效),
      還是照 workspace 預設 Mode A 由你手寫 Rust?— 決定 task 2 誰動手。
- [ ] task 順序 — 建議 task 1(rows-as-data generator)排到 task 2 之後:
      它不在 v0 閉環的關鍵路徑上,而 C15 要求 v0+v1 核心 2026-10-05 前完成。

## Now
- repo 已 init、結構已整理、已推上 github.com/GenYuLi/solid-octo-funicular(2026-08-19)。

## Next(Claude Code,依序)
- task 0: 校對 hooks settings 欄位名(官方 docs)→ 裝 `install/hooks/enqueue-session.sh`
  → 併 settings fragment(沒 worker 也無害:queue 積壓 = worker 測資)
- task 2: `review-worker`(Rust):drain / debounce / Tier 0 / claude -p / validator / renderer
  (Tier 0 參考實作:`experiments/triage.py`,收編時翻 Rust;含 I14 macOS adapter——
  launchd plist 模板在 `install/launchd/`)
- task 1: rows-as-data generator(docs/requirements-v1.6 → data + generated view)
- task 3: hub serving(tailnet-bound 靜態 serve + ntfy 通知,I15/D7)

## Next(你,皆不擋工)
- (10 min)requirements v1.6:只讀「政策」filter 11 條 + 已決 4 條,其餘不讀
- 手動試餵:`python3 experiments/triage.py --repo <repo> --issue <issue.txt>`

## Worktrees (machine-generated — do not hand-edit)
