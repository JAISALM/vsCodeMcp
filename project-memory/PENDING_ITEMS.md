# PENDING ITEMS — movie project (2026-10-24 ~16:00 IST)

One-by-one queue for the 2-man football movie. Each item: what it is, what's already
ready (details on disk), what's needed to start, how to start. User directive (2026-10-24):
"we have all the details about it, but we haven't started yet — list them out and we will do one by one."

Details live in: `AUDIO_PIPELINE_PLAN.md` (audio), `D112`/`D106` + `EXPERIMENTS.md` 2026-10-12
(Blender), `WORKFLOW_HISTORY.md` (workflows), `DECISIONS.md` (rules), `MOVIE_RESUME.md` (state).

---

## P1 — MALAYALAM LIP-SYNC + MOVIE AUDIO (D050) — **SETUP DONE** (2026-10-24) — awaiting user dubs

**Setup completed this session:** toolchain verified on disk (rvc venv ✓, openvoice
venv ✓, `clean_audio.py` CLI = `<input> -o <out_dir>` → `<stem>_clean.wav`,
`collect_references.py` ✓, `convert_character.py` ✓, `references\mithun` ✓,
`02_audio_raw` ✓). Created `03_audio_converted\` + `04_lipsync\` (05_final
pre-exists). **NEW: `D:\models\ai-movie\scripts\run_dub_pipeline.py`** — per-character
pipeline: raw dubs → clean (openvoice venv) → RVC convert (`rvc venv infer\cli.py
--f0-method rmvpe --protect 0.4`) → summary. RVC entry points = `repos\rvc-webui\
infer\cli.py` (convert) + `train\train.py` (train) + `webui.py`.
**LatentSync NOT yet cloned** (`repos\LatentSync` absent; WSL2 distros present,
Stopped — `wsl --list`). Next user actions: record dubs (headset) → drop in
`02_audio_raw\<char>\` → target-voice refs in `references\<char>\` (10+ min) or
`--skip-convert` → train `models\rvc\<char>.pth` (heavy GPU) → run
`run_dub_pipeline.py --character <char>` → then LatentSync (WSL2, repo clone +
`setup_env.sh` — heavy, coordinate with user).

**What:** user dubs all Malayalam dialogue (PC headset) → voice-convert per character (RVC) →
LatentSync lip-sync onto the scene videos → DaVinci assembly (user). This is the big "we haven't
really done it" item — every stage below is still untouched.

**Route decision (D050, 2026-09-08, user-confirmed):** the movie uses **RVC voice conversion,
NOT TTS**. TTS (Fish S2 Pro / IndicF5) Malayalam sounds non-native (Tamilian accent, flat flow).
User performs ALL lines themselves (pace/emotion = the acting); VC changes only timbre.
**TTS tools = PARKED** (both working, for future kids content) — do NOT re-invest in TTS for the movie.
OpenVoice = zero-shot fallback, but it garbles Malayalam words (English-centric timbre swap) —
production words come from the user's own clean dubs.

**Ready (verified on disk 2026-10-24):**
- RVC repo `D:\models\ai-movie\repos\rvc-webui` (RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
  + venv `D:\models\ai-movie\envs\rvc` (py3.12, torch 2.7.1+cu128 — RVC needs torch <2.8).
  Setup script `D:\models\ai-movie\scripts\setup_rvc.ps1`.
- RVC per-character recipe: 10+ min clean target-voice audio → train (F0 via RMVPE + HuBERT +
  FAISS index) → user dubs lines → `clean_audio.py` → RVC convert → LatentSync → DaVinci.
  Key params: `--f0_method rmvpe`, `--protect 0.3-0.5`, `--alpha 0.1-0.2`.
- `clean_audio.py` (run with openvoice venv python `D:\models\ai-movie\envs\openvoice\Scripts\python.exe`):
  any format → mono → **DeepFilterNet neural denoise** → loudnorm -16 LUFS → trim silence → 16 kHz mono
  → `<stem>_clean.wav`. BUILT + TESTED (2026-09-07).
- Voice reference: `D:\models\ai-movie\references\mithun\` (5 clean clips, 56–124 s each).
- `collect_references.py` (batch-clean a voice-notes folder → reference-ready 16 kHz mono + duration
  summary) + `convert_character.py` / `convert_multi_ref.py` (OpenVoice zero-shot; RULE: multiple short
  clean clips as a LIST, never one long concat).
- Demucs 4.1.0 in openvoice venv (`python -m demucs --device cpu --two-stems=vocals`) — only if a
  source has music baked in (movie-source dubbing; the user's headset dubs won't need it).
- Malayalam text handling (D116): type **Manglish → convert per scene** via
  `D:\models\vsCodeMcp\prompts\manglish_to_malayalam.txt` (local LLM pass — tone + name consistency
  lock). Dictation: Win+H (quick) or `D:\models\vsCodeMcp\utilities\transcribe_malayalam.py`
  (Whisper large-v3, Audacity WAV → `.ml.txt` with timestamps).
- **WSL2 = INSTALLED** (verified 2026-10-24: `docker-desktop` + `Ubuntu-22.04` distros present,
  state Stopped). LatentSync needs WSL2 (bash `setup_env.sh`) — this unblocks P1 step 4.

**Not started / needed (order):**
1. **USER:** record dubs per character (Jaisal, Zidhan, + any supporting cast) on headset, quiet
   room → drop raw files in `D:\models\ai-movie\02_audio_raw`.
2. **Target voices:** 10+ min clean reference per converted character (friends' voice notes →
   `collect_references.py` → pick best clip) — OR decide a character keeps the user's own voice
   (no conversion). **OPEN QUESTION for user:** which of Jaisal/Zidhan get converted voices vs
   the user's own? (Movie is now 2 men — the old 15-character ref plan in AUDIO_PIPELINE_PLAN is
   stale scope; only its tooling carries over.)
3. **RVC:** train per-character model (first RVC training run ever — never done).
4. **LatentSync:** set up in WSL2 (bash `setup_env.sh` in a conda env; checkpoints
   `latentsync_unet.pt` + `whisper/tiny.pt` from `ByteDance/LatentSync-1.6`). Facts: 1.6 = 18 GB
   VRAM (**D045: close ComfyUI first**), 16 kHz audio, 25 fps, 512×512 faces, **photoreal faces
   only** (no line-art/sketch). Params: `inference_steps` 20–50, `guidance_scale` 1.0–3.0.
5. Lip-sync each scene clip → `04_lipsync` → **USER: DaVinci Resolve** (import synced video, add
   ambience, export H.264).

**Rules:** **D041 NO MUSIC** (dialogue + natural ambience only). **D045** no LatentSync while
ComfyUI is active. STOP-ON-FAILURE for env changes.

---

## P2 — BLENDER LAYOUT → VIDEO (blockout → camera-ref → H3 R2V) — **NOT STARTED for movie scenes** (user-named)

**What:** blockout each movie scene in Blender → render a 5 s square camera-motion reference →
feed character-ref + environment-ref + camera-ref into MiniMax H3 R2V → finished scene video.
Pipeline is PROVEN (boar-grave case); the movie's 6 scenes have not been blockout-rendered.

**Ready (verified on disk 2026-10-24):**
- Blender **5.2.2 LTS** at `C:\Program Files\Blender Foundation\Blender 5.2` (NOT D:).
- Blender MCP end-to-end VERIFIED 2026-10-12 (D106): headless bridge
  `blender --background --online-mode --python D:\MCP\blender_mcp\start_bridge.py` (port 9876;
  keep the process alive — restart via `D:\MCP\blender_mcp\start_blender_bridge.bat` or background
  job), full 26-tool `blender-mcp.exe` server, scene build + render from pure code (11-object
  Kerala blockout → `BLENDER_EEVEE` 1024×576 render PASS).
- **Proven recipe (EXPERIMENTS.md 2026-10-12, boar-grave 5 angles):**
  - Blockout = grass ground + house cube + slanted-slab roof + 2 trees (cylinder trunk + sphere
    canopy) + character placeholder (cylinder body + sphere head) + sun + camera. Silhouette state
    = char1 BLUE / char2 RED for identification, then restore.
  - Camera motion = 5 s speed-ramp orbit: quick settled holds + fast travels, single extreme
    close-up (~3.75 s, both eyes visible), ends exactly at opening framing (seamless loop).
    Mannequin on checkerboard, soft light. Save editable .blend + render square mp4.
  - **Blender 5.2 gotchas:** engine ID = `BLENDER_EEVEE` (no `BLENDER_EEVEE_NEXT`);
    **NO FFMPEG in `render.image_settings.file_format` enum** → render a **PNG frame sequence**
    (`bpy.ops.render.render(animation=True)`) → encode with the bundled imageio_ffmpeg binary
    `E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe`
    (`-framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 19`);
    `scene.action.fcurves` absent in 5.2 (unified action system) → skip interpolation loops.
- **H3 R2V workflow:** `E:\minimax_workflow\blender+minimax\video_minimax_h3_r2v-workflow.json`
  (UI format, 25 nodes / 27 links): `MiniMaxH3ReferenceToVideo` **node 136**, native widget shape
  `[prompt, 1344, 768, 124, 'match']` (5 s @ 25 fps) ← LoadImage character-identity ref +
  LoadImage environment ref + **LoadVideo camera-reference mp4** (R2V accepts a video ref) →
  SaveVideo. Demo variant: `video_minimax_h3_r2v_blender_Comfyui_demo.json`.
- Package: `E:\minimax_workflow\blender+minimax\` (D112) — guide PDF
  `Blender_to_MiniMax_Complete_Guide.pdf` (14.7 MB), refs, workflow screenshots. Boar-grave kit
  staged at `E:\minimax_workflow\blender+minimax\boar_grave\` (blend + 5 renders + camref mp4 +
  identity refs + both workflows + README). `face_yolov8m.pt` in `models\ultralytics\bbox\`.

**To do (movie):** blockout the 6 scenes — S1 paddy (post-harvest, rain, farmers), S2 behind
normal Kerala house, S3 inside house, S4 Kerala bike, S5 minimal 7's ground, S6 rural village →
per-scene 5 s camref → H3 R2V with character refs from the new Klein LoRA set (P3).
**Boar-grave note:** the two existing blockout angles (side + upper) are ENOUGH — no rebuild.

---

## P3 — CHARACTER LoRA v2 (Flux Klein dataset) — **IN PROGRESS** (user building the Klein workflow, self-run)

- **Dataset = 20 images** (10 Jaisal + 10 Zidhan) generated from the immutable refs
  (`data\character_finals\{jaisal,zidhan}_final.png`) via **`flux-2-klein-9b` +
  `Flux2-Klein-9B-consistency-V2`** LoRA (both present in `E:\ComfyUI_windows_portable\ComfyUI\models\`).
- Diverse: the 6 movie scenes + close-ups / 3-4 angles / a profile + mixed lighting (overcast /
  warm / indoor); face clear and well-lit. **Zidhan: full short dense beard in ALL 10** (the beard
  was the old LoRA's failure — it came out clean-shaven). **Jaisal: clean-shaven/faint stubble,
  black tee, crooked nose.** Strict per-image curation: reject noisy/drifted/blackout images —
  no "acceptable" (2026-10-24 user verdict).
- **Train: rank 32 (~16 per subject), ~15–20 epochs, triggers `jeskvman`/`dlorman`** → ~2–3 h on
  the 5090. **Full rank (7 h) rejected as overkill for 2 subjects.** Tooling: Fizgig PRIMARY
  (D167, LoRA Isolation for 2 subjects — the 2026-10-22 `krea2fp` train recipe: People mode =
  Fizgig LoRA Isolation, sample prompts = one trigger per line), AI Toolkit SECONDARY.
- Then: retest with triggers across all 6 scenes at the strict bar (show user, never self-certify).
- Supersedes old Krea2-based `krea2fp_v2_ep64` (Zidhan clean-shaven) as the character identity pin.

---

## P4 — H3 R2V VIDEO for the 6 movie scenes — **NOT STARTED** (blocked on P3)

- Per scene: **2–3 frame refs max** (D020), each an explicit frame anchor for one shot with a
  simple prompt; **6-section R2V prompt with `<Picture N>`/`<Subject N>` tags in connection
  order** (D017, guide `docs\MINIMAX_H3_R2V_PROMPTING_GUIDE.md`); 5 s @ 25 fps, 1344×768 (1 MP);
  **NO MUSIC (D041)** — `non_diegetic_music` = the no-music statement, `overall_soundscape` =
  natural sounds only.
- Scene set FINAL (no boat): S1 post-harvest paddy (rain, farmers working), S2 behind a normal
  Kerala house, S3 inside a Kerala house, S4 on a Kerala bike (rural road), S5 minimal local 7's
  ground (small goals, low fence, benches — NOT a stadium; prompt proven), S6 rural village
  (paddy + homes + palms).
- Refs = Klein-LoRA stills (face + style anchors, D021) + optionally a Blender camref (P2) for
  the camera motion.
- **HARD DEADLINE: Nov 22.**

---

## P5 — SFX (ControlFoley) + DaVinci assembly — **NOT STARTED** (blocked on P4)

- **ControlFoley TC-V2A PROVEN** (2026-09-03, 3 package bugs patched on disk): workflow
  `jaisal_sketch_title_audio.json` (built by `utilities\build_controlfoley_audio.py`) — chain
  `LoadControlFoleyModel` → `ControlFoleyGenerate` ← `LoadControlFoleyVideo`;
  `ControlFoleyGenerate` → `SaveControlFoleyAudio` (WAV) + `MuxControlFoleyAudioToVideo` (replace
  → MP4). Submit with NAMED inputs via `utilities\submit_controlfoley.py` (bypasses the
  positional-widget misalignment). Prompt = the EXACT natural sounds in story order + the D041
  no-music rule. `guidance_scale` 4.5, `num_inference_steps` `fixed`, `seed` 42, batch 40.
  (ControlFoley was weak on 2D line-art — for photoreal H3 clips it's the right tool.)
- Per-scene sounds: S1 rain + paddy ambience + farmers + splashes, S2 house ambience + insects,
  S3 interior room tone, S4 bike engine + road + wind, S5 crowd + ball + whistle, S6 village birds
  + wind.
- **DaVinci Resolve assembly = USER** (dialogue + ambience only, no music; export H.264).

---

## P6 — SeedVR2 2K upscale (stills + video) — **READY, NOT STARTED for movie assets**

- Models present: `seedvr2_ema_7b_sharp_fp16.safetensors` (16.48 GB) + `ema_vae_fp16.safetensors`
  (0.50 GB) in `E:\ComfyUI_windows_portable\ComfyUI\models\SEEDVR2\`.
- Workflows BUILT + VALIDATED (0 errors): `seedvr2_image_upscale.json` (image → 2K 1440×2560,
  LoadImage node 1 + SaveImage prefix), `seedvr2_video_upscale.json` (1080 shortest-edge,
  batch 33, temporal_overlap 3, offload cpu), `seedvr2_lastframe_2k.json`. **D100: stop Qwen
  first, fresh tab.**
- Use: 2K upscale of final keeper stills + scene videos (original 2026-09-06 target = title video;
  never run). RULE: get more pixels with SeedVR2 post, NOT by upscaling the latent.

---

## P7 — LONG-SHOT SUITES: H3-LongTakeNoCuts + Herrgotts-H3-Infinite-Continuation-Suite — **BOTH PACKS INSTALLED + ANALYZED 2026-10-24, not yet loaded** (user-named)

Two complementary long-video packs, both cloned to `custom_nodes\` (one restart loads both —
do NOT restart mid-Klein-workflow). Full analyses in WORKFLOW_HISTORY.md 2026-10-24 entries.

**A. `xyzDist/H3-LongTakeNoCuts`** — 4 low-level nodes; fixes the motion-context "photocopy
effect" (degradation from segments 5–6 when extending without cuts) via a few-step SAM3-masked
REFINE resample (denoise 0.5–0.6) blended back into the chain latent at frames 22–44. Best for
ONE continuous shot: 360°/location-detail environment walk-throughs, the intro oner.
Examples → `E:\minimax_workflow\H3-LongTakeNoCuts\` (**v2 = the one to use**). Deps: ALL
SATISFIED (NikoDemon80 motion-context ✓ — the correct non-fork ✓, KJNodes ✓, Easy-Use ✓,
MiniMax-H3-Turbo ✓, core `SAM3_Detect` ✓, fl2va+ref2va int8 ✓, SAM3 ✓).
Limitations: workaround not fresh-regen; best on moving shots; audio artifacts = open question.

**B. `HerrgottMargott/Herrgotts-H3-Infinite-Continuation-Suite` v1.4** — 27 nodes (4 generations);
FL2VA **clip chain** with **native Masked AV continuation**: previous clip's full AV latent
copied in-place into the next target, protected by ComfyUI's native per-stream denoise masks
(video prefix mask 0 = preserve / future video 1 = generate; audio independently protected →
**dialogue can continue past the visual seam** = killer feature for our dubbing pipeline).
Auto Handover detects FL2VA freeze/brightness landing tails, snaps to the exact shared AV
boundary (39-frame contexts = 39/90/141/192… frames; default 39 ≈ 1.625 s @ 24 fps);
Last-Frame quality resets; Qwen References; Net New Content duration mode;
`H3ContinuousStitchSavedChainV14` = memory-bounded assembly of very long projects.
CRITICAL REQUIREMENT — **VERIFIED SATISFIED**: core PR #15375 per-stream H3 AV masks — our core
**v0.37.0 @ 8d534945e (2026-09-27)** has it (`comfy/ldm/minimax/model.py` carries separate
`denoise_mask` + `audio_denoise_mask`). Models ALL PRESENT: fl2va int8 ✓, `qwen3vl_32b_minimax_
h3_nvfp4_awq` ✓, `minimax_h3_video_vae_fp16` ✓, `minimax_h3_audio_vae_fp32` ✓.
Examples → `E:\minimax_workflow\Herrgotts-H3-Infinite-Continuation-Suite\` (01_Start, 02_
Continue, **03_3Clip_Showcase_AutoStitch**, 04_Stitch_Saved_Chain, README, 6.7 MB 11-clip
v1.4 demo mp4). Limitations: no HQ audio reset (audio drift over very long chains); carryover
preserves only already-generated audio; Net New Content = longer sampling; GPL-3.0.

**Verdict (2026-10-24, user asked "which is better?"):** **B (Herrgotts) = the PRIMARY
long-shot tool for the movie.** Native in-place AV preservation beats A's
blend-back workaround at the seam, and its first-class audio (previous-tail carryover →
ambience/dialogue continues past the seam) feeds P1 lip-sync. A stays the lightweight
fallback for a PURE R2V motion-context shot with no Last-Frame anchors (360° walk-through,
intro oner) — B supports keyframe-free continuation too, just less tested.
**Audio nuance (user asked "this locks the same audio?"):** the protected region carries
the previous clip's audio forward VERBATIM (seam = no cut/pop); beyond it H3 GENERATES new
audio from the prompt (H3 native audio = prompt-controlled ambient → fits D041; the
user's RVC dub layers over it in DaVinci). It cannot restore audio that was never
generated (mid-word cut source clips still need regen).
**When to use which:** A = one continuous R2V shot extended (environment walk, intro
oner). B = long multi-clip scenes with DIALOGUE + known endpoints (movie scenes S2/S3/S5
talking across 15–30 s; feeds P1 lip-sync cleanly). Complementary — both load on the
same restart.

**To do:** (1) **ComfyUI restart** at a convenient point → verify both packs' nodes appear.
(2) Validate the Herrgotts v1.4 examples (start with 03 showcase) + LongTakeNoCuts v2 against
our ComfyUI. (3) Test runs. (4) Apply to movie + intro (see use cases in WORKFLOW_HISTORY).

---

## P8 — `E:\minimax_workflow` workflow inventory — **DONE** (2026-10-24) → `docs\MINIMAX_WORKFLOW_INVENTORY.md`

User: "we need to check the workflows we have here inside this folder, but that's an open work."
**COMPLETED (2026-10-24):** all 24 top-level JSONs + 6 subfolders audited against the live
`/object_info` catalog (read-only). **8 files fully runnable today** (incl. the P4 tool
`video_minimax_h3_r2v+turbo.json`); 7 more with cosmetic gaps (note nodes) or one small pack
(rgthree — unlocks `minimax_h3_sam_r2v_2char_cinematic.json`, directly relevant to the 2-man
movie); 7 need real pack installs (EastMoe / JW / RAMCleanup / BiRefNet / BFSShot / refmod /
zuanfilm — gap list in the doc); 1 is a platform export (inline-graph v2 — not loadable).
Subfolders: P7 suites present (`H3-LongTakeNoCuts` v01/v02, `Herrgotts-H3-Infinite-
Continuation-Suite` v1.4 01–04 + README); `MiniMax-H3-NativeAudio-MusicVideo-Workflow` = full
git repo (music-oriented → low value under D041); `blender+minimax` = P2 assets;
`character_sheet` = 5 sheet workflows; `consistent_environment` = MyRoom refmod experiment.
Full table + pack gap list → `docs\MINIMAX_WORKFLOW_INVENTORY.md`.
~24 top-level workflow JSONs + subfolders (`blender+minimax`, `character_sheet`,
`consistent_environment`, `MiniMax-H3-NativeAudio-MusicVideo-Workflow`, `production_experiments`)
— audit what each is, which nodes it needs, which are runnable on our install, which are stale.
Top-level files include: `Ep29 MiniMaxH3_Continuation_Workflow.json`,
`fl_minimax_h3_turbo_lora_example_workflow.json`, `H3-Contest_BaseWorkflow.json`,
`h3_refmod_cinematic.json`, `minimaxH315SecondSeamlessMulti_v11.json`,
`minimaxH3Camera_v10/v20.json`, `minimax_h3_character_swap_workflow.json`,
`MiniMax_H3_FL2VA_Fiirst-and-Last-Frame-Workflow.json`, `minimax_h3_sam_r2v_*`,
`qwen_minimzed_h3.json`, `video_minimax_h3_r2v(+turbo).json`, `WF-H3_zuanfilm-*`,
`Dialogues.json`, `Minimax H3 Workflow_ Magic Time Period Shift.json`,
`minimax-h3-guided-consistent-characters-*.inline-graph.json`, `mini-max-refrance-to-video-1.json`,
`2BZ_H3_character_sheet_2stage_v1_EN.json`, `Workflow for Minimax H3 image editing w ComfyUI.json`.
Plus the new `H3-LongTakeNoCuts\` folder (P7).

---

## P9 — INCOMING QUEUE (user feeds one-by-one from 2026-10-24 16:36 IST onward)

User: "we have few more github repo's to check and a new model too … i will give one by one,
update the memory." **Process each as it arrives:** install → analyze thoroughly (read the code,
not just the README) → verify deps/models on disk → record in WORKFLOW_HISTORY.md + add/extend a
pending item here → commit. Log each entry below as it lands:

| # | Item | Status |
|---|------|--------|
| 1 | `HerrgottMargott/Herrgotts-H3-Infinite-Continuation-Suite` (long-shot FL2VA clip chain, native Masked AV) | **DONE 2026-10-24** — installed + analyzed; core capability + models verified ✓; examples + 11-clip demo copied; merged into P7. Awaiting the shared restart. |
| 2 | `Shrey-1o1/ComfyUI-Krea2-FilmStudio-Vionex` (reddit r/StableDiffusion 1vn7avz "KREA 2 Film Studio" — all-in-one film workflow + one-node pack) | **DONE 2026-10-24** — installed + analyzed. Stills-ONLY (0 MiniMax nodes in the pack — the "minimax loop" = our own still→H3 handoff, i.e. the movie flow itself). Deps ✓ (RES4LYF, krea2edit, T-Enhancer, GGUF); models ✓ (`krea2_turbo_fp8_scaled` + `qwen3vl_4b_fp8_scaled` + `krea2RealVae_v10`); only `comfyui-krea2-controlnet` missing (= optional CONTROL sub-feature). Not loaded (shared restart), not run. Notes → EXPERIMENTS.md + REPOS.md. |
| 3 | **7-item batch (user 2026-10-24 ~18:39 IST — goal-loop, one-by-one, no ComfyUI runs):** (1) vLo repo (PxTicks/vlo) · (2) reddit 1xbzw1o H3 replace-background 4K · (3) reddit 1xahodr production H3 music video + workflows + GitHub URLs (D041 note) · (4) reddit 1x9n0dl H3 recast swap up to 3 people · (5) reddit 1xbljy9 character swap H3 reference-to-video LoRA · (6) reddit 1x84uym seamless vlog 1-click (long-shot — check all node links) · (7) reddit 1ucdyvr ultrawide cinematic shots Ideogram v4 (KEEP prompts/film language ONLY — do NOT apply settings — adapt for Krea2) | **IN PROGRESS** — item 1 vLo **DONE**: cloned `D:\models\ai-movie\repos\vlo`, analyzed (README + install.bat + node script + 14 bundled default workflows incl. H3 i2v/inpaint/flf2va/r2v + krea2_turbo + klein_multi), full-capability install running in background (managed Node 22 + Python 3.13 + CUDA torch + SAM2 + SAM-Audio), 4 missing node packs (WanVideoWrapper, ComfyUI-vlo, controlnet_aux, GIMM-VFI) being installed into our ComfyUI → **add to shared restart list (P7)**. Details → REPOS.md "Video editing" section. Items 2–7 pending. |

**Tonight's plan (user, 2026-10-24):** user trains the Klein LoRA tonight (P3) and sleeps.
Agent standby: dataset curation on request. Work window = 16:36 IST → night.

---

## DO-NOT-RUN — dead routes (do NOT resurrect; 2026-10-24 user verdict)

- `k2f_jaisal_scenes.json` (run `a663e26c` — all 6 outputs REJECTED: face drift + noise).
- `k2f_zidhan_scenes.json` (built unvalidated — same rejected 2-pass approach).
- Face-lock-to-HD (`k2f_*_hd*.json`, `data\flock_hd_run`) — REJECTED.
- t2i re-rolling for an approved face (D163 dead end).
- `data\jaisal_variations\` = **NOT a verified set** — do NOT use as a LoRA dataset.
