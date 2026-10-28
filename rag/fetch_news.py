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

MCP_FETCH = os.path.join(ROOT, "mcp_fetch.js")
NODE = "node"


def _mcp_fetch(url, max_len=12000, timeout=90):
    """Fetch a URL with the SAME engine VS Code's websearch MCP uses
    (D:\\MCP\\web-search-mcp: axios fast path -> randomized chromium fallback).
    Returns (status, text, err). status in success|blocked|low_quality|error."""
    import subprocess
    try:
        res = subprocess.run([NODE, MCP_FETCH, url, str(max_len)],
                             capture_output=True, text=True, timeout=timeout,
                             encoding="utf-8", errors="replace")
        for line in (res.stdout or "").splitlines():
            line = line.strip()
            if line.startswith("{"):
                d = json.loads(line)
                return d.get("fetchStatus", "error"), d.get("content") or "", d.get("error")
        return "error", "", (res.stderr or "no JSON on stdout")[:200]
    except Exception as e:
        return "error", "", str(e)[:200]


def _parse_redlib(html):
    """Best-effort parse of a redlib (libreddit-fork) HTML top page -> post dicts.

    Markup varies across mirror versions, so every field is best-effort regex;
    a block only counts if a /comments/ anchor is found.
    """
    posts = []
    for b in re.split(r'class="thing', html)[1:]:
        m_title = re.search(r'<a[^>]+href="([^"]*?/comments/[a-z0-9]+/[^"]*)"[^>]*>(.*?)</a>', b, re.S)
        if not m_title:
            continue
        href = m_title.group(1)
        title = re.sub(r'<[^>]+>', '', m_title.group(2)).strip()
        m_id = re.search(r'/comments/([a-z0-9]+)/', href)
        m_score = re.search(r'title="([\d,]+)"', b[:4000])
        m_author = re.search(r'href="(/user/[^"]+)"', b)
        m_time = re.search(r'<time[^>]+title="([^"]+)"', b) or re.search(r'<time[^>]*>([^<]+)</time>', b)
        posts.append({
            "id": m_id.group(1) if m_id else re.sub(r"[^a-z0-9]", "_", href)[-30:],
            "title": title,
            "url": ("https://www.reddit.com" + href) if href.startswith("/") else href,
            "score": int(m_score.group(1).replace(",", "")) if m_score else 0,
            "author": m_author.group(1).split("/")[-1] if m_author else None,
            "time": m_time.group(1).strip() if m_time else None,
        })
    return posts


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
        data = None
        # tier 1: JSON API. Attach REDDIT_SESSION_COOKIE when set (user env,
        # 2026-10-25 — the cookie itself is VALID, verified via JWT exp 2026-10-26;
        # but a valid cookie does NOT beat an IP-level wall: 2026-10-26 matrix test
        # returned 403 on every .json host with AND without the cookie).
        hdrs = {"User-Agent": UA}
        cookie = os.environ.get("REDDIT_SESSION_COOKIE", "")
        if cookie:
            hdrs["Cookie"] = f"reddit_session={cookie}"
        for period in ("day", "week"):
            if data is not None:
                break
            purl = f"https://www.reddit.com/r/{sub}/top.json?t={period}&limit={limit}&raw_json=1"
            try:
                r = requests.get(purl, headers=hdrs, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                else:
                    log.append(f"reddit r/{sub} ({period}): HTTP {r.status_code}")
            except Exception as e:
                log.append(f"reddit r/{sub} ({period}): {e}")
        if data is None:
            # tier 2: VS Code's own engine (D:\MCP\web-search-mcp: axios + randomized chromium)
            status, txt2, err = _mcp_fetch(
                f"https://www.reddit.com/r/{sub}/top.json?t=day&limit={limit}&raw_json=1", 16000)
            if status == "success":
                s = txt2.find("[")
                e2 = txt2.rfind("]")
                if s >= 0 and e2 > s:
                    try:
                        data = {"data": {"children": json.loads(txt2[s:e2 + 1])}}
                    except Exception:
                        pass
            if data is not None:
                log.append(f"reddit r/{sub}: via web-search-mcp engine (VS Code engine)")
            else:
                log.append(f"reddit r/{sub}: mcp engine {status} ({err or 'no JSON array'})")
        if data is None:
            # tier 2b: redlib mirror — Anubis proof-of-work is auto-solved by the
            # engine's chromium (verified 2026-10-26 that the gate is JS-computable).
            # Best-effort: if a mirror's markup resists _parse_redlib, log and move on.
            for mirror in CFG.get("reddit_mirrors", []):
                if data is not None:
                    break
                murl = f"https://{mirror}/r/{sub}/top?t=week"
                try:
                    mstatus, html, merr = _mcp_fetch(murl, 24000)
                except Exception as e:
                    log.append(f"reddit r/{sub}: mirror {mirror} fetch failed: {e}")
                    continue
                if mstatus == "success" and len(html) > 2000:
                    posts = _parse_redlib(html)
                    if posts:
                        saved = 0
                        for p in posts[:limit]:
                            fn = _save_item(date, f"reddit/{sub}", p["id"], p["title"],
                                            p["url"], p["title"][:6000],
                                            {"author": p["author"], "score": p["score"],
                                             "age": p["time"],
                                             "note": f"redlib mirror {mirror} (reddit.com walled)"})
                            if fn:
                                saved += 1
                        log.append(f"reddit r/{sub}: via redlib mirror {mirror} ({saved} new posts)")
                        if saved:
                            data = {"data": {"children": []}}
                            break
                    else:
                        log.append(f"reddit r/{sub}: mirror {mirror} returned HTML but no posts parsed")
                else:
                    log.append(f"reddit r/{sub}: mirror {mirror} {mstatus} ({merr or 'no content'})")
        if data is None:
            # tier 3 (VERIFIED WORKING 2026-10-26): browser-rendered HTML top page.
            # The JSON API is IP-walled (403 with AND without a valid session cookie),
            # but the HTML top page auto-solves the JS challenge in the persistent
            # profile and renders shreddit-post cards carrying title/score/author/
            # created-timestamp/comment-count as attributes (reddit_html_top.py).
            # This is exactly what VS Code's integrated browser does — same engine.
            html_posts = None
            try:
                import subprocess
                env = dict(os.environ)
                env["PYTHONIOENCODING"] = "utf-8"
                # Pin the child's temp into the workspace (verified 2026-10-26: a
                # nested child doing mkdtemp in the system Temp gets EPERM under
                # the session's file-sandbox scope; a workspace temp dir works).
                _pin = os.path.join(ROOT, "temp")
                os.makedirs(_pin, exist_ok=True)
                for _k in ("TEMP", "TMP", "TMPDIR"):
                    env[_k] = _pin
                res = subprocess.run(
                    [r"C:\Program Files\Python310\python.exe",
                     os.path.join(ROOT, "reddit_html_top.py"), sub, "week"],
                    capture_output=True, text=True, timeout=300, encoding="utf-8",
                    errors="replace", env=env)
                if res.returncode == 0:
                    try:
                        html_posts = json.loads(res.stdout)
                    except Exception:
                        log.append(f"reddit r/{sub}: HTML tier stdout unparseable")
                else:
                    tail = (res.stderr or "").strip().splitlines()
                    log.append(f"reddit r/{sub}: HTML top page tier rc={res.returncode} "
                               f"{' | '.join(tail[-4:])[:400] or 'no posts rendered'}")
                # grace for the profile lock to release before the next sub
                time.sleep(5)
            except Exception as e:
                log.append(f"reddit r/{sub} HTML top page tier failed: {e}")
            if html_posts is not None:
                saved = 0
                for p in html_posts:
                    fn = _save_item(date, f"reddit/{sub}", p["id"], p["title"],
                                    p["url"] or f"https://www.reddit.com/r/{sub}/",
                                    p["title"],
                                    {"author": p["author"], "score": p["score"],
                                     "age": p["created"], "comments": p["comments"],
                                     "note": "browser-rendered HTML top page (JSON API walled)"})
                    if fn:
                        saved += 1
                log.append(f"reddit r/{sub}: via HTML top page tier "
                           f"({saved} new of {len(html_posts)} posts)")
            else:
                log.append(f"reddit r/{sub}: HTML top page tier got no posts "
                           f"(gated this run); retry next run")
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
                # tier 2: same engine VS Code uses (randomized headers may dodge the 429)
                status, txt2, err = _mcp_fetch(url, 16000)
                m2 = re.search(r'<script id="__NEXT_DATA__" type="application/json"[^>]*>(.*?)</script>',
                               txt2, re.S) if status == "success" else None
                if m2:
                    m = m2
                    log.append(f"x {acct}: via web-search-mcp engine after {err or 'blocked'}")
                else:
                    # tier 3: OUR OWN Playwright browser head (the proven route —
                    # same engine class as VS Code's integrated browser; D202/D203).
                    # Anonymous X is login-walled; with X_AUTH_TOKEN/X_CT0 set the
                    # tier injects the session cookies and reads the full timeline.
                    import subprocess
                    try:
                        child_env = dict(os.environ)
                        child_env["PYTHONIOENCODING"] = "utf-8"
                        _temp_pin = os.path.join(ROOT, "temp")
                        os.makedirs(_temp_pin, exist_ok=True)
                        for _tk in ("TEMP", "TMP", "TMPDIR"):
                            child_env[_tk] = _temp_pin
                        res = subprocess.run(
                            [r"C:\Program Files\Python310\python.exe",
                             os.path.join(ROOT, "x_browser_fetch.py"), acct],
                            capture_output=True, encoding="utf-8", errors="replace",
                            timeout=300, env=child_env)
                        data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else None
                        if data and data.get("tweets"):
                            log.append(f"x {acct}: via browser-head tier "
                                       f"({len(data['tweets'])} tweets)")
                            for t in data["tweets"][:25]:
                                fn = _save_item(date, f"x/{acct}", t["id"],
                                                t["text"][:120].replace("\n", " "),
                                                t["url"], t["text"],
                                                {"created_at": t.get("date", "")})
                                if fn:
                                    out.append(fn)
                            continue
                        note = (data or {}).get("note", "no tweets rendered")
                        log.append(f"x {acct}: no __NEXT_DATA__ (HTTP {r.status_code}, "
                                   f"engine {status}) -> browser-head tier: {note}")
                        continue
                    except Exception as e:
                        log.append(f"x {acct}: no __NEXT_DATA__ (HTTP {r.status_code}, "
                                   f"engine {status}) -> browser-head tier failed: {e}")
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


_CIVITAI_USER_CACHE = os.path.join(NEWS_DIR, "state", "civitai_users.json")


def _load_civitai_users():
    try:
        return json.load(open(_CIVITAI_USER_CACHE, encoding="utf-8"))
    except Exception:
        return {}


def _save_civitai_users(cache):
    try:
        os.makedirs(os.path.dirname(_CIVITAI_USER_CACHE), exist_ok=True)
        with open(_CIVITAI_USER_CACHE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=1)
    except Exception:
        pass


def _civitai_detail(mid, hdrs):
    try:
        r = requests.get(f"https://civitai.com/api/v1/models/{mid}",
                         headers=hdrs, timeout=20)
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}


def fetch_civitai(date, log):
    """Civitai public API (verified reachable no-auth from this machine,
    2026-10-26 probe: order=HOT/NEWEST/POPULAR OK; types enum includes
    ComfyWorkflows/Workflows/LORA; /posts endpoint is 404 so 'interesting
    posts' is approximated by the HOT feed).

    The LIST endpoint returns slim items (no stats/user) — stats come from
    the DETAIL endpoint (GET /models/{id}: stats.downloadCount/thumbsUp/
    commentCount, baseModels, userId) + a userId→username cache
    (news/state/civitai_users.json). Detail calls run only for items that
    will actually be saved (dedup check first)."""
    out = []
    cfg = CFG.get("civitai", {})
    base = "https://civitai.com/api/v1"
    hdrs = {"User-Agent": UA}
    fetches = [
        ("hot", f"{base}/models?limit={cfg.get('hot_limit', 30)}&order=HOT"),
        ("newest", f"{base}/models?limit={cfg.get('newest_limit', 25)}&order=NEWEST"),
        ("comfyworkflows", f"{base}/models?limit={cfg.get('workflow_limit', 15)}"
                           f"&types=ComfyWorkflows&order=NEWEST"),
        ("newloras", f"{base}/models?limit={cfg.get('lora_limit', 15)}"
                     f"&types=LORA&order=NEWEST"),
    ]
    user_cache = _load_civitai_users()
    seen = _seen()
    unresolved = []  # (uid, mid) pairs the no-auth API can't resolve -> browser tier
    for kind, url in fetches:
        try:
            r = requests.get(url, headers=hdrs, timeout=30)
            if r.status_code != 200:
                log.append(f"civitai {kind}: HTTP {r.status_code}")
                continue
            items = r.json().get("items", [])
            saved = 0
            for it in items:
                mid = it.get("id")
                if not mid:
                    continue
                if f"civitai/{kind}:{mid}" in seen:
                    continue
                # enrich (list items are slim) — only for items being saved
                det = _civitai_detail(mid, hdrs)
                time.sleep(0.4)
                stats = det.get("stats") or {}
                dl = stats.get("downloadCount", 0)
                likes = stats.get("thumbsUpCount", 0)
                base_models = ", ".join(det.get("baseModels") or []) or "n/a"
                uid = det.get("userId")
                user = user_cache.get(str(uid)) if uid else None
                if user is None and uid:
                    try:
                        ru = requests.get(f"{base}/users/{uid}", headers=hdrs, timeout=20)
                        if ru.status_code == 200:
                            user = ru.json().get("username") or "u/?"
                        else:
                            user = f"uid:{uid}"
                    except Exception:
                        user = f"uid:{uid}"
                    user_cache[str(uid)] = user
                    time.sleep(0.3)
                if user and user.startswith("uid:"):
                    unresolved.append((uid, mid))
                user = user or "u/?"
                desc = (det.get("description") or it.get("description") or "")[:3000]
                body = (f"Type: {it.get('type')} · Base models: {base_models}\n"
                        f"Author: u/{user} · Downloads: {dl:,} · Likes: {likes:,} · "
                        f"Comments: {stats.get('commentCount', 0):,}\n\n{desc}")
                fn = _save_item(date, f"civitai/{kind}", str(mid),
                                f"[{it.get('type')}] {it.get('name', '?')} (u/{user}, {dl:,} dl)",
                                f"https://civitai.com/models/{mid}", body,
                                {"kind": kind, "type": it.get("type"),
                                 "author": user, "downloads": dl,
                                 "likes": likes})
                if fn:
                    saved += 1
                    out.append(fn)
            log.append(f"civitai {kind}: {saved} new of {len(items)}")
        except Exception as e:
            log.append(f"civitai {kind}: {e}")
        _save_civitai_users(user_cache)
        time.sleep(1.5)
    # browser-head author tier (D203): Civitai model pages SSR
    # 'href="/user/<name>"' (verified 2026-10-27) while /users/{id} is 401
    # no-auth. Runs as a SUBPROCESS under the SYSTEM python — the RAG venv does
    # NOT have `playwright` (verified 2026-10-28: "No module named 'playwright'"
    # in-venv). ONE browser session for all unresolved uids (deduped by uid).
    if unresolved:
        import subprocess
        try:
            _pairs_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "temp", "civitai_author_pairs.json")
            os.makedirs(os.path.dirname(_pairs_file), exist_ok=True)
            with open(_pairs_file, "w", encoding="utf-8") as f:
                json.dump([[str(u), str(m)] for u, m in unresolved], f)
            child_env = dict(os.environ)
            child_env["PYTHONIOENCODING"] = "utf-8"
            _temp_pin = os.path.join(ROOT, "temp")
            os.makedirs(_temp_pin, exist_ok=True)
            for _tk in ("TEMP", "TMP", "TMPDIR"):
                child_env[_tk] = _temp_pin
            res = subprocess.run(
                [r"C:\Program Files\Python310\python.exe",
                 os.path.join(ROOT, "civitai_author_resolve.py"), _pairs_file],
                capture_output=True, encoding="utf-8", errors="replace",
                timeout=3000, env=child_env)
            data = json.loads(res.stdout) if res.stdout.strip().startswith("{") else {}
            for uid, name in (data.get("resolved") or {}).items():
                user_cache[uid] = name
            log.append(f"civitai author browser tier: {len(data.get('resolved') or {})} "
                       f"resolved, {len(data.get('unresolved') or [])} unresolved")
        except Exception as e:
            log.append(f"civitai browser author tier failed: {e}")
    _save_civitai_users(user_cache)
    return out


def run(date=None):
    date = date or datetime.now().strftime("%Y-%m-%d")
    os.makedirs(LOGS, exist_ok=True)
    log = []
    new = []
    new += fetch_reddit(date, log)
    new += fetch_hf(date, log)
    new += fetch_civitai(date, log)
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
