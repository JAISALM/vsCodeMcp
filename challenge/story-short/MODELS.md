# Models

All models are **open-weights**. Official H3 files come from
[Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3).

## Krea2 image stage (workflows 01 + 02)

| File | Folder | Size | Source |
|---|---|---|---|
| `krea2_turbo_fp8_scaled.safetensors` | `checkpoints/` or `diffusion_models/` | ~12.2 GB | Krea2 turbo base, fp8 scaled (community quant) |
| `qwen3vl_4b_fp8_scaled.safetensors` | `clip/` or `text_encoders/` | ~2.6 GB | Qwen3-VL 4B text encoder, fp8 (community quant) |
| `qwen_image_vae.safetensors` | `vae/` | ~350 MB | Qwen-Image VAE — [Comfy-Org/Qwen-Image](https://huggingface.co/Comfy-Org/Qwen-Image) |
| `Krea2-realism-V2.safetensors` (optional) | `loras/` | — | Third-party realism LoRA (Civitai) — optional skin-texture boost |
| `krea2_identity_edit_v1_2.safetensors` | `loras/` | — | **Our face-locking LoRA** — released with this repo |

## H3 video stage (workflow 03)

All from [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3):

| File | Folder | URL |
|---|---|---|
| `minimax_h3_ref2va_pruned_int8_convrot.safetensors` | `diffusion_models/` | [link](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors) |
| `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | `clip/` or `text_encoders/` | [link](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors) |
| `minimax_h3_video_vae_fp16.safetensors` | `vae/` | [link](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_video_vae_fp16.safetensors) |
| `minimax_h3_audio_vae_fp32.safetensors` | `vae/` | [link](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_audio_vae_fp32.safetensors) |
| `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` | `loras/` | [link](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/loras/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors) |

## VRAM

- Krea2 fp8 stage: ~16–20 GB peak (1152×2048).
- H3 stage: ~24 GB peak at 2K (SLA attention enabled in workflow 03).
- 32 GB VRAM covers both stages; 24 GB cards: run stages separately or use
  smaller resolutions.
