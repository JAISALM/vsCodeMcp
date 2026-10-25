#!/usr/bin/env python
"""Verify all 4 Jaisal sheet workflows (UI + project copies) point every face-ref
LoadImage at jaisal_portrait_HD.png (the new frontal base)."""
import json, os

WF_UI = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
WF_PRJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"
WFS = ["05d_charsheet_H3_wide_jaisal.json", "05e_charsheet_H3_fizgig_jaisal.json",
       "08j_KREA2_JAISAL_sheet.json", "09j_QWEN21_JAISAL_sheet.json"]

ok = True
for name in WFS:
    for label, base in (("UI", WF_UI), ("PRJ", WF_PRJ)):
        p = os.path.join(base, name)
        if not os.path.exists(p):
            print(f"!! {label} MISSING {name}")
            ok = False
            continue
        j = json.load(open(p, encoding="utf-8"))
        imgs = []
        for n in j["nodes"]:
            if n["type"] == "LoadImage":
                w = n.get("widgets_values") or []
                imgs.append((n["id"], w[0] if w else "?"))
        face_refs = [(i, f) for i, f in imgs if "portrait_HD" in f or "face" in f.lower() or "ref" in f.lower()]
        bad = [(i, f) for i, f in imgs if f != "jaisal_kit_ref.png"]
        print(f"{label} {name}: {imgs}")
        if any(f != "jaisal_portrait_HD.png" for i, f in bad):
            print(f"   !! face ref not canonical: {bad}")
            ok = False
print("\nALL WIRE TO jaisal_portrait_HD.png" if ok else "\nFIXES NEEDED")
