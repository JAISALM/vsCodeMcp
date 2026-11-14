# Pose Gallery — the motion library for H3 pose control

> Purpose: ONE recheck sheet for everything related to posing our characters.
> The decision it implements: **D — 2026-11-12: "H3 pose control = POSE REFERENCE IMAGES, not skeleton input"** (H3 has no native pose/skeleton socket).

## The core rule (11-12, confirmed by user)

H3 (FL2VA/ref2va) takes **images**, not skeletons. So the "stick animation → video" pattern becomes a 3-stage chain:

```
① SKELETON/POSE  →  ② POSE-CONTROL IMAGE  →  ③ IDENTITY ONTO POSE  →  H3 POSE REFERENCE
   (pose gallery)      (pose-control gen)        (identity-edit)          (action-pose slot,
                                                                                   explicit motion job)
```

- **Pose images = reusable motion assets** — the pose gallery IS the motion library.
- **Sustained specific pose** (e.g. hands-on-hips): prompt-only is unreliable → **2-anchor pattern**: first-frame anchor (start pose) + one pose image (target pose) + explicit "shifts into the exact pose in \<Picture 2> and holds it" (D020 2-anchor rule).
- In `minimax_h3_sam_r2v_2char_cinematic` the **4th image = `action_pose_variation_*.png`** (body position) and the **5th = `facial_angle_variation_*.png`** (head direction) — FL2VA composes frame 0 from the refs, so these two slots are where the pose gallery feeds in.

## The tooling (what we have, per stage)

### Stage ① — pose creation/editing (skeleton level)

| Tool | Location | Status | Role |
|---|---|---|---|
| **OpenPose Studio** (`andreszs/comfyui-openpose-studio`) | `E:\comfyUi_latest\...\custom_nodes\ComfyUI-OpenPose-Studio-main` | **INSTALLED + VERIFIED 11-14** (tarball route; `__init__.py` 378 lines intact, truncated locale PNG refetched from raw) — needs ComfyUI restart | THE pose gallery engine: visual keypoint editing (Blender-style canvas), preset/collection browsing with thumbnails, pose merger, standard OpenPose JSON import/export, hand editing (20 keypoints per hand), background-reference overlay, render toggles (body/hands/face). `poses/` folder inside the pack = auto-discovered gallery (incl. subdirs, partial poses) — **also registered as ComfyUI settings model folder `openpose_poses` (point the gallery at any folder via Settings)**, REST endpoints `/openpose/poses` + `/openpose/poses/{file}` power the gallery tab; no requirements.txt (no extra pip deps). |
| **DWPose Estimator** (`dwposedeluxe` pack) | custom_nodes ✓ installed | ✓ live | **Pose EXTRACTION from any image** → its `pose_keypoint` output plugs directly into OpenPose Studio's `pose_keypoint` input (upstream-detected pose loads into the editor). This is the gallery FILLING route: any still (our Krea2/H3 output, any reference photo) → extract skeleton → save to gallery. |
| **Shot Composer** (open-media, `D:\models\open-media`) | browser 3D (npm run dev) | ✓ installed 09-11 | 3D mannequin posing (joint gizmos, pose library) → **export PNG of a posed frame** (→ stage ②) or **export MP4 of motion** (→ H3 i2v motion reference). |
| **sam_3d_body_dinov3_bf16** | `E:\ComfyUI_windows_portable\ComfyUI\models\checkpoints\` | ✓ on disk | 3D body model for the pose pipeline (test queue item). |
| **VNCCS PoseStudio** (`AHEKOT/ComfyUI_VNCCS_Utils` v0.7.0 + 3 QI2.1 LoRAs, `loras\QI2.1\VNCCS\`) | ✓ all local, verified 10-25 | ✓ reference workflow `VNCCS_PoseStudio_QI2.1_REFERENCE.json` (0/0) | **Stage ②**: pose render (from the interactive 3D node) + character image → character rendered IN that pose on QI2.1. **WIRING (audited 11-14):** `image_1` = pose render from the interactive `VNCCS_PoseStudio` node (id488) · `image_2` = LoadImage character image (author's `DancersBunny.png` — SWAP for our face ref) · author prompt: "replace the pose of \<image 2> with the pose of \<image 1>. keep the character of \<image 2>" · LoRA `QI2.1\VNCCS\VNCCS_QI2_PoseStudioV1` @1.0 · UNET `qwen_image_2.1_int8_convrot` · CLIP `qwen3vl_8b_int8_convrot`. **FACE-DRIFT FIX (11-14, user run = bad face consistency):** ① the text node's `prompt` INPUT is wired to the pose node's `lighting_prompt` (link 791) — a connected link overrides the widget → unplug it and own the prompt in the widget ② add an IDENTITY ANCHOR (the author's one-liner has none — their consistent demos = same single character ref repeated, not the prompt): pose instruction + "same face as \<image 2>: 26yo Indian man, wavy black hair, plain black t-shirt" (or Zidhan line) ③ `image_2` = clean SINGLE FRONTAL face ref (`jaisal_face_frontal.png` / `zidane_face_frontal.png`) — NOT the 3-panel sheet, NOT a ¾ view ④ leave LoRA@1.0 + int8 stack (not the face-drift cause). |
| **Civitai 3045966** — "H3 Image w/ Pose Studio + Other Advanced Features [FoxFurEssence]" (r/comfyui u/foxdit) | API download was auth-walled 11-11 | ⚠ **USER: open civitai.com/models/3045966 in browser → click download → drop the JSON into the workflows dir** | All-in-one H3-Image + Pose Studio workflow (adopt candidate). |

### Stage ② — pose → character-in-pose image

1. **VNCCS PoseStudio** (above) — pose image + character sheet → posed character (QI2.1 stack, all local).
2. **H3-Image edit** (native v0.45.2) / **Krea2 identity-edit** (ref_boost 4.0) — re-render an existing character image in a new pose.
3. **Shot Composer PNG export** — mannequin pose frame (generic, no face — feed into stage ③).

### Stage ③ — identity onto the pose

- **`krea2_identity_edit.json`** (Krea2 Identity Edit v1.2, ref_boost 4.0) — face/identity from our locked refs (`krea2_char{1,2}_face_*`, v3 sheets) onto the posed image.

### Stage ④ — into H3

- Feed the finished pose reference into the **action-pose slot** of the R2V/FL2VA workflow with an **explicit motion job** (D017 R2V style: `<Picture N>` tag + job = "motion/pose reference"; 6-section prompt; 2-anchor pattern for sustained poses).

## The gallery FILLING flow (OpenPose Studio, post-restart)

1. **Extract**: `DWPose Estimator` (dwposedeluxe) on any source image → `pose_keypoint` → **OpenPose Studio** node (loads detected pose into the editor).
2. **Refine**: click the node's preview canvas → drag keypoints (COCO-18 body + individual hands; face = pass-through) → **Apply** (Enter). Undo = Ctrl+Z.
3. **Save to gallery**: export standard OpenPose JSON → drop into the pack's `poses/` folder (subdirs = collections; the preset tab auto-discovers with live thumbnails — Large/Medium/Small density modes).
4. **Use**: pick from the gallery → **render** (RGB output, 0-1 float) → straight into an H3 ref slot (or save as PNG → stage ②/③ if a character-in-pose image is needed instead of a stick figure).
5. **Merge**: pose merger node combines multiple JSONs into organized collections.

## OpenPose Studio — format facts (from the repo, 11-14)

- **COCO-18 body layout**: `pose_keypoints_2d` flat array `[x0,y0,c0, x1,y1,c1, …]` (18×3), pixel coords, confidence 0..1 (0 = missing). Order: 0 nose, 1 neck, 2-4 right arm, 5-7 left arm, 8-10 right leg, 11-13 left leg, 14-17 eyes/ears.
- **JSON shape**: `{"canvas_width": W, "canvas_height": H, "people": [{"pose_keypoints_2d": [...]}]}` — partial poses OK (missing = 0,0,0); legacy non-standard JSON loads correctly.
- **Node I/O**: input `Pose JSON` (STRING) + optional `areas` (CONDITIONING_AREAS, from ComfyUI-LoRA-Pipeline) + optional `pose_keypoint` (POSE_KEYPOINT — DWPose output). Outputs: **rendered IMAGE** (RGB float32 0-1) · **JSON** (OpenPose-style, canvas dims + people) · **KPS** (POSE_KEYPOINT, ControlNet-compatible).
- **Shortcuts**: Enter = apply · Esc = discard · Ctrl+Z/Y = undo/redo · Delete = remove keypoint · click = select · drag = move.
- **Render toggles**: body / hands / face (independently) · **background reference overlay** (contain/cover + opacity — load a reference image as a non-destructive editing overlay; persists per session, not saved in workflows).
- **Install**: ComfyUI Manager → "openpose-studio" or `git clone` (done 11-14) → **restart ComfyUI** (bundled with the Viggle-Remake restart).
- **Limitations**: face keypoints = pass-through only (not individually editable); scroll-zoom = TODO; background refs not saved in workflows.

## Pending / next

- [ ] **ComfyUI restart** (loads OpenPose Studio + the Viggle-Remake pack — bundle both into one restart).
- [ ] **Fill the gallery**: extract 10-20 base poses (DWPose on existing stills/references) → cull → the first motion library.
- [ ] **Civitai 3045966** browser download (user click, 11-11) — all-in-one H3-Image+Pose-Studio workflow.
- [ ] **Decision (user):** for the 2char action-pose slot — stick-figure render vs character-in-pose image (VNCCS/identity-edit) — A/B on the next test run.
