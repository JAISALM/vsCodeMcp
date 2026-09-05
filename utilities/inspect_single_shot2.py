import json

path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json"
d = json.load(open(path))

# instance node 105
for n in d["nodes"]:
    if n["id"] == 105:
        print("== instance 105 keys:", list(n.keys()))
        print("widgets_values len:", len(n.get("widgets_values", [])))
        print("has widgets_values_named:", "widgets_values_named" in n)
        if "widgets_values_named" in n:
            print("named keys:", list(n["widgets_values_named"].keys()))
        print("inputs:", [(i.get("name"), i.get("type")) for i in n.get("inputs", [])])

# internal node 104
for s in d.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        if n["id"] == 104:
            print("== internal 104 keys:", list(n.keys()))
            print("widgets_values len:", len(n.get("widgets_values", [])))
            print("has widgets_values_named:", "widgets_values_named" in n)
            if "widgets_values_named" in n:
                print("named keys:", list(n["widgets_values_named"].keys()))
            print("prompt head:", str(n.get("widgets_values", [""])[0])[:120])
