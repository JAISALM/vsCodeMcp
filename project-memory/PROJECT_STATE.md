# Project State

## AI Stack (The Engine)
- **Agent Brain:** Qwen3.8-27B-NVFP4-MTP-LOW (@8100) — Handles tools, coding, and orchestration.
- **Writer Models:** Gemma4-31B-QAT (@8106) as default; Ortenzya Q5 (@8107) as prose backup.
- **Hardware:** NVIDIA RTX 5090 (32GB VRAM) + 64GB System RAM.
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
