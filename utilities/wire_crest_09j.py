#!/usr/bin/env python
"""09j-only: PE custom prompt (node 555) = kit spec; subgraph-def 478 ROLE += KIT SPEC."""
import json, os

UI = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
PRJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"

P09J_PE = """Character design sheet of JAISAL — the man from the reference image, keep his exact face, wavy medium-length black hair, small patchy short beard, slim build. He wears the complete team kit in every body view: a plain royal blue short-sleeve soccer jersey (single flat royal blue color, no patterns) with the team crest on the left chest — a white clenched raised fist (fist of resistance) inside a thin white circle, all four fingers and the thumb fully visible, crisp and legible — the white name "JAISAL" centered on the upper back of the jersey, matching royal blue track pants with a single white stripe down each side, clean white football boots. Include a dedicated detail close-up of the crest emblem alone on a royal blue background, and a turnaround row (front, side, back) all wearing the complete kit. Photoreal high-end studio photography."""

KIT_SPEC = """## KIT SPEC (design source #2 — overrides any observed wardrobe)
Entity JAISAL wears the team kit in every view that shows the body: a plain royal blue short-sleeve soccer jersey (single flat royal blue color, no patterns, no numbers on the front), the team crest on the left chest = a white clenched raised fist (fist of resistance) inside a thin white circle — the fist fully visible, all four fingers and the thumb clearly visible, crisp and legible — the white name "JAISAL" centered on the upper back of the jersey, matching royal blue track pants with a single white stripe down each side, clean white football boots. Include ONE dedicated detail tile showing the crest emblem alone on a royal blue background. The reference image governs face, hair, skin and body ONLY; the kit above governs clothing.

"""

p = os.path.join(UI, "09j_QWEN21_JAISAL_sheet.json")
j = json.load(open(p, encoding="utf-8"))
ns = {n["id"]: n for n in j["nodes"]}
print("main-canvas node ids:", sorted(ns))

# 555 = PE instance (c832bb2a...) — its widgets_values[0] is the custom prompt (currently '')
assert ns[555]["widgets_values"][0] in ("", None), f"PE prompt not empty: {ns[555]['widgets_values'][0]!r}"
ns[555]["widgets_values"][0] = P09J_PE
print("555 PE custom prompt set")

# 478 ROLE lives in the subgraph definition
role_updated = 0
for sg in j.get("definitions", {}).get("subgraphs") or []:
    for n in sg["nodes"]:
        if n["id"] == 478 and "# USER" in n["widgets_values"][0] and "## KIT SPEC" not in n["widgets_values"][0]:
            n["widgets_values"][0] = n["widgets_values"][0].replace("\n# USER", "\n" + KIT_SPEC + "# USER", 1)
            role_updated += 1
print("478 ROLE updated in subgraph def:", role_updated)

with open(p, "w", encoding="utf-8") as f:
    json.dump(j, f, indent=4, ensure_ascii=False)
print("wrote UI copy")

# project copy (same edit)
p2 = os.path.join(PRJ, "09j_QWEN21_JAISAL_sheet.json")
j2 = json.load(open(p2, encoding="utf-8"))
ns2 = {n["id"]: n for n in j2["nodes"]}
assert ns2[555]["widgets_values"][0] in ("", None)
ns2[555]["widgets_values"][0] = P09J_PE
role_updated = 0
for sg in j2.get("definitions", {}).get("subgraphs") or []:
    for n in sg["nodes"]:
        if n["id"] == 478 and "# USER" in n["widgets_values"][0] and "## KIT SPEC" not in n["widgets_values"][0]:
            n["widgets_values"][0] = n["widgets_values"][0].replace("\n# USER", "\n" + KIT_SPEC + "# USER", 1)
            role_updated += 1
print("project 478 ROLE updated:", role_updated)
with open(p2, "w", encoding="utf-8") as f:
    json.dump(j2, f, indent=4, ensure_ascii=False)
print("wrote project copy — ALL DONE")
