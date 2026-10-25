#!/usr/bin/env python
"""Patch 09j (both copies) for the 3-panel reference feed:
1. 470 LoadImage -> jaisal_sheet_ref_3panel.png
2. rewire: PE 555.in0 and generator 459.in6 take the composite DIRECTLY (bypass 485 VSR which soft-upscaled the face)
3. 478 (subgraph, THE LIVE PE SPEC) -> new REFERENCE IMAGE LAYOUT + monochrome KIT SPEC
4. 555 widget[0] (dead field) mirrored to the same combined spec
"""
import json, copy

FILES = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json",
    r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\09j_QWEN21_JAISAL_sheet.json",
]

NEW_BLOCK = """## REFERENCE IMAGE LAYOUT (read this first)
The reference image is a single three-panel grid on a white ground:
- LEFT panel (dominant, full height): the identity portrait — face, hair, beard, skin. This is the SOLE identity source. Take identity ONLY from this panel; do not add or alter any character attribute that is not visible in it.
- TOP-RIGHT panel: the team crest emblem alone on a royal blue ground. Copy it EXACTLY as the chest emblem and in the crest detail tile — do not redesign it, do not invent a new emblem, do not change its colors or shape.
- BOTTOM-RIGHT panel: the team kit reference (jersey, pants, boots). Match its royal blue color and fabric, the single white side stripe and the white boots exactly.

## KIT SPEC (design source #2 — overrides any observed wardrobe)
Entity JAISAL wears the team kit in every view that shows the body: a plain royal blue short-sleeve soccer jersey (single flat royal blue color, no patterns, no numbers on the front) with the fabric color and texture of the BOTTOM-RIGHT panel, the team crest on the left chest copied EXACTLY from the TOP-RIGHT panel — a MONOCHROME clenched raised fist (fist of resistance) with solid white fill, black outline lines and thin black separator lines across the knuckles and forearm, inside a thin white circle, NO colors, all four fingers and the thumb fully visible, crisp and legible — the white name "JAISAL" centered on the upper back of the jersey, matching royal blue track pants with a single white stripe down each side, clean white football boots matching the BOTTOM-RIGHT panel. Include ONE dedicated detail tile showing the crest emblem alone on a royal blue background, copied EXACTLY from the TOP-RIGHT panel. The LEFT panel governs face, hair, skin and body ONLY; the TOP-RIGHT and BOTTOM-RIGHT panels govern the emblem and clothing."""

NEW_555_0 = ("Reference image = three-panel grid: LEFT = identity portrait (face, hair, beard, skin — the SOLE identity source; "
"take identity ONLY from this panel, do not add or alter any character attribute), TOP-RIGHT = team crest emblem on royal blue "
"(copy it EXACTLY as the chest emblem and in the crest detail tile — never redesign or invent it), BOTTOM-RIGHT = team kit reference "
"(match its royal blue color and fabric, the white side stripe and the white boots). He wears the complete team kit in every body view: "
"a plain royal blue short-sleeve soccer jersey (single flat royal blue color, no patterns) with the fabric color and texture of the "
"BOTTOM-RIGHT panel, the team crest on the left chest copied EXACTLY from the TOP-RIGHT panel — a MONOCHROME clenched raised fist "
"(fist of resistance) with solid white fill, black outline lines and thin black separator lines across the knuckles and forearm, "
"inside a thin white circle, NO colors, all four fingers and the thumb fully visible, crisp and legible — the white name \"JAISAL\" "
"centered on the upper back of the jersey, matching royal blue track pants with a single white stripe down each side, clean white "
"football boots matching the BOTTOM-RIGHT panel. Include a dedicated detail close-up of the crest emblem alone on a royal blue "
"background, and a turnaround row (front, side, back) all wearing the complete kit. Photoreal high-end studio photography.")

for P in FILES:
    j = json.load(open(P, encoding="utf-8"))
    nodes = {n["id"]: n for n in j["nodes"]}

    # 1. LoadImage file
    assert nodes[470]["widgets_values"][0] == "jaisal_portrait_HD.png", nodes[470]["widgets_values"]
    nodes[470]["widgets_values"][0] = "jaisal_sheet_ref_3panel.png"

    # 2. rewire links (UI array format: [id, origin, origin_slot, target, target_slot, type])
    links = {l[0]: l for l in j["links"]}
    assert links[959][:4] == [959, 485, 0, 555], links[959]
    assert links[747][:4] == [747, 485, 0, 459], links[747]
    assert links[743][:4] == [743, 470, 0, 485], links[743]
    links[959][1] = 470   # PE image <- composite
    links[747][1] = 470   # generator i2i image_1 <- composite
    j["links"] = [l for l in j["links"] if l[0] != 743]  # drop 470->485

    # node-side bookkeeping
    out470 = nodes[470]["outputs"][0]
    assert out470["links"] == [743, 989], out470["links"]
    out470["links"] = [959, 747, 989]
    in485 = nodes[485]["inputs"][0]
    assert in485["link"] == 743
    in485["link"] = None
    out485 = nodes[485]["outputs"][0]
    assert out485["links"] == [747, 959], out485["links"]
    out485["links"] = None

    # 3. 478 live spec: replace old KIT SPEC block with layout + new block
    for sg in j.get("definitions", {}).get("subgraphs", []):
        for n in sg.get("nodes", []):
            if n["id"] == 478:
                t = n["widgets_values"][0]
                i = t.find("## KIT SPEC")
                k = t.find("# USER")
                assert i > 0 and k > i, (i, k)
                assert t.count("## KIT SPEC") == 1
                n["widgets_values"][0] = t[:i] + NEW_BLOCK + "\n\n" + t[k:]
                print(f"{P.split(chr(92))[-3] if False else P}: 478 new len = {len(n['widgets_values'][0])}")

    # 4. 555 widget[0] mirror
    nodes[555]["widgets_values"][0] = NEW_555_0

    json.dump(j, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("patched", P)
print("done")
