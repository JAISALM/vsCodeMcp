"""Wire RawGirl v3 (iPhone-look LoRA) into krea2_identity_edit.json.

Chain becomes: 55 UNET -> 71 identity LoRA -> 96 RawGirl -> 79 patch -> 53 KSampler.
Also sets up a natural-look test (character ref + candid-photo prompts).
Backs up the original first.
"""
import json, shutil, sys

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json"
BAK = WF + ".rawgirl.bak"

shutil.copy2(WF, BAK)
with open(WF, "r", encoding="utf-8") as f:
    wf = json.load(f)

nodes = wf["nodes"]
links = wf["links"]
by_id = {n["id"]: n for n in nodes}

# --- new node 96: RawGirl LoRA ---
rawgirl = {
    "id": 96,
    "type": "LoraLoaderModelOnly",
    "pos": [60, 660],
    "size": [480, 120],
    "flags": {},
    "order": 26,
    "mode": 0,
    "inputs": [
        {"localized_name": "model", "name": "model", "type": "MODEL", "link": 41},
        {"localized_name": "lora_name", "name": "lora_name", "type": "COMBO", "widget": {"name": "lora_name"}, "link": None},
        {"localized_name": "strength_model", "name": "strength_model", "type": "FLOAT", "widget": {"name": "strength_model"}, "link": None},
    ],
    "outputs": [
        {"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [43]},
    ],
    "properties": {"Node name for S&R": "LoraLoaderModelOnly", "cnr_id": "comfy-core", "ver": "0.26.0"},
    "widgets_values": ["RawGirlV3.safetensors", 1.2],
}
nodes.append(rawgirl)

# --- rewire: link 41 now feeds 96 instead of 79 ---
for l in links:
    if l[0] == 41:
        l[3] = 96  # to node
        l[4] = 0   # to slot (model input)
# --- new link 43: 96 -> 79.0 ---
links.append([43, 96, 0, 79, 0, "MODEL"])

# --- node 79 model input now link 43 ---
for inp in by_id[79]["inputs"]:
    if inp["name"] == "model":
        inp["link"] = 43

# --- test setup: character ref + natural-look prompts ---
by_id[72]["widgets_values"] = ["intro_char_ref_face.png", "image"]

by_id[84]["widgets_values"] = [
    "Candid smartphone photo of the SAME boy from the reference: short dark hair, "
    "rose-pink collared shirt, sitting at a wooden table in a dim room, looking at the camera. "
    "ONLY ONE character, no other people, no duplicates. "
    "Natural unposed look, real skin texture with pores and imperfections, natural lighting from a window, "
    "slight motion blur, deep depth of field, sharp background, no fake bokeh, no editorial polish, "
    "looks like a real photo someone already took.",
    768,
    "",
]
by_id[85]["widgets_values"] = [
    "plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, "
    "stick figure, duplicate character, multiple people, watermark, logo",
    768,
    "",
]
by_id[29]["widgets_values"] = ["rawgirl_test"]

with open(WF, "w", encoding="utf-8") as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("OK: node 96 (RawGirl @1.2) wired 71 -> 96 -> 79; test prompts set; backup at", BAK)
