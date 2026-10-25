import json, io, os

p = r"E:\Krea2\bb0c2c32-93ab-4a61-8a5c-daf72b2db888.json"
raw = open(p, "rb").read()
enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
w = json.loads(io.open(p, encoding=enc).read())
if isinstance(w, dict) and isinstance(w.get("nodes"), list):
    print("bb0c: UI format (enc=%s) nodes: %d links: %d" % (enc, len(w["nodes"]), len(w.get("links", []))))
    from collections import Counter
    c = Counter(n["type"] for n in w["nodes"])
    for t, k in c.most_common(30):
        print("  %3d  %s" % (k, t))
else:
    print("bb0c type:", type(w), list(w.keys())[:15] if isinstance(w, dict) else "")

for mroot in (r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models",
              r"E:\ComfyUI_windows_portable\ComfyUI\models"):
    if not os.path.isdir(mroot):
        print("\nMISSING ROOT:", mroot); continue
    print("\n##### ROOT:", mroot)
    for sub in ("diffusion_models", "loras", "vae", "clip", "text_encoders"):
        d = os.path.join(mroot, sub)
        if not os.path.isdir(d): continue
        print("---", sub)
        for f in sorted(os.listdir(d)):
            fp = os.path.join(d, f)
            if os.path.isfile(fp):
                print("  %10.1f MB  %s" % (os.path.getsize(fp)/1e6, f))
