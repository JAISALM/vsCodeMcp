# Project State

Last Updated: 2026-10-03

**Current state (2026-10-03):** **VOICESTUDIO DUB HACK CONFIRMED.** User records rough audio for each dialogue (own voice) → VoiceStudio processes → LatentSync mouth-sync. **VoiceStudio backend FIXED + UP** (venv rebuilt on Python 3.12 — the cp313 `curated-tokenizers` Cython build failure left the venv empty; `uv sync` exit 0). **JAISAL voice already cloned** (`dd8bc71f`, Malayalam) + midhun (`094d6afe`). **Ubuntu-22.04 installed** (WSL2 2.7.13) → LatentSync ready after setup. **NEXT (user):** drop per-dialogue audios in `Jaisal-intro\dubs\` (A/C/E/F1/F2/G jaisal + optional camguy). **NEXT (me):** clean-as-is default (denoise+normalize, keep delivery; A/B with Convert re-speak) → LatentSync on A, C, E, F1, F2, G. See CURRENT_TASK.md 2026-10-03.

## Current Objective

Build the **"Jaisal Kut" channel-intro video** — a ~67s, 7-shot, **Black & White, NO
MUSIC** (D041) cinematic intro. (Supersedes the earlier bridge/title-video pipeline.)

Story (7 shots): walk-in → setup → slow 180° head twist (the hook) → perfect reverse →
plants grow (dream) → plants die (limitation) → **Jaisal explodes into ideas** (papers
+ mic + cricket bat + soccer ball; Jaisal vanishes, his ideas remain). Ends on
"നോക്കാം" (Let's see).

Pipeline: Krea2 Identity Edit keyframes (per shot) → MiniMax H3 ref-image-to-video →
SeedVR2 2K upscale → VoiceStudio/RVC voice + ControlFoley SFX → assembly.

**Current state (2026-10-02 EOD):** **DUB ROUTE CONFIRMED. Video stays locked. User going to sleep, resumes tomorrow.** The G re-run test came out **fundamentally broken** (random cuts, zero prompt adherence, music) — NOT a bad seed. The workflow/latent/refs/prompt are all correct on disk; the cause is a **runtime issue** (unverified). **DECISION:** the 8 finalized clips are the asset (locked). **TWO versions from one video:** (1) **ENGLISH** = MiniMax native audio (already in the clips, consistent) — **done.** (2) **MALAYALAM** = user's dub (6 Jaisal lines: A, C, E, F1, F2, G) + **LatentSync** (re-animates the mouth) + **English subs** (for the audience). Camera guy = muted (cards = questions). **NO RVC needed.** **NEXT (user, tomorrow):** (1) record 6 Jaisal lines (Malayalam) — Dolby On / Riverside / PC mic → drop in `Jaisal-intro\dubs\`; (2) confirm WSL2 reboot (LatentSync needs it); (3) assemble video in DaVinci (clips + cards, 72s). **NEXT (me):** LatentSync pass on the 6 speaking shots. **HARD RULE (new):** before any re-run, verify ComfyUI state + latent file + refs + prompt, and run 1 seed first. See D098/D099/D100 + CURRENT_TASK.md.

**Current state (2026-10-01):** **PRODUCTION MOVIE PIPELINE LOCKED (D097)** — the Jaisal-intro is the first instance of a reusable DUB-FIRST pipeline (SCRIPT → DUB → CLEAN → [RVC camera-guy] → LIP-SYNC (LatentSync) → SUBTITLES → DaVinci ASSEMBLY). **User-confirmed:** FINAL = **72s (1:12)** (cards OVERLAP clips, not full 3s segments — NOT the 82.34s raw concat); **card audio is NOT muted** (clip audio continues under the card = audio continuity); order = dub → lip-sync → subtitles → final; recording app = **Audacity** (mono/16-bit/48kHz/WAV); lip-sync = LatentSync on speaking shots (A, C, E, F1, F2, G), WSL2 reboot pending. **NEXT (user, NOW):** record ALL lines in Audacity (Jaisal + camera guy, one take each) + reboot (WSL2→LatentSync). **THEN (me):** clean_audio.py → RVC camera-guy lines (midhun_v2_40k) → LatentSync → re-time .srt to 72s cut → DaVinci assembly. See D097 + CURRENT_TASK.md.

**Current state (2026-09-29, EOD):** ALL 8 FINAL CLIPS DONE + **ALL UPSCALED** (2520×1440 @ 24fps, via `D:\models\SeedVR2-TensorRT-Studio` — TensorRT browser app; the earlier disk-full failure was fixed by deleting 85 GB of `*.pt` checkpoint cache, D: now ~198 GB free). **English subtitles + 4 black question cards BUILT** (unverified): `Jaisal-intro\subs\jaisal_intro_english.srt` (15 cues, Jaisal's lines only) + `Jaisal-intro\subs\cards\card_{B,D,F,G}_*.mp4` (2520×1440 @ 24fps, 3s, Malayalam + English, built via `utilities\build_question_cards.py` using ffmpeg `subtitles`/libass for proper Malayalam shaping). **TOMORROW (plan prepared, no action taken — user: "dont act now"):** Phase 0 (no GPU): verify card Malayalam rendering + re-time .srt to the actual concatenated timeline (order `A→card_B→B→C→card_D→D→E→card_F→F1→F2→card_G→G`). Phase 1 (GPU, user): DUB Malayalam (user's voice, RVC/OpenVoice; Jaisal's lines mouth-synced, camera-guy's lines over the cards; NO MUSIC D041). Phase 2 (GPU, user): LatentSync mouth-sync on speaking shots (A, C, E, F1, F2, G). Phase 3 (user, manual): DaVinci assembly (timeline + burn subtitles + swap dub audio + natural SFX + export). Subtitles = permanent decision for the intro AND the main movie. See CURRENT_TASK.md resume point + DECISIONS.md D096 updates 15-17.

**Current state (2026-09-26):** HARD DEADLINE = finish the intro video TODAY (2026-09-26). The A→B cut is visible because the bare bulb's OSCILLATION stops at the cut (shot B starts from A's static last frame). **FIX (user decision, supersedes the "bulb already flickering" idea) = REMOVE the oscillation ENTIRELY — bulb FULLY STATIC in shot A** (A's last frame = still bulb → static shot B cuts seamlessly; B needs no bulb-continuity prompting). APPLIED to `jaisal_intro_A_walkin.json` node 138 (swing line → COMPLETELY STILL + summary lock + negatives; backup `workflow_backups\jaisal_intro_A_walkin.json.pre_static_bulb.bak`; validates clean). B unchanged (already static-bulb). NEXT: user runs A → upscale → lastframe_2k → B's ref_image_0 = A's last frame → run B. Continuation verdict: **NikoDemon80 = visual latent-tail** (use for the A→B→C visual chain); **Ep29 = consistent-audio** (use for the speaking shots). Both packs CONFIRMED installed + registered in ComfyUI 0.34.3. **Neutral upscale (ffmpeg lanczos 2x)** for today's assembly; SeedVR2 parked (plastic look). WanAnimate/viggle nodes registered (parked for object-assembly shots G/J). See CURRENT_TASK.md 2026-09-26.

**Current state (2026-09-20):** Shots A/B/C done. **Shot D v3 (aggressive
non-speaking) = GOOD** (user confirmed); SeedVR2 upscale + last-frame-2K pipeline
wired for take `jaisal_intro_D_reverse_00006_.mp4` (user runs). **Plastic-look
problem diagnosed** (H3 prior + SeedVR2 amplification + chain compounding) →
user's locked direction: **Option 1 natural keyframe anchors + neutral upscaling +
Option 2 (2-3 refs/shot) + seamless continuation (NO hard cuts) + minimal drift**.
**Continuation packs INSTALLED (staged, ComfyUI restart pending):**
`SatoDive/Minimax-H3-Latent-Continuation` (Ep29 consistent-audio route, D092) +
`NikoDemon80/ComfyUI-H3-Motion-Context` v0.6.2 (visual latent-tail, D091).
**ComfyUI version = 0.34.3** (confirmed via `/system_stats`). **NEXT (user, next
week, stop Qwen first):** restart ComfyUI → verify Ep29 workflow loads (check
SLA/sampler/utility nodes) → test D→E continuation (Ep29 vs NikoDemon80) → prep
Shot E (Jaisal SPEAKING, plants grow; `ref_image_0` = `shot_D_lastframe.png`)
with 2-3 natural refs + minimal drift → neutral upscale test. See CURRENT_TASK.md
resume point.

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

**Web-search + loop-guard gateway (added 2026-09-26):**
- `web-search` MCP = `mrkrsl/web-search-mcp` v0.3.1 at `D:\MCP\web-search-mcp\` (tools: `full-web-search`, `get-web-search-summaries`, `get-single-web-page-content`). Chromium installed.
- **Loop-guard gateway** `D:\MCP\mcp-gateway\index.js` (zero-dep Node stdio) sits in front of web-search and enforces hard tool-call limits (total cap, identical-call cap, repeated-sequence, 2-failure block, web budget). `mcp.json` routes `web-search` through it (`GW_BACKENDS=web-search`); `comfy-mcp` stays DIRECT. Backup: `mcp.json.pre-gateway.bak`.
- **ComfyUI MCP has NO open-web search.** Its "search" verbs are registry/catalog lookups only (`models search` = HF/Civitai, `nodes search` = node-pack registry, `templates` = gallery catalog, `knowledge` = local RAG). Its "stay updated" mechanism = registry/catalog refresh: `comfy outdated` (surfaces as `server_info.freshness`), `comfy update`, `templates refresh`, `nodes refresh`. So ComfyUI MCP stays current on its own domain (models/packs/templates/version) but does NOT do open-web research — that's what web-search-mcp + gateway cover. No overlap; ComfyUI MCP left untouched.
- **MCP is CLIENT-attached, not model-attached.** The gateway/web-search/ComfyUI-MCP are configured in the clients (Copilot `mcp.json`, Kilo `globalStorage\kilocode.kilo-code\settings\mcp_settings.json` — Kilo configured 2026-09-26). They work regardless of how the model is launched (`.bat` or llama.cpp web UI). The **llama.cpp web UI is NOT an MCP client** — it's a plain chat frontend, so it has NO tools; use Copilot/Kilo for tool work. Usage guide: `docs/WEB_MCP_USAGE_GUIDE.md` (coding + movie-pipeline research: two-tier = ComfyUI registry first, then web for Reddit/X/GitHub community knowledge; x.com = summaries only, docs.comfy.org = SPA needs browser search).

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
