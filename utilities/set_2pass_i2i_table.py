"""Switch krea2_2pass_bf16_turbo.json to I2I FULL-IMAGE mode with table empty.png base.

Goal: i2i from the clean "table empty" base -> add a SMALL compact mic + loose papers,
keeping the table/chair/bulb/void/B&W style (the same way the original refs were made).

Changes from the current (inpaint) config:
  - LoadImage (265): image -> "table empty.png"  (staged to input)
  - SolidMask (297): BYPASSED -> ACTIVE  (full-image mask = i2i full image, not painted)
  - denoise (270 PrimitiveFloat): 1.0 -> 0.7  (partial: keep table/chair/bulb, add mic+paper)
  - prompt (247): small mic + paper scene + (word:-1.0) negatives
  - ImageResizeKJv2 (296): 1920x1088 (16:9 working size, matches base aspect)

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\set_2pass_i2i_table.py"
"""
import json, shutil, os

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_2pass_bf16_turbo.json"
BASE_SRC = r"D:\models\vsCodeMcp\Jaisal-intro\keyframes\table empty.png"
BASE_NAME = "table empty.png"
INPUT_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"

# 1. Stage the base image into ComfyUI input
dst = os.path.join(INPUT_DIR, BASE_NAME)
shutil.copyfile(BASE_SRC, dst)
print(f"staged base -> {dst} ({os.path.getsize(dst)/1024:.0f} KB)")

wf = json.load(open(WF, encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}

PROMPT = (
    "A weathered wooden table with a single empty wooden chair behind it, a single bare bulb "
    "hanging from a thin wire above, pure black void background. On the table sits a SMALL "
    "compact studio microphone on a SHORT LOW stand, with a few loose sheets of paper with "
    "dense handwriting scattered on the table surface. B&W high-contrast cinematic, fine film "
    "grain, static camera, medium-wide "
    "(large microphone:-1.0) (tall stand:-1.0) (tall object:-1.0) (color:-1.0) (people:-1.0) "
    "(extra objects:-1.0) (multiple microphones:-1.0)"
)

log = []

# LoadImage -> table empty base
n = nodes[265]
n["mode"] = 0
n["widgets_values"][0] = BASE_NAME
log.append(f"node 265 (LoadImage): active, image = {BASE_NAME}")

# SolidMask -> ACTIVE (full-image mask = i2i full image)
n = nodes[297]
n["mode"] = 0
log.append("node 297 (SolidMask): ACTIVE (full-image mask)")

# denoise -> 0.7 (partial: keep scene, add mic+paper)
n = nodes[270]
n["widgets_values"][0] = 0.7
log.append("node 270 (denoise): 0.7")

# ImageResizeKJv2 -> 1920x1088 (16:9, matches base aspect)
n = nodes[296]
n["mode"] = 0
n["widgets_values"][0] = 1920
n["widgets_values"][1] = 1088
log.append("node 296 (ImageResizeKJv2): 1920x1088")

# InpaintModelConditioning -> active (i2i conditioning)
nodes[267]["mode"] = 0
log.append("node 267 (InpaintModelConditioning): active")

# EmptyLatentImage -> bypassed (so latent switch picks the i2i latent)
nodes[254]["mode"] = 4
log.append("node 254 (EmptyLatentImage): BYPASSED")

# prompt
n = nodes[247]
n["widgets_values"][0] = PROMPT
log.append("node 247 (prompt): small mic + paper scene")

json.dump(wf, open(WF, "w", encoding="utf-8"), indent=1)
print("=== I2I FULL-IMAGE MODE (table empty base) ===")
for line in log:
    print("  ", line)
print("\nwrote:", WF)
