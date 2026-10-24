"""FAISS-cpu persistent store (replaces ChromaDB — chromadb's Rust bindings
fail on this machine with SQLITE_CANTOPEN for every path, all versions 1.3-1.5).

Collections: 'project' + 'news'. Vectors are L2-normalized (embed.py), so
IndexFlatIP = cosine similarity. Metadata kept in JSON (human-readable, diffable).
At our scale (<50k vectors) exact search is instant.
"""
import json
import os

import faiss
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
DIM = 384  # all-MiniLM-L6-v2


def _paths(col):
    return (os.path.join(DATA, f"{col}.faiss"),
            os.path.join(DATA, f"{col}.meta.json"))


def _load(col):
    ip, mp = _paths(col)
    if os.path.exists(ip):
        idx = faiss.read_index(ip)
    else:
        idx = faiss.IndexIDMap(faiss.IndexFlatIP(DIM))
    meta = {}
    if os.path.exists(mp):
        meta = {int(k): v for k, v in json.load(open(mp, encoding="utf-8")).items()}
    return idx, meta


def _save(col, idx, meta):
    os.makedirs(DATA, exist_ok=True)
    ip, mp = _paths(col)
    faiss.write_index(idx, ip)
    json.dump({str(k): v for k, v in meta.items()}, open(mp, "w", encoding="utf-8"), indent=0)


def count(col):
    return _load(col)[0].ntotal


def add(col, ids, embeddings, metadatas):
    """Upsert: remove existing ids, re-add everything given."""
    idx, meta = _load(col)
    for i in ids:
        if i in meta:
            try:
                idx.remove_ids(np.array([i], dtype="int64"))
            except Exception:
                pass
    arr = np.array(embeddings, dtype="float32")
    # faiss id must be int64: our chunk ids are sha1 hex — hash to int64
    import hashlib
    mapped = [int(hashlib.sha1(str(i).encode()).hexdigest()[:15], 16) % (2**62) for i in ids]
    idx.add_with_ids(arr, np.array(mapped, dtype="int64"))
    for i, m in zip(ids, metadatas):
        meta[int(hashlib.sha1(str(i).encode()).hexdigest()[:15], 16) % (2**62)] = m
    _save(col, idx, meta)


def delete(col, ids):
    idx, meta = _load(col)
    import hashlib
    mapped = [int(hashlib.sha1(str(i).encode()).hexdigest()[:15], 16) % (2**62) for i in ids]
    for m in mapped:
        if m in meta:
            try:
                idx.remove_ids(np.array([m], dtype="int64"))
            except Exception:
                pass
            del meta[m]
    _save(col, idx, meta)


def query(col, vec, k):
    idx, meta = _load(col)
    if idx.ntotal == 0:
        return []
    k = min(k, idx.ntotal)
    sims, ids = idx.search(np.array([vec], dtype="float32"), k)
    out = []
    for s, i in zip(sims[0], ids[0]):
        i = int(i)
        if i in meta:
            out.append((float(s), meta[i]))
    return out


def prune(col, keep_ids):
    """Remove store entries whose (hex) id is not in keep_ids. Returns removed count."""
    idx, meta = _load(col)
    import hashlib
    keep = {int(hashlib.sha1(str(i).encode()).hexdigest()[:15], 16) % (2**62) for i in keep_ids}
    stale = [i for i in meta if i not in keep]
    if stale:
        for i in stale:
            try:
                idx.remove_ids(np.array([i], dtype="int64"))
            except Exception:
                pass
            del meta[i]
        _save(col, idx, meta)
    return len(stale)
