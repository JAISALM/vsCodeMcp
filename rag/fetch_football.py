"""Football data fetcher for the Football Talkies pipeline (D255; on-demand, match-driven).

Source: understat.com (public pages, no auth) — top-5 leagues, last ~3 seasons.
fbref.com = fallback if understat changes layout.

Commands (all best-effort — every failure logged, parsing verified on the
FIRST real match per OPEN_ITEMS 3.1):
  python fetch_football.py --list SP          # recent matches of league SP (id/date/teams)
  python fetch_football.py --league SP        # per-player xG/xA table of the season
  python fetch_football.py --match <match_id> # shot list (xG per shot, location, shooter)

Output: rag/pipelines/football/store|data/ — isolated football store (D255).
Leagues: SP=LaLiga · EPL=PremierLeague · SA=SerieA · BUN=Bundesliga · FRA=Ligue1
"""
import json
import os
import re
import sys

import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
FB = os.path.join(ROOT, "pipelines", "football")
STORE = os.path.join(FB, "store")
DATA = os.path.join(FB, "data")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 DSH-RAG/1.0"
LEAGUES = {"SP": "LaLiga", "EPL": "PremierLeague", "SA": "SerieA",
           "BUN": "Bundesliga", "FRA": "Ligue1"}


def _get(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=45)
    r.raise_for_status()
    return r.text


def _js_var(html, name):
    """Extract `var <name> = <json>;` blobs understat embeds in its pages."""
    m = re.search(re.escape(f"var {name} =") + r"\s*(\[.*?\]|\{.*?\})\s*;", html, re.S)
    if not m:
        return None
    return json.loads(m.group(1))


def cmd_list(league):
    """Recent matches: parse match links + surrounding text on the league page."""
    html = _get(f"https://understat.com/league/{league}")
    out = []
    for m in re.finditer(r'href="/matches/(\d+)"[^>]*>(.*?)</a>', html, re.S):
        out.append({"match_id": m.group(1), "label": re.sub(r"<[^>]+>", "", m.group(2)).strip()[:160]})
    os.makedirs(STORE, exist_ok=True)
    path = os.path.join(STORE, f"matches_{league}.json")
    json.dump(out, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{path}: {len(out)} match links")
    return out


def cmd_league(league):
    """Per-player xG table embedded in the league page (tableData blob)."""
    html = _get(f"https://understat.com/league/{league}")
    td = _js_var(html, "tableData")
    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, f"players_{league}.json")
    if td:
        json.dump(td, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"{path}: {len(td)} players")
    else:
        open(path, "w").write("")
        print(f"{league}: tableData blob NOT found — layout likely changed; "
              f"save league HTML for inspection and re-derive the regex")
    return td


def cmd_match(match_id):
    """Shot list (per-shot xG, location, shooter, team, time) from a match page."""
    html = _get(f"https://understat.com/matches/{match_id}")
    shots = _js_var(html, "shotList")
    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, f"match_{match_id}.json")
    if shots:
        json.dump(shots, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"{path}: {len(shots)} shots")
    else:
        open(path, "w").write("")
        print(f"match {match_id}: shotList blob NOT found — layout likely changed; "
              f"inspect the match HTML and re-derive the regex")
    return shots


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    flag, val = sys.argv[1], sys.argv[2]
    if flag == "--list":
        cmd_list(val)
    elif flag == "--league":
        cmd_league(val)
    elif flag == "--match":
        cmd_match(val)
    else:
        print(__doc__)
        sys.exit(1)
