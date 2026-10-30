# Daily RAG watch — rolling file (D201/D202)

One `## <date>` block appended per daily 09:00 IST run (reminder
`schedule-6479d179`). Format per block: **new relevant items** (what it is +
how it helps us) → **action items** → **source failures** (honest, one line
each). Mondays also get the full extended weekly report
(`docs/research_watch/<date>_weekly.md`).

## 2026-10-30

**Sources:** Reddit ✅ HTML tier (SD 1 new/25, artificial 25 new/25, LocalLLaMA +
ComfyUI 0 new — all 403-JSON walled as usual; **comfyui_workflows GATED 6th
day** — browser tier rendered no shreddit cards) · HF ✅ 16 items · Civitai ✅
85 items (author tier production: named authors throughout) · X ❌
login-walled (7 accounts, browser tier ran, no `X_AUTH_TOKEN`/`X_CT0`).
**Pipeline note:** 08:00 schtask fetched + indexed (199 items) then got
**TERMINATED ~08:06** (exit 267009 = SCHED_S_TASK_TERMINATED — likely machine
sleep; only the final log line was lost). 08:13 manual re-run confirmed
idempotent completion: 0 new items, 0 newly indexed, store 1,218.

**New relevant items (vs 10-29 baseline):**
- **445u "Qwen3.8-Flash-Next tried to send a diagnostic file to a remote
  location, while stating otherwise"** — privacy/security post about our Qwen
  family running locally — quick read.
- **434u "TokenGate (Stanford/Berkeley): token-gated attention for long-context
  prefill"** — prefill speed tech relevant to our 260K ctx.
- **227u "New MiniMax H3 Finetune by Pika Labs"** — H3 pipeline ADOPT candidate.
- **168u "NVIDIA's new Open-H3-Regenerate-2K"** — H3 2K regeneration.
- **212u "Qwen Image 2.1 + TRELLIS.2 in Blender: prompt → textured rigged
  character → village"** — Qwen Image 2.1 + 3D pipeline signal.
- **184u "Flux 3 Image is #1 model"** — Flux 3 image release chatter.
- **197u "Interactive neuron steering playground for Qwen3.5-4B on WebGPU
  locally"** — interesting interpretability tool.
- **290u/1228 mistralai/Mistral-Large-4-1T-A52B** — day's top HF model (1T
  MoE — far beyond 32 GB; noted, not runnable here).
- **GPU-unlock cluster continues** (175u "lower power limit when unlocked" ·
  143u info post on which consumer cards/tasks · 134u "59% higher throughput
  on 3090 Ti") — all 30-series; Blackwell excluded → N/A for our 5090.
- **MOSS cluster** (229u tips · 226u char-LoRA results · 197u showcase · 166u
  variety tests · 159u "nailed Moss char loras" · 152u hype-psyop debate · 144u
  MOSS-Image-Edit-HQ v3) — noted; user opted out of MOSS checking.
- **HF new:** LiquidAI **LFM3-Omni-2B (206) + LFM3-VL-2B (167)** — new LFM3
  variants (b11960 runs LFM3 natively → optional local tests) ·
  nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D (30) · nvidia/Granary-v2
  (25).
- **Civitai: no new ADOPT candidates** — same top 10 (Gladas Krea 2 Turbo
  3,250 dl · kimimorgam char-replace 2,604 · Dasiwa Xtra 2,141 · LTX 2.3
  Director 2,053 · H3+Ultimate Upscale 1,769 · ReDetail 2.0 1,715 · H3
  Infinite Iteration 1,497 · Krea 2 Workflows 1,455 · H3 Looping 1,301 ·
  Gladas Anima 1,233 — all author-named). newloras = same legacy set →
  **NO ADOPT**.

**ACTION ITEMS (new today):**
1. **Pika Labs H3 finetune** (227u) + **NVIDIA Open-H3-Regenerate-2K** (168u)
   — inspect for the H3 pipeline.
2. **TokenGate** (434u) — read for long-context prefill implications (260K ctx).
3. **Qwen3.8-Flash-Next diagnostic-file post** (445u) — quick read (Qwen
   family, local-trust angle).
4. **LFM3-Omni-2B / VL-2B** — small, native on b11960 — optional test.
5. Carried: X cookies (`X_AUTH_TOKEN`/`X_CT0`) · H3 Relay Hires / Openjutsu /
   Krea2 BBOX / PixText reads · candidate-model tests (DeepSeek-V4.1-Flash /
   flint) · 3 Civitai adopt-tests.

**SOURCE FAILURES (tier status per D203):** X — tier 3 login-walled (browser
ran; no cookies set). r/comfyui_workflows — browser tier GATED 6th day. Reddit
JSON 403 all subs (HTML tier carries 4/5). redlib mirrors dead (410). Civitai
author tier ✅ production (all top-10 author-named).

## 2026-10-29

**Sources:** Reddit ✅ HTML tier (SD 49 + LocalLLaMA 47 + ComfyUI 25 +
artificial 25; comfyui_workflows GATED — 5th day) · HF ✅ 11 items · Civitai
✅ 85 items — **author tier production-verified: 83 named / 2 uid** · X ❌
login-walled (cookies not set). **08:00 schtask ran cleanly for the first
time in 3 days (machine awake) — 96 new items, no manual fetch needed.**
96 Reddit posts at 50+ (top: 1275u BF16-unlock).

**New relevant items (vs 10-28 baseline):**
- **1275u "RTX 3000 series can run BF16 almost 2× faster — NVIDIA locked it
  via kernel, not a hardware limit"** — day's top post; GPU-unlock cluster
  continues (Blackwell still excluded → N/A for our 5090, but the kernel-lock
  mechanism is confirmed).
- **993u "Krea 2 king of styles!"** — adoption signal for our Krea2 base.
- **511u "Openjutsu — one-click character swap (ComfyUI Higgsfield
  challenge)"** — character-swap node pack → ADOPT candidate for our
  charswapmask chain.
- **406u "Character Reference for Anima is released!"** — Anima ecosystem
  (our Gladas Anima candidate workflow).
- **296u "H3 Relay Hires node: 0.5 → 2 MP upscaler, ~4× faster than native"**
  — H3 pipeline **ADOPT candidate**.
- **297u "PixText: small fast model for fixing text in generated images"** —
  text-fix tool for our title compositing.
- **225u "Krea2 BBOX models have finished training and been released"** —
  Krea2 ecosystem expansion (bounding-box conditioning).
- **252u "testing minimax h3 ref2va with my ps2 style lora"** — validates our
  ref2va + style-LoRA technique · 271u H3 SLA + 8-step-LoRA
  lighting/physics tests.
- **306u "PSA: 10Eros-Max Beta 7 is out"** — new SD-family checkpoint.
- **MOSS cluster** (346u sft-normal-people, 253u MOSS-Image-Edit LoRA, 228u
  tips) — noted; user opted out of MOSS-image checking.
- **HF new:** tencent/Hy-SimulMT-30B-A3B-FP8 (380) · openbmb/MiniCPM-OCR-1.0
  (278) · NVIDIA-Nemotron-3.5-Transcribe-30B-A4B (205 — speech-to-text,
  D041-safe input-side) · secemp9/arxiv-complete dataset (744).
- **Civitai: no new ADOPT candidates** (same top 10, downloads rising: Gladas
  Krea 2 Turbo 3,225 · kimimorgam char-replace turbo 2,588 · ReDetail 2.0
  1,713 — authors now show real names). newloras still the legacy
  SD1.5/SDXL/Pony set → **NO ADOPT**.

**ACTION ITEMS (new today):**
1. **H3 Relay Hires node** (296u) — inspect pack/workflow (0.5→2 MP upscaler
   for our H3 route).
2. **Openjutsu character swap** (511u) — inspect for the charswapmask chain.
3. **Krea2 BBOX models** (225u) — quick read: what does BBOX conditioning
   give us for reference-sheet work?
4. **PixText** (297u) — text-fix option for title compositing.
5. Carried: X cookies (`X_AUTH_TOKEN`/`X_CT0`) · candidate-model tests now
   possible on b11960 (DeepSeek-V4.1-Flash / RecursiveSI-flint) · 3 Civitai
   workflow adopt-tests · Krea2+PoseStudio read.

**SOURCE FAILURES (tier status per D203):** X — tier 3 login-walled (browser
ran, no `X_AUTH_TOKEN`/`X_CT0` set). r/comfyui_workflows — browser tier
GATED 5th day (no further tier exists for that sub). Reddit JSON 403 all
subs (tier 3 HTML carries 4/5). redlib mirrors dead. Civitai author tier ✅
production (83 named / 2 uid — tier ran inside the venv subprocess fix).

## 2026-10-28

**Sources:** Reddit ✅ HTML tier (SD 25 + LocalLLaMA 48 + ComfyUI 25 +
artificial 25; comfyui_workflows gated again — 4th day) · HF ✅ 9 items ·
Civitai ✅ 85 items — **author resolution now live: all 48 unique authors
resolved via browser tier (0 unresolved); files patched with real names** ·
X ❌ all 7 login-walled (tier 3 browser ran; cookies still not set).
08:00 schtask missed again (machine asleep) — manual fetch run, 302 newly
indexed. **73 Reddit posts at 50+** (top 340u "everything will be local
eventually").

**New relevant items (vs 10-27 baseline):**
- **223u "Mysterious Qwen4 Appearance by New GitHub Accounts"** — Qwen4
  signals intensify (writer/agent lineage watch).
- **GPU-unlock cluster (new theme today):** 240u "GPU unlocks (FP32
  accumulation): why Turing/Ampere/Ada but not Blackwell" · 236u "free 3090
  speedup hack, verified 15% PP / 5% TG" · 179u "CMP170HX-inspired unlocks
  30x/40x, up to 2× prefill speedup" · 168u "lower power limit when
  unlocking" → GPU/VRAM-trick reading for our 5090 (Blackwell is NOT in the
  unlockable set — consistent with our 5090 being locked).
- **219u "Ling-3.1-flash-1019 weights out + base model released"** (Ant) —
  fast-model writer-candidate family; +190u Ling-3.0-flash-Sante (124B /
  5.1B active) from yesterday.
- **217u "My MOSS Character Lora Training Results" + 172u "MOSS-Image Vision
  Text Encode (ComfyUI node + workflow)"** — MOSS char-LoRA cluster continues;
  the **ComfyUI node + workflow for MOSS's vision text encoder is NEW** →
  ADOPT candidate if we adopt MOSS for image work.
- **198u + HF 194-likes "NVIDIA Nemotron-3.5-Bolt-E4B-4GB"** — 4 GB MoE that
  runs anywhere (edge agent option; not a writer/agent replacement for us).
- **148u "⚠️ PSA: Fake GitHub projects — especially AI tools & ComfyUI custom
  nodes"** — supply-chain security → verify origins of the node packs we
  install via ComfyUI-Manager (esp. new packs before `install_node`).
- **180u "neuron-steering playground for Qwen3.5-4B in-browser WebGPU"** ·
  **177u "35B MoE at 20.5 tok/s on an iPhone"** · 173u "NVIDIA/OpenShell
  private runtime for autonomous AI agents" (context) · 161u "ZPix local
  open-source app adds lasso inpainting" (our charswapmask is ComfyUI-native —
  note only).
- **HF new:** baidu/Unlimited-OCR-2 (256 likes — OCR) · LiquidAI/LFM3-1.7B
  (208) · ccore/Qwen3.5-4B-3D-Coder (181) · bones-studio/seed dataset (350
  likes) · nvidia/simready-central-library (51) · Rapidata text-to-3d-with-
  llm-code (42).
- **Civitai workflows — NO new adopt candidates today:** top 10 = same as
  10-27 (downloads rising): Gladas Krea 2 Turbo (3,201) · mini-max char
  replace turbo 4-step (2,577) · H3 Dasiwa Xtra (2,122) · LTX 2.3 + Director
  (2,048) · H3 + Ultimate Upscale 8 GB (1,713) · ReDetail 2.0 LTX-2.5 4K
  (1,700) · H3 Infinite Iteration (1,472) · Krea 2 Workflows (1,414) · H3
  Looping/Morphing (1,274) · Gladas Anima (1,205).
- **Civitai new LoRAs — still NO ADOPT:** same legacy SD1.5/SDXL/Pony
  detail/style set (Not Artists 665 k, Detail Tweaker 583 k/461 k/410 k,
  Hands XL 311 k, blindbox 307 k, MoXin 288 k, Velvet Mythic Fantasy 246 k
  — the only Krea2-tagged one, style LoRA, D021 candidate — unchanged),
  Cute_girl_mix4 231 k, Disney Princess XL 208 k.

**ACTION ITEMS (new today):**
1. GPU-unlock reading (240u/236u/179u/168u) — confirm none applies to our
   5090 (Blackwell excluded per 240u) — 10-min read, close the thread.
2. MOSS-Image Vision Text Encode ComfyUI node/workflow (172u) — inspect the
   pack + workflow before any MOSS adoption.
3. Fake-GitHub PSA (148u) — quick check that our installed node packs match
   their registry origins.
4. Carried (10-27): llama.cpp b11583 CVE-2026-116096 update at convenience ·
   Krea2+PoseStudio hack read · adopt-test the 3 Civitai workflows · X
   cookies (`X_AUTH_TOKEN`/`X_CT0`) — the X tier is wired and waiting.

**SOURCE FAILURES (tier status per D203):** X — tiers 1+2 429 all 7; tier 3
browser head ran per account: pages render but timeline is login-walled
(article shells, zero tweet text) → **still awaiting `X_AUTH_TOKEN`/`X_CT0`
from user** (one-time). r/comfyui_workflows — browser tier GATED 4th day
(3 attempts, fresh-profile fallback). Reddit JSON 403 all subs (tier 3 HTML
carries 4/5). redlib mirrors dead. Civitai `/users/{id}` 401 → **resolved via
browser tier today (48/48 authors, 0 unresolved)** — the uid placeholders are
gone.

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

**SOURCE FAILURES (tier status per D203 — browser head is now the standing
last tier):**
- **X:** tiers 1+2 (syndication, mcp engine) 429 all 7 → **new tier 3 browser
  head ran today: profile pages render but the timeline sits behind the LOGIN
  wall (article shells, zero tweet text; nitter mirrors dead, threadreader
  404 — all verified live).** Unlocked by one-time env `X_AUTH_TOKEN`
  (auth_token) + `X_CT0` (ct0) — same pattern as `REDDIT_SESSION_COOKIE`;
  tier injects the cookies and reads the full timeline. **AWAITING USER COOKIES.**
- **r/comfyui_workflows:** browser tier GATED (3 attempts, fresh-profile
  fallback, no cards — 3rd day). Next tier: none known for this sub (small,
  intermittently challenge-gated) — retry daily.
- **Reddit JSON 403** all subs (tier 1 dormant — IP wall, proven cookie
  doesn't beat it) → HTML top-page tier (tier 3) carries 4/5 subs.
- **redlib mirrors:** both dead (catsarch engine error; perennialte HTTP 410).
- **Civitai `/users/{id}` 401** no-auth → **browser tier wired today**: model
  pages SSR `href="/user/<name>"` (verified: ReDetail 2.0 author = u/bambushu);
  `fetch_civitai` now resolves unresolved authors via ONE browser session +
  cache (`news/state/civitai_users.json`). Today's 85 files stay `uid:<n>`
  until the next run's cache fills.

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
