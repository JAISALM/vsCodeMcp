# -*- coding: utf-8 -*-
"""
Fix the 10 Jaisal Kut intro shot workflows (2026-09-14).

Fixes (per user feedback):
  1. Resolution: ResolutionSelector megapixels 2 -> 1  (1 MP is what works;
     2 MP is why shot A took 2.3 min for 12%). The R2V node's width/height are
     LINKED from this selector, so this is the real resolution control.
  2. Stray reference: remove any LoadImage whose image is NOT in the keyframes
     folder (the template's leftover `jaisal_4_middle.png`), plus its link and
     the R2V ref slot it fed. All intro refs must come from ONE place:
     D:\\models\\vsCodeMcp\\Jaisal-intro\\keyframes.
  3. Prompt bug: dedupe the accidental `<Subject 1> is <Subject 1> is` ->
     `<Subject 1> is`.

SLA is already correctly wired (LoRA -> H3SLAAttention -> BasicGuider ->
Sampler) and enabled; no change needed there.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "D:\\models\\vsCodeMcp\\utilities\\fix_intro_workflows.py"
"""
import json, os, glob

WFDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
KFDIR = r"D:\models\vsCodeMcp\Jaisal-intro\keyframes"
valid = set(f for f in os.listdir(KFDIR) if f.lower().endswith((".png", ".jpg", ".jpeg")))

files = sorted(glob.glob(os.path.join(WFDIR, "jaisal_intro_*.json")))
print(f"Keyframes folder ({len(valid)} files):")
for f in sorted(valid):
    print("   ", f)
print()

for fp in files:
    with open(fp, encoding="utf-8") as fh:
        d = json.load(fh)
    name = os.path.basename(fp)
    changes = []
    nodes_by_id = {n["id"]: n for n in d["nodes"]}

    # 1. Resolution megapixels -> 1
    for n in d["nodes"]:
        if n["type"] == "ResolutionSelector":
            wv = n.get("widgets_values")
            if wv and len(wv) >= 2 and wv[1] != 1:
                changes.append(f"RES megapixels {wv[1]} -> 1")
                wv[1] = 1

    # 2. Remove stray LoadImage nodes (image not in keyframes folder)
    stray = [n["id"] for n in d["nodes"]
             if n["type"] == "LoadImage"
             and n.get("widgets_values", [""])[0] not in valid]
    for sid in stray:
        fname = nodes_by_id[sid].get("widgets_values", [""])[0]
        # clear the target ref slot(s) this node fed
        for l in [l for l in d["links"] if l[1] == sid]:
            tid, lid = l[3], l[0]
            if tid in nodes_by_id:
                for inp in nodes_by_id[tid].get("inputs", []):
                    if inp.get("link") == lid:
                        inp["link"] = None
        d["links"] = [l for l in d["links"] if l[1] != sid]
        d["nodes"] = [n for n in d["nodes"] if n["id"] != sid]
        changes.append(f"removed stray ref node {sid} ({fname})")

    # 3. Fix prompt duplication
    for n in d["nodes"]:
        if n["type"] == "PrimitiveStringMultiline":
            p = n.get("widgets_values", [""])[0]
            if "<Subject 1> is <Subject 1> is" in p:
                n["widgets_values"][0] = p.replace("<Subject 1> is <Subject 1> is", "<Subject 1> is")
                changes.append("fixed prompt dup <Subject 1>")

    with open(fp, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False)

    print(f"==== {name} ====")
    for c in changes:
        print("   ", c)
    if not changes:
        print("    (no changes)")
    # final ref list for verification
    refs = [n.get("widgets_values", [""])[0] for n in d["nodes"] if n["type"] == "LoadImage"]
    print("    refs now:", refs)
    print()

print("Done.")
