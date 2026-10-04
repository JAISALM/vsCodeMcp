"""Verify the model files for the bf16-krea + turbo-lora config.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\verify_2pass_models.py"
"""
import os

MODELS = r"E:\ComfyUI_windows_portable\ComfyUI\models"

def show(label, path):
    ok = os.path.isfile(path)
    size = os.path.getsize(path) / 1e9 if ok else 0
    print(f"{'OK  ' if ok else 'MISS'} {label:<45} {path}  ({size:.2f} GB)")
    return ok

print("=== UNet (bf16 krea) ===")
show("krea2_turbo_bf16", os.path.join(MODELS, "diffusion_models", "krea2_turbo_bf16.safetensors"))
show("krea2_turbo_fp8_scaled", os.path.join(MODELS, "diffusion_models", "krea2_turbo_fp8_scaled.safetensors"))

print("\n=== Turbo LoRA ===")
for cand in [
    os.path.join(MODELS, "loras", "KREA", "krea2_turbo_lora_rank_64_bf16.safetensors"),
    os.path.join(MODELS, "loras", "krea2_turbo_lora_rank_64_bf16.safetensors"),
]:
    show("turbo lora", cand)
# search for any turbo lora
print("--- search for krea2 turbo lora ---")
for dirpath, dirnames, filenames in os.walk(os.path.join(MODELS, "loras")):
    dirnames[:] = [x for x in dirnames if x != "__pycache__"]
    for fn in filenames:
        if "turbo" in fn.lower() and "krea" in fn.lower():
            print("   FOUND:", os.path.join(dirpath, fn), f"({os.path.getsize(os.path.join(dirpath, fn))/1e9:.2f} GB)")

print("\n=== VAE ===")
for fn in os.listdir(os.path.join(MODELS, "vae")):
    fp = os.path.join(MODELS, "vae", fn)
    if os.path.isfile(fp) and ("krea" in fn.lower() or "qwen" in fn.lower() or fn == "ae.safetensors"):
        print(f"   {fn}  ({os.path.getsize(fp)/1e9:.2f} GB)")

print("\n=== CLIP (krea2) ===")
for sub in ("clip", "text_encoders"):
    d = os.path.join(MODELS, sub)
    if os.path.isdir(d):
        for fn in os.listdir(d):
            if "qwen3vl" in fn.lower() or "krea" in fn.lower():
                fp = os.path.join(d, fn)
                if os.path.isfile(fp):
                    print(f"   [{sub}] {fn}  ({os.path.getsize(fp)/1e9:.2f} GB)")
