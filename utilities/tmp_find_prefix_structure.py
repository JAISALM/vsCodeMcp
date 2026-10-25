import json, io, os

# 1. search ALL comfy user dirs for the prefix krea2_t2i_face
roots = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user",
    r"E:\ComfyUI_windows_portable\ComfyUI\user",
]
found = []
for root in roots:
    if not os.path.isdir(root): continue
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.endswith(".json"):
                p = os.path.join(dp, f)
                try:
                    c = io.open(p, encoding="utf-8").read()
                    if "krea2_t2i_face" in c:
                        found.append(p)
                except Exception:
                    pass
print("files containing krea2_t2i_face:", found if found else "NONE")

# 2. old file structure: ids + input order
w = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1.json", encoding="utf-8"))
for n in w["nodes"]:
    ins = [(i, x.get("name"), x.get("type")) for i, x in enumerate(n.get("inputs", []))]
    outs = [(i, o.get("name"), o.get("type")) for i, o in enumerate(n.get("outputs", []))]
    wv = n.get("widgets_values")
    wvs = str(wv)[:60]
    print(n["id"], n["type"], "pos", n.get("pos"), "W:", wvs)
    print("    in:", ins)
    print("    out:", outs)
print("links:", w.get("links"))
