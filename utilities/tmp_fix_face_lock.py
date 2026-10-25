import json, io
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock.json"
w = json.load(open(p, encoding="utf-8"))
lid = w["last_link_id"] + 1
w["links"].append([lid, 79, 0, 53, 0, "MODEL"])
w["last_link_id"] = lid
for n in w["nodes"]:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in w["links"] if lk[3] == n["id"] and lk[4] == j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in w["links"] if lk[1] == n["id"]] or None
with io.open(p, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("added link", lid)
