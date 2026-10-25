#!/usr/bin/env python
"""Fix 08j: remove node 92 (VAEEncode for the deleted 2nd ref) + its links."""
import json, os

for path in [r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\08j_KREA2_JAISAL_sheet.json",
             r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\08j_KREA2_JAISAL_sheet.json"]:
    j = json.load(open(path, encoding="utf-8"))
    nodes = {n["id"]: n for n in j["nodes"]}
    assert nodes[92]["type"] == "VAEEncode"
    del nodes[92]
    j["nodes"] = [n for n in j["nodes"] if n["id"] != 92]
    before = len(j["links"])
    j["links"] = [l for l in j["links"] if l[1] != 92 and l[3] != 92]
    print(f"{os.path.basename(path)}: removed node 92 + {before - len(j['links'])} links")
    json.dump(j, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
