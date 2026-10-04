"""v2: small-mic ref from a CLEAN base (table empty.png) — nothing to fight.

v1 (mic_small_ref.json) used base mic+paper_2k.png which ALREADY has a tall mic +
floating papers; the identity edit (ref_boost 4) faithfully preserved them, so the
mic stayed tall and the papers stayed in the air.

v2 base = table empty.png (weathered table + empty chair + bare bulb + black void,
NO mic, NO papers). The instruction ADDS a small compact mic on a short low stand +
a few loose papers ON the table surface. Nothing competing.
"""
import json, os

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
SRC = os.path.join(WF_DIR, "krea2_intro_kf7b_page_mic_v8.json")
DST = os.path.join(WF_DIR, "krea2_small_mic_ref_v2.json")

d = json.load(open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}

INSTRUCTION = (
    "Black and white cinematic photograph, strictly monochrome, high contrast, fine film grain, no color at all. "
    "A single bare bulb hangs from above on a thin cord, the ONLY light source. "
    "A dark charcoal wall behind the table (deep gray, near-black at the edges), the wall falls into shadow away from the bulb's light pool, only the area under the bulb is lit. "
    "Everything outside the light pool fades into darkness. "
    "A simple weathered wooden table and ONE simple wooden chair behind it (consistent size, color, and position). ONLY ONE chair in the frame. "
    "There is NO person. "
    "On the table sits a SMALL compact studio microphone on a SHORT LOW stand - small and low-profile, its top well below the height of a tall broadcast mic, resting low on the table surface. "
    "A few loose sheets of paper with dense handwriting lie FLAT on the table surface, scattered around the microphone base. "
    "Straight-on, centered, symmetric framing, eye level, static camera. Medium framing, 50mm lens."
)

NEGATIVE = (
    "person, human, face, body, arms, hands, extra chairs, multiple chairs, second chair, another chair, "
    "tall microphone, tall stand, large microphone, broadcast mic, big mic, multiple microphones, second mic, "
    "floating papers, papers in the air, papers flying, papers floating, papers in the sky, "
    "extra papers, many papers, multiple papers, glowing effects, hologram, color, warm tones, "
    "multiple light sources, fill light, bright room, bright wall, white wall, cream wall, light background, "
    "washed out, overexposed background, text, watermark, logo, cartoon, 3d render, blurry, low quality, "
    "asymmetric, off-center, tilted camera, extreme close-up"
)

# 72: base image -> clean table
nodes[72]["widgets_values"] = ["table empty.png", "image"]
# 84: instruction
nodes[84]["widgets_values"] = [INSTRUCTION, 768, ""]
# 85: negative
nodes[85]["widgets_values"] = [NEGATIVE, 768, ""]
# 29: save name
nodes[29]["widgets_values"] = ["jaisal_cut/mic_small_ref_v2"]
# 53: fresh random seed
nodes[53]["widgets_values"] = [2345678901, "randomize", 10, 1, "euler", "simple", 1]
# 79: ref_boost 4, ref_boost_a 1, fit
nodes[79]["widgets_values"] = [4, 1, "fit"]

json.dump(d, open(DST, "w", encoding="utf-8"), indent=1)
print("WROTE", DST)
print("nodes:", len(d["nodes"]), "links:", len(d.get("links", [])))
