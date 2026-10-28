"""Resolve Civitai authors (uid -> username) via the browser head.

Run by `fetch_civitai` (fetch_news.py) as a SUBPROCESS under the SYSTEM python
(`C:\Program Files\Python310` — the only python with `playwright`; the RAG venv
does not have it). ONE browser session for all pairs (not one launch per item),
deduped by uid. Results are merged into `news/state/civitai_users.json`.

Usage: python civitai_author_resolve.py <json-file-with-pairs>
  pairs file: [[uid, mid], ...]
Prints JSON {resolved: {uid: username}, unresolved: [uid, ...]}.
"""
import json
import os
import re
import sys
import time

if sys.platform == "win32":
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import browser_head


def _cache_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "news", "state", "civitai_users.json")


def main():
    pairs_file = sys.argv[1]
    with open(pairs_file, "r", encoding="utf-8") as f:
        pairs = json.load(f)
    # dedupe by uid (first mid wins) — same author on many items = one visit
    by_uid = {}
    for uid, mid in pairs:
        by_uid.setdefault(str(uid), mid)
    # skip uids already named in the cache (only visit genuinely unknown ones)
    cache = {}
    cp = _cache_path()
    if os.path.exists(cp):
        try:
            cache = json.load(open(cp, encoding="utf-8"))
        except Exception:
            cache = {}
    todo = {u: m for u, m in by_uid.items()
            if not (cache.get(u) and not str(cache.get(u)).startswith("uid:"))}
    by_uid = todo
    resolved, unresolved = {}, []
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        ctx = browser_head._launch(p, verbose=True)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for uid, mid in by_uid.items():
            try:
                page.goto(f"https://civitai.com/models/{mid}",
                          wait_until="domcontentloaded", timeout=45_000)
                page.wait_for_timeout(2500)
                h = page.content()
                mu = re.search(r'href="/user/([A-Za-z0-9_]+)"', h)
                if mu:
                    resolved[uid] = mu.group(1)
                else:
                    unresolved.append(uid)
            except Exception:
                unresolved.append(uid)
            time.sleep(0.8)
        try:
            ctx.close()
        except Exception:
            pass
    # persist: merge resolutions into the shared uid->username cache
    if resolved:
        for uid, name in resolved.items():
            cache[uid] = name
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        with open(cp, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=1, sort_keys=True)
    print(json.dumps({"resolved": resolved, "unresolved": unresolved,
                      "cache_total": len(cache)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
