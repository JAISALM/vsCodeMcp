"""Daily news fetchers: Reddit (JSON API), HuggingFace (API), X (syndication, best-effort).

All unauthenticated. Every failure is logged, not fatal — the next daily run retries.
Output: one .md file per item in news/<YYYY-MM-DD>/ + a daily digest + seen.json dedup.
"""
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta

import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
NEWS_DIR = os.path.join(ROOT, "news")
STATE = os.path.join(NEWS_DIR, "state")
LOGS = os.path.join(NEWS_DIR, "logs")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 DSH-RAG/1.0"

CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))


def _seen():
    os.makedirs(STATE, exist_ok=True)
    p = os.path.join(STATE, "seen.json")
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return {}


def _save_seen(seen):
    os.makedirs(STATE, exist_ok=True)
    json.dump(seen, open(os.path.join(STATE, "seen.json"), "w", encoding="utf-8"), indent=0)


def _save_item(date, source, item_id, title, url, body, extra_meta):
    seen = _seen()
    key = f"{source}:{item_id}"
    if key in seen:
        return None
    os.makedirs(os.path.join(NEWS_DIR, date), exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", item_id)[:60]
    safe_src = re.sub(r"[^A-Za-z0-9_-]", "_", source)[:24]
    fn = os.path.join(NEWS_DIR, date, f"{safe_src}_{safe}.md")
    if os.path.exists(fn):
        seen[key] = date
        _save_seen(seen)
        return None
    meta = {"source": source, "id": item_id, "url": url, "fetched": date}
    meta.update(extra_meta)
    hdr = "\n".join(f"{k}: {v}" for k, v in meta.items() if v is not None)
    with open(fn, "w", encoding="utf-8") as f:
        f.write(f"---\n{hdr}\n---\n\n# {title}\n\n{body}\n")
    seen[key] = date
    return fn


def fetch_reddit(date, log):
    out = []
    limit = CFG.get("reddit_limit_per_sub", 30)
    for sub in CFG["subreddits"]:
        url = f"https://www.reddit.com/r/{sub}/top.json?t=day&limit={limit}&raw_json=1"
        data = None
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
            if r.status_code == 200:
                data = r.json()
            else:
                log.append(f"reddit r/{sub}: HTTP {r.status_code} -> playwright fallback")
        except Exception as e:
            log.append(f"reddit r/{sub}: {e} -> playwright fallback")
        if data is None:
            # browser fallback: persistent profile has the challenge state
            txt = ""
            try:
                import subprocess
                res = subprocess.run(
                    [r"C:\Program Files\Python310\python.exe",
                     r"D:\models\vsCodeMcp\utilities\reddit_browser_fetch.py",
                     url, "--text"],
                    capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace")
                txt = res.stdout or ""
                # JSON endpoint rendered in the browser: extract the JSON body
                s = txt.find("[")
                e = txt.rfind("]")
                if s >= 0 and e > s:
                    try:
                        data = {"data": {"children": json.loads(txt[s:e + 1])}}
                    except Exception:
                        data = None
            except Exception as e:
                log.append(f"reddit r/{sub} playwright fallback failed: {e}")
            if data is None:
                head = txt[:400].lower()
                challenged = ("<html" in head) or ("challenge" in txt.lower()[:2000] and "post" not in head)
                if challenged:
                    log.append(f"reddit r/{sub}: JS challenge wall (headless profile can't solve it); "
                               f"skip this run, retry later")
                elif len(txt) > 500:
                    # unstructured page text -> one item per page (still RAG-usable)
                    fn = _save_item(date, f"reddit/{sub}", f"page_{date}",
                                    f"r/{sub} top of the day ({date})",
                                    f"https://www.reddit.com/r/{sub}/top/?t=day",
                                    txt[:9000], {"note": "page-text fallback (JSON blocked)"})
                    if fn:
                        out.append(fn)
                else:
                    log.append(f"reddit r/{sub}: playwright returned no usable content "
                               f"(len={len(txt)}); retry next run")
                continue
        try:
            for ch in data["data"]["children"]:
                d = ch["data"]
                if d.get("sticked") or d.get("stickied"):
                    continue
                body = (d.get("selftext") or d.get("title") or "")[:6000]
                fn = _save_item(date, f"reddit/{sub}", d["id"], d.get("title", "?"),
                                d.get("permalink", ""), body,
                                {"author": d.get("author"), "score": d.get("score"),
                                 "comments": d.get("num_comments"),
                                 "flair": d.get("link_flair_text")})
                if fn:
                    out.append(fn)
        except Exception as e:
            log.append(f"reddit r/{sub}: parse error {e}")
    return out


def fetch_hf(date, log):
    out = []
    specs = [
        ("hf/models-trending", f"https://huggingface.co/api/models?sort=trendingScore&limit={CFG['hf']['trending_models']}"),
        ("hf/models-downloads", f"https://huggingface.co/api/models?sort=downloads&limit={CFG['hf']['top_downloads_models']}"),
        ("hf/datasets-trending", f"https://huggingface.co/api/datasets?sort=trendingScore&limit={CFG['hf']['trending_datasets']}"),
    ]
    for source, url in specs:
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
            r.raise_for_status()
            for d in r.json():
                pid = d.get("modelId") or d.get("id")
                title = pid
                body = d.get("description") or d.get("cardData") or ""
                if isinstance(body, dict):
                    body = json.dumps(body, ensure_ascii=False)
                fn = _save_item(date, source, pid, title, d.get("url", f"https://huggingface.co/{pid}"),
                                str(body)[:4000],
                                {"likes": d.get("likes"), "downloads": d.get("downloads"),
                                 "trending": d.get("trendingScore")})
                if fn:
                    out.append(fn)
        except Exception as e:
            log.append(f"hf {source}: {e}")
    return out


def fetch_x(date, log):
    """Best-effort unauth: syndication timeline-profile widget JSON.

    Parses the __NEXT_DATA__ blob for tweet entries. Fails gracefully per account.
    """
    out = []
    for i, acct in enumerate(CFG["x_accounts"]):
        if i:
            time.sleep(8)  # syndication rate-limits rapid sequential calls (429 seen 2026-10-25)
        url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{acct}"
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
            m = re.search(r'<script id="__NEXT_DATA__" type="application/json"[^>]*>(.*?)</script>',
                          r.text, re.S)
            if not m:
                log.append(f"x {acct}: no __NEXT_DATA__ (HTTP {r.status_code}) — best-effort source, skipped")
                continue
            data = json.loads(m.group(1))
            found = []

            def walk(o):
                if isinstance(o, dict):
                    if "full_text" in o and ("id_str" in o or "id" in o):
                        found.append(o)
                    for v in o.values():
                        walk(v)
                elif isinstance(o, list):
                    for v in o:
                        walk(v)

            walk(data)
            cutoff = datetime.now() - timedelta(days=3)
            for t in found[:25]:
                ts = t.get("created_at", "")
                try:
                    parsed = datetime.strptime(ts[:19], "%a %b %d %H:%M:%S %z %Y")
                    if parsed < cutoff:
                        continue
                except Exception:
                    pass
                tid = t.get("id_str") or t.get("id")
                title = (t.get("full_text") or "")[:120].replace("\n", " ")
                fn = _save_item(date, f"x/{acct}", str(tid), title or "tweet",
                                f"https://x.com/{acct}/status/{tid}",
                                (t.get("full_text") or "")[:4000],
                                {"created_at": ts, "likes": t.get("favorite_count")})
                if fn:
                    out.append(fn)
        except Exception as e:
            log.append(f"x {acct}: {e}")
    return out


def run(date=None):
    date = date or datetime.now().strftime("%Y-%m-%d")
    os.makedirs(LOGS, exist_ok=True)
    log = []
    new = []
    new += fetch_reddit(date, log)
    new += fetch_hf(date, log)
    new += fetch_x(date, log)
    _save_seen(_seen())

    # digest
    digest = os.path.join(NEWS_DIR, f"digest_{date}.md")
    with open(digest, "a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.now():%Y-%m-%d %H:%M} run\n")
        if new:
            for fn in sorted(new):
                src = os.path.basename(os.path.dirname(fn))
                f.write(f"- [{src}] {os.path.basename(fn)}\n")
        else:
            f.write("- no new items\n")
        for l in log:
            f.write(f"- LOG: {l}\n")
    print(f"new items: {len(new)}; log lines: {len(log)}")
    for l in log:
        print("  LOG:", l)
    return new


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else None)
