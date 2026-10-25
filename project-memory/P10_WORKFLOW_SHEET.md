# P10 workflow sheet — run these after the ComfyUI restart (2026-10-25)

> Format: **workflow — source (reddit/x/github/HF) — what we're aiming for / what to check.**
> All 9 items from the P10 batch. All models are local + verified. Workflows live in
> `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\`.
> **First: restart ComfyUI once (20 packs load — h3-relay + VNCCS_Utils are the new ones).**
> P9-batch workflows (`k2f_*_oneclick` ×8, `minimaxH3BackgroundSwap_v21a_LOCAL`,
> `VRGDG_MiniMaxH3_2Pass_MusicVideo_LOCAL` [D041 — other content only], `H3_Recast_LOCAL`,
> `MiniMax-H3-Character-Swap-Mask_LOCAL`, `withers_has_big_nattys_LOCAL` [audio OFF]) are
> listed in `P10_BATCH.md` "User post-restart checklist" — run those too if you haven't.

| # | Workflow / tool | Source (reddit / x / github / HF) | What we're aiming for — what to check |
|---|---|---|---|
| 1 | `FastH3_Omni_R2V_LOCAL.json` | HF `FastVideo/FastH3-Omni-Comfy` · X `x.com/BennyDaBall_OG/status/2113323686250106978` | **Fast omni R2V** (t2v + ref2v in one graph): 8 steps, cfg 1, shifts 12/3. Check: quality vs standard H3 at a fraction of the time (5090: 10 s @1344×768 ≈ 69 s). UNET `fasth3_omniref_qad_nvfp4_comfy` + pruned-int8 variant both local. |
| 2 | `CharSwap_v1.1_fro_LOCAL.json` | X `x.com/Alissonerdx/status/2111649216653148305` | **New character-swap LoRA (v1.1-fro) — COMPARE vs existing**: run the SAME clip through this and `MiniMax-H3-Character-Swap-Mask_LOCAL.json` (Akatz v1.5, our current swap) and judge likeness/identity. LoRA `minimax_h3_character_swap_v1.1_ref2va_fro` local. |
| 3 | `H3_HyperFlow_Fast_LOCAL.json` (+ refs `sol_h3_t2v.json`, `sol_h3_Sol-H3-Studio.json`) | GitHub `NVlabs/Sana` (sol-engine) + `models/minimax_h3/Sol-H3-ComfyUI` · X `x.com/xieenze_jr/status/2111123049571324395` + `x.com/PixelAigc/status/2113186476322324913` | **Faster MiniMax w/o quality loss.** Main: standard H3 + HyperFlow 8-step LoRA — works TODAY (validated 0 errors). Sol engine route = WSL2 only (`SolH3Generate` node) — reference workflows saved, not runnable on this box. Check: speed + any quality delta vs stock H3. |
| 4 | `RTX_Post_VFX_LOCAL.json` | GitHub `Comfy-Org/ComfyUI_Nvidia_VFX_Nodes` · blog `blog.comfy.org/p/nvidia-vfx-nodes-for-video-upscaling` | **Video upscale for post**: SR 2× → FrameGen ×2 → TrueHDR HLG chain. **Grainy outputs: set quality = `DENOISE_ULTRA` at same resolution** (the grain fix). Check: 2× upscale sharpness + frame-gen smoothness on an H3 clip. |
| 5 | `motion2mixamorig` (CLI + Blender — NOT a ComfyUI workflow) | GitHub `MaxLiu22/Motion2MixamoRig` · X `x.com/MaxLiu09/status/2109530569566744620` | **Motion out of video → 3D character animation.** Install done + doctor green. YOUR 3 assets: (1) SMPLX `SMPLX_NEUTRAL.npz` → `E:\minimax_workflow\Motion2MixamoRig\assets\body_models\smplx\`; (2) Mixamo FBX (Binary, T-pose) → `assets\mixamo\`; (3) one-person 5–20 s clip → `assets\video\`. Then `…\.venv\Scripts\python.exe -m motion2mixamorig.cli run --rig assets\mixamo\<Name>.fbx` (first run auto-downloads GVHMR ~5 GB) → `outputs\…\mixamo_character.glb` → Blender glTF import (hide Icosphere + armature). Movie use: Jaisal/Zidhan performance → 3D rig. |
| 6 | TTS-Audio-Suite **Qwen3-TTS engine** (node input `model_path = "local:Qwen3-TTS-12Hz-1.7B-CustomVoice"`) | HF `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` | **Audio pipeline A/B vs our OmniVoice.** 10 languages (NO Malayalam — IndicF5 stays the ML-native fallback), 9 premium stock timbres + natural-language style control, 3 s rapid clone on Base. Weights already in the suite dir (no re-download). Check: voice quality vs OmniVoice on a sample line; D050 = user-dubs → OpenVoice/RVC stays the movie path. |
| 7 | `H3-Person-Removal_LOCAL.json` | Reddit `reddit.com/r/StableDiffusion/comments/1x0kokb` | **Person remover (Krea2 duplicate fix)**: 24 fps source video (W/H divisible by 32, ~5 s) + **clean first frame** (person removed, same framing) into the green LoadImage + person description in the green CLIP node ("man in gray shirt"). Needs `h3-relay` pack (loads on restart). All 7 models local. Movie use: clean Krea2 duplicate-character refs + remove extras from plates. |
| 8 | `VNCCS_PoseStudio_QI2.1_REFERENCE.json` | Reddit `reddit.com/r/StableDiffusion/comments/1wmg9e8` · HF `MIUProject/VNCCS_PoseStudio_QI2.1` | **Pose-from-image → posed reference frames** (user: "amazing"): char1/char2 sheet + pose image → QI2.1-styled posed frames = R2V anchors. All models local + verified (3 LoRAs V1/V1.1/V2 + QI2.1 UNET/CLIP; VAE already had). `VNCCS_PoseStudio` node loads on restart. |
| 9 | `TTS_Suite_TTS_SRT_REFERENCE.json` · `TTS_Suite_ASR_SRT_Builder_REFERENCE.json` · `TTS_Suite_OmniVoice_REFERENCE.json` | GitHub `diodiogod/ComfyUI_ChatterBox_SRT_Voice` (evolved into **TTS-Audio-Suite v5.9.2** — already installed) | **The movie dubbing pipeline**: SRT-timed TTS node (line-accurate dubs, `smart_natural`, segment caching) · dub audio → ASR → SRT builder · OmniVoice (600+ languages — Malayalam candidate to A/B vs IndicF5). Ranked #1 audio orchestration layer over our pipeline. |

## After each run — record the verdict
Log the result (keep / drop / tweak + params) in `WORKFLOW_HISTORY.md` and say it in chat so
it gets persisted. The comparison items are **2 (vs v1.5 Akatz)** and **6 (vs OmniVoice/IndicF5)** —
those two need a verdict from you.
