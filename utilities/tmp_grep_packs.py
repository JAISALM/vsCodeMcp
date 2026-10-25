import io, re

base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes"

# krea2edit: find Krea2EditModelPatch class + INPUT_TYPES
c = io.open(base + r"\comfyui-krea2edit\__init__.py", encoding="utf-8", errors="replace").read()
i = c.find("class Krea2EditModelPatch")
seg = c[i:i+3000]
print("===== Krea2EditModelPatch =====")
print(seg[:2600])

# enhancer node names
e = io.open(base + r"\ComfyUI-Krea2T-Enhancer\turbo_sigma_scheduler.py", encoding="utf-8", errors="replace").read()
print("===== turbo_sigma_scheduler.py (head) =====")
print(e[:1500])
for m in re.finditer(r'class (\w+)', e):
    print("class:", m.group(1))
a = io.open(base + r"\ComfyUI-Krea2T-Enhancer\advanced.py", encoding="utf-8", errors="replace").read()
for m in re.finditer(r'class (\w+)', a):
    print("advanced class:", m.group(1))
p = io.open(base + r"\ComfyUI-Krea2T-Enhancer\attention_weighted_phrase.py", encoding="utf-8", errors="replace").read()
for m in re.finditer(r'class (\w+)', p):
    print("awp class:", m.group(1))

# negpip
n = io.open(base + r"\ComfyUI-krea2-negpip\krea2_negpip.py", encoding="utf-8", errors="replace").read()
print("===== krea2_negpip classes =====")
for m in re.finditer(r'class (\w+)', n):
    print("class:", m.group(1))
m = re.search(r'NODE_CLASS_MAPPINGS = \{(.*?)\}', n, re.S)
if m: print("mappings:", m.group(1)[:400])
