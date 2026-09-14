# JAISAL KUT — REUSABLE INTRO PIPELINE (Krea2 keyframes → MiniMax H3 video)

**Purpose:** this is the reusable workflow structure for the Jaisal Kut intro (and
future intros). The 2026-09-13 plant-keyframe run is the FIRST full pass — going
forward we evaluate whether we need this many keyframes.

**Core principle (user, 2026-09-13):**
- **Keyframes = NEUTRAL face + LOCKED scene/props** (plants, flowers, table,
  setup). The keyframe's job is to lock IDENTITY + SCENE + PROPS so MiniMax has a
  stable anchor and does NOT mess up the setup.
- **MiniMax H3 = MOTION + FACIAL EXPRESSION.** The prompt drives the emotion
  (joyful / melancholic / determined); the **Continuity cast** locks identity so
  the face doesn't drift.
- **Do NOT bake emotion into the keyframe** — the identity workflow locks the face
  to the reference (neutral), so emotion-in-prompt loses. Keep the keyframe face
  neutral; let MiniMax bring the emotion in the video.

---

## STAGE 1 — KEYFRAMES (Krea2 Identity Edit)

**Workflow:** `krea2_identity_edit.json` (Krea2 Identity Edit v1.2).
**Build scripts:** `utilities/build_plant_keyframes_v9.py` (plants),
`utilities/build_intro_keyframes_v8.py` (the 6-shot set).

### Node map (the reusable knobs)
| Node | Type | Role |
|---|---|---|
| 55 | UNETLoader | **`krea2_turbo_bf16.safetensors`** (bf16 = quality; FP8 = ceiling) |
| 71 | LoraLoaderModelOnly | `krea2_identity_edit_v1_2.safetensors` @ 1.0 (identity lock) |
| 72 | LoadImage | **PRIMARY ref** = the consistency anchor (e.g. `kf2_hands_table.png`) |
| 113 | LoadImage | **SECONDARY ref** (optional — e.g. the plants-alive image for kf6) |
| 92 | VAEEncode | encodes the secondary ref (enable only when 113 is used) |
| 79 | Krea2EditModelPatch | `[ref_boost_primary, ref_boost_secondary, 'fit']` (fidelity dials) |
| 84 | Krea2EditGroundedEncode | **positive prompt** (the CHANGE + camera; identity handles the rest) |
| 85 | Krea2EditGroundedEncode | **negative prompt** |
| 82 | EmptySD3LatentImage | `[2048, 1152, 1]` (output grid; `fit` snaps to ref size ~1928×1088) |
| 29 | SaveImage | save prefix |
| 114 | rgthree Image Comparer | **BYPASSED** (mode 4) |

### The reusable recipe
1. **Pick the base reference** (node 72) = the consistency anchor for the shot
   (e.g. `kf2_hands_table.png` = character, hands on table, facing camera).
2. **Write a SHORT prompt** (node 84) = the CHANGE (plants/props) + camera. The
   identity workflow reproduces character/B&W/table/wall from the ref — you only
   describe what's NEW.
3. **Neutral face** — do NOT put emotion in the prompt (it loses to the ref).
4. **For a state-change shot** (alive→dead): use the **2-ref** approach —
   primary = base (locks character), secondary = the previous state (locks
   prop positions). `ref_boost` = `[4, 2, 'fit']`.
5. **Negative (node 85):** no color, no grain/noise, no extra chairs, no hands
   under table, no wall texture, no facial distortion.
6. **Model = bf16** (node 55) for quality.
7. **Run one-by-one** → review → stage the good output to `input\` +
   `Jaisal-intro\<batch>\` → use it as the next shot's secondary ref.

### Quality settings (LOCKED — do not "fix" these)
- **Steps 10, cfg 1.0, euler/simple, denoise 1** — correct for the turbo model.
  **Do NOT raise steps** (distilled model → over-sharpening/artifacts).
- **Output ~1928×1088** (the identity-edit LoRA is a 1MP pipeline; `fit` snaps to
  the ref size). This is the LoRA's sweet spot — NOT a bug.
- **2K/4K = SeedVR2 upscale in post** (see Stage 3), NOT in-workflow.

### Noise fix (2026-09-13 lesson)
The "noisy/speckled wall" was the PROMPT: `fine film grain` + `dark charcoal
wall` → the model added grain + a textured wall. **Fix:** prompt = `clean smooth
image, NO grain, NO noise, NO speckles` + `background is SMOOTH and fades into
COMPLETE BLACK DARKNESS - no visible wall, no texture`. Verified: corner-std
noise proxy dropped 6.87 → 0.0.

---

## STAGE 2 — VIDEO (MiniMax H3)

**Workflow:** MiniMax H3 i2v/R2V (SLA stack, <240s at 1MP — D042).
**Identity lock:** `jaisal_continuity_character.json` (`MiniMaxH3Creator`,
Continuity pack) — cast-based, locks the character across shots.
**Camera motion:** `H3LocalCameraEditor` (installed + live) — compiles a 3D
camera trajectory (azimuth/elevation/distance keyframes) into H3 prompts. No LoRA
needed (optional `camera_motion_h3_lora` improves fidelity).

### The reusable recipe
1. **Feed the keyframes** as references (2-3 max, each = a shot's anchor — D020).
2. **Prompt drives MOTION + EMOTION** (the keyframe face is neutral; the prompt
   says "joyful smile" / "melancholic look" etc.).
3. **Continuity cast** locks identity so the face doesn't drift between shots.
4. **Camera node** for any camera move (e.g. the 180° head-twist shot).
5. **NO MUSIC** (D041) — natural sounds only.

---

## STAGE 3 — UPSCALE (SeedVR2)

**Tool:** SeedVR2 TensorRT Studio (`d:\models\SeedVR2-TensorRT-Studio`,
`Launch SeedVR Studio Pro.bat` → `http://127.0.0.1:7870`) OR ComfyUI SeedVR2
nodes (`SeedVR2Conditioning`/`Preprocess`/`PostProcessing`, models in
`models\SEEDVR2\`).
**Model:** `seedvr2_ema_7b_sharp_fp16.safetensors` (best quality).
**Pipeline:** Krea2 keyframe (1MP) → **SeedVR2 7B Sharp → 2K/4K**. This is how
we get Krea2-quality 2K–4K without fighting the LoRA's 1MP training.

---

## THE 11-KEYFRAME SET (script order) — see `docs/INTRO_KEYFRAME_PLAN.md`
kf1_empty → kf2_seated → kf3a_headnormal → kf3c_head90 → kf3b_head180 →
kf5a_stem → kf5_plants_grown → kf6_plants_dead → kf7a_page → kf7b_page_mic →
kf7c_cricket.

**Motion pairs for MiniMax (first → last):**
- Shot 1 walk-in: kf1 → kf2
- Shot 3 twist: kf3a → kf3c → kf3b
- Shot 5 growth: kf2 → kf5a → kf5
- Shot 6 dying: kf5 → kf6
- Shot 7 assembly: kf2 → kf7a → kf7b → kf7c
- Shot 4 reverse: kf2 (reversed in post)

---

## FOLDER RULE (user, 2026-09-13)
Batch outputs go in `Jaisal-intro\<batch>\` (e.g. `v8\`, `v9\`) — NEVER loose in
ComfyUI `output\jaisal_cut\`. ComfyUI `input\` copies are only for workflows to
load; the project folder is the source of truth.

## KEY LEARNINGS (2026-09-13)
1. **Identity workflow locks the face to the ref** — emotion-in-prompt loses.
   Keep keyframe faces neutral; MiniMax drives emotion.
2. **bf16 > FP8** for quality (`krea2_turbo_bf16` already installed).
3. **Noise = prompt** (`fine film grain` + `charcoal wall` → grain + textured
   wall). Fix with `clean smooth, no grain` + `smooth black darkness`.
4. **2-ref for state changes** (alive→dead) locks prop positions; but the
   secondary ref can make the output "same as the ref" if the state-change
   prompt is weak — if kf6 looks like kf5, drop the secondary ref (anchor to
   base only) so the model draws the dead state from scratch.
5. **1MP generate + SeedVR2 upscale** = the 2K/4K path (not in-workflow 2K).
6. **One-by-one** — generate, review, stage, then the next. No batch.
