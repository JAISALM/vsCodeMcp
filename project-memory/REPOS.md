# GitHub Repos Catalog

Single source of truth: every GitHub repo we know about, what it is, and its status on
this machine. **Maintenance rule:** every time a new repo lands (P9 one-by-one queue),
add its row here in the same turn + commit. Status values: `installed` (in
`E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\` unless noted) /
`not installed` / `local clone` / `reference only`.

Updated 2026-10-24.

## Long-shot / continuation (MiniMax H3)

| Repo | What it is | Status |
|---|---|---|
| [HerrgottMargott/Herrgotts-H3-Infinite-Continuation-Suite](https://github.com/HerrgottMargott/Herrgotts-H3-Infinite-Continuation-Suite) | **PRIMARY long-shot tool (v1.4 verdict 2026-10-24).** FL2VA clip chain with native Masked AV continuation — previous clip's full AV latent copied in-place into next target, protected by core per-stream denoise masks (video prefix 0 / future 1; audio independently protected → dialogue continues past the seam). Auto Handover snaps to exact shared AV boundary (39/90/141/192 frames; default 39 ≈ 1.625 s @ 24 fps); Last-Frame quality resets; Net New Content duration mode; `StitchSavedChainV14` memory-bounded assembly. Core PR #15375 requirement VERIFIED in our v0.37.0; models 4/4 ✓. GPL-3.0. | **installed** + analyzed ✓ (2026-10-24). Examples + 11-clip demo → `E:\minimax_workflow\Herrgotts-H3-Infinite-Continuation-Suite\`. Not loaded (shared restart). |
| [xyzDist/H3-LongTakeNoCuts](https://github.com/xyzDist/H3-LongTakeNoCuts) | **Fallback for pure R2V oners.** 4 nodes fixing motion-context "photocopy effect" (segment 5–6 degradation) via few-step SAM3-masked REFINE resample (denoise 0.5–0.6) blended back at frames 22–44. Best for ONE continuous shot: 360° environment walk-throughs, intro oner. v2 = the one to use. Deps all satisfied (NikoDemon80 motion-context ✓ etc.). | **installed** + analyzed ✓ (2026-10-24). Examples → `E:\minimax_workflow\H3-LongTakeNoCuts\`. Not loaded (shared restart). |
| [NikoDemon80/ComfyUI-H3-Motion-Context](https://github.com/NikoDemon80/ComfyUI-H3-Motion-Context) | Native H3 motion-context extension (the correct non-fork; LongTakeNoCuts depends on it). | **installed** ✓ |
| [SatoDive/Minimax-H3-Latent-Continuation](https://github.com/SatoDive/Minimax-H3-Latent-Continuation) | Latent continuation for H3 (H3_ECOSYSTEM entry). | **installed** ✓ |
| [seitanism/ComfyUI-H3-Motion-Context-MultiRef](https://github.com/seitanism/ComfyUI-H3-Motion-Context-MultiRef) | Multi-reference variant of H3 motion context. | not installed (not needed yet) |
| Local H3 ecosystem packs (see H3_ECOSYSTEM.md for details) | `minimax-h3-chunk-star7`, `MiniMax_H3_Semantic_Bridge` / `minimax-h3-semantic-bridge`, [AIMixer/ComfyUI_MiniMaxH3_Director](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director), [Adudeguyman/ComfyUI-H3-Project-Suite](https://github.com/Adudeguyman/ComfyUI-H3-Project-Suite), [Nekodificador/ComfyUI-NKD-VFX-Tools](https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools), H3-Optimizations, H3-Relight-Minimax-ComfyUI, ComfyUI-Spectrum-MiniMax-H3, `3d-Camera-control-H3-Minimax`, `Minimax-H3-Latent-Continuation` | chunk-star7 ✓ · semantic-bridge ✓ · H3-Project-Suite ✓ · NKD-VFX ✓ · H3-Optimizations ✓ · H3-Relight ✓ · Spectrum ✓ · 3d-Camera ✓ · **AIMixer Director = not installed** |

## Character / consistency / sheets

| Repo | What it is | Status |
|---|---|---|
| [lumosai8/ComfyUI-OrbitSheets](https://github.com/lumosai8/ComfyUI-OrbitSheets) | FREE OrbitSheets node — character template WITH VOICE audio + LOCATION template (360° location orbit). Needed for P2 `LocationOrbitSheetH3.json`. Also has the character sheet template. | **not installed** (P2 needs it) |
| [nicekriss/toobusy](https://github.com/nicekriss/toobusy) | 2BZ 2-stage H3 character sheet (ref2va: face+outfit → front/side/back + optional action panels, 16:9 composite). Publisher `neobabae`, needs ≥ v0.4.9. Public workflow: [2BZ_H3_character_sheet_2stage_v1_EN.json](https://github.com/nicekriss/toobusy/blob/main/docs/workflows/2BZ_H3_character_sheet_2stage_v1_EN.json). | **installed** ✓ (toobusy in custom_nodes) |
| [krea-ai/krea-2](https://github.com/krea-ai/krea-2) | Official Krea 2 repo — README verified for Krea2 model facts (DECISIONS.md). | reference only |
| [shootthesound/ComfyUI-Fizgig-H3-Still](https://github.com/shootthesound/ComfyUI-Fizgig-H3-Still) | Fizgig H3 Still (4096×1536 18 steps ≈ 1 min on 5090; PROVEN). | **installed** ✓ |
| Local: `ComfyUI-Fizgig-H3-Tweaks`, `ComfyUI-H3-FaceRefine`, `ComfyUI-H3-Multishot`, `ComfyUI-H3-NativeAudioLock`, `ComfyUI-H3-Prompt-IDE`, `ComfyUI-H3-Edit` (MiniMax-H3-Edit), `ComfyUI-Minimax-H3-Extender` | H3 feature packs in custom_nodes (audio lock = relevant to D041 + P1). | **installed** ✓ (public repo URLs not recorded) |

## Krea2 stills

| Repo | What it is | Status |
|---|---|---|
| [Shrey-1o1/ComfyUI-Krea2-FilmStudio-Vionex](https://github.com/Shrey-1o1/ComfyUI-Krea2-FilmStudio-Vionex) | "KREA 2 Film Studio" (VIONEX) — all-in-one local Krea2 cinematic stills: ONE `Krea2OneNode` (T2I/I2I/Control/IdentityEdit) expanding into NATIVE ComfyUI nodes at queue time; no external KREA API. 10 VIONEX style bundles, resolution buckets (optimal 1928×1088 16:9; Krea 1024/832×1216/1216×832/2048), multi-ref encode, 2-stage low-denoise refine sampling, RES4LYF default sampler. Shipped workflow `Vionex - Krea 2 Film (V.02).json` = 1 node + 3 notes. **Stills-only — no MiniMax nodes; the "minimax loop" = our own still→H3 handoff (the movie flow).** | **installed** + analyzed ✓ (2026-10-24, via reddit r/StableDiffusion 1vn7avz). Deps ✓ (RES4LYF/krea2edit/T-Enhancer/GGUF); only `comfyui-krea2-controlnet` missing (= optional CONTROL sub-feature). Models ✓ (`krea2_turbo_fp8_scaled`, `qwen3vl_4b_fp8_scaled`, `krea2RealVae_v10`). Not loaded (shared restart), not run. |
| [ClownsharkBatwing/RES4LYF](https://github.com/ClownsharkBatwing/RES4LYF) | Recommended sampler backend for Krea2 (Film Studio's default; `ClownsharKSampler_Beta` two-node chain). | **installed** ✓ |
| [city96/ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) | GGUF quantized diffusion models + text encoders for ComfyUI. | **installed** ✓ (+ ComfyUI-GGUF-nif0) |
| Local Krea2 packs: `comfyui-krea2edit` (Identity Edit v1.2, ref_boost 4.0 — D023), `ComfyUI-Krea2T-Enhancer`, `ComfyUI-krea2-negpip`, `one-node-flux-2-klein` (the one-node pattern FilmStudio was modeled on) | Krea2 edit/encode/negative-prompt/one-node packs. `comfyui-krea2-controlnet` = **NOT installed** (needed only for FilmStudio CONTROL sub-feature). | installed ✓ (public repo URLs not recorded) |

## Audio

| Repo | What it is | Status |
|---|---|---|
| [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) (local clone `D:\models\ai-movie\repos\rvc-webui`) | **The P1 dubbing engine** — RVC voice conversion (NOT TTS; D050). venv `D:\models\ai-movie\envs\rvc` (py3.12, torch 2.7.1+cu128). Recipe: `--f0_method rmvpe --protect 0.3-0.5 --alpha 0.1-0.2`. | **local clone** ✓ |
| [ai4bharat/IndicF5](https://github.com/ai4bharat/IndicF5) | Indic F5-TTS (parked — TTS route for kids content, not the movie). Install ref: `pip install git+https://github.com/ai4bharat/IndicF5.git` | reference only |
| [Anujatk1999/open-media](https://github.com/Anujatk1999/open-media) | "Shot Composer" — intro-video repo (see INTRO_VIDEO_PRODUCTION.md). | reference only (clone in `D:\models\ai-movie\repos\` if used) |

## Video editing (NLE / timeline AI editing)

| Repo | What it is | Status |
|---|---|---|
| [PxTicks/vlo](https://github.com/PxTicks/vlo) (local clone `D:\models\ai-movie\repos\vlo`) | **Free local open-source AI video editor** (AGPL-3.0, v0.3.0). Full-stack web app: React/TS frontend (PixiJS + mediabunny/webcodecs) + Python FastAPI backend; runs in Chromium browsers (Edge/Chrome) at `http://127.0.0.1:6332` (`run.bat`). Frame-accurate NLE: color grading, keyframes/splines, transitions, blending modes, motion paths, mask algebra, beat detection. **AI: SAM2 point masking + auto crop/stitch for video inpainting; SAM-Audio semantic stem separation (P1-relevant); LIVE ComfyUI bridge — sends timeline selections/images/videos to ComfyUI with automatic aspect-ratio adjustment and runs any workflow back onto the timeline.** Ships default timeline-editing workflows with `.rules.json` sidecars: `vlo_minimax_h3_{i2v, inpaint, inpaint_flf2va, masked_guide, r2v, ttm, fun_controlnet_union}`, `vlo_krea2_turbo` (our P4 stills), `vlo_klein_multi` (our P3!), `vlo_gimm_vfi` (frame interpolation), `vlo_ltx2_5_{inpaint, clean_plate, ic_edit}`, `vlo_qwen_image_2_1_edit`. **Install** (git prerequisite only): `install.bat -y --profiles all --cuda-torch` provisions vlo-managed Node 22.22.1 + Python 3.13.12 (uv) + npm ci + frontend build + backend venv + CUDA 13.0 torch + SAM2 + SAM-Audio. **Integration with OUR ComfyUI:** point vLo at `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI` (folder with `main.py`) on first launch; vLo does NOT install nodes into a foreign ComfyUI → run `python scripts/install-comfyui-nodes.py --comfyui-dir <our ComfyUI>` in our venv. **Node packs:** have LTXVideo/Spectrum-MiniMax-H3/VideoHelperSuite/KJNodes ✓; MISSING (being installed): kijai/ComfyUI-WanVideoWrapper, PxTicks/ComfyUI-vlo (the bridge node), Fannovel16/comfyui_controlnet_aux, kijai/ComfyUI-GIMM-VFI → **add to the shared restart list (P7)**. Models fetched in-app (workflow models → `<ComfyUI>/models`, SAM2 checkpoints, SAM-Audio; HF-gated → token). Env: `COMFYUI_URL` (default = our 127.0.0.1:8188), `COMFYUI_INSTALL_DIR`, `SAM2_DEVICE`, `SAM2_MAX_PROPAGATION_FRAMES` (default 900). vLo-launched ComfyUI gets `--enable-manager --preview-method latent2rgb`. Update = `update.bat`. **Movie relevance:** background replacement (item 2 = SAM2 + H3 inpaint workflows), long shots (item 6 = H3 i2v/r2v on timeline + VFI), character replacement (items 4/5), P1 audio stems, DaVinci-complement grading. | **local clone** ✓ (2026-10-24). Full-capability install RUNNING (background job; log `D:\models\ai-movie\logs\vlo_install.log`); node-pack install job (log `vlo_nodes_install.log`). NOT yet run — user opens `run.bat` → point at our ComfyUI. |

## H3 ecosystem index

[H3_ECOSYSTEM.md](H3_ECOSYSTEM.md) carries the deeper per-repo notes for the H3 packs
(Director, Project-Suite, lumibelle, Motion-Context, LongTakeNoCuts, Latent-Continuation,
MultiRef, NKD-VFX, etc.).
