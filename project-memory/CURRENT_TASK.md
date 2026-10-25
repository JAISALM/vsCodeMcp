# Current Task

## 🔴 TOP (2026-10-25 ~17:15 IST) — **A/B/C/D FastH3 controlled comparison test — READY FOR USER (D200). User runs A→B→C→D after stopping Qwen.**

User's request (16:49): test all four FastH3 workflows with **same prompt + same reference**, 15 s, 1 MP, "consistent and professional", named A/B/C/D; "this is the biggest test for fast and reliability". **All four standardized files BUILT + VALIDATED (0/0) in `user\default\workflows\`:**
- **A** = `ABCD_test_A_FastH3_Omni_R2V_LOCAL.json` (was `FastH3_Omni_R2V_LOCAL.json`, backup `*.ABCD.bak`) — NVFP4 QAD 13 GB route.
- **B** = `ABCD_test_B_H3_HyperFlow_Fast_LOCAL.json` (was `H3_HyperFlow_Fast_LOCAL.json`, backup `*.ABCD.bak`) — int8 21 GB + HyperFlow 8-step LoRA.
- **C** = `ABCD_test_C_FastH3_OmniRef_TEMPLATE.json` (copy of template `video_fasth3_ominiref_r2v.json`) — int8 22 GB OmniRef route; **gained the video-ref wiring** (new nodes 200 VHS_LoadVideo `distracted_guide.mp4` + 201 ImageResizeKJv2 ← ResolutionSelector, links 300–304 → `ref_videos.ref_video_0` slot 5 / `ref_video_audios.ref_video_audio_0` slot 6).
- **D** = `ABCD_test_D_FastH3_i2v_TEMPLATE.json` (copy of template `video_fastvideo_fasth3_i2v.json`) — FastVideo H3 V2 i2v route.

**Shared spec:** canonical Jaisal R2V prompt (D041 no-music) · refs `char1_sheet.png` + `distracted_guide.mp4` · **15 s** (362 frames) · **1 MP** (A/B/C 1376×768; D follows ref aspect ~896×1152) · seed **363275252574302 FIXED** (A/B were randomize) · save prefixes `ABCD_A_FastH3OmniR2V` / `ABCD_B_HyperFlowFast` / `ABCD_C_OmniRefTemplate` / `ABCD_D_FastH3i2vTemplate` (output ROOT — so outputs are unambiguous). D prompt = canonical minus the `<Video 1>` clause (i2v has no video channel; first_frame = char1_sheet). A/B: duration 4→15, scheduler named-steps 10→8, LoadImage named → actual file; C: picture yellow_plane→char1_sheet, duration 5→15, seed→fixed; D (subgraph internals are authoritative per AGENTS rule): prompt/seed/duration set on internal nodes 104/15/111 **and** instance 105, ImageScaleToTotalPixels 0.4→1.0 MP, first frame red_line_barrier→char1_sheet.
**Diagnosis delivered:** A's missing output = it was there: `output\Video_00002-audio.mp4` (15.08 s, 1376×768, 24 fps, audio) — A saves to the output ROOT with prefix `Video_`; the on-disk file's widgets lag the canvas (duration widget 4 vs canvas 15). **B's 00:11:12 run left NO `Video_*` file in the output root** — check B's canvas save node (bypassed prefix?) before running the test.
**TWO PHASES (user: "no video ABCD first, then with video"):**
- **PHASE 1 (FIRST) — no-video:** `ABCD_test_A_FastH3_Omni_R2V_LOCAL_novideo.json` · `ABCD_test_B_H3_HyperFlow_Fast_LOCAL_novideo.json` · `ABCD_test_C_FastH3_OmniRef_TEMPLATE_novideo.json` · `ABCD_test_D_FastH3_i2v_TEMPLATE_novideo.json` — A/B had nodes 13/17 (VHS load + resize) deleted + video-ref inputs cleared; C had nodes 200/201 removed; ALL FOUR share ONE identical text-described prompt (motion in words: "walks down a busy city street, glances to the side with a surprised expression, then continues walking") + ref = char1_sheet.png only. Save prefixes `NV_A_…/NV_B_…/NV_C_…/NV_D_…` (output root).
- **PHASE 2 (SECOND) — with-video:** the four files WITHOUT the `_novideo` suffix (prefixes `ABCD_…`), video ref = `distracted_guide.mp4` (Distracted Boyfriend meme — inherited from the community swap-workflow example inputs; only its motion/camera/audio are used, content not copied).
- All eight files `validate_workflow` clean (0/0).
**USER RUN ORDER:** stop Qwen → **phase 1**: A→B→C→D `_novideo` → **phase 2**: A→B→C→D (video). **Record per run:** total wall time ("Prompt executed in …"), s/it, staged VRAM (MiniMaxH3 …MB), graph breaks, output filename/duration/res/audio, visual quality. First-pass uncontrolled baselines (afternoon runs, 8 steps): A 17.41 s/it · B **74.62 s/it** · C 16.39 s/it · D 22.44 s/it. Models all verified on disk (`E:\ComfyUI_windows_portable\ComfyUI\models`). One-shot test files → NOT mirrored to the repo (per D131 one-shot rule); spec + results live in D200 + EXPERIMENTS.md.

## 🔴 TOP (2026-10-25 ~15:55 IST) — **Frontend update applied (user: RAM/VRAM node "got removed" → hypothesis stale frontend). `easy cleanGpuUsed` (ComfyUI-Easy-Use) VERIFIED PRESENT in live `/object_info` — node was never removed; 207 `easy*` classes loaded on 0.42.5. Frontend packages updated: comfyui_frontend_package 1.55.18 → **1.57.3**, comfy-kitchen 0.2.39 → 0.2.40, comfy-aimdo 0.5.6 → 0.6.0; workflow-templates 0.11.96 + embedded-docs 0.5.14 already latest on index. USER ACTION: RESTART ComfyUI (running server serves old 1.55.18 frontend from memory) + **hard-refresh browser (Ctrl+Shift+R)** — stale cached JS bundle is the likely reason the node "disappeared" from the UI. Rollback if UI breaks (frontend now newer than the 0.42.5-pinned 1.55.18/0.2.39/0.5.6): `pip install comfyui_frontend_package==1.55.18 comfy-kitchen==0.2.39 comfy-aimdo==0.5.6`.

## TOP (2026-10-25 ~12:10 IST) — **Option A STAGE 2 APPLIED: ComfyUI core 0.37.0 → v0.42.5 + nvvfx 0.2.0.0 (user back, asked "updated the front end and backend so i can resume P9?" → chose agent-kills-processes). Server is STOPPED — USER MUST START via run_nvidia_gpu.bat.**

**What was done (12:00–12:08):** (1) killed the 4 server python processes (port 8188 freed); (2) `finish_nvvfx_upgrade.bat` → **nvvfx 0.2.0.0 clean** — `Effect` + `QualityLevel` importable (the VFX pack's `cannot import name 'Effect' from 'nvvfx.effects'` is FIXED); (3) `update_core_0425.bat` — its `git log --format="%h %ad %s"` lines were eaten by cmd batch-param expansion (bat bug, fixed in the file with `%%` escaping), so the remainder ran manually: **`git checkout v0.42.5`** (tag, commit 483dae43, tree clean) → **`pip install -r requirements.txt`** → installed `comfyui-frontend-package 1.55.18` · `comfyui-workflow-templates 0.11.96` (+ new subpackages core/json/media-assets) · `comfyui-embedded-docs 0.5.14` · `comfy-kitchen 0.2.39` · `comfy-aimdo 0.5.6` (the versions v0.42.5's requirements actually pin; earlier notes' 1.57.1/0.2.40/0.6.0 were estimates). `transformers 5.9.0` + `hf-hub 1.33.0` UNTOUCHED (whisper fix holds).
**Verification ALL GREEN:** core import smoke (`comfy.model_patcher`+`nodes`+`execution` = CORE CHAIN OK) · `main.py` compiles · frontend package `static/` assets present · **all 4 launcher flags exist in 0.42.5 cli_args.py** (`--windows-standalone-build` `--reserve-vram` `--disable-cuda-malloc` `--enable-manager` → `run_nvidia_gpu.bat` needs NO change) · **pack-import diff vs baseline (rebuilt harness `data\pack_import_test_0425.py` + `data\diff_pack_import_tmp.py`): 0 REGRESSIONS** — no pack that imported OK on 0.37.0 now fails; remaining standalone FAILs = same known harness artifacts as baseline (`PromptServer.instance` ×11, `mediapipe.solutions` ×1) + `ComfyUI_Nvidia_VFX_Nodes` now OK (real fix). Harness caveat: the rebuilt test's entry-point selection counts 0 classes for most packs (not comparable to baseline counts) — the authoritative pack check is the SERVER STARTUP LOG (real loader).
**WITHERS PIPELINE PROVEN END-TO-END (run 5aa3a334, 13:29:47, SUCCESS — first completed withers run):** output `output\minimax\staticvlog\shot_00001-audio.mp4` (10.13 s, 480x864, 24 fps, aac audio). User reported "output is different, not our video" — DIAGNOSIS (frames + audio verified): ① video content = AUTHOR'S Withers vlog character/scene (gothic undead woman in candlelit chapel — matches the prompt 1:1 in every frame) — it is NOT our Jaisal/Zidhan movie, because the template is the author's vlog and only Mithun's VOICE was wired in · ② the three `LoadImageCrop` ref nodes loaded OUR images (`jaisal_t2i_base_00001_.png` = Jaisal, `2 closeUp.png`, `seedvr2_2k_kf6_00011_.png` = today's v21a frame — the author's images were never bundled) but **H3 IGNORED them — the detailed text prompt dominated** (no Jaisal anywhere in the video) · ③ AUDIO = 100% Mithun's real voice: mp4 audio track vs first 10.13 s of `02_mithun_story.wav` → RMS-envelope **correlation 1.0** (true audio reuse, not re-synthesized) · ④ character speaks + gestures per prompt (frame 3 mid-speech, frame 4 open-palm gesture) · ⑤ video is only ~10 s — the 124 s story cannot fit, only its first ~10 s plays (expected long-test semantics) · ⑥ full prompt verified: 6114 chars, {{transcript}} correctly replaced with the whisper English translation of the Malayalam story, D041 no-music respected. **REMAINING TIDY-UP:** `audio_load_cap` still 0 (this run loaded 02_+03_ = 248 s; set back to 1); counter was 1 (shot 3 → index 2 → file 02_). **TO MAKE IT "OUR VIDEO":** the template is a framework — rewrite subject_definitions/detailed_description for Jaisal/Zidhan + our scene, feed our character sheet as Picture 1; the whisper→transcript→lip-sync pipeline is fully generic. Pipeline now proven on 0.42.5 + sage 2.2.0: counter → per-shot audio → whisper (offline) → English transcript → long prompt → H3 with sage patch (no OOM) → video + Mithun audio.
**SAGEATTENTION 2.2.0 INSTALLED (2026-10-25 13:3x, user: "why cant we set that up?"):** source = sanjxz HF `sageattention-2.2.0-blackwell-sm120a` → **`sageattention-2.2.0-cp313-cp313-win_amd64.whl`** (cp313 = our python 3.13.12 EXACT; sm_120a = 5090; 7 MB; URL `huggingface.co/sanjxz/sageattention-2.2.0-blackwell-sm120a/resolve/main/...`). Prebuilt community cp311 wheels (mobcat40) unusable (python tag mismatch); PyPI sageattention FROZEN at 1.0.6; no MSVC on machine (no VS2022/cl) so source build was the only other route — wheel made it moot. ISOLATED TEST FIRST (session_tmp\sage_setup\sage_test via `pip install --target`): KJNodes contract (per_thread_int8_triton, per_warp_int8_cuda, per_block_int8_triton, per_channel_fp8, get_cuda_arch_versions, attn_false) ALL PRESENT · `get_cuda_arch_versions() = ['sm120']` · `sageattn()` real GPU probe OK on torch 2.12.0+cu130 (ABI clean) · 2.2.0 public surface: `core, quant, sageattn, sageattn_qk_int8_pv{16,fp8}_cuda{,_sm90}, sageattn_qk_int8_pv_fp16_triton, sageattn_varlen, sm80_compile, sm89_compile, triton`. PACK COMPAT SCAN (11 importers): ALL SAFE — WanVideoWrapper's guarded `sageattn_varlen` import now SUCCEEDS (new attention mode activated = feature), seedvr2 compat layer written for 2.x, T8/H3-Optim `smooth_k` hits are their OWN wrapper sigs (2.2.0 sageattn swallows unknown kwargs via **kwargs — no crash). BACKUP of 1.0.6 (22 files) = `session_tmp\sage_setup\sageattention_1.0.6_backup`; rollback = `pip install sageattention==1.0.6 --no-deps` (PyPI) or restore backup. **RUNNING SERVER STILL HOLDS 1.0.6 IN MEMORY — USER MUST RESTART ComfyUI for KJNodes to re-detect sm120** (the `_cuda_archs` capture happens at import time). POST-RESTART: ① un-bypass the withers "MiniMax H3 Mem Eff Sage Attention Patch" node ② queue withers (counter 0 → shot 1 → 01_mithun_story.wav) ③ T8 SLA/EAV-Strict-Sage paths now functional. **GOTCHA (permanent): embedded python has `python313._pth` → `PYTHONPATH` ENV IS IGNORED — use `sys.path.insert(0, ...)` for isolated-package tests.** **TODAY'S PLAN (user): P9 (7-item sheet — withers = item 6) + P10 (9-item sheet) experiments both today; LoRA training TONIGHT (details TBC).**
**withers 5th failure = NEW node (audio pipeline PASSED — counter fix confirmed): `MiniMaxH3MemoryEfficientSageAttentionPatch` (KJNodes/minimax, ltxv_nodes.py:2183, marked EXPERIMENTAL) raised "sageattention is not new enough version or could not determine CUDA architecture":** installed **sageattention 1.0.6** (predates Blackwell); 5090 = sm_120; the node's `_cuda_archs` is computed **at KJNodes import time** (`from sageattention.core import get_cuda_arch_versions` in try/except → None on 1.0.6/sm_120) so a pip upgrade mid-session won't help the RUNNING server — **immediate fix = BYPASS the node in the UI** (right-click → Bypass, turns yellow; it's a pure model passthrough VRAM-optimization, model in → model out; 32 GB 5090 + int8 pruned H3 should fit on standard attention). If OOM after bypass: free_memory/--reserve-vram path. PROPER FIX (later, stop window): Blackwell sageattention **2.2.0** — community prebuilt wheels exist for 5090 (mobcat40/sageattention-blackwell, sanjxz HF `sageattention-2.2.0-blackwell-sm120a`) but they target torch 2.11 nightly + CUDA 12.8 while this machine has **torch 2.12.0+cu130** → ABI fit must be verified before install; 11 packs import sageattention (KJNodes, minimax-h3-audio-T8, PlagueKind, ThinkingLLM, WanVideoWrapper, CRT-Nodes, H3-Optimizations, RES4LYF, seedvr2, toobusy, TTS-Audio-Suite) — most use the stable top-level `sageattn()`, KJNodes' `sageattention.core` internals are try/except-guarded (worst case: patch node stays unavailable). RECOMMENDATION: bypass + queue now; sage 2.2.0 wheel task is a separate stop-window project.
**withers 4th crash (13:02, b5aa1119) — user's "i made it 0" was the WRONG widget:** run history shows counter 5006 crept 2→3→4 across runs; the 13:02 run had **5006=4 AND `audio_load_cap`=0** — the user had set the **cap** widget inside the red node to 0 (thinking it was the index), not the separate 5006 counter node. Cap 0 = unlimited files; the shot math still computed index 5 (shot 6) → crash. INSTRUCTIONS GIVEN: ① Ctrl+F → `Run Counter` → the small node 5006 "Run Counter (set to 0 before each batch)" (currently 4) → set 0 (the red node's `start_index` row is WIRED — the value can only come from the counter) · ② red node `audio_load_cap` back to **1** (one file per shot; 0 joins all) · ③ Queue (red Error badge only clears on the next run) · ④ on green: check ShowText + video, Ctrl+S canvas. Counter history: 12:39 run=2/cap1 → shot 2 idx1 (1 file then), 12:53 run=3/cap1 → shot 4 idx3 (3 files), 13:02 run=4/cap0 → shot 6 idx5.
**withers 3rd crash root cause = Run Counter, not files (user 12:53, "same error"):** run 93e920fb's prompt revealed the full counter chain: **5006 `PrimitiveInt` "Run Counter (set to 0 before each batch)" = 3** (user never reset it) + 5409 "Total Generations (odd) = Batch Count" = 3 → 5410 "Shot Number (odds first, then evens)" = `2a+1 − b·min(1, max(0, a−(b+1)/2+1))` = **4** → 5005 start_index = 4−1 = **3** → `files[3:]` empty → crash (dir had indices 0-2). **FIX = user one-click: set node 5006 to 0 before each batch** (the node's own title says so); batch order then: counter 0→shot 1→01_, 1→shot 3→03_, 2→shot 2→02_ (files named = shot numbers, all present). I cannot click the user's canvas — this value is the only manual step. ALSO DISCOVERED: **user's live canvas DIVERGES from the on-disk file** (canvas has start_index wired ← 5005 + 5410/5411/5006/5409 chain; on-disk 5206 has literal start_index=0, no link) → user must Ctrl+S the canvas once the run works so file-side management is possible. Whisper re-confirmed passing in run 93e920fb's executed list (5420 ran).
**Voice wiring for withers (user: "wire one of jaisals voice there" → "take a longer one... midhuns audio around 2 minutes... this is a long workflow we should test that"):** dir now = **`01_`/`02_`/`03_mithun_story.wav`** — all three = **124.16 s Mithun story monologue** (Malayalam, dub-pipeline cleaned; source `D:\models\ai-movie\references\mithun\MITHUN_AUDIO_MALAYALAM_2_clean.wav`, mono 16 kHz 16-bit), the LONG-AUDIO test. **ROOT CAUSE of the repeated "No audio files to load (check start_index ...)" crash (found via `/history` on the user's failed run 0766ece5):** node 5206's `start_index` is **WIRE-linked in the canvas to node 5005 `easy mathInt` (a − b = shot − 1)** — the node's title is "Audio for this shot (index = shot - 1)"; the run's prompt shows `"start_index": ["5005", 0]`, so the node loads ONE file per shot (cap=1, Alphabetical ASC): shot N → file index N−1. The counter output ≥ 1 while the dir held only index 0 → `files[1:]` = empty → raise. FIX: duplicated the story to indices 0, 1, 2 (shots 1–3 all resolve). On-DISK file still has literal `start_index: 0` (unlinked) — the canvas wiring is the live truth. Whisper note: only the CURRENT shot's file is transcribed (cap=1) → long prompt = one 124 s transcript ×4 slots. Long-test expectations: video 124 frames @ 24 fps ≈ 5.2 s → character speaks the FIRST ~5 s of the story; ShowText shows the full whisper transcript. Different lines per shot = replace 02_/03_ with other clips. If the full story needs to be ON SCREEN = multi-clip seamless chain (H3BlockTailAnchor tail-chaining) or a longer `length` widget (author set 124 — H3 per-clip max unknown, don't guess). Voice pools: `Jaisal-intro\dubs` · `ai-movie\references\jaisal\jaisal_1..10_clean.wav` · `ai-movie\03_audio_processed` (RVC/Mithun variants, incl. `mithun_ml1_in_jaisal_v7.wav` 78.5 s).
**withers re-queue on 0.42.5 (user, ~12:20): whisper PASSED (offline load worked — crash now happens LATER), died at `LoadAudioBatchFromDir` (#5206): `FileNotFoundError: No audio files to load` — the dir had only README.txt. Root cause: the node HARD-RAISES on an empty dir (line 166), and the prompt blob uses the dir's joined audio as the character's DIALOGUE (`<Subject 1> (S1) speaks in the voice from <Audio 1>: <d>[English] {{transcript}}</d>`, {{transcript}} ×4, audio also → `<Audio 1>`/`ref_audios.ref_audio_0`). FIX (no workflow edit): **`00_placeholder_silence.wav`** (3 s, 16 kHz mono, pure digital silence) dropped in the dir → node loads it, whisper transcript ≈ empty → {{transcript}} slots blank → character speaks nothing, run completes. README in the dir rewritten (node mechanics, accepted extensions, sort_method note — default is "None" not alphabetical, delete-placeholder-before-real-run). In-workflow verification: the ShowText node displays the actual whisper transcript (if whisper hallucinates on silence, it will be visible there — adjust then).
**NEXT (user, 15:55 update):** ⓪ **RESTART ComfyUI + hard-refresh browser (Ctrl+Shift+R)** — frontend 1.57.3/kitchen 0.2.40/aimdo 0.6.0 just installed, takes effect at restart; then verify `easy cleanGpuUsed` (RAM/VRAM node) is back in the UI node search (server side already verified present — this is a UI/cache issue) → ① ~~restart + un-bypass + re-queue~~ **DONE — withers run SUCCEEDED** (5aa3a334, 13:29; video = `output\minimax\staticvlog\shot_00001-audio.mp4`; Mithun audio verified 1.0 correlation; see entry above) → ② withers-rewrite for OUR characters = **DEFERRED by user (15:32: "add pending task, we will come back to this; let me try with others") → PENDING_ITEMS.md P9 item 4** (TODO list there: 5416 prompt rewrite + ref alignment + `audio_load_cap` 0→1 + counter reset + Ctrl+S canvas) → ③ **user is now trying the OTHER experiments** (remaining P10 sheet items: P10_WORKFLOW_SHEET.md — FastH3 Omni R2V · CharSwap v1.1-fro · H3_HyperFlow_Fast/sol_h3 refs · RTX Post VFX · Motion2MixamoRig · Qwen3-TTS · H3-Person-Removal · VNCCS PoseStudio · TTS suite) — support on request; agent does NOT queue runs (D192) → ④ TONIGHT: LoRA training (details TBC — which character/LoRA? dataset curation on request) → ⑤ `prep_swap_run.py` for swap/vlog prep when resumed.
**Rollback if anything breaks:** `git -C E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI checkout v0.37.0` (the tag is still local) + `pip install -r requirements.txt` (0.37.0's) — packs/models were never touched.

## 🔴 (2026-10-25 ~11:45 IST) — **v21a GREEN (allocator fix CONFIRMED live) + withers whisper-crash FIXED + swap-prep helper built (user away 11:00–~12:00; D192 held — ZERO workflows queued).**

**v21a GREEN (user: "that works"):** 10:34–10:54 run on 0.37.0 with `--disable-cuda-malloc` confirmed in the live args → the upscaler `resource already mapped` crash is GONE (SyncTile 30 regions, canvas 2208×2848, 226 frames, out `output\Bruxos\teste_v001.mp4`). Upscaler sync patch still in place. User quality note: pipeline works; output "pretty lame" — blamed on **prompt quality + mask quality** ("masking was not quite good"); the p9 character-swap-mask workflow "didnt really worked because of the prompt maybe" → **deprioritized** ("i will put some more time in this when there is an actual need").
**Option A stage 2:** ~~pending user's next stop-window~~ **APPLIED 2026-10-25 ~12:08** (see the newer TOP entry above — core at v0.42.5, nvvfx 0.2.0.0, 0 pack regressions; server STOPPED, awaiting user start).

**Whisper crash (user's `withers_has_big_nattys_LOCAL` run 10:58–11:07, died after 360.80 s at node 5420 `TT-LoadWhisperModel`):** `OSError: Can't load the model for 'openai/whisper-large-v3'` → root cause = HF cache dir `C:\Users\user\.cache\huggingface\hub\models--openai--whisper-large-v3` was **weight-less** (only config.json 0 MB, refs, .no_exist) so the node's `from_pretrained(model_id, use_safetensors=True)` triggered a runtime download that died mid-file on the **xet CDN** (`File reconstruction error: CAS Client Error … us.aws.cdn.hf.co/xorbs/…`). The pack (`custom_nodes\ComfyUI-TranscriptionTools\components\load_whisper_model.py`) hardcodes a 12-entry model_id combo — **no local-path option, no retry** → **FIX = pre-populate the cache** (the node then loads 100 % offline). **FIX COMPLETE + VERIFIED (~11:50):** background job (embedded python, `HF_HUB_DISABLE_SYMLINKS_WARNING=1`) downloaded all 11 needed files (single `model.safetensors` 3.09 GB + config/tokenizer set; fp32 shards deliberately skipped) → **verified the node's exact call offline: `from_pretrained("openai/whisper-large-v3", use_safetensors=True)` → `WhisperForConditionalGeneration` loaded from cache in ~1 s** (no network). No `.incomplete` leftovers. Script `data\whisper_preload_tmp.py`. **No pack code was touched** (zero-risk fix). The `torch_dtype deprecated` warning in the load output is cosmetic (transformers 5.9).
**Second latent blocker FOUND + FIXED (same run would have died next):** `LoadAudioBatchFromDir` (#5206 + paired #5451 PrimitiveNode) pointed at **`W:\StableDiffusion\ComfyFlux\Comfy_UI_V61\ComfyUI\output\prepped_audio\withers`** — a W: drive that DOES NOT EXIST on this machine (stale path from the workflow author). → both widget values (positional + named, 4 occurrences) repointed to **`E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\prepped_audio\withers`** (dir created + README.txt: one audio file per vlog clip, alphabetical, D041 no music). Backup `withers_has_big_nattys_LOCAL.json.bak_audiofix_20261025`. Workflow validated still-clean shape (node/link counts preserved).
**Non-fatal warning noted (don't chase):** 2× `int() argument must be a string... not 'NoneType'` at 11:06:23 = UUID-template nodes with unmapped optional INT widgets during prompt conversion; run proceeded normally. File left untouched.
**MIMIC HELPER BUILT (user's ask: "get a video + add prompt + proper images… manual labour… mimic and dont mess things up"):** `utilities\prep_swap_run.py` — one-command prep that CLONES a template swap/vlog workflow and swaps in the manual parts, template NEVER modified, structure (nodes/links) verified preserved, only widget values changed (positional + named). Tested OK on BOTH templates: (a) charswapmask → `--video/--sheet/--track` (+ auto prompt word-substitution of the tracking word); (b) withers → `--ref0/1/2` (slot-mapped via the R2V node's `ref_images.ref_image_N` inputs) + `--audio-dir` (builds `output\prepped_audio\<dir>` + README + syncs the paired PrimitiveNode). Also `--prompt-file` (full prompt replacement), `--list-images` (candidate refs from char_refset/char_sheet/refset_v6/v7). **D192: the helper WRITES FILES ONLY — user queues the result.**
**INTEGRITY SWEEP (11:50, ALL 12 CHECKS GREEN — "make sure its not breaking"):** bat `--disable-cuda-malloc` ✓ (+standalone/manager flags) · upscaler sync patch ✓ · withers valid JSON, 0 stale W: paths, local audio path ×4, 50 nodes/72 links preserved, backup on disk ✓ · charswapmask UNTOUCHED (still `distracted_guide.mp4`, 32/43) ✓ · whisper cache 11/11 files (3.09 GB) ✓ · audio dir + README ✓ · no `.incomplete` leftovers ✓. Repo state: mirror re-synced (36 files), commits `d52c871` + `b8b2613` pushed.
**NEXT (user's call when back):** ① ~~confirm whisper preload~~ **DONE (verified offline load)** → ② re-queue `withers_has_big_nattys_LOCAL` — whisper now loads offline; audio dir is local (`output\prepped_audio\withers\` — drop voice clips there, or leave empty / switch off the whisper branch if not needed) → ③ use `prep_swap_run.py` for the next swap/vlog run → ④ Option A stage 2 (`update_core_0425.bat`) in the next stop-window.

## 🔴 TOP (2026-10-25 ~10:05 IST) — **ComfyUI core update PLAN (user chose Option A ~09:45): v21a retry on 0.37.0 FIRST, then 0.42.5. All prep DONE (zero impact on the running server).**

**Research (192 commits behind, v0.42.5, 5 minor releases):** **the allocator crash is NOT fixed upstream** — `cuda_malloc.py` unchanged across all 192 commits (only #16746 = auto-disable pinned memory on *integrated* GPUs — not our case); `--disable-cuda-malloc` remains the official fix and the flag EXISTS in 0.42.5 (verified in upstream `comfy/cli_args.py`) → the bat launcher needs no change after the update. H3-relevant: LightVAE support (v0.39 LynnReal + v0.41 #17049), H3 VAE tile blending (#16436 v0.38), single-head LoRAs on H3 PDD head banks (v0.42.3), core `ImageSDRToHDR` node (v0.41), higher-quality Save Video encode defaults (v0.39), assorted crash fixes. **Dependency bumps (checked vs our env):** `comfyui-frontend-package` 1.57.1 · `comfyui-workflow-templates` 0.11.96 · `comfyui-embedded-docs` 0.5.14 · **`comfy-kitchen` 0.2.35→0.2.40 (the Krea2 engine — our movie-still workhorse)** · `comfy-aimdo` 0.6.0 · torchaudio requirement dropped (nothing uninstalled). NO new heavy deps, NO transformers/hf-hub pin changes (the env repair holds), `requires-python >=3.10` ✓ (we're 3.13). Pillow 13.0.0 already satisfies the new `>=10.1.0`.
**Prep done (background, safe while server runs):** (1) **pre-update pack-import baseline saved** → `data\pack_import_baseline_037_20261025.txt` (standalone-import context: the `PromptServer.instance` FAILs are harness artifacts, NOT server state — server loads those packs fine; the REAL failures = `ComfyUI-Dwpose-Tensorrt` (no tensorrt) · `ComfyUI_Nvidia_VFX_Nodes` + superseded twin (nvvfx — pending finish bat) · `comfyui-controlnetaux` (mediapipe.solutions) · `comfyui-minimax-h3-audio-T8` shows 0 classes standalone (loads fine in-server)); (2) all 5 bumped wheels **prefetched into the pip cache** (~570 MB, `data\pip_prefetch\`); (3) **`update_core_0425.bat`** created at portable root — one-shot for the SECOND restart window: `git fetch` + **checkout of the v0.42.5 RELEASE tag (deliberately not master HEAD — releases are what's tested)** → `pip install -r requirements.txt` → version verification + core import smoke test.
**USER CARD (Option A):** ① stop ComfyUI → ② `finish_nvvfx_upgrade.bat` → ③ start via `run_nvidia_gpu.bat` (allocator fix + nvvfx live) → ④ **retry v21a** with `video_2026-10-25_07-54-35.mp4` → ⑤ tell the agent when v21a is GREEN (or run `update_core_0425.bat` yourself in the next stop-window) → ⑥ agent applies the 0.42.5 update in the background (or the bat already did) → ⑦ second start → check the startup log: all 21 packs, no NEW import failures vs the baseline file. Fallback if v21a still crashes on 0.37.0: lower `--reserve-vram` (4) or disable the upscaler's temporal chunking — BEFORE blaming anything new.

## 🔴 TOP (2026-10-25 ~08:45 IST) — **v21a upscaler crash: root cause found + fixed + full env repair (user away ~08:00–09:00; D192 held — ZERO workflows queued).**

**Root cause of `torch.AcceleratorError: CUDA error: resource already mapped`** (user's v21a run 07:57, node 271:169 `MinimaxH3LatentUpscaler3D`): ComfyUI 0.37.0 auto-enables the **`cudaMallocAsync`** PyTorch allocator (torch 2.12 + CUDA 13; `ComfyUI/cuda_malloc.py` — visible in the 06:53 startup log). The upscaler's `non_blocking=True` GPU→CPU pinned-buffer transfer collides with the UVA remap → crash. **Generation stage was FINE** (SyncTile 1 tile × 3 windows, 211+14 freeze, 640×832, per-model-call); only the 3.44× latent upscaler (40×52→138×178 = 2208×2848 px, T=67 chunking) crashed ~8 s into chunking.

**Fixes applied (all take effect on user's NEXT restart — v21a on-disk file needs NO changes):**
1. `run_nvidia_gpu.bat` + **`--disable-cuda-malloc`** (ComfyUI's official off-switch; backup `run_nvidia_gpu - bkp_preallocfix_25102026.bat`).
2. Upscaler patch `Comfyui_Minimax_h3_latent_Upscaler\nodes\minimax_h3_latent_upscaler_3d.py` (~L594): `torch.cuda.synchronize()` before the CPU transfer + both copies made **blocking** (`out.to("cpu")`, `model.to("cpu")`) — safe under any launch path.
3. **`ComfyUI-LTXVideo` pack fast-forwarded** (`229437c` 2026-05 → `220e1d4` 2026-10-20, `git merge --ff-only origin/master` — remote branch is **master** not main): new `rope_utils.py` provides `interleaved_freqs_cis`/`split_freqs_cis` locally (core PR #15056 removed them) → **re-import OK, 55 classes** (LTX enhance path unblocked).
4. **ENV REPAIR — my 08:12 background TTS job broke the env, it would have broken the next restart:** the job's install.py upgraded `huggingface-hub` to **2.3.0** (08:12), but `transformers 5.9.0` (core `comfy.lora` chain) + `diffusers` + `tokenizers` require `<2.0` → fresh start would have died at `comfy.model_base`. Fixed: **`huggingface-hub==1.33.0`** ✓; **`protobuf==5.29.6`** (only version in the wandb `<8` ∩ google-api-core `>=5.29.6` ∩ grpcio-status `<6` intersection; descript-audiotools wants `<3.20` — unsatisfiable together, accepted: Higgs engine optional); **`grpcio 1.81.1` + `grpcio-status 1.71.2` restored** (wheel module dirs are **`grpc`/`grpc_status`** — NOT `grpcio`/`grpcio_status`; earlier "missing module" readings were name mismatches); **`wheel-stub`** installed (the `nvidia-vfx` sdist's `wheel_stub.buildapi` build backend — PyPI `wheel-stub==0.5.0`); TTS engine deps installed: `s3tokenizer 0.3.0` · `cached-path` · `descript-audio-codec 1.0.0` (module **`dac`**) · `vector-quantize-pytorch 1.32.0` (module `vector_quantize_pytorch`) · `dacite` · `faiss-cpu 1.15.1` · `torchcrepe 0.0.24`. **Full chain verified `ENV OK`** (transformers 5.9.0 · hf-hub 1.33.0 · protobuf 5.29.6 · core `comfy.model_base` + all TTS imports green).
5. **`nvidia-vfx` 0.2.0.0 upgrade INTERRUPTED by a DLL lock** (pip uninstall aborted at `nvvfx\libs\nppc64_12.dll` held by the RUNNING server; package left half-uninstalled: `effects.py` + dist-info gone, locked libs remain) → **`finish_nvvfx_upgrade.bat`** created at portable root: **stop ComfyUI → run the bat** (cached 435 MB wheel, `--no-build-isolation --force-reinstall`, cleans leftover 0.1.0.1 TensorRT DLLs, verifies `QualityLevel`) **→ start again**. Then `ComfyUI_Nvidia_VFX_Nodes` (P10-4) loads with `nvvfx.QualityLevel`.
6. **`ComfyUI_Fill-ChatterBox` re-import OK (5 classes)** — `s3tokenizer` + deps now installed (earlier UnicodeEncodeError in my test = cp1252 console artifact, not a pack fault).

**Known import failures that will remain after restart (all benign for us):** `ComfyUI-JNodes` (`PromptServer.instance` — upstream unfixed at HEAD 2026-08-15; our `JoinVideos` comes from Animation_Nodes) · `ComfyUI-Dwpose-Tensorrt` (no tensorrt installed; `dwposedeluxe` loads fine) · `comfyui-controlnetaux` (stale hyphen duplicate; the underscore version loads).

**USER RESTART PROCEDURE (the one gate for everything above):** ① stop ComfyUI → ② run `E:\comfyUi_latest\ComfyUI_windows_portable\finish_nvvfx_upgrade.bat` → ③ start via `run_nvidia_gpu.bat` (now carries `--disable-cuda-malloc`) → ④ retry `minimaxH3BackgroundSwap_v21a_LOCAL` with `video_2026-10-25_07-54-35.mp4` (already in `input\`). **If the upscaler STILL crashes:** lower `--reserve-vram` (currently 4) or disable the upscaler node's temporal chunking / use smaller chunks. See WORKFLOW_HISTORY.md 2026-10-25 v21a entry.

## 🔴 TOP (2026-10-25 ~06:50 IST) — **Restart verification DONE (read-only).** All packs loaded: VNCCS (10 classes incl. PoseStudio), H3Relay (67), VRGDG (61), SyncTile×4, clown-anchoring, String Literal, LoadAudioBatchFromDir, TTS-Suite (Qwen3TTSEngineNode ✓). Re-validated all gated workflows: **CLEAN = H3-Person-Removal_LOCAL (0/0) · withers_has_big_nattys_LOCAL (0/0 after patch: LoadImageCrop→"LoadImageCrop (obvpm)" ×3, drop_17_frames bool→drop_frames INT 17 — pack renamed the class, author changed the widget) · VNCCS_PoseStudio_QI2.1_REFERENCE (valid, 2 benign multi-output-edge warnings) · TTS_Suite_TTS_SRT_REFERENCE (valid, 6 unreachable-alternative-engine warnings = expected).** **minimaxH3BackgroundSwap_v21a_LOCAL** = code clean; only 2 placeholder inputs to pick in UI before running (node 231 video `IMG_1242_1_1.mp4`, node 232 image `Flux2-Klein_00502_.png` — author's files, not on this machine; temporal_mode enum was already correct on disk = validator stale-conversion artifact, re-validate clean). **1 remaining gate: `VRGDG_MiniMaxH3_2Pass_MusicVideo_LOCAL` needs class `MiniMaxH3AVLatentSeparateT8` from a SEPARATE pack `comfyui-minimax-h3-audio-T8` (T8mars) — CLONED into custom_nodes (no extra deps); → ONE MORE SHORT RESTART loads it (pack count 20→21).** Then user works the two sheets (P9 → P10). Verdicts → WORKFLOW_HISTORY.md.

## 🔴 TOP (2026-10-25 ~06:35 IST) — **USER RESTARTED ComfyUI (06:30 IST)** — loads all 20 packs (h3-relay + VNCCS_Utils new). Verification done at 06:50 (see entry above).

## 🔴 TOP (2026-10-24 ~19:30 IST) — P9 7-ITEM BATCH (user queue 18:39 IST, one-by-one loop, NO ComfyUI runs D192). **DONE: item 1 vLo** (repo `D:\models\ai-movie\repos\vlo` = free local AI video editor w/ SAM2 masking + SAM-Audio + live ComfyUI bridge; full-capability install running from the REAL path `F:\ModelArchive\...` — first attempt failed on the `D:\models\ai-movie` junction (vite absolute-filename bug); 4 missing node packs installed ✓). **DONE: item 2 H3 background-replacement 4K** (reddit 1xbzw1o → repo `NyckM/Bruxosdovfx-SyncTile-MiniMax-H3-v5.4` cloned to `E:\minimax_workflow\` + `custom_nodes\`; v21a workflow → LOCAL adaptation `user\default\workflows\minimaxH3BackgroundSwap_v21a_LOCAL.json` w/ 4 model remaps to local files; validate clean except 6 new-pack classes (restart gate) + PDMD LoRA (downloading). Models: Background Replace v3 merge LoRA ✓ + LMS r64 ✓ downloaded; upscaler + PDMD downloading; packs Video-Util-ComfYUI + SyncTile cloned (LBH upscaler pack already loaded). Community: NO mask needed, use v21a, FEED HIGH-RES character clip; **all item-2 models now ON DISK** (Background Replace v3 + LMS r64 + PDMD 4-step + upscaler conv_v1 bf16 ✓). **DONE: item 3 production H3 music video** (reddit 1xahodr → `vrgamegirl19/comfyui-vrgamedevgirl` Beta2.0 cloned + copied to `custom_nodes\comfyui-vrgamedevgirl`; 2-pass recipe (Singularity ref2va 25 steps audio-driven → turbo 8step LoRA @4/0.35 + learned 3D latent upscale) → `VRGDG_MiniMaxH3_2Pass_MusicVideo_LOCAL.json`, all 6 models local (downloaded missing `minimax_h3_fl2v_turbo_8step` (lightx2v)); **⚠ D041: music-driven — NOT for our movie**; community: ref2va only no start frames, 2nd pass keeps far faces, builder UI = `VRGDG_MusicVideoBuilderUI`). **DONE: item 4 H3 recast swap up to 3 people** (reddit 1x9n0dl → `Bambushu/h3-recast` (MIT) cloned; H3 ref2va + BFS character-swap LoRA (already local) + optional FaceRefine lip-repair; `H3_Recast_LOCAL.json` (CLIP→nvfp4_awq; rank-21 ref2v turbo→base v0.1 already local; validate = only a subgraph weight_dtype converter blind spot, confirmed false positive); example inputs → `ComfyUI\input\`; NativeAudioLock pack + 2 Shrek3OnVH5 templates copied; D041-safe = clip's own audio). **DONE: item 5 character swap R2V LoRA** (reddit 1xbljy9 → NextDiffusion MASK variant; `MiniMax-H3-Character-Swap-Mask_LOCAL.json` — SAM3 track→mask→R2V (sheet + v1.5 swap LoRA + turbo v1.1 768p)→composite onto subject only; all 7 models local; **validate CLEAN**; community: minimal noise/blur tip). **DONE: item 6 seamless vlog 1-click** (reddit 1x84uym → roycho87; 5 repos cloned; main + clown-anchoring + audio-batch packs + TranscriptionTools + Fill-ChatterBox + comfy-image-saver + Animation_Nodes + JNodes installed; `withers_has_big_nattys_LOCAL.json` (all 5 models local; validate = 9 unknown_class_type restart gate); 2 demo workflows copied). **DONE: item 7 ultrawide Ideogram v4** (reddit 1ucdyvr → Civitai 2674413; **prompts/film language ONLY per user rule — no settings applied, adapt for Krea2 later**; v3.0 workflow = reference `E:\minimax_workflow\ideogramV4Workflow_v30.json`; schema + examples + Krea2 template → `docs\IDEOGRAM_V4_ULTRAWIDE_FILM_LANGUAGE.md`; HF dataset deleted; gallery PNG metadata = best prompt source). **ALL 7 P9 ITEMS COMPLETE.** **NEXT: shared ComfyUI restart (user's convenience, never mid-Klein-work) = 17 packs: FilmStudio, Herrgotts, LongTakeNoCuts, WanVideoWrapper, ComfyUI-vlo, controlnet_aux (new underscore dir), GIMM-VFI, Video-Util-ComfYUI, Bruxosdovfx-SyncTile, comfyui-vrgamedevgirl, + NEW item-6 packs: h3_clown_anchoring, comfyui-load-audio-batch-from-dir, ComfyUI-TranscriptionTools, ComfyUI_Fill-ChatterBox, comfy-image-saver, ComfyUI-Animation_Nodes_and_Workflows, ComfyUI-JNodes. Then user runs: 8 one-click Krea2 (item-7 adaptation ready), item-2/3/4/5/6 workflows, vLo `run.bat`.** **SHARED RESTART LIST (P7, at user's convenience):** FilmStudio + Herrgotts + LongTakeNoCuts + vLo packs (WanVideoWrapper, ComfyUI-vlo, controlnet_aux, GIMM-VFI) + Video-Util-ComfYUI + Bruxosdovfx-SyncTile + **comfyui-vrgamedevgirl (VRGDG, item 3)**. Details → WORKFLOW_HISTORY.md / REPOS.md / PENDING_ITEMS P9 log.

## 🔴 TOP (2026-10-24 ~19:00 IST) — Krea2 movie-shot still: user directive "just create a normal workflow out of the workflows they provided" → BUILT `k2f_jaisal_movie_shot_16x9_oneclick.json` = the pack's SHIPPED V.01 file (single `Krea2OneNode`) with our config filled (i2i/identity_edit, jaisal_ref.png, S1 paddy prompt, 1928×1088, Fast, seed 90201, + the two managed movie LoRAs + official wan_2.1_vae). **The missing settings I never used = their `canon_krea2` + `cinematic_movie_still_krea2` LoRAs @1.0 + the official VAE.** Only error on validate = `Krea2OneNode` not loaded (EXPECTED) → **GATE = the shared restart (P7: FilmStudio + Herrgotts + LongTakeNoCuts together, at user's convenience, never mid-Klein-work)**. After restart: open file → queue (first run auto-downloads 2 LoRAs + VAE, internet needed). All 4 first-round hand-built outputs REJECTED by user ("pixelated, grainy"); hand-built variants E/F (`..._qwenvae`) = fallback if oneclick underdelivers. **D192: agent never runs.**
- **⚠ D192 HARD RULE (new, 2026-10-24): NO agent-run ComfyUI workflows** — build/validate only, user runs. In AGENTS.md + DECISIONS.md.
- **⚠ Strict bar reaffirmed (user, furious 2026-10-24):** never self-certify — all 4 first-round stills (incl. my "WINNER" A) were grainy/speckled. Show + ask only.

## 🔴 TOP (2026-10-24 ~17:00 IST) — 2-PASS KREA2 FACE-LOCK REJECTED BY USER (all 7 Jaisal outputs: face drift + noise + blackouts = "2021 AI garbage") → PIVOT = Flux Klein 20-image dataset → rank-32 char-LoRA (user building the Klein workflow, self-run; **user trains the LoRA TONIGHT then sleeps**). Pending queue = PENDING_ITEMS.md (P1 Malayalam lip-sync/audio D050 · P2 Blender layout→video · P3 LoRA v2 · P4 H3 R2V 6 scenes · P5 SFX+DaVinci · P6 SeedVR2 · **P7 LONG-SHOT SUITES: H3-LongTakeNoCuts + Herrgotts-H3-Infinite v1.4 — BOTH installed + analyzed, core PR #15375 + all models VERIFIED ✓, one restart loads both** · **P8 E:\minimax_workflow inventory (open)** · **P9 incoming user-fed repos/models — item 1 (Herrgotts suite) DONE**). Resume brief = MOVIE_RESUME.md. See D183.
- **STRICT BAR (user verdict 2026-10-24):** "good/acceptable" is NOT the bar — outputs must be
  near-clean (specific face, no noise/blackout/drift). Never self-certify marginal outputs —
  show the user and ask.
- **`data\jaisal_variations\` is NOT a verified set** (the "COMPLETE" claim below is VOID — do
  not use as a LoRA dataset).

## ⚠ VOIDED (2026-10-24 ~14:30 IST) — "JAISAL VARIATION SET COMPLETE (6 scenes, zero face drift)" — user REJECTED all face-lock outputs; body below is historical only — next = Zidhan 6-scene set → fresh LoRA
- **2-PASS VARIATION APPROACH PROVEN (zero face drift):** (1) t2i scene base (generic Keralite man in scene,
  Krea2 random face — fine) → (2) FACE-LOCK that base to the finalized ref (Krea2 Identity Edit v1.2,
  ref_boost 4.0, denoise 0.35–0.4, 10 steps cfg 1 euler/simple, g768) → face locked to the finalized ref,
  pose/scene/background/clothing preserved = **zero face drift**. This is the variation recipe.
- **Jaisal 6-scene variation set COMPLETE** (all face-locked to `jaisal_final_ref.png`, zero face drift):
  - `data\jaisal_variations\S1_paddy.png` (post-harvest paddy, rain, farmers, wet black tee)
  - `S2_house.png` (behind a normal Kerala house, single person — duplicate fixed on re-run)
  - `S3_interior.png` (inside a Kerala house, clean face — pixelation fixed by face-lock)
  - `S4_bike.png` (on a Kerala bike, rural road — cracked-skin texture fixed by face-lock)
  - `S5_7sfoot.png` (minimal local 7's football ground, small goals, low fence, benches — NOT a stadium)
  - `S6_rural.png` (rural Kerala village, paddy + homes + palms)
  - Face-locked run `a663e26c` (workflow `k2f_jaisal_scenes.json`, 6-branch, seeds 9201–9206). Scene bases:
    run `859948ab` (S1/S6) + `93f99858` (S2/S3/S4/S5 re-run). All bases single-person + artifact-free.
- **Immutable anchors:** `data\character_finals\{jaisal,zidhan}_final.png` — hash-verified byte-identical
  to `data\locked_refs\*_LOCKED.png` after every batch (jaisal `B2B4EB8C…`, zidhan `D8BEBB85…`). Staged to
  `input\{jaisal,zidhan}_final_ref.png`.
- **NEXT:** (1) **Zidhan 6-scene variation set** (white tee; beard lives in the ref — face-anchor only, t2i
  base clean-shaven then face-locked to `zidhan_final_ref.png`) → (2) collect verified 12-image set →
  **fresh character LoRA** → retest with triggers (`jeskvman`/`dlorman`) → (3) per-shot refs (2–3, D020) →
  MiniMax H3 R2V (NO music D041) → SFX + assembly by **Nov 22**.

## 🔴 TOP (2026-10-24 ~13:27 IST) — CHARACTERS LOCKED (Jaisal crooked nose + Zidhan sharp nose/full beard) — next = variation set → fresh LoRA
- **BOTH CHARACTERS LOCKED 2026-10-24 (user-approved "zidane is good, lets lock zidane" + "good [Jaisal] crooked
  nose"):**
  - **Jaisal** = `data\locked_refs\jaisal_LOCKED.png` (run `65468343_000`, `k2f_jaisal_crookednose.json`):
    slim face, **crooked/naturally-bent nose**, medium wavy black hair (eyebrow length), clean-shaven/faint
    stubble, **black tee**, warm Keralite tan.
  - **Zidhan** = `data\locked_refs\zidhan_LOCKED.png` (run `c6b83489_000`, `k2f_zidhan_sharpnose.json`):
    rounder face, **sharp angular nose** (Dulquer-Salman-style), **full short dense beard**, short black hair,
    **white tee**, warm Keralite tan.
- **How locked:** Krea2 Identity Edit (face-lock) NOSE-only edits, anchored on each character's OWN t2i ref
  (so ONLY the nose changed, everything else preserved): Jaisal base = `ff8144a1_000` (k2d_jaisal_v3, seed
  820), Zidhan base = `3f8b025e_000` (k2c_zidhan_distinct2, seed 812). denoise 0.4, ref_boost 4.0, 10 steps
  cfg 1 euler/simple. Both validated 0/0.
- **MILESTONE WORKFLOWS (DO NOT MODIFY):** `k2f_jaisal_crookednose.json` + `k2f_zidhan_sharpnose.json`
  (recorded in WORKFLOW_HISTORY.md "CHARACTER MILESTONE WORKFLOWS (LOCKED)"). See DECISIONS.md D151 +
  EXPERIMENTS.md 2026-10-24 (2).
- **Zidhan beard lesson:** Krea2 t2i would NOT reliably grow a beard on fresh seeds (3/3 beard-sweep seeds
  841/842/843 came out clean-shaven despite a strong beard prompt). Beard LOCKED via the face-anchored
  3f8b025e ref, NOT re-rolled.
- **NEXT (user-directed):** **variation set** (several seeds per character, same description) → **fresh
  character LoRA** → retest with triggers (`jeskvman`/`dlorman`). Then per-shot refs (2–3, D020) →
  MiniMax H3 R2V (NO music D041) → SFX + assembly by **Nov 22**.
- **Superseded (D150):** the face-lock-to-HD + char-LoRA-t2i route is now the REFINEMENT path, not the lock
  path (both chars locked directly). Goal `goal-79c0817e` still armed (user paused earlier; honor the pause —
  no heavy goal work until the user resumes).

## 🔴 PRIMARY GOAL: Scripting Episode 1
**Phase:** Moving from the "Red Card/Fight" of the first half into the 1950 Mind-Trip.

**Writer entry point (D132):** `episode1\CONTINUE_SCRIPT.md` — self-contained brief.
The writer model (Gemma) reads it and writes **only** the new file it names
(`episode1\episode1_script_part2.md`) — it must NOT edit existing files; the agent
model (Qwen) updates memory + commits afterwards.

**Next Milestones:**
1. **The Humorous Selection:** Define the IQ-based players (The Mathematician, The Lazy Genius, etc.).
2. **The Ship Journey:** Script the la lloC (Cura la lloC) journey to Brazil, including coconut practice and the "Fax" fix.
3. **The Brazil Final:** Detailed clash between Jaisal's Tactical India and Zidhan's Physical Brazil.
4. **The 360 Return:** Transition back to 2026 and the final handshake.

**Pending Technicals:**
- Verify MTP (Speculative Decoding) is active for Gemma writers.
- Maintain the 262K context window for long-term reasoning.

## Resume plan (user-directed 19:01 IST — TOP)
- User: "start where we left off, with the krea2 character, for jaisal and zidane, and then the character sheet."
- **Order:** (1) Krea2 identity work for Jaisal + Zidane from the LOCKED v6 sheets (02 identity refset —
  10 steps euler/simple cfg 1, ref_boost 4.0, g768, 2MP), (2) then the new H3 character-sheet route
  (ranked P3 → P4 → P1 in CHARACTER_SHEET.md — route pick still needs explicit user confirmation;
  P3 recommended: 2 HF model downloads + toobusy + pysssss packs).
- **Step 1 DONE 19:15 IST:** server found UP (pid 26288 — user restarted it). 02 re-pointed from old
  10-08 anchors to the v6 sheets; bench pair generated: `output\refset_v6\zidane_bench_00001_.png`
  (seed 77, halal cut ✓ white tee ✓ half-smile ✓) + `output\refset_v6\jaisal_bench_00001_.png`
  (seed 42, wavy ✓ black tee ✓ — sits at bench edge, neutral expression). 02 file left in Run-B state
  (char1/Jaisal bench).
- **Face issue RESOLVED (19:4x IST):** A/B (b40/b25/b20, seed 77) proved it = ref_boost 4.0 cloning
  the sheet's flat face rendering + anti-smooth-skin negative fighting the anchor (D025 repeat).
  **RECIPE LOCKED:** ref_boost **2.5** + warm scene light (golden hour) + **no** anti-smooth-skin
  negative + warm-skin positive. Golden-hour bench pair: `refset_v6\zidane_bench_b25_00001_.png`
  (warm skin ✓ identity tight ✓) + `refset_v6\jaisal_bench_golden_00001_.png` (warm skin ✓ wavy ✓
  black tee ✓ — expression neutral, seated at bench edge). 02 file left in Jaisal golden-hour state.
  AWAITING USER VERDICT on the pair → then H3 character-sheet route (P3 prep needs GO: 2 HF model
  downloads + toobusy + pysssss packs).
- **refset_v7 sheet-bg (19:4x IST):** user wants proper neutral backgrounds for char-refs ("helpful
  for character reference sheet") + Jaisal face less long. Single-image mode can't change the
  background (ref's street scene is grounded) → **two-stage pipeline**: 01 t2i clean-bg base
  (jaisal_t2i_base_00001, copied to input/) → 02 TWO-IMAGE face-lock (72 = base scene, 113 =
  char1_sheet person, boost 2.5) → **`refset_v7\jaisal_face_lock_00001` = current best Jaisal
  char-ref** (v6 identity ✓ clean background ✓ not-elongated ✓ natural skin ✓).
  **Zidane same pipeline PENDING (GO).** 02 left in two-image Jaisal face-lock state.
- **⚠ PIPELINE PIVOT (user, 19:5x IST — D141):** identity-edit outputs "pretty much off" —
  **identity-edit DROPPED for char-refs**. New pipeline: normal t2i pics → H3 character sheet
  (P3) → LoRA training dataset → **train character LoRA** (the LoRA is the face-lock; no more
  identity-edit machinery). **Normal t2i pics DONE** (01, no identity edit):
  `refset_v7\jaisal_t2i_base_00001` (seed 42, wavy ✓ black tee ✓ clean bg ✓ natural face) +
  `refset_v7\zidane_t2i_base_00001` (seed 77, halal cut ✓ white tee ✓ clean bg ✓ natural face).
  AWAITING USER VERDICT on these faces → then character sheet (P3 prep needs GO: 2 model
  downloads + toobusy + pysssss packs) → LoRA dataset.
- **Skin-grain fix (19:5x IST — D142):** user: t2i skin "kinda off, like grains" + shared 2 Krea2
  Reddit threads (u/rynaleopard V2 post: natural-language 4-5 sentence prompts, not tag-stacking).
  A/B/C (Zidane seed 77, **NEW beard spec: full short beard neatly trimmed**): stock-negative 8s =
  grainy · **clean-negative 8s = natural warm skin (WINNER, D142 recipe)** · 16s = different face,
  not sharper. **NEW T2I RECIPE LOCKED:** natural-language paragraph + CLEAN negative (identity-
  safety only, no skin/AI-look terms) + 8 steps. Outputs: `refset_v7\zidane_clean8` (recommended)
  + `refset_v7\zidane_clean16` (alt face). New tools: `utilities\{extract_reddit_images,
  download_reddit_images,expand_reddit_images}.py` (lightbox click = full-res image extraction).
  **AWAITING USER PICK: zidane_clean8 vs zidane_clean16 face** → then Jaisal same recipe (small
  patchy beard unchanged) → character sheet (P3).
- **HD CLARITY pipeline (20:0x IST):** user: v7 clarity "too off — cant we generate HD?". Built
  `03_hd_upscale.json` (LoadImage → UpscaleModelLoader `RealESRGAN_x4plus.pth` (63MB, from mirror
  repo `schwgHao/RealESRGAN_x4plus` — HF now 401s the original, GATED) → ImageUpscaleWithModel
  (input name `upscale_model`) → SaveImage). Ran: 01 portrait close-up 1152×2048 (seed 77, clean
  recipe) → `refset_v7\zidane_portrait_00001` → 4x → **`refset_v7\zidane_portrait_HD_00001` =
  4608×8192 37MP — photo-grade face (individual hairs, pores, no grain)**. Preview crops in
  `data\reddit_krea2\imgs\` (zidane_portrait_HD_preview.jpg + zidane_HD_face_1600.jpg).
  **AWAITING USER VERDICT** on this face → Jaisal same pipeline → character sheet (P3).
  NOTE: HF gating may block the P3 model downloads → ask user for an HF token at P3 prep.
- **FINAL CHARACTER PAIR DONE (20:1x IST):** user approved Zidane HD + asked Jaisal medium close-up
  (same pipeline, seed 42): `refset_v7\jaisal_portrait_00001` (base 1152×2048 — wavy medium hair ✓
  small patchy beard ✓ black tee ✓) → `refset_v7\jaisal_portrait_HD_00001` (4608×8192, photo-grade
  face crop verified). **THE FINAL REFS:** `zidane_portrait_HD_00001_.png` + `jaisal_portrait_HD_00001_.png`
  (both 4608×8192, in output\refset_v7\; portrait bases also copied to input\). User: "lets create
  final 2 images so we can build character sheet and data sets". **NEXT: character sheet (P3) prep
  needs GO — AND an HF token (HF now 401s gated model files).**
- **Step 2 (character sheet) BLOCKED ON:** user's route pick (P3 recommended) + model/pack downloads.
- **DSH + GHCP collaboration verified this session (D139)** — cross-client tool hand-off via git;
  DSH can now fetch JS-gated Reddit pages itself (`reddit_browser_fetch.py`).

## 🔴 CHARACTER SHEET route analysis (2026-10-18, user-directed)
- User re-shared 5 reddit posts (P1 1wxixua, P2 1vov6jb, P3 1w2dujd, P4 1wsb4h3, P5 1wsee1y) + HF `PoopMan333/H3_Character_Sheet_Generator` + local folder `E:\minimax_workflow\character_sheet\` (4 workflows placed by user).
- **Reference file created: `project-memory\CHARACTER_SHEET.md`** — full source list, per-post explanations, local-workflow↔post mapping, model/pack gap analysis, fetch-route status.
- **Done:** HF README fetched (complete); all 4 local workflows node-analyzed; model + pack availability checked.
- **MILESTONE (18:25–18:35 IST): ALL 5 post bodies FETCHED — from DSH itself**, no session, via new
  helper `utilities\reddit_browser_fetch.py` (local Playwright Chromium, persistent profile,
  headless). DOMs + extracted text: `data\char_sheet_reddit\P{1..5}_dsh.html` / `P*_text.txt`
  (extractor: `utilities\extract_reddit_text.py`). Earlier "reCAPTCHA tier" verdict was a
  **false positive** (standard shell recaptcha script tag) — fixed in the helper (title-based
  `is_gated`). Root cause of the original failure: DSH's built-in web fetch is text-only
  (no JS) vs Reddit's JS challenge — browser rendering is the difference (VS Code's integrated
  browser proved it 17:55; DSH now has the same capability via the helper).
- **Key findings (ACTUAL post bodies, authors verified):** P1 = **u/cgpixel23** H3-as-IMAGE-GEN
  sheet (8/25 steps, 4096×1536, "H3 Turbo Fused"; Drive WF + Civitai article 36126 + video) —
  the PoopMan333 HF repo is a RELATED separate orbit approach, NOT P1. P2 = **u/lumos_ai
  OrbitSheets** (github.com/lumosai8/ComfyUI-OrbitSheets, FREE; character template WITH VOICE
  AUDIO + location template = our local file; Krea2 anchor + Krea2 Turbo model). P3 =
  **u/inazma44** 2-stage (= our local 2BZ file, public on github.com/nicekriss/toobusy; setup:
  ref2v int8 pruned + 4-step turbo @0.75 + T=1 image VAE + er_sde/sgm_uniform 8 steps; ~3.5
  min on 3090 24 GB; known issues: props repeat, back hair flat, lying/sitting unreliable;
  **all 6 model links extracted from note node 20** — gaps = 2 HF downloads + toobusy + pysssss).
  P4 = **u/-Ellary-** Fizgig H3 REF (civitai.red/posts/31291351 WF+prompts;
  github.com/shootthesound/ComfyUI-Fizgig-H3-Still = installed; 4096×1536 18 steps 1 min on
  5060Ti 16 GB; no LLM-processed prompts needed; faster than Qwen 2.1 at 2+ refs). P5 =
  **u/LeebLaab** Qwen 2.1 (local-LLM nodes REMOVED — any LLM drafts the 10-section prompt;
  original workflow: reddit s/Rjoz79yECS; tested sheets in minimax video = "fantastic").
- **HARD RULE (user): no ComfyUI workflow runs without explicit user confirmation.** Server currently DOWN (crash) — bring-up also needs go-ahead.
- **AWAITING USER:** (a) route choice (ranked in CHARACTER_SHEET.md: P3 → P4 → P1 → P2 → P5), (b) server bring-up. ~~cookie refresh~~ no longer needed.

## v6 sheets LOCKED (2026-10-18, user-approved — supersedes "pending verdict")
- User: v4/sweep "wood or wall, no emotion"; **Zidane = short halal cut (final)**; texture/realism gap vs civitai V2-LoRA; **base is NSFW → always explicit clothing**; sheets = normal weather, no rain/boat.
- **v6 = 01 t2i, V2 LoRA @1.0, `kr2realism` trigger, 8 steps, portrait** — `char_v6\jaisal_v2lora_00001`, `char_v6\zidane_v2lora_00001` — best sheets so far (weather clean, beards visible, halal cut, photographic texture).
- **LOCKED 2026-10-18:** copied to `challenge\consistent-short\refs\{jaisal,zidane}_sheet_v6.png` AND `input\char{1,2}_sheet.png` (overwrote the old 10-08 sheets). These are the canonical character refs — they REPLACE the rainy-street anchors as identity refs (D025 rain carry-over fix).
- **Next after sheet-route decision:** identity refset from CLEAN sheets → 04 demo → demo short.
- **Known limitation (user-acknowledged):** faces lack Kerala/South-Indian aesthetics (model + V2-LoRA European skew) — v6 is the best-so-far baseline; the new sheet workflows (esp. H3-based) are the lever for a better face prior.

## v4 emotional frames (2026-10-18) — pending user verdict
- User: v3/sweep faces "wood or wall, no human emotion"; **Zidane hair re-specified: short halal cut, no waves** (military/bun both deprecated); Jaisal = medium wavy (kept).
- v4 = candid emotional moments in prompts. **Zidane `char_v4\zidane_00001` = halal cut ✓ + half-smile ✓ (best so far)**. Jaisal `char_v4\jaisal_00001` = pensive, still the neutral one — may push expression harder.
- **After verdict:** lock refs → re-point 04 demo → demo short.

## Settings sweep — 02 runs at 10 steps now (2026-10-18)
- **User:** A/B images "feel like AI, some settings are clearly OFF." Root cause: 02 ran 6 steps (t2i sweet spot) — the identity-edit pack's design point is **10 steps** ("12 = more face detail").
- **Sweep:** Jaisal 10s@4MP clean + best detail (`char_sweep\jaisal_s10_4mp_00001`); Zidane @4MP DUPLICATED (seeds 77/78, grounding 384 didn't help — tracks 4MP on this ref); Zidane 10s@2MP clean (`char_sweep\zidane_s10_2mp_00001`).
- **Proposed lock (user verdict pending):** 02 = 10 steps, 2MP 16:9, g768, ref_boost 4. Jaisal may keep 4MP (clean there).
- **After verdict:** lock the two refs → re-point 04 demo shot → demo short.

## Jaisal/Zidane re-scope + V2-LoRA A/B (2026-10-18, user-directed — supersedes v3 face sheets)
- **User rejected v2/v3 sheets** ("trash, unworthy"). Picked exact face anchors: Jaisal = `char1_NEW_realism_s6_00001` (A/B output), Zidane = `krea2_char1_face_c_00001`. Corrected specs: Jaisal slim + medium wavy hair + thin beard; **Zidane athletic/muscular (not chubby) + SHORT military cut (bun spec deprecated) + thin beard**. Prompt style = author's cinematic natural language (user pasted the author's car prompt).
- **Done:** refs → `input\jaisal_ref.png`/`zidane_ref.png`; 02 gained V2-LoRA node 97 (pure vs +V2 @1.0); 4-way grid `output\char_ab\` (jaisal/zidane × pure/v2, author-style scenes: bridge / boat). Identity held both faces.
- **Read:** Jaisal pure≈v2 (near-identical). Zidane: pure = short crop (≈ military cut ✓), v2 = wavy like ref. Thin beard faint.
- **Pending user verdict:** variant per character + beard strength + Zidane build. Then lock refs → re-point 04 demo shot → demo short.

## Character sheets v3 — FACE-ONLY close-ups (2026-10-18, user-directed)
- **User directive:** v2 scene sheets "look awful, something is off — don't put anything about the background in the prompt, we want clear face images FIRST." → sheet prompts rewritten as face-only close-ups, ZERO scene/background words (`char_sheet_v3.py`), per-character distinct faces, explicit seeds (headless seed lesson).
- **Done:** `char_sheet\char1_00003_.png` (wavy shoulder hair, 5-o'clock shadow, narrow face, black tee) + `char_sheet\char2_00003_.png` (top bun, rounder face, thicker brows, white tee). Both clean plain-background close-ups, RAW skin quality, clearly different people. Copied to `input\char{1,2}_sheet.png` (overwriting v2 scene sheets).
- **Pending user verdict** on the two faces (char2 came out with light chin shadow despite clean-shaven ask — minor).
- **After verdict:** refset stage (02) uses these face refs + scene instructions (char1 bridge / char2 boat) — the scene words live ONLY in the refset instruction, not the sheet.

## Krea2 base LOCKED IN + character sheets DONE (2026-10-18)
- **User verdict:** Krea2Realism_V1 wins the A/B → locked in as the Krea2 base (D133 resolved).
- **Done:** app workflows `01_character_sheet`/`02_identity_refset` swapped to `Krea2Realism_V1` (6 steps, euler/simple, cfg 1; V2 LoRA zeroed in 01; old files kept as `*_oldturbo.json`).
- **Character sheets + refsets generated (new base):** `output\char_sheet\char{1,2}_00001_.png` + `output\char_refset\char{1,2}_00001_.png` (char1 = misty path → bridge; char2 = boat). Identity held sheet→refset. Refs in `input\char{1,2}_sheet.png`. These 4 are the app's canonical char1/char2 refs.
- **Remaining today:** user pick of canonical sheet (or keep 10/08 face set) · re-point 04 demo shot refs (2001/2002) from the old Jaisal bridge refs to `char_refset/char1` + a char1 second-frame ref · run the char1 bridge shot end-to-end on the timeline · episode1 age question (script says Jaisal 16).

## Character re-scope (2026-10-18, D137) — OLD schoolboy character DEPRECATED
- **New characters (user-directed):** char1 (Jaisal) ~26, wavy black hair, slim, plain black t-shirt; char2 (Zidhan) ~26, top bun, slim, plain white t-shirt. Face refs: `output\krea2_char{1,2}_face_{a,b,c}_*.png` (2026-10-08; a = misty forest profile, b = boat golden hour, c = rainy street).
- **Cleanup done:** AGENTS.md character section, PRODUCTION_CONSISTENCY.md costume lock, both challenge PIPELINE.md files, INTRO_VIDEO_PLAN.md, R2V guide examples — all updated. Violet-uniform/hat kid prompt verified already gone from all files. `prompts\jaisal_identity_instructions.txt` = OLD character (superseded).
- **Re-anchored A/B (D133 redo):** `data\krea2_abtest_char1.json` (validates 0/0) — char1 + char2 t2i, same prompt+seed on OLD turbo s10 vs NEW Krea2Realism_V1 s6, euler/simple cfg 1, 1152×1792. Job `30869cc1` queued 2026-10-18.
- **Open:** episode1 script still says "Jaisal (16, rose-pink shirt)" — user to confirm story age. Challenge demo shots (04 workflow) must be re-pointed to char1/char2 refs (currently still wired to the old Jaisal bridge refs).

## Krea2 Realism V1 A/B test (2026-10-17, D133) — A/B DONE, AWAITING USER VERDICT
- **Download:** terminal resume (user-sanctioned after 2 failed browser downloads) via `utilities\download_krea2_realism_resume.py` (Range-resumable). **COMPLETED 2026-10-18:** `E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\Krea2Realism_V1.safetensors` = exactly 13,141,769,680 bytes (verified); server lists it in `/models/diffusion_models` — no restart needed.
- **A/B run DONE 2026-10-18** (`data\krea2_abtest_realism.json`, seed 42, same prompt): outputs `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\krea2_abtest\OLD_turbo_fp8_s10_00001_.png` vs `NEW_realism_v1_s6_00001_.png`. Agent read: both good; NEW slightly more natural skin/texture + more dynamic framing — but one seed only. **User judges; if NEW wins → swap Krea2 base (keep old files).** Suggested: 2-3 more seeds before swapping.

## Open Source Higgsfield challenge — RESCOPE to "character-consistent short app" (D135, 2026-10-18) — BUILDING
- **Entry (user-approved 2026-10-18):** character-consistent short app = our `krea2_identity_edit` face-lock front-end (workflows 01/02) + 2-anchor H3 shots + **obvpm-timeline engine** (public, credited) + ffmpeg assembly. Targets: **Most Viral + Open Weights (5090) + H3 bonus ($1K credits)**; Most Innovative claim dropped (frontier = obvpm/LongTakeNoCuts/clown-anchoring/fizgig — all public, all credited).
- **Folder:** `challenge\consistent-short\` (new; user pushes as a NEW public GitHub repo — user's only TODO, plus final submit). `CHALLENGE_PLAN.md` (D134) kept for the cloud-ops steps.
- **Done 2026-10-18:** packs installed + obvpm updated to v0.2.16 (see D135); `04_h3_timeline_r2v.json` adapted + **validates 0 errors**; smoke test runs 1-4 failed on the dead Set/Get constant layer → **root cause found + fixed (D136)**: MCP converter treats SetNode/GetNode as UI-only and never honors obvpm Unbundle `get` widgets → ALL 9 affected nodes re-wired to real emitted sources (1374/1379 ← 752, 1390 ← 761, 1392 ← 1383, 1436 ← 1526, 1629/1630 ← 1449, engines 1359/1488 `in` ← 1457 LazyCaseSwitch + seeds ← 765 SeedNode, 1457 cases ← 1290/1335 ValuePresets + `in` ← 1449). **SMOKE TEST PASSED (run 5, job `b6774902`): first full end-to-end timeline render — `output\clip_00001.mp4` 5.17 s 1376×768 24 fps + AAC audio + `.mctx` sidecar; character consistent across the shot** (style drifts toward 3D-animated vs photoreal refs — demo shots should use identity-locked refs from 02).
- **Next:** character-lock sanity (02 refset) + 2nd-shot cross-face check → app README + MODELS credits → 2-3 demo shots + demo video → comfy-cli cloud Build test → submit typeform `V1dSQrkS` before **10/30 9am PT**.

**Project files (read these when resuming) — Episode 1 hub = `episode1\`:**
- `episode1\DECISIONS_EPISODE1.md` — **story decisions** (characters, metaphors, scene beats) — read first
- `episode1\episode1_script_part1.md` — full Episode 1 script (Part 1 / first half; ends at the B&W transition — **second half NOT written yet** = the work above)
- `episode1\episode1_first_half.md` — first-half sequence summary
- `episode1\narrative_map.md` — characters, symbols, concept map
- `episode1\first_script.md` + `episode1\episode1_structure_prompt.txt` — earlier outline + the Gemma structure prompt (@8106)
- `episode1\workflows\` — reusable Episode 1 workflow JSONs (see its README)
- `docs\` — pipeline guides; `utilities\commit_md.ps1` — daily .md safety-commit (D131)

## Character pipeline prep (2026-10-18 20:2x IST) — PACKS DONE, MODELS DOWNLOADING
- **User GO for packs + downloads** ("lets proceed with other packs installation ... download items parallely").
- **Packs:** toobusy **0.5.6 INSTALLED** via terminal `python_embeded\python.exe -m comfy_cli
  --workspace "E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI" node install toobusy` (MCP
  `install_node` targets WRONG default workspace `C:\Users\user\Documents\comfy\ComfyUI` — always
  use terminal + `--workspace` for node installs). pysssss = **ComfyUI-Custom-Scripts ALREADY
  PRESENT** (repo = `pythongosssss/ComfyUI-Custom-Scripts`; `pythonguru/comfyui-custom-nodes` 404s).
  **Both P3 deps ready.**
- **KLEIN 9B MODELS ALREADY EXIST (user: "i think i already have these models")** — in the
  **MAIN tree** `E:\ComfyUI_windows_portable\ComfyUI\models`: `diffusion_models\flux-2-klein-9b.safetensors`
  (16.9GB) + `flux-2-klein-9b-kv-fp8.safetensors` (9.1GB) + `text_encoders\qwen_3_8b_fp8mixed.safetensors`
  (8.1GB) + `vae\flux2-vae.safetensors` (0.3GB) + 3 klein LoRAs in `loras\`:
  `bfs_head_v1_flux-klein_9b_step3500_rank128` (face-swap), `Flux2-Klein-9B-consistency-V2`,
  `flux-2-klein-9B-360-erp-outpaint-lora_V1`. **The dataset workflow runs in the MAIN tree's
  ComfyUI** (its custom_nodes have `comfyui-custom-scripts` + `ComfyUI-Flux2Klein-Enhancer`;
  NOT running right now — only the latest-tree server on 8188 is up).
- **Previous dataset runs FOUND** (user ran it before): `E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\`
  = `character_1\` (20 imgs) + `character-2\` (20 imgs) + `krea2_character_2\` (2 imgs) —
  Image_1 = crisp 1136×912 frontal headshot (85mm style, white bg) — quality excellent.
- **Dataset run PREP DONE (20:4x):** HD faces copied to MAIN tree `input\` as
  `jaisal_portrait_HD.png` + `zidane_portrait_HD.png` (35MB each); **2 ready variants written**
  to `E:\Flux_klein\`: `1 Click Dataset (Klein 9b) - jaisal.json` (ref=jaisal HD →
  SaveImage `Dataset\Jaisal\Image`) + `... - zidane.json` (ref=zidane HD → `Dataset\Zidane\Image`).
  Script: `utilities\make_klein_dataset_variants.py`. **Runs in the user's main-tree ComfyUI**
  (user loads variant + queues — they've done it twice; or I launch that instance and drive
  via REST). OUTPUT FOLDERS = auto-created by SaveImage prefix.
- **ORDER CONFIRMED WITH USER: CHARACTER SHEET FIRST** ("before that we need to go for
  character sheet right?") — sheet (P3 2BZ H3) from the 2 HD faces → user approval → then
  the 2 dataset runs above.
- **P3 SHEET MODEL DOWNLOAD RUNNING (job pwsh-196, `utilities\download_p3_sheet_models.py`,
  ~13.6GB → LATEST-tree models dir = where the sheet runs on the MCP-managed server):**
  `models\vae\minimax_h3_t1_image_vae_step1597.safetensors` (5GB) +
  `models\text_encoders\gemma4_e4b_it_fp8_scaled.safetensors` (8.6GB, resumed from 797MB).
  (The Klein 9B set needed NO download — already in the main tree, see above.
  The earlier 9B download plan — `black-forest-labs/FLUX.2-klein-9B` +
  `Comfy-Org/vae-text-encorder-for-flux-klein-9b`, all OPEN repos, no token — is now
  only a backup route.)
- **User's flux klein workflows = `E:\Flux_klein\` (7 files, user-placed 20:31)** — logged in
  **`docs\EXTERNAL_WORKFLOW_SOURCES.md`** (also covers `E:\minimax_workflow\` — the earlier
  shared location). **THE DATASET WORKFLOW = `1 Click Dataset (Klein 9b).json`** (user: "this is
  what we are going to use"): 23 nodes, Ref-Latent-Controller by u/Capitan01R (Reddit 1se5a5z);
  models = `flux-2-klein-9b` + `qwen_3_8b_fp8mixed` (type **flux2**) + `flux2-vae`; LoadImage
  node 76 = char's reference face (default `ref_woman.png` → swap to our HD face in input/);
  node 377 `CR Prompt List` = embedded dataset prompt set; 768×1120 (3:4) output; SaveImage
  node 280 prefix `Dataset\Test_woman\Image` → rename per character. Copy already in UI
  workflows folder (kept in triage).
- **USER-WORKFLOWS FOLDER TRIAGED (20:35, user ask: 245 files "not good"):** 34 KEPT
  (current pipeline + tools — see `docs\WORKFLOW_TRIAGE_2026-10-18.md`), **211 MOVED** (not
  deleted) to `user\default\workflows_archive\2026-10-18\` (manifest inside; script
  `utilities\triage_user_workflows.py`). `character sheet\` subfolder kept. NOTE:
  `episode1\workflows\` has only a README — archive is the Episode-1 files' only backup.
- **CONCRETE PLAN (presented to user):** (1) char sheet P3 (2BZ H3 2-stage) from the 2 HD faces →
  user-approved sheet; (2) LoRA DATASET via FLUX.2-klein one-node (EDIT mode: HD face ref →
  15-25 scene/angle/lighting variations per character, curated); (3) train character LoRA
  (trainer availability = next gap to audit); (4) wire char LoRA into 01 t2i recipe → face-locked
  everywhere (replaces identity-edit machinery).

## 🔴 CHARACTER SHEET A/B/C TEST (2026-10-18 22:0x IST, user-directed) — RUNS QUEUED
- **User: "p3 is the one you're suggesting, but lets try 2 workflows and test it... is p3
  minimax one? if yes, lets try with qwen 2.1 and krea2 also, which is the best — ABC testing."**
  P3 = MiniMax H3 2BZ 2-stage CONFIRMED. **ABC = A: P3 2BZ H3 (MiniMax) · B: LEEBLAAB Qwen
  Image 2.1 (P5) · C: Krea2 t2i 3-view strip (our D142 recipe).** All 6 variants (3 routes ×
  2 chars) BUILT by `utilities\make_abc_sheet_variants.py` + VALIDATED (all valid:true; A's
  39 warnings = pruned stage-2 nodes only) + QUEUED (user pre-approved the ABC test):
  - A-jaisal `bb7a4fcd-36fc-464a-92cf-cb7be16a8e6d` · A-zidane `b6a6561b-951d-4312-9736-5dd33316d23e`
  - B-jaisal `83d7d96c-9784-4a4e-8cc5-c7aa7db40460` · B-zidane `f63bbbb1-a626-4d25-a26d-5094907d08da`
  - C-jaisal `ad36b40c-a13c-4582-904f-62a409b9f4b2` · C-zidane `a2e0f4fe-63e7-4cf3-a46c-ccbba716e093`
  Outputs → `output\charsheet\H3_{JAISAL,ZIDANE}_3VIEW`, `QWEN_{...}`, `KREA2_{...}`.
  Files in UI workflows folder + project copies `05a/05b/05c_charsheet_*.json`.
  **ALL 6 RUNS DONE + 1 A-jaisal retry (`501d79f7` → `H3_JAISAL_3VIEW_00002`). RESULTS:**
  C (Krea2) = 2/2 excellent 3-view sheets (kit + crest + name-on-back all correct, ~30 s/run)
  · A (H3) = 1.5/2 (Zidane sheet perfect; Jaisal run 1 = single view, run 2 = perfect sheet —
  H3 node has NO seed input = stochastic) · B (Qwen 2.1) = 0/2 (1024-token truncation killed
  the sheet layout; Zidane came out with wrong hair). **NEXT: USER PICKS THE ROUTE**
  (recommendation = C/Krea2; A as backup if the user prefers its studio look).
- **KIT IDENTITY LOCKED (user, same message):** both characters = **soccer jersey + track pants**.
  **Jaisal = royal blue kit, Zidane = dark green kit** — both with a white clenched-fist roundel
  crest ("PALESTINE RESISTANCE") on the left chest, **player name in white on the jersey back**,
  single white side stripe on the track pants. Continuity concept: **same team, different years**
  (different jersey colors = different seasons). Kit refs generated with Krea2 (07_kit_ref_*.json,
  8 steps D142 recipe) → `input\jaisal_kit_ref.png` + `input\zidane_kit_ref.png` (both verified:
  crest + PALESTINE RESISTANCE text rendered legibly, clean flat-lays).
- **Server/pack work this span:** user restarted the server (pid 15392 → then my clean relaunch
  pid 2608, same flags `--reserve-vram 4 --enable-manager`, log `data\comfy_startup_20261018.log`).
  **toobusy 0.5.6 loaded ✓** (ToobusyMiniMaxH3SemanticReference/ImageLatent now in object_info).
  **rgthree-comfy UPDATED** (June clone lacked `Fast Groups Muter` — `git pull` 91 files; the muter
  is a FRONTEND-only JS node → validator's `unknown_class_type` on it is benign but it was DELETED
  from the A variants along with stage-2-only nodes 125/126 (PreviewImage, dangling links) + 127
  (CustomCombo) — stage 2 stays OFF; SaveImage 106 is fed by VAEDecode 5, independent).
  **2BZ prompt wiring lesson:** H3 node 13's prompt slot is LINKED from node 24 (link id 127) —
  the node's own prompt widget is IGNORED at runtime; the character master prompt was therefore
  injected into node 24's text (master + author's stage-1 3-view template).
  **LEEBLAAB (B) lesson:** model names live on the SUBGRAPH INTERNAL nodes (451 UNET / 453 CLIP /
  454 VAE), not the instance widgets — patched internals to `qwen_image_2.1_bf16` (13.25GB,
  copied main→latest) + `qwen3vl_8b_int8_convrot` (8.71GB, copied) + `qwen_image_2.1_vae_bf16`
  (0.63GB, copied). All three copied main-tree→latest-tree.
- **NEXT:** user picks the winning route (presented: C recommended) → then the 2 Klein-9B
  dataset runs (`E:\Flux_klein\1 Click Dataset (Klein 9b) - {jaisal,zidane}.json`) → LoRA
  training.

## 🔴 ABC ROUND 2 — CREST SPEC CHANGE + NEW WORKFLOWS (2026-10-18 23:3x IST)
- **USER CREST SPEC CHANGE (D145):** "the jersey should have the crest with logo only... not
  obvious... emblem showing solidarity" → crest = **white clenched-fist roundel ONLY, NO text**
  (the old "PALESTINE RESISTANCE" wording is out). All prompts updated
  (`make_kit_ref_workflows.py` + `make_abc_sheet_variants.py`: A master/detail, B TEAM row →
  "SOLIDARITY", B CREST MACRO, C prompt) + NEG adds "words, letters, slogan".
- **USER FEEDBACK ON ABC RESULTS:** (1) Krea2 "some issue with the details such as eyes";
  (2) "qwen is wrong, we didnt get the character sheet at all" + user downloaded a NEW Qwen
  workflow `E:\minimax_workflow\character_sheet\Qwen Image 2.1 Character Design Sheet.json`
  = **LLM-architect design**: subgraph 549 `ThinkingLLM_QwenVL_GGUF_Advanced` (local GGUF
  `Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf`, temp 0.95) with system prompt "Character Sheet Prompt
  Architect" + `{{name}}` StringReplace → the LLM WRITES the sheet prompt at runtime (that's
  how the author got a working 12K-char sheet). Subgraph[0] internals = same as LEEBLAAB.
  **Node pack `ThinkingLLM_QwenVL_GGUF_Advanced` was MISSING → INSTALLED:
  `custom_nodes\ComfyUI-ThinkingLLM` (goodguy1963, v2.5.8 — has BOTH the GGUF variant AND an
  HF-weights variant `ThinkingLLM_QwenVL(_Advanced)` that needs no llama_cpp; deps:
  transformers 5.9 ✓ bitsandbytes ✓ faster_whisper ✓; missing = llama_cpp GGUF backend wheel
  + tiktoken). Server NOT yet restarted to load it.**
- **USER: the minimax (P1/civitai) "just 3 images, the workflow and reddit post had few more
  — check it again [1wxixua]"** → re-fetched: P1 = u/cgpixel23's H3 IMAGE-GEN sheet: 4096×1536
  wide canvas, author's prompt = sprite-sheet layout (left portrait closeup + center 3-angle
  full-body + right 6 detail circles) = "few more images". User drag-dropped the civitai post
  image (`E:\minimax_workflow\character_sheet\1CJX8DERQKDMG6Z2C5QC4D6HW0.png`, 4096×1536) with
  the FULL embedded workflow (civitai stores it as plain-text `workflow`/`prompt` tEXt chunks —
  NOT base64; extractor `utilities\parse_new_user_downloads.py`). Mapped: 45 nodes, H3 R2V
  node 28 `[prompt, 4096, 1536, 5, 'max']` + 9 refs via ImageScaleToTotalPixels; UNET
  `minimax_h3_ref2va_pruned_int8` ✓, CLIP `qwen3vl_32b_minimax_h3_nvfp4_awq` ✓, VAE
  `minimax_h3_video_vae_int8_convrot` (on disk per validator; we use the t1 IMAGE vae instead),
  audio VAE ✓; author's 5 LoRAs (test/NSFW/style) stripped; **ALL node types available locally
  (toobusy 0.5.6 stack) — only `ThinkingLLM_QwenVL_GGUF_Advanced` was missing.**
- **USER: "all of them looks plastic like — check this post [1wzcu5v]"** (the H3 plastic-look
  thread) → findings saved `data\h3_plastic_look`: (a) top answer = **2-pass latent upscale**
  (pass 1 = half-res 20 steps NO turbo LoRA; pass 2 = turbo 8-step @4 steps 0.35 denoise);
  (b) **0.98 MP = H3's trained default res** (use float primitive); (c) counter-comment
  (lavinia12345): "latent upscale is shit... **vanilla minimax model 30 steps er_sde/beta57,
  1 MP is good. Any use of lightning/turbo LoRAs, the Spectrum node, or PlagueKind's SLA node
  screw up eyes**"; (d) turbo LoRA needs H3 AdaLN LoRA Fix (`h3_silu_turb_grid` + PlagueKind
  node or larryvrh loader), strength 0.70–0.85. **Action: built the wide variant WITHOUT turbo
  + Spectrum (30-step vanilla er_sde/beta).**
- **NEW WIDE VARIANT (05d, user's "few more images" request):**
  `utilities\make_h3_wide_sheet.py` → `05d_charsheet_H3_wide_{jaisal,zidane}.json` (UI +
  project copies): civitai/cgpixel23 workflow adapted — 10 author refs → OUR 2 refs
  (`<char>_portrait_HD.png` ref_image_0 + `<char>_kit_ref.png` ref_image_1); author's
  test/NSFW/style LoRA chain (18/19/20/21) + TurboLoRA 39 + Spectrum 41 DELETED (anti-plastic);
  chain = UNET 10 → SigmaShift 40 → AttentionBackend 60 → EasyCache 42 → {BasicScheduler 7
  beta 30 steps, KSamplerSelect 6 er_sde, RandomNoise 12 fixed seed, BasicGuider 9,
  SamplerCustomAdvanced 8} → FizgigH3StillDecode 64 → SaveImage 68. VAE 2 →
  `minimax_h3_t1_image_vae_step1597`. Canvas 4096×1536, H3 node length 5, ref_image_size max.
  Prompt = R2V 6-section 3-view sheet, NEW CREST SPEC. **BUILDER GOTCHA: the UI→API converter
  reads the inputs[].link FIELDS, not just the links array — rewiring a link means syncing the
  target node's input `link` field (40/42 model inputs), else the chain silently breaks.**
  VALIDATES 0/0. **RUNS QUEUED 00:2x IST: jaisal `ebb3b88f` · zidane `54afafe1` →
  `output\charsheet\H3WIDE_{JAISAL,ZIDANE}`.**
- **KIT REFS REGENERATED (new crest):** 07_kit_ref_{jaisal,zidane} rebuilt (fist-only-crest
  prompt, seeds 13/29, prefixes `_00002`) → `jaisal_kit_ref_00002_00001_.png` +
  `zidane_kit_ref_00002_00001_.png` — BOTH VERIFIED (subtle line-art fist roundel, no text,
  correct kit colors, clean flat-lays) → staged to `input\{jaisal,zidane}_kit_ref.png`
  (overwrote the old text-crest refs).
- **SHEET ROUND 2 RESULTS (new-crest prompts):** C×2 rerun (`cd2e7b6f`/`bbc351c1`) →
  `KREA2_{JAISAL,ZIDANE}_00002_.png` — **BOTH EXCELLENT** (3-view, new text-free fist roundel,
  correct kit + name, good faces — eyes fine this round). A×2 rerun (`a223c93e`/`8d53f0ed`) →
  `H3_JAISAL_3VIEW_00003_.png` = **MISS (3rd Jaisal stochastic fail: man on sofa holding
  folded blue pants, face cropped)** vs `H3_ZIDANE_3VIEW_00002_.png` = **PERFECT SHEET**
  (3-view, fist roundel, name on back; nits: black boots instead of white). **Scoreboard:
  Zidane = H3 reliable (2/2) · Jaisal = H3 unreliable (0/3 on this route — scene-prior
  hijacks: palace, single view, sofa) → Jaisal's sheet must come from Krea2 (C) or the wide
  variant.**
- **PACKS/MODELS INSTALLED THIS SPAN:** (1) `ComfyUI-ThinkingLLM` cloned (v2.5.8; needs
  server restart); (2) `Comfyui_Minimax_h3_latent_Upscaler` (LBH-123-AI) ALREADY PRESENT in
  latest-tree custom_nodes (single `__init__.py` + `nodes/` module; models folder =
  `models\latent_upscale_models\`) — **model DOWNLOADED:**
  `minimax_h3_latent_upscaler_3d_conv_v1_bf16.safetensors` (0.64 GB, HF
  `LBH-123-AI/Minimax_h3_latent_Upscaler` — neural 24ch-latent upscaler, 2D+3D conv nodes,
  1.0–4× scales, Split-Upscale hires-fix nodes; "saves time, not VRAM"); (3) PE-I2I GGUF
  downloading to `ComfyUI\LLM\GGUF\`: `Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf` +
  `Qwen-Image-2.1-PE-I2I.mmproj-bf16.gguf` (HF `prithivMLmods/Qwen-Image-2.1-PE-I2I-GGUF`,
  job pwsh-60) — the EXACT model the user's new Qwen workflow expects.
- **AWAITING:** wide-variant outputs (ebb3b88f/54afafe1) → then RESTART server (kill pid 2608 +
  relaunch, or `comfy launch` after kill — NOT comfy-cli-managed) to load ThinkingLLM → adapt
  the user's new Qwen-2.1-LLM-architect workflow (our refs + chars + on-disk model names;
  GGUF node needs the llama_cpp vision wheel OR swap to the HF-weights
  `ThinkingLLM_QwenVL_Advanced` node variant) → test → USER PICKS ROUTE → Klein dataset →
  LoRA.
- **WIDE VARIANT RESULTS (00:3x IST):** BOTH EXCELLENT — `H3WIDE_JAISAL_00001_.png` (first-ever
  H3 Jaisal sheet! 3-view, identity held, crest + name correct, white boots, natural skin) +
  `H3WIDE_ZIDANE_00001_.png` (same quality). Wide canvas = the fix for Jaisal's square-canvas
  scene-prior hijacks.
- **USER DIRECTIVE (00:55 IST): "create 3 workflows, 1 minimax, 1 krea2, 1 qwen 2.1, assign
  jaisals image, READY NOT RUN — I will do it manually. Give me 3 names. If Jaisal's is good,
  we try zidane's."** → DELIVERED (all in ComfyUI workflows tab + project copies, all validated):
  1. `05d_charsheet_H3_wide_jaisal.json` — MiniMax H3 Fizgig (civitai/cgpixel23) wide sheet,
     2 refs, vanilla 30-step. (Already test-ran successfully = H3WIDE_JAISAL above.)
  2. `08j_KREA2_JAISAL_sheet.json` — Krea2 Identity Edit v1.2, node 72 =
     `jaisal_portrait_HD.png` (identity), kit in the instruction text (new crest spec, no text),
     ref_boost 2.5, 10 steps, 16:9 2MP. Builder: `make_3way_jaisal_sheets.py` +
     `fix_08j_dangling.py` (dangling VAEEncode 92 removed).
  3. `09j_QWEN21_JAISAL_sheet.json` — user's LLM-architect file adapted: 470 =
     `jaisal_portrait_HD.png` (→ RTX-VSR resize → PE-LLM + Qwen anchor), 481 = "JAISAL",
     subgraph internals 451/453 → on-disk `qwen_image_2.1_bf16` + `qwen3vl_8b_int8_convrot`,
     61 → `charsheet/QWEN21_JAISAL`. **GATES: server restart (ThinkingLLM node) + PE-I2I GGUF
     download (pwsh-60, ~5GB) into `ComfyUI\LLM\GGUF\`.**
- **USER DIRECTIVE (01:10 IST): "MiniMax H3 Fizgig this is a workflow we have, set it up too"
  → `minimaxh sheet patreon.json` in the user's folder = THE Fizgig one (FizgigH3StillDecode +
  SLA-attention subgraph 325-329). DELIVERED: `05e_charsheet_H3_fizgig_jaisal.json`
  (builder `make_h3_fizgig_jaisal.py`, validates 0/0): author's design kept (single ref =
  `jaisal_portrait_HD.png` node 25; author's video-VAE; vanilla 25-step beta er_sde; author's
  SLA subgraph untouched; 4096×1536) — SWAPS (author files not on disk): 71 UNET →
  `minimax_h3_ref2va_pruned_int8_convrot`, 72 CLIPLoaderGGUF (author's Q2_K GGUF missing) →
  CLIPLoader + `qwen3vl_32b_minimax_h3_nvfp4_awq` (proven), 68 → `charsheet/H3FIZ_JAISAL`,
  358 `LoadImageListFromDir` DELETED (orphaned + class not installed). **HEADS-UP given: the
  SLA stack = the thread's "screws up eyes" suspect.** KEY DISCOVERY: latest-tree
  `extra_model_paths.yaml` (base_path `E:/ComfyUI_windows_portable/ComfyUI`) makes the main
  tree's models visible to the latest server (video VAE + Qwen3VL-32B H3 GGUF CLIPs +
  Singularity/fl2va/viggle UNET variants all usable).
- **USER FEEDBACK (01:21 IST): "you're copying the workflows but the prompt is not... just update
  the prompt. And for other workflows as well, you have to copy the prompting technique they gave,
  not just the normal ones"** — we had replaced the authors' H3 prompt with our own generic 3-view
  sheet prompt. **BOTH author workflows (civitai cgpixel23 + patreon) share ONE sprite-sheet
  template** (verified: identical text, node 28 widget): `subject_definitions: <CHARACTER> character
  from <Picture 1> META for composition:` + `summary: [reference generation] static image of sprite
  sheet, keep the exactly same art style of <Picture 1>` + `detailed_description`: 1. LEFT portrait
  (head+chest) closeup · 2. CENTER full-body 3 angles (front/side/back) · 3. RIGHT 6 round images
  (2x3 vertical narrow row): single eye, lips, single ear (in circle), hair color, skin texture,
  outfit texture. **FIX (`fix_h3_author_prompts.py` + both builders synced):** 05e (single ref) =
  author template verbatim structure, the author's EMPTY 'META for composition:' field filled with
  our kit + crest spec (text-specified); 05d (2 refs) = same template with <Picture 2> = our kit
  flat-lay ref anchoring the emblem/kit color from the image (the author's 10-ref workflow only
  ever referenced <Picture 1> — we wire the kit ref to <Picture 2>). Both files (UI + project)
  updated + revalidated 0/0. LESSON: when adapting an author workflow, copy their PROMPT
  TECHNIQUE (layout, tags, structure), only inject our character identity + kit spec into the
  author's own template fields.
- **09j FULLY UNBLOCKED (01:30 IST): all 4 Jaisal workflows now runnable, no pending gates.**
  1) PE-I2I GGUF download finished (job pwsh-60): `Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf` (5.24GB) +
  `mmproj-bf16.gguf` (0.86GB). CRITICAL GOTCHA: download landed in `ComfyUI\LLM\GGUF\` but the
  pack scans `models_dir/LLM/GGUF` = **`ComfyUI\models\LLM\GGUF\`** (`_resolve_base_dir`:
  relative base_dir joins `folder_paths.models_dir`) → copied both files there → after restart
  `[local] Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf` IS in the model_name combo (97→98 options).
  2) SERVER RESTARTS DONE: killed old unmanaged pid 2608 → `launch_comfyui(extra_args
  ["--reserve-vram","4","--enable-manager"])` pid 9008 → then `restart_comfyui` pid 22080.
  Server is NOW COMFY-CLI-MANAGED (restart_comfyui works — future restarts easy).
  ThinkingLLM nodes verified loaded (all 4 variants).
  3) NODE 549 WIDGET FIX (`fix_09j_thinkingllm_widgets.py`): author's subgraph-internal
  ThinkingLLM node carried a 34-value widgets_values from a DIFFERENT pack version; installed
  v2.5.8 has 29 widgets (object_info input_order). Rebuilt positional array = author values where
  1:1 mappable (model '[local] PE-I2I', device auto, preset '💬 Custom prompt + image (no
  preset)', max_tokens 32768, temperature 1, top_p 0.9 [link 949 → 0.95 at runtime], rep 1,
  frame_count 10, ctx 32768, n_batch 512, gpu_layers 26, image_max_tokens 4096, top_k 20,
  pool 4194304, keep_loaded False, seed 1, 'fixed', enable_thinking True,
  auto_finalization_retry True, hf_token '') + installed defaults for version-artifact slots
  (legacy_unload False, n_ubatch 512, n_threads 0, n_threads_batch 0, flash_attn True,
  offload_kqv True, ctx_checkpoints 0, stream False). Dropped any widgets_values_named.
  → **09j validates 0 errors / 0 warnings.**
- **USER RAN THE BATCH (01:51-02:01 IST, own relaunch, Qwen killed via pwsh-101):**
  - `H3WIDE_JAISAL_00002` (05d, author-technique prompt) — best identity hold of the three;
    left closeup face slightly wider than ref, eyes a bit glassy.
  - `KREA2_JAISAL_ID_00001` (08j) — face good, EYES FLAT/DULL = Krea2's known model trait
    (open criterion), not ref-related.
  - `H3FIZ_JAISAL_00001` (05e, SLA stack) — face came out slightly YOUNGER/softer than ref;
    SLA didn't visibly ruin eyes this time (83.8% sparse, 200 dense fall-throughs).
  - 09j FAILED: `RuntimeError [QwenVL] llama_cpp is unavailable — No module named 'llama_cpp'`
    (runtime import inside ensure_llama_cpp_backend).
- **USER QUESTION (02:10 IST): "some issue with eyes in all sheets — is it because our base
  image is not a straight face but sideways? do we need a new base image?"** VERIFIED:
  `jaisal_portrait_HD.png` (4608×8192) IS a ~35-degree 3/4 view (downscaled check
  `data\jaisal_portrait_HD_small.jpg`). Diagnosis: H3 sheets must extrapolate the FRONT view
  from a 3/4 source → eye region (highest identity density) gets re-synthesized → glassy/
  drifted eyes; Krea2's dull eyes are model-specific, not ref-related. **ANSWER: yes — new
  frontal base recommended (also protects the future Klein dataset from learning Jaisal as a
  3/4 character).**
- **10a v1 (identity-edit @16MP) OOM'd on user's run (02:26 IST):** krea2edit
  `_ref_attn_bias` allocates an N² attention-bias matrix (target+2-ref sequence ~136k
  tokens → `torch.zeros(1,1,L,L)` = **72.92 GiB**) — impossible on 32GB. Author's own
  note in 02: "1MP is the sweet spot". ALSO user correctly objected that identity-edit
  (i2i) LOSES quality (it is a locking tool, not a face-creation tool).
- **REBUILT 10a as v2 = FRESH T2I (builder `make_frontal_base_jaisal.py` rewritten,
  validates 0/0, UI + project):** cloned `krea2_t2i_char1_pe3.json` (the PROVEN
  approved-face recipe) and deleted the 3 TextGenerate nodes (Qwen stopped) → full prompt
  straight into CLIPTE 300/313/318 (widget-driven, text links cleared). Prompt = author's
  verbatim character prefix (Malayali man, round face, medium wavy hair down, sparse
  patchy beard, lean, dark t-shirt) + FRONTAL clause (dead-center, both eyes fully open
  and symmetric, NO side angle/profile/3-4, 85mm face-focus) + author's tail (candid
  phone-snapshot look). Author's proven anti-studio negative VERBATIM (includes bad-eyes
  terms). 3 parallel branches, KSampler seeds 42/43/44 randomize → **3 candidates in ONE
  queue**. Latent 82 = [896, 1120, 1] (1MP 4:5 — the exact proven face latent; approved
  faces were made here then 4x-upscaled). LoRA chain Krea2-realism-V2 @1.0 →
  famegrid_spicy @0.7 untouched. Save prefixes `FACEFRONTAL_JAISAL_a/_b/_c`.
  **PIPELINE: queue 10a once → pick best frontal (identity match, symmetric eyes) →
  run it through `03_hd_upscale.json` (proven 4x) → new `jaisal_portrait_HD.png`
  (rename old to `jaisal_portrait_HD_34view.png`) → re-run sheet routes with the new
  anchor → same flow for Zidane.**
- **09j FIXED (pending user restart):** installed `llama-cpp-python 0.4.3+cu130` (JamePeng
  fork, cp313 win_amd64 wheel, `data\llama_cpp_python-0.4.3+cu130...whl`) into the embedded
  python (3.13.12) — matches ComfyUI's torch cu130. Verified:
  `from llama_cpp.llama_chat_format import Qwen3VLChatHandler, Qwen25VLChatHandler` OK +
  ggml/llama DLLs load. **CONFLICTS TO PIN LATER (server must be stopped — numpy loaded by
  the running process):** wheel pulled numpy 2.3.2 (opencv-python 4.12 requires <2.3) +
  pillow 13 (rembg requires <13) → when ComfyUI is next stopped:
  `python_embeded\python.exe -m pip install "numpy<2.3" "pillow<13"` (docs §5). User must
  RESTART ComfyUI once before running 09j (the failed run may have cached the backend error).
- **10a v2 RAN (user, 02:45-02:46 IST):** 3 candidates `FACEFRONTAL_JAISAL_a/_b/_c`
  (896×1120, no OOM). **USER PICKED `b`** → installed as NEW CANONICAL
  `input\jaisal_portrait_HD.png` (2.07 MB, 896×1120). Old 3/4 base backed up as
  `jaisal_portrait_HD_34view.png` (34.89 MB). Verified frontal: both eyes fully open and
  symmetric, dead-center, wavy hair down, sparse patchy beard, black tee — exact design
  match. NO upscale needed: all 4 sheet routes resize refs internally (H3 max ref size,
  krea2edit grounding_px 768, 09j ~1536²), so the 1MP source is sufficient.
- **WIRING CONFIRMED (`verify_jaisal_wiring.py`):** all 4 sheet workflows already
  reference the canonical `jaisal_portrait_HD.png` by filename (both UI + project
  copies): 05d node 71 (+72 kit) · 05e node 25 · 08j node 72 · 09j node 470 — the file
  swap IS the wiring; zero workflow edits needed.
- **USER PLAN (in flight):** stopping Qwen + ComfyUI, restarting both (the ComfyUI
  restart also clears any cached llama_cpp backend error from the failed 09j run), then
  running ALL 4 sheet routes (05d/05e/08j/09j) with the new frontal base.
- **ALL 4 SHEET ROUTES RAN ON NEW FRONTAL BASE (user, ~03:00 IST) — SCOREBOARD:**
  - **09j QWEN21** (`QWEN21_JAISAL_00001.png`) = **USER'S PICK: BEST SHEET** — gorgeous
    design-sheet layout (metadata column, turnaround row, action poses, silhouettes,
    expression study, detail close-ups) with a solid face. BUT it missed the kit: sheet
    shows charcoal tee + charcoal pants, no crest — the running PE prompt was EMPTY.
    **Architecture discovery:** the LLM-architect chain (478/480/481/549/551) is NOT
    instanced on the main canvas (its copies carry dangling link ids, never run); the
    LIVE path = face 470 → 485 (1536 resize) → 555 PE node (custom prompt widget = '')
    → 558 → 459 generator instance (subgraph 0: KSampler 458, TextEncode 557) → 461 save.
  - **05d H3WIDE** (`H3WIDE_JAISAL_00003.png`) = good sheet (closeup + 3 views + 6 detail
    circles); crest on jersey weak/blurry ("looks like a minicromax one"); closeup beard
    slightly fuller than ref (prompt already says sparse-patchy — model behavior, not
    prompt).
  - **05e H3FIZ** (`H3FIZ_JAISAL_00002.png`) = similar; SLA 83.8% sparse → 8 circles
    (duplicated eye/lip/ear pairs); crest weak.
  - **08j KREA2** (`KREA2_JAISAL_ID_00002.png`) = 3-photo sheet (front/side/profile/back),
    face good, small crest on jersey, no detail panel.
- **CREST FIX BUILT (13:2x IST, NOT YET RUN — user runs all 4):**
  - `input\jaisal_crest_ref.png` (512×512) = tight crop of ONLY the fist roundel out of
    `jaisal_kit_ref.png` (`utilities\crop_crest_ref.py`, box center (700,328) r75 in the
    1152² source) — verified: white clenched fist in thin circle on royal blue, clean.
  - **05d:** new LoadImage 900 → `ref_image_2` (link 204) = `<Picture 3>`; prompt +=
    crest-ref line + "crest rendered exactly as <Picture 3>" + 6th detail circle = crest
    emblem alone.
  - **05e:** new LoadImage 900 → `ref_image_1` (link 726) = `<Picture 2>` (crest there);
    same prompt upgrades.
  - **08j:** prompt now = plain royal blue jersey (no patterns/numbers) + full emblem spec
    (all 4 fingers + thumb visible, crisp, no distortion) + **4th element = round crest
    close-up alone** (separate detail, per user). NEGATIVE: **removed the generic "logo"
    term — it was suppressing the crest** — added malformed-emblem/deformed-fist/
    missing-fingers/illegible-crest/blurred-emblem terms.
  - **09j:** node 555 PE custom prompt (was '') = full kit spec (plain royal blue jersey,
    crest = white clenched raised fist in thin circle, all fingers + thumb visible,
    "JAISAL" on back, navy pants white stripe, white boots, dedicated crest detail
    close-up, turnaround in kit) + 478 ROLE (subgraph def copy) gained a KIT SPEC section
    before # USER (future-proofing in case the architect subgraph gets instanced).
  - **ALL 4 VALIDATE 0/0** (both copies; `wire_crest_4_wfs.py` + `wire_crest_09j.py`).
  - **09j main-canvas node list (debugging aid):** [13, 459, 461, 470, 481, 485, 555, 558,
    563, 566, 567, 568, 569, 570]; 459 = Qwen-2.1 generator instance (subgraph 0).
- **LOGO COMPARISON TASK (user, 14:0x IST):** user pasted a 3-fist Palestine poster
  (`C:\Users\user\Pictures\free-palestine-poster-free-palestine-poster-hand-fist-colors-
  palestine-flag-295785422.jpg`, 550×374 → saved `input\palestine_fist_ref.jpg`) and asked
  for two NEW crest designs to compare: **(A) 3-fist emblem** (like the poster) and
  **(B) single fist in a roundel** — royal blue background, NO text (D145).
  **`logo_fists_compare.json`** (UI workflows folder, validates 0/0) — 4 branches: H3
  ref-based (902/903 on ref 901 = the poster) + Qwen 2.1 i2i (956/957, same ref — the
  Qwen encode node REQUIRES an image input, t2i rejected by server). Save prefixes
  `LOGO_FISTS_{H3,QWEN}_{3fist,1fist}`.
  - **v1 (colored) RAN by user:** H3 1-fist = "looks good" (clean roundel, sharp lines).
  - **v2 MONOCHROME SPEC (user, 14:0x IST): "keep it as white fillers instead of colors,
    add black lines separating each color"** → all 4 branch prompts updated
    (`update_logo_mono.py`): fist+forearm = SOLID WHITE FILL + black outline, NO colors
    (no red/green); thin black separator lines where colored zones were — knuckle lines
    separating all 4 fingers + thumb, two horizontal lines dividing each forearm into 3
    zones; poster used for SHAPES/LAYOUT only ("its colors are ignored"). Validates 0/0.
    **NOT YET RUN — user runs.** After pick → swap `jaisal_crest_ref.png` (zero rewiring)
    → re-run 4 sheet routes.
- **TRANSPARENT LOGO WORKFLOW (user, 14:2x IST):** approved the monochrome 1-fist
  (`LOGO_FISTS_H3_1fist_00002` — "this is fine") and asked for an **abstract/transparent
  version** ("so that then only it will be applied to other t shirts with diff colors").
  **BUILT `logo_transparent.json`** (UI folder, validates 0/0): LoadImage
  `logo_1fist_mono.png` (copy of the approved logo, in `input\`) →
  **PixaromaRemoveBackground** (BiRefNet — `birefnet.safetensors` already installed in
  `E:\ComfyUI_windows_portable\ComfyUI\models\background_removal\`, 424MB — no download)
  → SaveImage `LOGO_TRANSPARENT/logo_1fist` (RGBA PNG, blue background gone) +
  PreviewImage. GENERIC: to process the 3-fist variant (or any logo), just change the
  LoadImage file + prefix.
  - **RAN by user 14:3x IST:** BiRefNet LOST the top arc of the thin white ring (ML
    mask on a 2px line) — the caveat materialized. **FIXED with deterministic
    blue-chroma color-key** (no ML, no GPU): `utilities\logo_to_transparent.py`
    (input → out_white + out_black): alpha from blue-chroma distance (B - max(R,G):
    ≤30 opaque, ≥70 transparent, linear ramp) — ring-safe, kills the top gray band.
    **ASSETS DELIVERED (verified: corners alpha=0, top-band alpha=0, 69.8%
    transparent, ring top opaque at y=95):**
    - `data\crests\logo_1fist_white_transparent.png` = white fill + black lines — for
      DARK shirts (royal blue / dark green / black).
    - `data\crests\logo_1fist_black_transparent.png` = black fill + white detail lines
      (inverted luminance, SAME alpha/shape) — for WHITE shirts (user: "black
      alternatives as well if needed in future" — done).
    - Copies in `E:\comfyUi_latest\...\output\` too.
    **Rule learned:** thin-line logo elements (rings, outlines) → deterministic
    color-key, NOT BiRefNet. ComfyUI `logo_transparent.json` stays for solid-body
    logos.
  - **WORKFLOWS UPDATED (user: "update the workflows with these additional image",
    14:4x IST):** `input\jaisal_crest_ref.png` SWAPPED → the new monochrome 1-fist
    roundel (`LOGO_FISTS_H3_1fist_00002` copy; old colored ref backed up as
    `jaisal_crest_ref_v1_colored.png`) — zero rewiring, all 4 sheet workflows already
    point at the filename. Crest descriptions in ALL 4 sheet workflows (BOTH copies,
    `patch_crest_mono.py`) upgraded to the v3 MONOCHROME spec (solid white fill +
    black outline lines + knuckle/forearm separator lines, NO colors, thin white
    circle); 08j negatives += "colored emblem, colored fist, red knuckles,
    flag-color stripes". All 4 validate 0/0. **NOT YET RUN — user runs the 4 sheets.**
  - **PIPELINE STRIP (user: "lets not add more characters details when we make the
    character sheet", 2026-10-20, D151):** sheet = face ref + kit/style ONLY. Character
    attribute re-descriptions (age/hair/beard/build/skin) REMOVED from 05d/05e subject
    lines + 09j PE (node 555) — now "the exact man from <Picture 1> — face, hair, beard,
    skin and build come ONLY from <Picture 1> (image is the sole identity source)". 08j
    already compliant. Rationale: fair A/B across the 4 routes (identical inputs) + no
    text-vs-image identity fight. All 4 validate 0/0 (both copies).
  - **QWEN 2.1 COMBO (user question, D152):** 09j subgraph node 453 CLIP upgraded
    `qwen3vl_8b_int8_convrot` → `qwen3vl_8b_fp8_scaled` (strongest 8b clip on disk;
    UNET 451 `qwen_image_2.1_bf16` = strongest on machine, VAE 454 bf16 unchanged).
    `qwen3vl_8b_bf16` NOT needed (~16 GB for negligible gain on an 8B text encoder).
    NO downloads. 09j validates 0/0.
  - **MODEL-LAYER SYNC (user: "i still dont see 09j wired properly, i see errors",
    2026-10-20, D153):** author defaults survived in `widgets_values_named` + instance
    node 459 layers (the exact `qwen3vl_8b_bf16` the user asked about). ALL layers of
    all 4 sheets synced to on-disk models (`sync_model_layers.py`, both copies): 09j
    451/453/454 named → bf16 UNET / fp8_scaled CLIP / bf16 VAE; 459 instance → same
    bare names (author's `qwen/`-prefixed names gone); 05d/05e named layers ← their
    positional (working) values (05e's real UNET = `minimax_h3_ref2va_pruned_int8_
    convrot`, same as 05d). PE gguf `Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf` exists at
    `models\LLM\GGUF\` (`[local]` prefix = node convention, resolves). All 4
    re-validate 0/0. **Rule: no manual model changes needed — stored value is what
    runs; localize all layers once.**
- **SHEET A/B VERDICT + 3-PANEL FEED (user ran all 4, 2026-10-20, D154):** **09j Qwen =
  winner** ("qwen ended up being the top") — only route with both the professional design-sheet
  layout and identity close to the reference. 05e = identity drift (a different man, fuller
  beard) + duplicated back view; 05d = good but H3's soft ref conditioning (video-model frame
  anchors, not identity locks); 08j Krea2 = good face + good crest but loose layout. **Root
  cause = architecture, not model** (user's hypothesis confirmed): 09j separates spec (text, PE
  architect that sees the face) from identity (image, i2i conditioning); other routes give
  image-only conditioning. **09j emblem-invention bug = dead spec layer:** the PE LLM received
  the OLD non-monochrome spec from internal node 478 — our turn-53 monochrome spec had gone
  into 555 widget[0], a dead field (proven by the user's debug paste). **Fix (file work, user
  runs):** 3-panel composite `input\jaisal_sheet_ref_3panel.png` (2304×1536, 3:2 = sheet
  aspect, no i2i crop; face LEFT dominant / crest TOP-RIGHT / kit BOTTOM-RIGHT —
  `build_3panel_ref.py`) fed into PE 555.in0 + i2i 459.in6 directly (VSR 485 bypassed — it
  soft-upscaled the face, half the blur); 478 ← REFERENCE IMAGE LAYOUT + monochrome KIT SPEC
  (`patch_09j_3panel.py`); both copies validate 0/0 (orphan 485 warning harmless). **Next:**
  user runs 09j (fresh tab) → if crest = actual roundel + jersey texture ✓ → 09j = locked
  sheet route → dataset/LoRA stage (Klein-9B dense, D143).
- **ZIDANE SHEET + PIPELINE CAPTURE (user, 2026-10-20, D155):** "lets do the same thing for
  zidane also ... zidane also need a front facing image, not the sideways one, so lets do it
  from there" + "capture the pipeline ... all these workflows names must be there in the md
  file ... so that we can introduce as many characters as we want with this pipeline".
  **BUILT (all validate 0/0, user runs in order):**
  1. `10a_frontal_base_zidane.json` (E: workflows) — **v1 FAILED, v2 REWRITTEN** (user:
     "when i tried creating a new one with 10a_frontal_base_zidane it just gave me the same
     image as jaisal, without hair lol"). v1 = 10a-jaisal clone (shared first ~30 tokens →
     face convergence to the jaisal-like face; tag-stack + NOT-clauses = D142's proven
     failure mode; 896×1120). **v2 = the CHAR2 chain** (`krea2_t2i_char2.json` — the
     workflow that produced `refset_v7\zidane_portrait_HD_00001` per memory: 01 t2i, D142
     recipe, seed 77, portrait 1152×2048): `krea2_turbo_fp8_scaled` + `Krea2-realism-V2`@1.0
     + `famegrid_spicy_3167060`@0.7, `qwen3vl_4b` (krea2), `qwen_image_vae`, KSampler
     **seed 77 / 8 steps** euler/simple cfg 1, latent **1152×2048**, `FameGridColorFinish`.
     Node 200 `PixaromaPromptEach` DELETED (it held 6 STALE man-bun-era zidane prompts + the
     301 widget held the JAISAL negative — "short haircut, clean-shaven, no beard" as
     negatives — the char2 file was never updated for the halal-cut/full-beard face; his
     actual face was generated with a LIVE-TYPED D142 prompt that was never saved).
     **TRUE SOURCE FOUND: `01_character_sheet.json`** (id `krea2-t2i-character`, the "01
     t2i") — on-disk = JAISAL's portrait (seed 42, save `refset_v7/jaisal_portrait`);
     zidane ran the SAME file with his prompt + **seed 77** (live, unsaved). Chain:
     `Krea2Realism_V1` (NOT turbo) + `Krea2-realism-V2`@1.0, `qwen3vl_4b` (krea2),
     `qwen_image_vae`, 8 steps, 1152×2048, D142 clean negative verbatim. **v2 (char2
     chain) SUPERSEDED — wrong chain. v3 = CLONE OF 01**: prompt = D142 natural-language
     (kr2realism trigger, medium close-up, 50mm style mirroring 01's jaisal prompt; his
     canonical attrs: short black halal cut, FULL short dark beard neatly trimmed, white
     tee) + dead-center FRONTAL emphasis; negative = 01's exact D142 clean + pose/hair-
     lock. KSampler seed 77 FIXED, 8 steps, 1152×2048. Save `FACEFRONTAL2_ZIDANE` (no
     slash → output ROOT, like `FACEFRONTAL_JAISAL_*` — the builder's glob now matches
     root level). Validate 0/0.
  2. `input\zidane_crest_ref.png` BUILT NOW (deterministic, `build_zidane_crest.py`): the
     approved monochrome 1-fist roundel on a DARK GREEN ground (38,73,63 — sampled from
     `zidane_kit_ref.png` so it matches the jersey; roundel pixels untouched, only the blue
     ground recolored).
  3. `09k_QWEN21_ZIDANE_sheet.json` (BOTH copies) = 09j clone: 470→`zidane_sheet_ref_3panel.png`,
     481→`ZIDANE`, 461→`charsheet/QWEN21_ZIDANE`, 478 live spec + 555[0] mirror → dark-green
     kit + green-ground crest (JAISAL→ZIDANE, royal blue→dark green).
  4. `build_zidane_sheet_ref.py` — run AFTER the face run: stages newest
     `output\FACEFRONTAL_ZIDANE\_00001_.png` → `input\zidane_portrait_front.png` (or pass
     a/b/c) → builds `input\zidane_sheet_ref_3panel.png` (2304×1536 3-panel, same layout as
     Jaisal).
  **v5/v5b FAILED (D162 — user: "the images looks exactly same as jaisals image without
  hair ... are we doing it in same seed? think outside the box"):** v5/v5b ran on
  Jaisal's turbo chain (896×1120) → output = JAISAL'S FACE wearing zidane's hair/tee
  (verified side-by-side; 4 randomize runs, same face). Krea2 anchors the FACE to
  chain + resolution + prompt family — NOT seed or prompt details. v5's prompt also
  kept jaisal's first 80 chars (caught by user) → v5b fully independent prompt, still
  jaisal's face (chain, not prompt).
  **v6 (CURRENT):** back to ZIDANE'S HOME CHAIN — `10a_frontal_base_zidane.json` =
  clone of `01_character_sheet.json` (`Krea2Realism_V1` + V2@1.0, `qwen3vl_4b` krea2,
  `qwen_image_vae`, 8 steps, **1152×2048**) + v4b prompt family (the one whose face
  the user approved — "first 3 is good", only the build was fat) with ONLY the build
  line fixed (lean and fit + distinctly ROUND face, zero fat words). 3 branches seeds
  **77/76/78 FIXED** (77 = his approved face seed = the lock). Saves
  `FACEFRONTAL2_ZIDANE_{a,b,c}` (root, next counter `_00006_`). Builder =
  `build_10a_zidane.py` (clones 01 + branches b/c + model/latent/cond fan-outs).
  Validate 0/0 (16 nodes), wiring verified. **v6 FAILED (D163→D164):** user: "the
  face is still somehow long ... a/b/c so identical to [earlier runs] ... idealy it
  should create a different man altogether ... the facial structure is still of
  jaisals, definetly something in the underhood". **ROOT CAUSE (D164):** (1) v6 used
  `fixed` ADJACENT seeds 76/77/78 — 77 = the exact v4b seed → 00006 ≈ 00002 (the
  user's "same seed?" suspicion was correct); (2) every zidane prompt so far was
  Jaisal's template with attributes swapped — the prompt description anchors the
  face. **i2i REJECTED by user (quality drift — standing order: no i2i for images).**
  **v7 (CURRENT):** `10a_frontal_base_zidane.json` = 01 home chain (8 steps,
  1152×2048) + GENUINELY NEW description (face-shape-first, Jaisal template retired,
  kr2realism trigger kept) + **DISTANT seeds 250/777/4242 fixed** → 3 genuinely
  different men. Builder `build_10a_zidane.py` (clones 01 + branches). Validate 0/0
  (16 nodes), wiring verified. Saves `FACEFRONTAL2_ZIDANE_{a,b,c}` (root, next
  counter `_00007_`). **USER RUNS** (fresh tab). Pick-set rule: distant seeds,
  scratch-written description. **NEW STANDARD (user): all live character
  prompts copied VERBATIM into PIPELINE.md (PROMPTS section); update in the same turn
  as any prompt change.** Validate 0/0 — re-run.
  **v4 (LOCK THE CHARACTER, D158 — user: "doesnt produce 3 images to pick ... lets lock
  the charaters ffs"):** one run, 4 candidates — 3 t2i branches (seeds 77/76/78 fixed,
  shared 01 chain) → `FACEFRONTAL2_ZIDANE_{a,b,c}` (output ROOT) + **1 i2i route from
  the APPROVED 3/4 face** (`zidane_portrait_00001_.png` → VAEEncode → KSampler
  denoise 0.4 → `FACEFRONTAL_I2I_ZIDANE`; his pixels anchor identity, only head rotation
  changes — strongest lock). Validate 0/0, wiring verified. `build_zidane_sheet_ref.py`
  glob updated for all 4 names (branch arg a/b/c supported; no-arg = newest by mtime).
  **v7 VERDICT (user, 2026-10-20):** user ran the v7 series (00007→00012, tweaked
  prompts) — "i think its because of the lora training, i tried different prompt
  altering few things and still getting similar result" (the `Krea2-realism-V2`
  LoRA @1.0 on every chain = working face-anchor theory). **USER PICKED
  `FACEFRONTAL2_ZIDANE_c_00012_.png` (1152×2048) = THE LOCKED ZIDANE FACE** (D165).
  Agent staged: face → `input\zidane_portrait_front.png`; built
  `11_sheet_composite.json` (D165 — the "combine multiple images into one"
  workflow: EmptyImage white canvas + 3 LoadImage + 3 ImageScale + 3
  ImageCompositeMasked + SaveImage `SHEET_COMPOSITE`; validate 0/0 + ran clean
  5.4s CPU-only → `SHEET_COMPOSITE_00001_.png` verified = spec layout: face left
  full-height, green roundel top-right, dark green kit bottom-right) and staged the
  composite → `input\zidane_sheet_ref_3panel.png` (2304×1536).
  **09k VERDICT (user, 2026-10-20): "character sheet is done, and thats good" —
  ZIDANE SHEET APPROVED. → DATASET STAGE (Klein-9B, D143).**
  **BLOCKER (D166):** `1 Click Dataset (Klein 9b).json` node 377 `CR Prompt List`
  = `unknown_class_type` — the **comfyroll pack was missing** from custom_nodes
  (wiped by the install refresh). Reinstalled via direct git clone
  (`Suzie1/ComfyUI_Comfyroll_CustomNodes`, verified `node_mappings.py` maps
  `CR Prompt List`; no extra deps). MCP cannot restart the user's launcher-started
  ComfyUI (`no_background_server`).
  **USER SEQUENCE:** (1) **CLOSE AND RE-OPEN ComfyUI** (loads the comfyroll pack) →
  agent re-validates the dataset workflow (expect 0/0), (2) run the Klein dataset
  (swap `ref_woman.png` → the locked zidane face ref; 20-prompt list is in node
  377; index widget picks the prompt), (3) then LoRA (D143) → movie stage.
- **PIPELINE.md CREATED (workspace root):** the full movie-production pipeline map — stage
  diagram (face ref → kit/crest refs → 3-panel combiner → Qwen sheet → dataset → LoRA → H3
  movie/Blender), EVERY workflow by name+details (Krea2 stage 1-2, 09j/09k stage 4, dataset
  stage 5 incl. `1 Click Dataset (Klein 9b).json`, H3 R2V + Blender + audio + seedvr2 stage
  6), the "how we add more details" methodology (IMAGE channel = copy-target panels + one
  478 line; TEXT channel = 478 spec; identity = left-panel-only, D151), the new-character
  checklist (8 steps — "introduce as many characters as we want"), and the hard-rules list
  (D150/D143/D144/D145/D150/D151/D152/D153/D154/D041). Committed.
- **USER RUN RULE (D150, this turn):** agent misread "you create these and let me know"
  as run approval and queued the logo job → user stopped it: "dont run anything untill i
  specify". ALSO: **never run things parallelly — Qwen llama-server (8100) and ComfyUI
  (especially MiniMax H3) cannot run together** (VRAM contention, 32GB 5090). User
  manages servers; confirm state before proposing a run.
- **NEXT:** user runs `logo_fists_compare.json` (or tells the agent to run it) → compare
  4 candidates → pick crest design → swap `jaisal_crest_ref.png` (zero rewiring — all 4
  sheet workflows already point at that filename) → user runs the 4 updated sheet routes
  → pick winning sheet route → Zidane flip (incl. `zidane_crest_ref.png`) → Klein
  dataset → LoRA.

## 🔴 DATASET DONE → LORA STAGE (user, 2026-10-20, D143-revised + D167)
- **User:** "i have created 20 images for both zidane and jaisal, 20 will be off same pose
  and same type but we got the data set, now lets build the lora". **DATASET = 20 images
  each, same pose/type, generated on the Klein-9B dataset workflow (post-comfyroll-fix,
  D166). LOCATIONS (verified):** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\
  output\Dataset\Jaisal\Image_00001..00020_.png` + `...\Dataset\zidane\Image_00001..00020_.png`
  (latest tree — the user's re-runs; the older main-tree runs `character_1`/`character-2`
  are the previous-generation sets).
- **USER CORRECTION — LoRA target = KREA 2 (D143 revised, not Klein-9B):** "our lora
  target is to create lora for krea2 ... we should be able to combine our lora with
  krea2 realism lora or checkpoint, thats the whole point ... flux 9b also fine, but we
  often get plastic look there ... even on our dataset image i have the same issue ...
  to the limit we can get realism with krea lora." → **train char LoRA(s) on Krea 2,
  stackable with `Krea2-realism-V2` at generation = identity + realism.**
- **TOOL CHOICE (D167):** **Fizgig = PRIMARY** — native Krea 2 support + **LoRA
  Isolation** (multi-subject: Jaisal + Zidane in ONE LoRA, each face locked to its own
  trigger — built for our 2-character movie; Krea2 tests: face bleed 48/50 → 0/50,
  likeness unchanged). **AI Toolkit = SECONDARY** (standard; Krea2 Raw/Turbo support,
  DOP, LoKr). User: "keep both of them in our armour." No better Krea2 alternatives
  exist (kohya/diffusion-pipe don't support it).
- **SETUP IN PROGRESS (2026-10-20):** **Fizgig = fresh install, job pwsh-106** (`D:\tools\
  Fizgig`, Python 3.12 venv, CUDA 12.8 torch, `install_fizgig.py`, log
  `D:\tools\Fizgig\install_log.txt`; GUI = `Launch Fizgig.bat` /
  `Launch Fizgig in browser.bat`). **AI Toolkit = ALREADY INSTALLED (user correction,
  turn 76: "ai toolkit is already installed right ... stop redundant work")** at
  `E:\AI-Toolkit-Easy-Install\` (easy-install v0.4.1: `AI-Toolkit\` repo + own
  `python_embeded\` py3.12.10 + `Start-AI-Toolkit.bat` → UI localhost:8675 +
  `Update-AI-Toolkit.bat`; torch 2.8.0+cu128, CUDA on 5090 verified, `aitk_db.db` =
  used before). **CAUGHT: that build = Feb-2026, NO Krea 2 support, 656 commits
  behind** → my redundant fresh clone (job pwsh-107) KILLED + `D:\tools\ai-toolkit`
  DELETED; instead **updating the existing install in place (job pwsh-118)**: git pull
  → latest (2026-10-19) + `python_embeded\python.exe -I -m pip install -r
  requirements.txt` (log `AI-Toolkit\update_log_20261020.txt`). After: verify Krea 2
  model definitions landed + `Start-AI-Toolkit.bat`.
- **✅ BOTH TOOLS READY (2026-10-20, verified):**
  - **AI Toolkit** (`E:\AI-Toolkit-Easy-Install`): HEAD `0473387` (2026-10-19, latest),
    **Krea 2 support VERIFIED** (`toolkit\models\registry.py` + `qwen3_vl.py` text
    encoder + `qwen_image.py` VAE = our exact Krea2 stack), requirements clean
    (diffusers 0.39.0.dev0, transformers 5.5.3, rc=0; log
    `AI-Toolkit\update_log_20261020.txt`). Launch: `Start-AI-Toolkit.bat` →
    localhost:8675.
  - **Fizgig** (`D:\tools\Fizgig`): install finished (job pwsh-106; the exit-1 was
    cosmetic — log ends "Installation Complete!", only optional MSVC Build Tools
    missing = torch.compile speedup, not required). **CUDA VERIFIED in venv: torch
    2.10.0+cu128, RTX 5090 seen, capability (12,0) Blackwell.** Launch:
    `D:\tools\Fizgig\Launch Fizgig.bat` (own window) or `Launch Fizgig in browser.bat`.
    First-use downloads: InsightFace models (~300MB) + Florence-2 captioning
    (~500MB-1.5GB from HF).
- **DATASET FOLDERS BUILT (2026-10-20, agent file work):** user's naming idea adopted —
  "we might need to describe the image description/heading instead of image1 image2".
  Verified: Image_NNNNN = prompt N of the 20-prompt list (node 377) 1:1 in order (spot-
  checked 00001 = headshot white bg, 00005 = industrial loft — DIFFERENT scenes, not
  repeated poses). **`D:\lora_training\{jaisal,zidane}\`** = 20 images + 20 `.txt`
  sidecar captions each (builder `utilities\build_lora_dataset_folders.py`, originals
  untouched). Descriptive names (`01_frontal_headshot_85mm_white_bg.png` ...
  `20_purple_bg_north_light.png`). **TRIGGERS (verified vs Krea 2 encoder per guide):**
  jaisal = **`jeskv`**, zidane = **`dlor`** (different first letters, no shared prefix,
  no meaningful pieces, end in consonant). Captions = `TRIGGER, a man, <full scene
  description>` — NO identity words (face/hair/beard excluded = trigger only; guide:
  "things left out tend to get learned as part of the person"). Fused at training:
  `jeskvman` / `dlorman`. **EPOCHS (guide §4):** two men ≈ 16 epochs (man-woman pair
  peaked at 10; two women needed 16) — keep intermediate epochs, pick best by eye.
- **NEXT (USER):** open **`D:\tools\Fizgig\Launch Fizgig in browser.bat`** (user's
  choice) → agent walks the tabs: **Start tab** = `D:\lora_training\jaisal` (subject 1;
  subject 2's folder box = `D:\lora_training\zidane` on the Subjects card) → **Captions
  tab** = folder triggers `jeskv` / `dlor` (already written into the .txt sidecars —
  verify Fizgig reads them) → **Training tab**: model = **Krea 2**, Subjects card =
  2 subjects, mode = **"Fizgig LoRA Isolation"**, ~16 epochs, preview prompts using
  the JOINED words (`jeskvman, ...` / `dlorman, ...`) → Start Training (user runs).
  First-use downloads: InsightFace ~300MB + Florence-2 ~0.5-1.5GB (only if the
  captioning/face features are touched — we have manual captions, so may not fire).
  OPEN QUESTION: Krea 2 model source in the GUI (HF `Krea-2-Raw` vs our local
  `Krea2Realism_V1` chain — confirm in Preferences).
- **Docs captured:** `docs\lora-tools\{fizgig_README, fizgig_LORA_ISOLATION,
  fizgig_MULTI_PERSON, ai_toolkit_README}.md`.
- **Training plan (Fizgig GUI):** Start tab = dataset folders → Captions tab = trigger
  words per `fizgig_MULTI_PERSON.md` guide → Training tab: model **Krea 2**, **Subjects
  card = 2 subjects** (jaisal folder + zidane folder), "Your subject and other people" =
  **Fizgig LoRA Isolation** → Start. Dataset caveat (user-accepted): images are
  Klein-generated (some plastic look) — Krea2 training pulls back toward natural skin.
  Optional later: regenerate some dataset shots on the Krea2 chain.
- **NEXT:** (1) both install jobs finish → verify CUDA visible to each venv, (2) confirm
  the 40 images are the approved set (spot-check faces), (3) organize per-character
  folders for Fizgig's Subjects card (+ captioning), (4) train (user drives GUI, agent
  drives CLI), (5) char LoRA + `Krea2-realism-V2`@1.0 = the new face-lock everywhere
  (replaces identity-edit machinery) → then movie stage.

## 🔴 MODEL AUDIT + ARCHIVE (user, 2026-10-21, D168) — STORAGE CRUNCH
- **Context:** E: models drive down to ~38 GB free; the **Krea 2 RAW DiT (25.9 GB)**
  download is in progress in Fizgig GUI (user-running) → ~12-15 GB left after.
- **Audit (agent):** all 194 model files in `E:\ComfyUI_windows_portable\ComfyUI\models`
  (817.9 GB) cross-referenced against all 63 workflow JSONs (both trees). 56 referenced
  files = keep; 127 unreferenced = candidates.
- **USER DECISIONS (2026-10-21):**
  - **MOVE (≈ 261 GB, 80 files) → `F:\models_bkp\<same subfolder>\`** (structure
    preserved, recoverable; script `utilities\move_models_to_bkp.py`, background job
    `pwsh-140`, log `D:\models\vsCodeMcp\move_bkp_log_20261021.txt`): all **Wan** (114.8),
    **umt5/FLUX.1 encoders** (41.7 — verified safe: klein workflows use
    `qwen_3_8b_fp8mixed`; umt5 = old FLUX.1 arch, zero references), **Qwen 2511/2512 gen**
    (64.0 — user: "may need in future, pull from the drive to models folder when needed"),
    **SDXL + orphaned controlnets** (16.05), **redundant encoders** (16.9 —
    `qwen3vl_4b_bf16` redundant with in-use fp8_scaled; `qwen_3_4b` zero references),
    **small unused misc** (14.3: sdpose, liveportrait, sam2, clip_vision, Z-Image Turbo
    LoRAs, vae_approx, etc.).
  - **LTX family = UNTOUCHABLE (user):** Lightricks VFX-week IC-LoRAs (Clean-Plate /
    Day-To-Night / SDR-To-HDR + more) are "super needy" for the movie — all LTX files
    stay, including the 5 saved LTX workflows they belong to.
  - **ditto KEPT (18.3 GB):** the ditto workflow is useful for style variants.
  - **Qwen edit-2511 chain stays** (`qwen_image_edit_2511_bf16` + Lightning +
    multiple-angles LoRA + `qwen_2.5_vl_7b` pair — referenced by
    `QWEN_click_multiple_character_angles`).
  - **Junk NOT deleted** (`Unconfirmed 819787.crdownload` 1.63 GB stays — user: "dont
    remove junk for now", don't interrupt the parallel download).
  - **Also left alone (not approved this pass):** ace_step (7.70), H3-adjacent variants
    (fasth3/viggle/character-swap ≈ 44.5), H3 GGUF pair (17.31), krea2_darkbrush /
    krea2_lineart / bfs_head / klein-consistency LoRAs.
- **Docs:** `docs\MODEL_INVENTORY.md` (keep/moved/untouched lists + pull-back
  procedure, committed af34ce2). **MOVE DONE + VERIFIED (11:14 IST):** job
  `pwsh-140` PASSED — 80/80 files at `F:\models_bkp` with matching byte sizes,
  all sources gone, 0 bad. **E: = 256.3 GB free** (was ~38 GB; RAW DiT 24.5 GB
  landed in shared `diffusion_models\` at 11:00). Models dir now 541.9 GB /
  188 files. Note: `F:\models_bkp` also carries the user's earlier archives
  (`wan_model` 300.5, `ltx` 97.6, `qwe_2512` 38.1 GB) — no collisions,
  nothing overwritten.
- **LTX VFX armour (11:0x IST):** `ComfyUI-LTXVideo` pack COPIED into the
  running install (from main tree) + `ninja~=1.11.1.4` pip-installed into the
  embedded python → activates on next ComfyUI restart (user restarts). User
  downloading 4-5 VFX IC-LoRAs (links in `docs\VFX_PIPELINE_LTX25.md`):
  sdr-to-hdr-scene-emb, clean-plate, day-to-night, water-simulation (+ optional
  ingredients). "Background text addition" verdict: NO standalone official
  text IC-LoRA exists — it's the base model's text-rendering capability (base
  already local); Ingredients = closest official element tool.
## 🔵 Fizgig API CONTROL (D170) — agent assists the GUI
- **Fizgig's web app (127.0.0.1:8081) has a full REST API** — agent can read/write
  the GUI's exact state instead of screen-sharing. Token: in the served page's
  `<meta name="fizgig-token" content="...">` (re-extract after every app restart).
  All `/api/*` calls need header `X-Fizgig-Token` (403 without). ~156 routes:
  `/api/state`, `/api/prefs`, `/api/runs`, `/api/queue`, `/api/captions/*`,
  `/api/studio/*` (source `D:\tools\Fizgig\src\fizgig\web\server.py`).
- **Done (12:2x IST):** all 5 Krea 2 model paths written via `POST /api/prefs`
  (`changes` dict, keys `krea2_raw_dit`/`krea2_vae`/`krea2_text_encoder`/
  `krea2_turbo_lora`/`krea2_turbo_dit`) + verified; family → `krea2`,
  image_folder → `D:\lora_training\jaisal` via `POST /api/state`.
- **Assist protocol:** user clicks, agent verifies via API; "look" = agent
  captures the screen (PowerShell screenshot → read_image) and guides visually.
- **Web UI sync mechanics (discovered 2026-10-22 06:25 IST, after the "changes
  don't show" saga):** the app is MULTI-CLIENT sync. Served JS (`/app.js`,
  427 KB; source `web/static/app.js`): each open page keeps `S.values` (whole
  form object for the shown family); `saveState()` POSTs the ENTIRE object on any
  change (debounced 600 ms) — ONE stale field on a page re-sends that whole stale
  form and clobbers API writes; `catchUp()` self-heals ONLY while the page is
  `visibilityState === "visible"` (hidden tabs never heal). The user's Brave page
  (loaded before the agent's writes, window hidden behind the DSH chat) kept the
  Subjects-card fields (FAMILY_SUBJECTS/PEOPLE_MODE) + DATASET_MEGAPIXELS at
  defaults and clobbered exactly those 3 on every sync (web_state.json writes
  6:12 / 6:17:49 / 6:20:50). The desktop "Fizgig" window = the `fizgig.py --web
  --open` CONSOLE only (not a client). FIX: agent final write → user HARD-REFRESH
  (Ctrl+F5) the one live Fizgig window → fresh load hydrates all fields from
  server truth. Agent can find/foreground/capture user windows via user32
  EnumWindows ("Fizgig - Brave" = the web client; "Fizgig" = console) +
  SetForegroundWindow + CopyFromScreen. RESOLUTION (06:30 IST): the user's live
  Brave page keeps an ancient in-memory snapshot (rank 4 / 1 subject / 0.25 MP)
  and re-sends it on every sync — API writes to those 3 fields keep getting
  clobbered (last catch: 06:29:40). Agent cannot press browser keys, so
  handover: USER'S OWN CLICKS are the source of truth that wins. Click list
  given: Subjects card → 2 subjects → subject 2 = `D:\lora_training\zidane` →
  Fizgig LoRA Isolation; Presets dropdown → "Krea 2 Standard (rank 32)";
  Target Megapixels → 1.0; Max Epochs 30, save every 1. Work in ONE window
  only (other tabs clobber). After user clicks: agent verifies via API, then
  Check settings → close ComfyUI + llama 8100 → Start.
- **NEXT (user's 3 clicks, agent verifies each):** Subjects card = 2 subjects
  (subject 2 = `D:\lora_training\zidane`) + "Fizgig LoRA Isolation"; Training
  card = Krea 2 Standard rank 32, DATASET_MEGAPIXELS 1.0, save-every-epoch, ~16+
  epochs, preview prompts `jeskvman`/`dlorman`; Check-a-trigger-word (jeskv/dlor).
  Then close ComfyUI + llama server 8100 → Start.

## Krea2 LoRA trained + A/B decision test (2026-10-22, 10:43 IST)
- **`krea2fp` TRAINED (user, page defaults):** 2 subjects + Fizgig LoRA Isolation ✓,
  rank 8 / 0.25 MP / 30 epochs / adaptive LR / seed 42, sample prompts
  `jeskvman`+`dlorman`, ~43 min (08:01→08:44). Outputs:
  `D:\tools\Fizgig\output_loras\krea2fp-000001..000030.safetensors` + final
  `krea2fp.safetensors` + 60 previews. **Copied to shared loras:**
  `krea2fp_rank8_ep30.safetensors` + `krea2fp_rank8_ep16.safetensors`.
- **User read of previews:** good, but (a) all close-ups = EXPECTED (dataset
  framing; movie shot-size comes from prompt), (b) **face 2 (Zidane) sometimes
  missing** → rank 8 / 0.25 MP underpowered for 2 identities.
- **Decision (user): A/B test before retraining.** Built + MCP-validated clean:
  `krea2_ab_A_baseline.json` (base chain, NO krea2fp, descriptive 2-man prompts,
  2 framings) vs `krea2_ab_B_lora.json` (same chain + `krea2fp_rank8_ep30`@1.0
  as node 303, trigger prompts `jeskvman and dlorman…`). Chain =
  krea2_turbo_fp8_scaled + Krea2-realism-V2@1.0 + famegrid_spicy@0.7, 10 steps
  CFG1, 1120×896. Both in `user\default\workflows\`.
- **NEXT (user):** restart ComfyUI (also activates LTXVideo pack + ninja) →
  Workflows tab → queue **A** then **B** → show results. Then decide: retrain
  rank 32 / 1.0 MP if B clearly better, descriptive-prompt route if A suffices.
  Movie stage unchanged: char LoRA + `Krea2-realism-V2`@1.0 face-lock → MiniMax
  H3 R2V (2-3 refs, NO music D041).

## krea2fp_V2 retrain done + v2 output test built (2026-10-22/23)
- **v2 TRAINED (user, ~15:30→16:16+ IST 10/22, ~4.3 h):** preset "Krea 2 Standard
  (rank 32, full model)" APPLIED ✓ — rank 32 / alpha 32, LR 1e-4 constant
  (adaptive OFF ✓), 64 epochs, 4608 steps @3.37 s/it, 1.0 MP, seed 42, EMA 0.98,
  adamw8bit, 2 subjects + `D:\lora_training\zidane` + Fizgig LoRA Isolation ✓,
  sample prompts `jeskvman`/`dlorman`, turbo 0.7, save-every-epoch. Loss smooth
  0.066→0.054, no divergence, result "finished". Run id 9e55de18807d.
- **User's "previews are all close-ups" concern:** EXPECTED — SAMPLE_PROMPT is the
  BARE triggers (`jeskvman`/`dlorman`) with no scene/pose words, so each epoch
  preview = base-model default (close-up portrait, white bg). Previews test
  identity + trigger response, NOT scene diversity; scene diversity comes from
  inference prompts. (Add scene words to SAMPLE_PROMPT for scene previews.)
- **Final previews (e64, 1024²):** `jeskvman` = decent Jaisal-TYPE (wavy black
  hair, black T, frontal) — closer to canonical than v1; `dlorman` = WRONG TYPE
  (short hair + full beard — NOT the bun-hair zidane). Judge by workflow output,
  not preview.
- **Copied to shared loras:** `krea2fp_v2_ep64.safetensors` (final, 223.9 MB) +
  `krea2fp_v2_ep32.safetensors` (mid, backup if ep64 overfit).
- **Built + verified `krea2_ab_B_lora_v2.json`:** B chain with node 303 →
  `krea2fp_v2_ep64.safetensors`@1.0; 3 test prompts: (0) `jeskvman` alone, rainy
  Kerala street, waist-up; (1) `dlorman` alone, SAME scene; (2) combined
  "jeskvman and dlorman side by side" dusk riverbank. Save prefix
  `krea2_ab_B_v2`.
- **v2 ROUND 1 RESULT (07:38 IST, `krea2_ab_B_v2_00001..6` = 2 queues):**
  (1) `jeskvman` = Jaisal-TYPE LOCKED (wavy hair, black T, slim — matches e64
  preview face; type-level lock solid, face = "Jaisal-ish" close-to-canonical).
  (2) `dlorman` = **COLLAPSED INTO FACE-1** (wavy hair + black tee — NOT bun +
  white tee; face-2 clone of face-1, not missing this time). (3) combined =
  TWO near-identical men, both face-1 type. → 2-person capability STILL broken;
  face-2 identity unstable (e64 preview = bearded short-hair face, workflow =
  face-1 clone — wanders).
- **Built + validated `krea2_ab_B_v2_noreal.json` (13 nodes vs 14 — converter
  drops bypassed node = bypass proof):** node 96 realism PRE-BYPASSED in file
  (mode 4), same 3 prompts, FRESH prefix `krea2_ab_B_v2_noreal` (counter
  restarts _00001 — no stale-file trap), seed stays randomize.
- **v2 queues 2-3 (7:38/7:5x IST, `_00004..00009`):** seed DID randomize
  (pixel-diff 1v7/2v8/3v9: only 1.3-1.8% samples identical, mean diff 10.5-13.9/255)
  but compositions repeat = LoRA scene-locked to dataset (over-shoulder rainy path,
  backwater pavilion). User: "first 3 good, rest 3 bad" = no new info.
- **CORRECTION (10/23, user: "you are blindly lying") — two wrong calls:**
  (a) I claimed "triggers are in the file" from the on-disk file (my 3 trigger
  prompts, last write 7:25). The ACTUAL run used the user's OWN 6 descriptive
  prompts in the UI (unsaved — file still shows my 3): all 6 describe Jaisal
  ("MEDIUM-LENGTH WAVY hair NOT in a bun/topknot", sparse beard, dark tee,
  "NOT a man-bun man"), NO trigger words. → all 6 images = Jaisal, and the run
  contains NO zidane test. Lesson: UI state is what runs; on-disk file can be
  stale — verify the actual prompts before claiming. (b) My "dataset = WRONG
  PERSON" verdict used the OLD D137 canonical (top bun + white tee). User
  re-scoped Zidhan on 10/20: **`FACEFRONTAL2_ZIDANE_{,a_,b_,c_}00001..12`**
  (10/20 18:08-19:27) = NEW Zidhan face = **buzz cut/fade + full short dense
  beard + white tee** — which MATCHES the dataset face (dataset 01/02 = same
  buzz+beard man). Dataset is FINE; e64 `dlorman` preview (buzz+beard) =
  correct identity. My `zidane_v2_scenes.txt` top-knot regen plan is VOID.
- **WHY images 2/8 (my `dlorman` prompt) came out Jaisal-type:** scene words
  (rainy Kerala street) are jaisal-dataset-bound → face-1 dominance; bare
  `dlorman` (e64 preview) = correct face.
- **USER ASKS (10/23):** (1) "where the trigger word? any issue with updating
  the prompt in comfyui?" → no issue: edit PixaromaPromptEach in UI, then SAVE
  the workflow so file = what runs (that gap caused my wrong claim). (2) FAIR
  TEST = jaisal + zidane in the SAME picture (combined prompt). (3) Zidhan
  description must come from the NEW ref `FACEFRONTAL2_ZIDANE_c_00012_.png`
  (buzz cut, full short beard, white tee) — NOT top knot; user to share the
  FINAL zidane image before I write the zidane description.
- **CHARACTER FINALS LOCKED (10/23, D171):** Jaisal = `FACEFRONTAL_JAISAL_b_00001_.png`
  (wavy hair DOWN, sparse beard, dark tee — verified), Zidhan =
  `FACEFRONTAL2_ZIDANE_c_00012_.png` (buzz/fade + full short beard + white tee).
  **Handy doc built: `docs\CHARACTERS.md`** — finals table, verified descriptions,
  VERBATIM face-frontal prompts + negatives picked from the generator workflows
  (`10a_frontal_base_jaisal.json` node 300/301, `10a_frontal_base_zidane.json`
  node 300/301), ready-to-use scene templates (trigger first), and the combined
  2-person FAIR TEST prompt.
- **WORKFLOW FILE TRAP explained (10/23):** on-disk `krea2_ab_B_lora_v2.json`
  (last write 7:25) = my 3 TRIGGER prompts; user's UI canvas = their 6 UN-SAVED
  descriptive prompts (same prefix `krea2_ab_B_v2`). Refreshing the tab keeps the
  unsaved canvas state → user "still doesn't see trigger words". Restarting ComfyUI
  would NOT help.
- **ROOT CAUSE of "prompts not visible" (10/23):** `PixaromaPromptEach` stores all
  prompts in ONE hidden widget `PromptEachState` — on disk `widgets_values` =
  single-element array whose element is a JSON state string
  (`{"version":2,"prompts":[...],"text":"","split":"line","expand":true,
  "trim":true,"skipEmpty":true,"cap":200,"wiredAt":"after"}`) — NOT an array of
  prompt strings. My first build used an 8-string array → UI rendered the node
  EMPTY, its re-save (08:48) clobbered the file with an empty state. Lesson now in
  AGENTS.md (workflow-format section). Node source: `custom_nodes\ComfyUI-Pixaroma
  \nodes\node_prompt_each.py` + `_prompt_each_helpers.py` (DEFAULT_STATE,
  parse_state heals bad shapes to defaults; row rules: `#`=off, `[a|b]`=expand
  both, `{a|b}`=random, cap 200).
- **`krea2_fair_test.json` CLEAN REBUILD (final, validated):** rebuilt from clean
  `krea2_ab_B_lora_v2.json` base (14 nodes), node 200 = state-blob widgets_values
  (1 string elem) + `widgets_values_named.prompteach` = same blob. 8 prompts:
  [1-6] user's 6 Jaisal scenes verbatim, ALL now saying "a short PATCHY BEARD"
  (wording unified to match user's emphasis — Jaisal's beard is patchy/uneven per
  `FACEFRONTAL_JAISAL_b_00001`), [7] `dlorman` Zidhan solo houseboat, [8] combined
  fair test. SaveImage prefix `krea2_fair_test`. MCP validate clean (14 nodes, 0
  errors). PS gotcha hit: `Add-Member -NoteProperty` is ambiguous here (use
  hashtables); a failed rebuild had left node 200 EMPTY — the clean-base rebuild
  fixed it.
- **USER SAW "6 OLD PROMPTS IN BOTH FILES, EVEN AFTER COMFYUI RESTART" (09:16) —
  ROOT CAUSE PROVEN:** both files on disk verified intact = 8 prompts each, last
  write 08:56 (my writes, never clobbered), no `krea2_fair_test_v2.json` exists
  (user's "v2" = my `krea2_fair_test2`). The 6-prompt canvas lives in the
  BROWSER's canvas/workflow cache — the Workflows tab restores the cached canvas
  instead of reading the file from disk; a ComfyUI server restart does NOT clear
  the browser cache. File-based fix: close the stale canvas tab, then use the
  folder-icon "Open" to load `krea2_fair_test2.json` straight from disk (bypasses
  the Workflows-tab cache).
- **FAIR TEST ROUND 1 RESULT (user-reported 09:3x): 7 Jaisal-type + 1 Zidhan image.**
  Old composition was Jaisal-heavy (6 Jaisal scenes + 1 Zidhan + 1 combined), so
  7:1 is exactly what it could produce. Learnings: `jeskvman` held on ALL 6 Jaisal
  scenes; `dlorman` SOLO produced Zidhan's face (prompt 7 worked); the COMBINED
  shot collapsed to Jaisal (second man did not survive — first trigger/description
  dominates). User's design call (accepted): the test MUST be balanced —
  **3 Jaisal + 3 Zidhan + 2 combined**.
- **FAIR TEST ROUND 2 VERDICT (user-attached 8 images, 14:46): 8/8 HELD** — 3 Jaisal
  ✓, 3 Zidhan ✓, 2 combined ✓ (both pair shots showed two distinct men; round-1
  collapse gone). `jeskvman`/`dlorman` solid. Jaisal patchy beard faint in solos.
  **User's call:** faces too similar — "same guy with different haircuts" →
  re-scope Jaisal's facial features + retrain (see D172).
- **HARD TEST VERDICT (ran 19:30 turbo; user: "quality too low, not even usable"):**
  identity HELD 6-7/8 hard cases (profile ✓, low-angle ✓, full-body sprint ✓, crowd
  ✓, Zidhan night profile ✓, Zidhan laughing close-up ✓, both-men shot = two
  distinct men ✓). Failures: [2] extreme close-up face drift (eyebrows wrong);
  [8] football-pass ACTION not performed (came out as conversation). Quality SOFT
  overall — ROOT CAUSE: the run was on the TURBO unet (`krea2_turbo_fp8_scaled`,
  10 steps, cfg 1) = a speed model. `krea2_raw_bf16` (production quality) sits
  UNUSED on disk; documented settings (workflow note): 40 steps, cfg 3-4,
  negatives matter.
- **RAW QUALITY TEST BUILT:** `krea2_raw_qtest.json` (MCP-validated, 14 nodes) —
  same proven chain, UNET→`krea2_raw_bf16`, 40 steps, cfg 3.5, existing negative,
  3 IDENTICAL hard prompts (Jaisal close-up, Jaisal profile, both-football) →
  direct turbo-vs-raw comparison. Prefix `krea2_raw_qtest`. User to run today.
- **MOVIE CONSISTENCY ARCHITECTURE (D173, for Nov 22 release = 30 days):**
  reference-DRIVEN chain, not text+LoRA: (0) finalize Jaisal v2 face (D172 —
  awaiting user confirm of features) + Zidhan final (locked) → (1) per-character
  ANCHOR SET (frontal/3-4/profile/close-up/2 expressions) at RAW quality,
  identity-edit locked (ref_boost 4.0, D023) → (2) 2-3 refs per movie shot via
  identity edit (D021) → (3) MiniMax H3 R2V 2-3 refs + short prompts, NO music
  (D020/D041) → (4) SFX-only audio + assembly + color. The VIDEO inherits faces
  from the reference images — that IS the consistency mechanism. LoRA retrain
  PROMOTED (D175): retrain character LoRAs on the RAW base (official Krea
  workflow); dataset = anchor set with angle/expression/framing variety.
- **TIMELINE (Nov 22):** face decision TODAY → anchor set day 2-4 → per-shot ref
  set day 5-10 → R2V video week 3 → SFX/assembly week 4 → buffer + final QC.
  Only slack: the face decision is the one thing that cannot slip.
- **ENGINE DECISION REVISED (user, 19:5x IST — D175 SUPERSEDES the D174 pivot):**
  "Krea2 is the best model we have for realism — check any forums... we are
  ditching it blindly because of a skill issue." → **Krea2 STAYS the production
  engine.** Official backing (krea.ai/krea-2-open-source): Krea 2 = "the most
  aesthetic open-source image model"; official pairing = "Train LoRAs on RAW,
  then run them fast on Turbo" (Turbo = fast polished t2i; RAW = malleable base
  for LoRA training; community reviews agree: train on RAW, LoRA transfers
  between the pair).
- **Root cause of the pasty/soft outputs = USAGE, not the model:** everything
  ran on `krea2_turbo_fp8` at 10 steps / cfg 1 (fast lane), and the character
  LoRAs (`krea2fp_*`) were trained on the TURBO fp8 base.
- **THE FIX:** (1) RETRAIN character LoRAs on `krea2_raw_bf16` (Fizgig) — now
  the OFFICIAL recommendation; dataset = anchor set with angle/expression/
  framing variety (D173). (2) Production generation on RAW: **40 steps, cfg 3-4,
  real negatives** (documented settings). Turbo stays the fast iteration lane.
- **Evidence today:** `krea2_raw_qtest.json` (same chain, RAW UNet, 40 steps,
  cfg 3.5, 3 identical hard prompts — also tests whether the existing
  turbo-trained LoRA still binds on RAW) — USER TO RUN. `qwen21_face_test.json`
  (built, validated) demoted to FALLBACK COMPARISON only — Qwen-Image-2.1
  (`qwen_image_2.1_bf16` + VAE + `qwen3vl_8b_fp8_scaled` type `qwen_image`,
  25 steps cfg 1; already wired in 09j/09k; plus
  `qwen-image-edit-2511-multiple-angles-lora` on disk) stays available if Krea2
  RAW still disappoints.
- **CINEMATIC RECIPE (2026-10-23 20:2x, D176) — user: "the test you gave me
  stupid low quality result, check forums how to get good cinematic shots in
  krea2":** raw_qtest outputs graded: close-up DID gain real skin texture on RAW
  ✓; profile + two-man = flat phone-photo look. Forum/official-guide findings
  (designloves2 ComfyUI Krea2 guide built on Krea's official prompting.md;
  Andro-Meta local-studio guide; Krea2SizePreset tiers): (1) Krea2 =
  NATURAL-LANGUAGE grapher briefs — "cinematic" alone does nothing; name the
  MEDIUM early (35mm film, 85mm/35mm lens, shallow DOF, golden hour, Portra
  400, film grain, muted grade); quality tags are wasted budget. (2) AGENT SKILL
  GAP (admitted): previous prompts were actively ANTI-cinematic ("candid phone
  snapshot... NOT a studio portrait"). (3) Aspect: 1120×896 = 1K near-square;
  cinematic = 1920×1080 16:9 (1.5K tier). (4) OFFICIAL: Turbo = polished output
  checkpoint (8 steps, cfg 0.0, Mu 1.15, fp8); RAW = training/LoRA/research
  base — raw_qtest's 40-step/cfg-3.5 was an untested mush setting (my bad).
  **Built `krea2_cine_test.json`** (validated 0/0): Turbo UNET, 10 steps cfg 1
  (proven identity settings), **1920×1080**, same 3 LoRAs, 3 prompts REWRITTEN
  as film-still briefs (medium+lens+lighting+mood+grain+grade). Prefix
  `krea2_cine_test`. USER TO RUN. If still soft → next lever = Krea-specific
  Mu=1.15 sampler param (stock KSampler doesn't expose it — needs a Krea
  sampler node) + reference-image style transfer.
- **OFFICIAL SETTINGS + MU-FIX (2026-10-23 20:5x, D177):** user asked for the
  full spec for Reddit ("details are off"). Official Krea2 repo: Turbo =
  **8 steps, cfg 0.0, mu 1.15, 1K-2K**; RAW = 52 steps cfg 3.5 ≤1K. ComfyUI
  applies the mu shift via a **ModelSamplingFlux(shift 1.15)** node — which our
  chain was MISSING (stock KSampler euler+simple only). **Built
  `krea2_mu_test.json`** (validated 0/0): same chain (55→303→96→97) + node 58
  ModelSamplingFlux(1.15) → KSampler at 8 steps cfg 0, 1920×1080. Paste file
  `mu_test_3_prompts_paste.txt`. USER TO RUN — decisive missing-shift test.
  If still soft → bf16 turbo fp8-comparison + Krea two-stage sampler pack.
- **MU_TEST FAILURE FORENSICS (21:3x, D178):** user ran krea2_mu_test -> 3
  outputs BYTE-IDENTICAL (same sha256) = 3-panel face-grid, not the prompted
  content. Prompts were on disk (file intact) but the UI ran an EMPTY canvas
  state (Pixaroma clobber/cached canvas - user's "pixaroma group issue" was
  right). Face-grid = `famegrid_spicy` LoRA prior dominating with no prompt.
  **Built `krea2_control_test.json` (0/0): NO prompteach - prompts directly in
  CLIPTextEncode widgets, nothing to paste.** 2 branches, 1 queue, seed 42
  fixed, 1920x1080, 8 steps cfg 0 + ModelSamplingFlux 1.15: A = bare engine
  (zero LoRAs, `krea2_bare_A`), B = engine + character LoRA only
  (`krea2_lora_B`). USER TO RUN - A good -> our 3-LoRA stack (famegrid first
  suspect) is the problem; A soft -> fp8-turbo path is the ceiling (bf16 +
  Reddit). Rule: diagnostics NEVER use prompteach.
- **OFFICIAL TEMPLATE ADOPTED (21:5x, D179):** user: "your way of structuring
  things is different from the comfyui default workflow... skill issue... dont
  want to get embarassed infront of others." Fetched official tutorial +
  template `image_krea2_turbo_t2i.json` (saved utilities\official_image_krea2_
  turbo_t2i.json). Official = subgraph [UNET turbo fp8 -> optional style LoRA
  -> KSampler 8/cfg1/euler/simple -> VAEDecode] + ConditioningZeroOut (no
  negative) + **TextGenerate LLM prompt expansion ON** + ResolutionSelector +
  SaveImage; NO ModelSamplingFlux. **Built `krea2_official_char_test.json`
  (0/0): template as-is + Jaisal short amateur-shot prompt + enable_lora ON +
  LoRA krea2fp_v2_ep64@1.0 trigger jeskvman, seed 42.** USER TO RUN (llama-
  server 8100 must be up). If good -> all future Krea2 work built on this
  template; if bad -> bf16 + Reddit. Open: optional post-process chain
  (contrast down > grain > slight blur).
- **RECIPE VS RESOLUTION A/B (D180):** user ran template-style 2K portrait
  (1152x2048, prefix krea2_t2i_face, 5 consistent face shots) but says the OLD
  realism workflows were better; user theory: 2MP/3MP > 1MP is the main reason.
  Checked old specs: krea2_t2i_char1 = turbo fp8 + realism@1.0 + famegrid@0.7
  (NO char LoRA, NO trigger - long text identity) + FameGridColorFinish(1.0/0.6)
  + 10/cfg1 + 896x1120 + 6 long candid-snapshot prompts. New 2MP run already
  had MORE resolution, so the RECIPE is the variable, not MP. **Built
  `krea2_realism_2mp.json` (0/0): old recipe verbatim, ONLY resolution 896x1120
  -> 1152x2048**, prompteach state-blob + paste file
  `realism_2mp_prompts_paste.txt` (6 prompts). USER TO RUN (paste 6 prompts).
  Compare vs old krea2_char1_face_*: 2MP good -> MP is a safe lever; 1MP
  better -> keep recipe at 896x1120. Old recipe face matches D171 lock better
  than the char-LoRA 2MP set.
- **PROMPT WIRING FIX + CORRUPT FILE FOUND (D181):** user: "i didnt even ran
  krea2_t2i_face / image_krea2_turbo_t2i because the prompt is bad/old ... the
  prompt update and wiring update youre doing is not working properly fix that
  goddamint ... just give me workflow names and i will generate." Root cause:
  the 5 good 2MP images (krea2_t2i_face_00013..17) came from CORRUPT archived
  file workflows_archive\2026-10-18\krea2_t2i_character.json - prompteach EMPTY,
  pos encode empty, VAEDecode + FameGridColorFinish MISSING (but 1152x2048,
  realism@1.0 + famegrid@0.7, 10/cfg1, neg = plastic/waxy skin list). Images were
  made with prompts PASTED INTO CANVAS, not from the file. **NEW PERMANENT RULE:
  all test workflows = one KSampler branch per prompt, each with a VISIBLE
  CLIPTextEncode holding the text - NO prompteach, nothing to paste.** Rebuilt
  `krea2_realism_2mp.json` (0/0, 37 nodes/57 links): old recipe verbatim, 6
  visible-prompt branches, 1152x2048, seeds 42-47, neg = plastic/waxy list.
  HANDOFF LIST (names only, open fresh tab, queue): krea2_realism_2mp (main A/B),
  krea2_official_char_test, krea2_control_test. Every handoff: dump the file's
  text widgets and confirm prompts on disk BEFORE telling user it's ready.
- **RUN COMPLETE (D181 follow-up):** agent RAN krea2_realism_2mp itself via MCP
  (prompt 2ca0eafc-3fb3-4bb2-b9b7-619d46c9fee0) - 6/6 outputs in
  data\realism_2mp_run\, identity consistent across all 6, face matches D171 lock,
  quality = the "better" old-recipe look. File-driven runs work end-to-end (no
  canvas/paste). AWAITING USER: (1) pick 3 anchor frames (suggested 002/004/000),
  (2) confirm this face = Jaisal final face (settles D172). Then: face-lock anchors
- **D172 RESOLVED + CINE-MAX STACK (D182):** user picked krea2_realism_2mp_4
  (campus frontal) as Jaisal's FINAL face (v2 proposal closed). Built + ran
  krea2_cine_max.json (0/0): turbo BF16 + identity-edit + Cinematic_Artstyle@0.8
  + TEnhancer(text_scale 1.5) + Krea2EditModelPatch blur-proof path + OFFICIAL
  turbo sigma schedule (pack node) + SamplerCustom, 2048x1152 16:9, 3 cinematic
  briefs - 3/3 frames in data\cine_max_run\, face held in all 3. This is the
  anchor-frame recipe. NEXT: Zidhan face lock -> anchor sets -> R2V (no music).
  (identity-edit) -> R2V per shot. Resolution chase CLOSED per user.

## LTX-2.5 VFX PIPELINE doc created (user, 2026-10-21, D169)
- **`docs\VFX_PIPELINE_LTX25.md`** — the full Lightricks LTX-2.5 IC-LoRA "VFX week"
  timeline (HF-verified dates 2026-09-08 → 09-28: Day-To-Night, Water-Simulation,
  Clean-Plate, Deblur, Colorization, Decompression, Ingredients, Layout-To-Render,
  Refine-Details, Restore, SDR-To-HDR + scene-emb, Alpha-Gen), our base-stack status
  (ALL local: distilled DiT int8 21.5 GB, gemma4-12b encoder 15.37 GB, VAEs, latent
  upscaler, SDR→HDR + Alpha-Gen LoRAs already in loras/), the movie-pipeline mapping
  (Clean-Plate = background removal, Day-to-Night = our moody night shots, SDR→HDR =
  gradeable deliverables, Alpha-Gen = character mattes, Refine-Details, Layout-to-
  Render, Native Resolution = 4K/8K Tiled Fusion), and download recommendations:
  **download now = only ~625 MB** (`sdr-to-hdr-scene-emb` 12.6 MB — completes the HDR
  pair we half-have, `clean-plate-1.0` 306 MB, `day-to-night-0.9` 306 MB).
- **COMFYUI GAP:** `ComfyUI-LTXVideo` (Lightricks' official pack) is in the MAIN tree
  only — NOT in the running install (`comfyUi_latest`) → install + restart needed
  before any LTX VFX workflow runs.
- **"Background text addition" LoRA** (user's memory): NOT in the official Lightricks
  org — closest = `Ingredients` (09-10); possibly a community LoRA (ltx.io/ltx-
  community) — flagged for the weekly check.
- **Monitoring:** weekly schedule set (Mondays 09:00 IST, `schedule-6479d179`) — diff
  the Lightricks HF org against the doc's timeline + watch for X posts.

## 2026-10-23 - quality loop (user back from isha)
- cine_v2 community-recipe t2i (e6b8ea11): quality fixed, pasted-head gone, face
  drifted. Face-lock i2i (20cc281e) pulls face back to Jaisal, scene preserved.
- E:\Krea2 4.6GB image download STALLED at 1.5 MB after ~15 min - user to restart.
- 2-pass pipeline is the new anchor recipe (see EXPERIMENTS 2026-10-23 entry).
- TODO: user verdict on 20cc281e_000 (face-lock frame) -> tune ref_boost if
  needed -> all 3 scenes through 2-pass -> Zidhan face -> anchor sets.

### 23:3x IST - weather_v3 (4MP concrete-rain) + face_lock_v2 (denoise 0.35) - WIN
- User feedback on v2 frames: "somewhat okayish... rain droplets don't feel natural" +
  "dont rely on the outputs, just check the notes" + "stick to the other posts i shared"
  (community recipes, not guesses). E:\Krea2 4.6GB download COMPLETED (2150 images,
  4.7GB). Read NOTES.md 348-round distill + SUMMARY.md.
- **Notes recipes applied:** concrete nouns win over poetic; weather+light = Krea2's best
  trick; native 4MP finals ("looks shot, not rendered"); rain realism = CONCRETE water
  cues (rain streaks in the air, droplets beaded on hair/skin catching the light, wet
  asphalt mirror reflections, droplets in lamp beams); identity drift is expected (seed
  locks layout not face); i2i face-lock at denoise 0.5 RE-RENDERED the rain (fake
  stippled droplets) -> drop to 0.35 to preserve the canvas's natural rain.
- **weather_v3** (krea2_weather_v3.json): krea2_turbo_fp8_scaled + turbo LoRA 0.7 +
  Krea2-realism-V2 0.8 + NegPiP, 12 steps cfg 1 er_sde/simple, NATIVE 4MP 2560x1440,
  6 branches (street x3 seeds 201-203 + monsoon x3 204-206), concrete-rain prompts.
  Run 80037527. WINNERS: street_b (80037527_000) + monsoon_b (80037527_004) - face
  close to Jaisal, NATURAL rain (streaks in lamp beams, droplets on skin/hair, wet
  reflections). The concrete-noun rain fixed the "unnatural droplets" complaint.
- **face_lock_v2** (krea2_face_lock_v2.json): i2i denoise 0.35 (preserves canvas
  rain/pose), ref_boost 4.0, face-ONLY prompt ("change only the face"), 10 steps
  euler/simple cfg 1, turbo fp8 + identity LoRA 1.0. Street face-lock =
  data\face_lock_v2_run\be651d88_000.png; monsoon face-lock =
  data\face_lock_v2_run\97aed4e5_000.png. Both: face pulled to Jaisal, natural rain +
  pose + scene fully preserved, no seam.
- **NEW CANONICAL JAISAL MOVIE FRAMES (4MP):** street = be651d88_000, monsoon =
  97aed4e5_000. Backwater wide (B1) still on old 2MP e6b8ea11_000 -> needs same
  weather_v3 treatment (concrete mist/water cues) + face_lock_v2.
- TODO: user verdict on the 2 new finals -> backwater v3 4MP -> Zidhan face (UNLOCKED)
  same 2-pass -> anchor sets -> MiniMax H3 R2V (NO music D041). Deadline Nov 22.

### 23:4x IST - backwater v3 4MP + face-lock DONE - ALL 3 JAISAL FRAMES COMPLETE
- backwater_v3 (krea2_backwater_v3.json): same 4MP stack, golden-hour concrete water cues
  ("long golden reflections, thin mist layer, glassy calm water"), 3 seeds 301-303. Run
  f8a4fdbb. Winner = backwater_a (f8a4fdbb_000): golden houseboat lit windows, mirror
  reflection, mist, face close to Jaisal.
- face_lock_v2 on backwater_a (run 005d8bc9) = data\face_lock_v2_run\005d8bc9_000.png:
  face pulled to Jaisal, golden scene fully preserved, no seam.
- **THE 3 JAISAL MOVIE FRAMES (all 4MP, face-locked, natural, no graft):**
  1. STREET   = data\face_lock_v2_run\be651d88_000.png
  2. MONSOON  = data\face_lock_v2_run\97aed4e5_000.png
  3. BACKWATER = data\face_lock_v2_run\005d8bc9_000.png
- Next (objective): apply the same 2-pass to ZIDHAN (UNLOCKED - no locked face yet;
  best existing ref = output\refset_v6\zidane_bench_b25_00001_.png). Generate Zidhan
  t2i (halal fade crop, full short dense trimmed beard, white t-shirt, trigger dlor) +
  face-lock against zidane_bench_b25 -> present as candidate for user to lock.

### RAG (D194) - local RAG for project memory + daily AI news - DONE (2026-10-25)
- User directive: stop manually lurking AI subs; build local RAG (chunking -> embedding -> vector DB -> search into prompt) running daily.
- Built D:\models\vsCodeMcp\rag\: config.json (sources), chunk.py (section-aware), embed.py (all-MiniLM-L6-v2 CPU), etch_news.py (reddit JSON+playwright fallback / HF trending+downloads / X syndication best-effort), ingest_project.py + ingest_news.py (hash-manifest incremental), daily.py (orchestrator), query.py (CLI), un_daily_rag.bat, store.py (FAISS).
- Stack decisions (verified): **Ollama NOT installed** -> sentence-transformers CPU embed (no VRAM contention, D192). **ChromaDB broken on this machine** (Rust bindings SQLITE_CANTOPEN code 14 on every path, chromadb 1.3.7/1.4.1/1.5.9) -> **FAISS-cpu IndexFlatIP** instead. HF model cache redirected to ag\hf_cache\ (C:\Users\user\.cache write-blocked).
- Seed verified: **1,248 project chunks + 65 news items** (today all HF; reddit 403 / X 429 logged+retry-next-day). Query tests return correct sections.
- Scheduled task **VsCodeMcp-RagDaily (daily 08:00 Asia/Calcutta)** registered. Churn dirs gitignored.
- See ag/README.md + **D194** in DECISIONS.md.
- **Workflow sheet (2026-10-25, user request):** `P10_WORKFLOW_SHEET.md` — all 9 P10 items as
  workflow-name / source-URL (reddit-x-github-HF) / what-to-check rows, for post-restart run-by-run.
  **P9 sheet added same day (user: "why did you forget that one?"):** `P9_WORKFLOW_SHEET.md` —
  all 7 P9 items (vLo · background-swap v21a · VRGDG 2-pass [D041] · H3 Recast · char-swap
  mask [clean, runnable today] · seamless vlog clown-anchoring [audio OFF] · Ideogram-v4
  ultrawide prompt-language doc). P10 sheet now cross-references it.
- **Auto-committer EXTENDED (2026-10-25, user directive "reusable items in the repo"):** `commit_md.ps1`
  now auto-commits `.md` + `.gitignore` + reusable dirs (`utilities/` 271 scripts, `prompts/`,
  `workflows/` mirror, `episode1/`, `docs/`, `rag/` code, `challenge/`, `.vscode/`) — images/media/
  logs/dumps excluded via .gitignore (also cleaned: `data/`, `session_tmp/`, `tools/`, `*.exe`,
  `*.whl`, `*.err`, `.comfy/` untracked). New `workflows/` = 35-file mirror of the reusable
  ComfyUI workflow JSONs (canonical stays at `E:\comfyUi_latest\...\workflows`); re-sync with
  `workflows/resync_workflows.ps1`. First run: 319 files committed + pushed (2026-10-25 06:17).
  AGENTS.md D131 section updated to match.
- Fixes (2026-10-25): task-context TEMP/TMP pinned to ag\temp (scheduler session has no writable system temp); ingest_project now deletes a file's previous chunk ids before re-adding (orphan fix) + store.prune(); store pruned 213 orphans (project 1253 == manifest). RAG code committed to git.
- **Source ladder upgrade (2026-10-25, user question "why can't we use our mcp browser?"):** RAG now uses the SAME engine VS Code uses —
  `rag\news\mcp_fetch.js` (node driver importing `D:\MCP\web-search-mcp\dist\enhanced-content-extractor.js`: axios fast path +
  randomized chromium fallback, gateway's env). fetch_news.py = 3-tier ladder per source: API → mcp engine → persistent-profile
  playwright (reddit) / syndication → mcp engine (x). **Empirical wall test same day:** VS Code's own gateway (mcp websearch tool)
  ALSO gets Reddit's "Prove your humanity" / "blocked by network security" today, and X syndication 429s — the walls are
  source-side anti-bot (IP-reputation based, they rotate), not a RAG defect. Redlib mirrors probed: 429/502 (unreliable — not
  added). HF = the reliable source; digest logs exactly which tiers were blocked so blocked days are visible, and the next
  daily run retries automatically (no code change needed when a wall lifts).

### P10 download batch - ALL 24 FILES DONE (2026-10-25 03:4x)
- `hf_resumable_download.py` full sequence complete + verified (sizes + safetensors headers): 6 big MiniMax/FastH3 UNETs (incl. ref2va_fp8 19,987 MB + fl2va_int8 32,462 MB), 3 turbo LoRAs, QI2.1 UNET 6,920 MB + CLIP 8,917 MB, VNCCS LoRAs ×3 (V2 repo file has trailing space — URL `%20`), Qwen3-TTS ×11 (suite dir `models\TTS\qwen3_tts\` — suite skips re-download; node input `local:Qwen3-TTS-12Hz-1.7B-CustomVoice`).
- Script hardened: 4xx = permanent fail (log + continue, no batch crash) + safe RETRY sizing.
- VNCCS_PoseStudio_QI2.1_REFERENCE.json re-validated: 0 model errors; only `VNCCS_PoseStudio` class restart-gated.
- **All agent-side P10 work complete.** Remaining = USER: restart ComfyUI (20 packs) → run checklist in P10_BATCH.md; item-5 manual assets (SMPLX_NEUTRAL.npz, Mixamo FBX, one-person video); item-7 clean first frame + 24 fps/%32 inputs.
