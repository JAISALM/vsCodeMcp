# Character Sheet — sources, workflows & analysis (created 2026-10-18)

**Purpose:** the single reference for everything related to character-sheet generation in this
project. Reconstructed 2026-10-18 — user had shared these before but the details were lost from
memory. Anything future related to character sheets starts here.

**Standing rule (user directive 2026-10-18): no ComfyUI workflow runs without explicit user
confirmation.** The ComfyUI server is currently DOWN (crashed ~17:12 during a Qwen-2.1 sheet
test) — bring-up also needs the user's go-ahead.

## Sources (user-shared, 2026-10-18)

| # | Source | Link | Working title |
|---|--------|------|---------------|
| P1 | reddit r/comfyui `1wxixua` | https://www.reddit.com/r/comfyui/comments/1wxixua/minimax_h3_image_generation_create_consistent/ | MiniMax H3 image gen — create consistent [character] |
| P2 | reddit r/StableDiffusion `1vov6jb` | https://www.reddit.com/r/StableDiffusion/comments/1vov6jb/create_full_character_location_sheets_in_seconds/ | Full character + location sheets in seconds |
| P3 | reddit r/StableDiffusion `1w2dujd` | https://www.reddit.com/r/StableDiffusion/comments/1w2dujd/i_turned_that_h3_as_an_image_editor_post_into_a/ | "H3 as an image editor" turned into a [workflow] |
| P4 | reddit r/StableDiffusion `1wsb4h3` | https://www.reddit.com/r/StableDiffusion/comments/1wsb4h3/minimax_h3_ref_fizgig_nodes_as_sota_ref2img/ | MiniMax H3 REF + Fizgig nodes as SOTA ref2img |
| P5 | reddit r/comfyui `1wsee1y` | https://www.reddit.com/r/comfyui/comments/1wsee1y/character_sheet_workflow_qwen21/ | Character sheet workflow — Qwen 2.1 |
| HF | HuggingFace `PoopMan333/H3_Character_Sheet_Generator` | https://huggingface.co/PoopMan333/H3_Character_Sheet_Generator/tree/main | H3 character sheet generator (repo) |
| LOCAL | `E:\minimax_workflow\character_sheet\` | (local disk, 4 files, user-placed 2026-10-18) | user-saved workflows — cross-check vs posts |

Local files: `2BZ_H3_character_sheet_2stage_v1_EN.json` (150 KB),
`LEEBLAAB-QwenImage21-Character-SHEET.json` (67 KB), `LocationOrbitSheetH3.json` (26 KB),
`minimaxh sheet patreon.json` (43 KB).
(Also present in `user\default\workflows\character sheet\`: the same 4 + a
`minimax_h3_character_sheet_1wxixua.json` copy.)

**Cross-references (existing memory):** `PRODUCTION_CONSISTENCY.md` "Sources (2026-10-08)" already
listed P4 (`1wsb4h3`), P5 (`1wsee1y` — "workflow already saved"), and P1 (`1wxixua`, "MiniMax H3
consistent character").

## Fetch status (2026-10-18)
- [x] Local workflow inventory + node-level analysis (all 4 files).
- [x] HF repo tree + full README (complete).
- [x] Model + node-pack availability gap check.
- [x] **ALL 5 post bodies fetched 2026-10-18 18:25–18:35 IST — from DSH itself**, via
  `utilities\reddit_browser_fetch.py` (local Playwright Chromium, persistent profile, headless,
  NO session cookie). 5× ~1 MB rendered DOMs + extracted text saved to
  `data\char_sheet_reddit\P{1..5}_dsh.html` / `P{1..5}_text.txt`
  (extractor: `utilities\extract_reddit_text.py`).
- [x] P3 model download links — extracted from the local workflow's note node 20 (6 direct HF URLs).

**Milestone (2026-10-18 18:25):** DSH can now fetch JS-gated Reddit posts itself — same
mechanism as VS Code's integrated browser, no session, no cookies. The helper's `is_gated`
false-positive (bare `recaptcha` substring in the standard page shell) was fixed 18:30 IST
(title-based detection now).

## Reddit fetch routes — tested 2026-10-18 (all blocked)

| Route | Result |
|---|---|
| **`utilities\reddit_browser_fetch.py` (REAL local Chromium, persistent profile)** | **PROVEN — ALL 5 POSTS FETCHED** 2026-10-18 18:25 IST, headless, no session (0.99–1.31 MB rendered DOMs each). The earlier "reCAPTCHA tier" verdict was a **false positive** — see correction below. |
| MCP `get-single-web-page-content` → reddit.com | 403 "Prove your humanity" (JS challenge) |
| harness `web_fetch` → reddit `.json` | 403 |
| `utilities\reddit_fetch.py` (session-cookie helper) | 403 ×3 — the `REDDIT_SESSION_COOKIE` env (from 2026-10-11) is stale |
| `red.artemislena.eu` mirror | Anubis proof-of-work gate (needs browser JS) |
| `rl.bloat.cat` mirror | dead (ECONNRESET) |
| `r.jina.ai` reader proxy | anonymous reddit access blocked until **13:04 UTC (18:34 IST) 2026-10-18** — retryable after that |
| websearch MCP / built-in search | 0 indexed results; built-in web_search has no API key configured |

**Clean fix (one-time user action):** refresh `REDDIT_SESSION_COOKIE` — open reddit.com in the
browser, F12 → Application → Cookies → www.reddit.com → copy the `reddit_session` value and
share it. The helper auto-solves the JS challenge and persists the new cookie
(`C:\Users\user\.dsh\fetch_creds\reddit_cookies.txt`). This route is proven (worked 2026-10-11).

### Root-cause finding (2026-10-18 17:45, user asked "why can't DSH/MCP do this when VS Code could?")
- **The web MCP IS fully capable for the open web** (proven: HF README, repo tree, 6 link-follows
  all extracted fine). No DSH/MCP defect, no code change needed, cookies NOT needed for normal
  sites.
- **Reddit is gated on the server side**, two layers:
  1. JS bot-challenge ("Prove your humanity") for anonymous/headless clients — plain-HTTP
     fetchers (MCP single-page AND MCP search-tool link-follower BOTH hit it) can't execute JS.
  2. **IP burst-block** — ~12 requests/short window from one IP → temporary
     "blocked due to a network policy" page (403s on EVERYTHING incl. cookie'd requests).
     Observed ~17:00–17:40 IST, **cleared ~17:45** (anonymous curl then returned a real
     `theme-beta` page shell).
- Even unchallenged, modern reddit pages are a JS SPA (`theme-beta`) — text fetchers see the
  shell, not the post.
- **Why VS Code could show posts:** almost certainly a browser-based web tool (real Chrome
  passes the challenge) or a moment when the IP wasn't challenged. Verify via the tool name in
  the VS Code agent transcript.
- **Reliable no-cookie route = user's browser console one-liner** (logged in):
  `copy((await fetch('https://www.reddit.com/comments/<ID>/.json?limit=20',{credentials:'include'})).text())`
  → paste JSON back. Fallbacks: fresh `reddit_session` cookie for the helper; jina proxy after
  13:04 UTC.
- **Headless-Chrome live test (17:50 IST, isolated profile, NO session):** real browser from
  this IP got the page shell (171 KB, `shreddit` markers) but the gate **escalated to
  reCAPTCHA** ("Prove your humanity" + gstatic recaptcha script) — plain headless cannot pass
  it; arithmetic `jsc` challenge (helper-solvable) was the earlier tier. Evidence saved:
  `data\char_sheet_reddit\headless_P1_dom.html`. So "run a local browser, no cookies" is ALSO
  gated right now — the tier escalation is tied to this IP's afternoon activity.
- **Why VS Code works without a session (CORRECTED 17:55 IST, live demo):** it is NOT a
  GitHub-cloud egress identity. The VS Code agent's **integrated browser** (Playwright
  Chromium, LOCAL, headed, persistent profile) is a REAL browser that EXECUTES JS. It
  solved Reddit's arithmetic JS challenge (final URL carries `solution=...&js_challenge=1&
  jsc_token=...` — proof the challenge was solved) and rendered the full SPA post. Same
  machine, same IP as DSH — the difference is **browser rendering vs text-only HTTP
  fetch**, not egress identity. DSH's 17:50 headless test hit reCAPTCHA because it was an
  ISOLATED clean profile at peak burst; the headed persistent-profile browser passes the
  tier. (**RESOLVED 18:25 IST:** with the PERSISTENT profile, the HEADLESS helper passed
  all 5 posts — no headed window, no session, no cookies.)
- **Live demo (17:55 IST, P1):** `openBrowserPage` → P1 URL → challenge auto-solved →
  `readPage` extracted the FULL post body (title, flair, 10-image gallery, all links).
  Same URL through the text-only MCP fetcher (`get-single-web-page-content`) returned the
  144-char "Prove your humanity" challenge page. Same URL, same moment, two tools, two
  outcomes — the rendering pipeline is the whole difference.
- **What DSH should do to mimic (best-first):**
  1. **`utilities\reddit_browser_fetch.py` — headless + persistent profile** — VERIFIED
     18:25 IST on all 5 posts (now the standard DSH route for Reddit). An ISOLATED clean
     profile gets challenged; the persistent profile carries challenge state + cookies
     across runs. `--headed` remains the fallback for genuinely gated runs.
  2. **VS Code integrated browser as the reader** (proven working right now) — open the
     URL, `readPage`, paste the extraction. Zero engineering, no session.
  3. **Logged-in browser one-liner** (challenge never applies to a session).

## DSH capability fix (2026-10-18 18:15 IST) — real-browser fetch helper

**Built & proven:** `d:\models\vsCodeMcp\utilities\reddit_browser_fetch.py`
- Drives the **local Playwright Chromium** (`C:\Users\user\AppData\Local\ms-playwright\chromium-1234\chrome-win64\chrome.exe`) with a **persistent profile** (`C:\Users\user\.dsh\fetch_creds\browser_profile`) — the exact mechanism VS Code's integrated browser uses.
- Run with **system Python** (`C:\Program Files\Python310\python.exe` — has `playwright` installed; the embedded ComfyUI python does NOT, and pip there is network-stuck).
- Usage: `python "d:\models\vsCodeMcp\utilities\reddit_browser_fetch.py" <url> [--text] [--out file.html] [--headed]`
- **Proven:** rendered 1 MB of real `shreddit-post` DOM from P1; extracted full HF repo page text clean.
- **Current state (VERIFIED 18:25–18:35 IST):** the helper fetched **all 5 target posts
  headless** from this IP with the persistent profile — no session, no cookies, no headed
  window. The earlier "reCAPTCHA tier" diagnosis (both DSH 17:50 and VS Code 18:15) was a
  **false positive in the gate check**: modern Reddit page shells include a `recaptcha`
  script tag even on fully-rendered post pages (observed at offset ~1598 of a 1 MB
  post DOM that contained the complete post). The reliable gate signal is the challenge
  **`<title>Reddit - Prove your humanity</title>`** — `is_gated` was fixed 18:30 IST to
  title-based detection. `--headed` remains available as a fallback for genuinely gated
  runs.
- **This is the answer to "make DSH capable":** DSH's web profile is a text-only HTTP fetcher (curl) — it cannot execute JS, so it can never pass the challenge. The fix is this helper: DSH (or the user) runs it via the shell tool instead of its built-in web fetch for Reddit. No DSH config change needed — it's a shell-callable script.

## Per-post explanations (ACTUAL post bodies fetched 2026-10-18 18:25–18:35 IST via DSH
`reddit_browser_fetch.py` — see `data\char_sheet_reddit\P*_text.txt`)

### P1 — "MiniMax H3 Image Generation Create Consistent Character Sheets in ComfyUI" (r/comfyui 1wxixua)
- **Author:** u/cgpixel23 ("Top 1% Poster"), 14 days ago, flair **Tutorial**.
- Memory (10-08): "MiniMax H3 consistent character: r/comfyui 1wxixua".
- **ACTUAL POST BODY (extracted 2026-10-18 17:55 IST via VS Code integrated browser):**
  "Hello everyone, I've just finished a new ComfyUI workflow that allows you to use
  **MiniMax H3 as an image generation model** and create detailed character sheets from a
  single reference image or a batch of images. The main goal is to use these character
  sheets as stronger references for **more consistent video generation**, giving you
  multiple views and details of the same character. The workflow is simple to use: load
  the required MiniMax H3 models, load your image or batch of images, choose the number of
  steps (**8 steps for faster generation or 25 steps for the best results**), and click
  Run. ... consistency is very good ... if we compare this to qwen image 2.1 H3 is clearly
  winner here in therm of quality because the results are with resolution of 4096x1536 vs
  x1664x928 for qwen, the consistency is slightly better. As for the generation time qwen
  is definitely faster here:"
  - Gen time 25 steps 12 mins (Minimax H3 Turbo Fused)
  - Gen time 6 steps 4.5 mins (Qwen 2.1+ Viggle4 Steps LORA)
  - **Workflow link:** https://drive.google.com/file/d/1v4NC6vEGN2uDxO2_L05g1q0JPkeoSsYo/view?usp=sharing
  - **Civitai article:** https://civitai.com/articles/36126/minimax-h3-image-generation-create-consistent-character-sheets-in-comfyui
  - **Video tutorial:** https://youtu.be/vy-oWQJwNgw
  - 10 images in the post (gallery, "Item 1 of 10").
- **What it is (corrected 18:35 IST — actual body fetched):** cgpixel23's workflow = use
  **MiniMax H3 as an IMAGE GENERATION model** (not video-orbit) to build character sheets from a
  single ref or a batch; sheets then serve as stronger refs for consistent video gen.
  8 steps (fast) / 25 steps (best). Native **4096×1536** output. "Minimax H3 Turbo Fused"
  naming ⇒ the **fused turbo model** (cf. P4's `fused_refdelta_r1024_turbo8`).
- **Workflow (Drive):** https://drive.google.com/file/d/1v4NC6vEGN2uDxO2_L05g1q0JPkeoSsYo/view?usp=sharing
  — likely = the saved local `user\default\workflows\character sheet\minimax_h3_character_sheet_1wxixua.json`
  (filename carries the P1 id).
- **Civitai article (model links + details):** https://civitai.com/articles/36126/...
- **Video tutorial:** https://youtu.be/vy-oWQJwNgw

### Related (not P1): PoopMan333 HF repo `H3_Character_Sheet_Generator` (user-shared separately)
- **Different approach:** H3 as a **VIDEO** model — slow 360° orbit (character statue-still, no
  hard cuts) from up to 9 refs → grab **6 frames** (4 in the faster version) → stitch = sheet
  with guaranteed consistency (six frames from ONE pass can't drift).
- A-Prompt (user: per-ref what to take / what to **ignore**) + B-Prompt (spin/pose/lighting;
  "general purpose" A prompt since 10 Sept makes it near-effortless). Optional outputs: 360 spin
  video + every frame.
- **Files:** `H3_CharSheetMaker_6_Panel.json` (front/sides/back + 2 face shots),
  `H3_CharSheetMaker_4_Panel_(Faster).json` (~40% fewer frames, 73 vs 124),
  `H3_ExpressionsSheetMaker_6_Panel.json` (experimental 22 Sept), `B prompts/`, `early_version/`,
  `old/`, `examples/`.
- **Update log:** 10 Sept — turbo LoRA → `minimax_h3_turbo_v4_step600_ema`; 29 Aug — speed-up
  nodes, **8 steps instead of 25** with speed-ups; 22 Sept — expressions sheet.
- **Models:** `minimax_h3_ref2va_pruned_int8_convrot` (diffusion_models/),
  `qwen3vl_32b_minimax_h3_int8_convrot` (text_encoders/ — we have the nvfp4_awq equivalent),
  `minimax_h3_video_vae_int8_convrot` + `minimax_h3_audio_vae_fp32` (vae/), optional turbo LoRA.
  INT8 low-VRAM builds; higher-precision text encoder = better prompt adherence.
- **Custom nodes:** near-vanilla; only the optional Speed Ups group needs **KJNodes + rgthree**.
- License: minimax-h3-community-license.

### P2 — "Create FULL Character & Location Sheets in SECONDS with this workflow and Custom Node!" (r/StableDiffusion 1vov6jb)
- **Author:** u/lumos_ai, 2 months ago, flair **Workflow Included**.
- **The custom node = `OrbitSheets`** — FREE, public: **https://github.com/lumosai8/ComfyUI-OrbitSheets**.
  Two templates (the local file is the LOCATION template):
  - **Character sheet:** type a character description → full turnaround (front, side profiles,
    back, close-ups) — and it **generates voice audio** so the character can literally speak.
    8 steps with the Turbo LoRA (up to 20/35 for detail).
  - **Location sheet:** describe any place → interior & exterior multi-angle shots. **Interior mode**
    (hallways/rooms) vs **exterior mode**; camera toggle: **cut views** (separate static angles)
    vs **continuous move** (full 360 camera tour) — "sometimes one gives better results than the
    other, so it helps to try both".
  - **Smart frame selector** picks the best shots automatically and arranges a clean sheet;
    controls for image count, columns, padding, frame size.
  - **Both use MiniMax H3 with the Krea2 anchor frame + the Krea2 Turbo model** — example files
    pre-set ("drop them in and start generating"). Built in ~2 days; more templates planned.
- **Local match: `LocationOrbitSheetH3.json`** (location template — interior/cut-views matches the
  post's description exactly) — two chains:
  (a) **Krea2 t2i** location image (`Krea2_Turbo_convrot_int8mixed` UNET + `qwen3vl_4b_fp8_scaled`
  CLIP krea2 + `qwen_image_vae`, 1920×1080) →
  (b) **H3 image-to-video orbit** of that location (`minimax_h3_fl2va_pruned_int8_convrot` UNET +
  `qwen3vl_32b_minimax_h3_nvfp4_awq` CLIP minimax + `minimax_h3_video_vae_fp16`, LoRAs
  `minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy` @1.0 + `minimax_h3_ref_lora_rank_256_bf16`
  @1.0, 1216×672 @ 124 frames, 8 steps euler/simple, MiniMaxH3SigmaShift 12.0/3.0).
- Frame handling: **OrbitSheetsFrameSelect** (6 frames, selector = **`vision_llm`** — content-based
  frame picking), **OrbitSheetsContactSheet** (2×2), `CreateVideo`/`SaveVideo` (24 fps).
- Custom pack: **OrbitSheets** (`OrbitSheetsLocationPrompt` — "interior / cut views / auto",
  `OrbitSheetsAttentionBackend` = "comfy kitchen (int8)") — **pack NOT installed here**.
- (Earlier guess "ethanfel derivative" SUPERSEDED: the author is **lumosai8**, pack =
  `github.com/lumosai8/ComfyUI-OrbitSheets` — the local file is one of its two templates.
  ethanfel's `H3_Cinematic_Multishot_Coverage` (HF) remains a related resource referenced by
  PoopMan333's README for room-orbit coverage.)

### P3 — "I turned that 'H3 as an image editor' post into a full character sheet workflow — front/side/back + poses, all local" (r/StableDiffusion 1w2dujd)
- **Author:** u/inazma44, 2 months ago, flair **Workflow Included**. (The 2BZ file is the
  author's own distribution version — "English edition intended for public distribution".)
- **Inspiration post (linked from the post + the file's note node 69):**
  r/StableDiffusion `1vr1i18` "MiniMax H3 as an image editor — 6 edits in one shot".
- **Structure (from the post):** Stage 1 = one face photo + one outfit image → front/side/back.
  Stage 2 (optional, OFF by default) = 1–4 more panels (poses, props, expressions, backgrounds)
  → composited into a **16:9 sheet**.
- **Exact setup (from the post):** MiniMax H3 **ref2v int8 pruned** + **4-step Turbo LoRA @0.75**
  + **T=1 image VAE** ("the bit that makes it emit a still instead of a clip") + **er_sde /
  sgm_uniform, 8 steps**. On a **3090 24GB**: Stage 1 ~100–125 s, Stage 2 ~105 s → ~3.5 min
  total (first run slower = model loading).
- **Known issues (from the post):** props repeat across panels (ask for one sword, get three);
  back-view hair goes flat; lying & sitting poses unreliable.
- **Workflow (public):** https://github.com/nicekriss/toobusy/blob/main/docs/workflows/2BZ_H3_character_sheet_2stage_v1_EN.json
  — **= our local file exactly.** Needs **rgthree** (installed ✓) + **toobusy** (search "toobusy"
  in Manager, publisher `neobabae`, **v0.4.9+** — repo github.com/nicekriss/toobusy — NOT
  installed). 6 LoadImage nodes go red on open (author's local files — point at our v6 sheets).
- **THE 6 REQUIRED MODELS + EXACT DOWNLOAD LINKS** (extracted from the file's note node 20,
  2026-10-18):
  1. `minimax_h3_ref2va_pruned_int8_convrot.safetensors` → diffusion_models/ —
     https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors — **HAVE ✓**
  2. `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` → loras/ —
     https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/loras/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors — **HAVE ✓**
  3. `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` → text_encoders/ —
     https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors — **HAVE ✓**
  4. `minimax_h3_t1_image_vae_step1597.safetensors` → vae/ (T=1 image VAE — the still-emitter) —
     https://huggingface.co/Mamad8/MiniMax-H3-Image-VAE/resolve/main/minimax_h3_t1_image_vae_step1597.safetensors — **MISSING ✗**
  5. `minimax_h3_audio_vae_fp32.safetensors` → vae/ —
     https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_audio_vae_fp32.safetensors — **HAVE ✓**
  6. `gemma4_e4b_it_fp8_scaled.safetensors` → text_encoders/ (Gemma describes the Stage-2 pose
     image + analyzes enabled optional refs; NOT used for Stage-1 face/outfit) —
     https://huggingface.co/Comfy-Org/Gemma4/resolve/main/text_encoders/gemma4_e4b_it_fp8_scaled.safetensors — **MISSING ✗**
  > Note-node rule: "This workflow uses a **T=1 VAE for still images**. Use a Video VAE for
  > ordinary H3 video generation."
- **Local match: `2BZ_H3_character_sheet_2stage_v1_EN.json`** — by **Too Busy Grasshopper (2BZ)**,
  YouTube @toobusyAI.
- **Structure:** Stage 1 = H3 orbit front/side/back sheet of **Picture 1 = face/identity** +
  **Picture 2 = outfit only**; Stage 2 (optional, default OFF) = 1–4 **action panels** entered
  as plain-English "Panel N: ..." requests ("jump while aiming the water gun") + a final
  horizontal 16:9 composite — i.e. H3 used as an IMAGE EDITOR over the sheet.
- **Reference semantics (the clever part):** 6 LoadImage slots — face/identity, outfit, optional
  prop/weapon, optional environment, optional extra accessory, Stage-2 pose. Three
  `ToobusyMiniMaxH3SemanticReference` nodes assign explicit `<Picture N>` jobs
  ("Picture 3 = environment — use only its location/surfaces/atmosphere/lighting; do not copy
  people or text"). Four `TextGenerate` nodes run a LOCAL LLM (CLIP `gemma4_e4b_it_fp8_scaled`,
  type krea2) to analyze the optional refs → "VISUAL_REFERENCE: YES/NO" lines + a
  "POSE TRANSFER:" block.
- **Models:** UNET `minimax_h3_ref2va_pruned_int8_convrot` ✓, CLIP
  `qwen3vl_32b_minimax_h3_nvfp4_awq` (type minimax) ✓, image VAE
  `minimax_h3_t1_image_vae_step1597` ✗, audio VAE `minimax_h3_audio_vae_fp32` ✓, turbo LoRA
  `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16` @0.75 ✓; sampling chain KSamplerSelect
  `er_sde` + BasicScheduler + SamplerCustomAdvanced + RandomNoise + BasicGuider;
  `ToobusyMiniMaxH3ImageLatent` 1344×768; save prefix `charsheet/H3_2STAGE_STAGE1_3VIEW`.
- **Packs:** **toobusy** (publisher `neobabae`, ≥ v0.4.9) ✗ NOT installed, **pysssss**
  (MathExpression, ImageConcanate) ✗ NOT installed, KJNodes ✓, rgthree ✓,
  ModelAttentionBackend (comfy kitchen) ✓, subgraph 40bb7e22 (14 nodes: 2nd orbit pass,
  ImageCrop, ImageConcanate, SaveImage).

### P4 — "MiniMax H3 REF + Fizgig Nodes: As SOTA (Ref2Img \ Img2Img) True Image Editing Model, Native 4096x1536 in 1 Minute, WF + Prompt for Every Example" (r/StableDiffusion 1wsb4h3)
- **Author:** u/-Ellary-, 20 days ago, "Top 1% Commenter", flair **Workflow Included**.
  Memory (10-08): already listed.
- **From the post:**
  - **WF + prompts for every example:** https://civitai.red/posts/31291351 (the "patreon" local
    file = this post's workflow).
  - **Nodes:** https://github.com/shootthesound/ComfyUI-Fizgig-H3-Still — **INSTALLED here ✓**
    (`ComfyUI-Fizgig-H3-Still` pack).
  - 4096×1536, **18 steps in 1 min (5060 Ti 16 GB)**; stellar prompt/spatial understanding;
    **no LLM-processed prompts needed per image**; imitates vast amounts of styles from the REF;
    great world knowledge / smart with concepts; sharp images, low artifacts; **way faster than
    Qwen 2.1 at 2+ image references**.
- **Local match: `minimaxh sheet patreon.json`** — a **sprite-sheet-style single-frame sheet**:
  **FizgigH3StillLatent (4096×1536) + FizgigH3StillDecode** — TRUE single-frame stills from H3
  (crisp, no banding; pack `ComfyUI-Fizgig-H3-Still` INSTALLED ✓) — plus
  `MiniMaxH3ReferenceToVideo` (prompt: "[reference generation] static image of sprite sheet..."),
  `LoadImageListFromDir //Inspire` feeding a WHOLE FOLDER of refs (`D:\character sheet`),
  `easy cleanGpuUsed` ×3 (Easy-Use ✓), `ImageScaleToTotalPixels`, and a custom H3-attention
  subgraph (`H3SLAAttention`, `MiniMaxChunkFeedForward`, `MiniMaxLowVRAMAttention`,
  `MiniMaxH3SigmaShift` — served by installed H3-Optimizations / Spectrum / chunk-star7 packs).
- **Hero model:** `minimax_h3_fused_refdelta_r1024_turbo8_mystic07_int8_convrot.safetensors`
  (weight dtype `fp8_e4m3fn`) — a **fused ref-delta turbo-8** single model (reference
  conditioning baked in — the "REF" of the title) ✗ MISSING.
- **CLIP:** GGUF `minimax\qwen3vl-32B-MiniMax-H3-Q2_K.gguf` via `CLIPLoaderGGUF`
  (ComfyUI-GGUF ✓) ✗ GGUF file MISSING.
- VAE `minimax_h3_video_vae_int8_convrot` ✓. Timing table in the file: 8 steps 4.4 min / 10 → 6 /
  16 → 7 / 25 → 12 (megapixel table).

### P5 — "Character Sheet Workflow - Qwen2.1" (r/comfyui 1wsee1y)
- **Author:** u/LeebLaab, 20 days ago, flair **Workflow Included**. Memory (10-08): "workflow
  already saved".
- **From the post (fetched 18:30 IST):** LeebLaab found a workflow, edited most of it, and
  **REMOVED the local-LLM nodes** — so the sheet prompt is drafted by **ANY LLM** (he uses
  "Qwen chat"): upload 1 image + the exact instruction prompt → LLM responds with the drafted
  10-section prompt → feed it to the workflow. "I tested the new sheets in minimax video, and
  results are fantastic."
  - **Original workflow (entire credit, linked from the post):**
    https://www.reddit.com/r/StableDiffusion/s/Rjoz79yECS
  - **Key for us:** we have local LLMs (Qwen PE / Gemma writer) — we can draft the 10-section
    sheet prompt locally from the v6 sheets, no cloud needed.
- **Local match: `LEEBLAAB-QwenImage21-Character-SHEET.json`** (filename author = LeebLaab ✓) — a SUBGRAPH
  pipeline: UNET `qwen_image_2.1_bf16` (or the author's `qwen_image_2.1_int8_convrot` variant) +
  CLIP `qwen3vl_8b_int8_convrot` + VAE `qwen_image_2.1_vae_bf16` →
  `TextEncodeQwenImage21` (sheet prompt + reference image = i2i) → `QwenImage21Cache` →
  KSampler (25 steps euler/simple, seed, schedulers "res_2m"/"beta") → VAEDecode →
  **VAEDeGrid 4× zoom** → `ImageStitch` → `ImageResizeKJv2` (nvidia_rtx_vsr → 1536) →
  `SaveImageAdvanced`.
- A MarkdownNote carries the **"Character Sheet Prompt Architect"** system prompt: input ONE
  reference image + entity name → output a 10-section sheet prompt (layout zones A–F, hero pose,
  turnaround, expression row, wardrobe, metadata column, style, lighting/palette, quality
  contract; every rendered string in English double quotes).
- Resolution presets: **1.0 MP fast / 3.4 MP balanced / 6.0 MP best** (default 6 MP, 16:9).
- **Models:** `qwen_image_2.1_bf16.safetensors` ✓ (13.3 GB), `qwen3vl_8b_int8_convrot` ✓
  (8.7 GB), `qwen_image_2.1_vae_bf16` ✓ (0.6 GB). The author's `qwen_image_2.1_int8_convrot`
  UNET variant ✗ missing → bf16 must be used.
- **CAUTION (tested 2026-10-18 ~17:12):** a headless run of this workflow with the bf16 UNET
  **crashed the ComfyUI server** (probably VRAM: 13.3 GB UNET + 8.7 GB CLIP + 1536 px + 4× zoom
  decode on the 32 GB 5090). If retried: lower the resolution (1–3.4 MP), free VRAM first, or
  obtain the int8_convrot variant. Also: the multi-angle turnaround format of this sheet was
  **rejected by the user** ("not the correct one") — do not run it without explicit confirmation.
- **Packs:** QwenImage21Cache / TextEncodeQwenImage21 / ModelAttentionBackend ✓, KJNodes
  (ImageResizeKJv2, SaveImageAdvanced, ResolutionSelector) ✓, DeGrid (VAEDeGrid) ✓.

## Local workflow ↔ post mapping

| Local file | Post | Route | Ready on this machine? |
|---|---|---|---|
| `minimax_h3_character_sheet_1wxixua.json` (saved workflows folder — filename carries P1's id; verify = cgpixel23's Drive file) | **P1** | H3 as IMAGE-GEN sheet (single/batch ref → 4096×1536 sheet, 8/25 steps) | models per Civitai article 36126 (likely "H3 Turbo Fused" = the P4 fused model ✗); KJNodes/rgthree ✓ |
| (PoopMan333 HF repo — related, NOT P1) | — | H3 360° **video orbit** → 6 frames → sheet | ref2va ✓, video VAE int8 ✓, audio VAE ✓, turbo4step ✓; int8_convrot 32B CLIP ✗ (have nvfp4_awq equivalent — likely swappable); v4 turbo LoRA ✗; KJNodes + rgthree ✓ |
| `LocationOrbitSheetH3.json` | **P2** | Krea2 t2i → H3 fl2va location orbit → contact sheet (OrbitSheets LOCATION template) | 3 models ✗ (Krea2_Turbo_convrot_int8mixed, lightx2v turbo, ref_lora_rank_256); **OrbitSheets pack ✗** (free: github.com/lumosai8/ComfyUI-OrbitSheets — also has the CHARACTER template + voice audio); vision LLM for frame select |
| `2BZ_H3_character_sheet_2stage_v1_EN.json` | **P3** | H3 2-stage (ref2va): face+outfit → front/side/back, optional action panels, 16:9 composite | Models 4/6 ✓; gaps = **2 model downloads (direct HF links — see P3) + toobusy pack (github.com/nicekriss/toobusy, ≥0.4.9) + pysssss** |
| `minimaxh sheet patreon.json` | **P4** | H3 Fizgig-still sprite sheet (4096×1536 native, fused ref-delta turbo8, folder of refs) | 2 models ✗ (fused_refdelta, Q2_K GGUF CLIP — WF+prompts at civitai.red/posts/31291351); Fizgig + Easy-Use ✓; post: 18 steps ≈ 1 min (5060 Ti 16 GB) |
| `LEEBLAAB-QwenImage21-Character-SHEET.json` | **P5** | Qwen 2.1 i2i design sheet (multi-angle) — local-LLM nodes REMOVED by author; any LLM drafts the 10-section prompt (original: reddit s/Rjoz79yECS) | All 3 models ✓; int8_convrot UNET variant ✗; **OOM risk on bf16** (crashed server); format rejected by user |

## What we HAVE (models, main tree `E:\ComfyUI_windows_portable\ComfyUI\models`)
- `minimax_h3_ref2va_pruned_int8_convrot.safetensors` (diffusion_models)
- `minimax_h3_fl2va_pruned_int8_convrot.safetensors` (diffusion_models)
- `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` (text_encoders)
- `minimax_h3_video_vae_fp16` + `minimax_h3_video_vae_int8_convrot` + `minimax_h3_audio_vae_fp32` (vae)
- `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` (loras)
- `qwen_image_2.1_bf16.safetensors` (13.3 GB, diffusion_models), `qwen3vl_8b_int8_convrot`
  (text_encoders), `qwen_image_2.1_vae_bf16` (vae)
- Krea2 line: `Krea2Realism_V1`, Krea2 V2 LoRA, `krea2_identity_edit` LoRA, `qwen3vl_4b_fp8_scaled`,
  `qwen_image_vae`
- Packs: KJNodes, rgthree-comfy, ComfyUI-Easy-Use, ComfyUI-GGUF, ComfyUI-Fizgig-H3-Still,
  ComfyUI-DeGrid, ComfyUI-H3-FaceRefine, H3-Optimizations, ComfyUI-Spectrum-MiniMax-H3,
  minimax-h3-chunk-star7, Minimax-H3-Latent-Continuation, ComfyUI-MiniMax-H3-Turbo,
  minimax-h3-semantic-bridge, ComfyUI-H3-Multishot, ComfyUI-H3-Project-Suite, …

## What is MISSING (with exact source, verified 2026-10-18)
| Item | Needed by | Exact source |
|---|---|---|
| `minimax_h3_t1_image_vae_step1597.safetensors` (T=1 image VAE — the still-emitter) | P3/2BZ | **HF direct:** https://huggingface.co/Mamad8/MiniMax-H3-Image-VAE/resolve/main/minimax_h3_t1_image_vae_step1597.safetensors |
| `gemma4_e4b_it_fp8_scaled.safetensors` (TextGenerate CLIP) | P3/2BZ | **HF direct:** https://huggingface.co/Comfy-Org/Gemma4/resolve/main/text_encoders/gemma4_e4b_it_fp8_scaled.safetensors |
| `Krea2_Turbo_convrot_int8mixed.safetensors` | P2 | OrbitSheets repo example files / author (lumosai8) |
| `minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy.safetensors` | P2 | HF (lightx2v lineage) |
| `minimax_h3_ref_lora_rank_256_bf16.safetensors` | P2 | OrbitSheets repo / author (lumosai8) |
| `minimax_h3_fused_refdelta_r1024_turbo8_mystic07_int8_convrot.safetensors` | P4 | **civitai.red/posts/31291351** (post's WF+prompts page; may be patreon-gated) |
| `minimax\qwen3vl-32B-MiniMax-H3-Q2_K.gguf` | P4 | **civitai.red/posts/31291351** (author's GGUF) |
| `minimax_h3_turbo_v4_step600_ema.safetensors` | P1 (recommended turbo) | HF PoopMan333 repo / MiniMax |
| `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` | P1 (CLIP; nvfp4_awq equivalent exists — verify swap) | HF (convrot conversions) |
| `qwen_image_2.1_int8_convrot.safetensors` | P5 (author variant; bf16 works but OOM-risky) | author's conversion (LeebLaab) |
| Pack **toobusy** (publisher `neobabae`, **≥ v0.4.9**) | P3/2BZ | **github.com/nicekriss/toobusy** (Manager: search "toobusy") |
| Pack **pysssss** (ComfyUI-SSS-Nodes) | P3/2BZ | ComfyUI Manager |
| Pack **OrbitSheets** | P2 | **github.com/lumosai8/ComfyUI-OrbitSheets** (FREE — node + character & location templates) |
| Pack **Inspire** (`LoadImageListFromDir //Inspire`) | P4 | ComfyUI Manager |

## Next steps (AWAITING USER CALL — nothing runs without confirmation)
1. ~~Fetch post bodies~~ **DONE 2026-10-18 18:35** — all 5 via DSH `reddit_browser_fetch.py`
   (no session needed).
2. Pick the sheet route (ranked by readiness on THIS machine):
   - **P3 (2-stage 2BZ)** — 2 small HF model downloads (direct links above) + toobusy pack +
     pysssss; proven ~3.5 min on a 3090 24 GB ⇒ fine on the 5090 32 GB; face+outfit →
     front/side/back is the closest format to our locked v6 sheets.
   - **P4 (Fizgig still)** — 2 models (civitai.red post) but the fused model may be
     patreon-gated; native 4096×1536 single-frame sheet; Fizgig pack already installed.
   - **P1 (cgpixel23 image-gen sheet)** — verify the local
     `minimax_h3_character_sheet_1wxixua.json` = the Drive file; models per Civitai article
     36126.
   - **P2 (OrbitSheets)** — free pack but 3 missing models (author conversions); location
     template is what we have locally; the CHARACTER template (+ voice audio) is new.
   - **P5 (Qwen 2.1)** — all models present but bf16 OOM crashed the server ~17:12 and the
     multi-angle format was rejected by the user.
3. Download missing models/packs, wire the LOCKED v6 sheets (`input\char1_sheet.png` /
   `char2_sheet.png`) as references, then run — with explicit user confirmation.
4. Bring the ComfyUI server back up (currently down) — also needs the user's go-ahead.
