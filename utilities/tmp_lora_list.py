import os, glob
def safe(s): return s.encode("cp1252","replace").decode("cp1252")
dirs = {
 "live(loras)": r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\loras",
 "main(loras)": r"E:\ComfyUI_windows_portable\ComfyUI\models\loras",
}
for label, d in dirs.items():
    print("=== %s : %s ===" % (label, safe(d)))
    if not os.path.isdir(d):
        print("  MISSING"); continue
    for f in sorted(os.listdir(d)):
        if f.lower().endswith(".safetensors"):
            print("  %8d  %s" % (os.path.getsize(os.path.join(d,f)), safe(f)))
