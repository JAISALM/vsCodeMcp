r"""Poll SeedVR2 job statuses.

Usage:
    & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\seedvr_poll.py" [job_id ...]

Defaults to the kf5/kf6 2K jobs.
"""
import urllib.request, json, sys

API = "http://127.0.0.1:7870"
DEFAULT = ["3188da26ae", "7cd1636d6d"]


def main():
    jobs = sys.argv[1:] or DEFAULT
    for jid in jobs:
        try:
            r = json.load(urllib.request.urlopen(API + "/api/jobs/" + jid, timeout=10))
            print(jid, "->", r.get("status"), "prog", r.get("progress"), r.get("name", ""))
        except Exception as e:
            print(jid, "ERR", e)


if __name__ == "__main__":
    main()
