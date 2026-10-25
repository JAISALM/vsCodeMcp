"""Robust resumable HF downloader: Range resume + retry with backoff.
Usage: python hf_resumable_download.py
Each job: (url, dest, target_size_bytes). Resumes from existing file size.
Re-running the script is the resume recipe (idempotent, skips complete files).
"""
import os
import sys
import time
import urllib.request

JOBS = [
    # (url, dest, target_bytes)
    ("https://huggingface.co/videorebirth/hyperflow/resolve/main/minimax_h3_hyperflow_8step_v1.0.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\loras\minimax_h3_hyperflow_8step_v1.0.safetensors",
     2_795_328_008),
    ("https://huggingface.co/FastVideo/FastVideo-FastH3-4-step-Preview-v1-LoRA/resolve/main/dense-datafree/adapter_model.safetensors",
     r"E:\minimax_workflow\sol_h3_weights\fasth3_4step_dense_datafree_adapter.safetensors",
     1_485_626_152),
    ("https://huggingface.co/Efficient-Large-Model/Sol-H3-VAE/resolve/main/fast_h3_vae_noncausal_24l.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\vae\fast_h3_vae_noncausal_24l.safetensors",
     6_471_256_328),
    ("https://huggingface.co/lightx2v/Minimax-h3-Turbo/resolve/main/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\loras\minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
     1_865 * 1024 * 1024),
    ("https://huggingface.co/FastVideo/FastH3-OmniRef-NVFP4-QAD-Comfy/resolve/main/fasth3_omniref_qad_nvfp4_comfy.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\fasth3_omniref_qad_nvfp4_comfy.safetensors",
     13_773_998_700),
    ("https://huggingface.co/FastVideo/FastH3-Omni-Comfy/resolve/main/diffusion_models/fasth3_omniref_8step_pruned_int8_convrot.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\fasth3_omniref_8step_pruned_int8_convrot.safetensors",
     22_213_723_064),
    ("https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/diffusion_models/minimax_h3_ref2va_pruned_fp8_scaled.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\minimax_h3_ref2va_pruned_fp8_scaled.safetensors",
     20_958_205_608),
    ("https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/diffusion_models/minimax_h3_fl2va_int8_convrot.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\minimax_h3_fl2va_int8_convrot.safetensors",
     34_038_892_334),
    # --- Qwen3-TTS-12Hz-1.7B-CustomVoice (P10 item 6) ---
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/model.safetensors",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\model.safetensors",
     3_833_402_552),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/speech_tokenizer/model.safetensors",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\speech_tokenizer\model.safetensors",
     682_293_092),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/config.json",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\config.json",
     4_908),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/generation_config.json",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\generation_config.json",
     245),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/merges.txt",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\merges.txt",
     1_671_839),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/preprocessor_config.json",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\preprocessor_config.json",
     127),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/speech_tokenizer/config.json",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\speech_tokenizer\config.json",
     2_336),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/speech_tokenizer/configuration.json",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\speech_tokenizer\configuration.json",
     76),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/speech_tokenizer/preprocessor_config.json",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\speech_tokenizer\preprocessor_config.json",
     234),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/tokenizer_config.json",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\tokenizer_config.json",
     7_344),
    ("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/resolve/main/vocab.json",
     r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\TTS\qwen3_tts\Qwen3-TTS-12Hz-1.7B-CustomVoice\vocab.json",
     2_776_833),
    # --- Item 8: VNCCS PoseStudio (QI2.1 pose-from-image) ---
    ("https://huggingface.co/MIUProject/VNCCS_PoseStudio_QI2.1/resolve/main/VNCCS_QI2_PoseStudioV1.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\loras\QI2.1\VNCCS\VNCCS_QI2_PoseStudioV1.safetensors",
     159_436_408),
    ("https://huggingface.co/MIUProject/VNCCS_PoseStudio_QI2.1/resolve/main/VNCCS_QI2_PoseStudioV1.1.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\loras\QI2.1\VNCCS\VNCCS_QI2_PoseStudioV1.1.safetensors",
     159_436_408),
    ("https://huggingface.co/MIUProject/VNCCS_PoseStudio_QI2.1/resolve/main/VNCCS_QI2_PoseStudioV2.safetensors%20",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\loras\QI2.1\VNCCS\VNCCS_QI2_PoseStudioV2.safetensors",
     159_436_400),
    ("https://huggingface.co/Comfy-Org/Qwen-Image-2.1/resolve/main/diffusion_models/qwen_image_2.1_int8_convrot.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\unet\qwen_image_2.1_int8_convrot.safetensors",
     7_256_783_064),
    ("https://huggingface.co/Comfy-Org/Qwen-Image-2.1/resolve/main/text_encoders/qwen3vl_8b_int8_convrot.safetensors",
     r"E:\ComfyUI_windows_portable\ComfyUI\models\clip\qwen3vl_8b_int8_convrot.safetensors",
     9_350_798_360),
]
MAX_RETRIES = 60          # per file
SLEEP_BASE = 5            # seconds, doubles each retry (cap 60 s)
CHUNK = 4 * 1024 * 1024   # 4 MB


def download_one(url: str, dest: str, target: int) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    name = os.path.basename(dest)
    attempt = 0
    while True:
        have = os.path.getsize(dest) if os.path.exists(dest) else 0
        if have >= target:
            print(f"DONE {name} ({have // 1024 // 1024} MB)", flush=True)
            return
        attempt += 1
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Range": f"bytes={have}-",
                },
            )
            with urllib.request.urlopen(req, timeout=600) as r, open(dest, "ab") as f:
                while True:
                    c = r.read(CHUNK)
                    if not c:
                        break
                    f.write(c)
            # loop re-checks size; if server returned fewer bytes we resume again
            if os.path.getsize(dest) >= target:
                print(f"DONE {name} ({os.path.getsize(dest) // 1024 // 1024} MB)", flush=True)
                return
        except urllib.error.HTTPError as e:  # noqa: BLE001
            if 400 <= e.code < 500:
                # Permanent (bad URL / missing file) — log and move on; never crash the batch.
                print(f"FAILED {name}: HTTP {e.code} (permanent) — check URL; continuing", flush=True)
                return
            raise
        except Exception as e:  # noqa: BLE001
            if attempt > MAX_RETRIES:
                print(f"FAILED {name} after {attempt} attempts: {e}", flush=True)
                return
            sleep_s = min(SLEEP_BASE * (2 ** min(attempt, 3)), 60)
            have_now = os.path.getsize(dest) // 1024 // 1024 if os.path.exists(dest) else 0
            print(f"RETRY {name} attempt {attempt} ({e.__class__.__name__}): resume at "
                  f"{have_now} MB in {sleep_s}s", flush=True)
            time.sleep(sleep_s)


def main() -> None:
    for url, dest, target in JOBS:
        print(f"START {os.path.basename(dest)} target={target // 1024 // 1024} MB "
              f"have={os.path.getsize(dest) // 1024 // 1024 if os.path.exists(dest) else 0} MB", flush=True)
        download_one(url, dest, target)
    print("ALL JOBS FINISHED", flush=True)


if __name__ == "__main__":
    sys.exit(main())
