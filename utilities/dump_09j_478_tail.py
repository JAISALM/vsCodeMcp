#!/usr/bin/env python
import json, io
P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json"
j = json.load(open(P, encoding="utf-8"))
out = io.StringIO()
for sg in j.get("definitions", {}).get("subgraphs", []):
    for n in sg.get("nodes", []):
        if n["id"] == 478:
            t = n["widgets_values"][0]
            out.write(f"== 478 total len {len(t)} ==\n")
            out.write("== TAIL 4000 ==\n" + t[-4000:] + "\n")
            out.write("\n== contains {{name}}? " + str("{{name}}" in t) + " ==\n")
            out.write("== contains 'Entity JAISAL'? " + str("Entity JAISAL" in t) + " ==\n")
            i = t.find("KIT SPEC")
            out.write(f"== first 'KIT SPEC' at index {i} ==\n")
            if i >= 0:
                out.write(t[i-200:i+2500] + "\n")
open(r"D:\models\vsCodeMcp\data\09j_478_tail.txt", "w", encoding="utf-8").write(out.getvalue())
print("ok")
