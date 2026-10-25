#!/usr/bin/env python
"""10a_frontal_base_zidane.json v7 — ROOT-CAUSE FIX (D164): distant seeds + NEW description.

Root cause (user: "we have to find out the root cause of why this is not generating
a new image and holding back"):
1. v6 set seeds to FIXED 76/77/78 — three ADJACENT numbers. Same seed 77 as the v4b
   run (00002) -> 00006 "so identical to 00002". Adjacent seeds = micro-variants of
   the same man. (The user's original suspicion — "are we doing it in same seed?" —
   was correct for v6.)
2. Every zidane prompt I wrote was structurally Jaisal's prompt with attributes
   swapped (same opening, same feature list) -> the face description anchors the
   face (evidence: jaisal's randomize frontals = same man across different seeds).
v7 = 01 home chain (Krea2Realism_V1 + V2@1.0, 8 steps, 1152x2048) + a GENUINELY NEW
description (face-shape-first, different opening/words — NOT jaisal's template) +
DISTANT seeds 250/777/4242 (far from 42/76/77/78 and from each other) -> three
genuinely different men to pick from. i2i route DEAD (user: quality drift).
Saves FACEFRONTAL2_ZIDANE_{a,b,c} (root; next counter _00007_).
"""
import copy, json, os

SRC = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\01_character_sheet.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\10a_frontal_base_zidane.json"

# v7: GENUINELY NEW description — face-shape FIRST, different opening and words from
# every previous attempt (jaisal's template is retired). Keep the kr2realism style
# trigger; change the description itself.
POS = ("kr2realism. Close-up photo of a young South Indian man facing the camera dead-"
"on, his face filling most of the frame. His face is round and full-cheeked — wide, "
"soft, with a short strong jaw — warm medium-brown skin with natural pores and a "
"healthy flush. His hair is a short black halal haircut: very short faded sides and "
"back, a short neat crop on top, no waves, no bun. A full short dark beard, neatly "
"trimmed and shaped, dense on the chin, jawline and upper lip. He is lean and slim, "
"wearing a plain white t-shirt. He looks straight into the camera with a relaxed "
"half-smile. Natural even daylight, a plain off-white wall behind him, sharp focus on "
"the face, looks like a real unposed phone photo, one person only, no other people.")

NEG = ("duplicate character, multiple people, watermark, logo, deformed face, bad eyes, "
"extra fingers, profile view, three-quarter view, head turned to the side, head "
"tilted, looking away from camera, long hair, wavy hair, man-bun, topknot, ponytail, "
"clean-shaven, no beard, missing beard")

j = json.load(open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
assert j["id"] == "krea2-t2i-character"
assert nodes[55]["widgets_values"][0] == "Krea2Realism_V1.safetensors"
assert nodes[82]["widgets_values"] == [1152, 2048, 1]
assert nodes[53]["widgets_values"][0] == 42

# shared: prompt / negative / branch A
nodes[300]["widgets_values"] = [POS]
nodes[301]["widgets_values"] = [NEG]
nodes[53]["widgets_values"] = [250, "fixed", 8, 1, "euler", "simple", 1]
nodes[29]["widgets_values"] = ["FACEFRONTAL2_ZIDANE_a"]

# branches B (seed 76) and C (seed 78): deepcopy the a-branch nodes
def branch(new_ids, seed, save_prefix, x_off):
    nks, ndec, nsave = None, None, None
    for n in j["nodes"]:
        if n["id"] == 53: nks = copy.deepcopy(n)
        if n["id"] == 54: ndec = copy.deepcopy(n)
        if n["id"] == 29: nsave = copy.deepcopy(n)
    nks["id"], ndec["id"], nsave["id"] = new_ids
    nks["pos"] = [nks["pos"][0] + x_off, nks["pos"][1]]
    ndec["pos"] = [ndec["pos"][0] + x_off, ndec["pos"][1]]
    nsave["pos"] = [nsave["pos"][0] + x_off, nsave["pos"][1]]
    nks["widgets_values"] = [seed, "fixed", 8, 1, "euler", "simple", 1]
    nsave["widgets_values"] = [save_prefix]
    # clear the copied link lists; rebuild from the links array at the end
    for n in (nks, ndec, nsave):
        for o in n["outputs"]:
            o["links"] = None
    j["nodes"].append(nks)
    j["nodes"].append(ndec)
    j["nodes"].append(nsave)

branch((314, 315, 317), 777, "FACEFRONTAL2_ZIDANE_b", 400)
branch((319, 320, 322), 4242, "FACEFRONTAL2_ZIDANE_c", 800)

# links (format: [id, from_node, from_slot, to_node, to_slot, type])
maxlink = max(l[0] for l in j["links"])
lid = maxlink
def newlink():
    global lid
    lid += 1
    return lid

fan = [
    # source, slot -> (targets, slot, type)
    (96, 0, [(314, 0, "MODEL"), (319, 0, "MODEL")]),
    (82, 0, [(314, 3, "LATENT"), (319, 3, "LATENT")]),
    (300, 0, [(314, 1, "CONDITIONING"), (319, 1, "CONDITIONING")]),
    (301, 0, [(314, 2, "CONDITIONING"), (319, 2, "CONDITIONING")]),
    (57, 0, [(315, 1, "VAE"), (320, 1, "VAE")]),
    (314, 0, [(315, 0, "LATENT")]),
    (315, 0, [(317, 0, "IMAGE")]),
    (319, 0, [(320, 0, "LATENT")]),
    (320, 0, [(322, 0, "IMAGE")]),
]
for src_id, src_slot, targets in fan:
    for to_id, to_slot, ttype in targets:
        j["links"].append([newlink(), src_id, src_slot, to_id, to_slot, ttype])

# rebuild every output's links list AND every input's link field from the links array
from collections import defaultdict
outmap = defaultdict(list)
inmap = {}
for l in j["links"]:
    outmap[(l[1], l[2])].append(l[0])
    inmap[(l[3], l[4])] = l[0]
for n in j["nodes"]:
    for i, o in enumerate(n["outputs"]):
        here = outmap.get((n["id"], i))
        o["links"] = here if here else None
    for i, inp in enumerate(n.get("inputs", [])):
        inp["link"] = inmap.get((n["id"], i))

j["id"] = "10a_frontal_base_zidane"
json.dump(j, open(DST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", DST, os.path.getsize(DST), "| nodes:", len(j["nodes"]), "| links:", len(j["links"]))
