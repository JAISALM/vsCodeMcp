import json

ss_path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json"
d = json.load(open(ss_path))

# Detailed single-continuous-take prompt with camera-lock discipline + explicit
# action chain + NOT-lists (per the H3 camera-correction lesson, 2026-08-31).
TITLE_PROMPT = (
    "MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: this is a 2D vector "
    "line-art animation. The whole video is ONE continuous MEDIUM shot (the figure's "
    "full body visible, a little of the bridge and river around him). NO wide shots, "
    "NO extreme close-ups. The camera is a STATIC EYE-LEVEL MEDIUM shot for the whole "
    "take - it is LOCKED and does NOT move, does NOT push in, does NOT drift, does NOT "
    "tilt, does NOT pan, does NOT zoom, does NOT orbit. ACCEPT the natural perspective "
    "of the locked camera. DO NOT auto-adjust the camera to a more flattering angle. "
    "DO NOT move the camera to make the figure look better. REJECT any camera angle "
    "that is not a static eye-level MEDIUM shot.\n\n"
    "A simple 2D vector line-art animation in a clean confident line-work style. A "
    "stick figure schoolboy (a round head, a line body, line arms, line legs, clean "
    "confident line work, a small line-art school bag on his back, ONLY ONE character, "
    "no other people, no duplicates) walks SLOWLY along a simple line-art stone "
    "bridge, his line legs in a slow walking stride, his line arms swinging gently. "
    "The bridge is drawn with simple lines: a flat deck line and a LOW HANDRAIL (a "
    "horizontal line with small vertical post lines) running along the edge of the "
    "bridge. The bridge is HIGH above the river - a clear visible gap between the "
    "deck and the water below, the deck well above the water surface. The river water "
    "below is drawn as scattered small dots and short wavy dashes (dots and dashes for "
    "the water surface), a couple of simple line trees on the bank.\n\n"
    "Then the figure STOPS and LOOKS AROUND - he TURNS HIS HEAD to one side, holds, "
    "then TURNS HIS HEAD to the other side, looking around both ways, then WHISTLES "
    "(a small line-art whistle gesture, one line arm raised to his head).\n\n"
    "Then the figure JUMPS off the edge of the high bridge into the river below, his "
    "line body in a mid-air jumping pose, his line arms out, his line legs bent, a "
    "real drop from the high deck into the water.\n\n"
    "Then the water is calm, and the title 'The Jaisal Cut' (in clean line-art "
    "lettering, the words 'The' small, 'Jaisal' big, 'Cut' medium) appears centered "
    "in the frame. NO stick figure in the title moment, NO person, NO character.\n\n"
    "WHAT THE FIGURE DOES, IN ORDER: (1) walks slowly, (2) stops, (3) looks around "
    "both sides, (4) whistles, (5) jumps into the river, (6) the title appears. "
    "WHAT THE FIGURE DOES NOT DO: does NOT run, does NOT slide, does NOT leave the "
    "bridge before the jump, does NOT jump before the whistle, is NOT duplicated, is "
    "NOT a second figure, is NOT a crowd, does NOT change into a different character. "
    "The figure is NEVER duplicated.\n\n"
    "Keep the 2D vector line-art style, clean line work, flat 2D, minimal, simple, "
    "no shading, no 3d, no photorealistic, no cartoon shading, just lines, "
    "consistent throughout. Every frame is a MEDIUM shot (the figure's full body "
    "visible, a little of the bridge and river around him). NO wide shots, NO "
    "extreme close-ups. DEEP FOCUS throughout (every line in the frame is sharp). "
    "The camera stays a locked static eye-level MEDIUM shot the whole time. All "
    "transitions are smooth and organic. Simple, funny, no special effects.\n\n"
    "Audio: a few soft footsteps on the bridge as the figure walks, a short whistle "
    "as he looks around, a soft splash as he jumps into the river, then a calm quiet "
    "hush as the title appears. No music, no dialogue."
)

for n in d["nodes"]:
    if n["id"] == 105:  # instance node (subgraph)
        n["widgets_values"][0] = TITLE_PROMPT
        if "widgets_values_named" in n:
            n["widgets_values_named"]["prompt"] = TITLE_PROMPT
        print("node 105 (instance) prompt set")

for s in d.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        if n["id"] == 104:  # internal MiniMaxH3ImageToVideo
            n["widgets_values"][0] = TITLE_PROMPT
            if "widgets_values_named" in n:
                n["widgets_values_named"]["prompt"] = TITLE_PROMPT
            print("internal node 104 prompt set")

json.dump(d, open(ss_path, "w"), indent=1)
print("done")
