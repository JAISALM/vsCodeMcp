#!/usr/bin/env python
import json, os
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\09j_QWEN21_JAISAL_sheet.json"
j = json.load(open(p, encoding="utf-8"))
ids = {n["id"] for n in j["nodes"]}
print("=== 09j LINKS (all) ===")
for l in j["links"]:
    d = " DANGLING-SRC" if l[1] not in ids else ""
    d += " DANGLING-DST" if l[3] not in ids else ""
    print(l, d)
print("=== SUBGRAPH 478 FULL ROLE ===")
for sg in j["definitions"]["subgraphs"]:
    for n in sg["nodes"]:
        if n["id"] == 478:
            print(n["widgets_values"][0])
print("=== subgraph internal links (trace 954/969/974/977/986) ===")
# internal link ids live in the subgraph's own links array
for i, sg in enumerate(j["definitions"]["subgraphs"]):
    sids = {n["id"] for n in sg["nodes"]}
    for l in sg.get("links", []):
        if l[0] in (954, 969, 974, 977, 986, 961, 981, 985) or l[3] in (954, 969, 974, 977, 986, 961):
            print(f"sg{i}:", l)
