"""Clone the kf7b keyframe workflow (Krea2 Identity Edit v1.2) for the small-mic ref.

The keyframe trick (from krea2_intro_kf7b_page_mic_v8.json):
  base image -> VAEEncode -> Krea2EditModelPatch (ref_boost 4) -> KSampler (10 steps, cfg 1)
  + Krea2EditGroundedEncode (plain-English instruction, grounding 768)
  + identity LoRA krea2_identity_edit_v1_2 @ 1.0
  + UNET krea2_turbo_fp8_scaled, CLIP qwen3vl_4b_fp8_scaled (krea2), VAE qwen_image_vae

Changes for the small-mic ref:
  - LoadImage base: mic+paper_2k.png (table + chair + bulb + papers + tall mic)
  - instruction: shrink the mic to a small compact studio mic on a short low stand,
    papers on the table, NO person
  - negative: no-person + no-tall-mic
  - SaveImage: jaisal_cut/mic_small_ref
"""
import json, os, shutil

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
SRC = os.path.join(WF_DIR, "krea2_intro_kf7b_page_mic_v8.json")
DST = os.path.join(WF_DIR, "krea2_small_mic_ref.json")

d = json.load(open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}

INSTRUCTION = (
    "Black and white cinematic photograph, strictly monochrome, high contrast, fine film grain, no color at all. "
    "A single bare bulb hangs from above on a thin cord, the ONLY light source. "
    "A dark charcoal wall behind the table (deep gray, near-black at the edges), the wall falls into shadow away from the bulb's light pool, only the area under the bulb is lit. "
    "Everything outside the light pool fades into darkness. "
    "A simple wooden table and ONE simple wooden chair (consistent size, color, and position). ONLY ONE chair in the frame, centered. "
    "There is NO person. "
    "On the table sits a SMALL compact studio microphone on a SHORT LOW stand - small and low-profile, NOT tall, NOT a broadcast mic. "
    "A few loose sheets of paper with dense handwriting are scattered on the table surface. "
    "Straight-on, centered, symmetric framing, eye level, static camera. Medium framing, 50mm lens."
)

NEGATIVE = (
    "person, human, face, body, arms, hands, extra chairs, multiple chairs, second chair, another chair, "
    "tall microphone, tall stand, large microphone, broadcast mic, big mic, multiple microphones, second mic, "
    "extra papers, many papers, multiple papers, glowing effects, hologram, color, warm tones, "
    "multiple light sources, fill light, bright room, bright wall, white wall, cream wall, light background, "
    "washed out, overexposed background, text, watermark, logo, cartoon, 3d render, blurry, low quality, "
    "asymmetric, off-center, tilted camera, extreme close-up"
)

# 72: base image
nodes[72]["widgets_values"] = ["mic+paper_2k.png", "image"]
# 84: instruction (grounding 768, empty 3rd slot)
nodes[84]["widgets_values"] = [INSTRUCTION, 768, ""]
# 85: negative
nodes[85]["widgets_values"] = [NEGATIVE, 768, ""]
# 29: save name
nodes[29]["widgets_values"] = ["jaisal_cut/mic_small_ref"]
# 53: fresh random seed
nodes[53]["widgets_values"] = [1234567890, "randomize", 10, 1, "euler", "simple", 1]
# 79: ref_boost 4, ref_boost_a 1, fit (same as kf7b)
nodes[79]["widgets_values"] = [4, 1, "fit"]

json.dump(d, open(DST, "w", encoding="utf-8"), indent=1)
print("WROTE", DST)
print("nodes:", len(d["nodes"]), "links:", len(d.get("links", [])))
