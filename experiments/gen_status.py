#!/usr/bin/env python3
"""Render docs/status.toml into docs/status.html — the v0 alignment board.

Single source is the TOML; this script only lays it out. It refuses to render
when work.covers and req.covered_by disagree, so the board cannot drift into
two inconsistent stories (C8: never render a plausible-looking half-truth).
usage: gen_status.py [--toml docs/status.toml] [--out docs/status.html]
"""
import argparse, datetime, html, sys, tomllib
from pathlib import Path

STATUS_ORDER = ["gap", "spec-only", "planned", "delivered", "policy"]
STATUS_LABEL = {"gap": "缺口", "spec-only": "合約在", "planned": "已認領",
                "delivered": "已交付", "policy": "政策"}
WORK_LABEL = {"next": "下一步", "todo": "待做", "doing": "進行中",
              "done": "完成", "deferred": "延後", "v1": "v1 核心(提案)"}
REPO_ISSUES = "https://github.com/GenYuLi/solid-octo-funicular/issues/"

def esc(s):
    return html.escape(str(s), quote=True)

def check_coverage(d):
    """Fail loudly if the two hand-maintained coverage fields disagree."""
    req_ids = {r["id"] for r in d["req"]}
    work_ids = {w["id"] for w in d["work"]}
    derived = {r: set() for r in req_ids}
    errors = []
    for w in d["work"]:
        for rid in w.get("covers", []):
            if rid not in req_ids:
                errors.append(f"{w['id']} covers unknown req {rid}")
            else:
                derived[rid].add(w["id"])
    for r in d["req"]:
        declared = set(r.get("covered_by", []))
        for wid in declared - work_ids:
            errors.append(f"{r['id']} covered_by unknown work {wid}")
        if declared != derived[r["id"]]:
            errors.append(f"{r['id']}: covered_by={sorted(declared)} "
                          f"but work.covers says {sorted(derived[r['id']])}")
    if errors:
        sys.exit("status.toml inconsistent:\n  " + "\n  ".join(errors))

def chips(ids):
    return "".join(f'<span class="chip">{esc(i)}</span>' for i in ids) or "—"

def pill(kind, label):
    return f'<span class="pill pill-{esc(kind)}">{esc(label)}</span>'

def render_kpis(d):
    as_of = datetime.date.fromisoformat(d["as_of"])
    deadline = datetime.date.fromisoformat(d["deadline"])
    days = (deadline - as_of).days
    v0 = [w for w in d["work"] if w["status"] not in ("deferred", "v1")]
    v1h = sum(w["hours"] for w in d["work"] if w["status"] == "v1")
    hours = sum(w["hours"] for w in v0)
    gaps = sum(1 for r in d["req"] if r["status"] == "gap")
    gap_notes = sum(1 for r in d["req"] if r.get("gap"))
    hours_num = f"{hours}<small>+{v1h}</small>" if v1h else str(hours)
    hours_label = "人時(v0 + v1 核心提案)" if v1h else "人時(v0 非延後項)"
    tiles = [
        (f'<span id="days-left">{days}</span>', "天到 2026-10-05", "C15 build window"),
        (hours_num, hours_label, f"v0 ≈ {hours/20:.1f}–{hours/15:.1f} 週 @ 15–20 h/週"),
        (f"{len(v0)}<small>+{len(d['work'])-len(v0)}</small>", "工作項(+延後·v1)",
         "W0 為下一步"),
        (f"{gaps}<small>/{gap_notes}</small>", "無人認領 / 缺口備註",
         "交付時漏掉的 v0 條目 / 帶缺口註記的條目"),
    ]
    out = ['<section class="kpis">']
    for num, label, sub in tiles:
        out.append(f'<div class="tile"><div class="num">{num}</div>'
                   f'<div class="label">{esc(label)}</div><div class="sub">{esc(sub)}</div></div>')
    out.append("</section>")
    return "\n".join(out)

def render_decisions(d):
    out = ['<section><h2 class="eyebrow">待你拍板</h2><ol class="decisions">']
    for x in d["decision"]:
        out.append(f'<li><span class="chip">{esc(x["id"])}</span> {esc(x["text"])}'
                   f'<div class="bites">→ {esc(x["bites"])}</div></li>')
    out.append("</ol></section>")
    return "\n".join(out)

def render_work(d):
    out = ['<section><h2 class="eyebrow">工作項 — v0 閉環施工順序</h2>',
           f'<p class="note">{esc(d["hours_note"])}</p>', '<div class="work">']
    for w in d["work"]:
        issue = (f'<a href="{REPO_ISSUES}{w["issue"]}">#{w["issue"]}</a>'
                 if w.get("issue") else '<span class="dim">issue 未開</span>')
        new = ' <span class="pill pill-gap">新增</span>' if w.get("new") else ""
        out.append(
            f'<div class="row w-{esc(w["status"])}">'
            f'<div class="head"><span class="wid">{esc(w["id"])}</span>'
            f'<span class="title">{esc(w["title"])}</span>{new}'
            f'{pill("w-" + w["status"], WORK_LABEL[w["status"]])}'
            f'<span class="hours">{w["hours"]} h</span><span class="issue">{issue}</span></div>'
            f'<div class="meta">覆蓋 {chips(w.get("covers", []))} · 依賴 {chips(w.get("depends", []))}</div>'
            f'<div class="wnote">{esc(w["note"])}</div></div>')
    out.append("</div></section>")
    return "\n".join(out)

def render_reqs(d):
    rows = sorted(d["req"], key=lambda r: STATUS_ORDER.index(r["status"]))
    out = ['<section><h2 class="eyebrow">v0 需求覆蓋 — 缺口排最前</h2>',
           '<div class="scroll"><table><thead><tr><th>ID</th><th>需求</th><th>狀態</th>'
           '<th>認領</th><th>證據 / 缺口</th></tr></thead><tbody>']
    for r in rows:
        gap = f'<div class="gap">缺:{esc(r["gap"])}</div>' if r.get("gap") else ""
        ev = esc(r.get("evidence") or ("" if gap else "—"))
        out.append(f'<tr class="s-{esc(r["status"])}"><td class="rid">{esc(r["id"])}</td>'
                   f'<td>{esc(r["title"])}</td><td>{pill(r["status"], STATUS_LABEL[r["status"]])}</td>'
                   f'<td>{chips(r.get("covered_by", []))}</td><td class="ev">{ev}{gap}</td></tr>')
    out.append("</tbody></table></div></section>")
    return "\n".join(out)

def render(d, css):
    body = "\n".join([
        '<header><p class="eyebrow">review-automation · v0 對齊板</p>',
        f'<h1>現在要做什麼、還缺什麼</h1>',
        f'<p class="lede"><b>北極星</b> {esc(d["north_star"])}</p>',
        f'<p class="lede"><b>v0 驗收</b> {esc(d["v0_acceptance"])}</p>',
        f'<p class="stamp">資料 {esc(d["as_of"])} · 來源 <code>{esc(d["source"])}</code> · '
        f'改 <code>docs/status.toml</code> 後跑 <code>experiments/gen_status.py</code></p></header>',
        render_kpis(d), render_decisions(d), render_work(d), render_reqs(d),
        '<script>(function(){var e=document.getElementById("days-left");if(!e)return;'
        f'var d=Math.ceil((new Date("{d["deadline"]}T00:00:00")-new Date())/864e5);'
        'if(isFinite(d))e.textContent=d;})();</script>'])
    return ("<title>review-automation v0 對齊板</title>\n"
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
            'family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
            f"<style>\n{css}\n</style>\n<main>\n{body}\n</main>\n")

def main():
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parent.parent
    ap.add_argument("--toml", default=root / "docs/status.toml")
    ap.add_argument("--out", default=root / "docs/status.html")
    args = ap.parse_args()
    d = tomllib.loads(Path(args.toml).read_text(encoding="utf-8"))
    check_coverage(d)
    css = (Path(__file__).with_name("status.css")).read_text(encoding="utf-8")
    Path(args.out).write_text(render(d, css), encoding="utf-8")
    print(f"wrote {args.out}")

if __name__ == "__main__":
    main()
