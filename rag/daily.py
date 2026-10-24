"""Daily RAG pipeline: fetch news -> index new news -> reindex changed project MD.

Usage: python daily.py [--project-only] [--news-only]
Scheduled via Windows task VsCodeMcp-RagDaily (run_daily_rag.bat).
"""
import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

# Scheduler sessions may lack a writable system temp dir (verified 2026-10-25) —
# pin TEMP/TMP into the workspace before anything imports tempfile-dependent code.
_tmp = os.path.join(ROOT, "temp")
os.makedirs(_tmp, exist_ok=True)
os.environ.setdefault("TEMP", _tmp)
os.environ.setdefault("TMP", _tmp)


def main():
    project_only = "--project-only" in sys.argv
    news_only = "--news-only" in sys.argv
    log = os.path.join(ROOT, "news", "logs",
                       f"daily_{datetime.now():%Y-%m-%d}.log")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    with open(log, "a", encoding="utf-8") as lf:
        lf.write(f"\n===== {datetime.now():%Y-%m-%d %H:%M} =====\n")
        lf.flush()

        if not project_only:
            import fetch_news
            new = fetch_news.run()
            lf.write(f"fetch: {len(new)} new items\n")
            lf.flush()
            import ingest_news
            ingest_news.run()

        if not news_only:
            import ingest_project
            ingest_project.run()

        lf.write("done\n")
    print("daily RAG complete")


if __name__ == "__main__":
    main()
