import io
base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes"
e = io.open(base + r"\ComfyUI-Krea2T-Enhancer\turbo_sigma_scheduler.py", encoding="utf-8", errors="replace").read()
i = e.find("class Krea2TurboReferenceSigmaSchedulerFromLatent")
print("===== scheduler class =====")
print(e[i:i+1800])
a = io.open(base + r"\ComfyUI-Krea2T-Enhancer\advanced.py", encoding="utf-8", errors="replace").read()
i = a.find("class Krea2TEnhancerAdvanced")
print("===== advanced class =====")
print(a[i:i+1600])
