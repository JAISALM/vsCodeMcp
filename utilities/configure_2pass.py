"""Configure krea2T2iI2iInpaint2pass_v15 for bf16-krea + turbo-LoRA + krea2RealVae.

Writes a ready-to-run copy with:
  - UNet  = krea2_turbo_bf16.safetensors          (bf16 krea)
  - VAE   = krea2RealVae_v10.safetensors          (already in place, now available)
  - Turbo LoRA enabled in the active model chain (Power Lora Loader, on:true)
  - LoadImage = mic_small_id_00001_.png           (base image for i2i/inpaint)

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\configure_2pass.py"
"""
import json, os

SRC = r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_2pass_bf16_turbo.json"

UNET = "krea2_turbo_bf16.safetensors"
VAE = "krea2RealVae_v10.safetensors"
TURBO_LORA = "krea2_turbo_lora_rank_64_bf16.safetensors"
BASE_IMAGE = "mic_small_id_00001_.png"

wf = json.load(open(SRC, encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}
changes = []

# 1. UNet -> bf16 krea
n = nodes[259]
n["widgets_values"][0] = UNET
changes.append(f"node 259 UNETLoader -> {UNET}")

# 2. VAE -> krea2RealVae_v10 (keep; now available)
n = nodes[37]
n["widgets_values"][0] = VAE
changes.append(f"node 37 VAELoader -> {VAE}")

# 3. Power Lora Loader (node 279) -> turbo LoRA, on:true (active model chain)
n = nodes[279]
wv = n["widgets_values"]
# widget index 2 is the LoRA spec dict
if isinstance(wv[2], dict):
    wv[2]["lora"] = TURBO_LORA
    wv[2]["on"] = True
    wv[2]["strength"] = 1.0
changes.append(f"node 279 Power Lora Loader -> {TURBO_LORA} (on:true)")

# 4. LoadImage (node 265) -> base image (for i2i/inpaint)
n = nodes[265]
n["widgets_values"][0] = BASE_IMAGE
changes.append(f"node 265 LoadImage -> {BASE_IMAGE}")

os.makedirs(os.path.dirname(DST), exist_ok=True)
json.dump(wf, open(DST, "w", encoding="utf-8"), indent=1)

print("=== configured ===")
for c in changes:
    print("  ", c)
print("\nwrote:", DST)
