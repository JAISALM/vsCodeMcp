"""Ingest news .md files into FAISS 'news'. Incremental by content hash."""
import glob
import hashlib
import json
import os
import re

import embed
import store
from ingest_project import DATA

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(DATA, "manifest_news.json")
COL = "news"


def _meta(fn):
    txt = open(fn, encoding="utf-8", errors="replace").read()
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    meta = {}
    if m:
        for ln in m.group(1).split("\n"):
            if ": " in ln:
                k, v = ln.split(": ", 1)
                meta[k] = v
    meta["_path"] = fn
    return meta, txt


def run():
    os.makedirs(DATA, exist_ok=True)
    manifest = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else {}
    files = glob.glob(os.path.join(ROOT, "news", "*", "*.md"))
    files = [f for f in files if not os.path.basename(f).startswith("digest_")]
    hashes = {f: hashlib.sha1(open(f, "rb").read()).hexdigest() for f in files}
    added = [f for f, h in hashes.items() if manifest.get(f, {}).get("hash") != h]
    if added:
        ids, vecs, metas, cids = [], [], [], []
        for f in added:
            meta, txt = _meta(f)
            body = txt[:9000]
            cid = hashlib.sha1(f.encode()).hexdigest()[:16]
            ids.append(cid)
            vecs.append(embed.embed([body])[0])
            m = {k: v for k, v in meta.items() if k != "_path"}
            m["file"] = os.path.basename(f)
            metas.append(m)
            cids.append(cid)
        store.add(COL, ids, vecs, metas)
        for f, cid in zip(added, cids):
            manifest[f] = {"hash": hashes[f], "chunk_ids": [cid]}
        json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), indent=1)
    print(f"news: {len(files)} items; newly indexed {len(added)}; store count {store.count(COL)}")
    return len(added)


if __name__ == "__main__":
    run()
