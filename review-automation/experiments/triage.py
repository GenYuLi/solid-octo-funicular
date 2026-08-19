#!/usr/bin/env python3
"""Tier 0 issue triage — deterministic layer of the B line (B2).

Input : an issue as plain text (adapter's normalized output; Jira ADF/v2
        flattening happens upstream of this file, see B1).
Output: (1) mini-brief markdown on stdout — the "eight-tenths" a human wants
        first: anchors -> suspect regions -> git archaeology;
        (2) --payload FILE: the exact JSON that Tier 1 (claude -p) would
        receive. This file is the I7 backend seam.

Deliberately NOT here: classification, hypotheses, dedupe (Tier 1 / B3 / B4),
tracker adapters (B1). Python 實驗區 per Q3 — worker 收編時翻成 Rust。
usage: triage.py --repo PATH --issue FILE [--payload OUT.json] [--top N]
"""
import argparse, json, re, subprocess, sys
from collections import defaultdict
from datetime import datetime, timezone

# ---------- anchor extraction (B2) ----------

ANCHOR_PATTERNS = [
    ("quoted",  re.compile(r'["`\u2018\u201c]([^"`\u2019\u201d\n]{6,80})["`\u2019\u201d]')),
    ("path",    re.compile(r'\b((?:src|tests|benches|examples)/[\w./-]+\.\w{1,5})\b')),
    ("symbol",  re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z_][A-Za-z0-9_]*)+)\b')),
    ("call",    re.compile(r'\b([a-z_][a-z0-9_]{3,})\(\)')),
    ("env",     re.compile(r'\b([A-Z][A-Z0-9_]{4,})\b')),
    ("version", re.compile(r'\b(\d+\.\d+\.\d+)\b')),
]
NOISE = {"the", "this", "should", "would", "which", "error", "panic"}

def extract_anchors(text: str):
    seen, out = set(), []
    for kind, rx in ANCHOR_PATTERNS:
        for m in rx.finditer(text):
            a = m.group(1).strip()
            if a.lower() in NOISE or a in seen:
                continue
            seen.add(a)
            out.append({"kind": kind, "text": a})
    return out

# ---------- repo localization ----------

def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args],
                       capture_output=True, text=True, timeout=30)
    return r.stdout if r.returncode == 0 else ""

def grep_repo(repo, needle, max_hits=8):
    """grep -rnF through tracked source files; returns [(file, line, snippet)]."""
    r = subprocess.run(
        ["git", "-C", repo, "grep", "-nF", "--max-count=3", needle,
         "--", "*.rs", "*.py", "*.c", "*.cc", "*.cpp", "*.h", "*.go", "*.ts"],
        capture_output=True, text=True, timeout=30)
    hits = []
    for line in r.stdout.splitlines()[:max_hits]:
        try:
            f, ln, snip = line.split(":", 2)
            hits.append({"file": f, "line": int(ln), "snippet": snip.strip()[:120]})
        except ValueError:
            continue
    return hits

def log_s(repo, needle, n=3):
    """git log -S: commits that added/removed the needle — the archaeology."""
    out = git(repo, "log", f"-S{needle}", "--format=%h%x09%cs%x09%s", f"-{n}")
    return [dict(zip(("sha", "date", "subject"), l.split("\t", 2)))
            for l in out.splitlines()]

def recent_commits(repo, path, n=3):
    out = git(repo, "log", f"-{n}", "--format=%h%x09%cs%x09%s", "--", path)
    return [dict(zip(("sha", "date", "subject"), l.split("\t", 2)))
            for l in out.splitlines()]

# ---------- suspect ranking ----------

GENERIC_TAILS = {"next", "new", "get", "set", "len", "iter", "from", "into"}

def build_suspects(repo, anchors):
    per_file = defaultdict(lambda: {"hits": [], "anchor_kinds": set()})
    named_paths = {a["text"] for a in anchors if a["kind"] == "path"}
    for p in named_paths:
        per_file[p]["anchor_kinds"].add("path")  # 就算 grep 零命中也要出現
    for a in anchors:
        if a["kind"] == "version":
            continue
        needle = a["text"].split("::")[-1] if a["kind"] == "symbol" else a["text"]
        if a["kind"] == "symbol" and (len(needle) < 5 or needle in GENERIC_TAILS):
            continue  # 尾巴太泛,grep 只會灌水
        for h in grep_repo(repo, needle):
            per_file[h["file"]]["hits"].append({**h, "anchor": a["text"]})
            per_file[h["file"]]["anchor_kinds"].add(a["kind"])
    suspects = []
    for f, d in per_file.items():
        commits = recent_commits(repo, f)
        days = 9999
        if commits:
            days = (datetime.now(timezone.utc)
                    - datetime.fromisoformat(commits[0]["date"] + "T00:00:00+00:00")).days
        score = (len(d["anchor_kinds"]) * 10 + len(d["hits"])
                 + (15 if days <= 30 else 5 if days <= 180 else 0)
                 + (25 if f in named_paths else 0))  # issue 點名的檔案直接進前排
        suspects.append({"file": f, "score": score, "distinct_anchors": len(d["anchor_kinds"]),
                         "hits": d["hits"][:5], "recent_commits": commits,
                         "days_since_touch": days})
    return sorted(suspects, key=lambda s: -s["score"])

# ---------- outputs ----------

def render_brief(issue_path, anchors, suspects, digs, top):
    lines = [f"# Tier 0 brief — {issue_path}", ""]
    lines.append("## Anchors")
    for a in anchors:
        lines.append(f"- [{a['kind']}] `{a['text']}`")
    lines.append("")
    lines.append(f"## Suspect regions (top {top}, score = anchor 多樣性 + 命中數 + 近期被動過)")
    for s in suspects[:top]:
        touch = (f"{s['days_since_touch']} 天前被動過" if s["days_since_touch"] < 9999
                 else "近期無變更")
        lines.append(f"- **{s['file']}** — score {s['score']}, "
                     f"{s['distinct_anchors']} 種 anchor 命中, {touch}")
        for h in s["hits"][:3]:
            lines.append(f"    - L{h['line']} (`{h['anchor']}`): {h['snippet']}")
        for c in s["recent_commits"][:2]:
            lines.append(f"    - recent: {c['sha']} {c['date']} {c['subject']}")
    lines.append("")
    lines.append("## git log -S 考古(誰引入/移除過這些字串)")
    for needle, commits in digs.items():
        if not commits:
            continue
        lines.append(f"- `{needle}`:")
        for c in commits:
            lines.append(f"    - {c['sha']} {c['date']} {c['subject']}")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--payload")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    issue_text = open(args.issue, encoding="utf-8").read()
    anchors = extract_anchors(issue_text)
    suspects = build_suspects(args.repo, anchors)
    digs = {a["text"]: log_s(args.repo, a["text"])
            for a in anchors if a["kind"] in ("quoted", "call", "env")}

    print(render_brief(args.issue, anchors, suspects, digs, args.top))

    if args.payload:
        head = git(args.repo, "rev-parse", "HEAD").strip()
        payload = {"schema_version": 1, "commit": head,
                   "issue_text": issue_text, "anchors": anchors,
                   "suspects": suspects[:args.top], "archaeology": digs}
        json.dump(payload, open(args.payload, "w"), ensure_ascii=False, indent=1)
        print(f"\n[tier1 payload -> {args.payload}]", file=sys.stderr)

if __name__ == "__main__":
    main()
