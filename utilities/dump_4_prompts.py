#!/usr/bin/env python
"""Dump the FULL prompt texts to edit: 05d/05e node 28 prompt, 08j node 84/85 prompts,
09j node 478 ROLE prompt. Plus the links arrays for 05d (dangling ref links check)."""
import json, os

PRJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"
UI = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

def nodes(p):
    j = json.load(open(p, encoding="utf-8"))
    return {n["id"]: n for n in j["nodes"]}, j

for wf in ("05d_charsheet_H3_wide_jaisal.json", "05e_charsheet_H3_fizgig_jaisal.json",
           "08j_KREA2_JAISAL_sheet.json", "09j_QWEN21_JAISAL_sheet.json"):
    ns, j = nodes(os.path.join(PRJ, wf))
    print("=" * 100)
    print(wf)
    for nid in (28, 84, 85, 478):
        n = ns.get(nid)
        if n and n.get("widgets_values"):
            print(f"---- {wf} node {nid} {n['type']} FULL PROMPT ----")
            print(n["widgets_values"][0])
            print()
    # 05d: links array (check dangling ref_image_2..8 links 66,70,71,72,76,75,98)
    if wf.startswith("05d"):
        ids = {n["id"] for n in j["nodes"]}
        print("---- 05d LINKS (all) ----")
        for l in j["links"]:
            dangling = " DANGLING-SRC" if l[1] not in ids else ""
            dangling += " DANGLING-DST" if l[3] not in ids else ""
            print(l, dangling)
        # subgraph definitions?
        if j.get("definitions"):
            print("HAS definitions/subgraphs")
print("=" * 100)
print("DONE")
