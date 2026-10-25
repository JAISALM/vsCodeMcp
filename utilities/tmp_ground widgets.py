import json
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json"
w = json.load(open(p, encoding="utf-8"))
for n in w["nodes"]:
    if n["id"] in (84, 85):
        print("=== node", n["id"], n["type"])
        print("inputs:", [(i["name"], i["type"], i.get("link")) for i in n["inputs"]])
        print("outputs:", [(o["name"], o["type"]) for o in n["outputs"]])
        print("widgets_values:", json.dumps(n["widgets_values"], ensure_ascii=False))
