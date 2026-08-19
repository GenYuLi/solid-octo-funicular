# NOW — review-automation

## Blocked on (you)
- [ ] 協作模式 — 本 repo 的 task 0–3 由 Claude Code 實作、你審(CLAUDE.md 合約生效),
      還是照 workspace 預設 Mode A 由你手寫 Rust?— 決定 task 2 誰動手。
- [ ] task 順序 — 建議 task 1(rows-as-data generator)排到 task 2 之後:
      它不在 v0 閉環的關鍵路徑上,而 C15 要求 v0+v1 核心 2026-10-05 前完成。
- [ ] 「v1 核心」(C15)指哪些 ID?建議 = I14 + B2,其餘入職後按 C14 解鎖。
      — 估時顯示 v0 本身(~88 人時)已吃掉剩餘 46 天,沒定義就無法判斷達標。

## Now
- repo 已 init、結構已整理、已推上 github.com/GenYuLi/solid-octo-funicular(2026-08-19)。
- v0 對齊板 `docs/status.html`(2026-08-20):工作項 W0–W11、46 條 v0 需求覆蓋、缺口。
  工作項細節與 issue 編號看板子,NOW.md 只留順序。

## Next(Claude Code,依序;W 編號對應 docs/status.html)
- W0 SessionEnd hook 上線(先校對官方 hooks docs 欄位名)→ W1 pre-push 觸發
- W2 review-worker 骨架(Rust)→ W3 Tier 0(tree-sitter)→ W4 LLM backend + validator
  → W5 S2 lint → W6 renderer + 送達
- 穿插小項:W7 session ledger(L2)、W8 合約強制 hooks、W9 repo 衛生
- 延後:W10 rows-as-data generator(原 task 1)、W11 hub serving(原 task 3)

## Next(你,皆不擋工)
- (10 min)requirements v1.6:只讀「政策」filter 11 條 + 已決 4 條,其餘不讀
- 手動試餵:`python3 experiments/triage.py --repo <repo> --issue <issue.txt>`

## Worktrees (machine-generated — do not hand-edit)
