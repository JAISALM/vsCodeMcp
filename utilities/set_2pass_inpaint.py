"""Set krea2_2pass_bf16_turbo.json to INPAINT mode for the mic-removal task.

Changes:
  - node 247 (CLIPTextEncode): prompt -> mic-removal inpaint prompt + (word:-1.0) negatives
  - node 265 (LoadImage):      BYPASSED -> ACTIVE  (image = mic_small_id_00001_.png)
  - node 296 (ImageResizeKJv2):BYPASSED -> ACTIVE, size 1088x1920 -> 1920x1088 (landscape, matches image)
  - node 267 (InpaintModelConditioning): BYPASSED -> ACTIVE
  - node 254 (EmptyLatentImage): ACTIVE -> BYPASSED  (so Latent switch picks the i2i latent)
  - node 297 (SolidMask):      ACTIVE -> BYPASSED  (so MaskChoice switch picks the painted mask)
  - denoise stays 1.0 (PrimitiveFloat 270 active, mxSlider 264 bypassed) — classic inpaint

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\set_2pass_inpaint.py"
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_2pass_bf16_turbo.json"
wf = json.load(open(WF, encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}

PROMPT = (
    "Plain empty weathered wooden table surface, seamless blend with the surrounding scene, "
    "B&W high-contrast cinematic, fine film grain, static camera "
    "(black microphone:-1.0) (microphone:-1.0) (mic stand:-1.0) (tall object:-1.0) "
    "(color:-1.0) (people:-1.0) (extra objects:-1.0)"
)

def set_mode(nid, mode):
    n = nodes[nid]
    old = n.get("mode")
    n["mode"] = mode
    return f"node {nid} ({n.get('type')}): mode {old} -> {mode}"

log = []

# 1. Prompt (node 247)
n = nodes[247]
old_prompt = (n.get("widgets_values") or ["<none>"])[0]
n["widgets_values"][0] = PROMPT
log.append(f"node 247 (CLIPTextEncode): prompt replaced")
log.append(f"   OLD: {str(old_prompt)[:80]}...")
log.append(f"   NEW: {PROMPT[:80]}...")

# 2. LoadImage active
log.append(set_mode(265, 0))
# ensure image filename
nodes[265]["widgets_values"][0] = "mic_small_id_00001_.png"
log.append("   node 265 image = mic_small_id_00001_.png")

# 3. ImageResizeKJv2 active + landscape size
log.append(set_mode(296, 0))
wv = nodes[296]["widgets_values"]
wv[0], wv[1] = 1920, 1088
log.append(f"   node 296 size -> {wv[0]}x{wv[1]} (landscape)")

# 4. InpaintModelConditioning active
log.append(set_mode(267, 0))

# 5. EmptyLatentImage bypassed
log.append(set_mode(254, 4))

# 6. SolidMask bypassed
log.append(set_mode(297, 4))

json.dump(wf, open(WF, "w", encoding="utf-8"), indent=1)
print("=== INPAINT MODE SET ===")
for line in log:
    print(line)
print("\nwrote:", WF)
