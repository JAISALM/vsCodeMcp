"""Per-pipeline news fetch runner (D255: separate RAGs per pipeline, isolated stores).

Usage:
  python run_pipeline.py pradhana_kerala [--date YYYY-MM-DD]
  python run_pipeline.py all

Reads pipelines/registry.json. Each pipeline with run_daily=true gets its
sources fetched into ITS OWN store dir + a per-day digest file in its digest
dir. Consumers (topic picking) read only their pipeline's digest — no cross
pipeline confusion. Failures are logged, never fatal (same standard as
fetch_news.py — the next daily run retries).
"""
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))          # rag/
REPO = os.path.dirname(ROOT)                               # repo root
sys.path.insert(0, ROOT)

REG = os.path.join(ROOT, "pipelines", "registry.json")


def _resolve(p):
    return p if os.path.isabs(p) else os.path.join(REPO, p)


def _write_digest(p, date, results):
    dd = _resolve(p["digest_dir"])
    os.makedirs(dd, exist_ok=True)
    path = os.path.join(dd, f"digest_{date}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {p['name']} digest — {date}\n\n")
        for src, (ok, n, err) in results.items():
            f.write(f"## {src}\n")
            if not ok:
                f.write(f"_FAILED: {err}_\n\n")
                continue
            src_store = os.path.join(_resolve(p["store_dir"]), date, f"{src}.md")
            if os.path.exists(src_store):
                f.write(open(src_store, encoding="utf-8").read() + "\n")
            else:
                f.write(f"_({n} items; store file missing)_\n\n")
    return path


def run_pipeline(name, date=None):
    reg = json.load(open(REG, encoding="utf-8"))
    p = next((x for x in reg["pipelines"] if x["name"] == name), None)
    if p is None:
        sys.exit(f"unknown pipeline '{name}' — registry has: {[x['name'] for x in reg['pipelines']]}")
    date = date or datetime.datetime.now().strftime("%Y-%m-%d")
    sd = _resolve(p["store_dir"])
    os.makedirs(os.path.join(sd, date), exist_ok=True)

    import re
    results = {}
    if p["name"] == "pradhana_kerala":
        import subprocess
        import fetch_kerala
        # X/Twitter HOT layer (D256): cookie-injected browser head on
        # x.com/search — the "talk", not the headlines. playwright is ONLY
        # in the system Python310 (NOT in rag\.venv — verified 2026-11-19),
        # so this tier runs as a subprocess under it.
        PY310 = r"C:\Program Files\Python310\python.exe"
        for src in p["sources"]:
            try:
                if src == "x_kerala_hot":
                    r = subprocess.run([PY310, os.path.join(ROOT, "fetch_kerala_x.py"), date],
                                       capture_output=True, text=True, timeout=900,
                                       encoding="utf-8", errors="replace")
                    out = (r.stdout or "").strip().splitlines()
                    tail = out[-1] if out else ""
                    m = re.search(r"x_kerala_hot: (\d+) posts", tail)
                    n = int(m.group(1)) if m else 0
                    results[src] = (n > 0, n, None if n > 0 else (tail or (r.stderr or "")[-200:]))
                else:
                    n = fetch_kerala.fetch_source(src, sd, date)
                    results[src] = (True, n, None)
                print(f"[{p['name']}] {src}: {results[src][1]} items"
                      + (f" ({results[src][2]})" if results[src][2] else ""))
            except Exception as e:
                results[src] = (False, 0, str(e)[:200])
                print(f"[{p['name']}] {src} FAILED: {str(e)[:200]}")
    else:
        print(f"[{p['name']}] not a daily-run pipeline ({p['fetcher']}) — skipped")
        return None
    path = _write_digest(p, date, results)
    print(f"[{p['name']}] digest -> {path}")
    return path


def run_all():
    reg = json.load(open(REG, encoding="utf-8"))
    for p in reg["pipelines"]:
        if p.get("run_daily"):
            try:
                run_pipeline(p["name"])
            except Exception as e:
                print(f"[{p['name']}] pipeline FAILED (non-fatal): {e}")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "all"
    date = None
    if "--date" in sys.argv:
        date = sys.argv[sys.argv.index("--date") + 1]
    if name == "all":
        run_all()
    else:
        run_pipeline(name, date)
