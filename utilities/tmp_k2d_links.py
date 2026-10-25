import json
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2d_jaisal_zidhan_v3.json"
w = json.load(open(p, encoding="utf-8"))
print("=== LINKS (id, from, from_slot, to, to_slot, type) ===")
for lk in w["links"]:
    print(lk)
print("=== last_link_id ===", w.get("last_link_id"))
print("=== last_node_id ===", w.get("last_node_id"))
