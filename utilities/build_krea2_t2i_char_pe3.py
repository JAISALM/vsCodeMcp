# build_krea2_t2i_char_pe3.py
#
# Builds the 3-image CHARACTER DATASET PE workflows:
#   krea2_t2i_char1_pe3.json  (3 branches = rows 1-3 of the original 6)
#   krea2_t2i_char2_pe3.json
#
# Goal (user 2026-10-08): the single-prompt PE workflow (D110) produced a good
# image but ONE per character; we need 3 images per character to build the
# character dataset. TextGenerate is single-prompt, so = 3 PE BRANCHES:
#
#   branch A (row 1, the approved "looking back" backwater shot):
#     TG 310 -> CLIPTE 300 -> KSampler 53 -> VAEDecode 54 -> FameGridColorFinish 302 -> SaveImage 29
#   branch B (row 2, houseboat):
#     TG 311 -> CLIPTE 313 -> KSampler 314 -> VAEDecode 315 -> FameGridColorFinish 316 -> SaveImage 317
#   branch C (row 3, monsoon rain):
#     TG 312 -> CLIPTE 318 -> KSampler 319 -> VAEDecode 320 -> FameGridColorFinish 321 -> SaveImage 322
#
# Shared: UNET 55, CLIPLoader 56, VAELoader 57, LoRA 96 (Krea2-realism-V2 @1.0)
# -> 97 (famegrid_spicy @0.7), latent 82 (1152x2048), negative CLIPTE 301.
# KSampler seeds: 42/43/44 (control_after_generate "randomize" = fine variance).
# PE seed: 42 in all three branches (dramatic knob, per-branch editable).
# SaveImage prefixes: krea2_charN_face_a / _b / _c (dataset-friendly naming).
#
# Node shapes cloned from the char originals (CLIPTE/KSampler/VAEDecode/
# FameGridColorFinish/SaveImage) + the proven on-mode TextGenerate shape from
# krea2_t2i_char1_pe.json (13-slot expanded widgets_values).
#
# Run:
#   & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\build_krea2_t2i_char_pe3.py"

import copy
import json
import os

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

PE_MAX_LENGTH = 1024
PE_SUBS = [0.7, 64, 0.95, 0.05, 1.05, 0.0]  # temperature, top_k, top_p, min_p, repetition_penalty, presence_penalty
PE_SEED = 42
PE_THINKING = False
PE_USE_DEFAULT_TEMPLATE = True
PE_MTP = "off"

# (tg_id, clipt_id, ks_id, vaed_id, cfgf_id, si_id, ks_seed, prefix_suffix, row_idx, pos_offsets)
# row_idx = index into the original 6-row prompt set (0-based)
BRANCHES = [
    dict(tg=310, clipt=300, ks=53,  vaed=54,  cfgf=302, si=29,  seed=42, suffix="a", row=0,
         pos=dict(tg=[400, 470], clipt=[760, 220], ks=[1120, 40], vaed=[1480, 40], cfgf=[1480, 140], si=[1700, 40])),
    dict(tg=311, clipt=313, ks=314, vaed=315, cfgf=316, si=317, seed=43, suffix="b", row=1,
         pos=dict(tg=[400, 720], clipt=[760, 560], ks=[1120, 380], vaed=[1480, 380], cfgf=[1480, 520], si=[1700, 380])),
    dict(tg=312, clipt=318, ks=319, vaed=320, cfgf=321, si=322, seed=44, suffix="c", row=2,
         pos=dict(tg=[400, 970], clipt=[760, 900], ks=[1120, 720], vaed=[1480, 720], cfgf=[1480, 860], si=[1700, 720])),
]

# link ids per branch: [tg_clip, tg_text, ks_model, ks_pos, ks_neg, ks_lat, vaed_lat, vaed_vae, cfgf_img, si_img, clipt_clip]
LINKS = [
    [14, 15, 5, 6, 7, 8, 9, 4, 10, 13, 2],   # branch A = the original single-branch links
    [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 36],
    [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37],
]


def build(char):
    src = os.path.join(WF_DIR, f"krea2_t2i_char{char}.json")
    pe = os.path.join(WF_DIR, f"krea2_t2i_char{char}_pe.json")
    dst = os.path.join(WF_DIR, f"krea2_t2i_char{char}_pe3.json")

    with open(src, encoding="utf-8") as f:
        wf = json.load(f)
    with open(pe, encoding="utf-8") as f:
        pe_wf = json.load(f)

    by_id = {n["id"]: n for n in wf["nodes"]}
    assert by_id[200]["type"] == "PixaromaPromptEach"
    rows = by_id[200]["properties"]["promptEachState"]["rows"]
    assert len(rows) >= 3

    tg_template = next(n for n in pe_wf["nodes"] if n["type"] == "TextGenerate")
    templates = {k: by_id[i] for k, i in dict(clipt=300, ks=53, vaed=54, cfgf=302, si=29).items()}

    # --- remove the 6-row loop node + its link ---
    wf["nodes"].remove(by_id[200])
    wf["links"] = [l for l in wf["links"] if l[0] != 11]
    by_id = {n["id"]: n for n in wf["nodes"]}

    # --- branch A reuses the original nodes (300/53/54/302/29); only rewire 300.text ---
    for inp in by_id[300]["inputs"]:
        if inp["name"] == "text":
            inp["link"] = LINKS[0][1]
    by_id[29]["widgets_values"] = [f"krea2_char{char}_face_a"]

    # --- add the three TextGenerate nodes ---
    titles = ["PE a — row1 backwater (looking back)", "PE b — row2 houseboat", "PE c — row3 monsoon rain"]
    for bi, b in enumerate(BRANCHES):
        if b["tg"] == 310:  # branch A
            tg = copy.deepcopy(tg_template)
            tg["id"] = 310
        else:
            tg = copy.deepcopy(tg_template)
            tg["id"] = b["tg"]
        tg["pos"] = b["pos"]["tg"]
        tg["title"] = titles[bi]
        # clip link = this branch's tg_clip link
        for inp in tg["inputs"]:
            if inp["name"] == "clip":
                inp["link"] = LINKS[bi][0]
        # generated_text output -> this branch's text link
        tg["outputs"] = [
            {"localized_name": "generated_text", "name": "generated_text", "type": "STRING", "links": [LINKS[bi][1]]},
            {"localized_name": "thinking", "name": "thinking", "type": "STRING", "links": None},
        ]
        prompt = rows[b["row"]]["text"]
        # slot order: prompt, max_length, "on", temperature, top_k, top_p, min_p,
        # repetition_penalty, SEED, PRESENCE_PENALTY, thinking, use_default_template, mtp
        tg["widgets_values"] = [prompt, PE_MAX_LENGTH, "on", 0.7, 64, 0.95, 0.05, 1.05,
                                PE_SEED, 0.0, PE_THINKING, PE_USE_DEFAULT_TEMPLATE, PE_MTP]
        if "widgets_values_named" in tg:
            tg["widgets_values_named"]["prompt"] = prompt
        wf["nodes"].append(tg)

    # --- branches B and C: clone the other 5 node types ---
    for bi in (1, 2):
        b = BRANCHES[bi]
        L = LINKS[bi]

        clipt = copy.deepcopy(templates["clipt"])
        clipt["id"] = b["clipt"]
        clipt["pos"] = b["pos"]["clipt"]
        clipt["inputs"] = [
            {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": L[10]},
            {"localized_name": "text", "name": "text", "type": "STRING", "widget": {"name": "text"}, "link": L[1]},
        ]
        clipt["outputs"] = [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [L[3]]}]
        wf["nodes"].append(clipt)

        ks = copy.deepcopy(templates["ks"])
        ks["id"] = b["ks"]
        ks["pos"] = b["pos"]["ks"]
        ks["widgets_values"] = [b["seed"], "randomize", 10, 1, "euler", "simple", 1]
        ks["inputs"] = [
            {"localized_name": "model", "name": "model", "type": "MODEL", "link": L[2]},
            {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "link": L[3]},
            {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "link": L[4]},
            {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT", "link": L[5]},
        ]
        ks["outputs"] = [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [L[6]]}]
        wf["nodes"].append(ks)

        vaed = copy.deepcopy(templates["vaed"])
        vaed["id"] = b["vaed"]
        vaed["pos"] = b["pos"]["vaed"]
        vaed["inputs"] = [
            {"localized_name": "samples", "name": "samples", "type": "LATENT", "link": L[6]},
            {"localized_name": "vae", "name": "vae", "type": "VAE", "link": L[7]},
        ]
        vaed["outputs"] = [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [L[8]]}]
        wf["nodes"].append(vaed)

        cfgf = copy.deepcopy(templates["cfgf"])
        cfgf["id"] = b["cfgf"]
        cfgf["pos"] = b["pos"]["cfgf"]
        cfgf["inputs"] = [{"localized_name": "image", "name": "image", "type": "IMAGE", "link": L[8]}]
        cfgf["outputs"] = [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [L[9]]}]
        wf["nodes"].append(cfgf)

        si = copy.deepcopy(templates["si"])
        si["id"] = b["si"]
        si["pos"] = b["pos"]["si"]
        si["inputs"] = [{"localized_name": "images", "name": "images", "type": "IMAGE", "link": L[9]}]
        si["widgets_values"] = [f"krea2_char{char}_face_{b['suffix']}"]
        si["outputs"] = []
        wf["nodes"].append(si)

    # --- shared-node output link lists ---
    by_id = {n["id"]: n for n in wf["nodes"]}
    by_id[56]["outputs"][0]["links"] = [2, 3, 14, 16, 26, 36, 37]
    by_id[57]["outputs"][0]["links"] = [4, 23, 33]
    by_id[82]["outputs"][0]["links"] = [8, 21, 31]
    by_id[97]["outputs"][0]["links"] = [5, 18, 28]
    by_id[301]["outputs"][0]["links"] = [7, 20, 30]

    # --- new links ---
    for bi in (1, 2):
        b = BRANCHES[bi]
        L = LINKS[bi]
        wf["links"].append([L[0], 56, 0, b["tg"], 0, "CLIP"])
        wf["links"].append([L[1], b["tg"], 0, b["clipt"], 1, "STRING"])
        wf["links"].append([L[2], 97, 0, b["ks"], 0, "MODEL"])
        wf["links"].append([L[3], b["clipt"], 0, b["ks"], 1, "CONDITIONING"])
        wf["links"].append([L[4], 301, 0, b["ks"], 2, "CONDITIONING"])
        wf["links"].append([L[5], 82, 0, b["ks"], 3, "LATENT"])
        wf["links"].append([L[6], b["ks"], 0, b["vaed"], 0, "LATENT"])
        wf["links"].append([L[7], 57, 0, b["vaed"], 1, "VAE"])
        wf["links"].append([L[8], b["vaed"], 0, b["cfgf"], 0, "IMAGE"])
        wf["links"].append([L[9], b["cfgf"], 0, b["si"], 0, "IMAGE"])
    wf["links"].append([14, 56, 0, 310, 0, "CLIP"])
    wf["links"].append([15, 310, 0, 300, 1, "STRING"])
    wf["links"].append([36, 56, 0, 313, 0, "CLIP"])
    wf["links"].append([37, 56, 0, 318, 0, "CLIP"])

    # --- order + metadata ---
    order_map = {55: 0, 56: 1, 57: 2, 96: 3, 97: 4, 82: 5, 301: 12,
                 310: 6, 311: 7, 312: 8, 300: 9, 313: 10, 318: 11,
                 53: 13, 314: 14, 319: 15, 54: 16, 315: 17, 320: 18,
                 302: 19, 316: 20, 321: 21, 29: 22, 317: 23, 322: 24}
    for n in wf["nodes"]:
        n["order"] = order_map[n["id"]]

    wf["id"] = f"krea2_t2i_char{char}_pe3"
    wf["last_node_id"] = 322
    wf["last_link_id"] = 37

    with open(dst, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)
    print(f"built {dst}: nodes={len(wf['nodes'])} links={len(wf['links'])}")
    print(f"  prefixes: krea2_char{char}_face_a (row1 backwater), _b (row2 houseboat), _c (row3 rain)")


build(1)
build(2)
print("done")
