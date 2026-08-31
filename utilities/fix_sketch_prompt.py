import json

DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_sketch.json"
w = json.load(open(DST, encoding="utf-8"))

WALK_POS = (
    "A 2D vector line art style, clean confident line work, black ink lines on a "
    "clean light background, flat 2D, minimal, simple, no shading, no 3d, no "
    "photorealistic, no cartoon shading, just lines, 16:9 widescreen. MEDIUM shot "
    "with the figure SMALL in the frame - a single simple stick figure schoolboy "
    "(a round head, a line body, line arms, line legs) - ONLY ONE character, no "
    "other people, no duplicates - the figure is SMALL, occupying only about "
    "one-third of the frame height, walking SLOWLY along a simple line-art stone "
    "bridge, his line legs in a slow walking stride, his line arms swinging "
    "gently, a small line-art school bag on his back. The bridge is drawn with "
    "simple lines: a flat deck line and a LOW HANDRAIL (a horizontal line with "
    "small vertical post lines) running along the edge of the bridge. The river "
    "water below is drawn as scattered small dots and short wavy dashes (dots and "
    "dashes for the water surface), a couple of simple line trees on the bank. "
    "The figure is small in the frame with plenty of bridge and river visible "
    "around him, clean simple line work, 16:9 widescreen\n"
)

SKETCH_NEG = (
    "3d, 3d render, photorealistic, photo, realistic, shading, shadow, gradient, "
    "color fill, flat color, cartoon, cartoon shading, cel shading, multiple "
    "characters, more than one figure, duplicate character, extra people, blurry, "
    "low quality, deformed, watermark, text, logo, wide shot, wide angle, "
    "establishing shot, extreme close-up, face close-up, detailed background, "
    "complex background, special effects, particles, glow, motion blur, large "
    "figure, figure filling the frame, big figure, figure taking up most of the "
    "frame, close-up of the figure, bridge without handrail, no handrail, plain "
    "flat water, no water dots, no water texture\n"
)

by_id = {n["id"]: n for n in w["nodes"]}
by_id[6]["widgets_values"] = [WALK_POS]
by_id[13]["widgets_values"] = [SKETCH_NEG]

json.dump(w, open(DST, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("UPDATED krea2_jaisal_sketch.json")
print("positive:", by_id[6]["widgets_values"][0][:200], "...")
print("negative:", by_id[13]["widgets_values"][0][:200], "...")
