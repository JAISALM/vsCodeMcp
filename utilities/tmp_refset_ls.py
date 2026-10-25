import os, glob
def safe(s): return s.encode("cp1252","replace").decode("cp1252")
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output"
for d in ["refset_v6","refset_v7"]:
    p = os.path.join(out,d)
    print("=== %s ===" % d)
    if os.path.isdir(p):
        for f in sorted(os.listdir(p)):
            print("  %8d  %s" % (os.path.getsize(os.path.join(p,f)), safe(f)))
    else:
        print("  MISSING")
