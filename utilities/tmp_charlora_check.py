import os, glob, json
def safe(s): return s.encode("cp1252","replace").decode("cp1252")
bases = [r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models", r"E:\ComfyUI_windows_portable\ComfyUI\models"]
print("=== krea2 UNET (diffusion_models) ===")
for b in bases:
    for f in glob.glob(os.path.join(b, "diffusion_models", "krea2*")):
        print("  %8d  %s" % (os.path.getsize(f), safe(f)))
print("=== char lora in MAIN loras ===")
for f in glob.glob(os.path.join(r"E:\ComfyUI_windows_portable\ComfyUI\models\loras", "krea2fp*")):
    print("  %8d  %s" % (os.path.getsize(f), safe(f)))
# object_info: is krea2fp_v2_ep64 a loadable lora on the live server?
import urllib.request
try:
    oi = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=20))
    loras = oi.get("LoraLoader", {}).get("input", {}).get("required", {}).get("lora_name", [])
    char = [l for l in loras if "krea2fp" in l.lower()]
    print("=== live object_info LoraLoader: krea2fp entries ===")
    for c in char: print("  ", c)
    unets = oi.get("UNETLoader", {}).get("input", {}).get("required", {}).get("unet_name", [])
    k2 = [u for u in unets if "krea2" in u.lower()]
    print("=== live object_info UNETLoader: krea2 entries ===")
    for u in k2: print("  ", u)
except Exception as e:
    print("object_info fetch failed:", e)
