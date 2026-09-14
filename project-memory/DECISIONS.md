# Project Decisions

## D001 — Use ComfyUI MCP for workflow interaction

Date: 2026-08-26
Status: Active

### Decision

Use ComfyUI MCP as the primary interface for inspecting, creating, modifying, and executing ComfyUI workflows.

### Reason

MCP can interact with the actual ComfyUI environment and saved workflows instead of relying on the model's knowledge of ComfyUI.

### Alternatives

Manual workflow editing and manually describing nodes to the model.

### Result

ComfyUI MCP is successfully generating and modifying workflows.

---

## D002 — Use local Qwen as the reasoning model

Date: 2026-08-26
Status: Active

### Decision

Use the local Qwen model through llama.cpp rather than relying on Claude/Codex for ComfyUI reasoning.

### Reason

Local inference provides control over the model, context, performance, and cost.

### Result

Qwen is successfully interacting with ComfyUI through MCP.

---

## D003 — Preserve project knowledge in Markdown

Date: 2026-08-26
Status: Active

### Decision

Use Markdown files under `project-memory/` as persistent project state.

### Reason

The AI chat context is temporary. Important project decisions must survive model/session changes.

### Result

Project state, decisions, experiments, and workflow history are stored separately from chat history.

---

## D004 — "The Jaisal Cut" title is composited in post, not rendered

Date: 2026-08-26
Status: Active

### Decision

Do NOT render the "The Jaisal Cut" title text with the diffusion model. Generate the title frame as the scene (kid looking up, sky clearing) without text, then composite the title + the J-dot effect (kid becomes the dot in the J) in post (After Effects / DaVinci Resolve).

### Reason

Diffusion is unreliable at spelling text correctly. The J-dot is a 2-second post effect, not a generation problem. This is the single biggest quality win.

### Alternatives considered

- In-image text rendering (rejected — unreliable spelling)

### Result

Title frame generated text-free; title + J-dot added in post.

---

## D005 — Locked Krea2 style chain for all Jaisal Cut frames

Date: 2026-08-26
Status: Active

### Decision

Every Jaisal Cut frame uses the same chain: `krea2_turbo_fp8_scaled.safetensors` + `Krea2_Cinematic_Artstyle.safetensors` LoRA (strength 1.0) + `qwen3vl_4b_fp8_scaled.safetensors` CLIP (type krea2) + `qwen_image_vae.safetensors`, with the style prefix "An angular, 3d art style, with brush stroke color texture." on every prompt. 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 0.7 for i2i.

### Reason

Consistent style = MiniMax blends the 9 frames smoothly into the 15s video. Identity is locked by i2i from the face anchor.

### Alternatives considered

- Per-frame style variation (rejected — breaks MiniMax blending)

### Result

All frames share one style; identity locked via i2i anchors.

---

## D006 — Medium shot is i2i from the face anchor

Date: 2026-08-26
Status: Active

### Decision

The medium shot (head + upper body on the bridge) is generated i2i from the face anchor (jaisal_face_v4_A.png), not t2i, to lock the kid's identity while widening the framing.

### Reason

t2i would risk a different face; i2i from the face keeps identity consistent across the wide / medium / close-up framings.

### Alternatives considered

- t2i medium shot (rejected — identity drift)

### Result

krea2_jaisal_medium.json generates the medium anchor with locked identity.

---

## D007 — Single character only, no duplicates

Date: 2026-08-26
Status: Active

### Decision

Every frame must show exactly ONE kid. No duplicate characters, no second kid. Added "duplicate character, 2 kids, duplicated kids, two kids, second kid" to the shared negative prompt, and "a single young Indian schoolboy, one kid only" to the wide-shot prompts.

### Reason

storysheet_01 rendered two characters (start and end of the bridge). The story is about one kid.

### Result

Single-character constraint enforced on all frames.

---

## D008 — Consistent costume: red school bag, no tie

Date: 2026-08-26
Status: Active

### Decision

The kid's red school bag must stay RED across all frames (it turned blue in the close-up). The kid wears NO tie (a tie appeared in the gust frame that wasn't in the others). Added "red school bag" to close-up prompts and "tie, necktie, blue bag, blue school bag" to the negative.

### Reason

Costume consistency is critical for MiniMax to blend the frames smoothly. A color change or added accessory breaks continuity.

### Result

Red bag + no tie enforced on all frames.

---

## D009 — Close-up frames keep the moody atmosphere

Date: 2026-08-26
Status: Active

### Decision

The close-up frames (4, 5, 6) keep the same moody overcast atmosphere. Beat 6 (rain clearing) is NOT a sunny/cleared sky — the rain has just stopped for a moment, the sky is still dark and moody. The rain effect from the generated frames is preserved by i2i from the current frames (jaisal_ss04/05/06.png).

### Reason

The emotional core is the rain coming and going in a moody setting. A sudden sunny sky breaks the mood. The rain effect in the generated frames is good and should be kept.

### Result

Moody atmosphere + preserved rain effect on close-up frames.

---

## D010 — The "cut" section camera is above the kid, zooming out

Date: 2026-08-26
Status: Active

### Decision

The "cut" section (beats 7, 8, 9) uses a HIGH-ANGLE camera above the kid (looking down, seeing the bridge + water body underneath), the kid looking up at the sky, and the camera panning + zooming out. Beat 8 CONTINUES the zoom-out (does NOT revert to the initial river-level camera). Beat 9 is the final wide shot of the whole river bridge (kid = the dot in the J), no text. Beats 7→8→9 are chained (each i2i from the previous) for a smooth zoom-out.

### Reason

The initial river-level camera (beats 1-2) is a different shot. The "cut" is a new camera angle (above the kid) that pans and zooms out to reveal the whole bridge for the title. Reverting to the river camera broke the flow.

### Result

Smooth high-angle zoom-out for the cut section, ending on the whole bridge for the title.

---

## D011 — Visual continuity is the top priority; fix by i2i from the good frame

Date: 2026-08-26
Status: Active

### Decision

When fixing a continuity problem between shots, do NOT independently redesign the scene. i2i from the frame that already has the correct look (identity, clothing, bag, environment, lighting, composition) and change only the specific problem. Use low denoise (0.5) for single-element fixes (tie removal, strap fix) and ~0.6-0.7 for camera/framing changes. For a continuous camera movement (the 07→08→09 aerial ascent), CHAIN the frames (each i2i from the previous) so the sequence reads as one drone shot.

### Reason

Independently regenerating shots breaks character/costume/environment continuity, which breaks MiniMax's ability to blend the frames into a coherent video. The rain effect in the close-ups is good and must be preserved — so close-up fixes i2i from the current close-up frames, not from the face anchor.

### Alternatives considered

- Regenerate from the face/base anchor (rejected — loses the environment/rain continuity)
- High denoise re-rolls (rejected — risks identity/environment drift)

### Result

Continuity fixes applied via targeted i2i: 03 from 04's environment, 05 tie removal (denoise 0.5), 06 both straps (denoise 0.5), 07→08→09 chained aerial ascent.

---

## D012 — Use inpainting for single-element removal that i2i can't fix

Date: 2026-08-26
Status: Active

### Decision

When a low-denoise i2i fails to remove a high-contrast element (e.g. a tie — the model preserves it because it's a strong detail), use INPAINTING: mask just the region to change (collar/tie), and regenerate ONLY that region with denoise 1.0 while the rest of the image stays locked. Workflow: LoadImage (frame) → VAEEncode → SetLatentNoiseMask (mask) → KSampler (denoise 1.0) → VAEDecode. The mask is a grayscale image (white = regenerate) loaded via LoadImage → ImageToMask → GrowMask (expand ~20px, tapered_corners false).

### Reason

A full-image i2i at low denoise keeps the tie because the model preserves high-contrast details. Inpainting isolates the change to the masked region, so the face, bag, environment, and composition are untouched — only the collar/tie area is regenerated.

### Alternatives considered

- Higher-denoise full i2i (rejected — risks identity/environment drift)
- Prompt-only negative (rejected — tie persisted)

### Result

krea2_jaisal_fix05_inpaint.json removes the tie from beat 05 via a collar-region mask. Mask file: jaisal_ss05_tie_mask.png (ellipse over the collar/tie region). NOTE: Krea2 is NOT an inpaint model — the Krea2 inpaint came out distorted. Use the Flux one-node for real inpainting.

---

## D013 — Use the Flux one-node (FluxKleinOneNode) for real inpainting

Date: 2026-08-26
Status: Resolved (manual UI run)

### Decision

For single-element removal that Krea2 can't handle (Krea2 is not an inpaint model — its inpaint output is distorted), use the **Flux one-node** (`FluxKleinOneNode`, "One Node · FLUX.2 [klein]") in PAINT/Inpaint mode.

### Blocker

The one-node is a FRONTEND-DRIVEN UI widget: its `noop` function just returns the JS preview image; generation is triggered from the ComfyUI UI (via `POST /flux_klein/set_output`), NOT through the standard prompt queue — so it CANNOT be driven via `run_workflow`/MCP. It also needs **FLUX.2 [klein] models** (a diffusion model + matching text encoder + VAE) that are NOT installed (local model dirs are empty). The ComfyUI-Inpaint-CropAndStitch dependency IS present.

### Resolution options

- (a) Install FLUX.2 [klein] models (diffusion + text encoder + VAE) into the local model dirs, then drive the one-node from the ComfyUI UI (PAINT → Inpaint: paint the tie region, describe "open collar, no tie").
- (b) User runs the one-node manually in the ComfyUI UI.

### Result

RESOLVED — the user ran the one-node manually in the ComfyUI UI (PAINT/Inpaint) and the tie was removed successfully. Beat 05 is done. The one-node works when driven from the UI; the MCP/prompt-queue path is not available for it.


---

## D014 - MiniMax H3 speed stack: Star7 + Comfy Kitchen INT8 + turbo 4-step LoRA

Date: 2026-08-27
Status: Active

### Decision

For fast MiniMax H3 video on the RTX 5090, use:
- **Star7 pack** (minimax-h3-chunk-star7) node MiniMaxH3ActivationChunkStar7 with attention_backend=comfy_kitchen_int8 (Comfy Kitchen INT8 attention + QKV/RoPE/MLP activation chunking).
- **Turbo 4-step LoRA** minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors (strength 1.0) with BasicScheduler simple/8/1.
- **fl2va model** for first-last-frame shots (drone ascent).
- **RTXVideoSuperResolution** (2x ULTRA) for 2K output; measure at 0.4MP (864x480) first.

### Reason

- triton is MISSING in the embedded Python -> KJNodes PathchSageAttentionKJ crashes (sage path is dead). comfy_kitchen IS installed, so CK INT8 is the working fast attention backend.
- Turbo 4-step halves the sampling steps vs 8-step.
- fl2va natively interpolates between a start and end frame - ideal for the drone-ascent shot.
- 0.4MP keeps the test fast; RTX VSR 2x brings it to ~2K.

### Alternatives considered

- KJNodes SageAttention (needs triton - unavailable).
- Spectrum SpectrumApplyMiniMaxH3 (spectral step-forecasting - installed, but Star7 CK INT8 is the simpler proven fast path; Spectrum kept as fallback).
- H3-Multishot H3MultishotMemorySampler (Joey Gambino long-form sampler - used by v11/v13 seamless templates; good for multi-shot, but single-shot drone ascent is simpler with core MiniMaxH3ReferenceToVideo + fl2va).

### Result

jaisal_drone_optimized.json built and validated (not yet run). All 5 models present in main path.

---

## D015 - Machine-built workflows must use NATIVE widget shape (not /object_info order)

Date: 2026-08-27
Status: Active

### Decision

When building or converting ComfyUI workflow JSON, `widgets_values` arrays MUST match the **native UI-saved shape**, NOT the API `/object_info` widget order. Specifically:
- **KSampler = 7 values** `[seed, control_after_generate, steps, cfg, sampler_name, scheduler, denoise]` — the hidden `control_after_generate` widget (randomize/fix/+1/-1 dropdown next to seed) is NOT in `/object_info`.
- **LoadImage = 2 values** `[filename, "image"]` — the 2nd literal `"image"` is NOT in `/object_info`.
- **No `widgets_values_named` key** — native UI-saved files don't have it; its presence marks a machine-built file.

### Reason

`/object_info` lists only the "required" widget inputs, which OMITS hidden widgets the UI actually renders. Building `widgets_values` from that order makes the array too short, so the server maps values positionally and they shift one slot left: KSampler `cfg` gets `'euler'`, `sampler_name` gets `'simple'`, `scheduler` gets `0.4` → prompt validation fails ("could not convert string to float", "Value not in list"); LoadImage image not shown; UI shows "no details". This affected ALL 21 machine-built workflows (the 08-27 converted batch + jaisal_drone_optimized).

### Alternatives considered

- Building from `/object_info` order (the original bug — rejected).
- Adding `widgets_values_named` to disambiguate (rejected — native files don't use it; the UI ignores it and it's a machine-built marker).

### Result

`fix_all_widget_shapes.py` applied the native shape to all 21 machine-built workflows (435 changes; backups in `d:\models\vsCodeMcp\workflow_backups\pre_widget_fix\`). All 21 re-validated via MCP (`valid: true`, 0 errors). **Rule for all future workflow building: copy `widgets_values` shapes from a native UI-saved workflow, never from `/object_info`.** See AGENTS.md "CRITICAL: widgets_values must match the server's widget order EXACTLY".

---

## D016 - Machine-built workflows must use `type='COMBO'` + LoadImage `upload` input (not static lists)

Date: 2026-08-27
Status: Active

### Decision

When building/converting workflow JSON, widget-input `type` fields for combo widgets (KSampler `sampler_name`/`scheduler`, LoadImage `image`, CLIPLoader `clip_name`/`type`/`device`, UNETLoader `unet_name`/`weight_dtype`, VAELoader `vae_name`, LoraLoaderModelOnly `lora_name`) MUST be the string `'COMBO'`, NOT a static list of values. And every LoadImage node MUST include the `upload` input (`type='IMAGEUPLOAD'`, `localized_name='choose file to upload'`).

### Reason

A static list dumped into `type` is a stale snapshot — the UI shows it but it doesn't refresh, and (critically) the converter DROPPED the `upload` input, so the LoadImage node had no "choose file to upload" button and no live dropdown. The node still held the correct filename in `widgets_values` (so it "picked up the correct image"), but the user couldn't select/preview a different image in the UI. `type='COMBO'` tells the frontend to populate the dropdown from the server live; the `upload` input renders the file-picker.

### Alternatives considered

- Keeping the static list (rejected — stale, no upload button).
- Only fixing LoadImage (rejected — the same static-list problem affected KSampler/CLIPLoader/UNETLoader/VAELoader/LoraLoaderModelOnly combo inputs too; fixed all in one pass).

### Result

`fix_combo_inputs.py` set 253 static-list inputs to `'COMBO'` and added 37 `upload` inputs across all 21 machine-built workflows (backups in `d:\models\vsCodeMcp\workflow_backups\pre_combo_fix\`). All re-validated via MCP (`valid: true`, 0 errors). **Rule: combo widget inputs use `type='COMBO'`; LoadImage always has both `image` (COMBO) and `upload` (IMAGEUPLOAD) inputs.** See AGENTS.md.

## D017 - MiniMax H3 R2V prompts use the official 6-section reference style

Date: 2026-08-27
Status: Active

### Decision

All MiniMax H3 reference-to-video (R2V) prompts MUST follow the official MiniMax H3 R2V prompting style: reference each input by a tag in **connection order** (`<Picture 1>` = `ref_image_0`, `<Picture 2>` = `ref_image_1`, …), assign each reference an explicit **job** (identity / style / motion / camera / frame anchor), and structure the prompt into the **6 sections** in order: `subject_definitions`, `summary` (with a `[task-type]` prefix like `[reference generation]`), `retention_analysis` (one line per label + a relationship marker), `detailed_description` (350-500 words, partitioned into `[Shot 1]`…`[Shot N] At MM:SS.mmm` with camera angles + actions), `overall_soundscape`, `non_diegetic_music`.

### Reason

The MiniMax H3 R2V model is trained on prompts in this exact structure. Using `<Picture N>` tags in connection order tells the model precisely which reference provides what (identity vs. frame anchor vs. style). Partitioning into timed `[Shot N]` blocks with camera angles gives the model a clear storyboard. A free-form prompt (the old style) under-uses the references and produces weaker shot control. The official guide is saved at `d:\models\vsCodeMcp\docs\MINIMAX_H3_R2V_PROMPTING_GUIDE.md` for reuse.

### Alternatives considered

- Free-form prose prompt (rejected — under-uses references, weak shot control).
- Only `<Subject N>` labels without `<Picture N>` frame anchors (rejected — loses the per-shot frame anchoring that R2V is built for).

### Result

`jaisal_lowangle.json` prompt rewritten to this style (5 `<Picture N>` frame anchors, `<Subject 1>` boy / `<Subject 2>` bridge, 5 timed shots, title composited in post). Validated `valid: true`. **Rule: every R2V prompt uses `<Picture N>`/`<Subject N>` tags in connection order + the 6-section structure + timed `[Shot N]` blocks.** See `MINIMAX_H3_R2V_PROMPTING_GUIDE.md`.

## D018 - Multi-ref workflow wiring: set the input `link` field by SLOT INDEX, not name number

Date: 2026-08-27
Status: Active

### Decision

When building a workflow with multiple reference inputs (e.g. `MiniMaxH3ReferenceToVideo` `ref_image_0`…`ref_image_8`), the `link` field on each input in the node's `inputs` array MUST be set to the link ID **by the input's array slot index**, NOT by the number in the input's name. The link's `to_slot` equals the input's position in the `inputs` array, which can differ from the number embedded in the input name.

### Reason

In `jaisal_lowangle.json`, the template had links 289 (LA4→136.6) and 290 (LA5→136.7) but the `MiniMaxH3ReferenceToVideo` node's `inputs` array had `link=None` on `ref_image_3` (slot 6) and `ref_image_4` (slot 7). The UI showed only 3 images wired and validation reported `node_not_reachable_from_output` for LA4/LA5. The bug: the input *name* number (`ref_image_3`→3) differs from the input *slot* position (index 6/7). Setting `link` by name number looked for a link targeting slot 3/4 (which don't exist for these inputs); setting it by actual array index (6/7) matched the real links.

### Alternatives considered

- Setting `link` by the name number (rejected — wrong slot, no match).
- Only creating the link without setting the input `link` field (rejected — UI shows no connection, validation flags unreachable).

### Result

`fix_lowangle_wiring_and_prompt.py` set `ref_image_3.link=289` and `ref_image_4.link=290` by slot index. All 5 images now wired; validation `valid: true`, 0 warnings. **Rule: when wiring multi-ref inputs, set each input's `link` field to the link ID whose `to_slot` equals that input's array index.**

## D019 - Subgraph templates: set widget values on INTERNAL nodes, not the instance

Date: 2026-08-28
Status: Active

### Decision

When a gallery template wraps its main node in a **subgraph** (the instance node's `type` is a UUID, e.g. `4c314f31-ecda-4b08-ae98-faaba1bf613f`), widget values (prompt, duration, turbo, LoRA, etc.) MUST be set on the **internal nodes** under `definitions.subgraphs[0].nodes`, NOT on the instance node's `widgets_values`. The instance node's `widgets_values_named` dict is also preferred over `widgets_values` by the UI→API converter, so update both.

### Reason

The `video_minimax_h3_i2v` template's `MiniMaxH3ImageToVideo` node (instance id=105) is a subgraph. Editing the instance's `widgets_values[10]` (LoRA) had NO effect — the converter read the LoRA from the internal `LoraLoaderModelOnly` node (id=121), which still held the template default `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` (not installed) → validation error `node 105/121: lora_name not in options`. The `105/121` notation = instance 105, internal node 121. Setting `lora_name` on internal node 121 (both `widgets_values[0]` and `widgets_values_named['lora_name']`) to the installed `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors` fixed it.

### Alternatives considered

- Editing only the instance `widgets_values` (rejected — ignored by the converter for subgraph nodes).
- Downloading the 8-step LoRA (rejected — we already have the 4-step 768p version, which is faster and proven on the drone workflow).

### Result

`jaisal_single_shot.json` validates `valid: true`, 0 errors. **Rule: for subgraph templates, locate the internal node and set its `widgets_values` + `widgets_values_named`; also update the instance's `widgets_values_named`.** Related: the `ResolutionSelector` aspect enum is `16:9 (Widescreen)` (the template's own `Widescreeen` spelling fails validation). See AGENTS.md.

## D020 - R2V: use 2-3 reference images max with a SIMPLE prompt (not 5 + 500 words)

Date: 2026-08-28
Status: Active

### Decision

For MiniMax H3 reference-to-video, use **2-3 reference images max**, each mapped 1-to-1 to a shot with an explicit "the first frame of [Shot N]" anchor, and a **short** prompt. Do NOT use 5 images + a 500-word 6-section essay.

### Reason

The 5-image `jaisal_lowangle.json` (5 `<Picture N>` tags + 500-word prompt) came out bad: style drift, the boy not running, and the model confused by the ref→shot mapping (it couldn't cleanly map `ref_image_0`→`<Picture 1>`→[Shot 1] across 5 anchors). The single-shot i2v alternative also came out bad (cartoon style, weak motion). The fix: **2 images** (`1.png` = boy at start of bridge → [Shot 1], `2.png` = boy in middle of bridge → [Shot 2]) with a simple prompt where each `<Picture N>` is explicitly "the first frame of [Shot N]". The model animates between 2 clear anchors far better than it follows a 5-anchor storyboard.

### Alternatives considered

- 5-image R2V (rejected — style drift, no running, confused mapping).
- Single-shot i2v (rejected — cartoon style, weak motion).
- 3-image R2V (fallback — add a 3rd reference showing the running pose if 2 images don't produce the run).

### Result

`jaisal_lowangle.json` rebuilt as 2-image via `build_2ref.py` (deleted LoadImage 143/LA4/LA5 + links 285/289/290, cleared `ref_image_2/3/4` link fields, simple 2-anchor prompt, save prefix `video/Jaisal_2Ref_1_2`). Validated `valid: true`, 0 errors. **Rule: 2-3 refs max, each an explicit frame anchor, simple prompt. If the character isn't doing the action, add a 3rd reference showing that pose or strengthen the motion verb.** See AGENTS.md.

## D021 - Hold the Krea2 style in MiniMax video via a Krea2-styled REFERENCE SET (not frame-by-frame)

Date: 2026-08-28
Status: Active

### Decision

To keep the Krea2 angular brush-stroke style across a WHOLE MiniMax H3 video (not just the first 2-3s), **generate a set of Krea2-styled reference images first** (character sheet, abstract, bridge, medium, close-up, water, running — all faceless character, rose shirt/black pant/black bag) and feed 2-3 of them as references to the MiniMax R2V workflow. Do NOT use a frame-by-frame Krea2 style-transfer pipeline (extra work).

### Reason

MiniMax H3 is a general video model — its prior smooths toward its own default look, so the Krea2 style "completely went" in the video. The turbo LoRA is a *speed* distillation, not a *style* LoRA. Reference images only anchor the first frame, so drift creeps in over 15s. A frame-by-frame Krea2 i2i pipeline would guarantee the style but is extra work (extract frames → batch i2i → reassemble). The cleaner path: create a proper Krea2-styled reference set upfront and feed it to MiniMax so it holds the style across the whole video.

### Alternatives considered

- Frame-by-frame Krea2 style transfer (rejected — extra work; user: "creating a video and snapping is extra work, let's create the images properly").
- Stronger style description in the prompt only (insufficient — text can't fully carry the style).
- Training a MiniMax H3 style LoRA (best long-term, but heavy — needs training infra; keep as a future option).

### Result

`krea2_jaisal_refs.json` (Krea2 t2i generator, validated) + `jaisal_ref_prompts.txt` (7 faceless-character prompts). **Rule: for style-consistent video, build a Krea2-styled reference set first and feed 2-3 of it to MiniMax.** See AGENTS.md.

## D022 - The Jaisal Cut character is FACELESS (head + hair only) with rose shirt / black pant / black bag

Date: 2026-08-28
Status: Active

### Decision

The Jaisal Cut character is a **normal young schoolboy with short dark hair** (face OK — see correction below). Costume: **rose-pink collared shirt, full-length black trousers, black school bag** (replacing the old red bag / school-uniform look). Every prompt must emphasize **ONLY ONE character, no duplicates** (Krea2 tends to duplicate the character).

### Reason

The user originally requested a faceless figure ("a head and hair, no nose, no face, no eyebrow, no mouth") because faces are the hardest thing to keep consistent in video. **Correction (2026-08-28): Krea2 CANNOT make a faceless character — it always renders a face.** The user accepted this: "krea 2 doesnt create faceless, but thats fine we are good with 1 character sheet." So the character is a normal boy with short dark hair + the new costume.

### Alternatives considered

- Faceless figure (rejected — Krea2 can't do it; it always renders a face).
- Keeping the red bag / school uniform (rejected — user changed the costume to rose shirt / black pant / black bag).

### Result

All reference images (`jaisal_ref_prompts.txt`) use the normal-face boy + new costume + "ONLY ONE character" emphasis. The bridge prompt pins the boy **ON THE BRIDGE DECK (left side), NOT in the water** (Krea2 had put him in the river). The MiniMax prompt (v2) still says "red school bag" — **update it to "black school bag"** when re-running MiniMax with the new references. **Rule: the Jaisal Cut character is a normal boy (short dark hair), rose-pink collared shirt, black trousers, black school bag, always a SINGLE character.**

## D023 - Face consistency via Krea2 Identity Edit v1.2 workflow (not t2i re-rolls)

Date: 2026-08-29
Status: Active

### Decision

To keep the SAME face across all Jaisal Cut reference images, use the **Krea2 Identity Edit v1.2** workflow (`krea2_identity_edit.json`, LoRA `krea2_identity_edit_v1_2.safetensors`, `comfyui-krea2edit` node pack — both already installed). Load a good reference (character sheet / clean close-up) in the LoadImage node, write a plain-English instruction for the new scene, and it regenerates the scene keeping the same face/identity. `ref_boost` = 4.0 (recommended fidelity), KSampler 10 steps cfg 1, `grounding_px` 384-768, 1MP output.

### Reason

Krea2 t2i gives a DIFFERENT face every time the character appears ("literally a different guy" across the reference set). The identity-edit model treats the reference image like a LoRA — much stronger face+body likeness than re-rolling t2i seeds. User found the workflow on reddit; it's the right tool for a production character.

### Alternatives considered

- Re-rolling t2i seeds until the face matches (rejected — unreliable, the face drifts every generation).
- Training a character LoRA (rejected — heavy; identity-edit is ready now).

### Result

`krea2_identity_edit.json` validates `valid: true` (1 expected warning: optional 2nd-image group ships bypassed). **Rule: for consistent-character reference sets, generate the base image with t2i, then lock the face with the identity-edit workflow (ref_boost 4).**

## D024 - Climate consistency: one moody tone once rain starts (no drastic changes)

Date: 2026-08-29
Status: Active

### Decision

Do NOT change the climate dramatically between shots. Once the rain starts, keep ONE moody tone across all rain/water shots (medium, close-up, water, running). The underwater shot must be DARK and moody (matching the rain), NOT bright/sunny.

### Reason

The generated water reference came out bright with a canal/bund look while the rest of the set was moody — a drastic light change between shots breaks continuity, and MiniMax won't bridge a hard climate jump between references.

### Result

Prompts 4-7 in `jaisal_ref_prompts.txt` updated: square handrails (not round/ornate/staircase), open river (not canal/bund), dark moody water (not bright), three-quarter view (not facing camera). **Rule: one moody tone from the first rain onward; no bright/sunny shots after rain starts.**

---

## D025 - Identity workflow: wire the STYLE LoRA in to match skin tone / lighting

Date: 2026-08-29
Status: Active

### Decision

Add the **style LoRA `Krea2_Cinematic_Artstyle.safetensors` @ 0.7** to the Krea2 Identity Edit v1.2 workflow (`krea2_identity_edit.json`) as a new node **95** between the identity LoRA (71) and the `Krea2EditModelPatch` (79). Chain: `55 UNETLoader → 71 identity LoRA → 95 style LoRA → 79 patch → 53 KSampler`.

### Reason

The identity workflow carries the **reference image's color tone** into the output. A neutral/bright character-sheet reference makes the boy come out studio-lit, clashing with the dark moody rainy scene (skin tone mismatch). The style LoRA pulls the output back into the angular brush-stroke style AND the moody palette of the scene.

### Alternatives considered

- Relying on the instruction's lighting words alone (helps but doesn't fully fix the reference's color tone).
- Using a reference that is already in the moody scene (best — then the tone matches automatically).

### Result

Style LoRA wired in + validated `valid: true`. **Tuning:** style too weak → raise node 95 to 0.8-1.0; face distorts → lower to 0.5. **Also:** keep the lighting words in the instruction ("moody overcast light"); if skin still too bright add "skin tone matching the dark moody overcast light, dim diffused light on the face, NOT studio lit". **Best:** use a reference already in the moody scene instead of the neutral character sheet. Backup: `krea2_identity_edit.json.pre_stylelora.bak`.

---

## D026 - Title card "The Jaisal Cut" via Krea2 i2i + Typnosis typography LoRA

Date: 2026-08-30
Status: Active

### Decision

Generate the title card with a dedicated Krea2 **i2i** workflow `krea2_jaisal_title.json`: load the underwater shot (`refs_water.png`), keep the SAME underwater scene, and swap the boy for the title **"The Jaisal Cut"** using the **Typnosis_Krea2** typography LoRA (verified: "Typnosis v2 triggerless Krea 2 Raw typography/domain LoRA") chained after the Cinematic style LoRA. Chain: `UNET krea2_turbo_fp8_scaled → Cinematic LoRA @1.0 → Typnosis LoRA @1.0 → KSampler (8 steps cfg 1, denoise 0.55)`.

### Reason

The underwater shot has generous negative space for a title. An i2i (low-moderate denoise) keeps the scene consistent while the typography LoRA renders the title text. Verified we already have Krea2 i2i workflows (`krea2_jaisal_title_moody.json` etc.), so this reuses the proven i2i pattern.

### Alternatives considered

- Compositing the title in post (Photoshop) — works but the user wanted it generated in ComfyUI with the typography LoRA.
- t2i from scratch — would lose the consistent underwater scene.

### Result

`krea2_jaisal_title.json` built + validated `valid: true`. Prompt (prompt 10 in `jaisal_ref_prompts.txt`) keeps the underwater scene + swaps the boy for the title. **Tuning:** title garbled → lower denoise to 0.4; boy still there → raise denoise to 0.65-0.7.

### Update 2026-08-30 (STR5 + bubble-formed title)

User tested the title card and **STR5 (strength 5.0) on the Typnosis LoRA reads best** for the title (per the Typnosis author notes: STR1-STR2 is most prompt-faithful, STR4+ gets more stylized and compositions converge — STR5 is the balanced-strong sweet spot). Set node 32 `strength_model` = **5.0**. User also asked for **bubbles**: the title is now **formed ENTIRELY from clusters of rising air bubbles** (each letter built from many small/medium bubbles glowing against the dark water) with **additional bubbles drifting around the title** — fits the underwater scene. Prompt 10 positive updated accordingly. **Tuning:** STR5 over-stylizes/distorts letters → drop to 3.0-4.0; bubbles too sparse → strengthen the bubble wording ("DENSE clusters of many small bubbles") or nudge the LoRA up.

### Update 2026-08-30 (wavy floating layout)

User asked for a **wavy type** since the bubbles are in water — the words should **float a little**: not too adjacent (spaced apart with generous gaps), letters can be **different sizes/shapes**, but the whole **"The Jaisal Cut"** must stay clearly readable. Prompt 10 positive now adds: "the letters and words arranged in a gentle WAVY floating layout, each word drifting at a slightly different height as if floating in the water, the words spaced apart with generous gaps between them (NOT cramped, NOT adjacent), the individual letters varying slightly in size and shape for an organic floating feel, the whole title 'The Jaisal Cut' clearly readable and centered". **Tuning:** words too flat/straight → strengthen the wavy wording ("each word drifting at a clearly different height, a gentle S-curve"); words too scattered / title stops reading as one line → soften it ("a SUBTLE gentle wave, words only slightly offset, kept close enough to read as one title").

### Update 2026-08-30 (CPU RAM exhaustion on the 7-ref MiniMax run — CORRECTED diagnosis)

The 7-shot `jaisal_lowangle.json` run failed with `numpy._core._exceptions._ArrayMemoryError: Unable to allocate 24.0 MiB for an array with shape (1088, 1928, 3) float32` at `nodes_minimax_h3.py:229 _resize`. **This is a CPU RAM exhaustion, NOT a VRAM problem and NOT a workflow bug.**

**CORRECTED (2026-08-30, after measuring with `top_ram.py`):** my first claim — "the 7 Krea2 runs left ~17 GB of Krea2 models resident in CPU RAM" — was **WRONG / unverified**. Measured reality: ComfyUI's `python.exe` was only **1.37 GB**. The dominant RAM consumer is the **local Qwen `llama-server.exe` at ~19-22 GB** (a SEPARATE process ComfyUI cannot touch). The system was at **95% load / 2.7 GB free**, so even a 24 MB CPU allocation failed. The process list accounted for ~36 GB; the rest of the 66 GB was page file / memory compression / transient allocations. **The real pressure source is the Qwen llama-server, not ComfyUI's models.**

**FIX APPLIED (user):** removed `--lowvram` from the ComfyUI launch script (now: `--windows-standalone-build --reserve-vram 4 --disable-pinned-memory --use-pytorch-cross-attention --cache-none --enable-manager`). Without `--lowvram`, ComfyUI keeps its models in **VRAM** (32 GB free) instead of offloading to CPU RAM, so it no longer competes with the Qwen llama-server for CPU RAM. After restart: system at **66% load / 22.4 GB free**, llama-server 22.3 GB, ComfyUI 1.37 GB. **The MiniMax 7-ref resize (24 MB float32 per image on CPU) now trivially succeeds.**

**Rule: the dominant CPU-RAM consumer is the local Qwen llama-server (~22 GB), NOT ComfyUI. Run ComfyUI WITHOUT `--lowvram` so its models stay in VRAM (32 GB free) and don't compete with Qwen for CPU RAM. If a heavy run still OOMs, the constraint is the llama-server's footprint — reduce its context/concurrency, not ComfyUI's. VERIFY RAM consumers with `top_ram.py` before diagnosing — do NOT assume which process is holding the RAM.**

### Update 2026-08-30 (Pipeline 1 — 2K render VRAM-thrashed → set to 1MP native; render-time baseline)

User: "I think we should have went with 1MP. [log: Model Initializing ... 0/8 [10:15<?, ?it/s] ... Prompt executed in 00:11:31] I had to stop this. Can you check the forums how much time it will take to render a 15 second 2mp REF2 on RTX 5090?"

**Diagnosis (from the user's own log, not forums):** the 2K render **never started sampling** — it was stuck at **0/8 steps, "Model Initializing", for 10+ minutes**. That is NOT slow sampling; it is the **~20 GB model (`19995MB Staged`) + 2K video activations thrashing in VRAM** (32 GB card, `--reserve-vram 4`). At 2048×1152 the video latent + activations are so large ComfyUI spends all its time moving the model in/out of VRAM instead of generating. It likely would not have finished in reasonable time.

**Render-time baseline (from the user's OWN machine, not forums):** the 11 `Jaisal_Production_1` outputs were written ~10–15 min apart (04:31 → 04:45 → 04:55 → 05:10 → 05:23), so **~10–15 min per 0.4 MP render** is the real baseline. Video cost scales with pixels × frames × steps:
- 0.4 MP (864×480): ~10–15 min (measured)
- **1.0 MP (1344×768, native): ~25–40 min**
- 2.4 MP (2048×1152, 2K): ~60–90 min AND VRAM-thrashing (what the user just hit)

The reference video barely adds compute (it's a conditioning input, not a big cost) — the cost is **output resolution × 15s × 8 steps**.

**⚠️ CORRECTION (2026-09-01) — the 25–40 min figure is for FULL-attention H3. Our ACTUAL speed stack is SLA, and 1MP generation is UNDER 240 SECONDS.** The user's production workflows (`jaisalproduction1.json`, `jaisal_2mp_test.json`, `beach_sprint_test.json`, `t2v_beach_sprint_test.json`) all wire an **`H3SLAAttention` node (id 150)** from `ComfyUI-PlagueKind-Nodes/ComfyUI-H3-SLA-Attention` (Sparse Linear Attention). Config in use: `widgets_values = [0.9, '32', 8192, 1, True, True, '0', 'comfy_kitchen', True, False, False]` → **sparsity 0.90, dense_backend = `comfy_kitchen_int8`**. With SLA, a 1MP H3 render completes in **< 240 s (~4 min)**, NOT 25–40 min. **Do NOT quote the 25–40 min estimate for our current pipeline — that number is obsolete now that SLA is in the graph.** (The 2K VRAM-thrashing diagnosis above still stands — SLA speeds the attention math but does not remove the 2K activation/VRAM pressure.) See **D042**.

**Decision: set the `ResolutionSelector` (node 115) to `['16:9 (Widescreen)', 1.0, 32]` → 1344×768 (MiniMax H3 NATIVE canvas).** 1MP is what the model is designed for, fits comfortably in VRAM, and renders in a finite ~25–40 min. For 2K, the clean path is **render at 1MP → upscale** (Topaz/RTX/Hunyuan upscalers are all installed) — faster and cleaner than a direct 2K render. The reference video node (149) stays wired as the motion anchor.

**Rule: do NOT render MiniMax H3 at 2K directly on a 32 GB card — the ~20 GB model + 2K activations thrash VRAM (stuck at 0/8 steps in "Model Initializing"). Render at the NATIVE 1344×768 (1.0 MP) and upscale to 2K in a separate step. Estimate render time from the user's OWN output timestamps (file mtimes), not forums — forums rarely have a clean per-GPU benchmark. A render stuck at 0/8 steps in "Model Initializing" for many minutes = VRAM thrashing, not slow sampling.**

### Update 2026-08-30 (Pipeline 1 — added reference VIDEO (motion anchor) + 2K resolution)

User: "I got one output, and I'm okay with it. Can I add it as a reference and render it in 2K so that it follows the same action?" (referring to `Jaisal_Production_1_00011_.mp4`, the most recent good output).

Updated `jaisalproduction1.json` (validated `valid: true`, now 23 nodes):
- **Added a `MiniMaxH3ReferenceVideoLoadStar7` node (id 149)** that loads the good output video as a MOTION anchor. The node scans the `input` dir, so the video was copied to `input\jaisal_prod1_ref.mp4` (from `output\video\Jaisal_Production_1_00011_.mp4`).
- **Wired:** node 149 IMAGE output (slot 0) → link 303 → node 136 `ref_videos.ref_video_0` (slot 9); node 149 AUDIO output (slot 1) → link 304 → node 136 `ref_video_audios.ref_video_audio_0` (slot 10). The 3 reference IMAGES stay (visual anchors); the video adds the motion/action anchor so the new render follows the same action.
- **Set 2K:** the `ResolutionSelector` (node 115) was `['16:9 (Widescreen)', 0.4, 32]` (≈864×480). Set to `['16:9 (Widescreen)', 2.4, 32]` → **~2048×1152 (2K)**. The middle widget is MEGAPIXELS (1.0 ≈ 1024×1024); 2.4 MP @ 16:9 = 2048×1152. The MiniMax node width/height accept up to 16384 (step 32), so 2K is valid.
- **`MiniMaxH3ReferenceVideoLoadStar7` widgets:** `[video, max_long_edge, allow_upscale]` = `['jaisal_prod1_ref.mp4', 1344, False]`. `max_long_edge` (default 1344) = the H3-aligned long edge the ref video is fitted to (keeps aspect). `allow_upscale` = False (avoids spending H3 reference tokens on interpolated detail; enable only for structure/motion A/B tests).

**Rule: to make a new MiniMax R2V render FOLLOW THE SAME ACTION as a good output, add a `MiniMaxH3ReferenceVideoLoadStar7` node that loads that output video and wire its IMAGE output to `ref_videos.ref_video_0` (+ AUDIO to `ref_video_audios.ref_video_audio_0`). The node scans the `input` dir, so copy the video there first. The reference images stay as visual anchors; the video is the motion anchor. For 2K, set the `ResolutionSelector` megapixels widget to ~2.4 (16:9 → 2048×1152). A 2K render is ~6× the pixels of the 0.4 MP default, so it's much slower + more VRAM — run it when the machine is free (the Qwen llama-server holds ~22 GB CPU RAM).**

### Update 2026-08-30 (Pipeline 1 prompt v10 — Shot 1 WIDE ANGLE + Shot 3 climbs then jumps (no hand gestures))

User reviewed Pipeline 1 v9: "(1) the first shot is literally NOT a wide angle shot - it went back to a different structure. (2) the 2nd one is stable. (3) the 3rd one is not good - I think it's because we said he is doing hand gestures, it confused [the model]. Let's remove that. He is SLOWLY LIFTING HIS LEG and CLIMBING and then JUMPING. That's it. But there should NOT be a static shot. Let's tweak the prompt a little more and I will try again."

User's inline edits in the pasted prompt (folded into v10):
- Shot 1: "we should not have any extra characters apart from the first character which is standing on the LEFT side of the bridge, only that character has to run" + "NOT an Extra Character" in the gait line.
- Shot 3: "he is not repeating the movement, he breathes in after the run" + "LEAPS over the low handrail SLOWLY".
- New `overall_landscape` section: "we should see VISIBLE RAINFALL, after the first picture throughout the sequence".

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Shot 1 = WIDE ANGLE:** "a WIDE ANGLE establishing shot - the camera is positioned FAR AWAY, showing the boy as a small figure on the bridge with the full landscape, sky, and river visible. This is a WIDE ANGLE view (NOT a medium shot, NOT a close-up)." + "ONLY ONE boy <Subject 1> is on the bridge, standing on the LEFT side of the bridge - there are NO other people, NO second boy, NO duplicates, NO extra characters. Only that ONE boy runs."
- **Shot 2:** UNCHANGED (user: "the 2nd one is stable").
- **Shot 3 = climbs then jumps (NO hand gestures):** "The boy is NOT standing still - he is SLOWLY LIFTING HIS LEG and CLIMBING over the low handrail, then JUMPING. He is not repeating the movement - he breathes in after the run." Then "LEAPS over the low handrail SLOWLY - his body fully airborne." (Removed the v9 "shakes his head, makes hand gestures" which confused the model.)
- **`<Picture 3>` definition** kept: "preparing to jump over the handrail".
- **summary** updated: "then climbs over the handrail and leaps" (was "then prepares and leaps").
- **overall_soundscape** updated: "a rising tension as the boy climbs and leaps" (was "prepares and leaps").
- **New `overall_landscape` section:** "We should see VISIBLE RAINFALL throughout the sequence after the first picture - rain is clearly falling and visible in [Shot 2] and [Shot 3]."
- RAIN still enforced in every shot. Timing still 4/6/5 (00:00.000 / 00:04.000 / 00:10.000).

**Rule: when a shot comes out NOT wide-angle, say "WIDE ANGLE establishing shot - the camera is positioned FAR AWAY, showing the boy as a small figure with the full landscape/sky/river visible (NOT a medium shot, NOT a close-up)" - the word "wide" alone is not enough, you need to describe the camera being FAR AWAY + the boy being a SMALL FIGURE. When a "preparing" action (head shake, hand gestures) confuses the model, REPLACE it with a concrete physical action that leads into the main action (SLOWLY LIFTING HIS LEG and CLIMBING over the handrail, then JUMPING) - a clear physical chain is less confusing than vague gestures. And to keep a shot from being static, say "he is NOT standing still - he is [concrete action]" + "he is not repeating the movement, he breathes in after the run" (a breath beat between actions prevents a frozen frame without adding confusing gestures).**

### Update 2026-08-30 (Pipeline 1 prompt v9 — Shot 3 PREPARES while camera moves, then leaps)

User reviewed Pipeline 1 v8: "the 3rd shot was working fine 3 prompts ago (v5), we need those camera moves, but we have to mention that the 3rd one is NOT a static frame - when it loads he has to do some action, like shaking head or some hand gestures while the camera is moving, and then he can jump, so while the camera is moving he can prepare also, so that feels more natural. The rule should be: where he is moving and what he is doing - we don't want him to run back and forth. Explain it cleanly. I want to get it done, it's been 8 hours."

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Shot 3 camera moves RESTORED to v5** (the user said v5's shot 3 was working fine): SIDE view from the VIEWER'S LEFT, boy on viewer's left, camera ANCHORED on viewer's left + TRACKS him (NOT a left-to-right sweep), swings to his BACK as he leaps, ENDS at his back mid-air BEFORE the water.
- **Shot 3 is NOT a static frame:** "The boy is NOT standing still - while the camera moves, he is PREPARING to jump: he shakes his head, makes hand gestures, and gets ready. Then the boy LEAPS over the low handrail." (This replaces v8's "ALREADY RUNNING and IN MOTION at the start" which was over-constraining and breaking the shot.)
- **<Picture 3> definition** updated: "the boy at the middle of the bridge, a side view from the VIEWER'S LEFT, **preparing to jump over the handrail**" (was "already running toward the handrail").
- **summary** updated: "then prepares and leaps over the handrail" (was "then runs toward the handrail and leaps over it").
- **overall_soundscape** updated: "a rising tension as the boy prepares and leaps" (was "runs and leaps").
- **CLEAN RULE (user's):** state WHERE the boy is moving and WHAT he is doing - do NOT have him run back and forth. Shot 3: he is at the middle of the bridge, facing the handrail (toward the river), PREPARING (shaking head, hand gestures) while the camera moves, then LEAPS. One direction, one action, no back-and-forth.
- RAIN still enforced in every shot (unchanged). Timing still 4/6/5 (00:00.000 / 00:04.000 / 00:10.000).

**Rule: when a shot keeps breaking under over-constraint, GO BACK to the last version that worked (v5's shot 3 camera moves) and add ONLY the one missing element (the boy is NOT static - he PREPARES: shakes head, hand gestures, while the camera moves, then leaps). The rule for describing motion is: state WHERE the subject is and WHAT he is doing in ONE direction - do NOT have him run back and forth. A "preparing" action (head shake, hand gestures) while the camera moves feels more natural than a static frame AND is less likely to break than a full run→crouch→plant→leap chain.**

### Update 2026-08-30 (Pipeline 1 prompt v8 — timing 4/6/5 + Shot 3 starts IN MOTION)

User reviewed Pipeline 1 v7: "(1) [Shot 1] should have 4 seconds, (2) [Shot 2] we can extend till 10 where we have proper direction, (3) [Shot 3] the same issue came back - the starting frame is standing still, we should not do that."

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Timing:** [Shot 1] = **4s** (00:00.000), [Shot 2] = **6s** (00:04.000 → 00:10.000, "proper direction" = the turn is clear and deliberate, body rotates fully toward the VIEWER'S LEFT), [Shot 3] = **5s** (00:10.000). Total = 15s (length node 132 stays 15).
- **Shot 3 starts IN MOTION:** "The boy is ALREADY RUNNING and IN MOTION at the start of this shot - he is NOT standing still, he is moving toward the handrail with momentum." Then he runs toward the handrail, crouches, plants, and LEAPS. (The v7 issue: the starting frame was standing still.)
- **<Picture 3> definition** updated: "the boy at the middle of the bridge, a side view from the VIEWER'S LEFT, **already running toward the handrail**" (was "about to climb over the handrail and leap").
- **summary** updated: "then runs toward the handrail and leaps over it" (was "then climbs over the handrail and JUMPS").
- **overall_soundscape** updated: "a rising tension as the boy runs and leaps" (was "climbs and leaps").
- RAIN still enforced in every shot (unchanged from v7).

**Rule: when a shot's STARTING FRAME comes out standing still, say explicitly "the boy is ALREADY RUNNING and IN MOTION at the start of this shot - he is NOT standing still" AND update the <Picture N> definition to describe the in-motion pose ("already running toward the handrail") - the reference frame anchor + the explicit in-motion line together prevent a static opening. And when the user gives a timing split (4/6/5), set the [Shot N] timestamps to match (00:00.000 / 00:04.000 / 00:10.000) and keep the length node = the total (15s).**

### Update 2026-08-30 (Pipeline 1 prompt v7 — SIMPLIFIED + RAIN enforced in every shot + Shot 3 ends mid-air)

User reviewed Pipeline 1 v6: "the first clip had a lot of issues, the hard rule didn't apply well, check out the H3 prompt guide, let's clear out the confusion and keep it simple. (1) Shot 1 should focus on the CLIMATE and MOOD, the kid is WALKING / SLOWLY RUNNING. (2) Shot 2 is fine. (3) Shot 3 is fine BUT we do NOT want to show the kid jumping TO the water - the jump and the cut should happen AFTER the jump, we don't need to show till he reaches the water, and the bridge has HEIGHT - do not treat this as a swimming pool. (4) IMPORTANT: none of them has RAIN in it - we should enforce MiniMax to add RAINING."

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **SIMPLIFIED** the whole prompt (removed the heavy CHARACTER COUNT block + the over-stuffed negative constraints that "didn't apply well"). Kept the 6-section structure per the H3 guide. Kept the ORIENTATION block (boy's right = viewer's left).
- **Shot 1:** now focuses on the CLIMATE and MOOD - the boy WALKS and SLOWLY RUNS (natural gait, feet lift+land separately, NOT a slide), MAIN PURPOSE = ESTABLISH THE CLIMATE AND MOOD (sky clear→moody, RAIN BEGINS TO FALL and builds, landscape shifting). Fixed wide static camera.
- **Shot 2:** UNCHANGED (user: "the second one is fine").
- **Shot 3:** the boy crouches → plants → LEAPS over the handrail, fully airborne. **The bridge is TALL - a real leap from height over the wide river, NOT a shallow pool.** The shot ENDS with the camera at his BACK as he is in the air, **BEFORE he reaches the water** - the cut happens right here so the next clip picks up the jump. (Removed the "DIVE into the river / SPLASH" - we do NOT show him reaching the water.)
- **RAIN enforced in EVERY shot:** "RAIN is present in EVERY shot - rain is falling in [Shot 1], [Shot 2], and [Shot 3]" (detailed_description global line) + "RAIN THROUGHOUT the whole video (light rain building in [Shot 1], heavier rain in [Shot 2] and [Shot 3])" (overall_soundscape). Shot 1 = rain BEGINS and builds; Shot 2 = rain streaks visible; Shot 3 = HEAVY RAIN.

**Rule: when a hard rule "doesn't apply well", SIMPLIFY - over-stuffed negative constraints (a whole CHARACTER COUNT block + many NOT-clauses) dilute the signal. Keep the 6-section structure, state the key requirement once clearly per shot, and ENFORCE the global element (RAIN) in BOTH the detailed_description global line AND the overall_soundscape so MiniMax can't drop it. For a jump that must NOT show the landing: end the shot mid-air BEFORE the water and say the bridge is TALL (a real leap from height, NOT a shallow pool) - the cut happens at the apex so the next clip picks up the jump.**

### Update 2026-08-30 (Pipeline 1 prompt v6 — ONLY ONE character + Shot 3 JUMP made explicit)

User reviewed Pipeline 1 v5: (1) **Shot 1 had 2 characters** — MiniMax duplicated the boy; need a HARD demand that there is ONLY ONE character. (2) **Shot 2 is fine** — keep as is. (3) **Shot 3 is fine on camera angle but the JUMP didn't happen** — the boy climbed but never actually jumped; need more detail so it speeds up and the leap actually occurs.

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Added a CHARACTER COUNT block** (new section): "There is ONLY ONE character in the entire video - the single young schoolboy <Subject 1>. There are NO other people, NO second boy, NO duplicates, NO extra figures, NO crowds, NO bystanders, NO reflections of a second person. Every shot shows exactly ONE boy and only that boy." Also added to summary, retention_analysis ("ALWAYS exactly ONE boy - never two, never a duplicate"), the detailed_description global line, and the [Shot 1] line ("ONLY ONE boy ... NO second person, NO duplicate, NO other figure anywhere in the frame").
- **Shot 2 UNCHANGED** (user: "second one is fine").
- **Shot 3 JUMP made explicit + sped up:** the boy "moves QUICKLY and with PURPOSE - he crouches, plants his feet, and then JUMPS: he LEAPS over the low handrail and DIVES into the river, his body fully airborne, arms out, a clear dynamic leap (NOT just climbing, NOT just standing, NOT just walking - he MUST actually JUMP and go over the handrail into the water)." Camera angle kept correct (SIDE view from viewer's left, anchored + tracks, swings to his back). summary + detailed_description now say "[Shot 3] MUST show the boy JUMPING into the river".
- **Sound:** added "a big SPLASH as he JUMPS into the river" to overall_soundscape.

**Rule: MiniMax DUPLICATES the character (a 2nd boy) unless you HARD-DEMAND "ONLY ONE character, no duplicates, no second figure" in a dedicated block + summary + retention + the wide-shot line (the wide shot is where a duplicate is most visible). And a JUMP/leap will NOT happen from a vague "climbs and leaps" — you must spell out the physical action (crouch → plant → LEAP over the handrail → DIVE into the water, fully airborne) and forbid the failure modes ("NOT just climbing, NOT just standing, NOT just walking"). If the action still doesn't happen, add a reference frame that already shows the airborne pose.**

### Update 2026-08-30 (Pipeline 1 prompt v5 — left/right orientation fix + sound + sliding)

User reviewed Pipeline 1 v4: (1) **Sound is bad in the first sequence** — needs to clearly convey **running footsteps + a building thunderstorm** (thunder rumbles, heavy rain). (2) **The left/right was wrong** — "when I say he is moving right I meant HIS right (the VIEWER'S LEFT), and that's how our 3rd portion starts." (3) **Shot 3 camera angle is confusing** — it was sweeping **left-to-right**; the user wants it **anchored on the VIEWER'S LEFT** (where the boy is after turning), tracking him, NOT sweeping across.

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Added an ORIENTATION block** (new section after subject_definitions): "The boy's RIGHT side is the VIEWER'S LEFT side of the frame. When the boy turns toward his right, he turns toward the VIEWER'S LEFT. [Shot 3] is a side view from the VIEWER'S LEFT side, and the boy is on the VIEWER'S LEFT of the frame." + "All left/right references use the VIEWER's perspective" in the detailed_description global line.
- **Shot 2:** the boy turns toward **HIS RIGHT = the VIEWER'S LEFT** (toward the river).
- **Shot 3:** now a **SIDE view from the VIEWER'S LEFT**, boy on the VIEWER'S LEFT of the frame; the camera is **anchored on the VIEWER'S LEFT and TRACKS the boy (does NOT sweep left-to-right)** as he climbs, then swings to his BACK as he jumps.
- **Shot 1 sliding:** even more forceful — "a REAL running gait - each foot clearly LIFTS and LANDS separately, visible leg movement, one step at a time (NOT a smooth slide, NOT a glide, NOT a blur, NOT a keyframe slide, NOT fast)".
- **Sound (overall_soundscape):** "Clear running footsteps on the stone bridge, heavy rain, a building thunderstorm with distant thunder rumbles, splashing water on the bridge stones, then a rising tension as the boy climbs and leaps."

**Rule: ALWAYS specify left/right from the VIEWER's perspective in R2V prompts (the boy's right = the viewer's left) — ambiguous "his right" makes MiniMax pick the wrong side. Anchor the camera to a fixed side (the viewer's left) and say it TRACKS the subject rather than "moves across" (which reads as a left-to-right sweep). And name the exact sounds you want (running footsteps + thunderstorm rumbles) in overall_soundscape — a vague "wind building" gives muddy audio.**

### Update 2026-08-30 (Pipeline 1 prompt v4 — wide shot as a HARD demand + slow run + climate change)

User: "make sure the wide shot is also a hard demand and the kid has to slowly run, but that shot should establish the climate change." Updated `jaisalproduction1.json` node 138 (validated `valid: true`): (1) the **wide shot is now a HARD REQUIREMENT** — added to the summary ("[Shot 1] MUST be a LONG WIDE establishing shot that shows the landscape and the climate change") and the detailed_description global line ("[Shot 1] MUST be a LONG WIDE establishing shot (a hard requirement - it must NOT be cut short, NOT turned into a close-up, NOT skipped)"), and the Shot 1 line itself ("a HARD REQUIREMENT - the camera does NOT move closer, does NOT push in, does NOT cut to a close-up - it stays a FIXED wide view the whole time"). (2) **Slow running** reinforced: "runs SLOWLY and DELIBERATELY... (NOT rushing, NOT sliding, NOT a blur, NOT fast)". (3) **Climate change is the shot's MAIN PURPOSE**: "The MAIN PURPOSE of this shot is to ESTABLISH THE CLIMATE CHANGE - the sky gradually darkens from clear to moody overcast, the wind picks up, and rain begins to fall, the whole landscape and environment shifting from clear to rainy." **Rule: when a shot has a specific job (establish the climate, hold the wide), state it as a HARD REQUIREMENT in BOTH the summary and the per-shot line, and explicitly forbid the failure modes (cut short / turned into a close-up / skipped) — MiniMax needs the negative constraints to hold the shot.**

### Update 2026-08-30 (Pipeline 1 prompt v3 — fixed wide shot 1, stop/turn-right shot 2, side→across→back shot 3)

User reviewed Pipeline 1 v2: (1) **Shot 1** must be a **LONG WIDE STATIC shot** (camera does NOT move closer / NOT push in) — the whole purpose is to show the **landscape + sky slowly changing mood**, boy runs slowly, **5s**. (2) **Shot 2:** boy runs, stops, **looks toward his RIGHT side** (toward the river), **5s** for running + stopping + turning. (3) **Shot 3 "completely gone from the sequence, didn't appear, camera movement not showing"** → new choreography: **SIDE view (his right) → camera MOVES ACROSS (tracking) as he climbs over the handrail → camera swings to his BACK side as he jumps**, ENDS at his back mid-leap. **CRITICAL FIX: MiniMax DROPPED Shot 3 entirely** (it compressed the sequence and skipped the last shot). Added strong emphasis to the prompt: "ALL THREE shots must appear in this order, each getting its full time - do not skip, compress, or drop any shot, especially [Shot 3]" (in summary + detailed_description). **Rule: MiniMax will DROP the last shot of a multi-shot R2V if the prompt doesn't explicitly demand all shots appear — add a hard "ALL N shots must appear, do not skip/compress/drop any" line. Also: a wide establishing shot's purpose is the LANDSCAPE + sky change, so keep the camera FIXED (no push-in) and let the environment shift; and specify the camera's exact path for the jump shot (side → tracking across → back side) rather than a vague "camera rotates".**

### Update 2026-08-30 (Pipeline 1 prompt v2 — slow running + stop/turn/pan + in-motion shot 3)

User reviewed `jaisalproduction1.json` (Pipeline 1 only — Pipeline 2 not yet tried): (1) **Shot 1 (7s)** the boy "rushing, doesn't feel like running, felt like sliding a keyframe, not real" → now **SLOW, DELIBERATE, step-by-step** running: "each step clearly visible, one foot at a time, feet landing one after the other in a clear step-by-step rhythm (NOT rushing, NOT a fast blur, NOT sliding, NOT a smooth glide - real running with distinct steps)". (2) **Shot 2 (3s)** was good/matching pace → kept, but added at the end: the boy **SLOWS and STOPS, then TURNS toward the river, and the camera PANS to follow him** into the next view (the user's "stop and turn, then pan to Picture 3" idea — motivates the cut). (3) **Shot 3 (5s)** was the worst — "static, standing still for 2s while camera tilts" → now the boy is **IN MOTION the whole time**: "just stopped and turned toward the river, looks down at the water, takes a few steps toward the edge, crouches, and gathers himself to leap... NEVER standing still - every moment he is doing something (turning, stepping, looking down, crouching)". Kept the camera-rotate structure the user liked. **Rule: MiniMax makes running look like a "sliding keyframe" if you just say "runs" — specify SLOW + step-by-step + distinct footfalls. And a shot that opens on a static standing figure reads as dead — keep the character in motion from the first frame (turning/stepping/looking), and bridge the cut with a stop+turn+pan so the next shot's first frame is motivated.**

### Update 2026-08-30 (2-pipeline production split — `jaisalproduction1.json` + `jaisalproduction2.json`)

User: the full sequence should be ~25s (not 15s) with better rhythm — wide run-up 7s, close-up 3s, gather/climb/push-off 5s (15s run-up), then jump + drown 5-6s + title 4s. **Decision: split into TWO separate MiniMax R2V generations** (shorter clips = less style drift, cleaner 3-ref mapping, the jump is a natural splice point, re-run only the bad segment). Shot 3 (running medium) REMOVED entirely.

**Built two workflows** (both validated `valid: true`, 22 nodes):
- **`jaisalproduction1.json`** (run-up, **15s**, save `video/Jaisal_Production_1`): refs `jaisal_1_longshot` (ref_image_0), `jaisal_2_closeup` (ref_image_1), `jaisal_4_middle` (ref_image_2). Shots: (1) wide, boy RUNS ~7s, sky darkens clear→moody, rain begins, static wide → slow push-in; (2) close-up, boy RUNS (NOT static), camera tracks, wind + rain ~3s; (3) SIDE view at middle in HEAVY RAIN, crouches + gathers, camera ROTATES, climbs over low handrail, pushes off toward river, ENDS mid-launch ~5s.
- **`jaisalproduction2.json`** (leap + title, **11s**, save `video/Jaisal_Production_2`): refs `jaisal_5_jump` (ref_image_0), `jaisal_6_underwater` (ref_image_1), `jaisal_7_title` (ref_image_2). Shots: (1) SHORT natural leap CLOSE to bridge (NOT a long throw / stone) ~2s; (2) underwater, sinks completely down, rising bubbles ~4.5s; (3) title card, bubbles foam up, 'The Jaisal Cut' slowly becomes visible, color grade EXACTLY matches shot 2 ~4s.
- **Both prompts lock a consistent color grade** (same dark moody palette / dim grey light / water color across all shots) to minimize the two-generation seam.
- **Splice:** cut at the push-off moment (pipeline 1 ends mid-launch, pipeline 2 starts in-air), HARD CUT not crossfade, color-match the splice frame in post.
- **Build script:** `d:\models\vsCodeMcp\utilities\build_production_pipelines.py` (copies `jaisal_lowangle.json`, keeps 3 LoadImage nodes per pipeline, rebuilds node 136 to 3 ref slots, new links 300-302, sets length + save prefix + prompt).
- **Rule: for a long cinematic sequence, split into 2-3 shorter R2V generations at natural action splice points (push-off → in-air) rather than one long run — less drift, cleaner refs, easier re-runs. Join in a video editor with a hard cut + color match.**

### Update 2026-08-30 (7-shot MiniMax R2V — `jaisal_lowangle.json`)

User: "now lets go to minimax... we have 7 images... first one is a long shot (add running + climate change), 2nd close-up (camera movement + wind), 3rd running (motion + camera + wind), 4th kid standing middle full figure (ADD rain), 5th wide low-angle jump (complete the motion into the river), 6th underwater (move kid completely down), 7th title. All transitions smooth and organic. NOTE: the picture added as 1 can be reference image 0 in the node and it can mess up the prompt if we add picture 1 in prompt — so let's not make that mistake. This is a multi-billion-dollar company's production animation — a cinematic masterpiece intro."

**Built `jaisal_lowangle.json` as a 7-shot R2V** (validated `valid: true`, 26 nodes):
- **7 LoadImage nodes** (137, 139, 147, 148, 149, 150, 151) → `MiniMaxH3ReferenceToVideo` (136) `ref_image_0`..`ref_image_6`. Images copied to `input\` as `jaisal_1_longshot.png` … `jaisal_7_title.png`.
- **CRITICAL (user's note):** the `<Picture N>` tags map 1-to-1 to `ref_image_N` IN CONNECTION ORDER — `<Picture 1>` = `ref_image_0` = image 1 (long shot), etc. This is the correct pattern (each reference is a frame anchor for its shot), NOT a mistake. The old 2-ref workflow's "mess up" concern was about a single reference being both the style anchor AND the first frame; here each of the 7 references is its own shot's first frame, so the mapping is clean.
- **Prompt (node 138):** 7-shot R2V structure (subject_definitions / summary / retention_analysis / detailed_description with timed `[Shot N] At MM:SS.mmm` blocks / overall_soundscape / non_diegetic_music). Each shot: (1) long shot — boy runs, sky darkens clear→moody, wind + rain begins, static wide → slow push-in; (2) close-up — gentle camera push-in/drift + wind in hair/shirt; (3) running — camera tracks alongside at running pace, wind + rain + splashes; (4) middle full figure — ADD heavy rain, steady camera with subtle drift; (5) wide low-angle jump — camera completes his motion into the river, big splash; (6) underwater — camera follows him sinking completely down, rising bubbles; (7) title — calm dark water, bubble-formed 'The Jaisal Cut' title held steady. **All transitions smooth and organic.**
- **Bag color FIXED:** prompt now says **BLACK school bag** (was "red school bag" — the pending fix from earlier).
- **Title:** shown in Shot 7 (the title reference image), NOT rendered as a text overlay by the model.
- **Build script:** `d:\models\vsCodeMcp\utilities\build_minimax_7shot.py` (copies images, grows node 136 to 7 ref slots, shifts downstream link slots prompt→13/width→14/height→15/length→16, adds links 289-294).

### Update 2026-08-30 (size hierarchy: The < Cut < Jaisal)

User asked for a **size hierarchy** in the title: **"The" = SMALL, "Jaisal" = BIG (the hero word, largest), "Cut" = MEDIUM** (between the two). Prompt 10 positive now states the hierarchy explicitly: "the title words sized in a clear hierarchy - the word 'The' SMALL, the word 'Jaisal' BIG and dominant (the largest word, the hero of the title), the word 'Cut' MEDIUM (between the two)". **Tuning:** 'Jaisal' not big enough → strengthen it ("'Jaisal' MUCH larger than the other words, the clear focal point"); hierarchy lost (all words same size) → restate more forcefully and/or lower denoise a touch so the layout is followed more faithfully.
---

## D027 - Title animation = 2D VECTOR / LINE-ART stick figure (not cartoon/3D), MEDIUM shots only

Date: 2026-08-31
Status: Active

### Decision

The title animation is a **2D vector / line-art** piece — a **stick figure** (round head + line body + line arms + line legs, clean confident line work, lines only, NO shading, NO 3D, NO cartoon shading). Story: the stick figure **walks slowly** on the bridge → **throws a paper plane** into the river → **jumps into the river** after the paper plane → the paper plane is **still flying** as the title **"The Jaisal Cut"** appears. Simple, funny, **no special effects**. **MEDIUM SHOTS ONLY** (the figure's full body visible) — **NO wide shots**, NO extreme close-ups.

### Reason

The user wants a simple vector/line look ("just with lines and everything", "a stick with a head and hand and legs"), not the cartoon/2D brush-stroke style. The paper-plane gag makes it funny. Medium shots keep the figure readable. The line-art look is carried by the **`krea2_lineart_v1_fp16.safetensors`** LoRA (Civitai "Krea2 Line Art Style", downloaded 2026-08-31, 56 MB, in the main loras path).

### Alternatives considered

- Cartoon/2D brush-stroke style (rejected — user wants pure lines).
- Wide establishing shots (rejected — user: "lets not keep any wide shots, medium shots are fine").
- Other Civitai sketch/vector LoRAs (`SimpleFineVector_Krea2_v1`, `krea2_coloringbook_v1`, `friendlysketch-v2_krea2`) — found but the Civitai download hit a Cloudflare challenge page (10 KB HTML); only `krea2_lineart_v1_fp16` downloaded cleanly. Re-download the others if the line-art LoRA isn't clean enough.

### Result

`d:\models\vsCodeMcp\prompts\jaisal_sketch_prompts.txt` created — 4 ready-to-paste Krea2 t2i prompts (walk / throw paper plane / jump / title) + shared style prefix + shared negative (excludes 3D/shading/color-fill/carton/wide-shot/close-up) + a full MiniMax H3 R2V prompt (4 refs, 4 shots, 4s each, 16s). **Rule: the title animation is a 2D vector line-art stick figure, medium shots only, paper-plane gag, no special effects. Use the `krea2_lineart_v1_fp16` LoRA @ 1.0.** See `jaisal_sketch_prompts.txt`.

### Production pipeline note (2026-08-31)

The production workflow renders at **1MP (1344×768, native) and is UPSCALED to 2MP** — we do NOT generate 2MP video directly (VRAM thrashing on the 32 GB card). Upscale path: `RTXVideoSuperResolution` (2× ULTRA) or `TopazVideoEnhance` (Starlight 1080p/4K) inserted between `CreateVideo` and `SaveVideo`.

---

## D028 - MiniMax R2V prompts use standard cinematography vocabulary (shot size + angle + movement + focus per shot)

Date: 2026-08-31
Status: Active

### Decision

Every MiniMax H3 R2V `[Shot N]` line names the **shot size + camera angle + camera movement + focus** EXPLICITLY using standard cinematography terms (e.g. "a static eye-level MEDIUM shot, deep focus", "a slow tracking shot from the side", "a low-angle shot looking up"). The full vocabulary (shot size / framing / focus / angle / movement / mechanism, each with a ready-to-paste phrase) is saved at `d:\models\vsCodeMcp\docs\CAMERA_SHOT_VOCABULARY.md` (sourced from the StudioBinder "50+ Types of Camera Shots, Angles, and Techniques" guide).

### Reason

MiniMax responds to standard cinematography vocabulary far better than vague words like "the camera moves" or "a nice angle". Naming the exact shot size + angle + movement + focus per shot gives much tighter shot control. The Jaisal Cut title animation uses MEDIUM shots only, static camera (low-angle for the jump), deep focus.

### Alternatives considered

- Vague camera descriptions (rejected — weak shot control).
- Naming real camera gear (tripod/dolly/drone) in a 2D line-art prompt (rejected — can confuse the model; for 2D animation just say "static" or "smooth tracking").

### Result

`CAMERA_SHOT_VOCABULARY.md` created (complete cheatsheet + ready-to-paste phrases). The Jaisal Cut title-animation MiniMax prompt (`jaisal_sketch_prompts.txt`) rewritten to the user's exact sequence (walk → stop → look around both sides → whistle → jump → title) using the camera vocabulary. **Rule: name shot size + angle + movement + focus explicitly for every [Shot N]; keep the vocabulary cheatsheet handy for reuse.**

## D029 - H3 camera-correction problem: force the angle with top-priority constraints + accept distortion + forbid the camera cheat

Date: 2026-08-31
Status: Active

### Decision

H3 has a strong internal prior to "correct" the camera toward a flattering eye-level view (especially with a face in frame). To force a specific camera angle, the prompt MUST: (1) put the camera constraint at the **absolute top** as a `MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: ...` line naming the exact angle (H3 weights the first lines most — a buried camera instruction is treated as background and ignored); (2) **explicitly accept the natural distortion** that angle causes ("ACCEPT NATURAL [ANGLE] PERSPECTIVE DISTORTION") so the face-enhancement tendency doesn't "fix" it by moving the camera; (3) **explicitly forbid moving the camera to fix the subject** ("DO NOT CORRECT CAMERA TO EYE-LEVEL TO FIX [SUBJECT] PROPORTION", "DO NOT auto-adjust camera perspective", "REJECT flat eye-level frontal camera"); (4) use **short hard negative commands** ("NO eye-level shot", "NO camera at face height", "FORBIDDEN: flat frontal camera") — long explanatory reasoning is less reliable than short `DO NOT`/`NO`/`FORBIDDEN` prohibitions; (5) **keep the reference's identity but discard its camera** ("COMPLETELY DISCARD <Picture N> original camera angle, framing, background, lighting, and pose") so the reference doesn't drag the camera back. For a STATIC shot, the lock is the inverse: "the camera is locked and does NOT move, does NOT push in, does NOT drift, does NOT tilt, does NOT pan, does NOT zoom." Also **be specific about what the subject does AND does not** — list the concrete action chain in order + an explicit NOT-list ("does NOT run, does NOT jump yet, is NOT duplicated").

### Reason

The user's high-overhead camera workflow (a 45-55° high-down overhead shot) kept failing because H3 silently moved the camera back to eye level to make the face look better (the cheat: camera stays eye-level, subject just tilts the head up). The fix is to lock the camera with top-priority constraints, accept the natural high-angle face distortion, and explicitly forbid the camera cheat. The same discipline applies to ANY forced angle (overhead, low-angle, static).

### Alternatives considered

- Burying the camera instruction in the middle of the prompt (rejected — H3 treats it as background and ignores it).
- Long explanatory reasoning about the camera (rejected — less reliable than short hard prohibitions).
- Letting the reference image set the camera (rejected — it drags the camera back to the reference's original angle).

### Result

Added a "Forcing a specific camera angle (the H3 camera-correction problem)" section to `docs/MINIMAX_H3_R2V_PROMPTING_GUIDE.md` (the 5 rules + a reusable camera-lock block). Rewrote BOTH title-animation prompts with this discipline: (1) the R2V prompt in `jaisal_sketch_prompts.txt` (top MANDATORY camera constraint + a GLOBAL CAMERA LOCK section + per-shot camera locks + per-shot action chains + NOT-lists); (2) the single-shot i2v prompt in `jaisal_single_shot.json` (nodes 105 + internal 104, validated `valid: true`). **Rule: to force a camera angle in H3, put the constraint at the top, accept the natural distortion, forbid the camera cheat with short hard negatives, discard the reference's camera, and give the subject an explicit action chain + NOT-list.** See D028 (cinematography vocabulary) for the shot-size/angle/movement/focus terms.

---

## D030 — Sketch title animation: B&W lock, plane stays small + in-air until 12s, wind, bubbles

Date: 2026-08-31
Status: Active

### Decision

The 2D vector line-art title animation (single-shot i2v, `jaisal_single_shot.json`) is updated with five hard rules after the first paper-plane run came out wrong:
1. **STRICTLY BLACK AND WHITE** — black ink lines on a pure white background ONLY, no color/grey/shading/warm tones (top-priority lock).
2. **BACKGROUND LOCK ACROSS ALL 15 SECONDS** — the pure white void is UNCHANGED and IDENTICAL from 0.00 to 15.00; explicitly forbid background change/shift/morph/new elements (the background was changing mid-video, around the 10s mark).
3. **PAPER PLANE SIZE LOCK** — the plane stays SMALL the whole time; never grows, never fills the screen, never huge (it was coming out huge after the throw).
4. **PAPER PLANE IN THE AIR UNTIL 12.00 SECONDS** — the plane stays flying/drifting in the AIR from the throw until 12.00s; it does NOT touch/float/land on the water before 12.00s; only floats on the water from 12.00s onward (it was floating on the water immediately).
5. **VISIBLE WIND** — line-art wind lines show the wind blowing throughout every second (the run felt windless).
Plus: after the figure sinks/drowns, a few small line-art bubbles rise in that area.

### Reason

User review of the first paper-plane run: (a) background still coming in / changing mid-video, (b) the paper plane huge after the throw, (c) the plane floating in the water instead of the air, (d) no visible wind, (e) wanted bubbles after the kid drowns.

### Alternatives considered

- Letting the plane fill the screen for the title (rejected — the user wants the plane to stay small; the title is composited in post per D004).
- A single "plain white" background line (rejected — not enough; must explicitly forbid the change/shift/morph family AND state the background is IDENTICAL across all seconds).

### Result

New prompt saved to `prompts/jaisal_single_shot_prompt_v2.txt` and applied to BOTH `jaisal_single_shot.json` instance node 105 (`widgets_values[0]` + `widgets_values_named['prompt']`) AND internal subgraph node 104 (D019 rule). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120). The R2V fallback prompt in `prompts/jaisal_sketch_prompts.txt` was updated to the SAME rules (B&W lock, background-identical-across-shots, plane small + in-air until 12.00s, wind lines, bubbles after sinking, title composited in post NOT rendered). **Rule: for the line-art title animation — strictly B&W, background IDENTICAL across all seconds, plane stays SMALL and IN THE AIR until 12.00s then floats on water, visible wind lines throughout, bubbles after the figure sinks.**


---

## D031 — Sketch title animation: 15s → 10s (background-change mitigation)

Date: 2026-08-31
Status: Active

### Decision

The single-shot i2v title animation (`jaisal_single_shot.json`) is now **10 seconds** (was 15s). The user reported the SAME background issue persisted after the v2 prompt (D030), and asked to shorten to 10s "that might fix this". The background issue is flagged as something to CHECK on (see below).

### What changed

1. **Length 15s → 10s** on BOTH nodes:
   - Instance node 105 `value_1` (length in SECONDS) = **10** (positional index 3).
   - Internal subgraph node 104 `length` (frame count at 24 fps, 17k+5 grid) = **243** (= 17×14+5 = ~10.1s; was a stale 73 = ~3s). Per D019 the converter reads the internal node, so both were set to be safe.
2. **Prompt compressed to a 10-second timeline** (saved to `prompts/jaisal_single_shot_prompt_v3_10s.txt`, applied to both nodes' `widgets_values[0]` + `widgets_values_named['prompt']`):
   - 10 per-second parts (0.00-1.00 … 9.00-10.00).
   - Paper plane now stays IN THE AIR until **9.00 seconds** (was 12.00s), then floats on the water in the final second (9.00-10.00).
   - The jump (7.00-8.00) + fall (8.00-9.00) + land/sink/bubbles + plane-lands-on-water are all compressed into the final 3 seconds.
   - All D030 rules retained: strictly B&W, background IDENTICAL across all 10 seconds, plane stays SMALL, visible wind lines, bubbles after the figure sinks.
3. Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Reason

User: "same issue, lets do this for 10 seconds, that might fix this, the background issue is something we should check on". Shorter timeline = less room for the background to drift/change mid-video.

### Background issue — CHECK ON (open)

The background (pure white void) keeps changing/coming in mid-video despite the BACKGROUND LOCK. Hypotheses to investigate:
- **The reference image itself** (`input\sketch_1_walk.png`) may have a non-pure-white background (cream/paper tone) that the model drifts toward — check the actual reference image's background color.
- **The i2v model's prior** may add a subtle environment over time even with a white reference — a shorter clip (10s) reduces the drift window.
- **The `length` widget** on the internal node was stale (73 frames = ~3s) while the instance said 15s — now synced to 243 frames (~10s); verify the actual output duration matches 10s after the next run.

### Alternatives considered

- Keeping 15s with an even stronger background lock (rejected — the user explicitly chose 10s as the mitigation).
- Splitting into 2 shorter i2v runs (deferred — try the 10s single take first).

### Result

`jaisal_single_shot.json` is now a 10s single take. **NEXT: run it and (a) confirm the output is ~10s, (b) check whether the background stays pure white across the whole clip, (c) check the reference image's background color if it still drifts.**


---

## D032 — Sketch title animation: pure-white void → minimal WATERCOLOR scene (overlay fix) + ONE plane + NO bubbles

Date: 2026-08-31
Status: Active

### Decision

The single-shot i2v title animation (`jaisal_single_shot.json`) prompt is changed from a **pure white void** background to a **FIXED MINIMAL WATERCOLOR SCENE** (a simple stone bridge over a river, soft pale blue-grey sky, soft muted blue river, soft muted green bank with a couple of simple line trees). The scene is COLORED (not pure white) and is the SAME fixed scene across all 10 seconds. Two more fixes: **ONLY ONE paper plane** (never two) and **NO bubbles** anywhere.

### Reason

User review of the v3 (10s, pure-white) run: (a) the **wooden overlay is STILL present** — the user's insight: a pure white void is unnatural, so the model hallucinates an overlay (wooden table/floor) to fill the "empty" space. Giving it a **consistent colored watercolor scene** gives it something to hold onto instead of inventing an overlay. (b) the model **threw TWO paper planes** — now locked to ONLY ONE. (c) the **bubbles were too high and too many** — removed entirely (only a small splash when the figure enters the water).

### What changed (prompt v4, saved to `prompts/jaisal_single_shot_prompt_v4_watercolor.txt`)

1. **STYLE** changed from "strictly BLACK AND WHITE" to "2D line-art + minimal watercolor" — clean black ink lines for the figure/bridge + SOFT MINIMAL WATERCOLOR COLOR WASHES for the scene (soft muted colors, flat 2D, no heavy shading/3d/photorealistic).
2. **BACKGROUND SCENE LOCK** (replaces the pure-white void): a FIXED MINIMAL WATERCOLOR SCENE — stone bridge over a river, soft pale blue-grey sky, soft muted blue river, soft muted green bank + a couple of simple line trees. The SAME fixed scene across all 10 seconds. Explicitly forbids background change/shift/morph/new scene/wooden overlay/room/wall/table/indoor setting.
3. **PAPER PLANE - ONLY ONE** (new top-priority lock): there is ONLY ONE paper plane in the whole video, NEVER two, NEVER a second plane, NEVER multiple. The figure throws ONE plane and only that ONE exists.
4. **NO BUBBLES** (new top-priority lock): NO air bubbles, NO rising bubbles, NO bubble clusters, NO bubble pops, NO bubble-formed anything. When the figure enters the water there is only a small splash (a few line-art splash lines), NO bubbles.
5. Retained from v3: 10-second timeline, paper plane stays SMALL + IN THE AIR until 9.00s then floats on the water, visible wind lines, static eye-level MEDIUM camera, deep focus, the figure NOT-list.

### Note on the file shape

The ComfyUI UI re-saved `jaisal_single_shot.json` between turns (native shape: all `widgets_values` are STRINGS, `widgets_values_named` stripped). The v4 prompt was written to the POSITIONAL `widgets_values[0]` on BOTH instance node 105 AND internal subgraph node 104 (105==104 verified). Node 104's `length` was reset to a stale `73` by the re-save and was re-set to `243` (~10s). Node 105's length stays `10` (seconds). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Alternatives considered

- Keeping the pure white void with an even stronger "no overlay" negative (rejected — the user's insight is that the void ITSELF invites the overlay; a consistent colored scene is the real fix).
- A fully detailed/photorealistic colored background (rejected — the user wants a MINIMAL watercolor look, not a detailed scene).

### Result

`jaisal_single_shot.json` now uses a minimal watercolor bridge-and-river scene (colored, consistent), ONE paper plane, NO bubbles. **Rule: for the line-art title animation, do NOT use a pure white void (it invites a hallucinated overlay) — use a FIXED MINIMAL WATERCOLOR SCENE (bridge + river + sky + bank, soft muted colors) that is IDENTICAL across all seconds; lock the paper plane to ONLY ONE; and use NO bubbles (only a small splash).** **NEXT: run `jaisal_single_shot.json` (10s, 1344×768, turbo 4-step) and check (a) no wooden overlay, (b) ONE paper plane, (c) no bubbles, (d) the watercolor scene stays consistent.**


---

## D033 — Sketch title animation: the wooden/mica overlay is a "line-art = physical drawing on a surface" prior (NOT a wiring bug, NOT the reference)

Date: 2026-08-31
Status: Active

### Diagnosis (traced the ACTUAL workflow + reference, not guessed)

The wooden/mica overlay that keeps appearing "on top of the image" was traced to its real cause by inspecting the workflow wiring and the reference image:

1. **Wiring is CLEAN** — the reference image enters the model in exactly ONE way: `114 (LoadImage) → 105.0 (IMAGE)` as the i2v **first frame**. There is NO IPAdapter, NO reference adapter, NO latent blend, NO separate image-conditioning node. So the overlay is NOT being fed in by a hidden node (rules out GPT's hypothesis #3/#4).
2. **The reference image is CLEAN** — `sketch_00008_.png` background is genuinely pure white (mean RGB 253-255, warm-tone fraction 0.000, R-B = -0.0). No wood/mica in the reference. So the overlay is 100% MODEL-GENERATED.
3. **ROOT CAUSE: the "line-art on white = a physical drawing on a surface" prior.** The model sees line art on a white background and interprets it as a PHYSICAL DRAWING ON A SHEET OF PAPER, so it renders the *paper/surface* the sketch is "drawn on" (wood grain / mica / paper grain). That's why it appears "applied on top of the image" — it's the model rendering the surface the drawing sits on. No amount of "NO WOOD" fixes it because we never told the model the line art is NOT on a physical surface at all.

### Fix (prompt v5, saved to `prompts/jaisal_single_shot_prompt_v5_flat.txt`)

1. **FLAT 2D ANIMATION, NOT A PHYSICAL DRAWING** (new top-priority lock, placed FIRST): the line art is NOT drawn on paper, NOT a sketch on a sheet, NOT a photo of a drawing, NOT on a physical surface. NO paper, NO paper texture, NO paper grain, NO surface, NO mica, NO mica texture, NO wood grain, NO wooden texture, NO texture of any kind on the background. The background is a flat clean 2D watercolor scene, NOT a textured surface/sheet/table/floor.
2. **GPT's structural cleanup applied:**
   - **REFERENCE IMAGE ROLE** (new): `<Picture 1>` is used ONLY as a reference for Subject 1's CHARACTER DESIGN. DO NOT preserve/copy/reconstruct the environment/background/floor/walls/objects/textures from `<Picture 1>`. The reference is NOT a scene reference; the environment is generated independently from the text.
   - **ENVIRONMENT LOCK** (replaces the old `<Subject 2> fully_preserved` retention): the environment is a FLAT 2D WATERCOLOR scene generated from the text description ONLY, NOT derived from `<Picture 1>`. The SAME fixed scene across all 10 seconds. NO wood/mica/paper/surface/room/table.
   - **DROPPED the `retention_analysis` section** (it told the model to "preserve" the reference's environment, which is what pulled the overlay in).
3. Retained: 10s timeline, ONE paper plane (never two), NO bubbles, plane SMALL + in-air until 9.00s then floats on water, visible wind lines, static eye-level MEDIUM camera, deep focus, the figure NOT-list.

### Note

The ComfyUI UI re-saves `jaisal_single_shot.json` in native shape (all `widgets_values` are STRINGS, `widgets_values_named` stripped). v5 was written to the POSITIONAL `widgets_values[0]` on BOTH instance node 105 AND internal subgraph node 104 (105==104 verified). Node 105 length = `10` (seconds), node 104 length = `243` (frames, ~10s). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Alternatives considered

- Adding more "NO WOOD" negatives (rejected — the overlay is a surface prior, not a text-following failure; more negatives don't break the "drawing on paper" interpretation).
- Changing the reference image (rejected — the reference is clean; the problem is the model's prior, not the reference).
- A different workflow / conditioning node (rejected — the wiring is already clean; there is no hidden conditioning node to remove).

### Result

`jaisal_single_shot.json` now uses a FLAT 2D watercolor scene with an explicit "NOT a physical drawing / NOT on a surface" lock + GPT's reference-role/environment-lock structural cleanup. **Rule: when line-art i2v renders a wooden/mica/paper overlay "on top of" the image, the cause is the model's "line art = a physical drawing on a surface" prior — fix it by explicitly stating the animation is FLAT 2D and NOT a drawing on paper/surface, and by telling the model the reference is CHARACTER-DESIGN-ONLY (not a scene reference) so it doesn't preserve the reference's environment. Do NOT just add more "NO WOOD" negatives.** **NEXT: run `jaisal_single_shot.json` (10s, 1344×768, turbo 4-step, base `sketch_00008_.png`) and check (a) NO wooden/mica/paper overlay, (b) ONE paper plane, (c) no bubbles, (d) the flat watercolor scene stays consistent.**


---

## D034 — Sketch title animation: back to B&W line-art + water splash + smooth plane descent + title + 15s (wooden issue stays gone)

Date: 2026-08-31
Status: Active

### Decision

The single-shot i2v title animation (`jaisal_single_shot.json`) prompt is updated (v6, saved to `prompts/jaisal_single_shot_prompt_v6_bw_title.txt`) after the flat-2D fix (D033) successfully removed the wooden/mica overlay. Changes:

1. **Back to STRICTLY BLACK AND WHITE line-art** (removed the watercolor coloring from v4/v5) — the user wants it to match the plain 2D reference (black ink lines on a clean white background). The environment is now a FLAT 2D LINE-ART scene (stone bridge, clean white sky, river as scattered dots + wavy dashes, a couple of line trees), NOT colored.
2. **WATER SPLASH** — when the figure enters the water (10.00-11.00s), a small line-art splash (a few line-art splash lines). NO bubbles (kept).
3. **SMOOTH PAPER PLANE DESCENT** (fixes the "went down fastly / hovering near the water" problem) — the plane descends SLOWLY and GENTLY, gradually losing altitude over several seconds (11.00-13.00s), a smooth slow drift downward, NOT a fast drop, NOT a sudden fall, NOT hovering just above the water, NOT stopping near the water surface. It gently touches the water around 13.00s, then floats calmly.
4. **TITLE 'The Jaisal Cut' ADDED** (14.00-15.00s) — appears in clean line-art lettering (hand-drawn line letters, outlined, not filled), 'The' small / 'Jaisal' big / 'Cut' medium, spelled T-h-e J-a-i-s-a-l C-u-t. NO figure in the title shot. (D004 fallback: if the spelling comes out garbled, composite the title in post.)
5. **EXTENDED to 15 seconds** (was 10s) — instance node 105 `value_1` = `15` (seconds); internal subgraph node 104 `length` = `362` (frames = 17×21+5 on the 17k+5 grid = ~15.08s at 24fps).
6. **WOODEN ISSUE STAYS GONE** — the FLAT 2D ANIMATION, NOT A PHYSICAL DRAWING lock (D033) is RETAINED at the top, plus the REFERENCE IMAGE ROLE (character-design-only) + ENVIRONMENT LOCK (generated from text, not derived from `<Picture 1>`) structural cleanup. NO wood/mica/paper/surface texture.

### Reason

User: "we have achieved an amazing feat, that wooden thing is gone now. now i feel like we can remove the coloring part or we can give some splash of existing white and black because since our image starts from plain 2d, so some kind of splashing will feel good right? also, now the paper plane is floating in the air, but it went down fastly, i think asking it to stay in the air its straight away moving to the near bottom layer of water and staying upthere, which feel like not real or smooth flow. also we can now add our title the jaisal cut and increase the title animation to 13 or 15 seconds, mind you that we should not get the wooden issue again. lets do this and fix the production intro."

### What changed (prompt v6)

- STYLE: watercolor → STRICTLY BLACK AND WHITE line-art (matches the plain 2D reference).
- ENVIRONMENT: colored watercolor scene → FLAT 2D LINE-ART scene (clean white sky, river as dots + wavy dashes, line trees).
- WATER SPLASH added at the figure's entry (10.00-11.00s).
- PAPER PLANE DESCENT: fast drop / hovering near water → SLOWLY and GENTLY, gradually losing altitude over 11.00-13.00s, touches water ~13.00s, then floats.
- TITLE 'The Jaisal Cut' added at 14.00-15.00s (line-art lettering, 'The' small / 'Jaisal' big / 'Cut' medium).
- LENGTH: 10s → 15s (instance `value_1`=15, internal `length`=362 frames).
- RETAINED: FLAT 2D NOT A PHYSICAL DRAWING lock, REFERENCE IMAGE ROLE (character-design-only), ENVIRONMENT LOCK, ONE paper plane, NO bubbles, visible wind lines, static eye-level MEDIUM camera, deep focus, the figure NOT-list.

### Note

The ComfyUI UI re-saves `jaisal_single_shot.json` in native shape (all `widgets_values` are STRINGS, `widgets_values_named` stripped). v6 was written to the POSITIONAL `widgets_values[0]` on BOTH instance node 105 AND internal subgraph node 104 (105==104 verified). Node 105 length = `15` (seconds), node 104 length = `362` (frames, ~15s). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Alternatives considered

- Keeping the watercolor coloring (rejected — the user wants plain B&W to match the 2D reference).
- A fast plane drop (rejected — the user wants a smooth, realistic, gradual descent).
- 13s instead of 15s (chose 15s — the user said "13 or 15"; 15s gives the title its own full second and matches the original production length).

### Result

`jaisal_single_shot.json` is now a 15s B&W line-art title animation: walk → stop → look around → throw ONE plane → wait → jump (with a small splash) → plane descends SLOWLY and GENTLY → plane floats → title 'The Jaisal Cut' appears. The wooden/mica overlay stays gone (flat-2D lock retained). **Rule: for the line-art title animation — keep it STRICTLY B&W line-art (match the plain 2D reference), add a small water splash at the figure's entry, make the paper plane descend SLOWLY and GENTLY (not a fast drop, not hovering near the water), add the title 'The Jaisal Cut' in line-art lettering in the final second, and KEEP the FLAT 2D NOT A PHYSICAL DRAWING lock so the wooden/mica overlay does not come back.** **NEXT: run `jaisal_single_shot.json` (15s, 1344×768, turbo 4-step, base `sketch_00008_.png`) and check (a) NO wooden/mica overlay, (b) B&W line-art, (c) water splash at entry, (d) smooth slow plane descent, (e) title 'The Jaisal Cut' appears (if garbled, composite in post per D004).**


---

## D035 — Sketch title animation: REVERT v6 (B&W) → v5 watercolor (the working one) + 12s. LESSON: change ONE thing at a time.

Date: 2026-08-31
Status: Active

### What happened

v6 (D034) REMOVED the watercolor and went back to a pure-white B&W background, added the title, and extended to 15s — all at once. The user reported the wooden/mica overlay came BACK ("again the same issue... gpt fixed it and you ruined it again"). **Root cause of the regression: removing the watercolor re-introduced the pure-white background, which re-triggered the "line art on white = a drawing on a sheet of paper" prior (D033). The watercolor in v5 was actually PROTECTING against that — a colored background does not read as a paper sheet.** v6 also piled on the title + 15s, so the regression could not be isolated.

### Fix (prompt v7, saved to `prompts/jaisal_single_shot_prompt_v7_12s.txt`)

**REVERTED to the exact v5 prompt** (the one that gave "the wooden thing is gone") — i.e. the FLAT 2D watercolor scene + FLAT 2D NOT A PHYSICAL DRAWING lock + REFERENCE IMAGE ROLE + ENVIRONMENT LOCK + ONE paper plane + NO bubbles — and made ONLY these changes:
1. **Timeline extended 10s → 12s** (instance node 105 `value_1` = `12` seconds; internal subgraph node 104 `length` = `289` frames = 17×17+1 on the 17k+5 grid = ~12.04s at 24fps).
2. **Paper plane in-air until 10.00s** (was 9.00s), then descends slowly and floats in the final second (11.00-12.00s).
3. **Title NOT rendered by the model** — back to "composited in post" (D004). The title is added in post over the final frame, NOT asked of the model (avoids the garbled-spelling risk and keeps the prompt focused).
4. **NO title in the prompt** (removed the v6 title-rendering beat).

Everything else is IDENTICAL to v5. Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### LESSON (recorded because it was a real mistake)

**Change ONE thing at a time.** v6 changed the style (watercolor→B&W), added the title, AND changed the length simultaneously — when the result regressed, it was impossible to tell which change caused it. The style change (removing the watercolor) was the culprit. **Rule: when a prompt is WORKING (the wooden overlay is gone), do NOT change the style/background — only adjust the timeline/length. To add the title, composite it in POST (D004), do NOT ask the model to render it. The watercolor background is a PROTECTION against the "drawing on paper" prior — do NOT revert to a pure-white background.**

### Result

`jaisal_single_shot.json` is back to the WORKING v5 watercolor prompt, now at 12s, title composited in post. **NEXT: run `jaisal_single_shot.json` (12s, 1344×768, turbo 4-step, base `sketch_00008_.png`) and confirm the wooden/mica overlay stays GONE. Then composite the 'The Jaisal Cut' title in post over the final frame.**

---

## D036 — Sketch title animation: v8 = 14s, B&W first second → color fades in, plane lands in natural motion, title at end. Krea2 identity-edit title image.

Date: 2026-08-31
Status: Active

### What changed (prompt v8, saved to `prompts/jaisal_single_shot_prompt_v8_14s.txt`)

Built on the WORKING v7 (v5 watercolor + 12s). Changes:
1. **12s → 14s** (instance node 105 `value_1` = `14` seconds; internal subgraph node 104 `length` = `345` frames = 17×20+5 on the 17k+5 grid = ~14.375s at 24fps).
2. **First second (0.00-1.00) is STILL + PLAIN BLACK AND WHITE line art** (no color yet).
3. **From the second second (1.00) onward, COLOR FADES IN** — the watercolor colors (teal water, warm sand, green hills, blue sky) fade in smoothly over the first ~2 seconds while the figure starts walking. (User: "let the color change from the second second onwards.")
4. **Paper plane LANDS in NATURAL MOTION** (user: "let the paper plane land in normal motion, let it not wait or stay extra long in air, it feels unnatural"): thrown at 4.00s, flies in a NATURAL ARC (rises slightly, then descends in a smooth curve), LANDS on the water ~7.00s. Does NOT hover, does NOT stay in the air long.
5. **Title 'The Jaisal Cut' appears at 13.00-14.00** (line-art lettering, 'The' small / 'Jaisal' big / 'Cut' medium). NOTE: this is a RISK — diffusion is unreliable at spelling (D004). If the model garbles the title, composite it in post over the final frame instead.
6. **Retained from v5/v7**: FLAT 2D ANIMATION NOT A PHYSICAL DRAWING (top priority), watercolor background (the PROTECTION against the "drawing on paper" prior — D033/D035), REFERENCE IMAGE ROLE, ENVIRONMENT LOCK, ONE paper plane, NO bubbles, wind lines, static eye-level MEDIUM camera.

Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Krea2 title image (separate workflow)

`krea2_identity_edit.json` (Krea2 Identity Edit v1.2) set up to generate the TITLE image:
- Node 72 (LoadImage) = `FINAL_TITLE_REFERENCE.png` (the user's screenshot of the final frame, copied to `input\`).
- Node 84 (positive instruction) = `prompts/jaisal_title_instruction.txt` — adds 'The Jaisal Cut' in the SAME colored watercolor style ('The' small / 'Jaisal' big / 'Cut' medium), keeps the scene identical, NO figure.
- Node 85 (negative) = no figure, no text errors, no extra elements.
- Node 29 (SaveImage) prefix = `jaisal_cut/title_final`.
- ref_boost = 4.0 (fidelity dial), KSampler 10 steps cfg 1 (turbo), 16:9 2048×1152.
- The user runs this in ComfyUI (vision unavailable in the agent session).

### Plan (user's final direction)

1. Run `krea2_identity_edit.json` → title image (`jaisal_cut/title_final_*.png`).
2. Feed that title image to the MiniMax workflow as a reference (or use it as the final frame).
3. Run `jaisal_single_shot.json` (14s, 1344×768, turbo 4-step, base `sketch_00008_.png`) → colored video with the title.
4. Cut from ~1s to 14s (or first second to 14s) to get the colored video with the title.

### LESSON

**The watercolor background is a PROTECTION against the "drawing on paper" prior (D033/D035) — do NOT revert to a pure-white background.** The B&W first second is a TEMPORARY state (only 0.00-1.00s) before the color fades in; it is NOT a pure-white background for the whole video, so it should not re-trigger the paper-surface prior. **Change ONE thing at a time** (D035) — v8 changed the timeline + color transition + plane motion + title, so if it regresses, the title-rendering is the most likely culprit (drop it and composite in post).

---

## D037 — Krea2 identity-edit title workflow: added Typnosis_Krea2 typography LoRA (node 95, strength 5.0)

Date: 2026-08-31
Status: Active

### What changed

Added the **`Typnosis_Krea2.safetensors`** typography LoRA (457 MB, confirmed present in `E:\ComfyUI_windows_portable\ComfyUI\models\loras`) into `krea2_identity_edit.json` so the title 'The Jaisal Cut' renders with cleaner, more legible lettering.

**New node 95** (`LoraLoaderModelOnly`) inserted into the MODEL chain between the identity LoRA and the patch:
- Chain is now: `55 UNETLoader → 71 identity LoRA (krea2_identity_edit_v1_2 @1.0) → 95 Typnosis_Krea2 @5.0 → 79 Krea2EditModelPatch → 53 KSampler`.
- Node 95 `widgets_values` = `["Typnosis_Krea2.safetensors", 5.0]`.
- Rewired: link 2 (71→79) replaced by link 38 (71→95) + link 39 (95→79). Node 71 output → [38]; node 79 model input → 39.
- Updated the file-list note (node 100) to list both LoRAs.

**Strength 5.0** = the STR5 sweet spot from the earlier title-card work (D030-era: STR1-2 most prompt-faithful, STR4+ more stylized + compositions converge; STR5 = balanced-strong).

Validated `valid: true`, 0 errors (1 pre-existing harmless warning on node 79 `source_latent_b` — the optional second-reference latent input, bypassed by default).

### Tuning

- Title lettering too weak / not stylized enough → raise node 95 to 6.0-7.0.
- Title over-stylized / letters distort → lower node 95 to 3.0-4.0.
- Identity (face/scene) getting washed out by the typography LoRA → lower node 95, or raise node 71 (identity) strength.
- The identity LoRA (71) stays at 1.0 — it is the face/scene fidelity anchor; the typography LoRA (95) only shapes the LETTERING.

### Rule

**For a Krea2 title image, chain the identity LoRA (face/scene fidelity) + the Typnosis_Krea2 typography LoRA (lettering) in series on the MODEL path, identity first then typography, both feeding the Krea2EditModelPatch.** The typography LoRA at STR5 gives the cleanest legible title lettering without destroying the scene identity.

---

## D038 — Title composition: title ON THE RIVER WATER + paper plane RIGHT NEXT TO it (the perfect end)

Date: 2026-08-31
Status: Active

### What changed (user: "i want the text to be on the river, after the kid drowned, there i need my title and right next to it we will have our paper plane, that will be our perfect end to the production pipeline")

The final beat (13.00-14.00s) of the title animation is now a **calm water surface** where:
1. **The title 'The Jaisal Cut' floats ON THE RIVER WATER** (lower-center of the frame, on the water surface — NOT in the sky, NOT on the bridge), in clean line-art lettering ('The' small / 'Jaisal' big / 'Cut' medium, spelled T-h-e J-a-i-s-a-l C-u-t).
2. **The ONE SMALL paper plane floats RIGHT NEXT TO the title** (a small line-art paper plane on the river surface, close to the title).
3. **NO figure / NO person / NO kid** — the figure has already drowned and is GONE.
4. The title-on-water + the paper plane next to it are the ONLY things in the frame.

Applied to BOTH:
- **`jaisal_single_shot.json`** (MiniMax i2v) — the 13.00-14.00s beat + the summary line updated (both instance node 105 + internal subgraph node 104, 105==104 verified, 14s / 345 frames). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).
- **`krea2_identity_edit.json`** (Krea2 title image) — node 84 (positive instruction) updated to the SAME composition (title on the river water + paper plane next to it + NO figure). Saved to `prompts/jaisal_title_instruction.txt`. Validated `valid: true`, 0 errors (1 pre-existing harmless warning on node 79 `source_latent_b`).

### Why this is the "perfect end"

The story is: walk → throw plane → jump → **drown** → the water is calm → the **title appears on the water** with the **paper plane floating beside it**. The drowned figure is gone, so the final frame is a clean, quiet, symbolic ending (title + plane on still water) — no character, just the title and the plane. This is the closing image of the production pipeline.

### Rule

**The title animation ENDS on a calm water surface: the title 'The Jaisal Cut' floats ON THE RIVER WATER (lower-center) with the ONE paper plane floating RIGHT NEXT TO it, NO figure (already drowned).** Both the MiniMax i2v final beat AND the Krea2 title-image instruction must match this composition so the video's last frame and the Krea2 title image agree.

---

## D039 — Title SIMPLIFIED: title ON THE RIVER (like the paper plane), Typnosis LoRA BYPASSED. LESSON: do not complicate.

Date: 2026-08-31
Status: Active

### What happened (user: "this aint working, we dont need the lora, so i reduced the strength and bypassed it... we need the The jaisal cut to be on river, just like we have our paper plane, do not complicate this")

Two things:
1. **The Typnosis_Krea2 typography LoRA (node 95) is BYPASSED** (mode 7) in `krea2_identity_edit.json` — it was not helping ("this aint working"). The chain is effectively back to `55 UNETLoader → 71 identity LoRA @1.0 → 79 Krea2EditModelPatch → 53 KSampler` (node 95 stays in the graph, bypassed, so it can be re-enabled later if ever wanted).
2. **The title instruction was SIMPLIFIED** (node 84 + `prompts/jaisal_title_instruction.txt` + the v8 prompt's 13.00-14.00s beat + summary): the title 'The Jaisal Cut' floats **ON THE RIVER WATER, like floating in water**, lower-center, NOT in the sky / NOT on the bridge. Hierarchy: **'The' Small, 'Jaisal' (largest), 'Cut' Small** (was 'The' small / 'Jaisal' big / 'Cut' medium). The title is on the river **just like the paper plane is on the river** — the "paper plane RIGHT NEXT TO the title" complication was REMOVED. NO figure (already drowned, GONE).

Applied to BOTH `jaisal_single_shot.json` (nodes 105 + 104, 14s/345 frames, validated `valid: true` 0 errors) AND `krea2_identity_edit.json` (node 84, validated `valid: true` 0 errors).

### LESSON

**Do NOT complicate the title.** The user's mental model is simple: the title sits ON THE RIVER the same way the paper plane sits on the river — one calm water surface, the title floating on it. Adding extra elements (a plane "right next to" the title, size-hierarchy essays) made it worse. Keep the instruction SHORT and CONCRETE: title on the water, like the plane is on the water. **A typography LoRA is NOT needed for a simple line-art title on water — the identity workflow's own line-art style is enough; bypass the LoRA.**

---

## D040 — MiniMax title animation: TWO-FRAME (first-to-last) — figure (first) → title-on-river (last). Title image wired as last_frame.

Date: 2026-08-31
Status: Active

### What changed (user: "im good with the title image, lets update the prompt and wire the 2 images in our minimax workflow")

The MiniMax H3 node in `jaisal_single_shot.json` is `MiniMaxH3ImageToVideo` running on `minimax_h3_fl2va` (first-**last**-to-video) — it has BOTH a `first_frame` and a `last_frame` input. Previously only `first_frame` was wired. Now BOTH images are wired:

1. **FIRST FRAME** = `sketch_00008_.png` (the walking figure on the bridge, B&W line art) — LoadImage node 114 → node 105 slot 0 (`first_frame`, link 218). UNCHANGED.
2. **LAST FRAME** = `jaisal_title_final.png` (= the user's chosen title image `title_final_00015_.png`, copied to `input\`) — NEW LoadImage node 125 → node 105 slot 1 (`last_frame`, link 229).

**Prompt updated to a TWO-FRAME (first-to-last) structure** (`prompts/jaisal_single_shot_prompt_v8_14s.txt`, applied to both node 105 + internal node 104, 105==104 verified, 14s/345 frames):
- The old "REFERENCE IMAGE ROLE" section (which said `<Picture 1>` is character-design-only) was REPLACED with a **TWO-FRAME ANIMATION (FIRST-TO-LAST)** section: FIRST FRAME = `<Picture 1>` (figure on bridge, B&W), LAST FRAME = `<Picture 2>` (title 'The Jaisal Cut' on the river water, colored). The video animates SMOOTHLY from first to last. **The title in the last frame is EXACTLY the title image provided in `<Picture 2>` — do NOT alter its spelling, position, size, or style. The FINAL frame MUST match `<Picture 2>` exactly.**
- The summary line + the 13.00-14.00s final beat updated: the scene CONVERGES to the last frame (the title image), the figure is GONE (drowned).

Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120), 28 nodes.

### Why this is the right approach

**The title is now GUARANTEED to be exactly the user's title image** — the last frame is the image itself, so there is NO spelling risk (the D004 garbled-title problem is eliminated for the final frame). The model only has to ANIMATE the transition (figure → title on the river), not RENDER the title text. This is the "perfect end": the video ends on EXACTLY the title image the user approved.

### Rule

**For a title ending, use the MiniMax first-to-last (fl2va) node with BOTH frames wired: first_frame = the scene/figure image, last_frame = the approved title image. The prompt describes the two anchor frames + the transition, and explicitly says the final frame must EXACTLY match the last-frame image (do not alter its text/position/style).** This eliminates the title-spelling risk — the model animates TO the title, it does not render it.

---

## D041 — Audio: NATURAL SOUNDS ONLY (no instrumental music) — HARD RULE (user is Muslim, does not promote instrumental music)

Date: 2026-08-31
Status: Active

### What changed (user: "i am a muslim and i dont want to promote instrumental music in my videos, whether its a movie or title animation. lets use natural sound, footsteps, wind, water sound and birds sound thats it for the current video")

**HARD RULE (persistent, applies to ALL future videos/animations in this project): NO instrumental music, NO musical instruments, NO melody, NO beat, NO soundtrack, NO background music.** Only NATURAL ambient sounds.

Updated the `overall_soundscape` + `non_diegetic_music` sections of `prompts/jaisal_single_shot_prompt_v8_14s.txt` (applied to both node 105 + internal node 104, 105==104 verified, 14s/345 frames):
- **overall_soundscape** = NATURAL SOUNDS ONLY: soft footsteps on the stone bridge, a gentle continuous wind, the soft flowing river water, a few birds chirping in the distance (natural ambient), a soft whoosh as the plane is thrown, a soft plop as the plane lands, a soft splash as the figure jumps in, then a calm quiet hush with water + wind as the title appears. **NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO soundtrack (HARD RULE).** No dialogue, NO bubble pops.
- **non_diegetic_music** = NO music of any kind (HARD RULE - the creator does not promote instrumental music). ONLY natural ambient sounds: footsteps, wind, river water, birds. No dialogue, no subtitles.

Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Audio-only option (user asked "can we add the audio alone for a video?")

The MiniMax H3 node (`minimax_h3_fl2va`) generates video **WITH** audio as one unit — the audio is baked in at generation time, so the cleanest fix is to **re-run the video with the updated natural-sounds prompt** (what we just did). If the user has a GOOD video but only wants to swap the audio track WITHOUT regenerating the video, that is a separate post step (extract video track + mux a natural-sounds audio file onto it in a video editor) — but since the model generates the audio, re-running with the corrected prompt is the intended path. **Rule: for this project, ALWAYS specify NATURAL SOUNDS ONLY (footsteps/wind/water/birds) + an explicit NO-music HARD RULE in the soundscape; never allow instrumental music.**

---

## D042 — Audio for a LOCKED video via ControlFoley (comfyui-controlfoley-official), TC-V2A mode

Date: 2026-09-02
Status: Active

### Decision

To add a natural-sounds soundtrack to an ALREADY-LOCKED video (without regenerating it), use the **ControlFoley** custom node pack (`comfyui-controlfoley-official`, Xiaomi Research's video-to-audio model) in **TC-V2A mode** (video + text-guided sounds). The locked video is `Jaisal_Sketch_Title_00010_.mp4` (12.25s, 24fps, 1344×768).

### Workflow (`jaisal_sketch_title_audio.json`, built by `utilities/build_controlfoley_audio.py`)

Chain: `LoadControlFoleyModel` → `ControlFoleyGenerate` ← `LoadControlFoleyVideo`; `ControlFoleyGenerate` → `SaveControlFoleyAudio` (WAV) and → `MuxControlFoleyAudioToVideo` (mode `replace` → final MP4 with the new audio replacing the original).
- `LoadControlFoleyVideo` loads `input\jaisal_sketch_title_00010.mp4` (video staged there), duration 12.5.
- `ControlFoleyGenerate` prompt = the exact natural sounds in story order (footsteps on stone, gentle wind, low whistle, flowing river water, distant birds, soft whoosh as the plane is thrown, soft plop as it lands, soft whoosh as the figure jumps, soft splash as he lands, then calm water + low birds) + the D041 NO-music HARD RULE. `guidance_scale` 4.5, `num_inference_steps` `fixed`, `seed` 42, `clip/sync_batch_size_multiplier` 40.
- `MuxControlFoleyAudioToVideo` output = `controlfoley/jaisal_sketch_title.mp4`.

### Setup facts (verified 2026-09-02)

- Node pack installed at `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-controlfoley-official` (10 nodes: LoadControlFoleyDependencies/Model, ControlFoleyTorchCompile, LoadControlFoleyVideo, ControlFoleyGenerate/Advanced/SimpleGenerate, SaveControlFoleyAudio, MuxControlFoleyAudioToVideo, UnloadControlFoleyModel). Imports cleanly.
- **Missing pip deps installed** into the embedded Python: soundfile, librosa, laion-clap, open-clip-torch, nnAudio, torchdiffeq, torchlibrosa, julius, flashy, dora-search (imports as `dora`), submitit, treetable, retrying, num2words, spacy, colorlog, pillow.
- **The running ComfyUI (port 8188) was started BEFORE the node pack was installed → the ControlFoley nodes are NOT registered** (validation shows `unknown_class_type`). **A ComfyUI RESTART is required** for the nodes to load. ComfyUI is a portable install started manually (NOT under comfy-cli control), so the USER restarts it.
- **First run auto-fetches** the ControlFoley source tree (pinned revision, shallow git clone into `<ComfyUI root>/controlfoley`) and **downloads ~16 GB of weights** from Hugging Face (`YJX-Xiaomi/ControlFoley`: `weights/controlfoley.pth` + 4 `ext_weights/*`) into `ComfyUI/models/controlfoley`, plus third-party HF deps (CLIP ViT-H, BigVGAN, musicgen-style, roberta/bart/bert-base, MERT). If huggingface.co is slow, set `$env:HF_ENDPOINT="https://hf-mirror.com"` before starting ComfyUI.
- `LoadControlFoleyModel` widgets: `[controlfoley_source_dir, model_weights_dir, variant=large_44k, device=auto, precision=bf16, low_vram=False, compile_encoders=False, auto_fetch_source=True]`. Leave `model_weights_dir` = `path/to/model_weights` (auto-downloads). `low_vram=False` is REQUIRED for V2A/TC-V2A (low_vram keeps video encoders on CPU and disables them).

### Reason

The user locked the video (`Jaisal_Sketch_Title_00010_`) and wants to add a natural-sounds soundtrack WITHOUT regenerating it. ControlFoley TC-V2A generates sound effects that FOLLOW the visual content, guided by a text prompt — exactly the "footsteps + whistle + wind + whoosh + splash + birds" the user described. This is the audio-only post path from D041 (swap the audio track on an existing video).

### Alternatives considered

- Re-running the MiniMax video with the natural-sounds prompt (D041's intended path) — rejected here because the user has ALREADY locked the video and only wants the audio added.
- Manual audio in DaVinci Resolve — the user explicitly wants to do it with AI (ControlFoley) for this simple video.

### Rule

**For a locked video, add a natural-sounds soundtrack with ControlFoley TC-V2A: `LoadControlFoleyVideo` (the video) + `ControlFoleyGenerate` (natural-sounds prompt + D041 NO-music rule) → `SaveControlFoleyAudio` (WAV) + `MuxControlFoleyAudioToVideo` (replace → final MP4). The node pack needs a ComfyUI restart to register, and the first run auto-downloads ~16 GB of weights. ALWAYS keep the D041 natural-sounds-only / NO-music HARD RULE in the prompt.**

### Resolution (2026-09-03) — WORKS after 3 package-level bug fixes

The first run (job `6b490126`) HUNG 2h40m with no output. Root cause was NOT the workflow — it was 3 bugs in the laion-clap package + node pack, each revealed one layer deeper:

1. **Import-time `SystemExit(2)` (the hang).** `laion_clap/training/params.py` ran `parse_args()` at import time (via `hook.py` → `training.data`). Under ComfyUI, `sys.argv` = ComfyUI's launch args, so argparse raised `SystemExit(2)` (a `BaseException`, slips past `except Exception`), leaving the prompt stuck. **FIX:** `params.py` `parse_args()` → `parse_known_args()[0]`. Backup `params.py.bak_comfyfix`.
2. **CLAP `position_ids` unexpected key.** `laion_clap/hook.py:129` `load_state_dict(ckpt)` used `strict=True`, rejecting the audioset checkpoint's extra `text_branch.embeddings.position_ids` buffer. **FIX:** `load_state_dict(ckpt, strict=False)`. Backup `hook.py.bak_comfyfix`.
3. **BigVGAN `resume_download` missing arg.** The node pack's `_patch_bigvgan_from_pretrained` wrapper only injected `proxies`, but the installed `huggingface_hub` now requires `resume_download` (keyword-only). **FIX:** `nodes.py` `_compat_from_pretrained` now also `kwargs.setdefault("resume_download", False)`.

**All three are package-level (persist across restarts). A ComfyUI RESTART is required after patching `nodes.py` (imported at startup, cached in memory).** After the fixes, the job completed and produced `output\controlfoley\jaisal_sketch_title_00001_.wav` (1.03 MB) + `jaisal_sketch_title_00002_.mp4` (13.77 MB, audio muxed in, replace mode).

**Submit with NAMED inputs** via `utilities/submit_controlfoley.py` (the UI→API converter mis-maps `ControlFoleyGenerate`'s positional `widgets_values` — a hidden widget shifts them — so `run_workflow` fails validation; named inputs bypass it). See EXPERIMENTS.md 2026-09-03.

---

## D043 — ControlFoley `LoadControlFoleyVideo` resolves the video from the `input\` dir (stage it there first)

Date: 2026-09-03
Status: Active

### Decision

The `LoadControlFoleyVideo` node's `video_path` widget is a **relative filename resolved against the ComfyUI `input\` directory** (via `_resolve_path`, which tries `input\`, the node dir, the ComfyUI root, and cwd in order). It is NOT a path into `output\`. So to feed a generated video to ControlFoley, **copy it from `output\video\` into `input\` first**, then set the node's `video_path` to that filename.

### Reason

The user tried to run the audio workflow on the actual video `Jaisal_Sketch_Title_00011_` and got `FileNotFoundError: Input video not found: jaisal_sketch_title_00011.mp4`. Two mismatches: (1) the node looks in `input\`, but the video lives in `output\video\`; (2) the actual output filename is `Jaisal_Sketch_Title_00011_.mp4` (capitalized, with a trailing `_` before `.mp4`), while the node's widget held `jaisal_sketch_title_00011.mp4` (lowercase, no trailing `_`). The node has **no file-picker UI** — the filename is a plain STRING widget, so the user can't browse to the file; it must be staged + named to match.

### Alternatives considered

- Pointing `video_path` at the absolute `output\video\Jaisal_Sketch_Title_00011_.mp4` path (works — `_resolve_path` accepts absolute paths — but the staged `input\` copy is the established convention and keeps the workflow portable).

### Result

Staged `output\video\Jaisal_Sketch_Title_00011_.mp4` → `input\jaisal_sketch_title_00011.mp4` and set node 2 (`LoadControlFoleyVideo`) `widgets_values` = `["jaisal_sketch_title_00011.mp4", 15.0]` (duration 15.0 = upper limit; the video is 14.33s so the output follows the input length). **Rule: to change the ControlFoley input video, copy the desired `output\video\*.mp4` into `input\` and set the `LoadControlFoleyVideo` `video_path` widget to that filename (the node has no file browser). The `duration` widget is an upper limit, not the output length.**

---

## D044 — ControlFoley prompt: use a TIMED, video-synced sound design (not a flat list); put exclusions in the NEGATIVE prompt; align duration to the video

Date: 2026-09-03
Status: Active

### Decision

For ControlFoley TC-V2A (video→audio), the `ControlFoleyGenerate` `prompt` must be a **TIMED, beat-by-beat sound design synced to the video** (e.g. `0-2s: soft footsteps`, `2-3s: whistle + plane whoosh`, `6s: plane plop on water`, `9s: splash`, `11s onward: flowing water only`), NOT a flat un-timed list of ~10 sounds. The **NO-music / NO-noise exclusions belong in the `negative_prompt` widget**, not crammed into the positive prompt. And the `duration` widget must be **≥ the actual video length** (upper limit) so the tail is not cut.

### Reason

The first 00011 run came out as **static noise, no real sounds** (user: "the output have only static noise, no real sound we wanted"). Three causes: (1) the positive prompt was a **flat, un-timed list** of ~10 sounds with no temporal structure — a video-to-audio model needs to know WHEN each sound happens to sync it to the visuals; an undifferentiated blob of sound words degrades into incoherent noise. (2) the **NO-music/NO-instrument/NO-melody/NO-beat/NO-soundtrack exclusions were stuffed into the positive prompt**, adding conflicting signal. (3) the `duration` widget was **12.5 but the video is 14.33s**, so the last ~2s (the title at ~11s) was cut/misaligned.

### Alternatives considered

- Keeping the flat list but adding "synced to the video" (insufficient — still no per-second structure).
- Leaving the NO-music words in the positive prompt (rejected — they belong in the negative prompt, which is what that widget is for).

### Result

Rewrote node 3 (`ControlFoleyGenerate`) via `utilities/update_controlfoley_prompt.py`: (1) **timed prompt** matching the user's exact beat-by-beat (footsteps 0-2s → whistle+throw 2-3s → quiet 3-6s → plane plop 6s → jump whoosh 6-7s → land+second jump 7-8s → splash 9s → calm water 9-11s → flowing water only 11s+); (2) **negative_prompt** = `music, instrumental music, musical instruments, melody, beat, rhythm, soundtrack, song, dialogue, speech, talking, voice, loud sounds, harsh noise, distortion, static, electronic sounds, beeps, alarms`; (3) **duration 12.5 → 15.0** (upper limit; video is 14.33s). Re-ran via `submit_controlfoley.py` → `output\controlfoley\jaisal_sketch_title_00005_.wav` (14.35s, matches the video) + `jaisal_sketch_title_00006_.mp4` (muxed, replace). **Rule: ControlFoley TC-V2A prompts are TIMED and video-synced (per-second sound beats), exclusions go in the negative prompt, and duration ≥ video length. If a run comes out as static noise, the prompt is too flat/undifferentiated — add per-second timing and move the exclusions to the negative prompt.**

### Update 2026-09-03 (v2 — NO-WATER A/B test)

The v1 timed prompt STILL came out as a continuous noise bed. **Hypothesis (user): the CONTINUOUS water/wind descriptions make the model fill the whole timeline with a water-noise bed that masks the discrete action sounds.** **v2 (`utilities/update_controlfoley_prompt_v2.py`):** removed ALL continuous water/wind beds — the prompt now has ONLY the discrete action sounds (footsteps, whistle+throw, plane plop, jump whoosh, land thud+second jump, splash) + an explicit "background is QUIET - no continuous water/wind/ambient bed" line; the NEGATIVE prompt also suppresses continuous water/wind (`continuous water, flowing water, river sound, water ambience, constant water, white noise, hiss, constant ambient, continuous wind, wind bed`). Re-ran → `jaisal_sketch_title_00007_.wav` + `jaisal_sketch_title_00008_.mp4`. **Rule: if a ControlFoley run is a continuous noise bed, the CONTINUOUS ambient descriptions (water/wind) are the likely culprit — describe ONLY the discrete action sounds, explicitly say the background is quiet, and put continuous-water/wind in the negative prompt. If it's STILL noise after that, the problem is elsewhere (raise `guidance_scale` 4.5→6, try a different `seed`, or the model is weak at this video→audio task).**

### Update 2026-09-03 (v3 — SOURCE AUDIO NOT THE ISSUE; CONTROLFOLEY UNSUITABLE FOR LINE-ART VIDEO)

The v2 no-water prompt STILL came out as a flat noise bed (user: "still the same, there is no sound for the actions we mentioned either, and the noise sound is there, first it should make this video soundless or should we make it? maybe thats the issue?"). **Diagnosis (measured, not guessed):** (1) **The source video's audio is NOT used by ControlFoley** — the `LoadControlFoleyVideo` node outputs `{"path", "duration"}` (file path + duration, NO audio track); the `ControlFoleyGenerate` node's `video` input is that dict, and its `video_input` (VIDEO) and `images` (IMAGE) inputs are NOT connected. The node conditions on the video's FRAMES (CLIP video features — `clip_batch_size_multiplier` = "frames per CLIP encoder call"), not its audio. **Proof:** stripped the audio from `input\jaisal_sketch_title_00011.mp4` (ffmpeg `-an -c:v copy`) and re-ran → the output `jaisal_sketch_title_00009_.wav` is **byte-for-byte identical** to the previous run (same per-second RMS ~-24 dB, same spectral centroid 5938 Hz, same peak/RMS ratio 10.88). (2) **The real cause: ControlFoley is NOT extracting the action sounds from this 2D line-art video.** The output is a **completely flat ~-24 dB broadband noise bed across all 14 seconds** (spectral centroid 5938 Hz = bright noise) — the model is NOT generating the footsteps/whistle/splash, it's just outputting a steady noise floor. The likely cause: **ControlFoley is trained on realistic video, but the video is a 2D line-art stick-figure animation** — it gives the CLIP video encoder almost no realistic visual cues to condition on, so the model falls back to a generic noise bed. **This is a fundamental limitation: ControlFoley is not suitable for 2D line-art video.** **Options:** (a) **Keep the MiniMax-generated audio** already in the video (it was generated with the natural-sounds prompt — footsteps, whistle, wind, water, birds, whoosh, splash — so its baked-in audio IS the natural-sounds track; simplest path); (b) **Generate action sounds separately** (text-to-audio / SFX library) and sync them manually in a video editor (more control, more work); (c) **ControlFoley is not suitable for this line-art video** — it's designed for realistic video, not 2D animation. **Rule: if a ControlFoley run on a stylized/line-art video produces a flat noise bed (not the action sounds), the video is too stylized for the model — the CLIP video encoder can't extract action cues from 2D animation. Keep the source video's own audio (if it's good) or generate the action sounds separately. Do NOT waste time tweaking the ControlFoley prompt for a line-art video.**

### Update 2026-09-03 (v4 — TEXT-ONLY MODE ALSO A NOISE BED; CONTROLFOLEY NOT SUITABLE)

The user wants a REUSABLE production workflow (strip audio + generate SFX alone) and asked to build the text-only ControlFoley path. **Built `jaisal_sketch_title_audio.json` in TEXT-ONLY mode** via `utilities/build_controlfoley_textonly.py` (backed up the video-mode version to `workflow_backups\jaisal_sketch_title_audio_video_mode.json`): removed the Node 2→Node 3 link (video no longer feeds the generator), set Node 3's `video` input link to None, updated the prompt to a clean text-only SFX timeline (no "synced to the video"), duration 14.5. Node 2 (LoadControlFoleyVideo) still feeds Node 5 (mux) so the SFX gets muxed into the soundless video. **Re-ran → `jaisal_sketch_title_00011_.wav` + `jaisal_sketch_title_00012_.mp4`.** **Result: STILL a noise bed** — per-second RMS ~-29 to -34 dB (quieter than video mode's -24 dB but still flat), spectral centroid 6489 Hz (bright/noisy), peak/RMS 14.44. **Text-only mode did NOT produce clean discrete SFX (footsteps/whistle/splash) — it's still a broadband noise floor.** **CONCLUSION: ControlFoley is NOT suitable for clean SFX generation for this content, in EITHER video mode OR text-only mode.** It consistently produces a noise bed. **The reusable text-only workflow is still a valid production item** (the wiring is correct and reusable for other videos), but ControlFoley's SFX quality is the limitation. **Next options for clean music-free SFX:** (a) **Music separation** on the MiniMax audio (Demucs/Spleeter — NOT installed) to remove the music and keep the natural SFX (the MiniMax audio already has the natural SFX synced to the video, just mixed with music); (b) **Manual SFX** in a video editor (reliable, "old way"); (c) a different SFX-generation tool. **Rule: ControlFoley (video + text-only) produces a noise bed for this line-art video — do NOT keep burning compute on it. For clean music-free SFX, try music separation on the source audio or manual SFX.**

---

## D042 — SLA (Sparse Linear Attention) is the actual H3 speed stack; 1MP < 240 s

Date: 2026-09-01
Status: Active

### Decision

The MiniMax H3 speed stack in all production workflows is **SLA (Sparse Linear Attention)** via the **`H3SLAAttention` node** from `ComfyUI-PlagueKind-Nodes/ComfyUI-H3-SLA-Attention`. With SLA wired in, a **1MP (1344×768) H3 render completes in UNDER 240 seconds (~4 min)** — NOT the 25–40 min full-attention estimate in D026.

### Reason

The user's production workflows (`jaisalproduction1.json`, `jaisal_2mp_test.json`, `beach_sprint_test.json`, `t2v_beach_sprint_test.json`) all wire `H3SLAAttention` (node id 150). Config in use: `widgets_values = [0.9, '32', 8192, 1, True, True, '0', 'comfy_kitchen', True, False, False]` → **sparsity 0.90, dense_backend = `comfy_kitchen_int8`**. The user measured 1MP generation at **< 240 s** on this stack.

### Alternatives considered

- Quoting the D026 25–40 min figure (rejected — that is full-attention H3; SLA is in the graph and is far faster).
- VDN-H3 (Video Delta Net) — a different hybrid-attention speedup; **deferred to a later step** (see D043). VDN 8-step turbo REPLACES the community turbo LoRAs and adds ~4.3 GB VRAM; it is a separate setup to benchmark against SLA, not a drop-in.

### Result

**Rule: when estimating MiniMax H3 render time on THIS machine, use the SLA stack — 1MP ≈ < 240 s. Do NOT quote 25–40 min (that is full-attention). The 2K VRAM-thrashing caveat from D026 still applies (SLA speeds attention but not 2K activation/VRAM pressure). When comparing speedups (e.g. VDN), benchmark against the SLA < 240 s baseline, not the 25–40 min figure.**

---

## D043 — Two new workflows ready: Face Detailer (close-ups) + SAM character/background swap

Date: 2026-09-01
Status: Active (installed; pending ComfyUI restart to register nodes)

### Decision

Two workflows are now installed and model-path-remapped for use in ~1–2 weeks (once the audio/dubbing path is settled):

1. **Face Detailer** — `WF-H3_zuanfilm-Face_Detailer.json` (close-up / face-refine shots). Node pack = **`Carasibana/ComfyUI-H3-FaceRefine`** (cloned into `custom_nodes`). Defines `H3FaceSelect`, `H3FaceTrackCrop`, `H3FaceStitch`, `H3InjectVideoLatent`, `H3PerFrameDenoise`, `H3FaceMaskSAM`, `H3FaceTransformInfo`. Chain: `VHS_LoadVideoPath` → `H3FaceTrackCrop` (per-frame face crop, 512² canvas, `auto_capped_768`, crop_factor 0.35) → `MiniMaxH3ReferenceToVideo` → `H3InjectVideoLatent` (real frames → img2img) → `MiniMaxH3NativeAudioLock` (audio→lipsync) → `H3PerFrameDenoise` (0.8→0.35 by face size) → `er_sde` 4-step / denoise 0.45 → `VAEDecode` → `H3FaceStitch` (face_only, feather 24px) → `VHS_VideoCombine`. Key dials: base denoise 0.45, crop_factor 0.35, canvas `auto_capped_768`, turbo LoRA @ 0.75, `paste_region=face_only`.
2. **Character / Background swap** — `minimax_h3_sam_r2v_cinematic.json`. Node pack = **`yujianvip/ComfyUI-SetGet-Resolver`** (cloned; pure frontend `GetNode`/`SetNode`, right-click canvas). Chain: `VHS_LoadVideoFFmpeg` (driving video) → `SAM3_VideoTrack` (person, thr 0.5) → `SCAIL2ColoredMask` → `ImageInvert` → `ImageAddNoise` → `ImageCompositeMasked` → `MiniMaxH3ReferenceToVideo` (refs = character sheet, masked video as `ref_video`) → `CreateVideo` → `VAEDecode` → `SaveVideo` (+ `RTXVideoSuperResolution` 2× ULTRA). `ComfySwitchNode` toggles Char Replace (True) / Background Replace (False). Prompt = "omni" structure (subject_definitions, summary `[video editing]`, integrated_multimodal_description, overall_soundscape with dialogue `<Subject 1> says <d>[Language] transcript</d>`, non_diegetic_music).

### Reason

The user wants close-up shots (face detailer) and character/background swap (SAM R2V) available as reference/build-on-top workflows for the Malayalam channel intro. Both were sourced from the community (reddit) and needed their model paths remapped to our layout.

### Model-path remaps applied (backups saved as `*.pre-remap.bak`)

- **SAM R2V** (7 nodes): UNET `minimax_h3_fl2va_pruned_int8_convrot.safetensors`; LoRA `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`; video VAE `minimax_h3_video_vae_fp16.safetensors`; audio VAE `minimax_h3_audio_vae_fp32.safetensors`; CLIP `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`; SAM3 `sam3.1_multiplex_fp16.safetensors`; the NSFW `MysticXXX_MMH3-V3` LoRA (strength 0, no-op) repointed to the valid turbo LoRA so validation passes.
- **Face Detailer** (2 nodes): LoRA `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`; UNET `minimax_h3_fl2va_pruned_int8_convrot.safetensors`. (Detector `bbox\face_yolov8m.pt` already matched our `models/ultralytics/bbox/` layout.)
- **FaceRefine pip deps** installed into embedded Python: `insightface`, `scenedetect>=0.7` (`ultralytics` + `scipy` were already present).

### Validation status

- **SAM R2V** validates with all model paths resolving. Only error = node 153 source video (`scene_13_begging_clip01_trimmed.mp4` not in our `input/`) — user-specific driving clip. Two non-blocking warnings (SAM3 type-annotation on node 182; dangling `VAEDecodeAudio` node 121 in the original).
- **Face Detailer** reports the 4 H3Face nodes as `unknown_class_type` — these resolve **after a ComfyUI restart** loads the newly-cloned FaceRefine pack. 5th error = node 8 source audio (`GATONIEL_2.wav`), user-specific.

### Result

**Rule: the two packs are cloned into `custom_nodes` and both workflows' model paths point at our real files. A ComfyUI restart is REQUIRED for the H3Face nodes to register (verify `H3FaceTrackCrop`/`H3FaceStitch`/`H3InjectVideoLatent`/`H3PerFrameDenoise`/`GetNode`/`SetNode` appear in `/object_info` after restart). The source video/audio widgets are user-specific placeholders — set them to the actual clip before running. VDN-H3 setup is DEFERRED to a later step (benchmark VDN vs the SLA < 240 s baseline).**

---

## D045 — NEVER run a ComfyUI workflow while a Qwen/llama.cpp session is active (contaminates benchmarks)

Date: 2026-09-06
Status: Active (HARD RULE)

### Decision

**Never submit a ComfyUI workflow (via MCP `run_workflow`/`run_template` or the UI) while a local Qwen/llama.cpp session is running.** The two compete for the same GPU + CPU + memory, so BOTH slow down: the LLM's reasoning gets sluggish AND the ComfyUI render gets slower. Any generation time measured under this contention is **contaminated and unusable** for a speed comparison.

### Reason

The user's explicit instruction (2026-09-06): "you should never run the workflow parallely when an active qwen session is going on, it will affect both the usecase, your thinking will get slow, comfyui will also be slow." This was triggered when the VDN-H3 t2v benchmark (1MP, 124 frames, 8 steps) was submitted while Qwen was active and came back at **418.22 s** — a number the user correctly judged unusable ("from this, I cannot come to a conclusion"). The 418 s is NOT a valid VDN figure.

### Alternatives considered

- Running the benchmark anyway and noting the caveat (rejected — the user wants a clean number to compare against the SLA < 240 s baseline, D042).
- Reducing the workload to fit under the contention (rejected — still contaminated).

### Result

**Rule: before submitting ANY ComfyUI workflow for a timed/benchmark run, confirm no Qwen/llama.cpp session is active (stop it first). For benchmark comparisons (VDN vs SLA, etc.), the run MUST be done with the LLM idle so the time is clean. If a run was submitted during an active LLM session, discard its timing and re-run clean. The user will run the VDN benchmark manually (workflow `vdn_h3_t2v_benchmark.json`) to get the correct number.**

### VDN-H3 setup state (recorded 2026-09-06)

- **Node pack:** `Saganaki22/ComfyUI-VDN-H3` **v1.4.0** cloned into `custom_nodes` (no new Python deps — runs on ComfyUI's existing torch + safetensors). Defines `ApplyVDNH3` (simple) + `ApplyVDNH3Advanced` (ablations + fast kernels).
- **Checkpoint (int8 ConvRot 8-step stage):** `E:\ComfyUI_windows_portable\ComfyUI\models\vdn\vdn-minimax-h3-int8-convrot-comfyui\` (source `drbaph/vdn-minimax-h3-int8-convrot-comfyui` on HF). 7 files, ~3.49 GB total: `model_spec.json` (25,705 B), `linear_branch/model_int8_convrot_comfyui.safetensors` (2.30 GB), `linear_branch/config.json`, `adapters/turbo/adapter_model.safetensors` (851 MB) + config, `adapters/default/adapter_model.safetensors` (334 MB) + config. All verified byte-for-byte against the HF API.
- **Why int8 ConvRot (not bf16 `OpenVDN/vdn-minimax-h3`):** (1) matches our int8_convrot base model; (2) ~4.7 GB more VRAM headroom (8.3 GB free vs 3.6 GB — critical for the ~20 GB base + VAEDecode spike on the 32 GB card); (3) ~1.2× faster (branch matmuls 2.7× faster); (4) smaller download (2.2 vs 4.3 GB); (5) identical output at same seed. bf16 is the fallback if int8 misbehaves.
- **Benchmark workflow:** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\vdn_h3_t2v_benchmark.json` — validates clean (16 nodes, 0 errors). Chain: UNETLoader(`minimax_h3_fl2va_pruned_int8_convrot`) → `ApplyVDNH3Advanced` → `MiniMaxChunkFeedForward`(2, 4096) → BasicGuider → SamplerCustomAdvanced; BasicScheduler also takes model from the chunk node. `ApplyVDNH3Advanced` widgets: `["vdn-minimax-h3-int8-convrot-comfyui", true, 1, 1, "merge", "auto", "auto", true, "grouped", 1, 5, "both", true, true, false]` (turbo ON, **merge** required for the 8-step DMD stage, **fast_kernels OFF** — README warns it drifts on 8-step DMD on torch 2.10). **14 s = 345 frames** (14×24=336, snapped up to the 17k+5 grid → 345) at **1344×768 (1MP)** — set to match the PROVEN production workload `jaisal_single_shot.json` (14 s @ 1344×768 @ turbo, the workload the SLA ~250 s number was measured on) so the speed comparison is apples-to-apples. 8 steps, `er_sde`, `beta` scheduler, fixed seed 981445682258077. t2v mode (no first/last frame). NO-music prompt (D041).
- **Run 1 (contaminated):** 124 frames (5 s), 418.22 s — INVALID (Qwen was active). Discarded.
- **Run 2 (clean, 345 frames / 14 s / 1344×768):** **OOM at step 0** (184.21 s to fail). The linear-branch readout (`branch.py:159 frame_statistics`: `torch.matmul(vb.transpose(-1,-2), kf).float()`) holds per-frame K/V statistics for all F=102 frames in fp32 → ~31.4 GiB, blowing the 31.84 GiB limit. The vendor's ~95 s reference is 61 frames (F≈19) — 5× fewer frames.
- **CONCLUSION: VDN-H3 is NOT viable at our production scale (14 s / 1MP) on the 32 GB card — it OOMs.** Its linear-branch memory scales with frame count (worse for longer clips — the opposite of where we need it). **SLA remains the default speed stack (D042).** Do NOT adopt VDN for 14 s / 1MP production clips.
- **If a clean VDN number is still wanted (tomorrow):** set `branch_weights="stream"` (widget idx 5) + `retain_buffers="off"` (idx 6) to cut linear-branch memory, and/or drop to 124 frames / 1280×736. Stop the Qwen session first (D045). Full details in `EXPERIMENTS.md` (2026-09-06 VDN-H3 entry).

## D046 — Intro-video pipeline: character consistency via ComfyUI-Continuity (no LoRA), 2K via SeedVR2 TensorRT Studio, Semantic Bridge = i2v-only

Date: 2026-09-06
Status: Active (research conclusions — do NOT re-research)

### Decision

For the **channel-intro monologue video** (natural face, close-up + medium shot, the user's own voice), the pipeline is:
1. **Character consistency WITHOUT a LoRA → `ComfyUI-Continuity`** (`roadmaus/ComfyUI-Continuity`, renamed from `ComfyUI-MiniMax-Creator`). Cast-based, `@`-references, drift guard, **supports MiniMax H3, fully local**, no pip install. This is the Reddit approach the user found.
2. **Generate → the SLA i2v workflow** (`jaisal_single_shot.json`, ~200 s, D042).
3. **Upscale to 2K → `VRGDG-SeedVR2-TensorRT-Studio`** (`github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio`) — a **standalone Windows app** (NOT a ComfyUI node): one-click `Install SeedVR Studio.bat` + `Launch SeedVR Studio Pro.bat`, drop the video in, render 2K. **~8 min for an 8 s clip → 2K on the RTX 5090** (7B Sharp FP16). Run it AFTER ComfyUI generation.
4. **Audio** (today's main goal).

### Reason

- **Upscaler:** `RTXVideoSuperResolution` (installed + registered) is FAST but does NOT add detail / natural look (user-confirmed limitation). SeedVR2 TensorRT Studio is the fully-local path that ADDS detail and is still fast (~8 min/8 s/2K on the 5090).
- **RefMods / `.char` (malcolmrey/minimaxh3, `ComfyUI-MiniMaxH3Mod` pack, `MiniMaxH3RefModsLoader`+`MiniMaxH3RefModApply`, `models/refmods/`):** these are **pre-encoded reference-latent adapters (~1.5 MB each), ZERO-TRAINING, instant-load** — NOT a LoRA, NOT a dataset. **BUT the public ones are for OTHER people's characters (celebrities); there is NO clear public tool to create one for OUR OWN character → DEAD END for our boy.** (Answer to the user's "is this for training our own dataset or LoRA?" = **neither**.)
- **Semantic Bridge (`speach1sdef178/MiniMax-H3-Semantic-Bridge`):** a conditioning-space adapter that improves prompt adherence. **SCOPE: i2v/FL2VA (text-conditioned) ONLY — does NOT work for Ref2VA/reference-conditioned (R2V) workflows** (model card: "Ref2VA / reference-conditioned workflows are not supported"). So it helps `jaisal_single_shot.json` (i2v) but NOT `jaisalproduction1/2.json` / `jaisal_lowangle.json` (R2V). Installed: pack `custom_nodes\MiniMax_H3_Semantic_Bridge` + adapter `E:\comfyUi_latest\...\models\semantic_bridge\MiniMaxH3_SemanticBridge_v1.safetensors`. Wired into a SEPARATE `jaisal_single_shot_semantic.json` (bridge node 300 on the conditioning path, alpha 0.10, per_token); the working `jaisal_single_shot.json` was RESTORED clean (backup `workflow_backups\jaisal_single_shot.pre_semantic_bridge.json`).
- **FastVideo-FastH3 (t2v) = NOT a fit:** t2v-only (FL2VA/Ref2VA not distilled), built for 4×B200 datacenter GPUs in the FastVideo runtime (not ComfyUI), needs the VSA-H3 backend. Our SLA + turbo LoRA already does 4-step t2v at ~200 s on one card.

### Alternatives considered

- **RefMods for our own character** (rejected — no public tool to create a RefMod for a custom character; only celebrity ones exist).
- **RTX upscaler for 2K** (rejected as the primary — fast but no detail/natural look; keep as the quick-preview option).
- **Semantic Bridge on the R2V production workflows** (rejected — not supported for reference-conditioned generation).

### Result

**Rule: for the intro video — character consistency via ComfyUI-Continuity (no LoRA), generate via SLA i2v, upscale to 2K via SeedVR2 TensorRT Studio (local), then audio. Semantic Bridge is i2v-only. RefMods are a dead end for our own character. FastVideo-FastH3 is not a fit.**

### GOTCHA (two ComfyUI instances)

The **running** ComfyUI is the **`comfyUi_latest`** instance — its models dir is `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models`, NOT the main `E:\ComfyUI_windows_portable\ComfyUI\models` path. **Put models in the `comfyUi_latest` path or you get "Missing Models".** (This is why the Semantic Bridge adapter first showed "Missing Models" — it was in the main path.)

---

## D047 — Character voices: create our own via a small curated reference set (timbre swap, not TTS)

Date: 2026-09-06
Status: Active (reference-sourcing approach pending user confirmation)

### Decision

For the 15-character bilingual movie, do NOT rely on 15 friends' voice messages. Instead **create our own character voices** by curating a small set of DISTINCT reference voices (~4–6: young male, older male, young female, older female), assigning one per character (similar characters can share a voice type), and cloning each character's lines onto their reference via **voice conversion (timbre swap)** — OpenVoice V1 (zero-shot, validated 2026-09-06) for quick tests, RVC/GPT-SoVITS for final quality. The user dubs ALL characters (Malayalam + English) in their own voice; only the timbre is swapped.

### Reason

- The user dubs well and wants to dub almost all characters themselves; a timbre swap keeps their performance (pace/emotion/expression = the acting) and only changes the voice color → **non-robotic by design** (the dub is the "soul", the reference only provides the color).
- 15 distinct friends' voices is hard to source and hard to keep consistent; a small curated set is easier to manage and consistent (same reference for all of a character's lines).
- Female voices are just a female reference sample — same pipeline, nothing special.
- The OpenVoice two-way test (prem↔jaisal) came out GOOD (user-confirmed), validating the zero-shot VC path.

### Alternatives considered

- **15 friends' voice messages** (rejected — hard to source, consistency risk, user prefers to dub all).
- **TTS per character (IndicF5/Svara)** (fallback only — TTS is less "the user's performance"; use for characters with no reference or if VC underperforms).
- **Reference sourcing:** (a) record real samples [CHOSEN 2026-09-07 — from VOICE NOTES]; (b) TTS speaker profiles as references (no recording, synthetic base); (c) public datasets (licensing caveats).

### UPDATE (2026-09-07) — reference source = voice notes

The user chose **(a) real samples from voice notes** (WhatsApp/Telegram .ogg/.m4a). Voice notes are PROVEN (the first successful test used two Opus voice notes). Collection pipeline built + tested: `collect_references.py` (batch-clean a folder of voice notes → 16 kHz mono reference files) + `convert_character.py` (per-character dub→reference-voice conversion). See `AUDIO_PIPELINE_PLAN.md` (VOICE STRATEGY section).

### Result

**Rule: create our own character voices from a small curated reference set (male/female/old/young) + the user's dubs + timbre-swap VC (OpenVoice now, RVC/GPT-SoVITS final). More/cleaner reference samples (30 s–1 min mono) = better, more consistent results. Same reference for all of a character's lines.** See `AUDIO_PIPELINE_PLAN.md` (VOICE STRATEGY section).

## D048 — OpenVoice timbre-swap: clean SOURCES + multi-clip reference (no music, no TTS base)

Date: 2026-09-07
Status: Active (v3 Malayalam fix built + run; user to listen)

### Decision

For OpenVoice timbre-swap to produce NATURAL, non-robotic output, the **SOURCE** must be clean speech and the **REFERENCE** must be a list of short clean clips:

1. **Multi-clip reference (not one long file):** pass the individual clean reference clips as a LIST to `extract_se` (per-clip embedding, then averaged). Never one long concatenated file — the `ref_enc` encoder was trained on short coherent utterances, so a 158 s heterogeneous blob → one blurry embedding → output stays close to the source with a muddy tint ("robotic / forcing a different audio").
2. **Clean source (no music):** movie/source audio with a music bed → run **Demucs** `--two-stems=vocals` FIRST, then convert the clean vocals. Timbre-swap keeps the source's CONTENT and only swaps the voice color, so a music bed comes through as HUMMING.
3. **No TTS base for natural lines:** for a natural English line, use a REAL human dub as the source (not MeloTTS). `convert()` keeps the source PROSODY and only swaps color → a robotic TTS base = robotic output.

### Reason

- The good prem↔jaisal test (user-confirmed) used a single ~6 s clean clip → clean embedding → good result. The bad Jaisal test used a 158 s concatenated reference → blurry embedding → robotic.
- Spectral analysis (`scripts\analyze_source.py`) confirmed the movie clip `reference.ogg` has a music bed (flatness 0.0132, RMS std 2.6 dB) → the "only humming" in the v2 output.
- MeloTTS base is robotic (centroid 2600 Hz, flatness 0.067) → "foreigner speaking".

### Alternatives considered

- **One long concatenated reference** (rejected — blurry embedding).
- **MeloTTS base for English** (rejected for natural lines — robotic prosody).
- **Convert movie audio directly** (rejected — music bed → humming).

### Result

**Rule: for OpenVoice timbre-swap — (1) multi-clip reference as a LIST, (2) Demucs `--two-stems=vocals` on any source with music, (3) real human dub (not TTS) for natural lines.** Tools: `scripts\convert_multi_ref.py`, `scripts\english_test_multi.py`, `scripts\analyze_source.py` (diagnostic). v3 Malayalam output: `03_audio_processed\ml_reference_vocals_in_jaisal_v3.wav` (clean, no humming). See `AUDIO_PIPELINE_PLAN.md` (JAISAL VOICE TEST v3 section).

## D049 — Malayalam words: IndicF5 TTS (correct words) + OpenVoice (voice color); OpenVoice alone CANNOT do Malayalam words

Date: 2026-09-08
Status: Active (IndicF5 test in progress; batch Jaisal→Midhun done)

### Decision

OpenVoice is an **English-centric timbre swap** — it does NOT understand Malayalam words, it only swaps voice color in the frequency domain. For Malayalam (retroflex consonants, allophonic variations, complex consonant combinations), that swap **distorts the phonemes** → the voice changes correctly but the WORDS get mangled. **Flipping the conversion direction does NOT fix this** (it's a tool limitation, not a direction issue).

**The fix:** use **IndicF5** (Malayalam-native TTS, proper G2P) to generate the words CORRECTLY first, then **OpenVoice** to swap the voice color. Pipeline: user dubs line → `clean_audio.py` → Whisper transcribe → IndicF5 speaks the text in the character's voice (Malayalam) / OpenVoice or GPT-SoVITS (English).

**Best-option recommendation (production house):**
1. **IndicF5 = Malayalam workhorse** (only Malayalam-native tool we have; zero-shot `model(text, ref_audio, ref_text)` = correct words + character voice).
2. **GPT-SoVITS = English workhorse** (production-ready, zero-shot + few-shot; Malayalam support uncertain — test before committing).
3. **Main character (user) = use clean dub directly** (no conversion = highest quality).

**Reference sourcing:** Midhun's audio (`D:\voice_notes\mithun_audio\`, 3 EN + 2 ML, comprehensive) is the current test reference. **Prem audio CANNOT be used** (no permission). The user's **52-letter idea** (record 5 files covering all 52 Malayalam letters per character) gives a more complete voice embedding → better conversion.

### Reason

- User confirmed (2026-09-08): "the voice is good, we can see change, but the wordings are not correct... the dialogue lacks the perfection of the letters they speak in malayalam."
- OpenVoice `convert()` preserves source CONTENT (words + prosody) and only swaps TIMBRE — a frequency-domain swap that mangles Malayalam phonemes.
- IndicF5 is explicitly Malayalam-native (fine-tuned for 11 Indian languages) → correct G2P → correct words.
- The user is an alone warrior aiming for Cannes — voice is the last piece (image/video models are in place).

### Alternatives considered

- **OpenVoice alone for Malayalam** (rejected — mangles words).
- **Flipping the conversion direction** (rejected — doesn't fix the tool limitation).
- **GPT-SoVITS for Malayalam** (uncertain — test before committing; use for English).
- **A2TTS / OmniVoice** (depsek suggestions — not yet evaluated; IndicF5 is already installed and Malayalam-native).

### Result

**Rule: for Malayalam dialogue — IndicF5 TTS (correct words) + OpenVoice (voice color). For English — user's dub + OpenVoice (or GPT-SoVITS). Main character = clean dub directly. More/cleaner reference samples (52-letter coverage) = better results.** See `AUDIO_PIPELINE_PLAN.md` (VOICE STRATEGY + 2026-09-08 sections).

---

## D050 � Voice pipeline: VC (RVC/OpenVoice) for the movie, TTS (IndicF5/S2 Pro) for future kids content

Date: 2026-09-08
Status: Active

### Decision

**For the current 15-character bilingual movie: use VOICE CONVERSION (VC), not TTS.** The user performs ALL 15 characters' dialogue themselves (they are alone in this project, have the script, no one else is involved). VC preserves the user's performance (emotion, timing, delivery, Malayalam pronunciation) and only changes the voice identity (timbre) to the character's voice.

**For future kids videos / content where natural voice is NOT needed: use TTS** (IndicF5 for Malayalam, Fish S2 Pro for multilingual) � text-to-speech, no performance required.

**VC tool choice: RVC (primary) over OpenVoice (fallback).** RVC is the established VC tool � it preserves prosody (rhythm, pitch contour, emotion) while changing only timbre. OpenVoice is a pure timbre swap that keeps the user's skeleton (confirmed limitation: output "still sounds like me"). RVC trains a per-character model from 10+ min clean audio.

**Workflow (per character):**
1. User records 10+ min clean audio of the target voice (or uses existing references like Midhun's).
2. Train RVC model on that audio (F0 extraction via RMVPE + HuBERT content features + FAISS index).
3. User dubs the character's lines (headset, quiet room, dry).
4. clean_audio.py (denoise + loudnorm + 16 kHz mono).
5. RVC converts the dub ? character's voice (preserving user's performance).
6. LatentSync lip-sync ? DaVinci Resolve mix.

**Key insight (user + DeepSeek agreed):** TTS fails at Malayalam because the AI doesn't understand Malayalam prosody/pronunciation. VC sidesteps that entirely � the USER speaks the Malayalam (correct pronunciation, natural emotion), and RVC just changes the voice color. This is NOT a trade-off � it's exactly what the user wants ("without it it feels like we are doing some blind translation").

**Two-track system:**
| Track | Tool | Use case |
|-------|------|----------|
| **VC (movie)** | RVC (primary) / OpenVoice (fallback) | 15-character movie � user performs, VC changes voice |
| **TTS (future)** | IndicF5 (ML) / Fish S2 Pro (multilingual) | Kids videos, content where natural voice not needed |

### Reason

- User confirmed (2026-09-08): "this is not the trade off, this is what actually wants... 15 voice overs i can do that because only i have the script and other people wont get involved here, its me, im alone in this."
- TTS (Fish S2 Pro) Malayalam output sounds non-native (Tamilian accent, flat flow) � a general multilingual model approximating Malayalam.
- VC preserves the user's actual performance (acting, emotion, timing) � the "soul" of the dialogue � and only changes the voice identity.
- RVC is the established open-source VC tool (used by AI voice cover creators), RTX 5090-ready (~20 GB VRAM inference).
- User can dub a kid character and "he can go away" � the RVC model persists, no need for the kid to remember/read lines.

### Alternatives considered

- **TTS for the movie** (rejected � Malayalam quality is the bottleneck; AI doesn't understand ML prosody).
- **OpenVoice for the movie** (fallback � pure timbre swap, keeps user's skeleton, "still sounds like me").
- **Seed-VC / ApexSVC** (zero-shot alternatives � no per-character training, but lower quality ceiling than trained RVC).
- **Sarvam API** (rejected � cloud API, user wants local).

### Result

**Rule: movie = VC (RVC primary, OpenVoice fallback) � user performs all 15 characters, RVC changes voice identity. Future kids content = TTS (IndicF5/S2 Pro). See AUDIO_PIPELINE_PLAN.md (VOICE STRATEGY + 2026-09-08 sections).**

---

## D051 — The assistant runs ON the local Qwen: NEVER stop Qwen myself (user runs GPU jobs manually)

Date: 2026-09-08
Status: Active

### Decision

The local Qwen (`llama-server`) is the LLM that powers THIS assistant. If it is killed, the user **cannot talk to me anymore**. Therefore the assistant must **NEVER execute a command that stops/kills Qwen** (e.g. `Stop-Process -Name "llama-server"`), and must **NOT run GPU scripts that stop Qwen as a side effect** (e.g. `run_indicf5_gpu.ps1`, which stops Qwen in step 1 and restarts it in step 4).

### Correct workflow for any GPU-heavy job (ComfyUI, RVC, IndicF5, etc.)

1. Assistant PROVIDES the exact stop command as text for the user to run MANUALLY in their own terminal: `Stop-Process -Name "llama-server" -Force`
2. User runs it themselves (this temporarily cuts off the chat — expected and acceptable).
3. User runs the GPU job themselves (or tells the assistant it's done).
4. User restarts Qwen MANUALLY: `Start-Process "D:\models\qwen\Qwen3.827BMTP.bat"`

The assistant only ever PROVIDES these commands as text. It does not execute them.

### Reason

- User confirmed (2026-09-08): "youre running locally on my GPU, if i kill that task i cannot talk to u."
- The assistant's own inference depends on the local Qwen process staying alive.
- This supersedes the old pattern where GPU scripts auto-stopped/restarted Qwen — that pattern is now UNSAFE because it can kill the assistant's own runtime.

### Alternatives considered

- **Assistant auto-stops Qwen in a script** (rejected — kills the assistant's own LLM, user loses the chat).
- **Run GPU jobs while Qwen is active** (rejected — D045, contaminates benchmarks + both slow down).

### Result

**Rule: for any GPU job, the assistant gives the user the stop/run/restart commands to run MANUALLY. The assistant never executes a Qwen stop. See user-preferences.md (CRITICAL: I run ON the local Qwen).**

---

## D052 — RVC inference needs the WRAPPED checkpoint, not the raw G_*.pth

Date: 2026-09-08
Status: Active

### Decision

For RVC inference via `infer/cli.py`, ALWAYS use the **wrapped** inference
checkpoint (`assets/weights/<exp>.pth`), never the raw training checkpoint
(`logs/<exp>/G_*.pth`). The raw checkpoint is `{"model": {weights}, ...}`;
`infer/cli.py` `load_model_metadata()` requires the wrapped format
`{"weight": {...}, "config": [18 values], "info", "sr", "f0", "version"}`.

### Reason

- `train/process_ckpt.py savee()` is what produces the wrapped format, but it
  crashed on a missing `assets/weights/` dir, so the wrapped model was never
  saved — only the raw `G_2333333.pth` existed.
- `infer/cli.py` reads `checkpoint["weight"]["emb_g.weight"]`; the raw file
  has no `weight` key → `Model does not contain weight/emb_g.weight`.
- **DeepSeek's "copy G_*.pth into assets/weights" was WRONG** — copying the raw
  file still fails (no `weight` key). The raw weights must be UNWRAPPED from
  `["model"]` and re-wrapped into the savee() format.

### Fix (applied, no re-run needed)

`scripts\wrap_ckpt.py` (rvc venv, CPU-only) reads `G_2333333.pth`, unwraps
`["model"]`, rebuilds the savee() format, saves to `assets/weights/midhun_v1_40k.pth`.

### Naming rule (CRITICAL)

The wrapped model MUST be named `<experiment>.pth` (e.g. `midhun_v1_40k.pth`),
**NOT** `<experiment>_e10.pth`. `infer/vc/utils.py get_index_path_from_model()`
strips `_e\d+_s\d+$` (requires BOTH `_e` AND `_s`); an `_e10`-only suffix is
not stripped, so the FAISS index auto-match fails. Named `midhun_v1_40k.pth`, the
index `assets/indices/midhun_v1_40k_added_IVF66_Flat_nprobe_1_midhun_v1_40k_v1.index`
matches via `startswith(experiment + "_added_")`.

### Verified

`python -m infer.cli --model midhun_v1_40k.pth --list-speakers` → `0-108`
(CPU-only, loads the model, exits before GPU work).

### Inference command (user runs, Qwen stopped)

`cd D:\models\ai-movie\repos\rvc-webui; D:\models\ai-movie\envs\rvc\Scripts\python.exe -m infer.cli --model midhun_v1_40k.pth --input <source_wav> --output D:\models\ai-movie\03_audio_processed\rvc_midhun_test.wav --f0-method rmvpe --protect 0.33 --index-rate 0.75`

### Result

**Rule: RVC inference = wrapped `assets/weights/<exp>.pth` (named without `_eN`),
auto-matched index. Build it with `scripts\wrap_ckpt.py` if `savee()` never ran.**

---

## D053 — RVC voice quality: more Midhun data is the biggest lever; test the real source first

Date: 2026-09-08
Status: Active

### Decision

The Midhun RVC model (`midhun_v1_40k`, ~3.5 min training data) produces a
recognizable Midhun voice but **quirky words** on a Jaisal source. This is NOT
the ceiling. **Do NOT retrain immediately** — first test the REAL production
source (the user's own dub), because the quirkiness is largely a SOURCE
articulation mismatch (Jaisal's words + Midhun's timbre), not a model limit.

### Reason

- RVC is **audio→audio** (no text): the source provides words/rhythm, the model
  provides the voice identity. A Jaisal source → Jaisal articulation + Midhun
  timbre = quirky. A user dub → user articulation + Midhun timbre = the real
  production result.
- Model stability is limited by ~3.5 min of training data (2 clips).
- **Two levers:** (1) MORE MIDHUN DATA (biggest) — 5–10 min clean, diverse
  speech (Malayalam + English, different topics/emotions/speeds) → more
  consistent, more Midhun-like, less quirky; (2) TUNING (quick, no retrain) —
  `--index-rate 0.9` (stronger Midhun pull), `--protect 0.4`,
  `--f0-method pm` (A/B vs rmvpe).

### Workflow

1. **Test the real source first:** user dubs a line (headset, quiet room) →
   `clean_audio.py` → RVC convert → listen. If good → done, use for the movie.
2. **If still weak:** collect 5–10 min clean, diverse Midhun speech →
   `collect_references.py` → retrain via `rvc_train_midhun.py` (point at the
   new trainset) → re-test.
3. **Tune** (no retrain): `--index-rate 0.9`, `--protect 0.4`,
   `--f0-method pm`.

### Result

**Rule: RVC quirkiness = source articulation + model stability. Test the real
source (user dub) before retraining. More clean, diverse Midhun data is the
biggest quality lever.**

---

## D054 — Intro video: Krea2 Identity Transfer (not LoRA) + Qwen3-VL prompt engine + Shot Composer

Date: 2026-09-10
Status: Active

### Decision

For the **Jaisal Kut channel-intro video** (`docs/INTRO_SCRIPT.md`, ~67s, B&W,
no music, 7 shots, JAISAL + CAMERA GUY):

1. **Character consistency = Krea2 Identity Transfer workflow**
   (`krea2_identity_edit.json`, Identity Edit v1.2) — NOT a LoRA. A Krea2 **LoRA**
   is reserved for the **movies** (full consistency across 100+ shots). The intro
   is short, so identity transfer (ref_boost 4.0, style LoRA @ 0.7) is enough.
   Reference set = `E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\character_1`
   (20 PNGs).
2. **Qwen3-VL as the H3 prompt engine** —
   `D:\models\Writing\Qwen\Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49-Q4_K_M.gguf` +
   `...-mmproj-F32.gguf` (a VLM fine-tuned for MiniMax H3 → emits H3-optimized
   prompts). Wire it into the H3 ComfyUI pipeline so prompts are H3-tuned.
3. **Shot Composer (open-media) = the "Blender way"** —
   `https://github.com/Anujatk1999/open-media` (browser-based local 3D
   shot/pose/camera composer, mannequin.js + three.js, MCP server). Previsualize
   the hard shots (3 head-twist, 5/6 plants, 7 object assembly) → export
   MP4/PNG → feed to H3 as a motion/pose reference.

### Reason

- The intro has hard VFX items (180° head twist, object assembly, plant
  growth/death, perfect reverse) that H3 alone will struggle with. Identity
  transfer keeps the character consistent without a training run; Shot Composer
  gives H3 an explicit motion reference for the hard shots; Qwen3-VL makes the
  H3 prompts adhere better.
- Shot 4 (perfect reverse) is done in **POST** (reverse the forward take), not
  asked of H3.
- B&W look applied in post (consistent across shots) or baked into the Krea2
  keyframes.

### Result

**Rule: intro = Krea2 Identity Transfer + Qwen3-VL prompts + Shot Composer motion
references + H3 (SLA) + RVC audio + diegetic SFX (NO MUSIC). Movies = Krea2 LoRA.**
Full plan: `project-memory/INTRO_VIDEO_PRODUCTION.md`.

## D055 — Intro video voice assignment: JAISAL = user's own voice, CAMERA GUY = Midhun (RVC)

Date: 2026-09-11
Status: Active (HARD RULE)

### Decision

The user is **alone** on this project — they write the stories, turn them into
scripts, direct, and check the camera (with AI help). They **dub ALL the
dialogue** themselves. Voice assignment for the Jaisal Kut intro:

1. **JAISAL (the main character, most of the dialogue) = the USER'S OWN VOICE.**
   The user dubs every JAISAL line (Malayalam + English). These are cleaned
   (`clean_audio.py`) and used as-is (the user's real voice) — NOT Midhun.
2. **CAMERA GUY (off-screen, asks the questions) = MIDHUN'S VOICE.** The user
   dubs the camera-guy lines (in their own voice), then RVC converts them to
   Midhun via the existing `midhun_v2_40k` model. **No second RVC model is
   needed** — we reuse `midhun_v2_40k` for the camera guy.

This **supersedes** the 2026-09-10 plan (§10b #1) that had JAISAL = Midhun and
CAMERA GUY = a new 26-yo male model. The roles are effectively swapped: the
main character now carries the user's own voice (they're the face/voice of the
channel), and the off-screen interviewer carries Midhun.

### Reason

- The user is the sole writer/director/performer; the main character is an
  extension of them, so their own voice is the natural fit and avoids a
  "not-me" feel on the hero.
- Midhun (`midhun_v2_40k`, 6.5 min data, already trained + wrapped) is a
  ready-made distinct voice for the interviewer — no new training run needed.
- RVC is audio→audio: the user's camera-guy dub provides words/rhythm,
  `midhun_v2_40k` paints Midhun's timbre.

### Result

**Rule: JAISAL = user's own voice (cleaned dub). CAMERA GUY = user's dub →
RVC `midhun_v2_40k` (Midhun). The user dubs ALL lines.**

### Process decision (dub-first)

Because this is a fully post/AI pipeline (video is cheap + regenerable, unlike
traditional film where footage is the scarce asset), the **audio is the timing
spine**: each shot's duration is set by how long its line takes to say. So the
order is **dub first → lock shot durations from the audio → generate
keyframes + video to match → SFX + assembly**. A quick B&W tone test (1-2
Krea2 keyframes) runs in parallel to lock the look while the dubs are recorded.

## D056 — Intro keyframes v4: scene-consistency lock + per-shot minimal change + head-180 effect

Date: 2026-09-11
Status: Active

### Decision

After the v3 keyframe review (2026-09-11), the v4 set is built with these hard rules:

1. **The BASE/scene-master image is the anchor** — it must be STRAIGHT-ON, centered, symmetric, eye-level, NO wall, NO tilt, pure blackness outside the light pool. The v3 base (kf1_scene_master_00001_.png) was rejected (tilted side shot with a wall). Regenerate it FIRST; every other shot is an identity-edit of it (or of a good shot) so the scene stays identical.
2. **Consistency lock in EVERY prompt** — bulb position (center-top, same height), table (same size/position/centered), ONE chair (centered, no extra chairs anywhere), character (dark wavy hair, black full-sleeve shirt unbuttoned halfway). No extra changes per shot — only the specified change.
3. **kf6 = identity edit OF kf5** — same composition, only the plants become dead + melancholy emotion. NOT a fresh generation (v3's kf6_00001 came out completely different).
4. **kf7 props** — ALL props (bat, ball, smiley paper, mic) SMALL and ON the table, not blocking the character; ONLY ONE mic at the table.
5. **kf3b head effect** — the HEAD ALONE rotated 180° (face visible from behind, body/shoulders stay facing away — an impossible pose), NOT a normal shoulder look-back.
6. **No dedicated head-rotation LoRA exists on Civitai** (API search 2026-09-11: only unrelated character/pose LoRAs). kf3b is attempted PROMPT-FIRST; if Krea2 can't hold the impossible pose, options are: (a) a custom Krea2 LoRA trained on a few head-180 reference images, (b) Shot Composer (3D) for the twist, (c) post compositing (cut the head, rotate, paste).

### Reason

The v3 set had: off-center chair (kf1), extra chairs (kf2/kf5/kf6_00002), visible walls (kf2/kf6_00001), plants too small (kf5), kf6 composition drift, kf7 props too big + 2 mics + giant robot figure, and a tilted/walled base image. The user's rule: "I don't want to mess it up again" — so the scene is locked to ONE anchor image and each shot changes exactly one thing.

### Alternatives considered

- Fresh t2i per shot (rejected — composition drift, the v3 problem).
- Custom LoRA for the head-180 effect (deferred — no public LoRA found; prompt-first, then custom LoRA / Shot Composer / post-composite fallbacks).

### Result

**Rule: v4 = regenerate the base image straight-on first, then identity-edit each shot from the anchor with the consistency lock; kf6 edits kf5; kf7 props small + one mic; kf3b = head-only 180° (prompt-first, no public LoRA exists).**

---

## D057 — Intro keyframes v5: TRAIN A KREA 2 LoRA for a natural (non-plastic) character look

**Date:** 2026-09-12

**Decision:** The Krea2 Identity-Edit keyframes look **plastic / AI-ish** on the
character. The user wants a **natural** look for the intro video. **NEXT STEP =
train a Krea 2 LoRA** (character + natural-look) if the identity-edit route can't
crack the natural look. The user explicitly said: "update the project, that we
need to train a KREA 2 lora."

**Context / findings (2026-09-12):**
- **Available Krea 2 LoRAs locally** (`E:\ComfyUI_windows_portable\ComfyUI\models\loras\`):
  `Krea2_Cinematic_Artstyle.safetensors`, `krea2_darkbrush.safetensors`,
  `krea2_identity_edit_v1_2.safetensors`, `krea2_lineart_v1_fp16.safetensors`,
  `Typnosis_Krea2.safetensors` (unknown purpose — no metadata). **No dedicated
  "natural / camera / realism" Krea 2 LoRA is installed.**
- **FameGrid "Spice" Krea 2 LoRA** (Reddit r/StableDiffusion, "corrected release",
  2026-09-12): the user shared this as a candidate for a natural look. **Could not
  scrape the Reddit/Civitai page (JS-rendered / 403) — the user should open the
  link and confirm what it does + download it.** If it's a natural/realism LoRA
  for Krea 2, test it in the identity-edit workflow (node 71 LoraLoaderModelOnly)
  before training.
- **1-click dataset workflow exists:** `1 Click Dataset (Klein 9b).json` (Flux 2
  Klein) — the user builds character datasets with it. **Check whether a Krea 2
  equivalent exists** for building the training set.
- **v5 started:** `utilities/build_intro_keyframes_v5.py` (copy of v4, writes
  `_v5` files). **kf2 V5 = character looking at the chair, BOTH hands on the
  table** (user's spec). Generated `kf2_seated_v5_00001_.png` — pose correct,
  natural look, clean void.

**Alternatives considered:**
- Use an existing natural/camera LoRA (none installed for Krea 2 — see above).
- Test the FameGrid Spice LoRA first (pending user confirmation of what it is).
- Train a custom Krea 2 LoRA (character + natural look) — **the chosen next step**.

**Status:** PENDING — (1) user confirms the FameGrid Spice LoRA + downloads it;
(2) test it in the identity-edit workflow; (3) if insufficient, build a Krea 2
training dataset (1-click dataset workflow) + train the LoRA.

---

## D058 — Intro keyframes v7: CHARACTER shots use the character ref ONLY (no scene anchor)

**Date:** 2026-09-12

**Decision:** CHARACTER keyframes (kf2, kf3a/b/c, kf5, kf5a, kf6, kf7a/b/c) use
the **character ref ONLY** (node 72 = full `intro_char_ref_bw.png`, node 113/92
BYPASSED). **Do NOT anchor character shots to the empty base** — the scene anchor
breaks the character identity.

**Root cause (user-confirmed 2026-09-12):** the scene anchor (node 113 = the
empty base `intro_scene_master.png` = table+chair+bulb, NO person) FIGHTS the
character ref ("put a person here" vs "empty room") → the face distorts / becomes
a different person. Evidence: V3 (char ref only) = GOOD character; V4/V5/V6
(char ref + empty-base scene anchor) = BROKEN character; V7 (char ref only, V3
settings) = GOOD character again.

**The V3 tradeoff (user accepted):** V3's character is good, but the scene has a
wall (right) + chair (left) + plant. Fixing walls/chair/plant WITHOUT a scene
anchor = **PROMPT-ONLY** (stronger negatives: no wall, one chair centered). Do
NOT "fix" the scene by adding a scene anchor — it breaks the character.

**V7 = the good-character base** (`utilities/build_intro_keyframes_v7.py`,
workflows `krea2_intro_kf*_v7.json`). Built from V3's exact settings.

**Alternatives considered:**
- Scene anchor for consistency (REJECTED — breaks the character, the user's #1
  priority).
- Face-only char ref crop (REJECTED — also broke identity; see
  `krea2-identity-face-crop-failure.md`).

**Status:** V7 character VERIFIED good (`kf2_seated_v7_00001_.png`). NEXT: fix
walls/chair/plant via prompt-only in V7, regenerate the set, then MiniMax H3.

---

## D059 — Head-rotation keyframes: hands/90° SOLVED via identity-edit; 180° face-at-camera UNSOLVED by Krea2

**Date:** 2026-09-12

**Decision:** For the Shot-3 head-twist keyframes, anchor identity-edit on the
**GOOD FRAME** (not a fresh t2i): `kf2_hands_table` anchored on
`kf2_00004_ref.png` (the good manual-inpaint front view); `kf3c_head90` +
`kf3b_head180` anchored on `kf3a_headnormal_v7` (the perfect back view).
**A 180° head rotation with the face at the camera CANNOT be done by Krea2
identity-edit** — it over-rotates to ~270° (face sideways). Use manual inpaint
or let MiniMax H3 do the 90→180 motion in video.

**Results (user-verified 2026-09-12):**
- `kf2_hands_table` = ✅ GOOD (both hands flat on table, facing camera).
- `kf3c_head90` = ✅ GOOD (back view, head ~90° side profile). The camera in the
  image is at 180 (back view), NOT 90 — user ACCEPTS this; the camera motion is
  the MiniMax H3 CAMERA NODE's job (`H3LocalCameraEditor`, installed 2026-09-12,
  needs ComfyUI restart + `camera_motion_h3_lora_v1_3000_pruned.safetensors`).
- `kf3b_head180` = ❌ UNSOLVED. Anchored on the back view + "face looking
  STRAIGHT AT THE CAMERA over the shoulder" + negatives (face in profile, 270
  degree rotation, head over-rotated) → seeds 501/601/602 ALL over-rotated to
  ~270° (face sideways). The body-stays-back constraint fights the head rotation.

**Root cause:** Krea2 identity-edit is CONSERVATIVE and holds the reference's
head orientation; asking it to rotate the head 180° while keeping the body in
back view is an impossible pose it resolves by over-rotating sideways.

**Alternatives for kf3b (when back):**
- (a) MANUAL INPAINT on kf3a (like the kf2 chair black-fill) — mask the head
  region, prompt "face turned around over shoulder looking at camera" (most
  controllable; matches how kf2 was solved).
- (b) Fresh t2i of the back-view-with-face-around (no anchor).
- (c) ACCEPT kf3c 90° as the only twist anchor and let MiniMax H3 do the
  90→180 motion itself (simplest — H3 is good at head turns in video).

**Consolidated folder (user's request — ONE path):**
`d:\models\vsCodeMcp\Jaisal-intro\kf2_headset\` = `kf2_hands_table.png`,
`kf3a_headnormal.png` (anchor), `kf3c_head90.png`, `kf3b_head180.png` (bad —
replace when solved).

**Workflows:** `krea2_kf2_hands_table.json`, `krea2_kf3c_head90.json`,
`krea2_kf3b_head180.json` (identity-edit clones; node 82 = [1928,1088,1],
ref_boost 4, grounding 768, Image Comparer node 114 BYPASSED mode=4 — the
submit script crashes on its type name otherwise). Build scripts:
`utilities/build_kf2_head_rotation.py`, `utilities/build_kf3_head_rotation.py`,
`utilities/run_kf3b_180_seeds.py`. Submit: `utilities/submit_krea2_workflow.py`.

**Status:** hands + 90° DONE. 180° UNSOLVED (pick option a/b/c when back).

---

## D060 — VoiceStudio added to the voice arsenal (local ElevenLabs alternative)

**Date:** 2026-09-12

**Decision:** Add **VoiceStudio** (github.com/debpalash/VoiceStudio, 23.8k stars,
AGPL-3.0, fully local) to the voice arsenal as a 5th option alongside RVC,
OpenVoice, IndicF5, Fish S2 Pro. It is a real local ElevenLabs alternative:
16 TTS engines (default **OmniVoice** = 600+ languages incl. Malayalam; also
CosyVoice 3, GPT-SoVITS, VoxCPM2, IndexTTS 2.5, etc.), 11 ASR engines, video
dubbing pipeline (transcribe → translate → preserve speakers → synthesize →
export), zero-shot voice cloning from a 3-15s clip, voice design, MCP server
(`http://localhost:3900/mcp`) + OpenAI-compatible API
(`http://localhost:3900/v1`).

**Why:** the movie is bilingual (Malayalam + English). OmniVoice's 600+ language
coverage + zero-shot cloning (no training, unlike RVC) makes it a strong
candidate for the character voices. The user's hypothesis: it may be the best of
all 5. **Keep it READY in the arsenal; A/B test against RVC `midhun_v2_40k`
before committing.**

**Install (DONE 2026-09-12):** current-user MSI (NO admin) →
`C:\Users\user\AppData\Local\VoiceStudio (Current User)\omnivoice-studio.exe`.
MSI downloaded to `D:\models\VoiceStudio\VoiceStudio_Current_User_0.5.2_x64_en-US.msi`
(177.9 MB). Launched — first-run creates the Python env (via `uv`) + downloads
the default OmniVoice model (watch the splash). GPU = NVIDIA/CUDA-only on
Windows (our RTX 5090 gets CUDA accel; no CUDA Toolkit install needed).
Backend runs loopback-only on `localhost:3900`.

**First voice (when the app is up):** Voice Cloning tab → add a clean 5-15s
reference clip (e.g. a Midhun or Jaisal clean wav from
`D:\models\ai-movie\references\`) → enter text → pick language (Malayalam /
English) → Generate.

**Triton/torch.compile OOM note (Windows):** if an engine OOMs on first
synth, Settings → Performance → "Disable torch.compile (Windows)" (sets
`TORCH_COMPILE_DISABLE=1`).

**MCP (optional, later):** add to `.vscode\mcp.json` →
`{"voicestudio": {"url": "http://localhost:3900/mcp"}}` (or the stdio shim
`python -m backend.mcp_shim`).

**Status:** INSTALLED + LAUNCHED. NEXT: confirm first-run bootstrap finished,
clone a test voice, A/B vs RVC.

---

## D061 — kf3b 180° head shot: 2nd face reference + head-REPLACEMENT prompt (2026-09-13)

Date: 2026-09-13
Status: Active (workflow ready, awaiting user's manual seed runs)

### Decision
For the kf3b horror 180° head shot, use a **TWO-reference** identity-edit setup:
- **Node 72 (primary/scene):** `kf3a_v7_back_ref.png` (the back-view frame being edited).
- **Node 113 (secondary/identity):** `jaisal_face_mono_closeup.png` — a monochrome
  face-only close-up cropped from the CORRECT character
  (`E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\character_1\Image_00001_.png`).
- **Node 79 = `[3, 1, fit]`** — `ref_boost` (3) applies to the LAST ref = the
  FACE (strong identity copy); `ref_boost_a` (1) applies to the FIRST ref = the
  scene (off, just the editing base).
- **Node 84 prompt = the user's WORKING head-REPLACEMENT prompt** (frames it as
  "replace only the head with a frontal view of the same man's face... looking
  directly into the camera... body/shoulders/torso facing completely away"), NOT
  "rotate 180 degrees" (which made Krea2 over-rotate to 270°).

### Reason
The single-reference attempts (D059) all over-rotated to ~270°. The user found
that (a) describing the END STATE (face at camera) instead of the rotation amount,
and (b) feeding a monochrome face close-up as a 2nd reference so the model COPIES
the actual face instead of hallucinating one, gets much closer.

### Key facts
- `Krea2EditModelPatch` boost semantics (from object_info): `ref_boost` = LAST
  ref (subject/face), `ref_boost_a` = FIRST ref (scene). `fit_mode` = `fit`.
- `ref_boost_mask` = optional region on the LAST ref to boost (e.g. the face).
- Face ref script: `utilities/make_mono_face_ref.py` (crop + grayscale +
  autocontrast). Project copy: `Jaisal-intro\kf2_headset\jaisal_face_mono_closeup.png`.
- **CORRECT character = `character_1` dataset** — NOT the Krea2 renders in
  `input/` (jaisal_face_*.png etc. are a DIFFERENT face). See repo memory
  `jaisal-correct-character-reference.md`.

### Status
Workflow `krea2_kf3b_head180.json` validated clean. User runs seeds manually.
If all seeds fail → fallbacks (a) manual inpaint on kf3a head region, (b) fresh
t2i, (c) accept kf3c 90° + MiniMax H3 does the 90→180 motion.

---

## D062 — VoiceStudio model selection: OmniVoice + Whisper large-v3 only (2026-09-13)

Date: 2026-09-13
Status: Active

### Decision
For the Jaisal movie (Malayalam + English, 2 characters), install ONLY:
- **OmniVoice** (default, k2-fsa, 2.4 GB) — 600+ langs incl. Malayalam, zero-shot.
- **Whisper large-v3** (faster-whisper, 2.9 GB) — transcription for dubbing.
- **Whisper Tiny** (0.1 GB) — dictation shortcut only (90+ langs, auto-detect).

### Reason
The app "recommends" a broad list for all users, but for our specific job the
other engines are redundant or wrong-language: KittenTTS (English-only), Whisper
Turbo/Tiny/medium/small/base (redundant with large-v3), Parakeet/Moonshine/
Zipformer/Paraformer (EN/ZH dictation), VoxCPM2/GPT-SoVITS/MOSS/dots.tts/
Confucius4 (other-language TTS), pyannote (multi-speaker video only). CosyVoice 3
(9.8 GB) is the only optional A/B but only 9 langs (mostly NOT Malayalam) — skip.

### Notes
- OmniVoice weights = CC-BY-NC (non-commercial — fine for the movie).
- VoiceStudio is NOT ElevenLabs — it's a free local 80-90% alternative. Its real
  value: (1) 5th engine for A/B, (2) unified dubbing pipeline, (3) API/MCP
  (localhost:3900) so the agent can drive it, (4) voice design (text→voice).
- **Convert tab is NOT a true voice conversion** — it transcribes (Whisper) then
  re-synthesizes (TTS), so emotion/delivery is LOST. For true voice conversion
  (keep performance, change timbre) use **RVC**.
- **Emotion on the default OmniVoice engine:** the #1 lever is an
  emotionally-performed reference clip (flat ref → flat output). Plus punctuation
  + `[pause Nms]`, `class_temperature` 0.3-0.7 + seed farming, `[laughter]`/
  `[sigh]` tags, `whisper` style, `postprocess_output` off. The default engine
  does NOT accept `[happy]`/`[sad]`/`[excited]` tags (it speaks the word).
  IndexTTS 2.5 emotion sliders = no Malayalam.
- Summary doc for asking DeepSeek/OpenAI: `Jaisal-intro\voicestudio_summary.md`.

---

## D063 — RVC source-leakage recipe: protect 0.0 + double pass (2026-09-13)

Date: 2026-09-13
Status: Pending A/B confirmation (recipe built, winner not yet locked)

### Decision
To reduce RVC source leakage (output still sounding like the user), use:
1. **Clean the source** (denoise, normalize, mono) before conversion.
2. **`--protect 0.0`** (the #1 fix — default 0.33 means "keep 33% of the
   original voice", which is the leak).
3. **`--index-rate 0.7-1.0`**, `--f0-method rmvpe`, pitch 0.
4. **Double pass** — run the output through the same model a 2nd time (protect
   0.0 again) to strip residual source character.
5. **Light post** — high-pass 80-100 Hz, loudness normalize.

### Reason
RVC's Protect parameter is the main source-leakage dial. A double pass is the
classic fix for "still sounds a bit like me".

### Status
A/B test pending (tomorrow): same line, 3 ways (single pass / double pass /
double pass + post). Winner gets LOCKED as the standard RVC conversion pipeline
for the movie (consistency across all lines). If leakage persists after the
double pass, the ceiling is the target model quality → retrain on cleaner/longer
data.

---

## D064 — C: drive cleanup: freed ~90 GB, pagefile stays on C: (2026-09-13)

Date: 2026-09-13
Status: Done

### Decision
Freed ~90 GB on C: (was 135 GB free → now 215 GB free):
- HF cache `.cache\huggingface` (36.3 GB) — deleted (re-downloads on demand).
- pip cache (23.9 GB) — `pip cache purge`.
- Temp (5.4 GB) + CrashDumps (2.8 GB) — deleted.
- **hiberfil.sys (24.6 GB) — `powercfg /h off`** (hibernation disabled; safe,
  reversible with `powercfg /h on`).
- **pagefile.sys (61.8 GB) — KEPT on C:** (user's decision). It's functional
  (virtual memory), NOT junk. Moving it is fiddly + risky; resizing needs admin +
  reboot. At 215 GB free there's no need.

### Reason
The "missing 90 GB" was the two hidden system files at C:\ root (pagefile 61.8 +
hiberfil 24.6 = 86.4 GB) — not in the user folder. SSDs don't slow down until
~85-90% full, so boot speed was never at risk (was ~73% full).

### Notes
- uv cache (6.1 GB) + npm cache (1.3 GB) cleanup optional (uv not on PATH →
  delete `AppData\Local\uv\cache` directly; npm blocked by execution policy →
  use `npm.cmd`).
- VoiceStudio (~17 GB) fits easily in the 215 GB free.

---

## D065 — SeedVR2 single-IMAGE upscaling via the numz ComfyUI pack (not the Studio app)

**Date:** 2026-09-13

**Decision:** For 2K/4K upscaling of **single keyframe images**, use the
**`numz/ComfyUI-SeedVR2_VideoUpscaler`** ComfyUI nodes (installed 2026-09-13),
NOT the SeedVR2 TensorRT Studio app. The Studio app is video-oriented and its
image jobs failed on model loading (`7B Sharp FP16` → `invalid python storage`).
The numz pack explicitly supports single images (`batch_size=1`).

**Why:** The Studio app's `POST /api/jobs` image submissions errored at 0.28
progress (model-load crash). The numz pack's `SeedVR2VideoUpscaler` node +
`SeedVR2LoadDiTModel`/`SeedVR2LoadVAEModel` handle a single image with
`batch_size=1` (per the official docs: "Use 1 only for single images").

**Setup done (2026-09-13):**
- Cloned `numz/ComfyUI-SeedVR2_VideoUpscaler` →
  `E:\comfyUi_latest\...\custom_nodes\seedvr2_videoupscaler`.
- Installed missing dep `rotary_embedding_torch` (0.9.1).
- **Fixed a transformers 5.9.0 bug** that blocked the import:
  `PACKAGE_DISTRIBUTION_MAPPING["flash_attn"]` KeyErrors when flash_attn is not
  installed. Patched 3 lines (988/1019/1030) in
  `transformers/utils/import_utils.py` → `.get("flash_attn", [])`. Backup at
  `import_utils.py.flash_attn_bak`. (Re-apply after any transformers upgrade.)
- Restarted ComfyUI so the 9 SeedVR2 nodes register.

**Workflow:** `seedvr2_image_upscale.json` (UI format, validated clean) built by
`utilities/build_seedvr2_image_wf.py <input.png> [prefix]`. Native widget shapes
(from the official `example_workflows/SeedVR2_simple_image_upscale.json`):
- LoadImage `["<img>","image"]`
- SeedVR2LoadDiTModel `["<model>","cuda:0",0,false,"none",false,"sdpa"]`
- SeedVR2LoadVAEModel `["ema_vae_fp16.safetensors","cuda:0",false,1024,128,false,1024,128,"false","none",false]`
- **SeedVR2VideoUpscaler `[42,"randomize",1440,2560,1,false,"lab",0,0,0,0,"cpu",false]`**
  (13 values — hidden "randomize" after seed, same pattern as KSampler)
- SaveImage `["<prefix>"]`

**Settings:** `seedvr2_ema_7b_sharp_fp16.safetensors` (max quality, local),
resolution 1440 / max 2560 (2K), batch_size 1, color_correction `lab`,
attention `sdpa`.

**CLI alternative (no ComfyUI):**
`python custom_nodes\seedvr2_videoupscaler\inference_cli.py <img> --dit_model seedvr2_ema_7b_sharp_fp16.safetensors --resolution 1440 --max_resolution 2560 --batch_size 1 --color_correction lab`
(needs `PYTHONIOENCODING=utf-8` on Windows).

**Status:** Active. Workflow validated `valid: true`. Next: run it on the plant
keyframes, copy 2K outputs to `Jaisal-intro\v9\`.

---

## D066 — Object-ref images: UNSEEN top light, NO visible bulb (2026-09-14)

**Decision:** All Krea2 t2i object-reference images (soccer ball, cricket bat,
paper-smiley — `krea2_object_refs.json`) are lit from directly above by a single
**UNSEEN** light source. The bulb/lamp itself must NOT appear in the frame — only
its light and hard shadow.

**Reason:** A visible bare bulb in the object refs confuses MiniMax H3 when the
objects are composited into the scene (it tries to reconcile two light sources /
a bulb that isn't in the scene). The light *effect* (top-down, hard shadow) is
kept; the *source* is removed.

**Implementation:**
- Positive prompts: "Lit from directly above by a single UNSEEN light source —
  the light itself is NOT visible in the frame, only its light and hard shadow."
- Negatives: `light bulb, bare bulb, lamp, visible light source, ceiling, cord,
  wire, hanging bulb, bulb in frame`.

**Alternatives considered:** keeping the bulb for consistency with the scene
keyframes (rejected — H3 confusion outweighs consistency); a side light (rejected
— breaks the top-down look of the whole film).

**Status:** Active. Applies to all future object/prop reference images.
