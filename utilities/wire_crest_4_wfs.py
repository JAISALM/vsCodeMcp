#!/usr/bin/env python
"""Wire the crest ref + strengthen kit/emblem prompts in all 4 Jaisal sheet workflows
(both UI + project copies). No runs — user runs them.

Changes:
  05d: + LoadImage 900 (jaisal_crest_ref.png) -> ref_image_2 (slot 5, link 204);
       prompt += <Picture 3> crest ref; emblem = 'exactly as <Picture 3>';
       6th detail circle = crest emblem alone.
  05e: + LoadImage 900 -> ref_image_1 (slot 4, link 726);
       prompt += <Picture 2> crest ref; same emblem/detail updates.
  08j: 84 prompt = stronger emblem spec + separate round crest detail + plain jersey;
       85 negative: drop generic 'logo' (was suppressing the crest), add emblem negatives.
  09j: 555 PE custom prompt (was '') = full kit spec; 478 ROLE (main + subgraph def)
       += KIT SPEC section before # USER.
"""
import json, copy, os

UI = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
PRJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"

CREST_FILE = "jaisal_crest_ref.png"

# ---------------------------------------------------------------- 05d prompt
P05D = """iintegrated_multimodal_description:

subject_definitions:
<CHARACTER> character from <Picture 1> — a ~26-year-old Indian man, wavy medium-length black hair, a small patchy short beard, slim build, medium-brown Indian skin. META for composition: <CHARACTER> wears the complete team kit from <Picture 2>.
<Picture 1> is the identity source portrait of <CHARACTER>.
<Picture 2> is the team-kit reference: a plain royal blue short-sleeve soccer jersey (single flat royal blue color, no patterns) with the team crest on the left chest and matching royal blue track pants with a single white stripe down each side.
<Picture 3> is the team crest emblem reference: a white clenched raised fist (fist of resistance) inside a thin white circle on a royal blue background — the fist fully visible with all four fingers and the thumb clear, crisp and legible.

summary:
[reference generation] static image of sprite sheet, keep the exactly same art style of <Picture 1>.

retention_analysis:
<CHARACTER>: fully_preserved — face, hair, beard, skin tone and body build come only from <Picture 1>.
<Picture 2>: partially_preserved — costume design, colors and emblem only; never inherit any donor face or body from <Picture 2>.
<Picture 3>: fully_preserved — the crest emblem (white clenched fist in a thin circle) is copied exactly, no redesign.

detailed_description:
The target image is a static image of sprite sheet showing <CHARACTER> from different angles, each element is separated and not overlap on each other, on a clean white studio background.

[Shot 1] static image.

<CHARACTER> on white background, sprite sheet showing <CHARACTER> composition adapted following all possible variants and angles:
1. <CHARACTER> On the left portrait (head and chest) closeup composition on white background.
2. <CHARACTER> In the center full body view from 3 different angles: straight from front, straight from side, straight from back — all wearing the complete team kit from <Picture 2>, with the team crest on the left chest rendered exactly as <Picture 3> (a white clenched raised fist inside a thin white circle, all four fingers and the thumb fully visible, crisp and legible, no distortion) and the white name JAISAL centered on the upper back of the jersey and clean white football boots.
3. <CHARACTER> On the right 6 round images (same size 2x3 vertical narrow row) with <CHARACTER>'s highlight details: single eye, lips, single ear (in circle), hair color, detailed skin texture color, and the team crest emblem alone on royal blue, exactly as <Picture 3> (white clenched raised fist in a thin circle, all fingers and thumb clearly visible, crisp and legible).

overall_soundscape: N/A

non_diegetic_music: N/A
"""

# ---------------------------------------------------------------- 05e prompt
P05E = """iintegrated_multimodal_description:

subject_definitions:
<CHARACTER> character from <Picture 1> — a ~26-year-old Indian man, wavy medium-length black hair, a small patchy short beard, slim build, medium-brown Indian skin. META for composition: <CHARACTER> wears the complete team kit — a plain royal blue short-sleeve soccer jersey (single flat royal blue color, no patterns) with the team crest on the left chest, matching royal blue track pants with a single white stripe down each side, clean white football boots, and the white name JAISAL centered on the upper back of the jersey.
<Picture 1> is the identity source portrait of <CHARACTER>.
<Picture 2> is the team crest emblem reference: a white clenched raised fist (fist of resistance) inside a thin white circle on a royal blue background — the fist fully visible with all four fingers and the thumb clear, crisp and legible.

summary:
[reference generation] static image of sprite sheet, keep the exactly same art style of <Picture 1>.

retention_analysis:
<CHARACTER>: fully_preserved — face, hair, beard, skin tone and body build come only from <Picture 1>.
<Picture 2>: fully_preserved — the crest emblem is copied exactly (white clenched fist in a thin circle), no redesign.

detailed_description:
The target image is a static image of sprite sheet showing <CHARACTER> from different angles, each element is separated and not overlap on each other, on a clean white studio background.

[Shot 1] static image.

<CHARACTER> on white background, sprite sheet showing <CHARACTER> composition adapted following all possible variants and angles:
1. <CHARACTER> On the left portrait (head and chest) closeup composition on white background.
2. <CHARACTER> In the center full body view from 3 different angles: straight from front, straight from side, straight from back — all wearing the complete team kit, with the team crest on the left chest rendered exactly as <Picture 2> (a white clenched raised fist inside a thin white circle, all four fingers and the thumb fully visible, crisp and legible).
3. <CHARACTER> On the right 6 round images (same size 2x3 vertical narrow row) with <CHARACTER>'s highlight details: single eye, lips, single ear (in circle), hair color, detailed skin texture color, and the team crest emblem alone on royal blue, exactly as <Picture 2> (white clenched raised fist in a thin circle, all fingers and thumb clearly visible, crisp and legible).

overall_soundscape: N/A

non_diegetic_music: N/A
"""

# ---------------------------------------------------------------- 08j prompts
P08J_POS = """kr2realism, a full-body character turnaround sheet of the same man from the reference image, wearing a plain royal blue short-sleeve soccer jersey (single flat royal blue color, no patterns, no numbers on the front) with the team crest emblem on the left chest — a white clenched raised fist inside a thin white circle, the fist fully visible with all four fingers and the thumb clearly visible, crisp edges, legible, no distortion — matching royal blue track pants with a single white stripe down each side, clean white football boots, and the white name JAISAL in the center of the upper back of the jersey. Exactly four elements arranged in a row, left to right, on a neutral light-grey studio background: front view relaxed A-pose, strict 90-degree right-side profile, back view, and one round close-up of the crest emblem alone on a royal blue background. Same scale and identical ground line in the three body views. The face stays exactly the same man in every view. Even studio lighting, photoreal, sharp detail."""

P08J_NEG = """stick figure, duplicate character, multiple people, watermark, words, letters, text, slogan, changed face, different person, helmet, mask, cropped head, cropped feet, extra panel, action pose, malformed emblem, deformed fist, missing fingers, extra fingers, illegible crest, blurred emblem, distorted logo"""

# ---------------------------------------------------------------- 09j texts
P09J_PE = """Character design sheet of JAISAL — the man from the reference image, keep his exact face, wavy medium-length black hair, small patchy short beard, slim build. He wears the complete team kit in every body view: a plain royal blue short-sleeve soccer jersey (single flat royal blue color, no patterns) with the team crest on the left chest — a white clenched raised fist (fist of resistance) inside a thin white circle, all four fingers and the thumb fully visible, crisp and legible — the white name "JAISAL" centered on the upper back of the jersey, matching royal blue track pants with a single white stripe down each side, clean white football boots. Include a dedicated detail close-up of the crest emblem alone on a royal blue background, and a turnaround row (front, side, back) all wearing the complete kit. Photoreal high-end studio photography."""

KIT_SPEC = """## KIT SPEC (design source #2 — overrides any observed wardrobe)
Entity JAISAL wears the team kit in every view that shows the body: a plain royal blue short-sleeve soccer jersey (single flat royal blue color, no patterns, no numbers on the front), the team crest on the left chest = a white clenched raised fist (fist of resistance) inside a thin white circle — the fist fully visible, all four fingers and the thumb clearly visible, crisp and legible — the white name "JAISAL" centered on the upper back of the jersey, matching royal blue track pants with a single white stripe down each side, clean white football boots. Include ONE dedicated detail tile showing the crest emblem alone on a royal blue background. The reference image governs face, hair, skin and body ONLY; the kit above governs clothing.

"""

def add_crest_node(j, ref_id, new_link_id):
    """Deep-copy an existing LoadImage node as node 900 pointing at the crest ref."""
    ns = {n["id"]: n for n in j["nodes"]}
    ref = ns[ref_id]
    new = copy.deepcopy(ref)
    new["id"] = 900
    new["pos"] = [ref["pos"][0] + 360, ref["pos"][1]]
    for i in new["inputs"]:
        i["link"] = None
    new["outputs"] = [
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [new_link_id]},
        {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
    ]
    new["widgets_values"] = [CREST_FILE, "image"]
    j["nodes"].append(new)
    j["links"].append([new_link_id, 900, 0, 28, None, "IMAGE"])  # to_slot fixed per workflow below
    return new

def fix_link_toslot(j, new_link_id, slot):
    for l in j["links"]:
        if l[0] == new_link_id:
            l[3] = 28
            l[4] = slot

def edit_05d(j):
    ns = {n["id"]: n for n in j["nodes"]}
    add_crest_node(j, 72, 204)          # crest LoadImage -> link 204
    fix_link_toslot(j, 204, 5)          # ref_image_2 = input slot 5
    ns[28]["inputs"][5]["link"] = 204
    ns[28]["widgets_values"][0] = P05D
    j["last_link_id"] = 204

def edit_05e(j):
    ns = {n["id"]: n for n in j["nodes"]}
    add_crest_node(j, 25, 726)          # crest LoadImage -> link 726
    fix_link_toslot(j, 726, 4)          # ref_image_1 = input slot 4
    ns[28]["inputs"][4]["link"] = 726
    ns[28]["widgets_values"][0] = P05E
    j["last_link_id"] = 726

def edit_08j(j):
    ns = {n["id"]: n for n in j["nodes"]}
    assert "three equal full-body photographs" in ns[84]["widgets_values"][0]
    ns[84]["widgets_values"][0] = P08J_POS
    assert "logo" in ns[85]["widgets_values"][0]
    ns[85]["widgets_values"][0] = P08J_NEG

def edit_09j(j):
    ns = {n["id"]: n for n in j["nodes"]}
    assert ns[555]["widgets_values"][0] in ("", None) or not ns[555]["widgets_values"][0]
    ns[555]["widgets_values"][0] = P09J_PE
    # 478 ROLE — main canvas copy
    role = ns[478]["widgets_values"][0]
    assert "# USER" in role
    ns[478]["widgets_values"][0] = role.replace("\n# USER", "\n" + KIT_SPEC + "# USER", 1)
    # 478 ROLE — subgraph definition copy
    for sg in j.get("definitions", {}).get("subgraphs") or []:
        for n in sg["nodes"]:
            if n["id"] == 478 and "# USER" in n["widgets_values"][0] and "## KIT SPEC" not in n["widgets_values"][0]:
                n["widgets_values"][0] = n["widgets_values"][0].replace("\n# USER", "\n" + KIT_SPEC + "# USER", 1)
                print("  09j subgraph-def 478 ROLE updated")

EDITS = {
    "05d_charsheet_H3_wide_jaisal.json": edit_05d,
    "05e_charsheet_H3_fizgig_jaisal.json": edit_05e,
    "08j_KREA2_JAISAL_sheet.json": edit_08j,
    "09j_QWEN21_JAISAL_sheet.json": edit_09j,
}

for name, fn in EDITS.items():
    for base in (UI, PRJ):
        p = os.path.join(base, name)
        j = json.load(open(p, encoding="utf-8"))
        fn(j)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(j, f, indent=4, ensure_ascii=False)
        print(f"edited {p}")
print("ALL DONE")
