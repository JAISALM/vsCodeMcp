"""Smoke-test setup for the obvpm timeline workflow:
- add 2 native-shape LoadImage nodes (Jaisal bridge refs)
- wire them into R2V node 797 ref_image_0/1 (replace bundle-sourced links 2314/2315)
- set the 2-anchor R2V prompt on subgraph node 763
- report ResolutionSelector 1086 current widget
"""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

# 1. add LoadImage nodes (native shape)
def load_image(nid, filename, x, y):
    return {
        "id": nid, "type": "LoadImage", "pos": [x, y], "size": [282.78, 322],
        "flags": {}, "order": 900, "mode": 0,
        "inputs": [
            {"localized_name": "image", "name": "image", "type": "COMBO",
             "widget": {"name": "image"}, "link": None},
            {"localized_name": "choose file to upload", "name": "upload",
             "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [2314]},
            {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
        ],
        "properties": {"Node name for S&R": "LoadImage"},
        "widgets_values": [filename, "image"],
    }

j["nodes"].append(load_image(2001, "jaisal_1_longshot.png", 1900, 120))
j["nodes"].append(load_image(2002, "jaisal_4_middle.png", 1900, 480))

# 2. re-point links 2314/2315 to the new nodes
for L in j["links"]:
    a = list(L)
    if a[0] == 2314:
        L[1] = 2001
        L[2] = 0
    if a[0] == 2315:
        L[1] = 2002
        L[2] = 0

# 3. set the prompt on subgraph node 763 (PrimitiveStringMultiline)
PROMPT = """[reference generation]

<Subject 1>: a young Indian schoolboy with short dark hair, wearing a rose-pink collared short-sleeve shirt, full-length black trousers, carrying a black school bag.

summary: a continuous 5-second tracking shot. <Picture 1> is the first frame: a wide view of the stone bridge over the backwater with <Subject 1> walking on the left side of the bridge. <Picture 2> is the middle of the shot: a medium view of <Subject 1> walking along the bridge.

retention_analysis:
<Subject 1> face, hair, clothing: fully_preserved
bridge, water, environment: fully_preserved

detailed_description:
[Shot 1] At 00:00.000 - wide tracking shot at bridge level. <Subject 1> walks steadily from the left side of the stone bridge toward the middle. The camera slowly dollies forward and pans slightly right, following him. Overcast grey sky, soft diffuse light, dark green palms on both banks, calm dark water below.
[Shot 2] At 00:02.500 - the camera settles into a medium shot of <Subject 1> in the middle of the bridge. He keeps walking at a steady pace, the black bag swaying gently. The stone railings pass by on both sides.

overall_soundscape: natural ambient only - soft rain on stone, gentle lapping water, distant birds, the boy's footsteps on the wet bridge.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient sounds only."""

for s in j["definitions"]["subgraphs"]:
    for n in s["nodes"]:
        if n["id"] == 763:
            n["widgets_values"] = [PROMPT]
            print("763 prompt set")
        if n["id"] == 1086:
            print("1086 ResolutionSelector current widgets:", n.get("widgets_values"))
        if n["id"] == 1217:
            print("1217 PrimitiveString current widgets:", n.get("widgets_values"))

json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved")
