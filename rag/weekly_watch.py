"""Weekly watch report (user directive 2026-10-26): scan the last N days of news
items, surface Reddit posts with min_upvotes+, list HF trending/downloads/datasets.

Writes news/weekly_watch_<date>.md (the durable log) and prints a summary.
The AGENT then authors the relevance report in docs/research_watch/<date>_weekly.md
(what each item does + how it helps our project) and commits it.

Usage: python weekly_watch.py
"""
import json
import os
import re
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
NEWS_DIR = os.path.join(ROOT, "news")
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
WW = CFG.get("weekly_watch", {"min_upvotes": 50, "days": 2})
MIN_UP = WW.get("min_upvotes", 50)
DAYS = WW.get("days", 2)


def parse_frontmatter(fn):
    meta = {}
    with open(fn, encoding="utf-8") as f:
        txt = f.read()
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, txt


def main():
    today = datetime.now()
    cutoff = today - timedelta(days=DAYS)
    date_dirs = []
    for d in os.listdir(NEWS_DIR):
        p = os.path.join(NEWS_DIR, d)
        if not os.path.isdir(p):
            continue
        try:
            dd = datetime.strptime(d, "%Y-%m-%d")
        except ValueError:
            continue
        if dd >= cutoff:
            date_dirs.append((dd, d))
    date_dirs.sort()

    hot_reddit, hf_trending, hf_downloads, hf_datasets, x_items, civitai = [], [], [], [], [], []
    for dd, d in date_dirs:
        for fn in sorted(os.listdir(os.path.join(NEWS_DIR, d))):
            if not fn.endswith(".md"):
                continue
            meta, _ = parse_frontmatter(os.path.join(NEWS_DIR, d, fn))
            src = meta.get("source", "")
            entry = {
                "date": d, "file": fn, "id": meta.get("id", fn),
                "url": meta.get("url", ""), "score": int(meta.get("score", 0) or 0),
                "likes": int(meta.get("likes", 0) or 0),
                "downloads": int(meta.get("downloads", 0) or 0),
                "age": meta.get("age", ""),
            }
            if src.startswith("reddit"):
                if entry["score"] >= MIN_UP:
                    hot_reddit.append(entry)
                else:
                    entry["score"] = entry["score"]
                    hot_reddit.append(entry)  # keep for context; report filters
            elif src == "hf/models-trending":
                hf_trending.append(entry)
            elif src == "hf/models-downloads":
                hf_downloads.append(entry)
            elif src == "hf/datasets-trending":
                hf_datasets.append(entry)
            elif src.startswith("x/"):
                x_items.append(entry)
            elif src.startswith("civitai/"):
                entry["kind"] = src.split("/", 1)[1]
                civitai.append(entry)

    hot = [e for e in hot_reddit if e["score"] >= MIN_UP]
    out = os.path.join(NEWS_DIR, f"weekly_watch_{today:%Y-%m-%d}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# Weekly watch — {today:%Y-%m-%d}\n")
        f.write(f"Window: last {DAYS} day(s) ({date_dirs[0][1] if date_dirs else 'n/a'} .. "
                f"{date_dirs[-1][1] if date_dirs else 'n/a'})\n\n")
        f.write(f"## Reddit — {len(hot)} posts with {MIN_UP}+ upvotes\n\n")
        if hot:
            for e in sorted(hot, key=lambda x: -x["score"]):
                f.write(f"- **{e['score']}** {e['id']} ({e['date']}) {e['url']}\n")
        else:
            f.write("NONE CAPTURED in window — Reddit sources walled (see digest logs). "
                    "Daily run retries automatically.\n")
        f.write(f"\n## HuggingFace trending models — {len(hf_trending)}\n\n")
        for e in sorted(hf_trending, key=lambda x: -x["likes"]):
            f.write(f"- {e['id']} (likes {e['likes']}, downloads {e['downloads']}) "
                    f"https://huggingface.co/{e['id']}\n")
        f.write(f"\n## HuggingFace top-download models — {len(hf_downloads)}\n\n")
        for e in sorted(hf_downloads, key=lambda x: -x["downloads"]):
            f.write(f"- {e['id']} (downloads {e['downloads']}) "
                    f"https://huggingface.co/{e['id']}\n")
        f.write(f"\n## HuggingFace trending datasets — {len(hf_datasets)}\n\n")
        for e in hf_datasets:
            f.write(f"- {e['id']} https://huggingface.co/datasets/{e['id']}\n")
        f.write(f"\n## X accounts — {len(x_items)}\n\n")
        if x_items:
            for e in x_items:
                f.write(f"- {e['id']} {e['url']}\n")
        else:
            f.write("NONE CAPTURED (HTTP 429 engine-blocked — best-effort source).\n")
        f.write(f"\n## Civitai — {len(civitai)} items (hot/newest/ComfyWorkflows/new LoRAs)\n\n")
        if civitai:
            for e in sorted(civitai, key=lambda x: -x["downloads"]):
                f.write(f"- ({e.get('kind', '?')}) {e['id']} (downloads {e['downloads']}) "
                        f"https://civitai.com/models/{e['id'].split('_')[-1] if e['url'].split('/')[-1].isdigit() else e['id']}\n")
        else:
            f.write("NONE CAPTURED this window.\n")
    print(f"written {out}")
    print(f"reddit {MIN_UP}+: {len(hot)}; hf trending: {len(hf_trending)}; "
          f"hf downloads: {len(hf_downloads)}; datasets: {len(hf_datasets)}; "
          f"civitai: {len(civitai)}; x: {len(x_items)}")


if __name__ == "__main__":
    main()
