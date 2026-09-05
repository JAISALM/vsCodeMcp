import json

ss_path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json"
d = json.load(open(ss_path))

# New sequence: walk -> throw paper plane -> jump -> plane fills screen -> title on plane.
# Background lock (plain white, no wooden floor) + no-drinking NOT-lists.
TITLE_PROMPT = (
    "MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: this is a 2D vector "
    "line-art animation. The whole video is ONE continuous MEDIUM shot (the figure's "
    "full body visible, a little of the bridge and river around him). NO wide shots, "
    "NO extreme close-ups. The camera is a STATIC EYE-LEVEL MEDIUM shot for the whole "
    "take - it is LOCKED and does NOT move, does NOT push in, does NOT drift, does NOT "
    "tilt, does NOT pan, does NOT zoom, does NOT orbit. ACCEPT the natural perspective "
    "of the locked camera. DO NOT auto-adjust the camera to a more flattering angle. "
    "REJECT any camera angle that is not a static eye-level MEDIUM shot.\n\n"
    "BACKGROUND LOCK, HIGHEST PRIORITY: the background is PLAIN WHITE / CLEAN, EXACTLY "
    "like the reference image - black ink lines on a clean white background ONLY. NO "
    "wooden floor, NO wooden background, NO table, NO room, NO wall, NO scene clutter, "
    "NO color, NO shading, NO additional background elements, NO out-of-space objects. "
    "The background stays plain white the whole time, just like the reference image.\n\n"
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
    "Then the figure THROWS a small line-art paper plane (a simple folded triangle of "
    "lines) into the river below - one line arm extended forward, the paper plane "
    "flying away from his hand toward the water.\n\n"
    "Then the figure JUMPS off the edge of the high bridge into the river below, "
    "following the paper plane, his line body in a mid-air jumping pose, his line arms "
    "out, his line legs bent, a real drop from the high deck into the water.\n\n"
    "Then the paper plane flies TOWARD the camera, growing LARGER and LARGER until it "
    "fills the screen - a large line-art paper plane on a plain white background.\n\n"
    "Then the title 'The Jaisal Cut' appears on the large paper plane in clean "
    "line-art lettering (the words 'The' small, 'Jaisal' big, 'Cut' medium), spelled "
    "exactly T-h-e J-a-i-s-a-l C-u-t. NO stick figure in the title moment, NO person, "
    "NO character.\n\n"
    "WHAT THE FIGURE DOES, IN ORDER: (1) walks slowly, (2) throws a paper plane into "
    "the river, (3) jumps into the river after the paper plane, (4) the paper plane "
    "flies toward the camera and fills the screen, (5) the title 'The Jaisal Cut' "
    "appears on the paper plane.\n"
    "WHAT THE FIGURE DOES NOT DO: does NOT drink, does NOT hold a cup, does NOT hold a "
    "bottle, does NOT hold any object to his mouth, does NOT run, does NOT slide, is "
    "NOT duplicated, is NOT a second figure, is NOT a crowd. The figure is NEVER "
    "duplicated.\n"
    "BACKGROUND: plain white, black ink lines only, NO wooden floor, NO wooden "
    "background, NO color, NO shading, NO scene clutter, exactly like the reference "
    "image.\n\n"
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
