"""Verify the to_slot convention on a WORKING MiniMax sibling workflow, then compare to G_revolt.

Hypothesis: in a correct workflow, each link's to_slot == the input's array index,
and the input's `link` field == that link's id. G_revolt has 2 stale to_slot values
(link 300 -> slot 0=clip, link 320 -> slot 7=ref_video_0) that break the UI.
"""
import json, os, glob

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

def dump_mm(path):
    d = json.load(open(path, encoding="utf-8"))
    mm = None
    for n in d["nodes"]:
        if n["type"] == "MiniMaxH3ReferenceToVideo":
            mm = n
            break
    if mm is None:
        return None
    links = {l[0]: l for l in d.get("links", [])}
    print(f"\n### {os.path.basename(path)}  (MiniMax node {mm['id']})")
    for i, inp in enumerate(mm.get("inputs", [])):
        lid = inp.get("link")
        if lid is not None and lid in links:
            l = links[lid]
            to_slot = l[4]
            match = "OK " if to_slot == i else "BAD"
            print(f"  [{i:2d}] {inp.get('name'):34s} link={lid} to_slot={to_slot} {match}")
    return mm

# G_revolt + any sibling G workflows
candidates = [
    "jaisal_intro_G_revolt.json",
    "jaisal_intro_G_papers.json",
    "jaisal_intro_G1_burst.json",
    "jaisal_intro_G2_aftermath.json",
]
for c in candidates:
    p = os.path.join(WF_DIR, c)
    if os.path.exists(p):
        dump_mm(p)
    else:
        print(f"\n### {c}  (NOT FOUND)")
