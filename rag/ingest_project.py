"""Ingest project MD files (project-memory + docs + episode1) into FAISS 'project'.

Idempotent: content-hash manifest in data/manifest_project.json; only new/changed
files are chunked + embedded; chunks of deleted files are removed.
"""
import glob
import hashlib
import json
import os

import chunk as chunkmod
import embed
import store

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = store.DATA
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
MANIFEST = os.path.join(DATA, "manifest_project.json")
COL = "project"


def run():
    os.makedirs(DATA, exist_ok=True)
    manifest = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else {}
    files = []
    for d in CFG["project_dirs"]:
        files += glob.glob(os.path.join(d, "**", "*.md"), recursive=True)
    files = [f for f in files if not os.path.basename(f).startswith(".")]
    cur = {os.path.normpath(f): hashlib.sha1(open(f, "rb").read()).hexdigest() for f in files}

    added = [f for f, h in cur.items() if manifest.get(f, {}).get("hash") != h]
    removed = [f for f in manifest if f not in cur]

    if added or removed:
        for f in removed:
            store.delete(COL, manifest[f].get("chunk_ids", []))
            del manifest[f]
        for f in added:
            # remove this file's PREVIOUS chunks first (content change -> new chunk ids;
            # otherwise old chunks orphan in the store)
            old = manifest.get(f, {}).get("chunk_ids", [])
            if old:
                store.delete(COL, old)
            chunks = chunkmod.file_chunks(f, CFG["chunk_chars"], CFG["chunk_overlap"])
            if not chunks:
                manifest[f] = {"hash": cur[f], "chunk_ids": []}
                continue
            ids, texts, metas = zip(*[(c[0], c[1], c[2]) for c in chunks])
            vecs = embed.embed(list(texts))
            store.add(COL, list(ids), vecs, list(metas))
            manifest[f] = {"hash": cur[f], "chunk_ids": list(ids)}
        json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), indent=1)

    total_chunks = sum(len(v.get("chunk_ids", [])) for v in manifest.values())
    print(f"project: {len(files)} files; new/changed {len(added)}; removed {len(removed)}; "
          f"total chunks {total_chunks}; store count {store.count(COL)}")
    for f in added:
        print("  +", os.path.relpath(f, ROOT))
    for f in removed:
        print("  -", os.path.basename(f))
    return len(added)


if __name__ == "__main__":
    run()
