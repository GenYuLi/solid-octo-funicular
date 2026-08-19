# NOW — review-automation

## Blocked on (you)
- (none)

## Next(Claude Code,依序)
- task 0: 校對 hooks settings 欄位名(官方 docs)→ 裝 `spec/hooks/enqueue-session.sh`
  → 併 settings fragment(沒 worker 也無害:queue 積壓 = worker 測資)
- task 1: rows-as-data generator(docs/requirements-v1.6 → data + generated view)
- task 2: `review-worker`(Rust):drain / debounce / Tier 0 / claude -p / validator / renderer
  (Tier 0 參考實作:`experiments/triage.py`,收編時翻 Rust;含 I14 macOS adapter——launchd plist 模板在 spec/launchd/)
- task 3: hub serving(tailnet-bound 靜態 serve + ntfy 通知,I15/D7)

## Next(你,皆不擋工)
- (10 min)requirements v1.6:只讀「政策」filter 11 條 + 已決 4 條,其餘不讀
- 手動試餵:`python3 experiments/triage.py --repo <repo> --issue <issue.txt>`

## Worktrees (machine-generated — do not hand-edit)
