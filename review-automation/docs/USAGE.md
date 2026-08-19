# USAGE — 從你的座位看這套 workflow

一句話:你不「操作」它;它在你本來就會行動的時刻,把整理好的東西端到面前。
v0 的新習慣只有一個:review 時開 dossier,不開 raw diff。

## v0 的一輪(review 線)
1. 照常開 Claude Code 幹活。差異來自 CLAUDE.md 合約:小 commit、
   大任務先提切分計畫、每個邏輯段落停下來給你看。
2. session 結束或 pre-push——你什麼都不用做。
   背景:hook → queue → worker(Tier 0 → claude -p → validator → lint → render)。
3. notify-send:「dossier ready: fix/PROJ-123 — 2 gaps · 1 scope-creep · ~340 加權行」。
4. 開 dossier(唯一新習慣):先看紅的——unmapped hunk、未實作需求、
   risk 排最前;點任何 claim 直接看到真實 code。約 15 分鐘。
5. 判斷照舊在 git / GitHub:有 gap → 下一輪 session 修;矩陣乾淨 → merge。

## 兩個手動迴路(被惹到才用)
- 看到爛句 → style.toml 的 fewshot 加一筆(S8)。
- 重複出現的 code smell → CLAUDE.md 或 risk 表加一條(C13 手動版)。

## v1 之後多的
- 早上開 triage board:隔夜 Jira issue 已附 brief(嫌疑 code 區、git 考古、假說)。
- session 開場:NOW.md 自動餵進 context,脈絡重建歸零。
- PR 上自動出現摘要 comment;`mdview` 一鍵渲染任何 markdown。

## 分工
- 系統:監看、抽取、對映、排序、渲染;乾淨就沉默,永不 nag。
- 你:讀排序後的結果、下判斷、偶爾餵迴路。決策永遠在你手上。
