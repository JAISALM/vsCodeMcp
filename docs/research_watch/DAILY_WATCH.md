# Daily RAG watch — rolling file (D201/D202)

One `## <date>` block appended per daily 09:00 IST run (reminder
`schedule-6479d179`). Format per block: **new relevant items** (what it is +
how it helps us) → **action items** → **source failures** (honest, one line
each). Mondays also get the full extended weekly report
(`docs/research_watch/<date>_weekly.md`).

## 2026-10-27

**Sources:** Reddit ✅ HTML tier (SD 25 + LocalLLaMA 50 + ComfyUI 25 +
artificial 25; comfyui_workflows gated again) · HF ✅ 5 trending + 2
datasets · Civitai ✅ 85 items (hot/newest/ComfyWorkflows/new LoRAs, now
enriched with downloads via detail endpoint) · X ❌ 429 all 7.
**Reddit 50+ today: 73** (top = LocalLLaMA 311u "8 GB GPU, 262K context, 3.5
BPW Qwen-Flash-Next Coder at 70 T/s using llama.cpp").

**New relevant items (vs 10-26 baseline):**
- **198u "I 'hacked' Krea 2 to work with Pose Studio"** (r/StableDiffusion,
  u/foxdit) — Krea2 + Pose Studio bridge for style diversity (complaint:
  Qwen/Klein style diversity). → our Krea2 reference-sheet chain (D021) —
  read the thread for the technique.
- **Civitai "Gladas' Workflow for Krea 2 Turbo"** (3,175 dl, top new workflow)
  — Krea2 Turbo ComfyUI workflow → **ADOPT candidate** for reference-sheet
  speed.
- **Civitai "mini max character replace — with turbo lora 4 steps"** (2,565 dl)
  — H3 character-swap + 4-step turbo → **ADOPT candidate** for our
  charswapmask pipeline + turbo speed.
- **Civitai "ReDetail 2.0: LTX-2.5 video refine + upscale to 4K (workflow +
  CLI)"** (1,688 dl) — LTX-2.5 refine/upscale → **ADOPT candidate** for our
  VFX pipeline (our base model).
- **Civitai "Easy Workflow — MiniMax H3 + Ultimate Upscale for TURBO Hybrid —
  8GB"** (1,689 dl) — H3 upscale chain (we have 32 GB — no constraint issue) —
  review.
- **137u "18 clip reel of my Minimax H3 LoRA on a 3090"** — H3 LoRA trained +
  used on a 24 GB card → input for tonight's LoRA training plan.
- **140u "I finally nailed Moss char loras"** + 157u MOSS-Image-Base LoRA
  (Smartphone Snapshot Photo Reality v14) — MOSS character-LoRA results →
  tonight's training inputs.
- **177u "Flux 3 Image is #1 model"** — Flux-3 adoption signal (our Flux-3-
  Klein reference path).
- **149u "Qwen4-27B's 4-way HC shift?"** + 139u "Qwen4 expectations" — Qwen4
  27B signals continue (writer/agent lineage).
- **131u IBM Granite Speech 5.0 2B** — another small speech model → audio
  pipeline candidate (D041 check: speech is fine, verify no music output).
- **222u ornith-ai/Ornith-1.5-122B** (Qwen finetune; HF 190 likes, 60 k dl) —
  new open 122B candidate.
- **Civitai new LoRAs feed** (top: Not Artists 665 k dl, Detail Tweaker 583 k,
  Hands XL 311 k, blindbox/MoXin/Cute_girl_mix4) — all SD1.5/SDXL/Pony
  detail+style LoRAs → **NO ADOPT** (not our Krea2/H3/MOSS model family).

**ACTION ITEMS (new today):**
1. ⚠️ **llama.cpp CVE-2026-116096** (127u PSA, verified): OOB write in
   Pocket-TTS `pockettts-gen.cpp` on malformed mmproj files; fixed in
   **b11796+** (current b11871); medium. **Our build = b11583** (2026-10-13)
   → below fix line. Real risk ≈ 0 (we never load mmproj / run Pocket-TTS) —
   **update `D:\llama` build at next convenience**, not urgent.
2. Krea2 + Pose Studio hack (198u) — read thread, evaluate for reference-set
   style diversity.
3. Adopt-test: Gladas Krea 2 Turbo workflow + mini-max character replace
   turbo workflow + ReDetail 2.0 (LTX-2.5 4K refine).
4. Tonight's LoRA training — inputs gathered: H3 LoRA 3090 reel (137u), MOSS
   char LoRAs (140u/157u).

**SOURCE FAILURES:** X 429 all 7 · r/comfyui_workflows HTML tier GATED (3
attempts, fresh-profile fallback, no cards) · Reddit JSON 403 all subs (tier 1
dormant) · redlib mirrors both failed (catsarch engine error; perennialte
HTTP 410) · Civitai `/users/{id}` needs auth (401) → authors shown as
`uid:<n>` (stats via detail endpoint work fine).

## 2026-10-26 (baseline — first extended watch, D201/D202)

**Source status:** Reddit ✅ via new HTML top-page tier (`rag/reddit_html_top.py`
— JSON API is IP-walled, HTML page is not); r/comfyui_workflows intermittently
gated; HF ✅ 66 items; X ❌ 429 all 7 accounts; "ComfyUI channel" (Discord)
❌ not directly accessible — awaiting a feed URL from the user; LTX org ✅ no new
models since 09-28.

**Reddit 50+ (last 2 days, pulled live):**
- r/StableDiffusion — 25/25 posts at 50+: H3 ref2va + PS2 style LoRA (231u) ·
  Krea2 Turbo @4-step LoRA (190u) · Hy-Nomas (Tencent video model) native in
  ComfyUI on 12 GB (150u) · FLUX.3 Klein 12-task editing comparison (158u) ·
  MOSS character-LoRA training results (194u) · Fibo2.0 character LoRA same-day
  (149u).
- r/LocalLLaMA — 50/50 posts at 50+: llama.cpp server default port **8080→9931**
  (135u) · Qwen3.8-27B low-quant SSD-streaming prefiller trick (199u) · all
  Qwen-3.8-FN engines benchmarked on a single 5090+128 GB (129u) · Eagle-4
  engine (242u) · Qwen3.8-Flash-Next 125B on 16 GB via NVMe offload (239u) ·
  ISTA GSQ-RCO GGUFs for DeepSeek-V4.1-Flash (203u) · Phonon 31M/40M edge TTS
  (193u).
- r/ComfyUI — 49 posts, none at 50+ this week (top ≈ 43u: selflift-Fish longer
  H3 clips on 16 GB; first H3 scene on a 3090; 2x2 storyboard grid R2V; H3 on
  Apple Silicon).
- r/artificial — 25 posts, none at 50+.

**HF trending relevance (10-25 capture):** sam3 (masks → charswapmask chain) ·
fishaudio/drama-3 (audio — D041 output-class check first) ·
MiniMax-M3.1-Flash (H3 team's LLM) · LTX-2.5 trending (adoption signal) ·
Flux-3-Image-Klein +comfy · DeepSeek-V4.1-Flash (+FP8/GGUF) · Qwen3.8-27B +
distills · Krea2 base (Qwen-Image-2.1) trending · bge-m3/bge-reranker (RAG
upgrade path over MiniLM-384d).

**X:** @ltx_io no new official drop (profile now features community work:
@wildmindai 2D hand-drawn IC-LoRA, CQdesign Enhancer V2).

**ACTION ITEMS (carried from 2026-10-26):**
1. ⚠️ llama.cpp default port 8080→9931 — check our writer/agent server configs.
2. Qwen3.8-27B SSD-streaming prefiller trick — our agent model class.
3. Krea2 4-step turbo LoRA — reference-sheet speed-up candidate.
4. H3 ref2va + style LoRA technique — our video pipeline.
5. Tencent Hy-Nomas (12 GB) — evaluate as H3 alternative.
6. Phonon 31M/40M TTS — D041-safe only if speech/ambient (verify output class).
7. "Background text addition" community LoRA — still absent (3rd check).
8. ComfyUI-LTXVideo pack missing from running install — fix before VFX workflows.
9. User to provide a "ComfyUI channel" (Discord) feed URL to wire into the RAG.
