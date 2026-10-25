#!/usr/bin/env python
"""Build the full A/B/C character-sheet test set (2026-10-18).

A = 2BZ H3 2-stage (MiniMax)  : E:\minimax_workflow\character_sheet\2BZ_H3_character_sheet_2stage_v1_EN.json
B = LEEBLAAB Qwen Image 2.1    : E:\minimax_workflow\character_sheet\LEEBLAAB-QwenImage21-Character-SHEET.json
C = Krea2 t2i 3-view strip     : D:\models\vsCodeMcp\challenge\consistent-short\workflows\01_character_sheet.json

Per character:
  A: node 16 = <char>_portrait_HD.png (face), node 21 = <char>_kit_ref.png (outfit),
     nodes 22/57/58/59 = neutral_placeholder.png, node 13 widget0 = character master prompt,
     node 106 = charsheet/H3_<CHAR>_3VIEW
  B: instance 459 widget0 = 10-section sheet prompt, widget7 = seed, widget8 = qwen_image_2.1_bf16
     (widgets 9/10 already match disk), 470 = <char>_portrait_HD.png, 461 = charsheet/QWEN_<CHAR>
  C: 01-based: 300 = 3-view strip prompt, 301 = clean negative, 82 = [2048,1152,1], 29 = charsheet/KREA2_<CHAR>
"""
import json
import os
import shutil

UI = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
PROJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"
A_SRC = r"E:\minimax_workflow\character_sheet\2BZ_H3_character_sheet_2stage_v1_EN.json"
B_SRC = r"E:\minimax_workflow\character_sheet\LEEBLAAB-QwenImage21-Character-SHEET.json"
C_SRC = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\01_character_sheet.json"

# ---------------------------------------------------------------------- A
def a_master(char, build, hair, beard, kit, name):
    return f"""subject_definitions:
<Subject 1> is the same ~26-year-old Indian man in <Picture 1>: {build} build, {hair}, {beard}, medium-brown Indian skin tone, brown eyes.
<Picture 1> is the source portrait of <Subject 1> against a neutral background.
<Picture 2> is the team-kit reference: a {kit} soccer jersey with a small subtle white emblem on the left chest — a clenched fist inside a thin circle, no text — and matching {kit} track pants with a single white side stripe; the jersey carries the player name {name} in white letters on the back.

summary:
[reference generation] Create one static high-resolution character sheet of <Subject 1> wearing the complete <Picture 2> team kit, preserving his exact facial identity, hair, beard, skin tone and body build from <Picture 1>. The name {name} appears in white letters on the back of the jersey.

retention_analysis:
<Subject 1>: fully_preserved - identity, age, hair, beard, skin tone and body proportions come only from <Picture 1>.
<Picture 1>: fully_preserved - sole identity reference.
<Picture 2>: partially_preserved - costume design, colors and crest only; never inherit any donor face or body from Picture 2.

detailed_description:
The target is one still image, not a video. <Subject 1> is a recognizable adult Indian footballer wearing the {kit} kit from <Picture 2>: {kit} jersey with a small subtle white clenched-fist roundel emblem on the left chest (no text), matching {kit} track pants with a single white stripe down each side, and the white name {name} on the back of the jersey. Keep his face exactly as in <Picture 1> in every view. Do not merge views, do not add extra people, and keep all views at the same scale on the same neutral studio background."""

# ---------------------------------------------------------------------- B
def b_sections(char, name, build, hair, beard, kit, kit_swatches):
    return f"""1. 3:2 landscape composition on warm off-white paper with a thin ink-black border inset 3% from every edge and signature-gradient corner ticks; seven zones defined as Zone A left metadata column x 0-18%, Zone B central hero x 18-62%, Zone C top-right turnaround row y 8-30%, Zone D mid-right action panel y 30-62%, Zone E bottom-left silhouette study lower-left quadrant, Zone F bottom-center expression study lower-middle, and Zone G bottom-right detail grid remaining lower-right area, separated by light warm gray hairline dividers; global rendering style is photoreal sports character photography with cinematic lighting, natural skin texture, and crisp fabric detail matching a professional team-photo medium; hero-only backdrop features a soft neutral studio sweep with gentle floor shadow exclusively within Zone B; visual cohesion maintained through a closed palette of {kit} kit color, white accent, ink black, warm dark gray, and warm off-white paper, with a high-contrast Didone display serif used for the title only, medium-bold warm dark gray letter-spaced uppercase sans-serif for section headers with gradient dot icons, and regular small ink-black sans-serif for all labels, values and captions.

2. Left metadata column displays title "{name}" in Didone serif font followed by caption "FOOTBALLER DESIGN SHEET" in letter-spaced uppercase sans-serif separated by a gradient divider line; three identity rows present small circular icons with quoted uppercase labels and values reading "AGE" "26 YEARS", "BUILD" "{build.upper()}", and "TEAM" "SOLIDARITY" derived from the character design; below these rows sits one horizontal array of three circular material swatches showing the exact kit colors with quoted labels {kit_swatches} positioned beneath each respective swatch; all elements are strictly left-aligned within the x 0-18% column boundary using regular small ink-black sans-serif for label text and maintaining consistent spacing without decorative embellishment.

3. Central hero view presents one dominant full-body figure in a three-quarter footballer stance with weight on the back leg, relaxed confident posture, and a calm focused expression; full restatement of identity locks includes {hair}, {beard}, {build} build, medium-brown Indian skin, the {kit} jersey with the small white clenched-fist roundel crest on the left chest, matching {kit} track pants with a single white side stripe down each side, and clean white football boots; the hero backdrop contains a soft neutral studio sweep with a gentle floor shadow and no other objects; caption "CENTRAL HERO VIEW" appears below in quoted text accompanied by a gradient dot icon.

4. Top-right turnaround row header reads "TURNAROUND ROW" in quoted medium-bold warm dark gray letter-spaced uppercase sans-serif with a gradient dot icon preceding the text; three full-body neutral views rendered at identical scale on a thin ink-gray baseline with soft gray oval contact shadows include a front view showing the clenched-fist roundel crest on the left chest and the relaxed A-pose stance, a clean side profile showing the {hair} volume contour and the single white stripe running down the track pant side, and a back view clearly showing the white player name "{name}" centered on the upper back of the jersey; centered quoted labels "FRONT VIEW", "SIDE VIEW", and "BACK VIEW" appear beneath the respective figures in regular small ink-black sans-serif font maintaining precise alignment within the y 8-30% zone.

5. Mid-right action panel header states "ACTION POSE REFERENCE" in quoted medium-bold warm dark gray letter-spaced uppercase sans-serif with a gradient dot icon; three full-body football action views contained within rounded-corner light warm gray tiles depict (a) a low dribbling stance with the ball at the feet, weight dropped and knees bent, (b) a two-fisted celebration with arms raised after scoring, and (c) a defending stance with arms out wide and feet planted; each tile keeps the exact same {kit} kit with crest on the left chest and the name "{name}" on the back where the back is visible; centered quoted labels "DRIBBLE", "CELEBRATION", and "DEFENDING" appear beneath each tile in regular small ink-black sans-serif font maintaining uniform sizing within the y 30-62% zone.

6. Bottom-left silhouette study header displays "SILHOUETTE STUDY" in quoted medium-bold warm dark gray letter-spaced uppercase sans-serif with a gradient dot icon; three solid ink-black silhouettes rendered with zero interior detail preserve the exact outline geometry of the character including the {hair} arc, the shoulder line of the {build} build, and the track pant leg line; the three views are frontal, pure profile, and rear, arranged triangularly with the profile silhouette largest at center flanked by smaller frontal and rear variants; tiny quoted labels "FRONTAL", "PROFILE", and "REAR" appear beneath the respective silhouettes in regular small ink-black sans-serif font maintaining minimal size and precise centering within the lower-left quadrant.

7. Bottom-center expression study presents three compact head-and-shoulders studies on a shared baseline maintaining the exact facial identity, {hair}, and {beard} from the reference portrait; the neutral state shows a calm closed-mouth expression with relaxed eyes; the celebrating state shows an open-mouthed joyful shout with head tilted back slightly; the determined state shows a focused forward gaze with set jaw; tiny centered quoted labels "NEUTRAL", "CELEBRATING", and "DETERMINED" appear beneath the respective studies in regular small ink-black sans-serif font maintaining consistent baseline alignment within the lower-middle zone.

8. Bottom-right detail close-up grid header reads "DETAIL CLOSE-UPS" in quoted medium-bold warm dark gray letter-spaced uppercase sans-serif with a gradient dot icon; six rounded-corner square tiles arranged in two rows of three contain extreme close-up renders with centered quoted captions: top row includes (1) "CREST MACRO" showing the small white clenched-fist roundel emblem (no text) on the {kit} jersey fabric, (2) "JERSEY FABRIC" showing the knit weave and collar detail of the {kit} jersey, and (3) "TRACK PANT STRIPE" showing the single white side stripe on the {kit} track pant; bottom row features (4) "FACE CLOSE-UP" preserving the exact reference face, hair and beard, (5) "BACK NAME" showing the white name "{name}" centered on the upper back of the jersey, and (6) "BOOT DETAIL" showing the clean white football boot; all captions use regular small ink-black sans-serif font centered beneath the respective tiles.

9. Typography hierarchy mandates the Didone display serif reserved exclusively for the hero title "{name}" while all section headers employ medium-bold warm dark gray letter-spaced uppercase sans-serif with gradient dot icons; labels, values and captions use regular small ink-black sans-serif left-aligned within the metadata column and centered beneath the detail tiles; the closed palette discipline restricts color usage to the {kit} kit color, white accent, ink black, warm dark gray, and warm off-white paper only, with the signature gradient applied strictly to frame ticks, header dots and swatch borders; the neutral studio backdrop remains exclusive to the central hero panel in Zone B and never appears in the other zones; photoreal sports photography rendering with natural skin texture and crisp fabric detail is consistent throughout all ten sections without stylistic drift.

10. Preserve the exact visible identity of "{name}" from the reference image across all views and tiles: the same {hair}, the same {beard}, the same {build} build, the same medium-brown Indian skin tone, and the same facial features and proportions in every face shown; the kit must stay exactly the {kit} jersey with the white clenched-fist roundel crest on the left chest plus the matching {kit} track pants with a single white side stripe in every full-body view; the white player name "{name}" must appear on the back of the jersey in every back view with correct spelling; do not change the face between views, do not add facial hair or hair changes absent from the reference, do not swap kit colors or add extra logos, and do not add other people; no duplicated figures, no merged views, no overlapping panels, no watermark, no text other than the quoted strings above; every rendered text string must appear exactly as quoted with exact spelling and capitalization."""

# ---------------------------------------------------------------------- C
def c_prompt(char, build, hair, beard, kit, name):
    return (
        f"Character design sheet on a clean light-gray studio background: three full-body views of the same ~26-year-old "
        f"Indian man arranged side by side — front view, strict right-side profile, and back view — at identical scale with "
        f"identical ground line. He has {hair}, {beard}, a {build} build, and medium-brown Indian skin. He wears a {kit} "
        f"soccer jersey with a small subtle white clenched-fist roundel emblem on the left chest (no text, just the fist symbol), "
        f"matching {kit} track pants with a "
        f"single white side stripe, clean white football boots, and the white name {name} in the center of the jersey back. "
        f"His face stays exactly consistent across all three views. Even studio lighting, photoreal, sharp. kr2realism"
    )

CHARS = [
    dict(
        char="jaisal", name="JAISAL", build="slim",
        hair="wavy medium-length black hair", beard="a small patchy short beard",
        kit="royal blue", swatches='"ROYAL BLUE", "WHITE", "INK BLACK"',
        seed=7, b_seed=42,
    ),
    dict(
        char="zidane", name="ZIDANE", build="athletic and muscular",
        hair="short black hair in a clean halal cut", beard="a full short neatly-trimmed beard",
        kit="dark green", swatches='"DARK GREEN", "WHITE", "INK BLACK"',
        seed=21, b_seed=43,
    ),
]

def load(p):
    return json.load(open(p, encoding="utf-8", errors="ignore"))

def save(j2, name, proj_name=None):
    ui = os.path.join(UI, name)
    json.dump(j2, open(ui, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"WROTE {ui}")
    if proj_name:
        pj = os.path.join(PROJ, proj_name)
        shutil.copy2(ui, pj)
        print(f"       + project copy {proj_name}")

# ============================== ROUTE A ==============================
a = load(A_SRC)
A_STAGE1_TEMPLATE = {n["id"]: n for n in a["nodes"]}[24]["widgets_values"][0]
# stage-2-only nodes that break validation while Stage 2 is OFF:
#   111 = Fast Groups Muter (frontend-only, no links)
#   125/126 = PreviewImage fed by the stage-2 subgraph (dangling in API graph)
#   127 = CustomCombo panel-count (feeds only stage-2 chains 49/139)
# Deleting them leaves the stage-1 path (5 -> 106 SaveImage) intact.
A_DELETE = {111, 125, 126, 127}
for c in CHARS:
    j2 = json.loads(json.dumps(a))
    n2 = {n["id"]: n for n in j2["nodes"]}
    n2[16]["widgets_values"] = [f"{c['char']}_portrait_HD.png", "image"]
    n2[21]["widgets_values"] = [f"{c['char']}_kit_ref.png", "image"]
    for opt in (22, 57, 58, 59):
        n2[opt]["widgets_values"] = ["neutral_placeholder.png", "image"]
    master = a_master(c["char"], c["build"], c["hair"], c["beard"], c["kit"], c["name"])
    # H3's prompt slot is LINKED from node 24 (link 127), so the character
    # description must ride in node 24's text or it never reaches the model.
    n2[24]["widgets_values"][0] = master + "\n\n" + A_STAGE1_TEMPLATE
    n2[13]["widgets_values"][0] = master  # documented fallback if link 127 is ever cut
    n2[106]["widgets_values"] = [f"charsheet/H3_{c['name']}_3VIEW"]
    j2["nodes"] = [n for n in j2["nodes"] if n["id"] not in A_DELETE]
    j2["links"] = [l for l in j2["links"] if l[1] not in A_DELETE and l[3] not in A_DELETE]
    save(j2, f"2BZ_H3_character_sheet_2stage - {c['char']}.json",
         f"05a_charsheet_H3_{c['char']}.json")

# ============================== ROUTE B ==============================
b = load(B_SRC)
bn = {n["id"]: n for n in b["nodes"]}
# sanity
assert bn[459]["widgets_values"][8] == "qwen_image_2.1_int8_convrot.safetensors"
assert bn[470]["type"] == "LoadImage" and bn[461]["type"] == "SaveImageAdvanced"
for c in CHARS:
    j2 = json.loads(json.dumps(b))
    n2 = {n["id"]: n for n in j2["nodes"]}
    n2[470]["widgets_values"] = [f"{c['char']}_portrait_HD.png", "image"]
    w = n2[459]["widgets_values"]
    w[0] = b_sections(c["char"], c["name"], c["build"], c["hair"], c["beard"], c["kit"], c["swatches"])
    w[7] = c["b_seed"]
    w[8] = "qwen_image_2.1_bf16.safetensors"          # quality-first bf16 (on disk)
    # w[9] = qwen3vl_8b_int8_convrot, w[10] = qwen_image_2.1_vae_bf16 — already match disk
    n2[461]["widgets_values"][0] = f"charsheet/QWEN_{c['name']}"
    # CRITICAL (subgraph rule): the converter reads widget values from the
    # INTERNAL nodes, not the instance — patch the loaders inside the subgraph.
    sg_nodes = {n["id"]: n for n in j2["definitions"]["subgraphs"][0]["nodes"]}
    assert sg_nodes[451]["type"] == "UNETLoader" and sg_nodes[453]["type"] == "CLIPLoader"
    sg_nodes[451]["widgets_values"][0] = "qwen_image_2.1_bf16.safetensors"
    sg_nodes[453]["widgets_values"][0] = "qwen3vl_8b_int8_convrot.safetensors"
    # internal 454 VAE = qwen_image_2.1_vae_bf16 — already matches disk
    save(j2, f"LEEBLAAB-QwenImage21-Character-SHEET - {c['char']}.json",
         f"05b_charsheet_QWEN_{c['char']}.json")

# ============================== ROUTE C ==============================
csrc = load(C_SRC)
cn = {n["id"]: n for n in csrc["nodes"]}
assert cn[300]["type"] == "CLIPTextEncode" and cn[301]["type"] == "CLIPTextEncode"
for c in CHARS:
    j2 = json.loads(json.dumps(csrc))
    n2 = {n["id"]: n for n in j2["nodes"]}
    n2[300]["widgets_values"] = [c_prompt(c["char"], c["build"], c["hair"], c["beard"], c["kit"], c["name"])]
    n2[301]["widgets_values"] = [
        "different face, inconsistent identity, changing face between views, extra people, duplicate faces, "
        "wrong jersey color, missing crest, blurry, low quality, watermark, deformed, extra limbs, "
        "text other than the player name"]
    n2[82]["widgets_values"] = [2048, 1152, 1]
    n2[53]["widgets_values"] = [c["seed"], "fixed", 8, 1, "euler", "simple", 1]
    n2[29]["widgets_values"] = [f"charsheet/KREA2_{c['name']}"]
    save(j2, f"07c_krea2_3view_sheet_{c['char']}.json",
         f"05c_charsheet_KREA2_{c['char']}.json")

print("ALL 6 VARIANTS BUILT")
