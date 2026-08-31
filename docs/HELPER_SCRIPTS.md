# Helper Python Scripts — Knowledge Transfer

Last updated: 2026-08-27

## Why these scripts exist

Three constraints forced us to work through **script files** instead of inline commands:

1. **PowerShell mangles inline Python** — quoting `python -c "..."` with special chars
   (quotes, backslashes, `**`, newlines) breaks in PowerShell 5.1. Script files avoid all of it.
2. **ComfyUI workflow JSON is huge** — reading it in the chat floods context. Scripts print
   only the fields we need (node types, widgets, links).
3. **`object_info` JSON has duplicate keys** — breaks PowerShell's `ConvertFrom-Json`;
   Python's `json` module handles it fine.

**Rule of thumb:** any time you need to inspect or modify a workflow JSON, or check
models/modules, write a small script in `d:\models\vsCodeMcp\utilities\` and run it
with the embedded Python:

```
& "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\<script>.py"
```

**Workspace layout (reorganized 2026-08-31):**
- `utilities/` — all helper Python scripts + `run_2mp_benchmark.bat`
- `prompts/` — all prompt `.txt` files (`jaisal_sketch_prompts.txt`, `jaisal_ref_prompts.txt`, …)
- `docs/` — reference docs (`CAMERA_SHOT_VOCABULARY.md`, `MINIMAX_H3_R2V_PROMPTING_GUIDE.md`, this file)
- `data/` — data artifacts (`object_info_cache.json`, `vram_monitor.csv`, `analyze_out.txt`)
- `project-memory/`, `workflow_backups/` — unchanged

---

## The scripts

### Workflow inspection (read-only)

| Script | What it does |
|---|---|
| `analyze_minimax.py` | Dumps node-type counts + key-node widgets + LoadImage links for `mini-max-refrance-to-video-1.json`. First look at the original MiniMax template. |
| `analyze_minimax2.py` | Dumps every link (from→to with node types) and what feeds the key nodes (46 SaveVideo, 75 MiniMax, 37 CreateVideo, 72 RTX upscale, 74 VHS combine) + full MiniMax widgets. Used to map the template's wiring before cloning it. |

### Workflow builders / fixers (write)

| Script | What it does |
|---|---|
| `setup_minimax_test.py` | Created `mini-max-jaisal-test.json` from the template: pointed the two LoadImage nodes at `jaisal_mm_start.png` / `jaisal_mm_final.png` and set the drone-ascent prompt on the MiniMax node. (Superseded — that workflow crashed on the sage node.) |
| `fix_minimax_bypass.py` | Bypassed the triton-dependent optimization chain (45 SageAttention → 47 EasyCache → 49 TorchCompile) in `mini-max-jaisal-test.json`: rewired links 67/68 so the raw UNET (node 1) feeds the guider/scheduler directly, set the 3 nodes to mode=4 (bypassed). |
| `build_optimized_workflow.py` | **The main builder.** Clones `video_minimax_h3_r2v+turbo.json` → `jaisal_drone_optimized.json` and applies: UNET→fl2va, LoRA→turbo 4-step, inserts `MiniMaxH3ActivationChunkStar7` (CK INT8) into the model chain, MiniMax node → 864×480/362 frames + drone prompt, refs → jaisal start/final, inserts `RTXVideoSuperResolution` (2× ULTRA) before CreateVideo, save prefix `video/Jaisal_Drone`. |
| `fix_named_widgets.py` | **Critical bug fix.** The new ComfyUI frontend prefers `widgets_values_named` over positional `widgets_values`; the builder only updated the positional list, leaving stale named values (1344×768/124 frames, wrong LoRA/refs/prompt). This script syncs `widgets_values_named` on all 7 modified nodes (136, 127, 146, 137, 139, 138, 92). **Lesson: when editing workflow JSON, ALWAYS update both `widgets_values` AND `widgets_values_named`.** |
| `build_title_moody.py` | Builds `krea2_jaisal_title_moody.json` from the `krea2_jaisal_medium.json` template: LoadImage→`jaisal_title_scene.png`, moody-climate positive prompt, KSampler denoise 0.4 (atmosphere-only), SaveImage prefix `jaisal_cut/title_moody`. |
| `fix_title_moody.py` | (Superseded by `fix_native_shape.py`.) First fix attempt — rebuilt `krea2_jaisal_title_moody.json` with 6-value KSampler / 1-value LoadImage arrays matching the API `/object_info` order. **This was WRONG** — see `fix_native_shape.py` below. |
| `fix_native_shape.py` | **THE real fix (2026-08-27).** The API `/object_info` widget order is missing HIDDEN widgets, so machine-built `widgets_values` arrays were too short and shifted: KSampler needs **7** values `[seed, control_after_generate, steps, cfg, sampler_name, scheduler, denoise]` (the hidden `control_after_generate` = randomize/fix/+1/-1 dropdown next to seed), LoadImage needs **2** values `[filename, "image"]`. This script sets those native shapes on `krea2_jaisal_title_moody.json` and **removes all `widgets_values_named` keys** (native UI-saved files don't have them). Verified against native files (`krea2_jaisal_base.json`, `mini-max-refrance-to-video-1.json`) + MCP validation. **Lesson: copy `widgets_values` shapes from NATIVE UI-saved workflows, never from `/object_info`.** |
| `diag_widget_order.py` | Extracts the true `widgets_values` shapes for every node type from native UI-saved workflows (the ground truth for hidden widgets). |
| `diag_struct.py` / `diag_native_nodes.py` / `diag_native.py` | Structural diagnostics: native vs converted node field comparison, native node dumps, and a full workflows-folder format/shape inventory. |
| `inventory_machine_built.py` | Dry-run inventory of all 21 machine-built workflows: per-node `widgets_values` length vs expected native length, flags mismatches. Run BEFORE `fix_all_widget_shapes.py` to scope the fix. |
| `fix_all_widget_shapes.py` | **THE comprehensive fix (2026-08-27).** Applies the native widget shape to ALL 21 machine-built workflows: KSampler 6→7 (insert hidden `control_after_generate`=`"randomize"` at index 1), LoadImage 1→2 (append literal `"image"`), removes ALL `widgets_values_named` keys. Backs up every original to `d:\models\vsCodeMcp\workflow_backups\pre_widget_fix\` first. 435 changes total. All 21 re-validated via MCP (`valid: true`, 0 errors). **This is the fix for the "KSampler cfg=euler / scheduler=0.4 / no details in UI" bug that affected every machine-built workflow.** |
| `scan_combo_inputs.py` | Scans all machine-built workflows for widget inputs whose `type` is a STATIC LIST (stale combo snapshot) instead of `'COMBO'`. Reports which (node_type, input_name) pairs are affected. |
| `fix_combo_inputs.py` | **Fixes the LoadImage "can't select/see image" bug (2026-08-27).** Sets every static-list widget input `type` to `'COMBO'` (so the frontend populates dropdowns from the server live) and adds the missing `upload` input (`type='IMAGEUPLOAD'`, the "choose file to upload" button) to every LoadImage node. 253 combo fixes + 37 upload inputs across all 21 workflows. Backups in `d:\models\vsCodeMcp\workflow_backups\pre_combo_fix\`. All re-validated via MCP. **Without this, LoadImage shows the right filename but has no dropdown/upload button in the UI.** |
| `inspect_user_node.py` / `diff_loadimage.py` | Inspect the user-added native LoadImage node (id=31) in `krea2_jaisal_title_moody.json` and field-by-field diff it against the converted node. Confirmed the converted node is now structurally identical to native (COMBO image + IMAGEUPLOAD upload inputs). |
| `wire_user_node.py` | Wires the user's native LoadImage node (id=31) into `krea2_jaisal_title_moody.json` as the active image selector: points it at `jaisal_title_scene.png`, rewires link 4 (`31→FKI2I:vae`), removes the redundant `FKI2I:img` node. |
| `fix_title_moody_prompts.py` | **Pose-drift fix (2026-08-27).** For `krea2_jaisal_title_moody.json`: denoise 0.4→0.3 (preserve pose), positive prompt anchors pose to reference ("EXACTLY matching the reference pose and head angle", pose as static state not new action), negative prompt replaces vague "different head position" with concrete pose-locking terms. See AGENTS.md "i2i pose/atmosphere edits". |
| `build_lowangle.py` | **Builds `jaisal_lowangle.json` (2026-08-27).** MiniMax H3 R2V low-angle ending workflow from the `video_minimax_h3_r2v+turbo.json` template: ref2va UNET + ref2v turbo LoRA, 5 LoadImage nodes (1.png–5.png) wired to `ref_image_0`–`ref_image_4`, 15s, 1344×768, Save prefix `video/Jaisal_LowAngle_1_2_3_4_5`. |
| `fix_lowangle_wiring_and_prompt.py` | **Fixes the 5-image wiring + rewrites the prompt (2026-08-27).** Sets the `link` field on `ref_image_3`/`ref_image_4` by SLOT INDEX (6/7, not name number 3/4) so all 5 images wire correctly (D018). Rewrites the prompt to the official MiniMax H3 R2V style: `<Picture 1>`–`<Picture 5>` frame anchors, `<Subject 1>` boy / `<Subject 2>` bridge, 6-section structure, 5 timed `[Shot N]` blocks (D017). Backs up to `*.pre_wiring_fix.bak`. |
| `verify_lowangle_wiring.py` | Read-only trace of `jaisal_lowangle.json`: which LoadImage feeds each `ref_image_N`, and whether each ref input's `link` field is set. Use to confirm all 5 images are wired. |
| `download_ref2v_lora.py` | Downloads `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` (1.96 GB) into the main models path. |
| `reapply_lowangle_prompt.py` | Re-applies the R2V-style prompt to `jaisal_lowangle.json` node 138 after the ComfyUI frontend re-saved the file and reverted the prompt. (Node IDs are INTS, not strings — match with `str(n["id"])`.) |
| `build_single_shot.py` | **Builds `jaisal_single_shot.json` (2026-08-28).** From the `video_minimax_h3_i2v` template: ONE LoadImage = `1.png` → `MiniMaxH3ImageToVideo` (fl2va), 15s, 1344×768 (16:9 0.98MP), turbo 4-step. Simple single-shot prompt (boy walks → rain → runs → jumps into river → camera dips underwater). Save prefix `video/Jaisal_SingleShot`. |
| `fix_single_shot.py` | **Fixes `jaisal_single_shot.json` (2026-08-28).** Updates the instance node's `widgets_values` AND `widgets_values_named` (prompt, duration=15, turbo=True, lora=4step, steps=4) + fixes the `ResolutionSelector` aspect typo (`Widescreeen`→`Widescreen`). NOTE: the LoRA is ALSO on the internal subgraph node 121 — fixed separately (see D019). |
| `build_2ref.py` | **Rebuilds `jaisal_lowangle.json` as a 2-image R2V (2026-08-28).** Deletes the 3 unused LoadImage nodes (143=3.png, LA4=4.png, LA5=5.png) + their links (285/289/290), clears `ref_image_2/3/4` link fields on the MiniMax node, writes a SIMPLE 2-anchor prompt (`<Picture 1>` = 1.png start-of-bridge → [Shot 1], `<Picture 2>` = 2.png middle-of-bridge → [Shot 2]), save prefix `video/Jaisal_2Ref_1_2`. Backs up to `*.pre_2ref.bak`. **Lesson (D020): 2-3 refs max + simple prompt beats 5 refs + 500-word essay.** |
| `build_krea2_refs.py` | **Builds `krea2_jaisal_refs.json` (2026-08-28).** Clones `krea2_jaisal_base.json` (Krea2 t2i) into a reference-image generator: default positive prompt = the FACELESS character sheet (head + hair, no facial features, rose-pink collared shirt, black trousers, black school bag), negative = faceless/consistency negatives, 2048×1152, save prefix `jaisal_cut/refs`. **Purpose (D021): generate a Krea2-styled reference SET to feed to MiniMax so it holds the style across the whole video.** Companion file: `jaisal_ref_prompts.txt` (7 ready-to-paste prompts: character sheet, abstract, bridge, medium, close-up, water, running). |

### Environment checks (read-only)

| Script | What it does |
|---|---|
| `check_modules.py` | Imports candidate attention modules and reports installed/missing. Result: `torch 2.12.0+cu130` OK, `comfy_kitchen` OK, but `triton`/`sageattention`/`flash_attn`/`xformers` all MISSING. |
| `inspect_kitchen.py` | Dumps the `comfy_kitchen` package API (location, `int8_attention`, `flash_attention`, `sage_attention` submodules, quantize/dequantize helpers). Confirmed it's the INT8 attention backend, not a node pack. |

### Downloads

| Script | What it does |
|---|---|
| `download_turbo_lora.py` | Downloads `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors` (1.96 GB) from HuggingFace (Comfy-Org/MiniMax-H3) directly to the **main model path** `E:\ComfyUI_windows_portable\ComfyUI\models\loras\`. Needed because the MCP `download_model` tool targets comfy-cli's default workspace (`C:\Users\user\Documents\comfy\ComfyUI`), NOT our main path. |

### Memory maintenance

| Script | What it does |
|---|---|
| `update_workflow_history.py` | Appends the `jaisal_drone_optimized.json` entry to `project-memory/WORKFLOW_HISTORY.md`. (Used because inline PowerShell heredocs with triple-quoted strings break.) |

### Workflow format diagnosis / conversion (2026-08-27)

| Script | What it does |
|---|---|
| `diagnose_workflow_format.py` | Classifies every workflow in the workflows folder as **UI** vs **API** format. UI = `nodes` is a list (renders in ComfyUI). API = top-level dict of `{node_id: {class_type, inputs}}` (shows EMPTY canvas in the UI). |
| `scan_broken.py` | Lists all node types + dict-valued inputs across the API-format files (to scope the converter). |
| `convert_api_to_ui.py` | **Converts API-format workflows to UI format** (the universal format that renders in the UI AND works in MCP). Backs up each original as `<name>.json.api.bak` before overwriting. Uses `object_info_cache.json` schemas for input/output types and widget ordering. Emits both `widgets_values` (positional) and `widgets_values_named` (dict). |
| `object_info_cache.json` | Cached `/object_info` from the live server (node schemas: input types, output types, `input_order`). Refresh by re-fetching if new node packs are added. |

### Output artifacts

| File | What it is |
|---|---|
| `analyze_out.txt` | Captured stdout from an early analysis run (MiniMax template node dump). |

---

## Key facts these scripts established (for future sessions)

- **`comfy_kitchen`** = the "ComfyUI-Kitchen" INT8 attention backend (installed in embedded Python). The node pack that wires it in is **Star7** (`minimax-h3-chunk-star7`, cloned into `custom_nodes`, node `MiniMaxH3ActivationChunkStar7`).
- **`triton` missing** → KJNodes `PathchSageAttentionKJ` crashes (`No module named 'triton'`). Sage path is dead on this setup.
- **`torch 2.12.0+cu130`** (CUDA 13.0). ComfyUI runs with `--use-pytorch-cross-attention`.
- **MCP `download_model` writes to the wrong workspace** — use `download_turbo_lora.py`-style direct downloads to `E:\ComfyUI_windows_portable\ComfyUI\models`.
- **ComfyUI is not under comfy-cli control** (portable launcher) → MCP `restart_comfyui` fails; restart manually (Stop-Process the `main.py` PID, relaunch with the same args).
- **Workflow JSON gotcha:** `widgets_values` (positional) and `widgets_values_named` (dict) can disagree; the frontend may prefer the named one. Update both.
- **CRITICAL — workflow format:** ComfyUI's UI (drag-drop + Workflows tab) only renders **UI format** (`nodes` = list of node objects + `links` array). **API/prompt format** (flat dict `{node_id: {class_type, inputs}}`) shows an **empty canvas** when dragged. MCP `run_workflow`/`validate_workflow` accept BOTH (they convert UI→API internally), so **always save workflows in UI format** — it's the universal format. When building a workflow from scratch, emit UI format. If a file is API format, run `convert_api_to_ui.py` on it. (All 19 previously-broken jaisal/krea2 workflows were converted 2026-08-27; originals kept as `*.json.api.bak`.)
