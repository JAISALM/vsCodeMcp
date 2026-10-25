import json
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock_v2.json"
w = json.load(open(p, encoding="utf-8"))
print("=== NODES ===")
for n in w["nodes"]:
    print(n["id"], n["type"], n.get("widgets_values"))
