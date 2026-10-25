#!/usr/bin/env python
"""10a_frontal3_zidane_i2i.json — THE FACE LOCK (D163).

Diagnosis (user turn 71: "the face is still somehow long ... it's creating similar
images ... idealy it should create a different man altogether right? ... there is
definetly something in the underhood"):
- Krea2 face = f(PROMPT, SEED, chain, resolution) — all four together.
- The APPROVED zidane face (refset_v7/zidane_portrait_00001_.png) was made with a
  live-typed prompt that was NEVER SAVED. Every reconstructed prompt (v3..v6) lands
  in a different face region — near Jaisal's — no seed fix can bring the approved
  face back. t2i re-rolling is a DEAD END.
- The character IS the approved image. The only reliable frontal version = i2i FROM
  that image: his pixels anchor the face, the model only rotates the head.
- v4's i2i at denoise 0.4 came out = the input (too weak). THIS one: denoise 0.55
  (head rotation needs 0.5-0.6).

Chain = his HOME chain (01): Krea2Realism_V1 + Krea2-realism-V2@1.0, qwen3vl_4b
(krea2), qwen_image_vae, 8 steps euler/simple cfg 1, 1152x2048 (the image's native
resolution). LoadImage zidane_portrait_00001_.png (input dir) -> VAEEncode ->
KSampler [77 fixed, denoise 0.55] -> VAEDecode -> SaveImage FACEFRONTAL3_ZIDANE.
"""
import copy, json, os

SRC = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\01_character_sheet.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\10a_frontal3_zidane_i2i.json"
IMG = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\zidane_portrait_00001_.png"
assert os.path.exists(IMG), "missing i2i source: " + IMG

# Identity anchor first (his face comes from the IMAGE, not the prompt), then the
# target pose, then attributes the image already has (halal cut, beard, white tee).
POS = ("kr2realism. The exact same man as the reference image — the SAME face, SAME "
"facial structure, same skin — now completely frontal: dead center, head straight, "
"both eyes fully open, looking straight into the camera with a relaxed easy "
"half-smile. His hair is a short black halal cut with very short faded sides and a "
"short neat crop on top, no waves. He has a full short dark beard, neatly trimmed "
"and shaped, dense and clearly visible on his chin, jaw and upper lip. He wears a "
"plain white t-shirt. Soft even natural daylight, a clean plain off-white wall "
"behind him, sharp focus on his face, realistic skin with visible pores and a "
"healthy flush, looks like a real unposed photo someone took on their phone, only "
"one character, no other people.")

NEG = ("different person, different face, duplicate character, multiple people, "
"watermark, logo, deformed face, bad eyes, extra fingers, profile view, "
"three-quarter view, head turned to the side, head tilted, looking away from "
"camera, long hair, wavy hair, man-bun, topknot, ponytail, clean-shaven, no "
"beard, missing beard")

j = json.load(open(SRC, encoding="utf-8"))
assert j["id"] == "krea2-t2i-character"
# drop the t2i branch (82 latent / 53 sampler / 54 decode / 29 save)
keep = [n for n in j["nodes"] if n["id"] not in (82, 53, 54, 29)]
j["nodes"] = keep
j["links"] = [l for l in j["links"] if l[1] not in (82, 53, 54, 29) and l[3] not in (82, 53, 54, 29)]

def node(nid, ntype, pos, widgets, inputs, outputs):
    return {"id": nid, "type": ntype, "pos": pos, "size": [225, 54], "flags": {},
            "order": 0, "mode": 0, "inputs": inputs, "outputs": outputs,
            "properties": {"Node name for S&R": ntype, "cnr_id": "comfy-core", "ver": "0.26.0"},
            "widgets_values": widgets}

# native shapes (copied from krea2_identity_edit.json UI-saved nodes)
j["nodes"].append(node(85, "LoadImage", [-1400, -100], ["zidane_portrait_00001_.png", "image"],
    [{"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
     {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None}],
    [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None},
     {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None}]))
j["nodes"].append(node(86, "VAEEncode", [-950, -60], [],
    [{"localized_name": "pixels", "name": "pixels", "type": "IMAGE", "link": None},
     {"localized_name": "vae", "name": "vae", "type": "VAE", "link": None}],
    [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": None}]))
j["nodes"].append(node(323, "KSampler", [-450, -60], [77, "fixed", 8, 1, "euler", "simple", 0.55],
    [{"localized_name": "model", "name": "model", "type": "MODEL", "link": None},
     {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "link": None},
     {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "link": None},
     {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT", "link": None}],
    [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": None}]))
j["nodes"].append(node(324, "VAEDecode", [0, -60], [],
    [{"localized_name": "samples", "name": "samples", "type": "LATENT", "link": None},
     {"localized_name": "vae", "name": "vae", "type": "VAE", "link": None}],
    [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None}]))
j["nodes"].append(node(325, "SaveImage", [450, -60], ["FACEFRONTAL3_ZIDANE"],
    [{"localized_name": "images", "name": "images", "type": "IMAGE", "link": None}],
    []))

n300 = next(n for n in j["nodes"] if n["id"] == 300)
n301 = next(n for n in j["nodes"] if n["id"] == 301)
n300["widgets_values"] = [POS]
n301["widgets_values"] = [NEG]

maxlink = max(l[0] for l in j["links"])
lid = maxlink
def newlink():
    global lid
    lid += 1
    return lid

for src_id, src_slot, to_id, to_slot, ttype in [
    (96, 0, 323, 0, "MODEL"),
    (300, 0, 323, 1, "CONDITIONING"),
    (301, 0, 323, 2, "CONDITIONING"),
    (85, 0, 86, 0, "IMAGE"),
    (57, 0, 86, 1, "VAE"),
    (86, 0, 323, 3, "LATENT"),
    (323, 0, 324, 0, "LATENT"),
    (57, 0, 324, 1, "VAE"),
    (324, 0, 325, 0, "IMAGE"),
]:
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

j["id"] = "10a_frontal3_zidane_i2i"
json.dump(j, open(DST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", DST, os.path.getsize(DST), "| nodes:", len(j["nodes"]), "| links:", len(j["links"]))
