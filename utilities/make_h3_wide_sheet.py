#!/usr/bin/env python
"""Build 05d_charsheet_H3_wide_{char}.json — the civitai/cgpixel23 H3 wide multi-panel sheet,
adapted to our characters.

Adaptations from the author's workflow (data/civitai_embedded_workflow.json):
- 10 author refs (9 LoadImages + 9 ImageScaleToTotalPixels) -> replaced by OUR 2 refs:
  <char>_portrait_HD.png (identity, ref_image_0) + <char>_kit_ref.png (kit, ref_image_1).
- Author's test/NSFW/style LoRA chain (18/19/20/21) DELETED — UNET 10 feeds SigmaShift 40 directly.
- ANTI-PLASTIC (reddit 1wzcu5v thread, lavinia12345): turbo LoRA 39 + Spectrum 41 DELETED
  (both "screw up eyes"); chain = UNET 10 -> SigmaShift 40 -> AttentionBackend 60 ->
  EasyCache 42 -> {BasicScheduler 7 (beta, 30 steps), BasicGuider 9, KSamplerSelect 6 er_sde,
  RandomNoise 12 (fixed seed), SamplerCustomAdvanced 8} -> FizgigH3StillDecode 64 -> SaveImage 68.
- VAE 2 -> minimax_h3_t1_image_vae_step1597.safetensors (our H3 image VAE).
- H3 node 28: canvas 4096x1536 (wide multi-panel), length 5, ref_image_size 'max',
  prompt = R2V 6-section 3-view sheet (NEW CREST SPEC: fist roundel, no text).
- 12 RandomNoise: fixed seed per character. 68 SaveImage: charsheet/H3WIDE_{NAME}.
"""
import json, os, sys

SRC = r"D:\models\vsCodeMcp\data\civitai_embedded_workflow.json"
OUT_UI = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
OUT_PRJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"

def wide_prompt(char, build, hair, beard, kit, name):
    """AUTHORS' prompting technique (cgpixel23/civitai sprite-sheet template, copied verbatim
    structure): left portrait closeup + center 3-angle full-body + right 6 round detail
    images. <Picture 1> = our face ref, <Picture 2> = our kit flat-lay ref."""
    return (
        f"iintegrated_multimodal_description:\n\n"
        f"subject_definitions:\n"
        f"<CHARACTER> character from <Picture 1> — a ~26-year-old Indian man, {hair}, {beard}, a {build} build, medium-brown Indian skin. "
        f"META for composition: <CHARACTER> wears the complete team kit from <Picture 2>.\n"
        f"<Picture 1> is the identity source portrait of <CHARACTER>.\n"
        f"<Picture 2> is the team-kit reference: a {kit} short-sleeve soccer jersey with a small subtle white emblem on the left chest "
        f"(a clenched fist inside a thin circle, no words, no letters) and matching {kit} track pants with a single white stripe down each side.\n\n"
        f"summary:\n"
        f"[reference generation] static image of sprite sheet, keep the exactly same art style of <Picture 1>.\n\n"
        f"retention_analysis:\n"
        f"<CHARACTER>: fully_preserved — face, hair, beard, skin tone and body build come only from <Picture 1>.\n"
        f"<Picture 2>: partially_preserved — costume design, colors and emblem only; never inherit any donor face or body from <Picture 2>.\n\n"
        f"detailed_description:\n"
        f"The target image is a static image of sprite sheet showing <CHARACTER> from different angles, each element is separated and not "
        f"overlap on each other, on a clean white studio background.\n\n"
        f"[Shot 1] static image.\n\n"
        f"<CHARACTER> on white background, sprite sheet showing <CHARACTER> composition adapted following all possible variants and angles:\n"
        f"1. <CHARACTER> On the left portrait (head and chest) closeup composition on white background.\n"
        f"2. <CHARACTER> In the center full body view from 3 different angles: straight from front, straight from side, straight from back — "
        f"all wearing the complete team kit from <Picture 2>, with the white name {name} centered on the upper back of the jersey and clean "
        f"white football boots.\n"
        f"3. <CHARACTER> On the right 6 round images (same size 2x3 vertical narrow row) with <CHARACTER>'s highlight details: single eye, "
        f"lips, single ear (in circle), hair color, detailed skin texture color, outfit texture color (the {kit} jersey fabric and the small "
        f"white clenched-fist roundel emblem from <Picture 2>).\n\n"
        f"overall_soundscape: N/A\n\n"
        f"non_diegetic_music: N/A"
    )

CHARS = [
    dict(char="jaisal", name="JAISAL", build="slim",
         hair="wavy medium-length black hair", beard="a small patchy short beard",
         kit="royal blue", seed=7,
         face="jaisal_portrait_HD.png", kit_ref="jaisal_kit_ref.png"),
    dict(char="zidane", name="ZIDANE", build="athletic muscular",
         hair="short black hair in a clean halal cut", beard="a full short neatly-trimmed beard",
         kit="dark green", seed=21,
         face="zidane_portrait_HD.png", kit_ref="zidane_kit_ref.png"),
]

j = json.load(open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

DELETE_NODES = {25, 26, 29, 30, 31, 32, 34, 35, 47, 48, 49, 50, 51, 52, 54, 55, 62, 63,  # author refs + scalers
               18, 19, 20, 21, 39, 41}  # LoRA chain + turbo + spectrum
DELETE_LINKS = {64, 65, 66, 70, 71, 72, 75, 76, 98,   # old ref links
                19, 20, 21, 22, 23,                    # LoRA chain
                55, 56, 93}                             # 41->42, 20->39, 39->40
# keep 35 (clip), 36 (vae), 37 (audio vae), 57 (42->7), 94 (40->60), 95 (60->41?)
# NOTE: link 95 = 60 -> 41 slot 0 — 41 is deleted, so 95 must be REWIREd 60->42
assert nodes[28]["type"] == "MiniMaxH3ReferenceToVideo"
assert nodes[7]["type"] == "BasicScheduler" and nodes[64]["type"] == "FizgigH3StillDecode"
assert nodes[10]["type"] == "UNETLoader" and nodes[40]["type"] == "MiniMaxH3SigmaShift"
assert nodes[42]["type"] == "EasyCache" and nodes[60]["type"] == "ModelAttentionBackend"
print("source structure confirmed")

for c in CHARS:
    j2 = json.loads(json.dumps(j))
    nodes2 = {n["id"]: n for n in j2["nodes"]}
    links2 = [l for l in j2["links"] if l[0] not in DELETE_LINKS and l[1] not in DELETE_NODES and l[3] not in DELETE_NODES]
    # remove node 41's target on link 95 (60->41): replace with a NEW link 60->42
    links2 = [l for l in links2 if not (l[1] == 60 and l[3] == 41)]
    new_lid = 200
    links2.append([new_lid, 60, 0, 42, 0, "MODEL"])      # 60 AttentionBackend -> 42 EasyCache
    links2.append([new_lid + 1, 10, 0, 40, 0, "MODEL"])  # 10 UNET -> 40 SigmaShift
    # CRITICAL: the converter reads inputs[].link fields, not just the links array —
    # sync the rewired nodes' model-input link ids to the new links.
    for n in (nodes2[40], nodes2[42]):
        for inp in n["inputs"]:
            if inp["name"] == "model":
                inp["link"] = new_lid if n["id"] == 42 else new_lid + 1
    # H3 node inputs: set slot3/slot4 link fields to the new refs (added below)
    n28 = nodes2[28]
    # new LoadImage nodes (native UI shape)
    n71 = {"id": 71, "type": "LoadImage", "pos": [80, 5740], "size": [282.78, 322], "flags": {},
           "order": 1, "mode": 0,
           "inputs": [
               {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
               {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
           ],
           "outputs": [
               {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [new_lid + 2]},
               {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
           ],
           "properties": {"Node name for S&R": "LoadImage"},
           "widgets_values": [c["face"], "image"]}
    n72 = {"id": 72, "type": "LoadImage", "pos": [420, 5740], "size": [282.78, 322], "flags": {},
           "order": 2, "mode": 0,
           "inputs": [
               {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
               {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
           ],
           "outputs": [
               {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [new_lid + 3]},
               {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
           ],
           "properties": {"Node name for S&R": "LoadImage"},
           "widgets_values": [c["kit_ref"], "image"]}
    links2.append([new_lid + 2, 71, 0, 28, 3, "IMAGE"])  # face -> ref_image_0 (slot 3)
    links2.append([new_lid + 3, 72, 0, 28, 4, "IMAGE"])  # kit  -> ref_image_1 (slot 4)
    # node 28 input slot link fields
    for inp in n28["inputs"]:
        if inp["name"] == "ref_images.ref_image_0":
            inp["link"] = new_lid + 2
        elif inp["name"] == "ref_images.ref_image_1":
            inp["link"] = new_lid + 3
    # widget edits
    n28["widgets_values"] = [wide_prompt(c["char"], c["build"], c["hair"], c["beard"], c["kit"], c["name"]), 4096, 1536, 5, "max"]
    nodes2[2]["widgets_values"] = ["minimax_h3_t1_image_vae_step1597.safetensors"]
    # author's folder-prefixed model names are invalid here — use bare on-disk filenames
    nodes2[11]["widgets_values"] = ["qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "minimax", "default"]
    nodes2[3]["widgets_values"] = ["minimax_h3_audio_vae_fp32.safetensors"]
    nodes2[10]["widgets_values"] = ["minimax_h3_ref2va_pruned_int8_convrot.safetensors", "default"]
    nodes2[7]["widgets_values"] = ["beta", 30, 1]
    nodes2[12]["widgets_values"] = [c["seed"], "fixed"]
    nodes2[68]["widgets_values"] = [f"charsheet/H3WIDE_{c['name']}"]
    if 23 in nodes2:
        nodes2[23]["widgets_values"] = [f"H3 wide 3-view sheet (civitai/cgpixel23 adapt) — {c['char']}: vanilla 30-step, no turbo/spectrum, 4096x1536, t1 image VAE"]
    # remove deleted nodes
    j2["nodes"] = [n for n in j2["nodes"] if n["id"] not in DELETE_NODES]
    j2["nodes"].extend([n71, n72])
    j2["links"] = links2
    j2["last_link_id"] = new_lid + 3
    j2["last_node_id"] = 72

    base = f"05d_charsheet_H3_wide_{c['char']}"
    out_ui = os.path.join(OUT_UI, base + ".json")
    out_prj = os.path.join(OUT_PRJ, base + ".json")
    for out in (out_ui, out_prj):
        json.dump(j2, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"WROTE {out}")
    print(f"  {c['char']}: seed {c['seed']} | {c['kit']} | save charsheet/H3WIDE_{c['name']}")
print("DONE")
