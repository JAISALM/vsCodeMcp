"""Check which node classes the H3 Extender registers vs the original Motion-Context pack,
and flag exact class-name conflicts (same class_type = one pack silently wins at load)."""
import re, sys

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes"
EXT = BASE + r"\ComfyUI-Minimax-H3-Extender"
ORIG = BASE + r"\ComfyUI-H3-Motion-Context"

def registered(root):
    """Collect class names from NODE_CLASS_MAPPINGS across all .py files in the pack."""
    import os
    names = set()
    for fn in os.listdir(root):
        if not fn.endswith(".py"):
            continue
        p = os.path.join(root, fn)
        try:
            s = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for m in re.finditer(r"NODE_CLASS_MAPPINGS\s*=\s*\{(.*?)\}", s, re.S):
            names.update(re.findall(r"['\"](\w+)['\"]\s*:", m.group(1)))
        # also catch dict.update({...}) style
        for m in re.finditer(r"\.update\(\s*\{(.*?)\}\s*\)", s, re.S):
            names.update(re.findall(r"['\"](\w+)['\"]\s*:", m.group(1)))
    return names

ext = registered(EXT)
orig = registered(ORIG)

print("=== Extender registered classes ===")
for n in sorted(ext):
    print("  ", n)
print("=== Original Motion-Context registered classes ===")
for n in sorted(orig):
    print("  ", n)
conf = ext & orig
print("=== CONFLICTS (same class_type in BOTH) ===")
if conf:
    for n in sorted(conf):
        print("  !!", n)
else:
    print("  (none)")
