"""Diagnose the MiniMax H3 Reference to Video link-type errors in G_revolt.

UI reports:
  - ref_images.ref_image_2        incompatible
  - ref_video_audios.ref_video_audio_0  incompatible

Dump the MiniMax node's inputs (name/type/link) + trace every link's source
node type + output, so we can see EXACTLY what is wired to the two bad slots
and what type it actually is.
"""
import json, os

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json"
d = json.load(open(P, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}
links = d.get("links", [])

# link id -> (from_node, from_slot, to_node, to_slot)
link_map = {}
for l in links:
    # ComfyUI UI link format: [id, from_node, from_slot, to_node, to_slot, type?, ...]
    lid, fn, fs, tn, ts = l[0], l[1], l[2], l[3], l[4]
    link_map[lid] = (fn, fs, tn, ts)

# find the MiniMax node
mm = None
for nid, n in nodes.items():
    if "MiniMax" in n["type"] and "Video" in n["type"]:
        mm = n
        break
print("MiniMax node id:", mm["id"], "type:", mm["type"])
print("=" * 80)
print("INPUTS (name / type / link_id / source_node_type):")
for inp in mm.get("inputs", []):
    name = inp.get("name")
    itype = inp.get("type")
    lid = inp.get("link")
    src_type = "?"
    if lid is not None and lid in link_map:
        fn, fs, tn, ts = link_map[lid]
        src_type = nodes[fn]["type"] if fn in nodes else "?"
    flag = ""
    if name in ("ref_image_2", "ref_video_audio_0"):
        flag = "   <<< REPORTED BAD"
    print(f"  {name:24s} type={itype:10s} link={lid}  src={src_type}{flag}")

print("=" * 80)
print("ALL LINKS touching the MiniMax node:")
for l in links:
    lid, fn, fs, tn, ts = l[0], l[1], l[2], l[3], l[4]
    if fn == mm["id"] or tn == mm["id"]:
        ftype = nodes[fn]["type"] if fn in nodes else "?"
        ttype = nodes[tn]["type"] if tn in nodes else "?"
        print(f"  link {lid}: {fn}({ftype}) s{fs} -> {tn}({ttype}) s{ts}")
