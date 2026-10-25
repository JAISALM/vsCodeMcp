"""Package the 3 public Story-Short workflows from the private source workflows.

Surgery:
  01_character_sheet.json  <- krea2_t2i_character.json
      - remove PixaromaPromptEach (node 200) + its link into the positive text
      - remove famegrid_spicy LoRA (node 97) and rewire UNET chain: 96 -> 53
      - set generic character prompt on positive CLIPTextEncode (node 300)
      - SaveImage prefix -> story_short/character_sheet
  02_identity_refset.json  <- krea2_identity_edit.json
      - remove Typnosis (95, already orphaned) + RawGirlV3 (96) LoRAs
      - rewire: 71 (identity-edit) -> 79 (patch)
      - generic reference image names + generic instruction
      - SaveImage prefix -> story_short/identity_ref
  03_h3_r2v_2ref.json      <- beach_sprint_test.json
      - generic reference image names + generic 3-anchor R2V prompt
      - SaveVideo prefix -> story_short/shot

Writes UI-format JSON to challenge/story-short/workflows/.
"""
import json, os, copy

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
OUT = r"D:\models\vsCodeMcp\challenge\story-short\workflows"
os.makedirs(OUT, exist_ok=True)

def load(name):
    with open(os.path.join(WF, name), "r", encoding="utf-8") as f:
        return json.load(f)

def save(j, name):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(j, f, ensure_ascii=False)
    print("wrote", path)

def nodes(j):
    return {n["id"]: n for n in j["nodes"]}

def remove_nodes(j, ids):
    N = nodes(j)
    keep_links = []
    for L in j["links"]:
        a = list(L)
        if a[1] in ids or a[3] in ids:
            # clear link refs on the surviving endpoint
            tgt = N.get(a[3])
            if tgt:
                for inp in tgt.get("inputs", []):
                    if inp.get("link") == a[0]:
                        inp["link"] = None
            src = N.get(a[1])
            if src:
                for out in src.get("outputs", []):
                    out["links"] = [x for x in (out.get("links") or []) if x != a[0]]
        else:
            keep_links.append(L)
    j["links"] = keep_links
    j["nodes"] = [n for n in j["nodes"] if n["id"] not in ids]
    print(f"  removed nodes {sorted(ids)}, {len(keep_links)} links kept")

def set_widget(node, idx, value):
    node["widgets_values"][idx] = value
    # keep named map in sync if present
    if "widgets_values_named" in node:
        # widget order is positional; for single-widget nodes the key is the widget name
        pass

def add_link(j, link_id, src_id, src_slot, dst_id, dst_slot, ltype):
    j["links"].append([link_id, src_id, src_slot, dst_id, dst_slot, ltype])
    N = nodes(j)
    N[dst_id]["inputs"] = [i for i in N[dst_id]["inputs"]]  # noop
    for inp in N[dst_id]["inputs"]:
        if inp.get("link") is None or True:
            pass
    # set the dst input's link by name
    dst = N[dst_id]
    src = N[src_id]
    # find dst input at the given slot by matching the slot index
    # (UI format: inputs list order == slot order)
    dst["inputs"][dst_slot]["link"] = link_id
    # update src output links
    if src_slot < len(src.get("outputs", [])):
        out = src["outputs"][src_slot]
        out["links"] = [link_id] if out.get("links") in (None, []) else out["links"] + [link_id]

# ---------------------------------------------------------------- 01
print("== 01 character sheet ==")
j = load("krea2_t2i_character.json")
N = nodes(j)
remove_nodes(j, [200, 97])
N = nodes(j)
# positive prompt (node 300): text widget is slot 0
N[300]["widgets_values"][0] = (
    "Character sheet of a young man, round face, wavy medium hair, full beard, "
    "wearing a dark t-shirt, standing on a misty backwater path, natural skin "
    "texture, realistic fabric, cinematic photograph, soft overcast light, "
    "ONLY ONE character, no other people, no duplicates"
)
# the text input of 300 was linked from Pixaroma (link 11, now gone) — ensure widget drives it
for inp in N[300]["inputs"]:
    if inp.get("name") == "text" and inp.get("widget"):
        inp["link"] = None
add_link(j, 20, 96, 0, 53, 0, "MODEL")
N = nodes(j)
N[29]["widgets_values"][0] = "story_short/character_sheet"
# KSampler seed: keep randomize
save(j, "01_character_sheet.json")

# ---------------------------------------------------------------- 02
print("== 02 identity refset ==")
j = load("krea2_identity_edit.json")
N = nodes(j)
remove_nodes(j, [95, 96])
N = nodes(j)
N[72]["widgets_values"][0] = "ref_character.png"
N[113]["widgets_values"][0] = "ref_person.png"
N[84]["widgets_values"][0] = (
    "Candid smartphone photo of the SAME person from the reference: young man "
    "with wavy medium hair, full beard, dark t-shirt, standing on a stone "
    "bridge over a calm river, moody overcast light, looking at the camera. "
    "ONLY ONE character, no other people, no duplicates. Natural unposed look, "
    "real skin texture with pores and imperfections, natural overcast lighting, "
    "slight motion blur, deep depth of field, looks like a real photo someone "
    "already took."
)
# rewrite the files-note (100) for the public chain
note100 = (
    "Files needed:\n"
    "- krea2_turbo_fp8_scaled.safetensors (UNET, node 55)\n"
    "- qwen3vl_4b_fp8_scaled.safetensors (CLIP, type 'krea2', node 56)\n"
    "- qwen_image_vae.safetensors (VAE, node 57)\n"
    "- krea2_identity_edit_v1_2.safetensors (identity LoRA, node 71, released with this repo)\n"
    "See MODELS.md for download links."
)
N[100]["widgets_values"][0] = note100
N[29]["widgets_values"][0] = "story_short/identity_ref"
add_link(j, 20, 71, 0, 79, 0, "MODEL")
save(j, "02_identity_refset.json")

# ---------------------------------------------------------------- 03
print("== 03 H3 R2V 3-anchor ==")
j = load("beach_sprint_test.json")
N = nodes(j)
N[137]["widgets_values"][0] = "ref_shot1.png"
N[139]["widgets_values"][0] = "ref_shot2.png"
N[148]["widgets_values"][0] = "ref_shot3.png"
N[138]["widgets_values"][0] = (
    "subject_definitions: <Picture 1> is the young man with wavy medium hair, "
    "full beard and a dark t-shirt. His face, hair and clothing come ENTIRELY "
    "from the reference images - do not alter his appearance in any way.\n\n"
    "summary: [reference generation] A continuous 10-second shot: the man "
    "stands on a misty backwater path, then walks away along the path as the "
    "camera pulls back.\n\n"
    "detailed_description: "
    "[Shot 1] <Picture 1> - medium shot at eye level, the man stands still "
    "looking at the water, slow push-in, misty overcast light, water lapping, "
    "his quiet breathing.\n"
    "[Shot 2] <Picture 2> - wide shot, the man walks away along the path from "
    "left to right, static camera, grey light, footsteps on wet gravel.\n\n"
    "overall_soundscape: natural ambient only - wind through palms, distant "
    "water lapping, footsteps on gravel. No other sounds.\n\n"
    "non_diegetic_music: NO music, NO instrumental music, NO musical "
    "instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song. "
    "Natural ambient sounds only."
)
N[92]["widgets_values"][0] = "story_short/shot"
save(j, "03_h3_r2v_2ref.json")
print("done.")
