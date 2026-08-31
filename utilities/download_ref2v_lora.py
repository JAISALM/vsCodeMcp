import os, urllib.request, urllib.error

LORA_DIR = r"E:\ComfyUI_windows_portable\ComfyUI\models\loras"
NAME = "minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors"
URL = f"https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/loras/{NAME}"
DEST = os.path.join(LORA_DIR, NAME)

# 1) What ref2v / turbo LoRAs are already present?
print("=== Existing ref2v/turbo LoRAs ===")
for f in sorted(os.listdir(LORA_DIR)):
    if "ref2v" in f or "turbo" in f or "fl2v" in f:
        print(f"   {f}  ({os.path.getsize(os.path.join(LORA_DIR, f))} bytes)")

# 2) Is the target already there?
if os.path.exists(DEST):
    print(f"\nAlready present: {NAME} ({os.path.getsize(DEST)} bytes)")
else:
    print(f"\nDownloading {NAME} ...")
    try:
        req = urllib.request.Request(URL, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"   URL OK, size = {r.headers.get('Content-Length')} bytes")
    except urllib.error.HTTPError as e:
        print(f"   *** URL 404/ERROR: {e.code} {e.reason}")
        print(f"   Trying alternate v1.0 name ...")
        NAME2 = "minimax_h3_ref2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors"
        URL2 = f"https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/loras/{NAME2}"
        try:
            req = urllib.request.Request(URL2, method="HEAD")
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"   ALT URL OK: {NAME2} ({r.headers.get('Content-Length')} bytes)")
        except urllib.error.HTTPError as e2:
            print(f"   *** ALT also failed: {e2.code} {e2.reason}")
        raise SystemExit("Download URL not found - check the exact LoRA filename.")
    # Download
    urllib.request.urlretrieve(URL, DEST)
    print(f"   Downloaded to {DEST} ({os.path.getsize(DEST)} bytes)")
