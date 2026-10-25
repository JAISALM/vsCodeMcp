#!/usr/bin/env python
"""09k_QWEN21_ZIDANE_sheet.json = clone of 09j (the winning PE-architect sheet) for ZIDANE:
- 470  -> zidane_sheet_ref_3panel.png
- 481  -> ZIDANE
- 461  -> charsheet/QWEN21_ZIDANE
- 555[0] (dead-field mirror) -> zidane combined spec
- 478 (subgraph = THE LIVE PE SPEC) -> JAISAL->ZIDANE, royal blue->dark green
Writes both copies (E: workflows + challenge\\consistent-short\\workflows).
"""
import json, os

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json"
DSTS = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09k_QWEN21_ZIDANE_sheet.json",
    r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\09k_QWEN21_ZIDANE_sheet.json",
]

NEW_555_0 = ("Reference image = three-panel grid: LEFT = identity portrait (face, hair, beard, skin — the SOLE identity source; "
"take identity ONLY from this panel, do not add or alter any character attribute), TOP-RIGHT = team crest emblem on dark green "
"(copy it EXACTLY as the chest emblem and in the crest detail tile — never redesign or invent it), BOTTOM-RIGHT = team kit reference "
"(match its dark green color and fabric, the white side stripe and the white boots). He wears the complete team kit in every body view: "
"a plain dark green short-sleeve soccer jersey (single flat dark green color, no patterns) with the fabric color and texture of the "
"BOTTOM-RIGHT panel, the team crest on the left chest copied EXACTLY from the TOP-RIGHT panel — a MONOCHROME clenched raised fist "
"(fist of resistance) with solid white fill, black outline lines and thin black separator lines across the knuckles and forearm, "
"inside a thin white circle, NO colors, all four fingers and the thumb fully visible, crisp and legible — the white name \"ZIDANE\" "
"centered on the upper back of the jersey, matching dark green track pants with a single white stripe down each side, clean white "
"football boots matching the BOTTOM-RIGHT panel. Include a dedicated detail close-up of the crest emblem alone on a dark green "
"background, and a turnaround row (front, side, back) all wearing the complete kit. Photoreal high-end studio photography.")

j = json.load(open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

# 470 ref file
assert nodes[470]["widgets_values"][0] == "jaisal_sheet_ref_3panel.png"
nodes[470]["widgets_values"][0] = "zidane_sheet_ref_3panel.png"
# 481 name
assert nodes[481]["widgets_values"][0] == "JAISAL"
nodes[481]["widgets_values"][0] = "ZIDANE"
# 461 save prefix
assert nodes[461]["widgets_values"][0] == "charsheet/QWEN21_JAISAL"
nodes[461]["widgets_values"][0] = "charsheet/QWEN21_ZIDANE"
# 555 dead-field mirror
assert "three-panel grid" in nodes[555]["widgets_values"][0]
nodes[555]["widgets_values"][0] = NEW_555_0

# 478 live spec — the subgraph that actually feeds the LLM
done = []
for sg in j.get("definitions", {}).get("subgraphs", []):
    for n in sg.get("nodes", []):
        if n["id"] == 478:
            t = n["widgets_values"][0]
            n_jaisal = t.count("JAISAL")
            n_blue = t.count("royal blue")
            assert n_jaisal >= 2 and n_blue >= 5, (n_jaisal, n_blue)
            t = t.replace("JAISAL", "ZIDANE").replace("royal blue", "dark green")
            assert "JAISAL" not in t and "royal blue" not in t
            assert "Entity ZIDANE wears" in t
            n["widgets_values"][0] = t
            done.append(len(t))
assert len(done) == 1, done

for DST in DSTS:
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    json.dump(j, open(DST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved", DST, os.path.getsize(DST))
print("done")
