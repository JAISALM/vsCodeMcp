# -*- coding: utf-8 -*-
"""Search the whole ComfyUI install + project for the 2BZ character-sheet
workflow (by filename or by content), and list the installed character-sheet
node family."""
import os, glob, json

roots = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user",
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI",
    r"D:\models\vsCodeMcp",
]
needles = ["2BZ", "character_sheet", "2stage", "character sheet"]

print("=== FILENAME matches ===")
for root in roots:
    for dirpath, dirnames, filenames in os.walk(root):
        # skip heavy dirs
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git", "models", "output", "input")]
        for fn in filenames:
            if fn.lower().endswith(".json"):
                low = fn.lower()
                for nd in needles:
                    if nd.lower() in low:
                        print("  FILE:", os.path.join(dirpath, fn))
                        break

print("\n=== CONTENT matches (2BZ / 2stage) in workflow json ===")
for root in [r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows",
             r"D:\models\vsCodeMcp"]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git")]
        for fn in filenames:
            if fn.lower().endswith(".json"):
                p = os.path.join(dirpath, fn)
                try:
                    s = open(p, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                if "2BZ" in s or "2stage" in s or "character_sheet" in s:
                    print("  CONTENT:", p)
