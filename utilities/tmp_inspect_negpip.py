import json
src = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_charlora_v3.json", encoding="utf-8"))
for n in src["nodes"]:
    if n["type"] == "ApplyKrea2NegPiP":
        print("node", n["id"], "inputs:", [(i.get("name"), i.get("type")) for i in n.get("inputs", [])])
    if n["type"] == "LoraLoaderModelOnly" and n["id"] == 96:
        print("node 96 inputs:", [(i.get("name"), i.get("type")) for i in n.get("inputs", [])])
    if n["type"] == "LoraLoaderModelOnly" and n["id"] == 95:
        print("node 95 inputs:", [(i.get("name"), i.get("type")) for i in n.get("inputs", [])])
