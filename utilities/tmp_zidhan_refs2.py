import os, glob
def safe(s): return s.encode("cp1252","replace").decode("cp1252")
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output"
print("=== subdirs ===")
for d in sorted(os.listdir(out)):
    if os.path.isdir(os.path.join(out,d)): print("  DIR", safe(d))
print("=== zidane/char2/face files (top 60) ===")
hits = []
for root, dirs, files in os.walk(out):
    for f in files:
        lf = f.lower()
        if ("zidane" in lf or "zidhan" in lf or "char2" in lf) and f.lower().endswith((".png",".jpg")):
            hits.append(os.path.join(root,f))
for h in sorted(hits)[:60]:
    print("%8d  %s" % (os.path.getsize(h), safe(h)))
print("total hits:", len(hits))
