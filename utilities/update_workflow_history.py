p = r"d:\models\vsCodeMcp\project-memory\WORKFLOW_HISTORY.md"
txt = open(p, encoding="utf-8").read()
addition = """

---

## jaisal_drone_optimized.json (MiniMax H3 optimized drone ascent)

Date: 2026-08-27
Status: Built + validated, NOT yet run

### Purpose

Fast 15s drone-ascent shot for "The Jaisal Cut" (kid on bridge -> tiny dot). First-last-frame interpolation via fl2va model, optimized for RTX 5090 speed.

### Location

E:\\comfyUi_latest\\ComfyUI_windows_portable\\ComfyUI\\user\\default\\workflows\\jaisal_drone_optimized.json

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
"""
open(p, "w", encoding="utf-8").write(txt.rstrip() + "\n" + addition)
print("added jaisal_drone_optimized.json to WORKFLOW_HISTORY.md")
