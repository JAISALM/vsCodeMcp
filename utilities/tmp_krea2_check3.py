import json, io, os
p = r"E:\Krea2\bb0c2c32-93ab-4a61-8a5c-daf72b2db888.json"
raw = open(p, "rb").read()
print("head bytes:", raw[:8].hex())
for enc in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be", "cp1252", "latin-1"):
    try:
        t = raw.decode(enc)
        if t.lstrip()[:1] == "{":
            print("decoded OK with", enc)
            w = json.loads(t)
            if isinstance(w, dict) and isinstance(w.get("nodes"), list):
                from collections import Counter
                c = Counter(n["type"] for n in w["nodes"])
                print("bb0c UI format, nodes:", len(w["nodes"]), "links:", len(w.get("links", [])))
                for t2, k in c.most_common(30):
                    print("  %3d  %s" % (k, t2))
            else:
                print("keys:", list(w.keys())[:15])
            break
    except Exception as e:
        print(enc, "fail:", str(e)[:60])

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
