import os
base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes"
hits = []
for d in sorted(os.listdir(base)):
    p = os.path.join(base, d)
    if not os.path.isdir(p):
        continue
    if any(k in d.lower() for k in ("nvidia", "rtx", "vfx")):
        hits.append(d)
        for root, _, files in os.walk(p):
            for f in files:
                if f.endswith(".py"):
                    fp = os.path.join(root, f)
                    try:
                        src = open(fp, encoding="utf-8", errors="ignore").read()
                    except Exception:
                        continue
                    for cls in ("RTXVideoSuperResolution", "RTXTrueHDR", "RTXVideoFrameGeneration"):
                        if f"class {cls}" in src:
                            print(f"{d} :: {os.path.relpath(fp, p)} :: class {cls}")
print("candidate dirs:", hits if hits else "NONE")
clone = os.path.join(base, "ComfyUI_Nvidia_VFX_Nodes")
print("clone exists:", os.path.exists(clone))
if os.path.exists(clone):
    print("clone files:", os.listdir(clone))
