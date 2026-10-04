# -*- coding: utf-8 -*-
"""
Fix the 15-second length bug in the 9 R2V intro shot workflows (2026-09-14).

ROOT CAUSE: the R2V node's `length` input is LINKED from a hidden
ComfyMathExpression node (131) fed by a PrimitiveFloat (132) = 15 (seconds).
The math node computes max(5, round(15*24)) = 360 -> 362 frames = 15.1s,
OVERRIDING the widget value. So every shot ran at 15s even though the widget
showed the correct per-shot length (A=124=5.2s, B=73=3s, ...).

FIX: unlink the R2V `length` input (set its `link` to None) so the WIDGET
value (the intended per-shot length, all valid 5+k*17 values) is used directly.
The orphaned math node + primitive float are left in place (harmless).

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "D:\\models\\vsCodeMcp\\utilities\\fix_intro_lengths.py"
"""
import json, os, glob

WFDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
files = sorted(glob.glob(os.path.join(WFDIR, "jaisal_intro_*.json")))

for fp in files:
    with open(fp, encoding="utf-8") as fh:
        d = json.load(fh)
    name = os.path.basename(fp)
    changed = False
    for n in d["nodes"]:
        if n["type"] == "MiniMaxH3ReferenceToVideo":
            wv = n.get("widgets_values", [])
            widget_len = wv[3] if len(wv) > 3 else None
            for i in n.get("inputs", []):
                if i["name"] == "length" and i.get("link") is not None:
                    old_link = i["link"]
                    i["link"] = None
                    changed = True
                    print("%-38s UNLINKED length (was link %s) -> widget value %s frames = %.1fs"
                          % (name, old_link, widget_len, widget_len / 24 if isinstance(widget_len, int) else 0))
    if changed:
        with open(fp, "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False)
    else:
        print("%-38s (no length link to remove - camera node or already unlinked)" % name)

print("\nDone. All R2V shots now use their widget length (per-shot), not the hidden 15s math node.")
