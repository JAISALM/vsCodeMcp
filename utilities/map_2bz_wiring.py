#!/usr/bin/env python
"""Map the wiring around the optional 2BZ reference nodes (list-form links)."""
import json

j = json.load(open(r"E:\minimax_workflow\character_sheet\2BZ_H3_character_sheet_2stage_v1_EN.json", encoding="utf-8", errors="ignore"))
nodes = {n["id"]: n for n in j["nodes"]}

print(f"total links: {len(j['links'])}")
print()
for l in j["links"]:
    lid, o_id, o_slot, t_id, t_slot, ltype = l[0], l[1], l[2], l[3], l[4], l[5]
    if o_id in (16, 21, 22, 57, 58, 59, 77, 78, 79) or t_id in (16, 21, 22, 57, 58, 59, 77, 78, 79):
        tgt = nodes[t_id]
        tname = tgt["inputs"][t_slot]["name"] if t_slot < len(tgt["inputs"]) else "?"
        print(f"link {lid}: {o_id} ({nodes[o_id]['type']}) out-slot {o_slot} -> {t_id} ({tgt['type']}) in-slot {t_slot} [{tname}]")
