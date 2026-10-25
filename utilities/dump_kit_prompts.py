#!/usr/bin/env python
import json
for f in ["07_kit_ref_jaisal", "07_kit_ref_zidane"]:
    p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows" + "\\" + f + ".json"
    j = json.load(open(p, encoding="utf-8"))
    print("=====", f, "id:", j["id"])
    for n in j["nodes"]:
        if n["type"] == "CLIPTextEncode":
            print("-- node", n["id"], "text:")
            print(n["widgets_values"][0])
        elif n["type"] in ("KSampler", "EmptySD3LatentImage", "SaveImage", "UNETLoader", "LoraLoaderModelOnly", "EmptyLatentImage", "ImageScale", "LoadImage"):
            print("-- node", n["id"], n["type"], n.get("widgets_values"))
    print()
