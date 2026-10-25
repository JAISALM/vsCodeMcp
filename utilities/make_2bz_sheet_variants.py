#!/usr/bin/env python
"""Build Jaisal/Zidane variants of the 2BZ H3 character sheet (2-stage v1 EN).

Per-character wiring:
  node 16 (Picture 1 - face/identity) = <char>_portrait_HD.png
  node 21 (Picture 2 - outfit)        = <char>_portrait_HD.png (portrait includes the tee)
  nodes 22/57/58/59 (optional add/prop/pose/env) = neutral_placeholder.png (white,
        so the analyzers report VISUAL_REFERENCE: NO and no foreign identity leaks in)
  node 106 (SaveImage) prefix         = charsheet/<CHAR>_3VIEW
Everything else (models, switches, prompts) untouched.
"""
import json
import os
import shutil

SRC = r"E:\minimax_workflow\character_sheet\2BZ_H3_character_sheet_2stage_v1_EN.json"
OUTDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
PROJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"

CHARS = [
    ("jaisal", "jaisal_portrait_HD.png", "charsheet/JAISAL_3VIEW", "05_charsheet_2BZ_jaisal.json"),
    ("zidane", "zidane_portrait_HD.png", "charsheet/ZIDANE_3VIEW", "06_charsheet_2BZ_zidane.json"),
]

j = json.load(open(SRC, encoding="utf-8", errors="ignore"))
nodes = {n["id"]: n for n in j["nodes"]}

# sanity: confirm node roles before touching
assert nodes[16]["type"] == "LoadImage" and nodes[16]["widgets_values"][0] == "2bz_character_face_photo1.jpg"
assert nodes[21]["type"] == "LoadImage"
assert nodes[106]["type"] == "SaveImage"
print("source OK:", nodes[106]["widgets_values"])

for char, face, prefix, projname in CHARS:
    j2 = json.loads(json.dumps(j))
    n2 = {n["id"]: n for n in j2["nodes"]}
    n2[16]["widgets_values"] = [face, "image"]
    n2[21]["widgets_values"] = [face, "image"]
    for opt in (22, 57, 58, 59):
        n2[opt]["widgets_values"] = ["neutral_placeholder.png", "image"]
    n2[106]["widgets_values"] = [prefix]
    ui = os.path.join(OUTDIR, f"2BZ_H3_character_sheet_2stage - {char}.json")
    json.dump(j2, open(ui, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    shutil.copy2(ui, os.path.join(PROJ, projname))
    print(f"WROTE: {ui}")
    print(f"       + project copy: {projname}")
