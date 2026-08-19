# v0 spec 包 — 2026-08-17(對應 requirements v0.6,v0 已凍結)

一句話:這是凍結後 v0 的可執行展開;紙面最後一站,下一站是 code。

## 檔案地圖(讀的順序)
1. `CLAUDE.md` — G1–G5 輸出合約種子。放 repo 根;今天就能生效。
2. `style.toml` — S1 資料源;S8 名人堂已有兩筆真實樣本。
3. `schemas/job-spec.schema.json` — queue job(I1)。
4. `schemas/claims.schema.json` — Tier-1 輸出;validator 不變量寫在 description。
5. `prompts/tier1-dossier.md` — prompt_version 1(I5:改了就 bump)。
6. `hooks/enqueue-session.sh` + `settings-fragment.json` — L1 hook。
7. `systemd/review-worker.{path,service}` — I2/I3;worker binary 之後補。
8. `NOW.template.md` — P1/P6。

## 驗證狀態(誠實帳)
- 機器已驗:兩個 schema 可載入且樣本實例通過;style.toml 可 parse;
  hook script 在容器內真實 git repo 跑過,輸出通過 job-spec schema,
  原子寫入與 no-op 路徑都測了。
- 待官方 docs 校對:settings-fragment 的 hooks 欄位名(不憑記憶信)。
- 待 host 驗:systemd units(容器裡沒 systemd);hook 已改為零 jq 依賴。

## v0 coding 順序(下一站)
1. requirements 轉 rows-as-data + generated view(review = data diff)。
2. `review-worker`(Rust):drain、debounce、Tier 0 抽取、claude -p 呼叫、
   validator、renderer。
3. S2 lint(script 掃描 + OpenCC + banned map)。

NEXT: nothing — 我按上面順序開工,喊停即停。
