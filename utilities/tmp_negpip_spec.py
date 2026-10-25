import io, re
base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes"
n = io.open(base + r"\ComfyUI-krea2-negpip\krea2_negpip.py", encoding="utf-8", errors="replace").read()
i = n.find("class ApplyKrea2NegPiP")
j = n.find("def patch", i)
print(n[i:i+4000])
print("===== base T-Enhancer =====")
e = io.open(base + r"\ComfyUI-Krea2T-Enhancer\advanced.py", encoding="utf-8", errors="replace").read()
# base node may be in a separate file; search all
import os
for f in os.listdir(base + r"\ComfyUI-Krea2T-Enhancer"):
    if f.endswith(".py"):
        c = io.open(os.path.join(base, "ComfyUI-Krea2T-Enhancer", f), encoding="utf-8", errors="replace").read()
        if "class ComfyUI" in c and "Krea2T" in c:
            i2 = c.find("class ComfyUI")
            print("FILE:", f)
            print(c[i2:i2+2000])
