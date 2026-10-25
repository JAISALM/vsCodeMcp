import json
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json"
w = json.load(open(p, encoding="utf-8"))
print("=== NODES ===")
for n in w["nodes"]:
    wv = n.get("widgets_values")
    wv = (str(wv)[:70] + "...") if wv and len(str(wv))>70 else wv
    print("%-4d %-28s pos=%s widgets=%s" % (n["id"], n["type"], n.get("pos"), wv))
print("\n=== LINKS (id, from, from_slot, to, to_slot, type) ===")
for l in w["links"]:
    print(l)
