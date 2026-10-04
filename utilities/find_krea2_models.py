"""Check for the two missing model files across all likely locations.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\find_krea2_models.py"
"""
import os

targets = ["krea2RealVae_v10", "Krea2_Turbo_convrot_int8mixed", "krea2RealVae", "convrot_int8mixed"]
roots = [
    r"E:\ComfyUI_windows_portable\ComfyUI\models",
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models",
    r"E:\Krea2",
    r"D:\models",
]
print("=== searching for missing model files ===")
for root in roots:
    if not os.path.isdir(root):
        print("skip (no dir):", root)
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [x for x in dirnames if x not in ("__pycache__", ".git", "node_modules")]
        for fn in filenames:
            low = fn.lower()
            for t in targets:
                if t.lower() in low:
                    fp = os.path.join(dirpath, fn)
                    print("FOUND: %s  (%.2f GB)" % (fp, os.path.getsize(fp) / 1e9))

print("\n=== what krea2 models ARE present (main path) ===")
for sub in ("unet", "vae", "diffusion_models", "checkpoints"):
    d = os.path.join(r"E:\ComfyUI_windows_portable\ComfyUI\models", sub)
    if os.path.isdir(d):
        print("---", sub, "---")
        for fn in sorted(os.listdir(d)):
            if "krea" in fn.lower() or "vae" in fn.lower():
                fp = os.path.join(d, fn)
                if os.path.isfile(fp):
                    print("   %s  (%.2f GB)" % (fn, os.path.getsize(fp) / 1e9))
