#!/usr/bin/env python
"""Build the Krea 2 '1 Click Dataset' workflow (UI format).

Strategy: load the TESTED krea2_identity_edit.json (known-good slot orders,
widget values, links) and transform it:
  1. Add a PixaromaPromptEach node holding 20 scene prompts (rows state).
  2. Wire its `prompt` output -> positive Krea2EditGroundedEncode.prompt.
  3. Clear the positive encode's prompt widget value (now link-driven).
  4. Point SaveImage prefix at krea2_ds.
  5. Save as krea2_1click_dataset.json.

One Run -> the executor re-runs the downstream chain once per prompt
(OUTPUT_IS_LIST) -> 20 images, same memory as one image.

LoRA chain (2026-10-08): UNET -> identity v1.2 (71) -> Krea2-realism-V2
(node 96 @1.0) -> FameGrid Spice iPhone look (node 97 @0.7) -> Krea2Edit
ModelPatch (79). Character = 26yo Kerala man, lean-but-fit, NOT well
groomed; set CHARACTER = "full" or "short" to match the master reference.
"""
import json

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json"
OUT = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_1click_dataset.json"

REF_IMAGE = "krea2_test_ref.png"
SAVE_PREFIX = "krea2_ds"

# Two characters (user 2026-10-08): both lean-but-fit (NOT bulky), both NOT
# well groomed, Kerala topical look. Set CHARACTER to match the master
# reference image you picked from the t2i run.
CHARACTER = "full"  # "full" or "short"
CHAR_FULL = ("the SAME man from the reference: 26-year-old Indian man from "
             "Kerala, short dark hair, a FULL unkempt beard (patchy, uneven, "
             "not well groomed), lean and fit build (NOT bulky, NOT "
             "muscular), plain dark t-shirt")
CHAR_SHORT = ("the SAME man from the reference: 26-year-old Indian man from "
              "Kerala, short dark hair, a SHORT patchy beard (short length, "
              "sparse, not well groomed, not a full beard), lean and fit "
              "build (NOT bulky, NOT muscular), plain dark t-shirt")
CHAR = CHAR_FULL if CHARACTER == "full" else CHAR_SHORT
REALISM = ("ONLY ONE character, no other people, no duplicates. Natural unposed "
           "look, real skin texture with pores and imperfections, natural "
           "lighting, slight motion blur, deep depth of field, sharp background, "
           "no fake bokeh, no editorial polish, looks like a real photo someone "
           "already took.")

SCENES = [
    "A frontal headshot of {c}, neutral expression, head tilted slightly to the right. Close-up, 85mm lens f/2.8, sharp focus on the eyes. Soft overcast daylight, plain muted background. {r}",
    "{c} walking down a wet city street in the afternoon, head turned slightly toward the camera, candid expression. Medium shot, 35mm f/4.0, urban background. Natural overcast light. {r}",
    "A wide shot of {c} standing on the stone bridge over the river, looking directly at the camera. Full-body, 50mm f/8.0, head to toe. Moody overcast light, open river behind. {r}",
    "{c} standing in a dark alleyway, head in sharp profile toward a light source. Medium shot, 35mm f/1.8, high-contrast moody atmosphere, dim ambient light. {r}",
    "{c} standing in a dimly lit indoor corridor, head angled three-quarters away from the camera. Full-body, 24mm, natural light streaks from a high window, deep shadows. {r}",
    "A true profile view of {c}, chin tilted slightly upward. Close-up, 105mm telephoto, compressed background. Soft golden-hour light from behind. {r}",
    "{c} sitting on a simple wooden stool, head tilted slightly downward, eyes looking up at the camera. Medium shot, 85mm f/4.0, soft even light, neutral grey background. {r}",
    "{c} standing on a rooftop at dusk, body facing away, head turned back over the shoulder toward the camera. Half-body, 35mm f/2.0, moody sky. {r}",
    "{c} riding a train, head bowed slightly as if in thought. Medium shot, 50mm f/2.8, soft window light, blurred interior. {r}",
    "{c} standing in a foggy forest at dusk, head tilted back looking up into a beam of light. Medium shot, 50mm f/1.4, a single bright shaft through the mist. {r}",
    "A close-up of {c} in a messy artist's studio, head tilted slightly to the left, curious expression. Close-up, 85mm prime f/2.8, warm practical light. {r}",
    "{c} sitting on a concrete ramp at a sun-bleached skatepark, head turned away from the sun toward the horizon. Medium shot, 35mm f/4.0, bright daylight. {r}",
    "A wide shot of {c} standing with arms crossed against a plain wall, looking directly at the camera with a slight chin tuck. Full-body, 50mm f/8.0, even soft light. {r}",
    "A low-angle shot looking up at {c}, head tilted down toward the lens with a confident gaze. Medium shot, 24mm wide-angle, overcast sky behind. {r}",
    "{c} walking through a lush green park, head turned in a three-quarter view as if looking at something in the distance. Full-body, 35mm f/4.0, dappled daylight. {r}",
    "{c} face illuminated solely by the glow of a computer screen in a pitch-black room, head angled slightly upward. Blue light reflects off the face. Close-up, 85mm f/2.0. {r}",
    "{c} standing in a cozy, cluttered record store, viewed from a profile angle as they look at a shelf. Medium shot, 35mm f/2.0, warm ambient light. {r}",
    "{c} standing under a single flickering street lamp in the rain, head bowed slightly so the face is partially in shadow. Half-body, 50mm f/2.8, wet pavement reflections. {r}",
    "{c} standing on a wooden beach pier during sunset, head tilted back slightly with eyes closed, enjoying the breeze. Medium shot, 85mm f/2.8, warm low sun. {r}",
    "A relaxed, three-quarter view of {c} standing against a plain muted background, head turned slightly off-camera. Medium shot, 50mm f/4.0, soft even light. {r}",
]
PROMPTS = [s.format(c=CHAR, r=REALISM) for s in SCENES]
assert len(PROMPTS) == 20, len(PROMPTS)

with open(SRC, encoding="utf-8") as f:
    wf = json.load(f)

nodes = wf["nodes"]
by_id = {n["id"]: n for n in nodes}

load_image = by_id[72]   # reference image
pos_encode = by_id[84]   # positive grounded encode (prompt widget)
save_image = by_id[29]   # SaveImage

# --- 1. set reference image + save prefix ---
load_image["widgets_values"][0] = REF_IMAGE
save_image["widgets_values"][0] = SAVE_PREFIX

# --- 1b. swap the RawGirlV3 LoRA (node 96) for Krea2-realism-V2 ---
# RawGirlV3 is a FEMALE LoRA - wrong for a male character.
by_id[96]["widgets_values"][0] = "Krea2-realism-V2.safetensors"
by_id[96]["widgets_values"][1] = 1.0

# --- 1c. insert the iPhone-look LoRA (node 97) between 96 and 79 ---
# Source chain: 71 -> 96 (link 43) -> 79. Reroute link 43 to node 97 and
# add a new link 97 -> 79.
import copy
iphone = copy.deepcopy(by_id[96])
iphone["id"] = 97
iphone["pos"] = [by_id[96]["pos"][0], by_id[96]["pos"][1] + 120]
for inp in iphone["inputs"]:
    if inp["name"] == "model":
        inp["link"] = 43
    else:
        inp["link"] = None
lora_link_id = max([l[0] for l in wf["links"]] + [0]) + 1
iphone["outputs"][0]["links"] = [lora_link_id]
iphone["widgets_values"] = ["famegrid_spicy_3167060.safetensors", 0.7]
nodes.append(iphone)
by_id[97] = iphone
for l in wf["links"]:
    if l[0] == 43:
        l[3] = 97  # 96.0 -> 97.0
wf["links"].append([lora_link_id, 97, 0, 79, 0, "MODEL"])
# node 79's model input must point at the NEW link (97 -> 79)
for inp in by_id[79]["inputs"]:
    if inp["name"] == "model":
        inp["link"] = lora_link_id

# --- 2. add the PixaromaPromptEach node ---
new_id = 200
while new_id in by_id:
    new_id += 1
max_link = max([l[0] for l in wf["links"]] + [0])
new_link = max_link + 1

rows = [{"text": p, "enabled": True} for p in PROMPTS]
state = {
    "version": 2,
    "rows": rows,
    "split": "line",
    "expand": True,
    "trim": True,
    "skipEmpty": True,
    "cap": 200,
    "wiredAt": "after",
}

pix_node = {
    "id": new_id,
    "type": "PixaromaPromptEach",
    "pos": [400, 460],
    "size": [420, 320],
    "flags": {},
    "order": 99,
    "mode": 0,
    "inputs": [
        {"localized_name": "text", "name": "text", "type": "STRING", "link": None},
    ],
    "outputs": [
        {"localized_name": "prompt", "name": "prompt", "type": "STRING", "links": [new_link]},
        {"localized_name": "index", "name": "index", "type": "INT", "links": None},
        {"localized_name": "total", "name": "total", "type": "INT", "links": None},
    ],
    "properties": {"Node name for S&R": "PixaromaPromptEach", "promptEachState": state},
    "widgets_values": [],
}
nodes.append(pix_node)
by_id[new_id] = pix_node

# --- 3. wire pix_node.prompt (output 0) -> pos_encode.prompt (input index 3) ---
prompt_idx = None
for i, inp in enumerate(pos_encode["inputs"]):
    if inp.get("name") == "prompt":
        prompt_idx = i
        break
assert prompt_idx is not None, "prompt input not found on positive encode"
pos_encode["inputs"][prompt_idx]["link"] = new_link
# widgets_values order = [prompt, grounding_px, system_prompt]; prompt now link-driven
pos_encode["widgets_values"][0] = ""

# --- 4. add the link: [id, from_node, from_slot, to_node, to_slot, type] ---
wf["links"].append([new_link, new_id, 0, pos_encode["id"], prompt_idx, "STRING"])

# --- 5. bump last_link_id / last_node_id ---
wf["last_link_id"] = max(wf.get("last_link_id", 0), new_link)
wf["last_node_id"] = max(wf.get("last_node_id", 0), new_id)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("written:", OUT)
print("pixaroma node id:", new_id, "| link id:", new_link)
print("wired to positive encode node", pos_encode["id"], "input", prompt_idx)
print("reference image:", REF_IMAGE, "| save prefix:", SAVE_PREFIX)
print("prompts:", len(PROMPTS))
