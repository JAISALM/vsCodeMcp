# -*- coding: utf-8 -*-
"""
Build jaisal_intro_A_walkin_v2.json = shot A + the character sheet
(Image_00001_.png) added as a 3rd reference (identity anchor).

Reference order (connection order -> <Picture N>):
  ref_image_0 = table empty.png            -> <Picture 1> (first frame)
  ref_image_1 = jaisal_hand_under_the_table.png -> <Picture 2> (last frame)
  ref_image_2 = Image_00001_.png (character sheet) -> <Picture 3> (identity anchor)

The prompt is updated so <Picture 3> is the CHARACTER SHEET identity anchor
(face, hair, build). Everything else identical to shot A, so the only variable
is the added character-sheet reference.
"""
import json, os, copy

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin_v2.json"
CHAR_SHEET = "Image_00001_.png"

d = json.load(open(SRC, encoding="utf-8"))
nodes = d["nodes"]
nodes_by_id = {n["id"]: n for n in nodes}

# --- Find the R2V node ---
r2v = next(n for n in nodes if n["type"] == "MiniMaxH3ReferenceToVideo")
r2v_id = r2v["id"]
print("R2V node id:", r2v_id)

# --- Find the ref_image_2 input and confirm it's free ---
ref2 = next(i for i in r2v["inputs"] if i["name"] == "ref_images.ref_image_2")
print("ref_image_2 current link:", ref2.get("link"))
assert ref2.get("link") is None, "ref_image_2 already wired - abort"

# --- Pick free node id + link id ---
max_node_id = max(n["id"] for n in nodes)
new_node_id = max_node_id + 1
max_link_id = max([l[0] for l in d["links"]] + [d.get("last_link_id", 0)])
new_link_id = max_link_id + 1
print("new node id:", new_node_id, "new link id:", new_link_id)

# --- Create the character-sheet LoadImage node (clone an existing LoadImage shape) ---
li_template = next(n for n in nodes if n["type"] == "LoadImage")
new_li = copy.deepcopy(li_template)
new_li["id"] = new_node_id
new_li["widgets_values"] = [CHAR_SHEET, "image"]
new_li["pos"] = [li_template["pos"][0], li_template["pos"][1] + 400]
# outputs: IMAGE (will carry the new link), MASK (none)
new_li["outputs"] = [
    {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [new_link_id]},
    {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
]
nodes.append(new_li)
print("added LoadImage node", new_node_id, "for", CHAR_SHEET)

# --- Wire it to ref_image_2 (to_slot = 2, the ref_image number) ---
d["links"].append([new_link_id, new_node_id, 0, r2v_id, 2, "IMAGE"])
ref2["link"] = new_link_id
d["last_link_id"] = new_link_id
print("wired link", new_link_id, "-> ref_image_2")

# --- Update the prompt: add <Picture 3> = character sheet identity anchor ---
for n in nodes:
    if n["type"] == "PrimitiveStringMultiline":
        p = n["widgets_values"][0]
        # Insert the <Picture 3> line right after the <Picture 2> line.
        lines = p.split("\n")
        out = []
        inserted = False
        for line in lines:
            out.append(line)
            if not inserted and line.startswith("<Picture 2>"):
                out.append("<Picture 3> is the CHARACTER SHEET (identity anchor) - the young boy's face, hair and build. Use it to lock the character's identity exactly; do NOT change his face, hair or build.")
                inserted = True
        # Also add a retention line for <Picture 3>.
        if inserted and "<Picture 3> (identity anchor)" not in "\n".join(out):
            text = "\n".join(out)
            anchor = "<Picture 3> (identity anchor): fully_preserved - the character's face, hair and build are locked to this sheet."
            # insert after the <Picture 2> retention line
            idx = text.find("<Picture 2> (last frame)")
            if idx != -1:
                end = text.find("\n", idx)
                if end != -1:
                    text = text[:end] + "\n" + anchor + text[end:]
            n["widgets_values"][0] = text
        print("prompt updated with <Picture 3> identity anchor")
        break

# --- Change the SaveVideo prefix so the output is distinguishable ---
for n in nodes:
    if n["type"] == "SaveVideo":
        n["widgets_values"][0] = "jaisal_intro_A_walkin_v2"
        print("SaveVideo prefix ->", n["widgets_values"][0])

json.dump(d, open(DST, "w", encoding="utf-8"), ensure_ascii=False)
print("\nwrote", DST)
