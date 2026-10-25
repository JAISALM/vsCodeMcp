import io, os
root = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"
hits = []
for dp, dn, fn in os.walk(root):
    if "custom_nodes" in dp or "python_embeded" in dp or "__pycache__" in dp:
        continue
    for f in fn:
        if f.endswith(".py"):
            p = os.path.join(dp, f)
            try:
                c = io.open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if "class SamplerCustom" in c:
                hits.append(p)
print(hits)
if hits:
    c = io.open(hits[0], encoding="utf-8", errors="replace").read()
    i = c.find("class SamplerCustom")
    print(c[i:i+2400])
