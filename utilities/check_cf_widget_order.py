import urllib.request, json

base = "http://127.0.0.1:8188"
oi = json.load(urllib.request.urlopen(base + "/object_info"))

node = oi.get("ControlFoleyGenerate")
if not node:
    print("ControlFoleyGenerate NOT in object_info")
else:
    req = node["input"]["required"]
    print("=== ControlFoleyGenerate REQUIRED widget order (server) ===")
    i = 0
    for name, spec in req.items():
        # link inputs (model) are not widgets
        if spec[0] in ("CONTROLFOLEY_MODEL",):
            print(f"  [link] {name}")
            continue
        i += 1
        default = spec[1].get("default", spec[1]) if isinstance(spec[1], dict) else spec[1]
        print(f"  {i:2d}. {name:32s} type={spec[0]:20s} default={default!r}")
    print(f"\nTotal widget count (excl. model link): {i}")
