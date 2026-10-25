"""Fix all Set/Get ordering holes in the timeline workflow:
- 1374: in-link 2542 origin 1373(SetNode) -> 752 slot 0
- 1379: drop link 3002; add 3003 [752,0 -> 1379,0]
- 1390: add 3004 [761,0 -> 1390,0]
- 1392: add 3005 [1383,0 -> 1392,0]
- 1436: add 3006 [1526,0 -> 1436,0]
- 1629: add 3007 [1449,0 -> 1629,0]
- 1630: add 3008 [1449,0 -> 1630,0]
Also: check 1082 LoadVideo mode + file existence; find h3_upscale_options setter.
"""
import json, os

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
links = {list(L)[0]: L for L in j["links"]}
used_ids = {list(L)[0] for L in j["links"]}

def add_link(lid, src, src_slot, dst, dst_slot, ltype):
    assert lid not in used_ids, f"link id {lid} already used"
    j["links"].append([lid, src, src_slot, dst, dst_slot, ltype])
    used_ids.add(lid)
    # source outputs array
    for out in nodes[src].get("outputs", []):
        out["links"] = (out.get("links") or []) + [lid]
    # target input slot
    tgt = nodes[dst]
    if not tgt.get("inputs"):
        tgt["inputs"] = []
    if dst_slot < len(tgt["inputs"]):
        tgt["inputs"][dst_slot]["link"] = lid
    else:
        tgt["inputs"].append({"localized_name": "in", "name": "in", "type": ltype, "link": lid})

def set_in_link(nid, lid, ltype="OBVPM_BUNDLE"):
    tgt = nodes[nid]
    if not tgt.get("inputs"):
        tgt["inputs"] = [{"localized_name": "in", "name": "in", "type": ltype, "link": None}]
    for i in tgt["inputs"]:
        if i.get("name") == "in":
            i["link"] = lid
            return
    tgt["inputs"].append({"localized_name": "in", "name": "in", "type": ltype, "link": lid})

# 1. 1374: re-point link 2542 origin 1373 -> 752 slot 0
L = links[2542]
L[1], L[2] = 752, 0
# remove 2542 from 1373's output links
nodes[1373]["outputs"][0]["links"] = [x for x in (nodes[1373]["outputs"][0].get("links") or []) if x != 2542]
print("1374 in-link 2542 now <- 752 slot 0")

# 2. 1379: drop 3002 (to SetNode 1373), add 3003 from 752
if 3002 in links:
    L3002 = links[3002]
    nodes[1373]["outputs"][0]["links"] = [x for x in (nodes[1373]["outputs"][0].get("links") or []) if x != 3002]
    j["links"] = [x for x in j["links"] if list(x)[0] != 3002]
    used_ids.discard(3002)
    del links[3002]
add_link(3003, 752, 0, 1379, 0, "OBVPM_BUNDLE")
print("1379 in-link = 3003 <- 752 slot 0")

# 3. 1390 <- 761 slot 0
add_link(3004, 761, 0, 1390, 0, "OBVPM_BUNDLE")
print("1390 in-link = 3004 <- 761 slot 0")

# 4. 1392 <- 1383 slot 0
add_link(3005, 1383, 0, 1392, 0, "OBVPM_BUNDLE")
print("1392 in-link = 3005 <- 1383 slot 0")

# 5. 1436 <- 1526 slot 0
add_link(3006, 1526, 0, 1436, 0, "OBVPM_BUNDLE")
print("1436 in-link = 3006 <- 1526 slot 0")

# 6/7. 1629/1630 <- 1449 slot 0
add_link(3007, 1449, 0, 1629, 0, "OBVPM_BUNDLE")
add_link(3008, 1449, 0, 1630, 0, "OBVPM_BUNDLE")
print("1629 in-link = 3007, 1630 in-link = 3008 <- 1449 slot 0")

# 8. 1082 LoadVideo: check mode + file
n1082 = nodes.get(1082)
print(f"1082 LoadVideo mode={n1082.get('mode')} w={n1082.get('widgets_values')}")
inp = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
for f in ("clip_00027.mp4", "audio_00001.flac"):
    print(f"  input/{f}: {os.path.exists(os.path.join(inp, f))}")

# 9. find h3_upscale_options setter (canvas + subgraphs)
def find_setter(nodes_list, where):
    for n in nodes_list:
        w = n.get("widgets_values") or []
        for v in w:
            if isinstance(v, str) and "h3_upscale_options" in v:
                print(f"  {where} node {n['id']} [{n['type']}]: {str(w)[:100]}")
                return
find_setter(j["nodes"], "canvas")
for s in j.get("definitions", {}).get("subgraphs", []):
    find_setter(s.get("nodes", []), "subgraph")

json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved")
