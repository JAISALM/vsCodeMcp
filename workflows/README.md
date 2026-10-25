# workflows/ — repo mirror of reusable ComfyUI workflow JSONs (2026-10-25)

**What this is:** copies of the reusable workflows, so the repo holds them
("the reusing items should be stored here so we can get the details from here").

**Canonical location (live, run from here):**
`E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\`
The files here are MIRRORS — edit/fix the canonical file, then re-sync:

```
powershell -ExecutionPolicy Bypass -File "D:\models\vsCodeMcp\workflows\resync_workflows.ps1"
```

**Contents (35 files):**
- **P10 batch:** `FastH3_Omni_R2V_LOCAL.json` · `CharSwap_v1.1_fro_LOCAL.json` ·
  `H3_HyperFlow_Fast_LOCAL.json` · `sol_h3_t2v.json` + `sol_h3_Sol-H3-Studio.json`
  (Sol engine = WSL2-only reference) · `RTX_Post_VFX_LOCAL.json` ·
  `H3-Person-Removal_LOCAL.json` + `H3-Person-Removal-Relay-V2_REFERENCE.json` ·
  `VNCCS_PoseStudio_QI2.1_REFERENCE.json` (see sheet) · `TTS_Suite_{TTS_SRT,ASR_SRT_Builder,OmniVoice}_REFERENCE.json`
- **P9 batch:** `k2f_*` (Jaisal/Zidhan one-click sets ×~18) ·
  `minimaxH3BackgroundSwap_v21a_LOCAL.json` · `VRGDG_MiniMaxH3_2Pass_MusicVideo_LOCAL.json`
  (D041 — other content only) · `H3_Recast_LOCAL.json` ·
  `MiniMax-H3-Character-Swap-Mask_LOCAL.json` · `withers_has_big_nattys{,_LOCAL}.json`

**Format:** all UI format (top-level `nodes` list + `links`) — open in the ComfyUI
Workflows tab. See `P10_WORKFLOW_SHEET.md` (project-memory) for the run-order sheet
with sources + what to check per workflow.

**Auto-committed** by `utilities/commit_md.ps1` (daily 22:30 task + on-demand), so a
corrupted local file restores from git: `git checkout <commit> -- workflows/<file>`.
