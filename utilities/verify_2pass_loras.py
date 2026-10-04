"""Verify exact LoRA paths for the 2-pass config (KREA subfolder vs flat).

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\verify_2pass_loras.py"
"""
import os

LORAS = r"E:\ComfyUI_windows_portable\ComfyUI\models\loras"

print("=== KREA subfolder? ===")
krea_dir = os.path.join(LORAS, "KREA")
if os.path.isdir(krea_dir):
    print("KREA subfolder EXISTS:")
    for fn in sorted(os.listdir(krea_dir)):
        print("   KREA\\", fn, f"({os.path.getsize(os.path.join(krea_dir, fn))/1e9:.2f} GB)")
else:
    print("KREA subfolder DOES NOT EXIST")

print("\n=== all krea2-related LoRAs (flat + nested) ===")
for dirpath, dirnames, filenames in os.walk(LORAS):
    dirnames[:] = [x for x in dirnames if x != "__pycache__"]
    for fn in filenames:
        if "krea" in fn.lower() or "cinematic" in fn.lower() or "turbo" in fn.lower():
            rel = os.path.relpath(os.path.join(dirpath, fn), LORAS)
            print(f"   {rel}  ({os.path.getsize(os.path.join(dirpath, fn))/1e9:.2f} GB)")
