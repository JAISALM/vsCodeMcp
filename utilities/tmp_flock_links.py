import json
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock_v2.json"
w = json.load(open(p, encoding="utf-8"))
print("=== LINKS (id, from, from_slot, to, to_slot, type) ===")
for lk in w["links"]:
    print(lk)
