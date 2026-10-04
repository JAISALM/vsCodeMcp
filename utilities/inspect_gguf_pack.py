# -*- coding: utf-8 -*-
import re
s = open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-GGUF-nif0\nodes.py", encoding="utf-8").read()
print("=== NODE CLASSES ===")
for m in re.findall(r"class (\w+)\(", s):
    print("  ", m)
print()
print("=== NODE_CLASS_MAPPINGS ===")
m = re.search(r"NODE_CLASS_MAPPINGS\s*=\s*\{(.*?)\}", s, re.S)
if m:
    for line in m.group(1).splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            print("  ", line)
print()
print("=== README (first 60 lines) ===")
r = open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-GGUF-nif0\README.md", encoding="utf-8").read()
print("\n".join(r.splitlines()[:60]))
