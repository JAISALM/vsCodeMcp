# -*- coding: utf-8 -*-
import json
fp = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\2BZ_H3_character_sheet_2stage_v1_EN.json"
d = json.load(open(fp, encoding="utf-8"))
print("top-level keys:", list(d.keys()))
nodes = d.get("nodes", [])
print("node count:", len(nodes))
print()
print("=== KEY NODES ===")
for n in nodes:
    if n["type"] in ("LoadImage", "DecodeH3CharacterSheet", "TextEncodeH3Edit",
                     "AddH3EditReference", "H3EditOptions", "SaveImage", "SaveVideo",
                     "MiniMaxH3ReferenceToVideo", "UNETLoader", "CLIPLoader",
                     "VAELoader", "LoraLoaderModelOnly", "KSampler", "EmptyLatentImage",
                     "VAEDecode", "ResolutionSelector", "PrimitiveStringMultiline",
                     "PrimitiveString", "H3SLAAttention", "BasicGuider", "SamplerCustomAdvanced"):
        print("  %s  %s  %s" % (n["id"], n["type"], n.get("widgets_values")))
print()
print("=== ALL NODE TYPES ===")
from collections import Counter
print(Counter(n["type"] for n in nodes))
