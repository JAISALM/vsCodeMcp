# PENDING ITEMS — movie project (2026-10-24 ~16:00 IST)

One-by-one queue for the 2-man football movie. Each item: what it is, what's already
ready (details on disk), what's needed to start, how to start. User directive (2026-10-24):
"we have all the details about it, but we haven't started yet — list them out and we will do one by one."

Details live in: `AUDIO_PIPELINE_PLAN.md` (audio), `D112`/`D106` + `EXPERIMENTS.md` 2026-10-12
(Blender), `WORKFLOW_HISTORY.md` (workflows), `DECISIONS.md` (rules), `MOVIE_RESUME.md` (state).

---

## P1 — MALAYALAM LIP-SYNC + MOVIE AUDIO (D050) — **NOT STARTED** (user-named)

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

## DO-NOT-RUN — dead routes (do NOT resurrect; 2026-10-24 user verdict)

- `k2f_jaisal_scenes.json` (run `a663e26c` — all 6 outputs REJECTED: face drift + noise).
- `k2f_zidhan_scenes.json` (built unvalidated — same rejected 2-pass approach).
- Face-lock-to-HD (`k2f_*_hd*.json`, `data\flock_hd_run`) — REJECTED.
- t2i re-rolling for an approved face (D163 dead end).
- `data\jaisal_variations\` = **NOT a verified set** — do NOT use as a LoRA dataset.
