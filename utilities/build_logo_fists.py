#!/usr/bin/env python
"""Build logo_fists_compare.json — 4 branches:
  H3 ref-based (user's 3-fist ref image): 3-fist emblem + 1-fist roundel
  Qwen 2.1 t2i: same two designs
Square 1024x1024, no text on the emblem (D145).
"""
import json, copy

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
OUT = f"{BASE}\\logo_fists_compare.json"

h3 = json.load(open(f"{BASE}\\05d_charsheet_H3_wide_jaisal.json", encoding="utf-8"))
qw = json.load(open(r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\05b_charsheet_QWEN_jaisal.json", encoding="utf-8"))
qsg = qw["definitions"]["subgraphs"][0]

H3N = {n["id"]: n for n in h3["nodes"]}
QWN = {n["id"]: n for n in qsg["nodes"]}

P_H3_3FIST = """iintegrated_multimodal_description:

subject_definitions:
<EML> a flat vector sports-club emblem: exactly three raised clenched fists side by side, like the resistance/solidarity symbol in <Picture 1> — the middle fist slightly taller and in front, the outer two slightly behind and lower. Each fist: clean white hand with solid red knuckles, each forearm wrapped in horizontal Palestinian flag stripes (green on top, white in the middle, black on the bottom), bold clean white outline around every fist.
<Picture 1> is the style and composition reference for <EML>.

summary:
[reference generation] static image of a single clean flat vector emblem, keep the exactly same flat vector art style of <Picture 1>.

retention_analysis:
<Picture 1>: fully_preserved — fist shapes, flag stripe colors and layout are copied exactly; no redesign.
<EML>: fully_preserved — rendered on a new plain royal blue background, no other elements.

detailed_description:
The target image is a single static image: one flat vector sports-club emblem <EML> centered on a solid plain royal blue background (the same royal blue as a soccer jersey). Three raised clenched fists in a row, middle fist slightly larger and in front, exactly as in <Picture 1>. White fists with solid red knuckles, forearms in green-white-black horizontal flag stripes, bold clean white outlines, crisp sharp edges, flat 2D vector logo style, even lighting, no shading gradients, no drop shadows. NO text, NO letters, NO words, NO numbers anywhere. The emblem fills about 70% of the image, perfectly centered, plenty of plain royal blue space around it.

overall_soundscape: N/A

non_diegetic_music: N/A
"""

P_H3_1FIST = """iintegrated_multimodal_description:

subject_definitions:
<EML> a flat vector sports-club emblem: exactly ONE single raised clenched fist inside a thin white circle (roundel), like the central fist in <Picture 1> — clean white hand with solid red knuckles, the forearm wrapped in horizontal Palestinian flag stripes (green on top, white in the middle, black on the bottom), bold clean white outline, all four fingers and the thumb clearly visible.
<Picture 1> is the style reference for <EML> (the central fist).

summary:
[reference generation] static image of a single clean flat vector emblem, keep the exactly same flat vector art style of <Picture 1>.

retention_analysis:
<Picture 1>: partially_preserved — only the central fist design, flag stripe colors and outline style are copied; the two outer fists are NOT included.
<EML>: fully_preserved — single fist in a thin white circle on a new plain royal blue background.

detailed_description:
The target image is a single static image: one flat vector sports-club emblem <EML> centered on a solid plain royal blue background (the same royal blue as a soccer jersey). Exactly ONE raised clenched fist (the middle one from <Picture 1>) enclosed in a thin white circle (roundel). White fist with solid red knuckles, forearm in green-white-black horizontal flag stripes, bold clean white outline, all four fingers and the thumb clearly visible, crisp sharp edges, flat 2D vector logo style, even lighting, no shading gradients, no drop shadows. Only one fist in the image — no other hands, no duplicates. NO text, NO letters, NO words, NO numbers anywhere. The roundel fills about 70% of the image, perfectly centered, plenty of plain royal blue space around it.

overall_soundscape: N/A

non_diegetic_music: N/A
"""

P_QWEN_3FIST = """Flat vector sports-club emblem logo: exactly three raised clenched fists side by side (solidarity / resistance symbol), the middle fist slightly taller and in front, each fist a clean white hand with solid red knuckles, each forearm wrapped in horizontal Palestinian flag stripes (green on top, white in the middle, black on the bottom), bold clean white outline around every fist, perfectly centered on a solid plain royal blue background, flat 2D vector logo style, crisp sharp edges, even lighting, no gradients, no shadows, no text, no letters, no words, no numbers"""

P_QWEN_1FIST = """Flat vector sports-club emblem logo: one single raised clenched fist enclosed in a thin white circle (roundel), the fist a clean white hand with solid red knuckles, the forearm wrapped in horizontal Palestinian flag stripes (green on top, white in the middle, black on the bottom), bold clean white outline, all four fingers and the thumb clearly visible, perfectly centered on a solid plain royal blue background, flat 2D vector logo style, crisp sharp edges, even lighting, no gradients, no shadows, only one fist, no text, no letters, no words, no numbers"""

P_NEG = """text, letters, words, numbers, watermark, photograph, photorealistic, 3D render, gradient background, drop shadow, blurry, duplicate hands, extra fingers, missing fingers, deformed fist, extra fists, background clutter"""

def deep(src):
    return copy.deepcopy(src)

def set_links(node, in_links, out_links):
    for i, inp in enumerate(node["inputs"]):
        inp["link"] = in_links[i] if i < len(in_links) else None
    for o, out in enumerate(node["outputs"]):
        out["links"] = [l for l in out_links[o]] if o < len(out_links) else None

def build():
    nodes = []
    links = []
    LID = [0]
    def link(src_id, src_slot, dst_id, dst_slot, typ):
        LID[0] += 1
        links.append([LID[0], src_id, src_slot, dst_id, dst_slot, typ])
        return LID[0]

    def add(node):
        node["pos"] = node.get("pos", [0, 0])
        nodes.append(node)

    # ---------- shared H3 spine (from 05d) ----------
    n10 = deep(H3N[10]); n22 = deep(H3N[22]); n40 = deep(H3N[40]); n60 = deep(H3N[60])
    n42 = deep(H3N[42]); n11 = deep(H3N[11]); n2 = deep(H3N[2]); n3 = deep(H3N[3])
    n6 = deep(H3N[6]); n7 = deep(H3N[7])
    for n in (n10, n22, n40, n60, n42, n11, n2, n3, n6, n7):
        n["inputs"] = n.get("inputs", [])
        for inp in n["inputs"]:
            inp["link"] = None
        for out in n["outputs"]:
            out["links"] = None
        add(n)
    n10["pos"] = [40, 40];  n22["pos"] = [300, 40];  n40["pos"] = [40, 220]; n60["pos"] = [560, 40]
    n42["pos"] = [820, 40]; n11["pos"] = [40, 400];  n2["pos"] = [40, 560];   n3["pos"] = [40, 680]
    n6["pos"] = [40, 820];  n7["pos"] = [300, 820]
    n7["widgets_values"] = ["beta", 30, 1]

    # ---------- H3 branches ----------
    n902 = deep(H3N[28]); n902["id"] = 902; n902["pos"] = [40, 1000]
    n903 = deep(H3N[28]); n903["id"] = 903; n903["pos"] = [40, 1500]
    for n in (n902, n903):
        for inp in n["inputs"]:
            inp["link"] = None
        n["widgets_values"][0] = None  # set below per branch
    n902["widgets_values"][0] = P_H3_3FIST
    n903["widgets_values"][0] = P_H3_1FIST
    add(n902); add(n903)

    n904 = deep(H3N[9]); n904["id"] = 904; n904["pos"] = [700, 1000]
    n907 = deep(H3N[9]); n907["id"] = 907; n907["pos"] = [700, 1500]
    n909 = deep(H3N[8]); n909["id"] = 909; n909["pos"] = [960, 1000]
    n915 = deep(H3N[8]); n915["id"] = 915; n915["pos"] = [960, 1500]
    n908 = deep(H3N[12]); n908["id"] = 908; n908["pos"] = [960, 820]; n908["widgets_values"] = [42, "fixed"]
    n914 = deep(H3N[12]); n914["id"] = 914; n914["pos"] = [960, 1320]; n914["widgets_values"] = [43, "fixed"]
    n910 = deep(H3N[65]); n910["id"] = 910; n910["pos"] = [700, 1250]
    n916 = deep(H3N[65]); n916["id"] = 916; n916["pos"] = [700, 1750]
    n910["widgets_values"] = [1024, 1024, 1]
    n916["widgets_values"] = [1024, 1024, 1]
    for n in (n904, n907, n909, n915, n908, n914, n910, n916):
        for inp in n["inputs"]:
            inp["link"] = None
        for out in n["outputs"]:
            out["links"] = None
    add(n904); add(n907); add(n909); add(n915); add(n908); add(n914); add(n910); add(n916)

    n917 = deep(H3N[64]); n917["id"] = 917; n917["pos"] = [1220, 1000]
    n918 = deep(H3N[64]); n918["id"] = 918; n918["pos"] = [1220, 1500]
    for n in (n917, n918):
        for inp in n["inputs"]:
            inp["link"] = None
        for out in n["outputs"]:
            out["links"] = None
    add(n917); add(n918)

    n901 = deep(H3N[71]); n901["id"] = 901; n901["pos"] = [40, 760]
    n901["widgets_values"] = ["palestine_fist_ref.jpg", "image"]
    for inp in n901["inputs"]:
        inp["link"] = None
    n901["outputs"][0]["links"] = None
    add(n901)

    n905 = deep(H3N[66]); n905["id"] = 905; n905["pos"] = [240, 1250]; n905["widgets_values"] = [1024, "fixed"]
    n906 = deep(H3N[67]); n906["id"] = 906; n906["pos"] = [240, 1350]; n906["widgets_values"] = [1024, "fixed"]
    for n in (n905, n906):
        for inp in n["inputs"]:
            inp["link"] = None
        for out in n["outputs"]:
            out["links"] = None
    add(n905); add(n906)

    n919 = deep(H3N[68]); n919["id"] = 919; n919["pos"] = [1480, 1000]; n919["widgets_values"] = ["LOGO_FISTS_H3_3fist"]
    n920 = deep(H3N[68]); n920["id"] = 920; n920["pos"] = [1480, 1500]; n920["widgets_values"] = ["LOGO_FISTS_H3_1fist"]
    for n in (n919, n920):
        for inp in n["inputs"]:
            inp["link"] = None
        for out in n["outputs"]:
            out["links"] = None
    add(n919); add(n920)

    # ---------- Qwen 2.1 branches ----------
    n951 = deep(QWN[451]); n951["id"] = 951; n951["pos"] = [40, 2000]
    n952 = deep(QWN[453]); n952["id"] = 952; n952["pos"] = [40, 2150]
    n953 = deep(QWN[454]); n953["id"] = 953; n953["pos"] = [40, 2300]
    n954 = deep(QWN[476]); n954["id"] = 954; n954["pos"] = [300, 2000]
    n955 = deep(QWN[469]); n955["id"] = 955; n955["pos"] = [560, 2000]
    n956 = deep(QWN[557]); n956["id"] = 956; n956["pos"] = [40, 2450]
    n957 = deep(QWN[557]); n957["id"] = 957; n957["pos"] = [40, 2750]
    n956["widgets_values"] = [P_QWEN_3FIST, P_NEG, 1024]
    n957["widgets_values"] = [P_QWEN_1FIST, P_NEG, 1024]
    n958 = deep(QWN[458]); n958["id"] = 958; n958["pos"] = [820, 2450]; n958["widgets_values"] = [42, "fixed", 25, 1, "euler", "simple", 1]
    n960 = deep(QWN[458]); n960["id"] = 960; n960["pos"] = [820, 2750]; n960["widgets_values"] = [43, "fixed", 25, 1, "euler", "simple", 1]
    n959 = deep(QWN[456]); n959["id"] = 959; n959["pos"] = [820, 2300]
    n961 = deep(QWN[456]); n961["id"] = 961; n961["pos"] = [820, 2600]
    n959["widgets_values"] = [1024, 1024, 1]
    n961["widgets_values"] = [1024, 1024, 1]
    n962 = deep(QWN[457]); n962["id"] = 962; n962["pos"] = [1220, 2450]
    n963 = deep(QWN[457]); n963["id"] = 963; n963["pos"] = [1220, 2750]
    for n in (n951, n952, n953, n954, n955, n956, n957, n958, n960, n959, n961, n962, n963):
        for inp in n["inputs"]:
            inp["link"] = None
        for out in n["outputs"]:
            out["links"] = None
    add(n951); add(n952); add(n953); add(n954); add(n955)
    add(n956); add(n957); add(n958); add(n960); add(n959); add(n961); add(n962); add(n963)

    n964 = deep(H3N[68]); n964["id"] = 964; n964["pos"] = [1480, 2450]; n964["widgets_values"] = ["LOGO_FISTS_QWEN_3fist"]
    n965 = deep(H3N[68]); n965["id"] = 965; n965["pos"] = [1480, 2750]; n965["widgets_values"] = ["LOGO_FISTS_QWEN_1fist"]
    for n in (n964, n965):
        for inp in n["inputs"]:
            inp["link"] = None
        for out in n["outputs"]:
            out["links"] = None
    add(n964); add(n965)

    # Note
    note = {"id": 966, "type": "Note", "pos": [40, 0], "size": [400, 200], "flags": {}, "order": 0, "mode": 0,
            "inputs": [], "outputs": [],
            "widgets_values": ["Logo comparison (D145): 3-fist vs 1-fist roundel.\nH3 branches = ref-based on your image (palestine_fist_ref.jpg).\nQwen 2.1 branches = t2i.\nRun once -> 4 candidates in output (LOGO_FISTS_*).\nNo text on the emblem."]}
    add(note)

    # ---------- links ----------
    # spine
    link(10, 0, 22, 0, "MODEL")
    link(22, 0, 60, 0, "MODEL")
    link(40, 0, 60, 0, "MODEL")  # 40's model input is fed below; out -> 60
    # wait: 40 in <- 10. Fix order:
    # (handled below by explicit link() calls; remove the wrong one)
    links.pop()
    link(10, 0, 40, 0, "MODEL")
    link(60, 0, 42, 0, "MODEL")
    link(42, 0, 7, 0, "MODEL")
    link(42, 0, 904, 0, "MODEL")
    link(42, 0, 907, 0, "MODEL")
    link(11, 0, 902, 0, "CLIP")
    link(11, 0, 903, 0, "CLIP")
    link(2, 0, 902, 1, "VAE")
    link(3, 0, 902, 2, "VAE")
    link(2, 0, 903, 1, "VAE")
    link(3, 0, 903, 2, "VAE")
    link(901, 0, 902, 3, "IMAGE")
    link(901, 0, 903, 3, "IMAGE")
    link(902, 0, 904, 1, "CONDITIONING")
    link(903, 0, 907, 1, "CONDITIONING")
    link(908, 0, 909, 0, "NOISE")
    link(904, 0, 909, 1, "GUIDER")
    link(6, 0, 909, 2, "SAMPLER")
    link(7, 0, 909, 3, "SIGMAS")
    link(910, 0, 909, 4, "LATENT")
    link(905, 0, 902, 9, "INT")
    link(906, 0, 902, 10, "INT")
    link(905, 0, 903, 9, "INT")
    link(906, 0, 903, 10, "INT")
    link(905, 0, 910, 0, "INT")
    link(906, 0, 910, 1, "INT")
    link(905, 0, 916, 0, "INT")
    link(906, 0, 916, 1, "INT")
    link(914, 0, 915, 0, "NOISE")
    link(907, 0, 915, 1, "GUIDER")
    link(6, 0, 915, 2, "SAMPLER")
    link(7, 0, 915, 3, "SIGMAS")
    link(916, 0, 915, 4, "LATENT")
    link(909, 0, 917, 0, "LATENT")
    link(2, 0, 917, 1, "VAE")
    link(915, 0, 918, 0, "LATENT")
    link(2, 0, 918, 1, "VAE")
    link(917, 0, 919, 0, "IMAGE")
    link(918, 0, 920, 0, "IMAGE")
    # qwen
    link(951, 0, 954, 0, "MODEL")
    link(954, 0, 955, 0, "MODEL")
    link(955, 0, 958, 0, "MODEL")
    link(955, 0, 960, 0, "MODEL")
    link(952, 0, 956, 0, "CLIP")
    link(953, 0, 956, 3, "VAE")
    link(952, 0, 957, 0, "CLIP")
    link(953, 0, 957, 3, "VAE")
    link(956, 0, 958, 1, "CONDITIONING")
    link(956, 1, 958, 2, "CONDITIONING")
    link(959, 0, 958, 3, "LATENT")
    link(957, 0, 960, 1, "CONDITIONING")
    link(957, 1, 960, 2, "CONDITIONING")
    link(961, 0, 960, 3, "LATENT")
    link(958, 0, 962, 0, "LATENT")
    link(953, 0, 962, 1, "VAE")
    link(960, 0, 963, 0, "LATENT")
    link(953, 0, 963, 1, "VAE")
    link(962, 0, 964, 0, "IMAGE")
    link(963, 0, 965, 0, "IMAGE")

    # sync node input/output link caches from the links array (UI cache)
    byid = {n["id"]: n for n in nodes}
    for l in links:
        _, src, src_slot, dst, dst_slot, _t = l
        snode, dnode = byid[src], byid[dst]
        dnode["inputs"][dst_slot]["link"] = l[0]
        if snode["outputs"][src_slot]["links"] is None:
            snode["outputs"][src_slot]["links"] = []
        snode["outputs"][src_slot]["links"].append(l[0])

    j = {"last_node_id": 966, "last_link_id": LID[0], "id": "logo-fists-compare",
         "revision": 0, "version": 0.4, "wall": {}, "nodes": nodes, "links": links,
         "config": {}, "options": {}, "flags": {}, "extra": {}}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(j, f, indent=4, ensure_ascii=False)
    print("wrote", OUT, "nodes:", len(nodes), "links:", len(links))

build()
