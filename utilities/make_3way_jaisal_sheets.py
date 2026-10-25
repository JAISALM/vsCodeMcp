#!/usr/bin/env python
"""Build the two remaining Jaisal sheet workflows (READY, not run):

1. 08j_KREA2_JAISAL_sheet.json — Krea2 Identity Edit v1.2 (02 base) with Jaisal's HD face
   assigned as the identity reference (node 72), optional 2nd ref (113) REMOVED, kit carried
   in the instruction text (new crest spec: fist roundel, no text). 16:9 2MP, ref_boost 2.5,
   10 steps euler/simple cfg 1. SaveImage -> charsheet/KREA2_JAISAL_ID.

2. 09j_QWEN21_JAISAL_sheet.json — the user's `Qwen Image 2.1 Character Design Sheet.json`
   (LLM-architect: ThinkingLLM PE-I2I GGUF writes the sheet prompt at runtime) with:
   - 470 LoadImage -> jaisal_portrait_HD.png (Jaisal's face ref for the PE-LLM + Qwen anchor)
   - 481 PrimitiveString -> JAISAL (the {{name}} the LLM substitutes)
   - 461 SaveImageAdvanced prefix -> charsheet/QWEN21_JAISAL
   - subgraph internal 451 UNET -> qwen_image_2.1_bf16.safetensors (on disk)
   - subgraph internal 453 CLIP -> qwen3vl_8b_int8_convrot.safetensors (on disk)
   - everything else UNTOUCHED (485 nvidia_rtx_vsr verified valid; 549 PE-I2I GGUF model
     downloading to ComfyUI\\LLM\\GGUF\\; 13 ResolutionSelector 3:2 3.4MP; 459 25 steps).
   NOTE: requires the ComfyUI-ThinkingLLM pack LOADED (server restart pending) and the
   PE-I2I GGUF + mmproj files in ComfyUI\\LLM\\GGUF\\ (download in progress).
"""
import json, os, copy

OUT_UI = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
OUT_PRJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"

# ---------------------------------------------------------------- 1. Krea2
j = json.load(open(r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json", encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
assert nodes[72]["type"] == "LoadImage" and nodes[113]["type"] == "LoadImage"
assert nodes[84]["type"] == "Krea2EditGroundedEncode" and nodes[85]["type"] == "Krea2EditGroundedEncode"

nodes[72]["widgets_values"] = ["jaisal_portrait_HD.png", "image"]
nodes[84]["widgets_values"] = [
    "kr2realism, a full-body character turnaround sheet of the same man from the reference image, "
    "wearing a royal blue short-sleeve soccer jersey with a small subtle white emblem on the left chest "
    "(a clenched fist inside a thin circle, no words, no letters), matching royal blue track pants with a "
    "single white stripe down each side, clean white football boots, and the white name JAISAL in the "
    "center of the jersey back. Exactly three equal full-body photographs arranged side by side, left to "
    "right, on a neutral light-grey studio background: front view relaxed A-pose, strict 90-degree "
    "right-side profile, back view. Same scale and identical ground line in all three views. The face "
    "stays exactly the same man in every view. Even studio lighting, photoreal, sharp detail.",
    768, "",
]
nodes[85]["widgets_values"] = [
    "stick figure, duplicate character, multiple people, watermark, logo, words, letters, text, slogan, "
    "changed face, different person, helmet, mask, cropped head, cropped feet, extra panel, action pose",
    768, "",
]
nodes[29]["widgets_values"] = ["charsheet/KREA2_JAISAL_ID"]
if 100 in nodes:
    nodes[100]["widgets_values"] = [
        "08j KREA2 JAISAL SHEET (identity-edit v1.2, Jaisal's image assigned):\n"
        "- node 72 = YOUR IMAGE = jaisal_portrait_HD.png (identity source)\n"
        "- node 84 = instruction (kr2realism + team kit + 3-view sheet, new crest spec: fist roundel, no text)\n"
        "- node 85 = identity-safety + no-text negative\n"
        "- node 79 = ref_boost 2.5 (D142) · node 53 = 10 steps euler/simple cfg 1\n"
        "- node 83 = 16:9 2MP\n- node 29 -> charsheet/KREA2_JAISAL_ID\n"
        "- 2nd ref node 113 REMOVED (kit is in the instruction text)"
    ]
# remove optional 2nd ref (113) + its 4 links
del nodes[113]
j["nodes"] = [n for n in j["nodes"] if n["id"] != 113]
DROP_LINKS = {34, 35, 36, 37}
j["links"] = [l for l in j["links"] if l[0] not in DROP_LINKS]
base = "08j_KREA2_JAISAL_sheet"
json.dump(j, open(os.path.join(OUT_UI, base + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(j, open(os.path.join(OUT_PRJ, base + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"WROTE {base}.json (UI + project copy)")

# ---------------------------------------------------------------- 2. Qwen
j2 = json.load(open(r"E:\minimax_workflow\character_sheet\Qwen Image 2.1 Character Design Sheet.json", encoding="utf-8"))
nodes2 = {n["id"]: n for n in j2["nodes"]}
assert nodes2[470]["type"] == "LoadImage" and nodes2[481]["type"] == "PrimitiveString"
assert nodes2[461]["type"] == "SaveImageAdvanced"
nodes2[470]["widgets_values"] = ["jaisal_portrait_HD.png", "image"]
nodes2[481]["widgets_values"] = ["JAISAL"]
nodes2[461]["widgets_values"] = ["charsheet/QWEN21_JAISAL", "png", "8-bit", "sRGB"]
# subgraph internals (converter reads internal nodes — D019 rule)
subs = j2["definitions"]["subgraphs"]
for sg in subs:
    for n in sg.get("nodes", []):
        if n["id"] == 451:  # UNETLoader
            n["widgets_values"] = ["qwen_image_2.1_bf16.safetensors", "default"]
        elif n["id"] == 453:  # CLIPLoader
            n["widgets_values"] = ["qwen3vl_8b_int8_convrot.safetensors", "qwen_image", "default"]
base = "09j_QWEN21_JAISAL_sheet"
json.dump(j2, open(os.path.join(OUT_UI, base + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(j2, open(os.path.join(OUT_PRJ, base + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"WROTE {base}.json (UI + project copy)")
print("NOTE 09j: needs ThinkingLLM pack loaded (server restart) + PE-I2I GGUF in ComfyUI\\LLM\\GGUF\\ (downloading)")
