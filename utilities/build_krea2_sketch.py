import json, shutil, os

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_refs.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_sketch.json"

# Clone the native UI-saved file (preserves all native widget shapes / pos / size / inputs / outputs)
shutil.copyfile(SRC, DST)
w = json.load(open(DST, encoding="utf-8"))

WALK_POS = (
    "A 2D vector line art style, clean confident line work, a simple stick figure "
    "character (a round head, a line body, line arms, line legs), black ink lines on a "
    "clean light background, flat 2D, minimal, simple, no shading, no 3d, no "
    "photorealistic, no cartoon shading, just lines, 16:9 widescreen. MEDIUM shot, a "
    "single stick figure schoolboy - ONLY ONE character, no other people, no "
    "duplicates - walking SLOWLY along a simple line-art stone bridge, his line legs "
    "in a slow walking stride, his line arms swinging gently, a small line-art school "
    "bag on his back, the bridge is a few simple lines (a flat deck line + a low "
    "handrail line), a few wavy lines for the river water below, a couple of simple "
    "line trees on the bank, the figure's full body (head to feet) is visible, a "
    "little of the bridge and river around him, clean simple line work, 16:9 widescreen\n"
)

SKETCH_NEG = (
    "3d, 3d render, photorealistic, photo, realistic, shading, shadow, gradient, "
    "color fill, flat color, cartoon, cartoon shading, cel shading, multiple "
    "characters, more than one figure, duplicate character, extra people, blurry, "
    "low quality, deformed, watermark, text, logo, wide shot, wide angle, "
    "establishing shot, extreme close-up, face close-up, detailed background, "
    "complex background, special effects, particles, glow, motion blur\n"
)

by_id = {n["id"]: n for n in w["nodes"]}

# LoRA -> line-art LoRA @ 1.0
by_id[15]["widgets_values"] = ["krea2_lineart_v1_fp16.safetensors", 1]
# positive prompt -> walking stick figure
by_id[6]["widgets_values"] = [WALK_POS]
# negative prompt -> sketch negative
by_id[13]["widgets_values"] = [SKETCH_NEG]
# save prefix
by_id[29]["widgets_values"] = ["jaisal_cut/sketch"]
# KSampler: keep t2i denoise 1.0, 8 steps, cfg 1, euler/simple (already correct)
# EmptyLatentImage: keep [2048, 1152, 1]

json.dump(w, open(DST, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("WROTE", DST)
print("nodes:", [(n["id"], n["type"], n.get("widgets_values")) for n in w["nodes"]])
