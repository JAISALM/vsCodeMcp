import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_medium.json"
wf = json.load(open(p, encoding="utf-8"))
for n in wf["nodes"]:
    if n["id"] in ("3", "FKI2I:img"):
        print("=== id", n["id"], n["type"], "===")
        print(json.dumps(n, indent=1, ensure_ascii=False))
        print()
