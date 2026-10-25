r"""Fetch the 5 character-sheet reddit posts via the session-cookie helper, save raw JSON
under D:/models/vsCodeMcp/data/char_sheet_reddit, and print a condensed digest
(title, selftext, top comments).
Run with the portable python_embeded exe on the script at
D:/models/vsCodeMcp/utilities/fetch_char_sheet_reddit.py
"""
import json, os, subprocess, time

PY = r"E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe"
HELPER = r"D:\models\vsCodeMcp\utilities\reddit_fetch.py"
OUT = r"D:\models\vsCodeMcp\data\char_sheet_reddit"
os.makedirs(OUT, exist_ok=True)

POSTS = {
 "P1_1wxixua": "https://www.reddit.com/r/comfyui/comments/1wxixua/.json?limit=40&sort=top",
 "P2_1vov6jb": "https://www.reddit.com/r/StableDiffusion/comments/1vov6jb/.json?limit=40&sort=top",
 "P3_1w2dujd": "https://www.reddit.com/r/StableDiffusion/comments/1w2dujd/.json?limit=40&sort=top",
 "P4_1wsb4h3": "https://www.reddit.com/r/StableDiffusion/comments/1wsb4h3/.json?limit=40&sort=top",
 "P5_1wsee1y": "https://www.reddit.com/r/comfyui/comments/1wsee1y/.json?limit=40&sort=top",
}

def clean_body(out: str) -> str:
    i = out.rfind("===HTTP:")
    return (out[:i].strip() if i != -1 else out.strip())

for name, url in POSTS.items():
    r = subprocess.run([PY, HELPER, url], capture_output=True, timeout=150)
    body = clean_body(r.stdout.decode("utf-8", "replace"))
    open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8").write(body)
    try:
        j = json.loads(body)
        listing = j[1] if isinstance(j, list) else j
        post = listing["data"]["children"][0]["data"]
        print(f"== {name}: {post['title']} (u/{post['author']}, score {post['score']})")
        st = (post.get("selftext") or "").replace("\n", " | ")
        print(f"   selftext: {st[:1800]}")
        print(f"   post_url: {post.get('url','')}")
        for c in listing["data"]["children"][1:]:
            if c.get("kind") != "t1":
                continue
            cd = c.get("data", {})
            txt = (cd.get("body") or "").replace("\n", " | ")
            if txt:
                print(f"   [c {cd.get('score')}] u/{cd.get('author')}: {txt[:700]}")
    except Exception as e:
        print(f"== {name}: PARSE FAIL ({e}) — head: {body[:300]}")
    time.sleep(5)
