# -*- coding: utf-8 -*-
import re
s = open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-GGUF-nif0\nodes.py", encoding="utf-8").read()
# Find the CLIPLoaderGGUF class and print its INPUT_TYPES + folder logic
m = re.search(r"class CLIPLoaderGGUF.*?(?=\nclass |\Z)", s, re.S)
if m:
    print("=== CLIPLoaderGGUF class ===")
    print(m.group(0)[:3000])
else:
    print("CLIPLoaderGGUF class not found")
# Also find where it looks for files (folder_names / get_clip / text_encoder)
print()
print("=== folder references ===")
for line in s.splitlines():
    if any(t in line for t in ("folder_names", "text_encoder", "clip", "get_clip", "models")):
        print("  ", line.strip())
