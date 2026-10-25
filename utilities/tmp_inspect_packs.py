import os, json, io, glob

base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes"
for pack in ("ComfyUI-Krea2T-Enhancer", "comfyui-krea2edit", "ComfyUI-krea2-negpip"):
    d = os.path.join(base, pack)
    print("=====", pack, "=====")
    if not os.path.isdir(d):
        print("  MISSING"); continue
    for f in sorted(os.listdir(d)):
        if f.endswith(".py"):
            p = os.path.join(d, f)
            print(" ", f, os.path.getsize(p), "bytes")
    # read __init__ for NODE_CLASS_MAPPINGS
    ini = os.path.join(d, "__init__.py")
    if os.path.isfile(ini):
        c = io.open(ini, encoding="utf-8", errors="replace").read()
        for line in c.split("\n"):
            if "CLASS" in line or "MAPPINGS" in line or "import" in line.lower()[:8]:
                print("   |", line.strip()[:120])

# identity-edit workflow structure
w = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json", encoding="utf-8"))
print("===== krea2_identity_edit.json =====")
for n in w["nodes"]:
    wv = str(n.get("widgets_values"))[:90]
    print(" ", n["id"], n["type"], "pos", n.get("pos"), wv)
    for i, x in enumerate(n.get("inputs", [])):
        print("      in%d %s %s link=%s" % (i, x.get("name"), x.get("type"), x.get("link")))
    for i, o in enumerate(n.get("outputs", [])):
        print("      out%d %s %s" % (i, o.get("name"), o.get("type")))
print("links:", w.get("links"))
