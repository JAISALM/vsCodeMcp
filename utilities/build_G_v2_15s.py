"""Build G v2 (15s, 5 refs):
- node 136 length 264 -> 360 (15s @ 24fps)
- add 3 LoadImage nodes (165/166/167) for the object refs
- wire links 318/319/320 -> node 136 ref_image_2/3/4
- update node 138 prompt to shot_G_papers_v2_15s.txt
Native LoadImage shape (from krea2_jaisal_title_moody.json node 31):
  inputs: image (COMBO) + upload (IMAGEUPLOAD), outputs: IMAGE + MASK
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_papers.json"
PROMPT = r"d:\models\vsCodeMcp\Jaisal-intro\prompts\shot_G_papers_v2_15s.txt"

with open(WF, "r", encoding="utf-8") as f:
    wf = json.load(f)

def find(nid):
    for n in wf["nodes"]:
        if n["id"] == nid:
            return n
    raise KeyError(nid)

# 1. length 264 -> 360
n136 = find(136)
n136["widgets_values"][3] = 360
print(f"length -> 360 (15s)")

# 2. add 3 LoadImage nodes for object refs
# (node_id, filename, pos, link_id, to_slot) — to_slot = input ARRAY INDEX in node 136
# node 136 inputs: [0]=clip [1]=vae [2]=audio_vae [3]=ref_image_0 [4]=ref_image_1
#                  [5]=ref_image_2 [6]=ref_image_3 [7]=ref_image_4 [8]=ref_image_5
new_nodes = [
    (165, "obj_cricket_bat_00002_.png", [-2421.33, 4200.0], 318, 5),
    (166, "obj_soccer_ball_00002_.png", [-2090.0, 4200.0], 319, 6),
    (167, "obj_paper_smiley_00002_.png", [-1760.0, 4200.0], 320, 7),
]
# input NAME suffix for each slot (names are ref_image_2/3/4, slots are 5/6/7)
name_suffix = {5: 2, 6: 3, 7: 4}
for nid, fname, pos, link_id, slot in new_nodes:
    node = {
        "id": nid,
        "type": "LoadImage",
        "pos": pos,
        "size": [290, 330],
        "flags": {},
        "order": 10,
        "mode": 0,
        "inputs": [
            {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
            {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [link_id]},
            {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
        ],
        "properties": {"Node name for S&R": "LoadImage"},
        "widgets_values": [fname, "image"],
    }
    wf["nodes"].append(node)
    # link: [id, from_node, from_slot, to_node, to_slot, type]
    wf["links"].append([link_id, nid, 0, 136, slot, "IMAGE"])
    # set the input link field on node 136 (input NAME uses the suffix, not the slot)
    for inp in n136["inputs"]:
        if inp["name"] == f"ref_images.ref_image_{name_suffix[slot]}":
            inp["link"] = link_id
    print(f"added node {nid} ({fname}) -> link {link_id} -> 136 slot {slot} (ref_image_{name_suffix[slot]})")

# 3. update prompt
n138 = find(138)
with open(PROMPT, "r", encoding="utf-8") as f:
    n138["widgets_values"] = [f.read().strip()]
print(f"prompt updated ({len(n138['widgets_values'][0])} chars)")

with open(WF, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=1)
print("G v2 saved")
