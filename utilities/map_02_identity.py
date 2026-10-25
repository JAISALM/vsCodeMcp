#!/usr/bin/env python
"""Map 02_identity_refset.json nodes (Krea2 identity-edit base)."""
import json

j = json.load(open(r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json", encoding="utf-8"))
for n in j["nodes"]:
    w = n.get("widgets_values") or []
    ws = " | ".join(str(x)[:90] for x in w[:8])
    print(f'id={n["id"]:>4} {n["type"]:<30} [{ws}]')
print()
for l in j["links"]:
    print(l)
