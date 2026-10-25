import json, io
t = json.load(open(r"D:\models\vsCodeMcp\utilities\official_image_krea2_turbo_t2i.json", encoding="utf-8"))
si = [n for n in t["nodes"] if n["type"] == "SaveImage"][0]
print("template SaveImage prefix:", si["widgets_values"])
old = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1.json", encoding="utf-8"))
pe = [n for n in old["nodes"] if n["type"] == "PixaromaPromptEach"][0]
wv = pe["widgets_values"]
print("old prompteach format:", type(wv).__name__, "len", len(wv))
if wv and isinstance(wv[0], str) and wv[0].startswith("{"):
    import re
    blob = wv[0]
    state = json.loads(blob)
    for i, p in enumerate(state["prompts"]):
        print("--- prompt", i+1, "---")
        print(p)
else:
    for i, p in enumerate(wv):
        print("--- prompt", i+1, "---")
        print(p)
