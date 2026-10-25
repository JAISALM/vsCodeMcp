import json, io
def safe(s): return s.encode("cp1252","replace").decode("cp1252")
w = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_cine_v2.json", encoding="utf-8"))
for n in w["nodes"]:
    if n["type"] == "CLIPTextEncode":
        print("--- node", n["id"], "widget:", safe(str(n.get("widgets_values",""))[:400]))
    if n["type"] == "SaveImage":
        print("save node", n["id"], "prefix:", n.get("widgets_values"))
