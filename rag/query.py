"""RAG query CLI.

Usage:
  python query.py "character swap LoRA"            # search project+news
  python query.py "HyperFlow" -k 12               # more results
  python query.py "sampler" --collection news     # news only
  python query.py "VFX" --collection project     # project memory only
  python query.py "trending models" --days 3     # news from last 3 days

This is the retrieval path for the agent/user: targeted context instead of
dumping all MD files.
"""
import argparse
import os
from datetime import datetime

import embed
import store

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-k", type=int, default=8)
    ap.add_argument("--collection", choices=["all", "project", "news"], default="all")
    ap.add_argument("--days", type=int, default=0, help="news: only last N days (0 = any)")
    args = ap.parse_args()

    qvec = embed.embed_query(args.query)
    results = []
    cols = (["project"] if args.collection == "project"
            else ["news"] if args.collection == "news"
            else ["project", "news"])
    for col in cols:
        n = args.k * (3 if args.days else 1)
        for score, meta in store.query(col, qvec, n):
            if col == "news" and args.days:
                fetched = meta.get("fetched", "")
                try:
                    if (datetime.now() - datetime.strptime(fetched, "%Y-%m-%d")).days > args.days:
                        continue
                except Exception:
                    pass
            results.append((score, col, meta))
    results.sort(key=lambda r: -r[0])
    for score, col, meta in results[:args.k]:
        src = meta.get("file", "?")
        url = meta.get("url", "")
        section = meta.get("section", "")
        date = meta.get("fetched", meta.get("modified", ""))
        title = meta.get("doc", "")
        print(f"[{score:.3f}] {col} | {src}{' > ' + section if section else ''} | {date}")
        if url:
            print(f"         {url}")


if __name__ == "__main__":
    main()
