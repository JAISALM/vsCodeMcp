# -*- coding: utf-8 -*-
import json, urllib.request
BASE = "http://127.0.0.1:8188"
types = ["KSampler", "LoadImage", "EmptySD3LatentImage", "CLIPLoader",
         "UNETLoader", "VAELoader", "LoraLoaderModelOnly",
         "Krea2EditGroundedEncode", "Krea2EditModelPatch", "SaveImage",
         "ResolutionSelector"]
for t in types:
    try:
        info = json.load(urllib.request.urlopen(f"{BASE}/object_info/{t}", timeout=30))[t]["input"]
        req = list(info.get("required", {}).keys())
        opt = list(info.get("optional", {}).keys())
        print(f"{t}: required={req} optional={opt}")
    except Exception as e:
        print(f"{t}: ERROR {e}")
