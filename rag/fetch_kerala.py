"""Kerala/Malayalam news fetcher for the pradhana_kerala pipeline (D254/D255).

Sources (best-effort headline scraping — every failure is logged, not fatal;
the next daily run retries). Probed 2026-11-19:
  - manorama_ml : https://www.manoramaonline.com/malayalam/
      (SOFT-404: returns HTTP 404 but serves ~226 KB of real Malayalam
      content — acceptance is content-based, not status-based)
  - news18_ml   : https://malayalam.news18.com/   (200, ~854 KB, best source)
  - kaumudi_ml  : https://www.keralakaumudi.com/  (200, Kerala-local)
  (asianet_ml was DEAD on probe: redirect loop on both paths — dropped.)

Output: <store_dir>/<date>/<source>.md — headline list (Malayalam text + URL).
Fetch ladder per source: plain requests -> web-search-mcp engine (same engine
VS Code uses) -> logged failure. (Browser head is the next tier if both fail —
add on demand.)
"""
import json
import os
import re
import sys

import requests
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from fetch_news import _mcp_fetch  # noqa: E402  (shared MCP-fetch engine tier)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 DSH-RAG/1.0"
MAX_HEADLINES = 20

SOURCES = {
    "manorama_ml": "https://www.manoramaonline.com/malayalam/",
    "news18_ml": "https://malayalam.news18.com/",
    "kaumudi_ml": "https://www.keralakaumudi.com/",
}

ML_RE = re.compile(r"[\u0d00-\u0d7f]")  # Malayalam script range


def _strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def _extract_headlines(html, base):
    """Best-effort: anchors whose text is Malayalam and long enough to be a
    headline (not nav/menus). Dedup by text, keep order, cap at MAX_HEADLINES."""
    seen = set()
    out = []
    for m in re.finditer(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.S | re.I):
        href, text = m.group(1), _strip_tags(m.group(2))
        if len(text) < 25 or not ML_RE.search(text):
            continue
        # skip obvious nav/menu/label anchors
        if any(k in text.lower() for k in ("കൂടുതൽ", "വിലാസം", "സംപർക്കം", "ad", "subscribe")):
            continue
        if text in seen:
            continue
        seen.add(text)
        out.append((urljoin(base, href), text))
        if len(out) >= MAX_HEADLINES:
            break
    return out


def _fetch_html(url):
    """requests tier -> mcp engine tier. Returns (html, tier, err)."""
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "ml,en"},
                         timeout=30)
        # Content-based acceptance: manorama serves real Malayalam content
        # with HTTP 404 (soft-404) — a status-only check would drop it.
        if len(r.text) > 2000 and ML_RE.search(r.text):
            tier = "requests" + ("" if r.status_code == 200 else f" (http {r.status_code} soft)")
            return r.text, tier, None
        err1 = f"http {r.status_code}, {len(r.text)} bytes"
    except Exception as e:
        err1 = str(e)[:120]
    try:
        status, text, err2 = _mcp_fetch(url, max_len=60000, timeout=90)
        if status == "success" and text and len(text) > 2000:
            return text, "mcp_engine", None
        err1 += f"; mcp_engine: {status} {err2}"
    except Exception as e:
        err1 += f"; mcp_engine exception: {str(e)[:120]}"
    return None, None, err1


def fetch_source(name, store_dir, date):
    """Fetch one source -> <store_dir>/<date>/<name>.md. Returns headline count.
    Raises on total failure (runner logs it, non-fatal)."""
    if name not in SOURCES:
        raise ValueError(f"unknown kerala source '{name}' — {list(SOURCES)}")
    url = SOURCES[name]
    html, tier, err = _fetch_html(url)
    if html is None:
        raise RuntimeError(f"{name}: all tiers failed — {err}")
    heads = _extract_headlines(html, url)
    if not heads:
        raise RuntimeError(f"{name}: fetched via {tier} but 0 headlines parsed "
                           f"(layout may have changed — check {url})")
    day_dir = os.path.join(store_dir, date)
    os.makedirs(day_dir, exist_ok=True)
    path = os.path.join(day_dir, f"{name}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {name} — {url} — {date} (tier: {tier})\n\n")
        for i, (href, text) in enumerate(heads, 1):
            f.write(f"{i}. {text}\n   {href}\n")
    return len(heads)


if __name__ == "__main__":
    date = sys.argv[2] if len(sys.argv) > 2 else __import__("datetime").datetime.now().strftime("%Y-%m-%d")
    store = os.path.join(ROOT, "pipelines", "pradhana_kerala", "store")
    for src in SOURCES:
        try:
            print(f"{src}: {fetch_source(src, store, date)} headlines")
        except Exception as e:
            print(f"{src} FAILED: {e}")
