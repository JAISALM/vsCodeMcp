# workflows/ — repo mirror of the reusable movie-production pipeline (reorg 2026-11-19)

**What this is:** mirror of the `movies/` subtree — the reusable production-pipeline
workflows (all models), so the repo holds them ("the reusable items should be stored
here so we can get the details from here").

**Canonical location (live, run from here):**
`E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\movies\`
Files here are MIRRORS — edit/fix the canonical file, then re-sync:

```
powershell -ExecutionPolicy Bypass -File "D:\models\vsCodeMcp\workflows\resync_workflows.ps1"
```

**Structure (92 files, 8 stage folders — full triage: `docs/WORKFLOW_TRIAGE_2026-11-19.md`):**
- `sheets/` (30) — character sheets, ALL models: Krea2 t2i/3-view/kit/frontal (incl.
  batch + PE3 prompt-expansion), H3 wide/fizgig/patreon/2-stage, Qwen-Image-2.1
  (PE-I2I GGUF, multi-angles, face i2i), VNCCS PoseStudio
- `identity/` (5) — face lock/refine: Krea2 identity-edit v1.2 (+ batch rig),
  H3 FaceRefine auto/manual (YOLO face detect), Zuanfilm face detailer
- `motion/` (21) — H3 video: R2V/turbo, FastH3 omni, HyperFlow, seamless 15s/30s,
  BG swap, camera v20, sam 2-char/cinematic, recast, char-swap ×2, pika flex ×6,
  viggle remake ×2
- `image/` (17) — H3 image (t2i/20MP/pose-ref), Krea2 duo (2-char) ×4, quad (4-char) ×5,
  raw recipe, 2-pass i2i ×2
- `grade/` (9) — Zuanfilm Retrolab (B&W emulsion/film grain — the 1950 grade),
  seedVR2 ×4 (2K master), person removal ×2, RTX Post VFX, RIFE interpolation
- `world/` (2) — pano angles (LC 360 View geometry layer), H3 world shot
- `audio/` (3) — TTS_Suite (D041-compliant — NO music, natural sounds only)
- `utility/` (5) — sheet composite, SDPose ×3, logo transparent (birefnet)

**`special/` is NOT mirrored** — 110 char-specific one-offs / tests / LoRA-training /
intro-video-era workflows live in the canonical dir only (repo rule: one-shot tests
and broken attempts are never committed).

**Format:** all UI format — open from the ComfyUI Workflows tab (subfolders show
nested). Run-order sheet: `P10_WORKFLOW_SHEET.md` (project-memory). R2V prompting:
`docs/MINIMAX_H3_R2V_PROMPTING_GUIDE.md`.

**Auto-committed** by `utilities/commit_md.ps1`; a corrupted file restores from git:
`git checkout <commit> -- workflows/movies/<stage>/<file>`.
