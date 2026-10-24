"""CPU-only embedding (sentence-transformers MiniLM) — zero GPU contention
with ComfyUI/llama.cpp (D192). Ollama not installed on this box (checked 2026-10-24)."""
import json
import os

# C:\Users\user\.cache is write-blocked on this box (WinError 5, checked 2026-10-25)
# -> keep the HF model cache inside the workspace.
os.environ.setdefault("HF_HUB_CACHE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "hf_cache"))
os.environ.setdefault("HF_HOME", os.path.join(os.path.dirname(os.path.abspath(__file__)), "hf_home"))
os.environ.setdefault("TRANSFORMERS_CACHE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "hf_cache"))

_model = None
_cfg = None


def _load_cfg():
    global _cfg
    if _cfg is None:
        _cfg = json.load(open(os.path.join(os.path.dirname(__file__), "config.json"), encoding="utf-8"))
    return _cfg


def embed(texts, batch_size=32):
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(_load_cfg()["embed_model"], device="cpu")
    if isinstance(texts, str):
        texts = [texts]
    vecs = _model.encode(texts, batch_size=batch_size, normalize_embeddings=True, show_progress_bar=False)
    return vecs.tolist()


def embed_query(text):
    return embed([text])[0]
