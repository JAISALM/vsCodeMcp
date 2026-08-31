import json, urllib.request

# 1) What the server says the KSampler + LoadImage widgets are (ground truth order)
info = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=30))
for name in ("KSampler", "LoadImage"):
    node = info.get(name, {})
    inputs = node.get("input", {})
    req = inputs.get("required", {})
    opt = inputs.get("optional", {})
    print(f"=== {name} ===")
    print("  required order:", list(req.keys()))
    print("  optional order:", list(opt.keys()))
    for k, v in req.items():
        print(f"    {k}: {v[0] if isinstance(v, list) else v}")
    print()

# 2) What's actually in the file for those nodes
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_title_moody.json"
wf = json.load(open(p, encoding="utf-8"))
for n in wf["nodes"]:
    if n["type"] in ("KSampler", "LoadImage"):
        print(f"=== FILE node {n['id']} {n['type']} ===")
        print("  widgets_values:", n.get("widgets_values"))
        print("  widgets_values_named:", n.get("widgets_values_named"))
        print()
