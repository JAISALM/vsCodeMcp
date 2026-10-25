#!/usr/bin/env python
"""Fix the H3 sheet prompts: copy the AUTHORS' prompting technique (sprite-sheet layout:
left portrait closeup + center 3-angle full-body + right 6 round detail images) instead of
our generic 3-view prompt.

05e (patreon, SINGLE ref): author template verbatim structure; the author's empty
'META for composition:' field is filled with our kit + crest spec (text-specified, since
this workflow has only the face ref).

05d (civitai, 2 refs): same author template; <Picture 2> = our kit flat-lay ref (the
author's 10-ref workflow only ever referenced <Picture 1> — we wire the kit ref to
<Picture 2> so the emblem/kit color inherit from the image, not just text).
"""
import json

OUTS = {
    "05d": [r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\05d_charsheet_H3_wide_jaisal.json",
            r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\05d_charsheet_H3_wide_jaisal.json"],
    "05e": [r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\05e_charsheet_H3_fizgig_jaisal.json",
            r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\05e_charsheet_H3_fizgig_jaisal.json"],
}

# ---- 05e: single-ref (face only) — author template, META field = our kit + crest spec
PROMPT_05E = (
    "iintegrated_multimodal_description:\n\n"
    "subject_definitions:\n"
    "<CHARACTER> character from <Picture 1> — a ~26-year-old Indian man, wavy medium-length black hair, "
    "a small patchy short beard, slim build, medium-brown Indian skin. META for composition: <CHARACTER> "
    "wears the complete team kit — a royal blue short-sleeve soccer jersey with a small subtle white emblem "
    "on the left chest (a clenched fist inside a thin circle, no words, no letters), matching royal blue "
    "track pants with a single white stripe down each side, clean white football boots, and the white name "
    "JAISAL centered on the upper back of the jersey.\n"
    "<Picture 1> is the identity source portrait of <CHARACTER>.\n\n"
    "summary:\n"
    "[reference generation] static image of sprite sheet, keep the exactly same art style of <Picture 1>.\n\n"
    "retention_analysis:\n"
    "<CHARACTER>: fully_preserved — face, hair, beard, skin tone and body build come only from <Picture 1>.\n\n"
    "detailed_description:\n"
    "The target image is a static image of sprite sheet showing <CHARACTER> from different angles, each "
    "element is separated and not overlap on each other, on a clean white studio background.\n\n"
    "[Shot 1] static image.\n\n"
    "<CHARACTER> on white background, sprite sheet showing <CHARACTER> composition adapted following all "
    "possible variants and angles:\n"
    "1. <CHARACTER> On the left portrait (head and chest) closeup composition on white background.\n"
    "2. <CHARACTER> In the center full body view from 3 different angles: straight from front, straight from "
    "side, straight from back — all wearing the complete team kit.\n"
    "3. <CHARACTER> On the right 6 round images (same size 2x3 vertical narrow row) with <CHARACTER>'s "
    "highlight details: single eye, lips, single ear (in circle), hair color, detailed skin texture color, "
    "outfit texture color (the royal blue jersey fabric and the small white clenched-fist roundel emblem).\n\n"
    "overall_soundscape: N/A\n\n"
    "non_diegetic_music: N/A"
)

# ---- 05d: two refs (face + kit flat-lay) — <Picture 2> anchors the kit from the IMAGE
PROMPT_05D = (
    "iintegrated_multimodal_description:\n\n"
    "subject_definitions:\n"
    "<CHARACTER> character from <Picture 1> — a ~26-year-old Indian man, wavy medium-length black hair, "
    "a small patchy short beard, slim build, medium-brown Indian skin. META for composition: <CHARACTER> "
    "wears the complete team kit from <Picture 2>.\n"
    "<Picture 1> is the identity source portrait of <CHARACTER>.\n"
    "<Picture 2> is the team-kit reference: a royal blue short-sleeve soccer jersey with a small subtle "
    "white emblem on the left chest (a clenched fist inside a thin circle, no words, no letters) and "
    "matching royal blue track pants with a single white stripe down each side.\n\n"
    "summary:\n"
    "[reference generation] static image of sprite sheet, keep the exactly same art style of <Picture 1>.\n\n"
    "retention_analysis:\n"
    "<CHARACTER>: fully_preserved — face, hair, beard, skin tone and body build come only from <Picture 1>.\n"
    "<Picture 2>: partially_preserved — costume design, colors and emblem only; never inherit any donor "
    "face or body from <Picture 2>.\n\n"
    "detailed_description:\n"
    "The target image is a static image of sprite sheet showing <CHARACTER> from different angles, each "
    "element is separated and not overlap on each other, on a clean white studio background.\n\n"
    "[Shot 1] static image.\n\n"
    "<CHARACTER> on white background, sprite sheet showing <CHARACTER> composition adapted following all "
    "possible variants and angles:\n"
    "1. <CHARACTER> On the left portrait (head and chest) closeup composition on white background.\n"
    "2. <CHARACTER> In the center full body view from 3 different angles: straight from front, straight from "
    "side, straight from back — all wearing the complete team kit from <Picture 2>, with the white name "
    "JAISAL centered on the upper back of the jersey and clean white football boots.\n"
    "3. <CHARACTER> On the right 6 round images (same size 2x3 vertical narrow row) with <CHARACTER>'s "
    "highlight details: single eye, lips, single ear (in circle), hair color, detailed skin texture color, "
    "outfit texture color (the royal blue jersey fabric and the small white clenched-fist roundel emblem "
    "from <Picture 2>).\n\n"
    "overall_soundscape: N/A\n\n"
    "non_diegetic_music: N/A"
)

for path in OUTS["05e"]:
    j = json.load(open(path, encoding="utf-8"))
    n28 = next(n for n in j["nodes"] if n["id"] == 28)
    assert n28["type"] == "MiniMaxH3ReferenceToVideo"
    n28["widgets_values"][0] = PROMPT_05E
    json.dump(j, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("updated 05e:", path)

for path in OUTS["05d"]:
    j = json.load(open(path, encoding="utf-8"))
    n28 = next(n for n in j["nodes"] if n["id"] == 28)
    assert n28["type"] == "MiniMaxH3ReferenceToVideo"
    n28["widgets_values"][0] = PROMPT_05D
    json.dump(j, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("updated 05d:", path)
print("\nDONE — both H3 workflows now use the authors' sprite-sheet prompting technique")
