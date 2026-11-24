# -*- coding: utf-8 -*-
"""Weekly lab-watch diff (D228 resume, 2026-11-24): probe all 16 WATCHLIST orgs
via the HF API (plain-HTTP tier), report top-5 by lastModified, flag anything
modified since 2026-11-17 (the last watch date before the outage window)."""
import json, urllib.request, datetime

ORGS = ["Qwen", "MiniMaxAI", "black-forest-labs", "meta-llama", "stabilityai",
        "mistralai", "deepseek-ai", "facebook", "fishaudio", "Comfy-Org",
        "Lightricks", "meituan-longcat", "Wan-AI", "google", "tencent", "nvidia"]
CUTOFF = "2026-11-17"

def probe(org):
    url = ("https://huggingface.co/api/models?author=%s&sort=lastModified&limit=8"
           "&expand[]=lastModified&expand[]=downloads" % org)
    req = urllib.request.Request(url, headers={"User-Agent": "vsCodeMcp-watch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

print("weekly lab diff — cutoff %s (outage window 11-18..11-24)\n" % CUTOFF)
for org in ORGS:
    try:
        rows = probe(org)
    except Exception as e:
        print("[%s] PROBE FAIL: %s" % (org, e))
        continue
    fresh = [m for m in rows if (m.get("lastModified") or "")[:10] >= CUTOFF]
    flag = " <<< FRESH" if fresh else ""
    print("=" * 70)
    print("[%s] top by lastModified:%s" % (org, flag))
    for m in rows[:5]:
        lm = (m.get("lastModified") or "?")[:10]
        mark = " *NEW*" if lm >= CUTOFF else "      "
        print("  %s %s  dl=%s  %s" % (mark, m.get("id"), m.get("downloads"), lm))
