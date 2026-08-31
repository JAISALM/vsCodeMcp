# Workflow History

Newest changes first.

---

## 2026-08-31 — krea2_jaisal_sketch.json (new)

### Workflow

krea2_jaisal_sketch.json — Krea2 2D vector / line-art t2i generator for the Jaisal Cut title animation (stick figure).

### Objective

Generate the 2D line-art reference images for the title animation (a stick figure that walks the bridge, throws a paper plane, jumps into the river). The first image is the WALKING medium shot — the anchor we feed to MiniMax H3 so it animates the walk + head-turn + whistle + jump.

### Changes

- Cloned from the native `krea2_jaisal_refs.json` (preserves all native widget shapes / pos / size / inputs / outputs — no machine-built widget bug).
- LoRA node (15) → `krea2_lineart_v1_fp16.safetensors` @ 1.0 (the Civitai "Krea2 Line Art Style" LoRA, downloaded 2026-08-31).
- Positive prompt (node 6) → the WALKING stick-figure medium-shot prompt (2D vector line art, stick figure, line-art bridge + wavy line river, full body visible, medium shot).
- Negative prompt (node 13) → the sketch negative (excludes 3D / shading / color fill / cartoon / wide shot / close-up / special effects).
- SaveImage (29) → `jaisal_cut/sketch`.
- KSampler (3): 8 steps, cfg 1.0, euler/simple, denoise 1.0 (t2i). EmptyLatentImage (5): [2048, 1152, 1].

### Configuration

- Chain: UNET `krea2_turbo_fp8_scaled` → LoRA `krea2_lineart_v1_fp16` @1.0 → KSampler → VAEDecode → SaveImage.
- CLIP `qwen3vl_4b_fp8_scaled` (krea2), VAE `qwen_image_vae`.
- 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 1.0.
- Build script: `d:\models\vsCodeMcp\utilities\build_krea2_sketch.py`.

### Result

RAN (22.7s) → `output\jaisal_cut\sketch_00001_.png` (2048×1152). Pending user review in ComfyUI (vision unavailable in agent).

### Decision

Pending user review — confirm the line-art stick figure is clean (lines only, no shading/color fill, single character, medium shot). If good, this is the MiniMax anchor.

### Reason

User wants a 2D vector / line-art title animation (a stick figure, lines only, no cartoon/3D). The line-art LoRA carries the look. See D027.

---

## 2026-08-27 — krea2_jaisal_title_moody.json (new)

### Workflow

krea2_jaisal_title_moody.json — i2i fix for the FINAL/title shot: add ONLY moody climate, keep structure + boy position.

### Objective

- The final (aerial/title) shot was "messed up". Rather than recreate it, take the existing `storysheet_09_cut_title_scene_00001_.png` (staged as `jaisal_title_scene.png`) and add **only moody climate** — the bridge structure, river, banks, and the boy's position (MIDDLE of the bridge) stay EXACTLY the same.
- The camera ANGLE is handled separately by the user via their Qwen multi-angle workflow — this i2i does NOT change the angle.

### Changes

- Source image: `jaisal_title_scene.png` (from `output\jaisal_cut\storysheet_09_cut_title_scene_00001_.png`).
- Positive prompt: same scene/composition as reference (wide aerial stone bridge, boy in middle), keep structure/river/banks/position EXACTLY, ONLY change climate to MOODY (heavy dark overcast storm clouds, dim cold grey light, low mist, light rain, wet glistening stones, muted desaturated colors, dramatic moody lighting). Style prefix + single-character guard.
- KSampler: seed 424242, 8 steps, cfg 1.0, euler/simple, **denoise 0.4** (atmosphere-only, structure preserved).
- SaveImage prefix `jaisal_cut/title_moody`.
- Negative: carried over from krea2_jaisal_medium.json (identity/structure guard).

### Configuration

- Locked Krea2 chain: UNET `krea2_turbo_fp8_scaled` + LoRA `Krea2_Cinematic_Artstyle` @1.0 + CLIP `qwen3vl_4b_fp8_scaled` (krea2) + VAE `qwen_image_vae`.
- 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 0.4.
- Built from krea2_jaisal_medium.json template (UI format). Validated via MCP (valid, 0 errors).

### Result

Built + validated, NOT yet run. Pending user run + review in ComfyUI.

**2026-08-27 FIX (root cause):** machine-built `widgets_values` arrays were built from the API `/object_info` order, which is MISSING hidden widgets → arrays too short → positional shift → KSampler `cfg='euler'`/`sampler_name='simple'`/`scheduler=0.4` validation errors + LoadImage not showing. **Native UI-saved files use a DIFFERENT shape:** KSampler = **7** values `[seed, control_after_generate, steps, cfg, sampler_name, scheduler, denoise]` (hidden `control_after_generate` = randomize/fix/+1/-1 dropdown next to seed), LoadImage = **2** values `[filename, "image"]`, and native files have **NO `widgets_values_named` key**. Fixed with `fix_native_shape.py` (KSampler=`[424242, 'randomize', 8, 1.0, 'euler', 'simple', 0.4]`, LoadImage=`['jaisal_title_scene.png', 'image']`, all `widgets_values_named` removed). Verified against native files + MCP validation (`valid: true`, 0 errors). **Open in a FRESH tab (not the stale `#converted-` view).** NOTE: this bug affects ALL machine-built workflows (the 08-27 converted batch + `jaisal_drone_optimized.json` + `krea2_jaisal_medium.json`) — fix them the same way before running.

### Decision

Pending user review — confirm the moody climate is added while the bridge structure and the boy's middle-of-bridge position are preserved.

**2026-08-27 POSE-DRIFT FIX:** user reported the boy's HEAD POSITION was changing between the reference and the i2i output. Root causes: (1) denoise 0.4 regenerates enough of the figure to re-derive the head angle; (2) the prompt re-described the pose as a fresh action ("looking at the sky above") instead of anchoring it to the reference, so the model re-posed it; (3) the negative's "different head position, different look" was too vague to push against. Fix applied via `fix_title_moody_prompts.py`:
- **Denoise 0.4 → 0.3** (biggest lever — preserves pose far better for a climate-only edit).
- **Positive:** anchor pose to reference — "EXACTLY matching the reference pose and head angle", "Keep ... body pose, and head angle EXACTLY the same as the reference", and describe the pose as a static state ("head tilted back with face and gaze turned upward toward the sky") rather than a new action.
- **Negative:** replaced the vague "different head position, different look" with concrete pose-locking terms: "changed pose, different pose, different body position, head facing forward, head turned to the side, looking down, looking at camera, turned away, different head angle, different body angle, shifted position, moved position".
- Validated: `valid: true`, 0 errors.
- **If head still drifts at 0.3:** try denoise 0.25, or use an inpaint/mask workflow (mask = sky + background only, exclude the boy) so the figure is never regenerated.

### Reason

User: "lets not recreate, lets add the moody climate alone for this storysheet_09_cut_title_scene_00001_ image in i2i, then i will get the angle from qwen multiple character angle workflow."

---

## 2026-08-26 — krea2_jaisal_aerial_v5.json (new)

### Workflow

krea2_jaisal_aerial_v5.json — drenchiness + face-continuity fixes for beats 08, 09

### Objective

- Beat 08 (v4) had the right pose/scene but was missing the DRENCHED/wet look from the previous shot.
- Beat 09 (v4) had a changed face (new kid) + a double-character problem.

### Changes

- **Beat 08 v5** (storysheet_08_cut_aerial_wide_v5): i2i from jaisal_ss08v4.png (the v4 08), SAME pose/scene, added DRENCHED/WET look (soaked hair/uniform, dripping, water droplets, wet glistening bridge), denoise 0.55.
- **Beat 09 v5** (storysheet_09_cut_aerial_title_v5): i2i from the NEW 08 v5 (chained, so the face stays consistent), boy = tiny dot far away, SINGLE character, DRENCHED, strong duplicate + "different face/new kid" negative.
- Negative strengthened: different character, different face, different boy, new kid, changed face, duplicate character, 2 kids, two kids, second kid, multiple people, extra person, double, twin, two figures, two boys, two people, reflection, mirror image.

### Configuration

- Same locked style chain + prefix
- 2048×1152, 8 steps, cfg 1.0, euler/simple
- Denoise: 0.55 (beat 8 — keep pose, add drench), 0.6 (beat 9 — zoom to tiny dot)
- Beats 8→9 chained for face continuity

### Result

All 2 frames generated, 2048×1152.

### Decision

Pending user review — confirm 08 v5 (drenched + same pose) and 09 v5 (same face, single character, tiny dot).

### Reason

The aerial section must keep the drenched look and the SAME kid's face across 08→09. Chaining 09 from the new 08 preserves the face; the drench prompt restores the wet look.

---

## 2026-08-26 — krea2_jaisal_aerial_v4.json (new)

### Workflow

krea2_jaisal_aerial_v4.json — corrected aerial sequence (beats 07, 08, 09)

### Objective

Fix the aerial "cut" section: beat 07 had a tilted camera; beat 09 had a double-character problem.

### Changes

- **Beat 07** (storysheet_07_cut_aerial_start_v4): NO camera tilt, boy centered (horizontally + vertically), bridge runs VERTICALLY through the frame (road/bridge surface behind the boy visible), boy looking up at the camera, close/medium. i2i from jaisal_medium_mid2.png.
- **Beat 08** (storysheet_08_cut_aerial_wide_v4): camera risen higher + pulled away (drone zoom-out), boy smaller + centered, more bridge + water revealed. i2i from beat 07 (chained).
- **Beat 09** (storysheet_09_cut_aerial_title_v4): max wide, boy = tiny dot, sky dominates upper frame (negative space for title), SINGLE character. i2i from beat 08 (chained).
- **Negative prompt strengthened** against duplicates: duplicate character, 2 kids, duplicated kids, two kids, second kid, multiple people, extra person, double, twin, two figures, two boys, two people, reflection, mirror image.

### Configuration

- Same locked style chain + prefix
- 2048×1152, 8 steps, cfg 1.0, euler/simple
- Denoise: 0.7 (beat 7), 0.6 (beats 8, 9)
- Beats 7→8→9 chained for a continuous drone ascent

### Result

All 3 frames generated, 2048×1152.

### Decision

Pending user review — confirm 07 no-tilt centered vertical-bridge, 08 zoom-out, 09 single-character max-wide.

### Reason

The aerial section must read as one continuous no-tilt drone ascent ending on a single-character wide shot for the title.

---

## 2026-08-26 — krea2_jaisal_fix05_inpaint.json (new)

### Workflow

krea2_jaisal_fix05_inpaint.json — inpaint the collar/tie region of beat 05 to remove the tie

### Objective

Remove the tie from storysheet_05 (rain close-up gust) that a low-denoise i2i (v3, v4) failed to remove. Inpainting regenerates ONLY the masked collar/tie region; the face, bag, and environment stay locked.

### Pipeline

- LoadImage (jaisal_ss05v4.png) → VAEEncode → SetLatentNoiseMask (mask) → KSampler (denoise 1.0, seed 545) → VAEDecode
- Mask: jaisal_ss05_tie_mask.png (grayscale ellipse over the collar/tie region) → ImageToMask (red channel) → GrowMask (expand 20, tapered_corners false)
- Prompt: "the shirt collar is open and untied, NO tie, no necktie, no bow tie"; negative: tie, necktie, bow tie, knotted tie, tied collar

### Result

storysheet_05_rain_closeup_gust_inpaint_00001_.png (2048×1152).

### Decision

Pending user review — confirm tie gone, face/bag intact. Adjust the mask ellipse if it missed the tie or bled into the face.

### Reason

A high-contrast element (tie) survives low-denoise i2i. Inpainting isolates the change to the masked region.

---

## 2026-08-26 — krea2_jaisal_continuity.json (new)

### Workflow

krea2_jaisal_continuity.json — visual-continuity fixes for the Jaisal Cut story sheet

### Objective

Fix continuity problems between shots WITHOUT independently redesigning scenes. i2i from the frame that already has the correct look, change only the specific problem.

### Fixes

- **Beat 3** (storysheet_03_run_medium_rain_v3): i2i from jaisal_ss04v2.png (04's preferred environment) + medium running prompt → transfers 04's background into 03's composition. Fixes the 03→04 background mismatch.
- **Beat 5** (storysheet_05_rain_closeup_gust_v3): i2i from jaisal_ss05v2.png + "NO tie, no necktie, open collar", denoise 0.5 → removes ONLY the tie, preserves bag color/environment/composition.
- **Beat 6** (storysheet_06_rain_closeup_clearing_v3): i2i from jaisal_ss06v2.png + "red school bag with BOTH shoulder straps visible", denoise 0.5 → fixes the missing strap, preserves everything else.
- **Beats 7→8→9** (chained aerial ascent): 07 from medium anchor (close/medium, kid centered, looks up at camera, bridge+water below) → 08 from 07 (risen higher, kid smaller, full bridge + more water) → 09 from 08 (max wide, kid = tiny dot, sky dominates, negative space for title). One continuous drone shot.

### Configuration

- Same locked style chain + prefix
- 2048×1152, 8 steps, cfg 1.0, euler/simple
- Denoise: 0.7 (beat 3, 7), 0.5 (beats 5, 6 — single-element fixes), 0.6 (beats 8, 9 — camera changes)
- Shared negative prompt node (includes tie, necktie, blue bag, duplicate character)

### Result

All 6 frames generated, 2048×1152.

### Decision

Pending user review — confirm 03↔04 background match, 05 tie removed, 06 both straps, 07→08→09 continuous aerial ascent.

### Reason

Visual continuity is the top priority for MiniMax to blend the frames into a coherent video. Targeted i2i from the good frame preserves identity/environment while fixing only the problem.

---

## 2026-08-26 — krea2_jaisal_storysheet.json (new)

### Workflow

krea2_jaisal_storysheet.json — the 9-image story sheet for "The Jaisal Cut"

### Objective

Generate all 9 story beats in one batch, each i2i from its anchor, so the face stays identical within each framing group.

### Anchors

- Beats 1, 2, 8, 9 (wide): jaisal_base_final.png (Anchor A)
- Beats 3, 7 (medium): jaisal_medium_mid2.png (medium anchor, kid at middle of bridge)
- Beats 4, 5, 6 (close-up): jaisal_face_v4_A.png (Anchor B)

### Beats (temporal order)

1. storysheet_01_run_wide — kid at start of bridge, calm sky, rain clouds on horizon
2. storysheet_02_run_mid_rain — kid mid-bridge running, first rain streaks, sky darkening, wind
3. storysheet_03_run_medium_rain — kid running, rain falling, dynamic, water splashing
4. storysheet_04_rain_closeup_start — kid's face, rain starting, looking ahead
5. storysheet_05_rain_closeup_gust — gust of rain sweeping across, droplets in frame, moody, wind-blown
6. storysheet_06_rain_closeup_clearing — rain gone, kid stopped, looking up, droplets on face
7. storysheet_07_cut_medium_pan — kid looking up, camera beginning to pan, sky clearing
8. storysheet_08_cut_wide_clearing — full scene, kid small figure, sky clearing, light breaking through
9. storysheet_09_cut_title_scene — title moment scene (kid looking up, sky clearing) WITHOUT text (title composited in post)

### Configuration

- Same locked style chain + prefix as base/face/medium
- 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 0.7
- Seeds: 101, 202, 303, 404, 505, 606, 707, 808, 909
- Shared negative prompt node (NEG) on all 9
- Beat 9 prompt explicitly excludes text/letters/words/title

### Result

All 9 frames generated, 2048×1152, ~3 min total on RTX 5090.

### Decision

Pending user review — flag weak frames for re-roll, then wire best 6-9 into MiniMax H3 video.

### Reason

9-image story sheet is the input for the MiniMax H3 ref-image-to-video (15s). Temporal order matters (MiniMax reads refs left-to-right as a storyboard).

---

## 2026-08-26 — krea2_jaisal_medium.json (new)

### Workflow

krea2_jaisal_medium.json — medium shot anchor for "The Jaisal Cut"

### Objective

Create a medium shot (head + upper body on the bridge) — wider than the face close-up (Anchor B) but tighter than the wide base (Anchor A). i2i from the face anchor to lock the kid's identity.

### Previous Version

krea2_jaisal_face_v3.json (face close-up, Anchor B)

### Changes

- i2i from jaisal_face_v4_A.png (latest face anchor)
- Prompt: medium shot, head + upper body, stone bridge handrails, paddy fields + coconut palms + open sky, no houses
- Same locked style chain + prefix as base/face
- denoise 0.7, 8 steps, cfg 1.0, euler/simple, 2048×1152
- Seeds: 343, 454, 777

### Result

krea2_medium_00001_.png (343), krea2_medium_00002_.png (454), krea2_medium_00003_.png (777) — all 2048×1152, ~16-20s each on RTX 5090.

### Performance

~16-20s per 2K image.

### Decision

User picked **00003 (seed 777)** as the base. Refined v2 (i2i from 00003): plain square handrail posts (no rounded/decorative), zoomed out a bit more (medium half shot), left hand holding the red school bag for support after running. krea2_medium_v2_00001_.png (555), krea2_medium_v2_00002_.png (888).

### Reason

Medium shot is the bridge between the wide base and the face close-up; needed for the story sheet's medium framing beats.

### Refinement notes (v2)

- Anchor changed from jaisal_face_v4_A.png → jaisal_medium_00003.png (keep approved composition, apply targeted fixes)
- Prompt: "medium half shot", "a little more of the bridge around him", "plain simple square stone handrail posts and a plain flat stone railing", "no rounded shapes, no decorative or exotic railing details", "his left hand holding the strap of a red school bag for support after running"
- Negative prompt added: rounded handrail, rounded railing, decorative railing, exotic railing, ornate railing, curved railing, fancy railing
- Output prefix → jaisal_cut/krea2_medium_v2

### Refinement notes (mid — middle of bridge)

- User preferred v2_00001 but the framing showed the kid at the START of the bridge with close trees/paddy fields
- Anchor changed → jaisal_medium_mid.png (the preferred v2_00001)
- Prompt: "standing at the middle of the stone bridge, the bridge stretching away on both sides", "the lush paddy fields and tall coconut palms are far in the background, distant and small"
- Negative prompt added: close trees, close paddy fields, foreground trees
- Output prefix → jaisal_cut/krea2_medium_mid
- Result: krea2_medium_mid_00001..2.png (seeds 666/999). **jaisal_medium_mid2.png (mid_00001) staged as the medium anchor** for the story sheet.

---

## 2026-08-26 — Baseline inventory (no changes)

### Workflow

All existing saved workflows in E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows

### Objective

Record the known-good baseline before any modifications begin.

### Previous Version

None — initial inventory.

### Changes

None. Inventory only.

Image:

- jaisal_shot1_t2i.json
- jaisal_shot2_i2i.json
- jaisal_shot3_i2i.json
- jaisal_sketch_shot1_i2i.json
- jaisal_sketch_shot2_i2i.json
- jaisal_sketch_shot3_i2i.json
- krea2_jaisal_base.json
- krea2_jaisal_face.json
- krea2_jaisal_face_v2.json
- krea2_jaisal_face_v3.json
- kerala_kid_2d_ref.json
- _ref_krea2_t2i_int8.json
- oneNode-Flux.json

Video:

- video_minimax_h3_t2v.json
- mini-max-refrance-to-video-1.json
- MiniMaxH3_NativeAudio_MusicVideo_TEMPLATE.json
- RIFE_WAN_Method_Interpolation_TEMPLATE.json

Chained series (each with a GGUF variant):

- 05_Chained.json / 05_GGUF_Chained.json
- 06_Chained_AudioLock.json / 06_GGUF_Chained_AudioLock.json
- 07_Chained_RefImage.json / 07_GGUF_Chained_RefImage.json
- 08_Chained_RefImage_AudioLock.json / 08_GGUF_Chained_RefImage_AudioLock.json

### Result

Baseline recorded.

### Performance

Not benchmarked yet.

### Decision

Keep all as-is until individually changed.

### Reason

Preserve known-good workflows; compare every new version against this inventory.

---


---

## jaisal_drone_optimized.json (MiniMax H3 optimized drone ascent)

Date: 2026-08-27
Status: Built + validated, NOT yet run

### Purpose

Fast 15s drone-ascent shot for "The Jaisal Cut" (kid on bridge -> tiny dot). First-last-frame interpolation via fl2va model, optimized for RTX 5090 speed.

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_drone_optimized.json

### Models

- UNET: minimax_h3_fl2va_pruned_int8_convrot.safetensors (first-last-frame)
- LoRA: minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors (turbo 4-step, strength 1.0)
- CLIP: qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (type minimax)
- VAE: minimax_h3_video_vae_fp16.safetensors + minimax_h3_audio_vae_fp32.safetensors

### Key custom nodes

- MiniMaxH3ActivationChunkStar7 (Star7 pack) - attention_backend=comfy_kitchen_int8, chunk_tokens=8192, mlp=8192, qkv=4096
- RTXVideoSuperResolution (comfyui_nvidia_rtx_nodes) - 2x ULTRA upscale
- MiniMaxH3ReferenceToVideo (core) - ref_image_0=jaisal_mm_start.png, ref_image_1=jaisal_mm_final.png

### Resolution / params

- 864x480 (0.4MP 16:9), 362 frames (15s @24fps), BasicScheduler simple/8/1, KSamplerSelect res_multistep
- Save prefix: video/Jaisal_Drone

### Chain

UNETLoader -> LoraLoaderModelOnly -> MiniMaxH3ActivationChunkStar7 -> BasicScheduler + BasicGuider -> SamplerCustomAdvanced -> VAEDecode -> RTXVideoSuperResolution -> CreateVideo(24fps) -> SaveVideo

### Known issues

- NOT yet run. First run should be timed (target <15-20 min for 2K; this is 0.4MP so faster).
- Star7 pack must be loaded (ComfyUI restarted after clone).
- widgets_values_named were stale from the turbo template and FIXED (all 7 modified nodes consistent).

### Next improvement

- Run at 0.4MP, time it, review quality. Then bump to 2K (1344x768 or higher) and re-time.
- If CK INT8 quality is too approximate, try attention_backend=existing (native pytorch cross-attention) or Spectrum.

## jaisalproduction1.json + jaisalproduction2.json (MiniMax H3 R2V, 2-pipeline — CURRENT)

Date: 2026-08-30
Status: Built + validated (`valid: true`, 22 nodes each), NOT yet run

### Purpose

The full ~26s title sequence split into **two separate MiniMax R2V generations** (shorter clips = less style drift, cleaner 3-ref mapping, the jump is a natural splice point). Shot 3 (running medium) removed.

- **`jaisalproduction1.json`** — run-up, **15s**, save `video/Jaisal_Production_1` (prompt v10 + REFERENCE VIDEO + 1MP, 2026-08-30):
  - ref_image_0 = jaisal_1_longshot.png → [Shot 1] **WIDE ANGLE** establishing shot (camera positioned FAR AWAY, boy a small figure with full landscape/sky/river visible, NOT a medium/close-up, camera fixed), ONLY ONE boy (standing on the LEFT side of the bridge, NO extra characters) WALKS and SLOWLY RUNS (natural gait, feet lift+land separately, NOT a slide), MAIN PURPOSE = ESTABLISH THE CLIMATE AND MOOD (sky clear→moody, RAIN BEGINS TO FALL and builds, landscape shifting) **~4s** (00:00.000)
  - ref_image_1 = jaisal_2_closeup.png → [Shot 2] close-up, boy RUNS, then SLOWS + STOPS + TURNS toward HIS RIGHT = the VIEWER'S LEFT (toward the river), the turn is clear and deliberate (body rotates fully) **~6s** (00:04.000 → 00:10.000) (UNCHANGED — stable)
  - ref_image_2 = jaisal_4_middle.png → [Shot 3] SIDE view from the VIEWER'S LEFT (boy on viewer's left, facing the handrail) → the boy is **NOT a static frame** - he is **SLOWLY LIFTING HIS LEG and CLIMBING over the handrail, then JUMPING** (NO hand gestures/head shake - that confused the model), he is not repeating the movement, he breathes in after the run → then **LEAPS over the handrail SLOWLY fully airborne** (the bridge is TALL - a real leap from height over the wide river, NOT a shallow pool) → camera ANCHORED on viewer's left + TRACKS him (NOT a left-to-right sweep) → camera swings to his BACK side, ENDS at his back mid-air **BEFORE he reaches the water** (the cut happens here so the next clip picks up the jump) **~5s** (00:10.000)
  - **ORIENTATION block:** "The boy's RIGHT side is the VIEWER'S LEFT side of the frame. When the boy turns toward his right, he turns toward the VIEWER'S LEFT. [Shot 3] is a side view from the VIEWER'S LEFT side, and the boy is on the VIEWER'S LEFT of the frame." + "All left/right references use the VIEWER's perspective".
  - **RAIN enforced in EVERY shot (v7):** detailed_description global line "RAIN is present in EVERY shot - rain is falling in [Shot 1], [Shot 2], and [Shot 3]" + overall_soundscape "RAIN THROUGHOUT the whole video (light rain building in [Shot 1], heavier rain in [Shot 2] and [Shot 3])". Shot 1 = rain BEGINS and builds; Shot 2 = rain streaks visible; Shot 3 = HEAVY RAIN.
  - **Sound (v10):** "Clear footsteps on the stone bridge, RAIN THROUGHOUT the whole video (light rain building in [Shot 1], heavier rain in [Shot 2] and [Shot 3]), a building thunderstorm with distant thunder rumbles, splashing water on the bridge stones, then a rising tension as the boy climbs and leaps."
  - **overall_landscape (v10, NEW):** "We should see VISIBLE RAINFALL throughout the sequence after the first picture - rain is clearly falling and visible in [Shot 2] and [Shot 3]."
  - **REFERENCE VIDEO (motion anchor, 2026-08-30):** a `MiniMaxH3ReferenceVideoLoadStar7` node (id 149) loads `input\jaisal_prod1_ref.mp4` (= the good output `Jaisal_Production_1_00011_.mp4`) → wired to `ref_videos.ref_video_0` (link 303) + `ref_video_audios.ref_video_audio_0` (link 304) so the new render FOLLOWS THE SAME ACTION. The 3 reference images stay as visual anchors.
  - **Resolution (2026-08-30):** `ResolutionSelector` (node 115) set to `['16:9 (Widescreen)', 1.0, 32]` → **1344×768 (MiniMax H3 NATIVE canvas)**. The 2K (2.4 MP) render VRAM-thrashed (stuck at 0/8 steps in "Model Initializing" for 10+ min on the 32 GB card) so it was dropped. 1MP fits VRAM, ~25–40 min. For 2K, render at 1MP then UPGRADE with an upscaler (Topaz/RTX/Hunyuan, all installed). Render-time baseline from the user's own outputs: ~10–15 min per 0.4 MP, so 1MP ≈ 25–40 min.
  - **CRITICAL (v3→v4):** MiniMax DROPPED Shot 3 entirely in the v2 run → prompt hard-emphasizes "ALL THREE shots must appear in this order, each getting its full time - do not skip, compress, or drop any shot, especially [Shot 3]" (in summary + detailed_description). **v4:** the wide shot is ALSO a hard demand — "[Shot 1] MUST be a LONG WIDE establishing shot (a hard requirement - it must NOT be cut short, NOT turned into a close-up, NOT skipped)" + slow running + the shot's MAIN PURPOSE is to ESTABLISH THE CLIMATE CHANGE. **v5:** orientation fix (boy's right = viewer's left, all left/right from viewer's perspective), shot 3 camera anchored on viewer's left + tracks (NOT a left-to-right sweep), sound = running footsteps + thunderstorm rumbles, sliding fix (real gait, feet lift+land separately). **v6:** CHARACTER COUNT block HARD-DEMANDS ONLY ONE character / no duplicates (v5's shot 1 came out with 2 boys), shot 3 JUMP made explicit + sped up (crouch → plant → LEAP over handrail → DIVE into river fully airborne, "NOT just climbing/standing/walking"), sound adds a big SPLASH as he jumps. **v7:** SIMPLIFIED (removed the heavy CHARACTER COUNT block + over-stuffed negative constraints that "didn't apply well"), shot 1 focuses on CLIMATE + MOOD (boy WALKS / SLOWLY RUNS), shot 3 ENDS mid-air BEFORE the water (bridge is TALL, NOT a shallow pool, cut at the apex so the next clip picks up the jump), RAIN enforced in EVERY shot (detailed_description global line + overall_soundscape). **v8:** timing split 4/6/5 (shot 1 = 4s, shot 2 = 6s 00:04.000→00:10.000 with a clear deliberate turn, shot 3 = 5s 00:10.000), shot 3 STARTS IN MOTION ("the boy is ALREADY RUNNING and IN MOTION at the start - he is NOT standing still" + <Picture 3> definition = "already running toward the handrail") because v7's shot 3 starting frame came out standing still. **v9:** shot 3 camera moves RESTORED to v5 (anchored on viewer's left + tracks, swings to back), shot 3 is NOT a static frame - the boy PREPARES while the camera moves (shakes head, hand gestures, gets ready) then LEAPS (replaces v8's over-constrained "already running at the start"), <Picture 3> definition = "preparing to jump over the handrail", CLEAN RULE = state WHERE he is + WHAT he is doing in ONE direction (no running back and forth). **v10:** shot 1 = **WIDE ANGLE** establishing shot (camera positioned FAR AWAY, boy a small figure with full landscape/sky/river visible, NOT a medium/close-up) + ONLY ONE boy on the LEFT side of the bridge (NO extra characters), shot 3 = **SLOWLY LIFTING HIS LEG and CLIMBING over the handrail, then JUMPING** (removed the v9 hand gestures/head shake that confused the model), he is not repeating the movement, he breathes in after the run, LEAPS SLOWLY, new **overall_landscape** section (VISIBLE RAINFALL throughout after the first picture).
- **`jaisalproduction2.json`** — leap + title, **11s**, save `video/Jaisal_Production_2`:
  - ref_image_0 = jaisal_5_jump.png → [Shot 1] SHORT natural leap CLOSE to bridge (NOT a long throw) ~2s
  - ref_image_1 = jaisal_6_underwater.png → [Shot 2] underwater, sinks completely down, rising bubbles ~4.5s
  - ref_image_2 = jaisal_7_title.png → [Shot 3] title card, bubbles foam up, 'The Jaisal Cut' slowly becomes visible, color grade matches shot 2 ~4s

Both prompts lock a consistent color grade (same dark moody palette / dim grey light / water color). **Splice:** pipeline 1 ends mid-launch, pipeline 2 starts in-air → hard cut + color-match the splice frame in post. Build script: `build_production_pipelines.py`.

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction1.json
E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction2.json

---

## jaisal_lowangle.json (MiniMax H3 R2V, 7-image — SUPERSEDED by the 2-pipeline split)

Date: 2026-08-30 (rebuilt from the 2-image version)
Status: Built + validated (`valid: true`, 0 errors, 26 nodes), NOT yet run

### Purpose

Cinematic 7-shot R2V sequence for "The Jaisal Cut" (production-quality intro). Uses **7 reference images** as frame anchors, one per shot:
- `jaisal_1_longshot.png` → `ref_image_0` → `<Picture 1>` → [Shot 1] long shot (boy runs, sky darkens, wind + rain begins)
- `jaisal_2_closeup.png` → `ref_image_1` → `<Picture 2>` → [Shot 2] close-up (camera push-in + wind)
- `jaisal_3_running.png` → `ref_image_2` → `<Picture 3>` → [Shot 3] running (camera tracks alongside, wind + rain)
- `jaisal_4_middle.png` → `ref_image_3` → `<Picture 4>` → [Shot 4] middle full figure (ADD heavy rain)
- `jaisal_5_jump.png` → `ref_image_4` → `<Picture 5>` → [Shot 5] wide low-angle jump (camera completes motion into river)
- `jaisal_6_underwater.png` → `ref_image_5` → `<Picture 6>` → [Shot 6] underwater (boy sinks completely down)
- `jaisal_7_title.png` → `ref_image_6` → `<Picture 7>` → [Shot 7] title card (bubble-formed 'The Jaisal Cut')

All transitions smooth and organic. **CRITICAL:** `<Picture N>` maps 1-to-1 to `ref_image_N` in connection order (each reference = its shot's first frame). Bag color = BLACK school bag. Title shown in Shot 7 (not a text overlay).

### 2026-08-30 rebuild (2-image → 7-image)

Rebuilt with `build_minimax_7shot.py`: copied the 7 output images to `input\` (clean names), added 5 LoadImage nodes (147-151), grew node 136 to 7 `ref_image` slots (3-9), shifted downstream link slots (prompt→13/width→14/height→15/length→16), added links 289-294, wrote the 7-shot prompt (node 138). **Note:** this is a deliberate departure from the earlier "keep R2V to 2-3 refs" lesson — the user has a full 7-image set and wants a 7-shot cinematic sequence, so each reference is a clean per-shot anchor (not a confused 5-anchor storyboard).

### Purpose (2-image, 2026-08-28 — SUPERSEDED)

15s two-shot R2V sequence. Uses **2 reference images** as frame anchors: `1.png` (boy at START of bridge) → [Shot 1], `2.png` (boy in MIDDLE of bridge) → [Shot 2]. The boy walks → weather turns → runs through the rain. Title composited in post.

### 2026-08-28 rebuild (5-image → 2-image)

The 5-image version came out bad (style drift, kid not running, model confused by 5 `<Picture N>` tags + a 500-word prompt). Rebuilt with `build_2ref.py`: deleted LoadImage nodes 143/LA4/LA5 (3.png/4.png/5.png) + links 285/289/290, cleared `ref_image_2/3/4` link fields, wrote a SIMPLE prompt with only 2 `<Picture N>` tags (each explicitly "the first frame of [Shot N]"). **Lesson: keep R2V to 2-3 reference images max with a simple prompt — the model maps refs to shots far better with fewer, clearer anchors.**

### Purpose (original 5-image, 2026-08-27 — SUPERSEDED)

15s five-shot R2V sequence for "The Jaisal Cut" low-angle ending. Uses 5 reference images (1.png–5.png) as frame anchors for 5 shots, ending on a low-angle long shot with negative space for the title (composited in post).

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_lowangle.json

### Models

- UNET: minimax_h3_ref2va_pruned_int8_convrot.safetensors (ref2va — reference-to-video)
- LoRA: minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors (turbo 4-step, strength 1.0)
- CLIP: qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (type minimax)
- VAE: minimax_h3_video_vae_fp16.safetensors + minimax_h3_audio_vae_fp32.safetensors

### Key custom nodes (CURRENT 7-image)

- MiniMaxH3ReferenceToVideo (core, node 136) — 7 ref images wired (slots 3-9):
  - ref_image_0 = jaisal_1_longshot.png → `<Picture 1>` → [Shot 1]
  - ref_image_1 = jaisal_2_closeup.png → `<Picture 2>` → [Shot 2]
  - ref_image_2 = jaisal_3_running.png → `<Picture 3>` → [Shot 3]
  - ref_image_3 = jaisal_4_middle.png → `<Picture 4>` → [Shot 4]
  - ref_image_4 = jaisal_5_jump.png → `<Picture 5>` → [Shot 5]
  - ref_image_5 = jaisal_6_underwater.png → `<Picture 6>` → [Shot 6]
  - ref_image_6 = jaisal_7_title.png → `<Picture 7>` → [Shot 7]
- LoadImage nodes: 137 (1), 139 (2), 147 (3), 148 (4), 149 (5), 150 (6), 151 (7)
- ref_image_size: match

### Resolution / params

- 1344x768 (2K 16:9), 15s, BasicScheduler simple/8/1, KSamplerSelect res_multistep
- Save prefix: video/Jaisal_2Ref_1_2 (update to e.g. video/Jaisal_7Shot for the 7-shot run)

### Prompt style (CURRENT 2-image — SIMPLE)

Official MiniMax H3 R2V style but SIMPLIFIED (see `d:\models\vsCodeMcp\docs\MINIMAX_H3_R2V_PROMPTING_GUIDE.md`):
- Only `<Picture 1>` + `<Picture 2>` tags, each explicitly "the first frame of [Shot N]"
- `<Subject 1>` = the boy (both pics), `<Subject 2>` = the stone bridge (both pics)
- 6-section structure kept but SHORT (no 500-word bloat)
- 2 shots: [Shot 1] boy at start of bridge, walks, sky darkens, wind, rain, starts running; [Shot 2] At 00:07.000 boy in middle of bridge, running through heavy rain, drenched
- Title composited in post (NOT rendered by the model)

### Shot plan (15s, 2 shots)

- Shot 1 (0-7s): boy at start of bridge (from 1.png), walks forward, sky darkens, wind picks up, rain begins, boy starts running
- Shot 2 (7-15s): boy in middle of bridge (from 2.png), running through heavy rain, fully drenched, water splashing on stones, camera follows

### Known issues

- 5-image wiring bug FIXED (2026-08-27): `ref_image_3`/`ref_image_4` had `link=None` despite links existing. Fixed by setting `link` by slot index (6/7), not name number (3/4). See `fix_lowangle_wiring_and_prompt.py`.
- 5-image version came out bad (style drift, no running) → rebuilt as 2-image (2026-08-28).
- NOT yet run. Confirm ComfyUI running with Star7 pack before running.

### Next improvement

- Run the 2-image version, review quality in ComfyUI.
- If 2-image works, this is the template for all future R2V shots (2-3 refs max, simple prompt).
- If the boy still doesn't run, try adding a 3rd reference (a running pose) or a stronger motion verb in the prompt.

## krea2_identity_edit.json (Krea2 Identity Edit v1.2 — face consistency)

Date: 2026-08-29
Status: Validated (`valid: true`, 1 expected warning), ready to use

### Purpose

Lock the SAME face across the Jaisal Cut reference set (D023). "Use an image like a LoRA": load a reference (character sheet / clean close-up), write a plain-English instruction, regenerate the scene keeping the same face/identity. Fixes the "different guy every time" problem from t2i.

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json

### Models / nodes

- UNET: krea2_turbo_fp8_scaled.safetensors
- LoRA: krea2_identity_edit_v1_2.safetensors @ 1.0 (INSTALLED, 1.83 GB)
- CLIP: qwen3vl_4b_fp8_scaled.safetensors (type krea2)
- VAE: qwen_image_vae.safetensors
- Krea2EditModelPatch (ref_boost=4, ref_boost_a=1, fit_mode=fit) — from `comfyui-krea2edit` node pack (INSTALLED)
- Krea2EditGroundedEncode (instruction + grounding_px=768)
- KSampler: 10 steps, cfg 1, euler/simple (turbo)
- ResolutionSelector: 1:1 1MP (1024×1024) — the 1MP sweet spot

### Key params

- `ref_boost` (fidelity dial) = 4.0 recommended (strong face+body likeness; >10 over-copies, <1 suppresses the ref)
- `grounding_px` 384-768 (lower if compositions double/split)
- 2nd-image group (person-into-scene) ships BYPASSED — enable by right-clicking the group title → toggle Bypass off

### Usage for Jaisal Cut

1. Load a clean character reference (character sheet or close-up) in the LoadImage node (node 72)
2. Write the instruction in node 84 (e.g. "the same boy running on the stone bridge in heavy rain, square stone handrails, moody overcast")
3. Queue → same face, new scene

### Known issues

- 1 expected warning: node 79 `source_latent_b` edge_type_mismatch (the optional 2nd-image group ships bypassed — harmless).

## krea2_jaisal_refs.json (Krea2 reference-image generator)

Date: 2026-08-28
Status: Built + validated (`valid: true`, 0 errors), ready to run

### Purpose

Generate the Krea2-styled REFERENCE SET for the Jaisal Cut (D021): character sheet (faceless), abstract, bridge, medium, close-up, water, running. Feed 2-3 of these to MiniMax H3 R2V so it holds the angular brush-stroke style across the WHOLE video (not just the first 2-3s).

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_refs.json

### Models (locked Krea2 chain)

- UNET: krea2_turbo_fp8_scaled.safetensors
- LoRA: Krea2_Cinematic_Artstyle.safetensors @ 1.0
- CLIP: qwen3vl_4b_fp8_scaled.safetensors (type krea2)
- VAE: qwen_image_vae.safetensors

### Params

- KSampler: 8 steps, cfg 1.0, euler/simple, denoise 1.0 (t2i)
- 2048×1152 (2K 16:9)
- Save prefix: jaisal_cut/refs
- Default positive prompt = faceless character sheet (front/side/back turnaround)

### Character (D022)

Normal young schoolboy with short dark hair (face OK — Krea2 can't do faceless). Costume: rose-pink collared shirt, full-length black trousers, black school bag. ALWAYS "ONLY ONE character, no duplicates". Bridge prompt pins the boy ON THE BRIDGE DECK (left side), NOT in the water.

### Prompts

`d:\models\vsCodeMcp\prompts\jaisal_ref_prompts.txt` — 7 ready-to-paste prompts (character sheet, abstract, bridge, medium, close-up, water, running) + shared negative + how-to-use.

### Next improvement

- Run each prompt, save as refs_*.png, stage the best 2-3 into input\, feed to MiniMax R2V.
- Update the MiniMax prompt (v2) to "black school bag" + faceless when re-running.

## jaisal_single_shot.json (MiniMax H3 i2v single-shot, 1 image)

Date: 2026-08-28
Status: Built + validated (`valid: true`, 0 errors), NOT yet run

### Purpose

PIVOT from the 5-image R2V (which came out bad — style drift, no running, no intro). ONE continuous shot from `1.png` (wide base): boy walks the bridge → sky darkens, wind, rain → boy runs → boy jumps into the river midway → camera dips underwater with bubbles (title composited in post over the bubbles).

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json

### Built from

`video_minimax_h3_i2v` template (Image to Video). Built via `build_single_shot.py` + `fix_single_shot.py` + inline subgraph LoRA fix.

### Models

- UNET: minimax_h3_fl2va_pruned_int8_convrot.safetensors (first/last-frame)
- LoRA: minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors (turbo 4-step, strength 1.0) — on INTERNAL subgraph node 121
- CLIP: qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (type minimax)
- VAE: minimax_h3_video_vae_fp16.safetensors + minimax_h3_audio_vae_fp32.safetensors

### Key custom nodes

- MiniMaxH3ImageToVideo (SUBGRAPH, type UUID `4c314f31-ecda-4b08-ae98-faaba1bf613f`, instance id=105) — first_frame = 1.png, last_frame = none
- ResolutionSelector: 16:9 (Widescreen), 0.98MP → 1344×768
- Save prefix: video/Jaisal_SingleShot

### Prompt

Simple single-shot (NOT the 500-word R2V structure): opens exactly on `<Picture 1>` (boy at start of bridge) → walks → sky darkens/wind/rain → runs → jumps into river midway → camera dips underwater with bubbles. Title composited in post (NOT rendered). Audio: wind building, rain, splash, muffled underwater.

### Gotchas

- The i2v template's main node is a SUBGRAPH — widget values (prompt, duration, turbo, LoRA) must be set on the INTERNAL nodes (`definitions.subgraphs[0].nodes`), not just the instance. LoRA on internal node 121.
- Template default LoRA (`fl2v_turbo_8step`) not installed → swapped to 4-step 768p.
- `ResolutionSelector` aspect enum is `16:9 (Widescreen)` (template's `Widescreeen` spelling fails validation).
- Instance node's `widgets_values_named` dict is preferred over `widgets_values` by the converter — update both.

### Next improvement

- Run, review in ComfyUI. If the jump-to-river is too much for one shot, split into two i2v runs (walk→run→jump, then underwater) and stitch in post, or drop the jump and end on the run.
