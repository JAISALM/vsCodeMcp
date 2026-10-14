# H3 Ecosystem Reference (2026-10-05)

Reference catalog of MiniMax H3 community tools the user shared. Check here
whenever a chaining/consistency/VFX issue comes up. All URLs verified 2026-10-05.

## Status legend
- ✅ INSTALLED (in `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes`)
- ⏳ PLANNED / DEFERRED
- ❌ DROPPED

## The 9 shared repos

### 1. AIMixer/ComfyUI_MiniMaxH3_Director — ⏳ DEFERRED
- URL: https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director
- All-in-one multi-segment "director console" node (Chinese README, EN available).
- Features: multi-segment timeline (split/even-split/PySceneDetect smart shot split),
  task types t2v/i2v/fl2v/r2v/v2v/rv2v, first-last-frame groups with inter-segment
  guidance (last N frames of prev segment), reference material groups (images 1-9,
  audio 1-3, video 1-3 per group, `<Picture N>`/`<Video K>`/`<Audio J>` refs),
  select-run (only run checked segments), external group wiring, native stereo audio.
- Built on official MiniMaxH3ImageToVideo/ReferenceToVideo + SigmaShift + KSampler.
- VERDICT: likely redundant with Project Suite + Motion Context; revisit only if
  we need the PySceneDetect auto-split or the all-in-one UI.

### 2. Adudeguyman/ComfyUI-H3-Project-Suite — ✅ INSTALLED (2026-10-05)
- URL: https://github.com/Adudeguyman/ComfyUI-H3-Project-Suite
- Project MANAGER for long H3 videos, one clip at a time.
- Default LATENT mode: clips handed to next clip in model's internal format (no
  decode/re-encode between clips → no compounding quality loss).
- Context window manager: create/automate extensions without disrupting your own
  prompt editors/media loaders. Project manager panel: review, compare takes,
  approve next clip, one-click export.
- v1.5.0: drift report includes SOUND (loudness/hiss/high-end per clip — voice
  wearing down shows as a number). ANCHOR LATENT: feeds clip 1's sound to every
  later clip as reference (keeps voices sounding like themselves down a chain).
- v1.4.2: "Hold framing" toggle (keeps prev shot's framing after overlap ends;
  off by default, can leave slight ghost at seam).
- v1.4.0: import your own footage (live-action plate/other model/master) as a clip;
  export from latents (rebuild master from saved latents — cleaner joins, slower);
  one picture size per project (Hub takes/gives width+height).
- Works inside SwarmUI (v1.5.1 fix).
- VERDICT: ⭐ the project manager for the festival film.
- Companion repos by same author: ComfyUI-Fantastic-MiniMaxH3-PromptBuilder,
  comfyui_fantastic-loras.

### 3. lumibelle (radiatingreverberations) — ❌ DROPPED
- URL: https://github.com/radiatingreverberations/lumibelle · site: https://lumibelle.ai
- .NET 10 desktop app: screenplay → cast/locations as reference images → compose
  and generate shots → cut together. Windows x64 unsigned preview build.
- ESCAPES ComfyUI (own pipeline, localhost:5183, .NET 10 SDK, MAUI host).
- VERDICT: user does NOT want to escape ComfyUI. Dropped.

### 4. omnichar — H3 consistent character workflow — ⏳ TRY NEXT
- URL: https://www.omnichar.org/workflows/minimax-h3-guided-consistent-characters-via-reference-identity-face-body-cloths
- NOT a node pack — a WORKFLOW (omnichar.org / Inline Studio canvas).
- Guides character with consistent face/body/cloths: up to 9 reference images
  ported into face/body/cloth reference slots → builds portable `.char` file
  (saved under `/core/model/characters`) → reuse across workflows via
  Load Character node → Add Prompt → H3 Ref2VA node.
- Models needed: minimax_h3_ref2va_pruned_fp8_scaled.safetensors,
  qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors, minimax_h3_video_vae_fp16,
  minimax_h3_audio_vae_fp32, face_detection_yunet_2023mar.onnx,
  face_recognition_sface_2021dec.onnx, dinov2-base folder.
- Prompting: NAME your character (e.g. "emmy"), encode all features in the
  character prompt, trigger by name only in generation prompt. Cropped refs
  (body shots face-cropped; face = different angle; cloths separate top/bottom).
- VERDICT: ⭐ H3-native character consistency — complements our Krea2 Identity
  Edit (stills). We've never tried it. Test with Jaisal (rose shirt, black pant,
  black bag).

### 5. NikoDemon80/ComfyUI-H3-Motion-Context — ✅ ALREADY INSTALLED
- URL: https://github.com/NikoDemon80/ComfyUI-H3-Motion-Context
- Chain H3 clips so motion AND sound keep going across the cut.
- Slices prev clip's tail straight from its LATENT (bit-for-bit, no pixel
  round-trip). Audio window ENDS at the join and reaches BACKWARDS into sound
  that already played (true continuation, not soundalike).
- Nodes: H3 Motion Context (context_latent), Trim (wire trim_frames),
  Save/Load Latent pair (clip_index: Load 0 = first clip, Save 1; next: Load 1,
  Save 2), Seam Probe (measures if join is real continuation or imitation),
  Chain node (use instead of Run button — only sees Load/Save if all three in
  SAME canvas group).
- Requires ComfyUI 0.34.0+ (arbitrary keyframe anchors). We run 0.37.0 ✓.
- VERDICT: ⭐ clean base chaining engine. Already in custom_nodes.

### 6. HerrgottMargott/Herrgotts-H3-Infinite-Continuation-Suite — ⏳ DEFERRED
- URL: https://github.com/HerrgottMargott/Herrgotts-H3-Infinite-Continuation-Suite
- Long H3 videos from connected FL2VA (first-last-frame) clips.
- v1.4: Native Masked AV continuation — copies prev latent directly into new
  target, protected by ComfyUI native separate video/audio denoise masks.
  Freeze-safe handover (finds safe pre-freeze video endpoint, snaps to exact
  Masked-AV boundary). Audio may continue beyond video boundary (dialogue
  protection). Net New Content default duration mode.
- Exact AV context lengths: 39/90/141/192/... frames (default 39 ≈ 1.625s).
  Requires current ComfyUI build with PR #15375.
- Repeated Last Frame keyframes = quality resets (pull composition/identity back
  toward clean reference before drift accumulates). Memory-bounded Saved Chain
  Stitcher for very long projects.
- VERDICT: for VERY long sequences / when #5+#7 aren't enough. Defer.

### 7. SatoDive/Minimax-H3-Latent-Continuation — ✅ ALREADY INSTALLED
- URL: https://github.com/SatoDive/Minimax-H3-Latent-Continuation
- Fork of nkxx188/ComfyUI-MiniMaxH3-Easy. Native latent chaining, zero quality
  loss (raw uncompressed latents passed between shots).
- DUAL-REFERENCE: `Seed Video` (temporal transition guide = tail of prev clip)
  + `Seed Ref Video` (macro context = earlier wide master shot of room layout →
  changing camera angles doesn't break environment).
- Auto last-frame trim & stitch (finds transition boundary, joins clips into one
  file). Subject Weight Modulation (lower ref strength on recurring subjects so
  new characters get focus). Latent Save/Load by label.
- Roadmap v2: one-shot multi-segment (master prompt → 6+ clips auto-chained).
- VERDICT: ⭐ the ENVIRONMENT consistency tool (room layout across angles).
  Already in custom_nodes.

### 8. seitanism/ComfyUI-H3-Motion-Context-MultiRef — ⏳ PLANNED (superset of #5)
- URL: https://github.com/seitanism/ComfyUI-H3-Motion-Context-MultiRef
- Modified fork of #5 + multi-ref + latent masking + music video + motion
  transfer + custom keyframes. Update 9 (2026-09-05): streamed-output memory
  retention fixes, spatial masks, AV Bridge timing, dated output folders.
- Constraints: constant 24 fps input videos. AV Bridge contexts = 39+51k frames
  (39/90/141/192...), target lengths = 5+17k, start 192 target/39 context.
  V2V fractional strength quantized to 1/4096 steps (start 0.9995, denoise 1.0).
- ⚠️ INSTALL CONFLICT: when testing, REPLACE the existing #5 pack directory
  rather than installing alongside (same node names).
- VERDICT: install only if #5 proves insufficient (need multi-ref/masking/music).

### 9. Nekodificador/ComfyUI-NKD-VFX-Tools — ✅ INSTALLED (2026-10-05)
- URL: https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools
- VFX art-direction nodes (each with its own viewport — set by eye, no
  guess-and-requeue). Nodes under "😺NKD Nodes" menu. No extra downloads.
- Nodes: Relight (from depth+normal passes, drag lights on sphere),
  Normal Detail (pores/stubble/hair into normal maps), Lens Blur (DoF from depth
  map, click focus point, set aperture), **Preview 3D (GLB/GLTF models +
  gaussian splats in a node — THE Blender→ComfyUI bridge)**, Projection Pass /
  Bake Projection (inpaint views of 3D model, project back to texture),
  **fSpy Camera (drag two vanishing-line pairs over photo → solves the camera)**,
  Camera Delta Prompt (writes camera move as JSON for camera-move LoRA),
  Perspective Unwarp/Rewarp (flatten angled view, edit head-on, put back),
  Lens Distort (barrel/pincushion, chromatic aberration, vignette, anamorphic),
  Mask Scheduler (one mask → batch fading over value list).
- fSpy Camera = fspy.io 2-point vanishing-point solve (credit to stuffmatic).
  Gaussian splat rendering via Spark (MIT).
- VERDICT: ⭐ keep in armoury. fSpy + Preview 3D are the camera/3D bridge.

## Install log
- 2026-10-05: cloned #2 (ComfyUI-H3-Project-Suite) + #9 (ComfyUI-NKD-VFX-Tools)
  into portable custom_nodes (git clone --depth 1). Both have __init__.py.
  ComfyUI restarted to load. #5 + #7 were already installed.
- ComfyUI version: 0.37.0 running (latest 0.38.0 — one behind, fine; #5 needs 0.34+).
- Running server = portable install `E:\comfyUi_latest\ComfyUI_windows_portable`
  (launched: `python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build
  --reserve-vram 4 --enable-manager`). MCP default workspace
  (`C:\Users\user\Documents\comfy\ComfyUI`) is NOT the running server.

### Verified loaded nodes (2026-10-05, object_info = 2547 nodes)
- **Project Suite (#2):** `H3ProjectHub`, `H3ProjectSave` (the Hub is the project
  manager panel; drift report + voice anchor live on the Hub).
- **Motion Context (#5):** `MiniMaxH3MotionContext`, `...Trim`, `...SaveLatent`,
  `...LoadLatent`, `...Chain`, `...SeamProbe`, `...Manual` (all 7 present).
- **NKD (#9):** 11 nodes — `NKDLensBlurNode`, `NKDMaskScheduler`, `NKDfSpyCamera`,
  `NKDPreview3D`, `NKDPerspectiveUnwarp`, `NKDPerspectiveRewarp`, `NKDLensDistort`,
  `NKDCameraDeltaPrompt`, `NKDNormalDetail`, `NKDProjectionPass`, `NKDBakeProjection`.
  (Relight node not in the list — may be named differently or conditional; check
  the 😺NKD Nodes menu in the UI.)
- **SatoDive (#7):** already installed (Minimax-H3-Latent-Continuation dir present).

### ⚠️ Startup gotcha (2026-10-05)
ComfyUI startup is SLOW (~4-5 min) because `dwposedeluxe` tries to pip-install
`tensorrt-cu13` when TensorRT is missing ("Attempting to install 'tensorrt-cu13'
for CUDA 13.x. This may take a while..." — took 186s this time). The process looks
stuck (low CPU, no port) during this. **Don't kill it early.** Launch via
`run_nvidia_gpu.bat` or capture output to a log and wait. Once TensorRT is cached,
subsequent starts are faster.

## Recommended film stack (decision 2026-10-05)
1. #4 omnichar — character consistency (test first, smallest win)
2. #5 Motion Context — chaining engine (clean base; #8 if multi-ref needed)
3. #7 SatoDive — room/environment consistency across angles
4. #2 Project Suite — project manager + drift monitoring + voice anchor
5. #9 NKD — VFX/camera armoury (fSpy + Preview 3D for Blender bridge)
Drop: #3 lumibelle. Defer: #1 Director, #6 Herrgott (very long sequences).

## Blender (installed 2026-10-05)
- **Installed:** Blender **5.2.2 LTS** at `C:\Program Files\Blender Foundation\Blender 5.2`
  (NOT D: — user installed to Program Files). `blender.exe` present, build 2026-09-15.
- **Dual-GPU box:** AMD Radeon iGPU drives the 4K display (3840x2160, driver
  32.0.11024.2); NVIDIA RTX 5090 present but idle (driver 32.0.15.9579).
- **Black-viewport gotcha:** command-line test instances (`blender.exe --debug gpu`
  — note `gpu` gets misparsed as a filename; `--gpu-backend opengl`) rendered a
  BLACK 3D viewport (window + title bar fine, content black). This is the known
  Blender 5.1/5.2 Vulkan black-viewport bug on dual-GPU Windows (blender.org
  issues #157029 "5.2 Vulkan system freeze", #155371 "Vulkan black renders
  NVIDIA driver"). User's NORMAL launch (launcher/shortcut) renders fine.
- **Fix applied:** set Windows GPU preference
  `HKCU:\Software\Microsoft\DirectX\UserGpuPreferences` → `blender.exe_HDGA00000000 = 0`
  (high-performance GPU). Placeholder LUID — may not have applied, but Blender
  works now. If black again: restart, or Edit→Preferences→System→GPU Backend
  (toggle Vulkan↔OpenGL).
- **MCP:** official Blender MCP add-on (5.1+) supports local LLMs (llama.cpp →
  our local Qwen). Community: mcp-for-blender (ahujasid), hsaigroup/blender-mcp.
  NOT yet wired up.
- Role: complex geometry (cars, rooms) → export GLB → NKD Preview 3D / fSpy
  camera → MiniMax H3 motion reference. Shot Composer (D:\models\open-media,
  Vite dev server `npm.cmd run dev` → localhost:5173) = simple character shots;
  layout CONFIRMED rendering (mannequin + shot size/angle/elevation + timeline).

## roycho87 production workflows (2026-10-05, user-downloaded)

User downloaded 3 workflows from **roycho87** (GitHub, "minimax_wf" repo, 52
stars) to `E:\minimax_workflow\production_experiments\`. Byte sizes match the
GitHub repos exactly (verified via API).

### 1. `audio_splitter.json` (= repo `minimax_continuous_audio_splitter`,
file `you_do_not_know_what_kind_of_man_i_am.json`)
- 139-node subgraph "Audio Splitter": `LoadAudioUI` → 19× `PainterAudioCut`
  (frame-accurate audio trim, 4N+1 alignment) + 19× `SaveAudioAdvanced` +
  `ImpactExecutionOrderController` (ordered execution) + easy forLoop.
- **Purpose:** split one long audio track into N frame-aligned chunks for
  continuous/long-video audio stitching. THE audio part the user flagged.
- Missing packs: `princepainter/ComfyUI-PainterNodes` (PainterAudioCut),
  `comfyui-impact-pack` (ImpactExecutionOrderController/ImpactSwitch),
  `ComfyMath` (CM_IntToFloat).

### 2. `continuous_static_video_without_quality_loss.json`
- 169 nodes + 9 subgraphs: Video Settings (VideoResolutionNode), Model Options
  (MiniMaxChunkFeedForward, LowVRAMAttention, SageAttention patch), First and
  Last Frame (MiniMaxH3AddGuide), H3 Sparse Attention (H3SparseAttention),
  Turbo Sampler (MiniMaxH3SigmaShift + LoRA), Force Audio (VAEEncodeAudio +
  SetLatentNoiseMask), Block/Use <Video 1> Audio, V2V editing mode.
- **Purpose:** long continuous video WITHOUT quality loss — chunked H3
  generation with audio continuity, V2V character replacement, control panel
  (resolution/duration/ref counts/continuation/upscale/interpolation).
- Notes carry the full model download list (Comfy-Org/MiniMax-H3 vae/diffusion/
  text_encoders/latent_upscale) + resolution table (0.2-0.9 MP × 16:9).
- Missing packs: `h3-prompt-ide` (H3PromptIDE + H3PromptReferenceInputs —
  the 6-section R2V prompt builder!), `h3-optimizations` (H3SparseAttention),
  `video-resolution` (hyukudan/comfyui-video-resolution "Kirei"),
  `rgthree-comfy` (Fast Groups Bypasser — HAVE rgthree-comfy dir but node
  missing? verify), `ComfyMath`.

### 3. `foxydits_sucks_at_making_workflows_v7.2.json` (the BIG one, 221 nodes)
- Superset of #2 + VFX: 6× VHS_VideoCombine, RIFE VFI (frame interpolation),
  MinimaxH3LatentUpscaler3D (latent upscale), AnimatedMaskDrawer,
  MVEx_* (maskvidexperiments: SubjectCrop/Uncrop/MaskToLatentSpace/MaskCleanup),
  CRTFirstLastFrameSelector, SolidColor, ImageBlend, 3× LoadAudioUI.
- **Purpose:** full production pipeline — multi-segment video with masks,
  subject crop/uncrop, latent upscaling, frame interpolation, audio.
- Missing packs: `comfyui-frame-interpolation` (RIFE VFI),
  `comfyui-minimax-h3-latent-upscaler` (MinimaxH3LatentUpscaler3D),
  `comfyui-animated-mask-editor` (AnimatedMaskDrawer),
  `maskvidexperiments` (MVEx_*), `crt-nodes` (CRTFirstLastFrameSelector),
  `comfyui_essentials` (SolidColor — dir exists, verify), + all of #2's.

### Already HAVE (verified on live server):
KJNodes (LazySwitchKJ, ComfyMathExpression, AudioConcat, ImageBatchMulti,
ImageResizeKJv2, ImagePass, PreviewAudio, MiniMaxLowVRAMAttention), Easy-Use
(easy blocker/showAnything/forLoop/BasicGuider), WhatDreamsCost (LoadAudioUI,
LoadVideoUI), ComfyUI-Continuity (MiniMaxH3AddGuide, LTXVConcatAVLatent,
MiniMaxChunkFeedForward, MiniMaxH3MemoryEfficientSageAttentionPatch,
MiniMaxH3SigmaShift, SamplerCustomAdvanced, RandomNoise),
3d-Camera-control-H3-Minimax (MiniMaxH3ReferenceToVideo),
comfyui-obvpm (LoadImageCrop), VHS, core (TrimAudioDuration, SaveAudioAdvanced,
EmptyAudio, VAEEncodeAudio, SetLatentNoiseMask, AudioAdjustVolume, SolidMask,
BasicScheduler, KSamplerSelect, VAEDecodeAudio, PreviewAnimation, ImageBlend,
ImageFromBatch, GetImageSizeAndCount, GetImageSize, EmptyLatentImage,
Primitive*, INTConstant).
Note/MarkdownNote/GetNode/SetNode "missing" from object_info = FRONTEND-ONLY
nodes (notes + KJ get/set are client-side) — NOT a blocker.

### Install log (2026-10-05, ALL CLONED into portable custom_nodes):
| cnr_id | node(s) | repo | status |
|---|---|---|---|
| (PainterAudioCut) | PainterAudioCut | `princepainter/ComfyUI-PainterNodes` | ✅ cloned |
| comfyui-impact-pack | ImpactExecutionOrderController, ImpactSwitch | `ltdrdata/ComfyUI-Impact-Pack` | ✅ cloned |
| ComfyMath | CM_IntToFloat, CM_FloatToInt, CM_IntToBool | `evanspearman/ComfyMath` | ✅ cloned |
| h3-prompt-ide | H3PromptIDE, H3PromptReferenceInputs | `ethanfel/ComfyUI-H3-Prompt-IDE` | ✅ cloned |
| h3-optimizations | H3SparseAttention | `Zironic/H3-Optimizations` | ✅ cloned |
| video-resolution | VideoResolutionNode ("Kirei") | `hyukudan/comfyui-video-resolution` | ✅ cloned |
| comfyui-minimax-h3-latent-upscaler | MinimaxH3LatentUpscaler3D | `LBH-123-AI/Comfyui_Minimax_h3_latent_Upscaler` | ✅ cloned |
| maskvidexperiments | MVEx_SubjectCrop/Uncrop/MaskToLatentSpace/MaskCleanup | `drozbay/MaskVidExperiments` | ✅ cloned |
| crt-nodes | CRTFirstLastFrameSelector | `PGCRT/CRT-Nodes` | ✅ cloned |
| comfyui-animated-mask-editor | AnimatedMaskDrawer | `BISAM20/ComfyUI-AnimatedMaskEditor` | ✅ cloned |
| (RIFE VFI) | RIFE VFI | `Fannovel16/ComfyUI-Frame-Interpolation` | ✅ cloned (Kosinkadink 404'd; Fannovel16 is the real repo) |
| TTS | TTS-Audio-Suite (diodiogod) | `diodiogod/TTS-Audio-Suite` | ✅ cloned |
Already had: ComfyUI_essentials (SolidColor), rgthree-comfy (Fast Groups
Bypasser — verify node loads), KJNodes, Easy-Use, WhatDreamsCost,
ComfyUI-Continuity, VHS, comfyui-custom-scripts.
NOTE: `Minimax-H3-Latent-Continuation` (SatoDive, installed) registers as
`MiniMaxH3EasyLatentUpscaler3D_SatoDive` — the workflows want
`MinimaxH3LatentUpscaler3D` (LBH-123-AI pack, now cloned).
**Restart:** old server PID 22924 stopped; relaunched via
`cmd /c python -s ComfyUI\main.py --windows-standalone-build --reserve-vram 4
--enable-manager > server_restart_20261005.log` (background shellId 155).
⚠️ `Start-Process -WindowStyle Hidden` with cmd SILENTLY FAILED (no log, no
process) — use `cmd /c ... > log 2>&1` in an async powershell instead.
**VERIFIED after boot (2026-10-05, 3078 nodes, was 2547):** PainterAudioCut,
ImpactExecutionOrderController, ImpactSwitch, CM_IntToFloat/FloatToInt/IntToBool,
H3PromptIDE, H3PromptReferenceInputs, H3SparseAttention, VideoResolutionNode,
MinimaxH3LatentUpscaler3D, MVEx_SubjectCrop/Uncrop/MaskToLatentSpace/MaskCleanup,
CRTFirstLastFrameSelector, AnimatedMaskDrawer, SolidColor — ALL PRESENT.
TTS-Audio-Suite nodes present: ChatterBoxEngineNode, F5TTSEngineNode,
Qwen3TTSEngineNode, MossTTSEngineNode, EchoTTSEngineNode, DotsTTSEngineNode,
ChatterBoxOfficial23LangEngineNode, IndexTTSEngineNode, IndexTTSEmotionOptionsNode,
UnifiedTTSTextNode, **UnifiedTTSSRTNode** (the SRT dubbing node),
ChatterBoxVoiceCapture, ChatterBoxAudioAnalyzer(+Options),
ChatterBoxF5TTSEditVoice(+Options).
Still missing (non-blocking): "Fast Groups Bypasser (rgthree)" (rgthree pack
loads 24 other nodes fine — bypasser may be a newer rgthree version; workflows
still run without it), Note/MarkdownNote/GetNode/SetNode (FRONTEND-ONLY, never
in object_info — not a problem). RIFE VFI = Fannovel16 pack, added in final
restart (shellId 163).

## TTS: diodiogod (2026-10-05)
- `diodiogod/ComfyUI_ChatterBox_SRT_Voice` v3.4.4 (refactor of
  ShmuelRonen/ComfyUI_ChatterBox_Voice) — **EVOLVED INTO**
  `diodiogod/TTS-Audio-Suite` v4.0.0+ (universal multi-engine TTS: ChatterBox
  classic+multilingual, F5-TTS, RVC, Echo-TTS, Qwen3-TTS, Cozy Voice 3,
  Step Audio EditX, IndexTTS-2, Higgs Audio 2/3, VibeVoice; unlimited text
  length, SRT timing, character switching `[Alice]`/`[Bob]`, language
  switching `[de:Alice]`, iterative voice conversion, audio wave analyzer).
- **For us:** SRT-timed TTS = dubbing pipeline upgrade (phone recording →
  clean_dub.py → TTS-Audio-Suite SRT node → LatentSync). Voice conversion
  (iterative refinement) could fix the "subtle eco" issue differently than
  Demucs. NOT yet installed. v3.x branch kept for legacy workflow compat;
  v4.0.0 requires workflow migration.

## Blender (planned, 2026-10-05)
- User downloading Blender (official: https://www.blender.org/download/),
  install target D: drive (E: is ComfyUI-only).
- Official Blender MCP server (Blender 5.1+ add-on, blender.org/lab/mcp-server)
  supports LOCAL LLMs — setup docs point to llama.cpp → our local Qwen can drive
  Blender. Community: mcp-for-blender (ahujasid), hsaigroup/blender-mcp.
- Role: complex geometry (cars, rooms) → export GLB → NKD Preview 3D / fSpy
  camera → MiniMax H3 motion reference. Shot Composer (D:\models\open-media)
  stays for simple character-only shots.
