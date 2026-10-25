import io, os, re
base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Krea2T-Enhancer"
for f in os.listdir(base):
    print("FILE:", f)
# readme if any
for f in os.listdir(base):
    if f.lower().endswith(".md"):
        c = io.open(os.path.join(base, f), encoding="utf-8", errors="replace").read()
        print("=====", f, "===== (first 2500 chars)")
        print(c[:2500])
# the rest of turbo_sigma_scheduler.py
e = io.open(os.path.join(base, "turbo_sigma_scheduler.py"), encoding="utf-8", errors="replace").read()
i = e.find("def get_sigmas")
print("===== get_sigmas + tail =====")
print(e[i:i+1600])
# grep SamplerCustom mentions in pack
for f in os.listdir(base):
    if f.endswith(".py"):
        c = io.open(os.path.join(base, f), encoding="utf-8", errors="replace").read()
        for m in re.finditer(r'.*SamplerCustom.*', c):
            print(f, ">>>", m.group(0).strip()[:160])
