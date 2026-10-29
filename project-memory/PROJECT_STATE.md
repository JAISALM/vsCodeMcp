# Project State

## AI Stack (The Engine)
- **Agent Brain:** Qwen3.8-27B-NVFP4-MTP-LOW (@8100) — Handles tools, coding, and orchestration.
- **Writer Models:** Gemma4-31B-QAT (@8106) as default; Ortenzya Q5 (@8107) as prose backup.
- **Hardware:** NVIDIA RTX 5090 (32GB VRAM) + 64GB System RAM.
- **llama.cpp:** `D:\llama` = **b11960** (CUDA 13.4 self-contained, upgraded from b11583 on 2026-10-29 — D204 in-place pattern, old build at `D:\llama_bkp_b11960_*`). Above CVE-2026-116096 fix line; v0.8.0 adds LFM3 / DeepSeek-V4.1-Flash / Flint arch support. Restart 8100 via `D:\models\qwen\start_qwen_8100.bat`.
- **SLA (Sparse Linear Attention):** Used in MiniMax H3 workflows to keep 1MP generation under 4 minutes.

## Current Objective (2026-10-14)
**The Movie Project: Episode 1.**
Moving from the "Ground Reality" (First Half) to the "Mind-Trip" (Second Half). 

## Current Status
- **Setting:** Kerala village, 2026.
- **First Half:** Fully scripted with high-depth dialogues, cinematic transitions (Coconut Tree Wipe), and emotional beats.
- **Second Half:** Transitioning into the 1950 World Cup (Black & White).
- **VRAM Management:** STOP Qwen 8100 when running Gemma writers to avoid OOM.
- **Git Safety Net (D131):** all `.md` files committed via `utilities\commit_md.ps1` (scheduled task `VsCodeMcp-MdDailyCommit`, daily 22:30). Nuked/corrupted files are restored from git history.
- **Local RAG (D194, 2026-10-25):** `D:\models\vsCodeMcp\rag\` — chunking → embedding → vector store → search. Replaces "load all MD at once". Daily task `VsCodeMcp-RagDaily` (08:00) fetches AI news (Reddit/HF/X) + re-indexes project MD. Stack: `all-MiniLM-L6-v2` CPU embed (sentence-transformers; **Ollama NOT installed**), **FAISS-cpu** store (ChromaDB Rust bindings broken on this machine — D194). Query: `rag\.venv\Scripts\python.exe rag\query.py "<keywords>"`. Seed 2026-10-25: 1,248 project chunks + 65 news items.
