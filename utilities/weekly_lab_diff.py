# -*- coding: utf-8 -*-
"""Weekly lab-watch diff (D228 resume, 2026-11-24): probe all 16 WATCHLIST orgs
via the HF API (plain-HTTP tier), report top-5 by lastModified, flag anything
modified since the last watch date (auto-cutoff: newest lab_watch_*.md in
rag/news/, fallback 2026-11-17 = last watch date before the outage window).

Headless-safe (2026-11-27, VsCodeMcp-BatchDaily): writes the full report to
rag/news/lab_watch_<date>.md so the next run's cutoff auto-advances; also
prints to stdout."""
import json, urllib.request, datetime, glob, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
NEWS_DIR = os.path.join(ROOT, "..", "rag", "news")

ORGS = ["Qwen", "MiniMaxAI", "black-forest-labs", "meta-llama", "stabilityai",
        "mistralai", "deepseek-ai", "facebook", "fishaudio", "Comfy-Org",
        "Lightricks", "meituan-longcat", "Wan-AI", "google", "tencent", "nvidia"]

def auto_cutoff():
    newest = None
    for fn in glob.glob(os.path.join(NEWS_DIR, "lab_watch_*.md")):
        m = re.match(r"lab_watch_(\d{4}-\d{2}-\d{2})\.md$", os.path.basename(fn))
        if m and (newest is None or m.group(1) > newest):
            newest = m.group(1)
    return newest or "2026-11-17"

CUTOFF = auto_cutoff()

def probe(org):
    url = ("https://huggingface.co/api/models?author=%s&sort=lastModified&limit=8"
           "&expand[]=lastModified&expand[]=downloads" % org)
    req = urllib.request.Request(url, headers={"User-Agent": "vsCodeMcp-watch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

out_lines = []
def say(line=""):
    out_lines.append(line)
    print(line)

fresh_count = 0
say("weekly lab diff — cutoff %s\n" % CUTOFF)
for org in ORGS:
    try:
        rows = probe(org)
    except Exception as e:
        say("[%s] PROBE FAIL: %s" % (org, e))
        continue
    fresh = [m for m in rows if (m.get("lastModified") or "")[:10] >= CUTOFF]
    fresh_count += len(fresh)
    flag = " <<< FRESH" if fresh else ""
    say("=" * 70)
    say("[%s] top by lastModified:%s" % (org, flag))
    for m in rows[:5]:
        lm = (m.get("lastModified") or "?")[:10]
        mark = " *NEW*" if lm >= CUTOFF else "      "
        say("  %s %s  dl=%s  %s" % (mark, m.get("id"), m.get("downloads"), lm))

today = datetime.date.today().isoformat()
out_file = os.path.join(NEWS_DIR, "lab_watch_%s.md" % today)
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines) + "\n")
say("\nwritten %s (fresh items: %d)" % (out_file, fresh_count))
