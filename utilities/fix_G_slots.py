"""Fix stale to_slot values on the MiniMax node's input links in G_revolt.

Root cause: the links array to_slot values are stale (from an older node-pack
input order). The input `link` fields are CORRECT (server uses them). Re-align
each link's to_slot to the input's array index so the UI stops showing false
type-incompatibility errors.

ONLY changes to_slot (index 4) on links connected to node 136's inputs.
Does NOT touch: link ids, from_node, from_slot, the input `link` fields,
the prompt/dialogue wiring (link 279), or the audio inputs.
"""
import json, os, shutil

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json"
BAK = P + ".preslots.bak"

d = json.load(open(P, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}
mm = [n for n in d["nodes"] if n["type"] == "MiniMaxH3ReferenceToVideo"][0]
mm_id = mm["id"]

# link id -> index in links array
link_idx = {l[0]: i for i, l in enumerate(d["links"])}

changes = []
# For each input with a link, ensure that link's to_slot == input index
for i, inp in enumerate(mm.get("inputs", [])):
    lid = inp.get("link")
    if lid is None:
        continue
    if lid not in link_idx:
        print(f"  WARN: input[{i}] {inp.get('name')} link {lid} not in links array")
        continue
    li = link_idx[lid]
    cur_to_slot = d["links"][li][4]
    if cur_to_slot != i:
        d["links"][li][4] = i
        changes.append((lid, inp.get("name"), cur_to_slot, i))

# backup then save
shutil.copy(P, BAK)
json.dump(d, open(P, "w", encoding="utf-8"), indent=1)

print(f"BACKUP -> {os.path.basename(BAK)}")
print(f"CHANGES ({len(changes)}):")
for lid, name, old, new in changes:
    print(f"  link {lid} ({name}): to_slot {old} -> {new}")
print("Saved.")
