import json, io, os
# bb0c structure
p = r"E:\Krea2\bb0c2c32-93ab-4a61-8a5c-daf72b2db888.json"
w = json.load(open(p, encoding="utf-8"))
if isinstance(w, dict) and isinstance(w.get("nodes"), list):
    print("bb0c: UI format, nodes:", len(w["nodes"]), "links:", len(w.get("links", [])))
    from collections import Counter
    c = Counter(n["type"] for n in w["nodes"])
    for t, k in c.most_common(30):
        print("  %3d  %s" % (k, t))
else:
    print("bb0c keys:", list(w.keys())[:20] if isinstance(w, dict) else type(w))
# models on disk
mroot = r"E:\ComfyUI_windows_portable\ComfyUI\models"
for sub in ("diffusion_models", "loras", "vae", "clip", "text_encoders"):
    d = os.path.join(mroot, sub)
    if os.path.isdir(d):
        print("\n===", sub, "===")
        for f in sorted(os.listdir(d)):
            fp = os.path.join(d, f)
            if os.path.isfile(fp):
                print("  %10.1f MB  %s" % (os.path.getsize(fp)/1e6, f))
