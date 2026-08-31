import json, os

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

# Native files (UI-saved, named=False)
native_files = [
    "krea2_jaisal_base.json",
    "QWEN_click_multiple_character_angles-v1.0.json",
    "mini-max-refrance-to-video-1.json",
    "05_Chained.json",
    "video_minimax_h3_t2v.json",
]

# node_type -> first native node object found
found = {}
for f in native_files:
    p = os.path.join(BASE, f)
    if not os.path.exists(p):
        continue
    wf = json.load(open(p, encoding="utf-8"))
    if not isinstance(wf.get("nodes"), list):
        continue
    for n in wf["nodes"]:
        t = n.get("type")
        if t not in found:
            found[t] = (n, f)

need = ["UNETLoader", "CLIPLoader", "VAELoader", "LoadImage", "CLIPTextEncode",
        "LoraLoaderModelOnly", "VAEEncode", "KSampler", "VAEDecode", "SaveImage",
        "PreviewImage"]

for t in need:
    if t in found:
        n, f = found[t]
        print(f"### {t}  (from {os.path.basename(f)}) ###")
        print("   keys:", list(n.keys()))
        print("   widgets_values:", n.get("widgets_values"))
        print("   widgets_values_named:", n.get("widgets_values_named"))
        print("   inputs:", [(i.get('name'), i.get('widget')) for i in n.get('inputs', [])])
        print()
    else:
        print(f"### {t}  *** NOT FOUND in native files ***\n")
