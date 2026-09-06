# Project State

Last Updated: 2026-08-26

## Current Objective

Build a production-ready title video for the production house: **"The Jaisal Cut"**.

Story: kid walks a stone bridge (wide, camera in the river) → clouds change, wind → sudden rain → kid runs → mid-bridge rain hits → close-up of face as rain comes and goes like a gust → kid stares at sky → camera pans/zooms out → "The Jaisal Cut" title where the kid becomes the dot in the J.

Pipeline: 9-image story sheet (16:9, 2048×1152) → MiniMax H3 ref-image-to-video (15s) → paper-tear title clip → title composited in post (NOT rendered by the model).

Immediate goal: build the character/style sheet (wide base ✅, face base ✅, medium shot ✅, remaining frames ⏳), then wire into the MiniMax H3 video workflow.

## Current AI Stack

### LLM

- Model: Qwen3.8-27B-NVFP4-MTP-LOW.gguf
- Runtime: llama.cpp
- API: OpenAI-compatible
- Endpoint: http://127.0.0.1:8100/v1
- Start: D:\models\qwen\Qwen3.827BMTP.bat
- Alternatives in D:\models\qwen: Qwen3.6-27B-Q6_K.gguf, Qwen3.6-35B-A3B-Uncensored (Q4_K_M), Gemma4-26B-A4B-Uncensored (Q4_K_M)

### GPU

- NVIDIA RTX 5090
- VRAM: ~32 GB

### ComfyUI

- Local Windows installation
- ComfyUI is running locally
- ComfyUI MCP is installed and working

### MCP

- Package: comfy-mcp
- Current version: 0.10.0
- Transport: stdio
- MCP is being invoked by the AI client rather than manually operated as a standalone HTTP service.

### Workspace layout (reorganized 2026-08-31, now a git repo)

`d:\models\vsCodeMcp\` is a **git repository** (for tracking + pushing to GitHub). Layout:

- `AGENTS.md` — project instructions (root)
- `project-memory/` — persistent memory (PROJECT_STATE, DECISIONS, EXPERIMENTS, WORKFLOW_HISTORY, CURRENT_TASK)
- `prompts/` — all prompt `.txt` files (`jaisal_sketch_prompts.txt`, `jaisal_ref_prompts.txt`, `jaisal_identity_instructions.txt`, `jaisal_single_ref_prompt*.txt`)
- `docs/` — reference docs (`CAMERA_SHOT_VOCABULARY.md`, `MINIMAX_H3_R2V_PROMPTING_GUIDE.md`, `HELPER_SCRIPTS.md`)
- `utilities/` — all helper Python scripts + `run_2mp_benchmark.bat` (run with the embedded Python)
- `data/` — data artifacts (`object_info_cache.json`, `vram_monitor.csv`, `analyze_out.txt`)
- `workflow_backups/` — pre-fix workflow backups (tracked in git, ~1.4 MB)
- `.github/` — copilot instructions + prompt templates

**Rule: scripts live in `utilities/`, prompts in `prompts/`, docs in `docs/`, data in `data/`.** Run a script: `& "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\<script>.py"`. Commit changes with `git add -A; git commit`.

### Paths

- **Models (MAIN PATH): E:\ComfyUI_windows_portable\ComfyUI\models** — ALL models live here (diffusion_models, text_encoders, vae, loras, etc.). Check this path for model availability, NOT the comfyUi_latest path.
- ComfyUI (portable install, outputs/workflows): E:\comfyUi_latest\ComfyUI_windows_portable
- MCP server exe: E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Scripts\comfy-mcp.exe
- COMFY_BIN env value: E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Scripts\comfy.exe
- MCP config: .vscode\mcp.json (in this project)
- MCP manual start: E:\comfyUi_latest\ComfyUI_windows_portable\start_mcp.bat
- Saved workflows: E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows
- Outputs: E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output
- Inputs: E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input
- llama.cpp runtime: D:\llama-b9616-bin-win-cuda-13.3-x64 (llama-server.exe)

### MiniMax H3 models (verified present at the main models path)

- minimax_h3_ref2va_pruned_int8_convrot.safetensors (19.53 GB) — diffusion_models
- qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (14.61 GB) — text_encoders
- minimax_h3_video_vae_fp16.safetensors (4.85 GB) — vae
- minimax_h3_audio_vae_fp32.safetensors (0.56 GB) — vae
- The MiniMax H3 video workflow runs LOCALLY (no Comfy Cloud auth needed).

## Current Workflow

The user is building the **"The Jaisal Cut"** production title video using `@comfy-mcp`:

- inspect saved workflows
- create new workflows
- modify workflows
- debug workflows
- execute workflows
- inspect results

Active workflows (in E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows):

- krea2_jaisal_base.json — wide base (Anchor A), t2i
- krea2_jaisal_face_v3.json — face close-up (Anchor B), i2i
- krea2_jaisal_medium.json — medium shot, i2i from face (new)
- mini-max-refrance-to-video-1.json — MiniMax H3 ref-image-to-video (15s)
- WF-H3_zuanfilm-Face_Detailer.json — **Face Detailer** (close-up / face-refine shots). Pack `Carasibana/ComfyUI-H3-FaceRefine` (cloned 2026-09-01). Model paths remapped to our files. **Needs a ComfyUI restart for the H3Face nodes to register.** See D043.
- minimax_h3_sam_r2v_cinematic.json — **Character / Background swap** (SAM3 R2V). Pack `yujianvip/ComfyUI-SetGet-Resolver` (cloned 2026-09-01). 7 model paths remapped to our files. See D043.

### H3 speed stack (SLA) — 1MP < 240 s

All production MiniMax H3 workflows wire an **`H3SLAAttention` node** (Sparse Linear Attention, `ComfyUI-PlagueKind-Nodes/ComfyUI-H3-SLA-Attention`), sparsity 0.90, dense_backend `comfy_kitchen_int8`. **1MP (1344×768) H3 generation is UNDER 240 s (~4 min)** on this stack — NOT the 25–40 min full-attention figure. See **D042**. VDN-H3 (a different hybrid-attention speedup) is a deferred next step to benchmark against this SLA baseline.

## Current Strategy

Prefer:

1. Existing saved workflows when available
2. ComfyUI MCP for workflow inspection and modification
3. Actual workflow execution/results over theoretical reasoning
4. Small incremental changes
5. Persistent project memory for important decisions

## Current Blockers

None unless recorded here.

## Next Step

Continue workflow development using ComfyUI MCP and preserve important decisions/results in project-memory.
