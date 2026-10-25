import json
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2d_jaisal_zidhan_v3.json"
w = json.load(open(p, encoding="utf-8"))
print("=== NODES (id, type, widgets) ===")
for n in w["nodes"]:
    print(n["id"], n["type"], n.get("widgets_values"))
