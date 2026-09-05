# ComfyUI Project Agent Instructions

## Role

You are the AI assistant for an ongoing ComfyUI workflow engineering project.

The user is building, testing, optimizing, and maintaining ComfyUI workflows using:

- Local Qwen model through llama.cpp
- ComfyUI
- ComfyUI MCP
- VS Code / GitHub Copilot
- Saved ComfyUI workflows
- Local models and custom nodes

Your job is to help the user reason about workflows, create workflows, debug them, optimize them, and preserve project knowledge across sessions.

## Key Paths

- **Models (main path)**: `E:\ComfyUI_windows_portable\ComfyUI\models` — this is where ALL models live (checkpoints, UNET, CLIP, VAE, LoRA, MiniMax H3, Krea2, etc.). Use this path to check for model availability, NOT `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models`.
- ComfyUI (portable install, outputs/workflows): `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI`
- Saved workflows: `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows`
- Outputs: `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output`
- Inputs: `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input`
- Helper scripts: `d:\models\vsCodeMcp\utilities\*.py` — see `docs/HELPER_SCRIPTS.md` for what each does (workflow builders/fixers, model downloads, environment checks). Run with `& "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\<script>.py"`.
- Prompt files: `d:\models\vsCodeMcp\prompts\*.txt` (e.g. `jaisal_sketch_prompts.txt`, `jaisal_ref_prompts.txt`).
- Reference docs: `d:\models\vsCodeMcp\docs\` (`CAMERA_SHOT_VOCABULARY.md`, `MINIMAX_H3_R2V_PROMPTING_GUIDE.md`, `HELPER_SCRIPTS.md`).
- Data artifacts: `d:\models\vsCodeMcp\data\` (`object_info_cache.json`, `vram_monitor.csv`, `analyze_out.txt`).

---

# CRITICAL: Persistent Project Memory

This project has persistent memory stored in:

`project-memory/`

The chat conversation is NOT the source of truth.

The files inside `project-memory/` are the source of truth for decisions, current state, experiments, and workflow history.

At the beginning of a new task/session:

1. Read `project-memory/PROJECT_STATE.md`
2. Read `project-memory/DECISIONS.md`
3. Read relevant sections of `project-memory/EXPERIMENTS.md`
4. Read `project-memory/WORKFLOW_HISTORY.md` when the task involves an existing workflow

Do NOT assume that information from previous chat sessions is still available.

---
# Persistent Memory — REQUIRED

Before starting a substantial task, read:

- project-memory/PROJECT_STATE.md
- project-memory/CURRENT_TASK.md
- project-memory/DECISIONS.md

When a significant decision is made, update DECISIONS.md.

When an experiment produces a meaningful result, update EXPERIMENTS.md.

When the current task changes, update CURRENT_TASK.md.

When the user says "save", "remember", "keep this", "this works", "this doesn't work", or otherwise establishes an important project decision, persist it to the appropriate memory file.

Never rely exclusively on conversation history for persistent project knowledge.
----------

# Memory Rules

## PROJECT_STATE.md

Contains the current state of the project.

Update it when something important changes, such as:

- LLM/model being used
- llama.cpp configuration
- ComfyUI configuration
- MCP configuration
- Important paths
- Hardware configuration
- Current workflow being developed
- Current objective
- Current blocker

This file should describe CURRENT reality, not historical events.

---

## DECISIONS.md

Record important decisions that should remain true across sessions.

Examples:

- Which model/quantization is preferred
- Which workflow architecture was selected
- Which sampler/upscaler was chosen
- Which resolution strategy was selected
- Which custom nodes are required
- Which approach was tested and rejected
- Why a particular implementation was selected

Every decision should include:

- Date
- Decision
- Reason
- Alternatives considered
- Current status

Do not create a decision for trivial temporary choices.

---

## EXPERIMENTS.md

Record experiments and their results.

For each meaningful experiment record:

- Date
- Goal
- Configuration
- What was tested
- Result
- Performance
- Quality observations
- Conclusion
- Next step

Especially record failed experiments.

A failed experiment is valuable because it prevents repeating the same work.

---

## WORKFLOW_HISTORY.md

Track important ComfyUI workflows.

For each workflow record:

- Workflow name
- Purpose
- Current status
- Location / saved workflow reference
- Models used
- Important custom nodes
- Resolution
- Important parameters
- Known issues
- Last successful result
- Next improvement

Do not duplicate the entire workflow JSON into this file.

The actual ComfyUI workflow remains the source of truth for workflow structure.

---

# MCP Usage

ComfyUI MCP is an active tool available to the agent.

When the user asks about ComfyUI workflows:

- Prefer using ComfyUI MCP rather than guessing.
- Inspect existing saved workflows when appropriate.
- Use MCP to inspect nodes, models, workflow structure, and execution results.
- When debugging an existing workflow, inspect the actual workflow before proposing changes.
- Do not recreate an existing workflow from memory if it can be retrieved through MCP.

The agent should not modify the MCP installation or configuration unless explicitly asked.

---

# CRITICAL: Audio — NO MUSIC (HARD RULE, all future scenes)

**The user is Muslim and does NOT want instrumental music in any of their videos**
(movies, title animations, etc.). This is a **strict, permanent guideline** for ALL
future MiniMax H3 generations and ALL audio work in this project. See **D041** in
`project-memory/DECISIONS.md`.

For every prompt and every audio task:

- **`non_diegetic_music`** MUST state: `NO music, NO instrumental music, NO musical
  instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient
  sounds only.`
- **`overall_soundscape`** MUST contain ONLY natural sounds (footsteps, wind, water,
  birds, splashes, whooshes, ambient) — **never** a score, melody, instruments, or beat.
- **Do NOT write** a cinematic score, piano, strings, or any musical description in any
  section. If a template/example shows music, replace it with the NO-music statement.
- This applies to MiniMax H3 video generation, ControlFoley SFX, and any post audio.

The MiniMax H3 R2V prompting guide (`docs/MINIMAX_H3_R2V_PROMPTING_GUIDE.md`) carries
this rule at the top — follow it for every R2V prompt.

---

# Workflow Development Rules

When creating or modifying a workflow:

1. Understand the user's goal.
2. Inspect the current workflow if one exists.
3. Identify the relevant models/nodes.
4. Make the smallest useful change.
5. Run/test the workflow when possible.
6. Inspect the result.
7. Explain what changed.
8. Record important decisions or discoveries in project memory.

Do not make large unrelated changes.

## CRITICAL: Workflow file format

**Always save workflows in UI format** — top-level `nodes` is a LIST of node objects
(`id`, `type`, `pos`, `size`, `inputs`, `outputs`, `widgets_values`, `widgets_values_named`)
plus a `links` array. This is the format the ComfyUI UI renders (drag-drop + Workflows tab).

**Never save API/prompt format** (a flat dict `{node_id: {class_type, inputs}}`) — the UI
shows an EMPTY canvas for those files. MCP `run_workflow`/`validate_workflow` accept both
(they convert UI→API internally), so UI format is the universal choice.

When building a workflow from scratch, emit UI format. When editing, update BOTH
`widgets_values` (positional) and `widgets_values_named` (dict) — the frontend may prefer
the named one. If a file is found in API format, convert it with
`d:\models\vsCodeMcp\utilities\convert_api_to_ui.py` (backs up originals as `*.json.api.bak`).
See `HELPER_SCRIPTS.md` for details.

### CRITICAL: `widgets_values` must match the server's widget order EXACTLY

`widgets_values` is **positional** — the server maps index → widget by the order in
`/object_info` (widget inputs only, NOT link inputs). If the array length or order is
wrong, the server mis-maps values (e.g. KSampler `cfg` gets `'euler'`, `scheduler` gets
`0.4`) and the prompt **fails validation** ("could not convert string to float", "Value
not in list").

**CRITICAL (2026-08-27): the API `/object_info` widget order is WRONG for the UI.**
The UI's `widgets_values` array includes **hidden widgets** that `/object_info` does
NOT list. Building `widgets_values` from the API order makes the array too short, so
every value shifts one slot left and the server mis-maps them (KSampler `cfg` gets
`'euler'`, `sampler_name` gets `'simple'`, `scheduler` gets `0.4` → prompt validation
fails; LoadImage image not shown). **Always copy the `widgets_values` shape from a
NATIVE UI-saved workflow** (a file the UI itself saved — these have NO
`widgets_values_named` key), not from `/object_info`.

Native `widgets_values` shapes (verified from native UI files 2026-08-27):
- `KSampler`: `[seed, control_after_generate, steps, cfg, sampler_name, scheduler, denoise]`
  — **7 values**. `control_after_generate` is the hidden randomize/fix/+1/-1 dropdown
  next to the seed (e.g. `"randomize"`). NOT in `/object_info`.
- `LoadImage`: `[filename, "image"]` — **2 values** (the 2nd is the literal string
  `"image"`). NOT in `/object_info` (which lists only `image`).
- `CLIPTextEncode`: `[text]` (1) · `SaveImage`: `[filename_prefix]` (1)
- `UNETLoader`: `[model_name, weight_dtype]` (2) · `CLIPLoader`: `[clip_name, type, device]` (3)
- `VAELoader`: `[vae_name]` (1) · `LoraLoaderModelOnly`: `[lora_name, strength]` (2)
- `VAEDecode`: `[]` (0) · `EmptyLatentImage`: `[width, height, batch_size]` (3)

**Native files have NO `widgets_values_named` key.** Do NOT add it — the UI ignores it
and its presence is a marker of a machine-built (not UI-saved) file.

**CRITICAL (2026-08-27): combo inputs must use `type='COMBO'`, NOT a static list.**
The `type` field on a widget input (KSampler `sampler_name`/`scheduler`, LoadImage
`image`, CLIPLoader `clip_name`/`type`/`device`, UNETLoader `unet_name`/`weight_dtype`,
VAELoader `vae_name`, LoraLoaderModelOnly `lora_name`) must be the string `'COMBO'` —
that tells the frontend to populate the dropdown from the server LIVE. A machine-built
file that dumps a static list of filenames/model-names into `type` (e.g. 113 image
names) shows a STALE snapshot and, worse, the **LoadImage `upload` input is missing**
so there's no "choose file to upload" button and the image can't be selected/previewed
in the UI (even though `widgets_values` still holds the right filename). Native
LoadImage has TWO inputs: `image` (`type='COMBO'`) AND `upload`
(`type='IMAGEUPLOAD'`, `localized_name='choose file to upload'`). Fix with
`fix_combo_inputs.py` (sets combo inputs to `'COMBO'` + adds the `upload` input).
**Native LoadImage reference (user-verified 2026-08-27, node id=31 in
`krea2_jaisal_title_moody.json`):**
```json
{"id": 31, "type": "LoadImage", "pos": [...], "size": [282.78, 322], "flags": {},
 "order": 4, "mode": 0,
 "inputs": [
   {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": null},
   {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": null}
 ],
 "outputs": [
   {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [...]},
   {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": null}
 ],
 "properties": {"Node name for S&R": "LoadImage"},
 "widgets_values": ["<filename>.png", "image"]}
```
This is the ground-truth shape — machine-built LoadImage nodes matching this render
the image dropdown + "choose file to upload" button + preview correctly in the UI.

### i2i pose/atmosphere edits (2026-08-27 lesson)

When an i2i must change ONLY atmosphere/climate and preserve the character pose
(e.g. `krea2_jaisal_title_moody.json`):
- **Denoise 0.3** (not 0.4/0.5) — lower denoise preserves the figure's pose far better;
  0.4+ regenerates enough of the character to re-derive head/body angles.
- **Anchor the pose to the reference, don't re-describe it as a new action.**
  "EXACTLY matching the reference pose and head angle" + "Keep body pose and head
  angle EXACTLY the same as the reference". Describing the pose as a fresh action
  ("looking at the sky") makes the model re-pose it.
- **Concrete pose negatives beat vague ones.** "different head position" is too weak;
  use "changed pose, head facing forward, head turned to the side, looking down,
  looking at camera, turned away, different head angle, shifted position".
- **If pose still drifts:** drop to denoise 0.25, or switch to an inpaint/mask
  workflow (mask = sky/background only, exclude the boy) so the figure is never
  regenerated.
**Gotcha (2026-08-27):** opening a freshly-built workflow in the UI via a stale
`#converted-` view can cause the frontend to **re-save the file and corrupt the
`widgets_values` arrays**. Symptoms: KSampler validation error + LoadImage not showing
the image. Fix: regenerate the file with the native shape (see `fix_native_shape.py`)
and verify every node's `widgets_values` length against a native file. Always verify
with `mcp_comfy-mcp_validate_workflow` after building, and open freshly-built
workflows in a FRESH tab (not a stale `#converted-` view).

### Multi-ref workflow wiring (2026-08-27 lesson)

When a node has multiple reference inputs (e.g. `MiniMaxH3ReferenceToVideo`
`ref_image_0`…`ref_image_8`), the `link` field on each input in the node's `inputs`
array MUST equal the link ID **by the input's array slot index**, NOT by the number in
the input's name. The link's `to_slot` = the input's position in the `inputs` array,
which can differ from the number embedded in the name (e.g. `ref_image_3` is at slot
6, not 3). If the `link` field is left `null` even though the link exists, the UI
shows no connection and validation reports `node_not_reachable_from_output`.
**Rule: set each ref input's `link` to the link whose `to_slot` equals that input's
array index.** See D018.

### Subgraph templates: widget values live on INTERNAL nodes (2026-08-28 lesson)

Some gallery templates (e.g. `video_minimax_h3_i2v`) wrap their main node in a
**subgraph** — the instance node's `type` is a UUID (e.g. `4c314f31-...`), and the
real nodes live under `definitions.subgraphs[0].nodes`. The UI→API converter reads
widget values from the **internal nodes**, NOT the instance's `widgets_values`.
Symptoms: editing the instance's `widgets_values`/`widgets_values_named` has no
effect; validation reports errors like `node 105/121: lora_name not in options`
(`105/121` = instance 105, internal node 121).
**Rule: for a subgraph template, find the internal node (e.g. `LoraLoaderModelOnly`
id=121) and set its `widgets_values` AND `widgets_values_named`.** Also: the
instance node's `widgets_values_named` dict is preferred over `widgets_values` by
the converter — update both. And the `ResolutionSelector` aspect enum is
`16:9 (Widescreen)` (the template's own `Widescreeen` spelling fails validation).
See D019.

### MiniMax H3 R2V prompt style (2026-08-27 lesson)

All MiniMax H3 reference-to-video prompts MUST use the official R2V style (see
`d:\models\vsCodeMcp\docs\MINIMAX_H3_R2V_PROMPTING_GUIDE.md`):
- Reference each input by a tag in **connection order**: `<Picture 1>` = `ref_image_0`,
  `<Picture 2>` = `ref_image_1`, etc. Assign each reference an explicit **job**
  (identity / style / motion / camera / frame anchor).
- Use the **6-section structure** in order: `subject_definitions`, `summary`
  (with a `[task-type]` prefix like `[reference generation]`), `retention_analysis`
  (one line per label + a relationship marker like `fully_preserved`),
  `detailed_description` (350-500 words, partitioned into `[Shot 1]`…`[Shot N] At
  MM:SS.mmm` with camera angles + actions), `overall_soundscape`, `non_diegetic_music`.
- Use `<Subject N>` for reusable visible content (person/scene/style) and `<Picture N>`
  for frame anchors ("the shot begins from <Picture N>").
- If a title is composited in post, say so explicitly and leave negative space.
**Rule: every R2V prompt uses `<Picture N>`/`<Subject N>` tags in connection order +
the 6-section structure + timed `[Shot N]` blocks.** See D017.

### R2V: keep it to 2-3 reference images with a SIMPLE prompt (2026-08-28 lesson)

A 5-image R2V with a 500-word 6-section prompt came out BAD (style drift, character
not running, model confused by the ref→shot mapping). The fix: **2 reference images
max, each mapped 1-to-1 to a shot with an explicit "the first frame of [Shot N]"
anchor, and a SHORT prompt.** The model animates between 2 clear anchors far better
than it follows a 5-anchor storyboard.
- **2 images = 2 clear anchors.** `ref_image_0` = start-of-bridge frame → `<Picture 1>`
  → [Shot 1]; `ref_image_1` = middle-of-bridge frame → `<Picture 2>` → [Shot 2].
- **Delete the unused LoadImage nodes + their links + clear the `ref_image_N` link
  fields** when dropping images (see `build_2ref.py`).
- **Keep the 6-section structure but SHORT** — no 500-word bloat. The model needs the
  anchors + the motion, not an essay.
**Rule: for R2V, use 2-3 reference images max, each an explicit frame anchor for one
shot, with a simple prompt. If the character isn't doing the action, add a 3rd
reference showing that pose or strengthen the motion verb.** See D020.

### Holding the Krea2 style in MiniMax video (2026-08-28 lesson)

MiniMax H3 is a GENERAL video model — its prior smooths toward its own default look,
so the Krea2 angular brush-stroke style "completely went" in the video (held only the
first 2-3s). The turbo LoRA is a *speed* distillation, NOT a style LoRA. Reference
images only anchor the FIRST frame, so drift creeps in over 15s.
**Fix: generate a SET of Krea2-styled reference images first** (character sheet,
abstract, bridge, medium, close-up, water, running — see `jaisal_ref_prompts.txt`)
and feed 2-3 of them to the MiniMax R2V workflow so it holds the style across the
whole video. Do NOT use a frame-by-frame Krea2 i2i pipeline (extra work).
**Rule: for style-consistent video, build a Krea2-styled reference set first and feed
2-3 of it to MiniMax.** See D021.

### The Jaisal Cut character (2026-08-28 decision)

The character is a **normal young schoolboy with short dark hair** (face OK). Costume:
**rose-pink collared shirt, full-length black trousers, black school bag** (NOT the old
red bag / school uniform).
**Krea2 CANNOT make a faceless character** — it always renders a face (the faceless
idea was dropped 2026-08-28; user accepted a normal face).
**Krea2 quirks:** it tends to DUPLICATE the character (multiple kids) and can place
the boy IN THE RIVER instead of on the bridge. Every prompt says "ONLY ONE character,
no other people, no duplicates" and the bridge prompt pins him "ON THE BRIDGE DECK,
left side, NOT in the water". If it still duplicates/misplaces, re-run with a
different seed.
**Rule: normal boy (short dark hair), rose shirt, black pant, black bag, SINGLE
character, on the bridge.** See D022.

### Face consistency: Krea2 Identity Edit v1.2 (2026-08-29)

Krea2 t2i gives a DIFFERENT face every time the character appears. To lock the face
across a reference set, use `krea2_identity_edit.json` (**Krea2 Identity Edit v1.2**):
load a good reference (character sheet / clean close-up) in the LoadImage node, write a
plain-English instruction for the new scene, and it regenerates the scene keeping the
same face/identity. LoRA `krea2_identity_edit_v1_2.safetensors` + `comfyui-krea2edit`
node pack (both installed). **Key params:** `ref_boost` = 4.0 (fidelity dial — strong
face+body likeness; >10 over-copies, <1 suppresses the ref), KSampler 10 steps cfg 1
(turbo), `grounding_px` 384-768 (lower if compositions double/split), 1MP output.
**Rule: generate the base image with t2i, then lock the face with the identity-edit
workflow (ref_boost 4).** See D023.

**Skin-tone / lighting match (2026-08-29, D025):** the identity workflow carries the
REFERENCE image's color tone into the output — a neutral/bright character-sheet
reference makes the boy come out studio-lit, clashing with the dark moody scene.
**Fix: the style LoRA `Krea2_Cinematic_Artstyle.safetensors` @ 0.7 is now wired in as
node 95** (chain `55 → 71 identity LoRA → 95 style LoRA → 79 patch → 53 KSampler`).
Tune node 95: style too weak → 0.8-1.0; face distorts → 0.5. Also keep the lighting
words in the instruction ("moody overcast light"), and BEST use a reference that is
already in the moody scene (not the neutral character sheet) so the tone matches
automatically.

### Climate consistency (2026-08-29 rule)

Do NOT change the climate dramatically between shots. Once the rain starts, keep ONE
moody tone across all rain/water shots. The underwater shot must be DARK and moody
(matching the rain), NOT bright/sunny. A drastic light change breaks continuity and
MiniMax won't bridge it. Also: keep the bridge handrails SQUARE (not round/ornate/
staircase) and the river OPEN (not a canal/bund) in every prompt. See D024.

---

# Decision Preservation

Whenever the user says things such as:

- "Let's use this"
- "This is better"
- "Keep this"
- "Don't change this"
- "We should use..."
- "This works"
- "This doesn't work"
- "From now on..."
- "Let's stick with..."

consider whether this represents a persistent project decision.

If it does, update `DECISIONS.md`.

Do not wait for the user to remember to save it.

---

# Experiment Preservation

When a meaningful test produces a useful result, update `EXPERIMENTS.md`.

Include successful AND unsuccessful experiments.

Example:

> Qwen 3.6 27B Q6 + MTP produced ~170 tok/s under the current llama.cpp configuration. Quality was considered sufficient for workflow reasoning.

This should be recorded because it may influence future model/configuration decisions.

---

# Session End

When the user indicates that a session/task is finished, or asks to save progress:

1. Review what changed.
2. Update PROJECT_STATE.md.
3. Add important decisions to DECISIONS.md.
4. Add meaningful experiments to EXPERIMENTS.md.
5. Update WORKFLOW_HISTORY.md if workflows changed.

Do not write unnecessary historical information.

---

# Resuming Work

When starting a new session, do not ask the user to explain everything again.

First inspect the project memory.

Then provide a concise understanding of:

- Current objective
- Current setup
- Important decisions
- Last known successful state
- Current blocker
- Recommended next step

Then continue the work.

---

# Important Principle

The user's chat history is temporary context.

The project-memory files are persistent context.

Never rely on chat history when the required information can be stored in project memory.
