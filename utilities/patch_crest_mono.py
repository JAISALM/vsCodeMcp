#!/usr/bin/env python
"""Patch crest descriptions to the v3 MONOCHROME spec (white fill + black outline/separator lines, no colors).
Applies to both copies (UI folder + project folder). Asserts each old string appears exactly once."""
import json

BASES = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows",
    r"D:\models\vsCodeMcp\challenge\consistent-short\workflows",
]

CREST_SUBJ = "a white clenched raised fist (fist of resistance) inside a thin white circle on a royal blue background — the fist fully visible with all four fingers and the thumb clear, crisp and legible."
CREST_SUBJ_NEW = "a MONOCHROME clenched raised fist (fist of resistance) — solid white fill with black outline lines and thin black separator lines across the knuckles and the forearm — inside a thin white circle on a royal blue background, NO colors, the fist fully visible with all four fingers and the thumb clear, crisp and legible."

# per-file: (node_id, widget_index, [(old, new), ...]) — subgraph nodes marked ("sub", 478)
PATCHES = {
    "05d_charsheet_H3_wide_jaisal.json": [
        (28, 0, [
            (CREST_SUBJ, CREST_SUBJ_NEW),
            ("the crest emblem (white clenched fist in a thin circle) is copied exactly",
             "the crest emblem (monochrome white-fill clenched fist with black outline lines in a thin white circle, no colors) is copied exactly"),
            ("(a white clenched raised fist inside a thin white circle, all four fingers and the thumb fully visible, crisp and legible, no distortion)",
             "(a monochrome white-fill clenched fist with black outline and separator lines inside a thin white circle, all four fingers and the thumb fully visible, no colors, crisp and legible, no distortion)"),
            ("(white clenched raised fist in a thin circle, all fingers and thumb clearly visible, crisp and legible)",
             "(monochrome white-fill clenched fist with black outline lines in a thin white circle, no colors, all fingers and thumb clearly visible, crisp and legible)"),
        ]),
    ],
    "05e_charsheet_H3_fizgig_jaisal.json": [
        (28, 0, [
            (CREST_SUBJ, CREST_SUBJ_NEW),
            ("the crest emblem is copied exactly (white clenched fist in a thin circle), no redesign.",
             "the crest emblem is copied exactly (monochrome white-fill clenched fist with black outline lines in a thin white circle, no colors), no redesign."),
            ("(a white clenched raised fist inside a thin white circle, all four fingers and the thumb fully visible, crisp and legible)",
             "(a monochrome white-fill clenched fist with black outline and separator lines inside a thin white circle, all four fingers and the thumb fully visible, no colors, crisp and legible)"),
            ("(white clenched raised fist in a thin circle, all fingers and thumb clearly visible, crisp and legible)",
             "(monochrome white-fill clenched fist with black outline lines in a thin white circle, no colors, all fingers and thumb clearly visible, crisp and legible)"),
        ]),
    ],
    "08j_KREA2_JAISAL_sheet.json": [
        (84, 0, [
            ("a white clenched raised fist inside a thin white circle, the fist fully visible with all four fingers and the thumb clearly visible, crisp edges, legible, no distortion",
             "a MONOCHROME clenched raised fist — solid white fill with black outline lines and thin black separator lines across the knuckles and forearm — inside a thin white circle, NO colors, the fist fully visible with all four fingers and the thumb clearly visible, crisp edges, legible, no distortion"),
        ]),
        (85, 0, [
            ("blurred emblem, distorted logo",
             "blurred emblem, distorted logo, colored emblem, colored fist, red knuckles, flag-color stripes"),
        ]),
    ],
    "09j_QWEN21_JAISAL_sheet.json": [
        (555, 0, [
            ("a white clenched raised fist (fist of resistance) inside a thin white circle, all four fingers and the thumb fully visible, crisp and legible",
             "a MONOCHROME clenched raised fist (fist of resistance) — solid white fill with black outline lines and thin black separator lines across the knuckles and forearm — inside a thin white circle, NO colors, all four fingers and the thumb fully visible, crisp and legible"),
        ]),
        ("sub", 478, [
            ("the team crest on the left chest = a white clenched raised fist (fist of resistance) inside a thin white circle — the fist fully visible, all four fingers and the thumb clearly visible, crisp and legible",
             "the team crest on the left chest = a MONOCHROME clenched raised fist (fist of resistance) — solid white fill with black outline lines and thin black separator lines across the knuckles and forearm — inside a thin white circle, NO colors — the fist fully visible, all four fingers and the thumb clearly visible, crisp and legible"),
        ]),
    ],
}

for base in BASES:
    for fname, specs in PATCHES.items():
        p = f"{base}\\{fname}"
        j = json.load(open(p, encoding="utf-8"))
        nodes = []
        for n in j["nodes"]:
            if n["id"] not in [s[0] for s in specs if s[0] != "sub"]:
                nodes.append(n)
        for spec in specs:
            nid, widx, reps = spec
            if nid == "sub":
                for sg in j["definitions"]["subgraphs"]:
                    for n in sg["nodes"]:
                        if n["id"] == nid:
                            for old, new in reps:
                                cnt = n["widgets_values"][widx].count(old)
                                assert cnt == 1, f"{fname} sub-{nid}: '{old[:60]}...' x{cnt}"
                                n["widgets_values"][widx] = n["widgets_values"][widx].replace(old, new)
            else:
                for n in j["nodes"]:
                    if n["id"] == nid:
                        for old, new in reps:
                            cnt = n["widgets_values"][widx].count(old)
                            assert cnt == 1, f"{fname} node {nid}: '{old[:60]}...' x{cnt}"
                            n["widgets_values"][widx] = n["widgets_values"][widx].replace(old, new)
        json.dump(j, open(p, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
        print("patched", p)
print("all done")
