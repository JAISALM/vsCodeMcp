import json
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2f_jaisal_crookednose.json"
w = json.load(open(p, encoding="utf-8"))
for n in w["nodes"]:
    if n["id"] in (79, 53, 72, 113, 84, 85, 73, 92, 71):
        print("=== NODE", n["id"], n["type"], "===")
        print("  widgets:", n.get("widgets_values"))
        print("  inputs:", [(i.get("name"), i.get("type"), i.get("link")) for i in n["inputs"]])
        print("  outputs:", [(o.get("name"), o.get("type")) for o in n["outputs"]])
