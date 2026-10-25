"""Final fix: wire engine in-port + seed ports to real (emitted) sources.
- 2729 (1488.in): source 1490 -> 1457 slot 0 (timeline-selected settings bundle)
- 2717 (1359.in): source 1478 -> 1457 slot 0
- 2730 (1488.noise_seed): source 1491 -> 765 slot 0 (SeedNode)
- 2726 (1359.noise_seed): source 1480 -> 765 slot 0
"""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
links = {list(L)[0]: L for L in j["links"]}

def repoint(lid, new_src, new_slot):
    L = links[lid]
    old_src = L[1]
    # remove lid from old source's output links
    for out in nodes[old_src].get("outputs", []):
        if out.get("links"):
            out["links"] = [x for x in out["links"] if x != lid]
    L[1], L[2] = new_src, new_slot
    # add lid to new source's output links
    for out in nodes[new_src].get("outputs", []):
        out["links"] = (out.get("links") or []) + [lid]
    print(f"link {lid}: {old_src} -> {new_src} slot {new_slot}")

repoint(2729, 1457, 0)
repoint(2717, 1457, 0)
repoint(2730, 765, 0)
repoint(2726, 765, 0)

json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved")
