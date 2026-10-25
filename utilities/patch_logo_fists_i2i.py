#!/usr/bin/env python
"""Wire 901 (palestine_fist_ref) into 956/957 images.image_1 (slot 1) for i2i logo generation."""
import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\logo_fists_compare.json"
j = json.load(open(p, encoding="utf-8"))
byid = {n["id"]: n for n in j["nodes"]}
for tgt in (956, 957):
    j["last_link_id"] += 1
    j["links"].append([j["last_link_id"], 901, 0, tgt, 1, "IMAGE"])
    byid[tgt]["inputs"][1]["link"] = j["last_link_id"]
    byid[901]["outputs"][0]["links"].append(j["last_link_id"])
json.dump(j, open(p, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
print("patched, last_link_id =", j["last_link_id"])
