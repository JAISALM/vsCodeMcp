#!/usr/bin/env python
import json, io, sys
P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json"
OUT = r"D:\models\vsCodeMcp\data\09j_pe_texts_dump.txt"
j = json.load(open(P, encoding="utf-8"))
buf = io.StringIO()
for sg in j.get("definitions", {}).get("subgraphs", []):
    buf.write(f"== SUBGRAPH {sg.get('id')}\n")
    for n in sg.get("nodes", []):
        tag = n["id"]
        if tag in (478, 549):
            buf.write(f"\n----- INTERNAL NODE {tag} ({n['type']}) -----\n")
            for i, w in enumerate(n.get("widgets_values") or []):
                s = json.dumps(w, ensure_ascii=False)
                buf.write(f"[{i}] len={len(s)}\n{s}\n")
        else:
            wvs = json.dumps(n.get("widgets_values"))[:100] if n.get("widgets_values") is not None else "None"
            buf.write(f"  node {tag} {n['type'][:30]:<30} {wvs}\n")
main = {n["id"]: n for n in j["nodes"]}
buf.write("\n== MAIN 555 widgets VALUES ==\n")
for i, w in enumerate(main[555]["widgets_values"]):
    s = json.dumps(w, ensure_ascii=False)
    buf.write(f"[{i}] len={len(s)}\n{s}\n")
buf.write("\n== MAIN 555 widgets NAMED ==\n" + json.dumps(main[555].get("widgets_values_named"), ensure_ascii=False, indent=1) + "\n")
open(OUT, "w", encoding="utf-8").write(buf.getvalue())
print("written", OUT, len(buf.getvalue()), "chars")
