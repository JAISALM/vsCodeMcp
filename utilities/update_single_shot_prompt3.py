import json

ss_path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json"
d = json.load(open(ss_path))

# Stronger background lock (pure white, NOT cream/paper/wooden) + PHASE-based
# sequence with explicit state locks (fixes "still walking after jump").
TITLE_PROMPT = (
    "MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: this is a 2D vector "
    "line-art animation. ONE continuous MEDIUM shot (the figure's full body visible, a "
    "little of the bridge and river around him). NO wide shots, NO extreme close-ups. "
    "The camera is a STATIC EYE-LEVEL MEDIUM shot for the whole take - it is LOCKED and "
    "does NOT move, does NOT push in, does NOT drift, does NOT tilt, does NOT pan, does "
    "NOT zoom, does NOT orbit. REJECT any camera angle that is not a static eye-level "
    "MEDIUM shot.\n\n"
    "BACKGROUND LOCK, HIGHEST PRIORITY: the background is PURE WHITE (a clean empty "
    "white void), EXACTLY like the reference image. NOT cream, NOT beige, NOT tan, NOT "
    "paper, NOT wooden. NO wooden overlay, NO wooden floor, NO wooden table, NO wood "
    "grain, NO brown tones, NO warm tones, NO table, NO room, NO wall, NO scene, NO "
    "environment, NO setting, NO color, NO shading, NO additional background elements, "
    "NO out-of-space objects. The background is a flat pure white void with ONLY black "
    "ink lines on it, the whole time.\n\n"
    "A simple 2D vector line-art animation in a clean confident line-work style. A "
    "stick figure schoolboy (a round head, a line body, line arms, line legs, clean "
    "confident line work, a small line-art school bag on his back, ONLY ONE character, "
    "no other people, no duplicates) on a simple line-art stone bridge (a flat deck "
    "line and a LOW HANDRAIL with small vertical post lines), the bridge HIGH above the "
    "river (a clear visible gap between the deck and the water below), the river water "
    "drawn as scattered small dots and short wavy dashes, a couple of simple line trees "
    "on the bank.\n\n"
    "THE SEQUENCE (one continuous take, in this exact order):\n"
    "PHASE 1 - WALK: the figure walks SLOWLY along the bridge, his line legs in a slow "
    "walking stride, his line arms swinging gently. He is ON the bridge.\n"
    "PHASE 2 - THROW: the figure THROWS a small line-art paper plane (a simple folded "
    "triangle of lines) into the river below - one line arm extended forward, the paper "
    "plane flying away from his hand toward the water. He is still ON the bridge.\n"
    "PHASE 3 - JUMP: the figure JUMPS off the edge of the high bridge into the river "
    "below, following the paper plane. He LEAVES the bridge - he is NO LONGER on the "
    "bridge, he is in the AIR, his line body in a mid-air jumping pose, his line arms "
    "out, his line legs bent, a real drop from the high deck into the water. He is NOT "
    "walking, he is NOT on the bridge deck.\n"
    "PHASE 4 - PLANE FILLS SCREEN: the paper plane flies TOWARD the camera, growing "
    "LARGER and LARGER until it fills the screen - a large line-art paper plane on a "
    "pure white background. The figure is GONE (he is in the water, not visible).\n"
    "PHASE 5 - TITLE: the title 'The Jaisal Cut' appears on the large paper plane in "
    "clean line-art lettering (the words 'The' small, 'Jaisal' big, 'Cut' medium), "
    "spelled exactly T-h-e J-a-i-s-a-l C-u-t. NO stick figure, NO person, NO "
    "character.\n\n"
    "WHAT THE FIGURE DOES NOT DO: does NOT drink, does NOT hold a cup, does NOT hold a "
    "bottle, does NOT hold any object to his mouth, does NOT run, does NOT slide, is "
    "NOT duplicated, is NOT a second figure, is NOT a crowd. AFTER THE JUMP (PHASE 3), "
    "the figure is NO LONGER on the bridge - he does NOT walk on the bridge after "
    "jumping, he does NOT return to the bridge, he does NOT reappear on the bridge.\n\n"
    "Keep the 2D vector line-art style, clean line work, flat 2D, minimal, simple, "
    "no shading, no 3d, no photorealistic, no cartoon shading, just lines, "
    "consistent throughout. Every frame is a MEDIUM shot (the figure's full body "
    "visible, a little of the bridge and river around him). NO wide shots, NO "
    "extreme close-ups. DEEP FOCUS throughout (every line in the frame is sharp). "
    "The camera stays a locked static eye-level MEDIUM shot the whole time. All "
    "transitions are smooth and organic. Simple, funny, no special effects.\n\n"
    "Audio: a few soft footsteps on the bridge as the figure walks, a soft whoosh as "
    "the paper plane is thrown, a soft splash as he jumps into the river, then a calm "
    "quiet hush as the title appears. No music, no dialogue."
)

for n in d["nodes"]:
    if n["id"] == 105:
        n["widgets_values"][0] = TITLE_PROMPT
        if "widgets_values_named" in n:
            n["widgets_values_named"]["prompt"] = TITLE_PROMPT
        print("node 105 (instance) prompt set")

for s in d.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        if n["id"] == 104:
            n["widgets_values"][0] = TITLE_PROMPT
            if "widgets_values_named" in n:
                n["widgets_values_named"]["prompt"] = TITLE_PROMPT
            print("internal node 104 prompt set")

json.dump(d, open(ss_path, "w"), indent=1)
print("done")
