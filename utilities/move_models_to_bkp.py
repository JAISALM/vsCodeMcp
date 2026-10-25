# move_models_to_bkp.py — archive unused models E:\ComfyUI_windows_portable\ComfyUI\models
# -> F:\models_bkp\<same subfolder>\ (structure preserved, recoverable).
# Explicit file list (no globs). Pre-checks every file (exists + size), moves,
# then verifies: destination exists with identical size, source gone.
# See docs/MODEL_INVENTORY.md for the full list + reasoning.

import os, sys, shutil

SRC = r"E:\ComfyUI_windows_portable\ComfyUI\models"
DST = r"F:\models_bkp"

# (subfolder, filename, group)
FILES = [
 # ---- Wan (~114.8 GB) ----
 ("diffusion_models", "wan2.1_14B_SCAIL_2_fp16.safetensors", "wan"),
 ("unet", "wan2.2_i2v_high_noise_14B_Q8_0.gguf", "wan"),
 ("unet", "wan2.2_i2v_low_noise_14B_Q8_0.gguf", "wan"),
 ("unet", "wan2.2_t2v_high_noise_14B_Q8_0.gguf", "wan"),
 ("unet", "wan2.2_t2v_low_noise_14B_Q8_0.gguf", "wan"),
 ("vae", "wan2.2_vae.safetensors", "wan"),
 ("vae", "wan_2.1_vae.safetensors", "wan"),
 ("vae", "Wan2_1_VAE_bf16.safetensors", "wan"),
 (os.path.join("vae", "wan"), "Wan2_1_VAE_bf16.safetensors", "wan"),
 ("loras", "lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank256_bf16.safetensors", "wan"),
 ("loras", "lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors", "wan"),
 ("loras", "WanAnimate_relight_lora_fp16.safetensors", "wan"),
 ("loras", "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors", "wan"),
 ("loras", "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors", "wan"),
 ("loras", "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "wan"),
 ("loras", "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "wan"),
 ("loras", "wan2.1_SCAIL_2_DPO_lora_bf16.safetensors", "wan"),
 ("loras", "Wan_2_1_I2V_14B_ChronoEdit_distill_lora_rank32.safetensors", "wan"),
 ("loras", "Wan21_CausVid_14B_T2V_lora_rank32.safetensors", "wan"),
 ("loras", "Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors", "wan"),
 ("loras", "Wan21_CausVid_bidirect2_T2V_1_3B_lora_rank32.safetensors", "wan"),
 # ---- umt5 / FLUX.1 text encoders (~41.7 GB) ----
 ("text_encoders", "umt5_xxl_fp16.safetensors", "umt5"),
 ("text_encoders", "umt5-xxl-enc-bf16.safetensors", "umt5"),
 ("text_encoders", "umt5-xxl-enc-bf16_mocha.safetensors", "umt5"),
 ("text_encoders", "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "umt5"),
 ("text_encoders", "t5-base.safetensors", "umt5"),
 # ---- Qwen-Image 2511/2512 gen (~64 GB; edit-2511 chain stays) ----
 ("diffusion_models", "qwen_image_2512_fp8_e4m3fn.safetensors", "qwen2512"),
 ("unet", "Qwen-Image-Edit-2509-Q8_0.gguf", "qwen2512"),
 ("loras", "Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors", "qwen2512"),
 ("loras", "Qwen-Image-Lightning-4steps-V1.0.safetensors", "qwen2512"),
 ("loras", "Qwen-Image-Lightning-4steps-V1.0-bf16.safetensors", "qwen2512"),
 ("loras", "Qwen-Image-Lightning-8steps-V1.0.safetensors", "qwen2512"),
 ("loras", "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "qwen2512"),
 ("loras", "qwen-360-diffusion-2512-int8-bf16-v2.safetensors", "qwen2512"),
 ("loras", "nicegirls_qwen2512.safetensors", "qwen2512"),
 ("loras", "qwen-cinema.safetensors", "qwen2512"),
 ("text_encoders", "qwen3.5_9b_qwen_image_2.1_pe_i2i.int8_convrot.safetensors", "qwen2512"),
 ("model_patches", "qwen_image_canny_diffsynth_controlnet.safetensors", "qwen2512"),
 # ---- SDXL + orphaned controlnets (~16 GB) ----
 ("checkpoints", "RealVisXL_V4.0.safetensors", "sdxl"),
 ("controlnet", "xinsircontrolnet-union-sdxl__model_promax.safetensors", "sdxl"),
 ("controlnet", "InstantXFLUX.1-dev-Controlnet-Union.safetensors", "sdxl"),
 # ---- redundant encoders (~16.9 GB, verified redundant) ----
 ("text_encoders", "qwen3vl_4b_bf16.safetensors", "redundant_enc"),
 ("text_encoders", "qwen_3_4b.safetensors", "redundant_enc"),
 # ---- small unused misc (~14.3 GB) ----
 ("checkpoints", "sdpose_wholebody_fp16.safetensors", "misc"),
 ("clip_vision", "clip_vision_h.safetensors", "misc"),
 ("clip_vision", "sigclip_vision_patch14_384.safetensors", "misc"),
 ("audio_encoders", "wav2vec2_large_english_fp16.safetensors", "misc"),
 ("geometry_estimation", "moge_2_vitl_normal_fp16.safetensors", "misc"),
 ("insightface", "inswapper_128.onnx", "misc"),
 ("liveportrait", "spade_generator.safetensors", "misc"),
 ("liveportrait", "warping_module.safetensors", "misc"),
 ("liveportrait", "motion_extractor.safetensors", "misc"),
 ("liveportrait", "appearance_feature_extractor.safetensors", "misc"),
 ("liveportrait", "stitching_retargeting_module.safetensors", "misc"),
 ("sam2", "sam2_hiera_base_plus.safetensors", "misc"),
 ("sam2", "sam2.1_hiera_base_plus-fp16.safetensors", "misc"),
 ("loras", "adonis_base.safetensors", "misc"),
 ("loras", "adonis_refine.safetensors", "misc"),
 ("loras", "Iyo-Sumiv_10.safetensors", "misc"),
 ("loras", "GrandlineLSIv1.0Krea.safetensors", "misc"),
 ("loras", "refcontrol_v2_poses.safetensors", "misc"),
 ("loras", "vh5tape-comfyui.safetensors", "misc"),
 ("loras", "flux-2-klein-9B-360-erp-outpaint-lora_V1.safetensors", "misc"),
 ("loras", "HighResolution9B.safetensors", "misc"),
 ("loras", "lenovo.safetensors", "misc"),
 ("loras", "Technically_Color_Z_Image_Turbo_v1_renderartist_2000.safetensors", "misc"),
 ("loras", "pixel_art_style_z_image_turbo.safetensors", "misc"),
 ("model_patches", "Z-Image-Turbo-Fun-Controlnet-Union.safetensors", "misc"),
 ("model_patches", "uso-flux1-projector-v1.safetensors", "misc"),
 ("ultralytics", "face_yolov8n.pt", "misc"),
 (os.path.join("ultralytics", "bbox"), "face_yolov8n.pt", "misc"),
 (os.path.join("ultralytics", "bbox"), "hand_yolov8s.pt", "misc"),
 ("vae_approx", "taesd_encoder.safetensors", "misc"),
 ("vae_approx", "taesd_decoder.safetensors", "misc"),
 ("vae_approx", "taesdxl_encoder.safetensors", "misc"),
 ("vae_approx", "taesdxl_decoder.safetensors", "misc"),
 ("vae_approx", "taef1_encoder.safetensors", "misc"),
 ("vae_approx", "taef1_decoder.safetensors", "misc"),
 ("vae_approx", "taesd3_encoder.safetensors", "misc"),
 ("vae_approx", "taesd3_decoder.safetensors", "misc"),
]

def main():
    print("PRE-CHECK")
    ok = True
    total = 0
    plan = []
    for sub, f, grp in FILES:
        sp = os.path.join(SRC, sub, f)
        if not os.path.isfile(sp):
            print("  MISSING (skip):", os.path.join(sub, f)); ok = False; continue
        sz = os.path.getsize(sp)
        dp = os.path.join(DST, sub, f)
        if os.path.exists(dp):
            print("  DEST EXISTS (skip):", os.path.join(sub, f)); ok = False; continue
        plan.append((sub, f, grp, sp, dp, sz))
        total += sz
    print("pre-check files: %d, total %.1f GB" % (len(plan), total/1e9))
    if not ok:
        print("PRE-CHECK FAILED — nothing moved"); return 1

    print("MOVING")
    moved = 0
    for sub, f, grp, sp, dp, sz in plan:
        os.makedirs(os.path.dirname(dp), exist_ok=True)
        shutil.move(sp, dp)
        moved += 1
        print("  [%d/%d] %s" % (moved, len(plan), os.path.join(sub, f)))

    print("VERIFY")
    bad = 0
    for sub, f, grp, sp, dp, sz in plan:
        if not os.path.isfile(dp) or os.path.getsize(dp) != sz:
            print("  VERIFY FAIL:", os.path.join(sub, f)); bad += 1
        if os.path.exists(sp):
            print("  SOURCE STILL THERE:", os.path.join(sub, f)); bad += 1
    print("moved %d files, %d bad" % (moved, bad))
    print("DONE rc=%d" % (1 if bad else 0))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
