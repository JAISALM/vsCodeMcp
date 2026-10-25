import json, io
src = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock.json"
w = json.load(open(src, encoding="utf-8"))
for n in w["nodes"]:
    if n["id"] == 79:
        n["widgets_values"] = [3.5, 1.0, "fit"]
    if n["id"] == 29:
        n["widgets_values"] = ["krea2_face_lock_b"]
dst = src.replace("krea2_face_lock.json", "krea2_face_lock_b.json")
with io.open(dst, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("wrote", dst)
