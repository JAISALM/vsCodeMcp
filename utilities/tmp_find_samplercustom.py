import json, io, os
roots = [r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user", r"E:\ComfyUI_windows_portable\ComfyUI\user"]
found = 0
for root in roots:
    if not os.path.isdir(root): continue
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(".json"): continue
            p = os.path.join(dp, f)
            try:
                c = io.open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if '"SamplerCustom"' in c:
                w = json.loads(c)
                if isinstance(w, dict) and isinstance(w.get("nodes"), list):
                    for n in w["nodes"]:
                        if n.get("type") == "SamplerCustom":
                            print("FILE:", p)
                            print(json.dumps(n, indent=1)[:2000])
                            found += 1
                            if found >= 2: raise SystemExit
