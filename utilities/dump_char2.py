#!/usr/bin/env python
import json
P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char2.json"
j = json.load(open(P, encoding="utf-8"))
for n in j["nodes"]:
    t = n["type"]
    wv = n.get("widgets_values")
    if t in ("CLIPTextEncode", "KSampler", "EmptyLatentImage", "SaveImage", "PreviewImage",
             "UNETLoader", "CLIPLoader", "VAELoader", "LoraLoader", "LoraLoaderModelOnly",
             "FameGridColorFinish", "ResolutionSelector", "ImageResizeKJv2"):
        print(f"== {n['id']} {t} ==")
        print(json.dumps(wv, ensure_ascii=False)[:2500])
        print()
