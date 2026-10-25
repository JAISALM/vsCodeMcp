#!/usr/bin/env python
"""Dump everything needed to wire the crest ref + kit spec into the 4 Jaisal sheet workflows."""
import json, os

PRJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"
WFS = ["05d_charsheet_H3_wide_jaisal.json", "05e_charsheet_H3_fizgig_jaisal.json",
       "08j_KREA2_JAISAL_sheet.json", "09j_QWEN21_JAISAL_sheet.json"]

def show(name):
    p = os.path.join(PRJ, name)
    j = json.load(open(p, encoding="utf-8"))
    print("=" * 90)
    print(name, "| last_node_id:", j.get("last_node_id"), "last_link_id:", j.get("last_link_id"))
    for n in j["nodes"]:
        w = n.get("widgets_values")
        ws = str(w)[:250] if w is not None else None
        print(f"--- {n['id']} {n['type']} widgets={ws}")
        for i, inp in enumerate(n.get("inputs", [])):
            if inp.get("link") is not None or inp.get("type") in ("IMAGE", "MODEL", "CONDITIONING", "LATENT", "STRING"):
                print(f"    in[{i}] {inp.get('name')} ({inp.get('type')}) link={inp.get('link')}")
        for o, out in enumerate(n.get("outputs", [])):
            if out.get("links"):
                print(f"    out[{o}] {out.get('name')} -> {out.get('links')}")
    for sg in (j.get("definitions", {}).get("subgraphs") or []):
        print("### SUBGRAPH nodes:")
        for n in sg.get("nodes", []):
            w = n.get("widgets_values")
            ws = str(w)[:400] if w is not None else None
            print(f"  --- {n['id']} {n['type']} widgets={ws}")
            for i, inp in enumerate(n.get("inputs", [])):
                if inp.get("link") is not None:
                    print(f"      in[{i}] {inp.get('name')} link={inp.get('link')}")
            for o, out in enumerate(n.get("outputs", [])):
                if out.get("links"):
                    print(f"      out[{o}] {out.get('name')} -> {out.get('links')}")

for wf in WFS:
    show(wf)
print("=" * 90)
print("DONE")
