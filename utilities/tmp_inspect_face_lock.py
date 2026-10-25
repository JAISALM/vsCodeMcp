import json
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2f_jaisal_crookednose.json"
w = json.load(open(p, encoding="utf-8"))
print("=== NODES (id, type, widgets) ===")
for n in w["nodes"]:
    print(n["id"], n["type"], n.get("widgets_values"))
print("=== LINKS (id, from, from_slot, to, to_slot, type) ===")
for lk in w["links"]:
    print(lk)
