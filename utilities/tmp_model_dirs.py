import os
def safe(s): return s.encode("cp1252","replace").decode("cp1252")
live = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"
main = r"E:\ComfyUI_windows_portable\ComfyUI"
def is_link(p):
    try: return os.path.islink(p)
    except: return False
for label, base in [("LIVE", live), ("MAIN", main)]:
    m = os.path.join(base, "models")
    print("=== %s models dir: %s (islink=%s) ===" % (label, safe(m), is_link(m)))
    if not os.path.isdir(m):
        print("  MISSING"); continue
    for sub in sorted(os.listdir(m)):
        p = os.path.join(m, sub)
        if os.path.isdir(p):
            n = len([x for x in os.listdir(p) if x.lower().endswith(".safetensors")])
            print("  [%s] islink=%s  .safetensors=%d" % (sub, is_link(p), n))
# where is krea2_turbo_fp8_scaled?
import glob
print()
print("=== krea2_turbo_fp8_scaled locations ===")
for base in [live, main]:
    for f in glob.glob(os.path.join(base, "models", "unets", "krea2_turbo_fp8_scaled*")):
        print("  ", safe(f))
print("=== krea2fp_v2_ep64 locations ===")
for base in [live, main]:
    for f in glob.glob(os.path.join(base, "models", "loras", "krea2fp_v2_ep64*")):
        print("  ", safe(f))
