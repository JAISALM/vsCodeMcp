import json

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
PROMPT_FILE = r"d:\models\vsCodeMcp\prompts\jaisal_sketch_prompts.txt"

# The bridge-height line to insert after the handrail description.
HEIGHT_LINE = (
    "The bridge is HIGH above the river - a clear visible gap between the deck "
    "and the water below, the deck well above the water surface, so the jump "
    "into the river is a real drop. "
)

# ---------------------------------------------------------------------------
# 1. krea2_jaisal_sketch.json — node 6 (positive prompt): add bridge height
# ---------------------------------------------------------------------------
sketch_path = WF_DIR + r"\krea2_jaisal_sketch.json"
d = json.load(open(sketch_path))
for n in d["nodes"]:
    if n["id"] == 6:
        p = n["widgets_values"][0]
        anchor = "running along the edge of the bridge. "
        if HEIGHT_LINE.strip().split(" - ")[0] not in p:
            p = p.replace(anchor, anchor + HEIGHT_LINE, 1)
            n["widgets_values"][0] = p
            print("sketch node 6: bridge height added")
        else:
            print("sketch node 6: bridge height already present")
json.dump(d, open(sketch_path, "w"), indent=1)

# ---------------------------------------------------------------------------
# 2. jaisal_sketch_prompts.txt — prompt 1 (walking): add bridge height
# ---------------------------------------------------------------------------
txt = open(PROMPT_FILE).read()
anchor_txt = "running along the edge of the bridge. The river"
if "The bridge is HIGH above the river" not in txt:
    # Only the WALKING prompt (prompt 1) has "walking SLOWLY ... school bag on his back. The bridge is drawn ... running along the edge of the bridge. The river"
    walk_anchor = (
        "a small line-art school bag on his back. The bridge is\n"
        "drawn with simple lines: a flat deck line and a LOW HANDRAIL (a horizontal line\n"
        "with small vertical post lines) running along the edge of the bridge. The river"
    )
    walk_repl = (
        "a small line-art school bag on his back. The bridge is\n"
        "drawn with simple lines: a flat deck line and a LOW HANDRAIL (a horizontal line\n"
        "with small vertical post lines) running along the edge of the bridge. "
        "The bridge is HIGH above the river - a clear visible gap between the deck and\n"
        "the water below, the deck well above the water surface, so the jump into the\n"
        "river is a real drop. The river"
    )
    if walk_anchor in txt:
        txt = txt.replace(walk_anchor, walk_repl, 1)
        print("prompt file: walking prompt bridge height added")
    else:
        print("prompt file: walking anchor NOT found (manual check needed)")
open(PROMPT_FILE, "w").write(txt)

# ---------------------------------------------------------------------------
# 3. jaisal_single_shot.json — single-image title animation
# ---------------------------------------------------------------------------
ss_path = WF_DIR + r"\jaisal_single_shot.json"
d = json.load(open(ss_path))

TITLE_PROMPT = (
    "A simple 2D vector line-art animation in a clean confident line-work style. "
    "A stick figure schoolboy (a round head, a line body, line arms, line legs, "
    "clean confident line work, ONLY ONE character, no other people, no duplicates) "
    "walks SLOWLY along a simple line-art stone bridge, his line legs in a slow "
    "walking stride, his line arms swinging gently, a small line-art school bag on "
    "his back. The bridge is drawn with simple lines: a flat deck line and a LOW "
    "HANDRAIL (a horizontal line with small vertical post lines) running along the "
    "edge of the bridge. The bridge is HIGH above the river - a clear visible gap "
    "between the deck and the water below, the deck well above the water surface. "
    "The river water below is drawn as scattered small dots and short wavy dashes "
    "(dots and dashes for the water surface), a couple of simple line trees on the "
    "bank.\n\n"
    "Then the figure STOPS and LOOKS AROUND - he TURNS HIS HEAD to one side, holds, "
    "then TURNS HIS HEAD to the other side, looking around both ways, then WHISTLES "
    "(a small line-art whistle gesture, one line arm raised to his head).\n\n"
    "Then the figure JUMPS off the edge of the bridge into the river below, his "
    "line body in a mid-air jumping pose, his line arms out, his line legs bent, a "
    "real drop from the high bridge into the water.\n\n"
    "Then the water is calm, and the title 'The Jaisal Cut' (in clean line-art "
    "lettering, the words 'The' small, 'Jaisal' big, 'Cut' medium) appears centered "
    "in the frame. NO stick figure in the title moment.\n\n"
    "Keep the 2D vector line-art style, clean line work, flat 2D, minimal, simple, "
    "no shading, no 3d, no photorealistic, no cartoon shading, just lines, "
    "consistent throughout. Every frame is a MEDIUM shot (the figure's full body "
    "visible, a little of the bridge and river around him). NO wide shots, NO "
    "extreme close-ups. DEEP FOCUS throughout. All transitions are smooth and "
    "organic. Simple, funny, no special effects.\n\n"
    "Audio: a few soft footsteps on the bridge as the figure walks, a short whistle "
    "as he looks around, a soft splash as he jumps into the river, then a calm "
    "quiet hush as the title appears. No music, no dialogue."
)

for n in d["nodes"]:
    if n["id"] == 114:  # LoadImage
        n["widgets_values"][0] = "sketch_1_walk.png"
        print("single_shot node 114 (LoadImage) -> sketch_1_walk.png")
    if n["id"] == 92:   # SaveVideo
        n["widgets_values"][0] = "video/Jaisal_Sketch_Title"
        print("single_shot node 92 (SaveVideo) -> video/Jaisal_Sketch_Title")
    if n["id"] == 105:  # instance node (subgraph)
        n["widgets_values"][0] = TITLE_PROMPT
        if "widgets_values_named" in n:
            n["widgets_values_named"]["prompt"] = TITLE_PROMPT
        print("single_shot node 105 (instance) prompt set")

# internal node 104 (MiniMaxH3ImageToVideo) inside the subgraph
for s in d.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        if n["id"] == 104:
            n["widgets_values"][0] = TITLE_PROMPT
            if "widgets_values_named" in n:
                n["widgets_values_named"]["prompt"] = TITLE_PROMPT
            print("single_shot internal node 104 prompt set")

json.dump(d, open(ss_path, "w"), indent=1)
print("done")
