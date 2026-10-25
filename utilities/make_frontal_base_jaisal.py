#!/usr/bin/env python
"""REBUILD 10a_frontal_base_jaisal.json (v2 — replaces the OOM'd identity-edit version).

v1 (identity-edit, 16MP) OOM'd: krea2edit's _ref_attn_bias allocates an N^2 attention
bias matrix (target+refs sequence ~136k tokens -> 72.92 GiB). AND the user correctly
objected that identity-edit (i2i) loses quality — it is a LOCKING tool, not a face-
creation tool.

v2 = FRESH T2I, the proven approved-face recipe (krea2_t2i_char1_pe3.json):
  - UNET Krea2Realism_V1 -> LoRA Krea2-realism-V2 @1.0 -> LoRA famegrid_spicy @0.7
  - CLIP qwen3vl_4b_fp8_scaled (krea2 type), VAE qwen_image_vae
  - 3 parallel branches, KSampler seeds 42/43/44 (control_after_generate randomize)
    -> 3 candidates in ONE queue press
  - latent 82 = [896, 1120, 1] (1MP 4:5 — the exact proven face latent; the approved
    faces were generated here then 4x-upscaled via 03_hd_upscale.json)
  - author's full character prefix verbatim + FRONTAL clause (dead-center, both eyes
    fully open/symmetric, no side angle) + author's face-focus clause + author's tail
  - author's proven negative verbatim (anti-studio/candid look + bad-eyes terms)
No TextGenerate/PE node (Qwen llama-server is stopped) — the full prompt goes straight
into CLIPTextEncode.

After picking the best candidate: run it through 03_hd_upscale.json (proven 4x) ->
new jaisal_portrait_HD.png (keep the old 3/4 as jaisal_portrait_HD_34view.png).
"""
import json

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1_pe3.json"
OUT_UI = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\10a_frontal_base_jaisal.json"
OUT_PRJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\10a_frontal_base_jaisal.json"

CHAR_PREFIX = (
    "A candid phone snapshot of a 26-year-old young Malayali man from Kerala, India, South Indian "
    "facial features, warm medium-brown natural skin, a young MAN (male only), with a ROUND youthful "
    "face, softer rounded features and a masculine jaw, MEDIUM-LENGTH WAVY dark hair worn DOWN and "
    "loose around his neck and ears (wavy, natural, slightly messy, hair is NOT tied up, NOT in a "
    "bun, NOT a topknot, NOT a short haircut), a sparse short BEARD on his chin and jaw (sparse "
    "uneven dark patches you can see on his face, more than stubble, NOT clean-shaven, NOT a dense "
    "full beard), a lean and fit young man, NOT bulky, NOT muscular, wearing a plain dark t-shirt, "
    "his face completely frontal."
)
FRONTAL_CLAUSE = (
    " He is standing alone, facing the camera directly, dead-center, head and shoulders framing, "
    "both eyes fully open and symmetric, looking straight into the lens, calm neutral relaxed "
    "expression, face completely frontal, NO side angle, NO profile, NO three-quarter view. His "
    "wavy hair is down and loose, the sparse beard visible on his chin and jaw. Sharp focus on the "
    "man's face, his face is the main subject, in focus, crisp facial detail, detailed iris and "
    "eye texture."
)
TAIL = (
    " He looks like a real young man in his mid-20s: youthful fresh face, natural young skin, no "
    "wrinkles, no aging, no grey hair. Candid unposed snapshot caught in a real moment, natural "
    "ambient light, looks like a real photo someone took on their phone, slight natural "
    "imperfections, a real ordinary person, ONLY ONE character, no other people, NOT a studio "
    "portrait, NOT a headshot, NOT a stock photo, NOT a professional photo."
)
PROMPT = CHAR_PREFIX + FRONTAL_CLAUSE + TAIL

j = json.load(open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

# --- remove the three TextGenerate nodes + their 6 links ---
tg_ids = {310, 311, 312}
drop_links = {14, 15, 16, 17, 26, 27}
j["nodes"] = [n for n in j["nodes"] if n["id"] not in tg_ids]
j["links"] = [l for l in j["links"] if l[0] not in drop_links]
nodes = {n["id"]: n for n in j["nodes"]}

# 56 (CLIP) output link list: drop the TG clip feeds
clip_out = next(o for o in nodes[56]["outputs"] if o["name"] == "CLIP")
clip_out["links"] = [lk for lk in (clip_out["links"] or []) if lk not in drop_links]

# --- CLIPTE text: widget-driven now (links removed) ---
for nid in (300, 313, 318):
    n = nodes[nid]
    assert n["type"] == "CLIPTextEncode"
    n["widgets_values"] = [PROMPT]
    for inp in n["inputs"]:
        if inp["name"] == "text":
            inp["link"] = None

# --- save prefixes (3 candidates, one queue) ---
nodes[29]["widgets_values"] = ["FACEFRONTAL_JAISAL_a"]
nodes[317]["widgets_values"] = ["FACEFRONTAL_JAISAL_b"]
nodes[322]["widgets_values"] = ["FACEFRONTAL_JAISAL_c"]

# sanity: latent + kSamplers unchanged
assert nodes[82]["widgets_values"] == [896, 1120, 1], nodes[82]["widgets_values"]
assert nodes[53]["widgets_values"][0] == 42 and nodes[314]["widgets_values"][0] == 43 and nodes[319]["widgets_values"][0] == 44

# --- renumber order sequentially ---
for i, n in enumerate(j["nodes"]):
    n["order"] = i

j["id"] = "10a_frontal_base_jaisal"
j["last_node_id"] = max(n["id"] for n in j["nodes"])

for path in (OUT_UI, OUT_PRJ):
    json.dump(j, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE", path)
print("DONE — 10a v2 = fresh t2i, 3 seeds per queue, 896x1120 proven latent")
