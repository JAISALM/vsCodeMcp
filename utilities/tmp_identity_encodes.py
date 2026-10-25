import json, io
w = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json", encoding="utf-8"))
for n in w["nodes"]:
    if n["id"] in (82, 83, 84, 85, 92, 113, 114):
        print("=====", n["id"], n["type"], "pos", n.get("pos"))
        print("widgets_values:", str(n.get("widgets_values"))[:120])
        for i, x in enumerate(n.get("inputs", [])):
            print("   in%d %s type=%s link=%s" % (i, x.get("name"), x.get("type"), x.get("link")))
        for i, o in enumerate(n.get("outputs", [])):
            print("   out%d %s type=%s links=%s" % (i, o.get("name"), o.get("type"), o.get("links")))
