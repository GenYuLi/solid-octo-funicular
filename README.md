# review-automation

一句話:Claude Code session 結束或 pre-push 後幾分鐘,一份帶 requirement↔span 矩陣與
risk ranking 的 dossier 自動出現在通知裡;自動化的是理解,判斷留在人手上。
規格 single source:`docs/requirements-v1.6.html`(96 條,v0 已凍結 2026-08-17)。

## 目錄(讀的順序)
- `CLAUDE.md` — G1–G5 輸出合約種子,對本 repo 與所有被 review 的 repo 生效。
- `NOW.md` — P1 rolling state:Blocked-on(you)/ Now / Next。唯一的待決事項落點(P6)。
- `style.toml` — S1 資料源;S8 名人堂真實樣本。
- `docs/` — `requirements-v1.6.html`(規格本體)、`USAGE.md`(從使用者座位看 workflow)。
- `spec/` — 程式會直接消費的合約:`schemas/`(job-spec、claims、brief)、
  `prompts/`(tier1-dossier、tier1-brief;prompt_version 在檔頭,改即 bump,I5)、
  `NOW.template.md`。
- `install/` — 要複製到 host 的整合檔:`hooks/`(SessionEnd enqueue + settings fragment)、
  `systemd/`(path + service,Linux)、`launchd/`(plist,macOS,I14)。
- `experiments/` — Python 實驗區(Q3):`triage.py` = Tier 0 雛形,`demo/` 為 anyhow repo 實跑樣本。
- `crates/`(尚未建立)— Rust 核心:`review-worker`、lint;task 2 起建 Cargo workspace。

spec/ 與 install/ 的分界:前者是 binary 會 include 或載入的資料,後者是部署模板。

## 驗證狀態(誠實帳,2026-08-17 spec 包交付時)
- 機器已驗:schema 可載入且樣本實例通過;style.toml 可 parse;hook 在容器內真實
  git repo 跑過,輸出通過 job-spec schema,原子寫入與 no-op 路徑都測了。
- 待官方 docs 校對:settings-fragment 的 hooks 欄位名(不憑記憶信)。
- 待 host 驗:systemd units(容器裡沒 systemd);hook 零 jq 依賴。

## 怎麼開始
看 `NOW.md`。v0 coding 順序:hook 上線(queue 開始積 job)→ `review-worker`(Rust:
drain、debounce、Tier 0、claude -p、validator、renderer)→ S2 lint → hub serving。
手動試 Tier 0:`python3 experiments/triage.py --repo <repo> --issue <issue.txt>`。
