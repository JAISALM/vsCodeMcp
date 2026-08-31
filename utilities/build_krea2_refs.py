import json, shutil

# Clone the proven Krea2 t2i base workflow and repurpose it as a reference-image
# generator for the Jaisal Cut. Style chain (locked):
#   UNET krea2_turbo_fp8_scaled + LoRA Krea2_Cinematic_Artstyle @1.0
#   + CLIP qwen3vl_4b_fp8_scaled (krea2) + VAE qwen_image_vae
#   KSampler 8 steps, cfg 1.0, euler/simple, denoise 1.0 (t2i)
#   2048x1152 (2K 16:9)
src = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_base.json"
dst = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_refs.json"
shutil.copy(src, dst)
wf = json.load(open(dst, encoding="utf-8"))

# Character sheet prompt (abstract faceless character, rose shirt, black pant, black bag)
char_sheet = (
    "An angular, 3d art style, with brush stroke color texture. A character reference "
    "turnaround sheet of a young schoolboy figure, shown in three views side by side "
    "(front, side, back) on a clean neutral background. The figure has a head with short "
    "dark hair but a completely BLANK face - no nose, no eyes, no eyebrows, no mouth, a "
    "smooth featureless face. Wearing a rose-pink collared shirt, full-length black "
    "trousers, and carrying a black school bag. Consistent proportions across all three "
    "views, character model sheet, highly detailed, 16:9 widescreen"
)

# Negative: keep the style/consistency negatives, drop the old red-bag/uniform specifics
negative = (
    "shorts, short pants, bare legs, face, nose, eyes, eyebrows, mouth, facial features, "
    "red bag, red school bag, school uniform, tie, necktie, duplicate character, 2 kids, "
    "duplicated kids, blurry, low quality, deformed, watermark, text, logo, cartoon, "
    "flat vector, photorealistic, photo, different character, different costume"
)

for n in wf["nodes"]:
    if n["type"] == "CLIPTextEncode":
        # The positive prompt node is the one with the long style text; the negative is shorter.
        cur = n["widgets_values"][0]
        if "angular" in cur and "art style" in cur:
            n["widgets_values"] = [char_sheet]
            print("Positive prompt -> character sheet")
        else:
            n["widgets_values"] = [negative]
            print("Negative prompt -> faceless/consistency negatives")
    if n["type"] == "SaveImage":
        n["widgets_values"][0] = "jaisal_cut/refs"
        print("SaveImage -> jaisal_cut/refs")
    if n["type"] == "EmptyLatentImage":
        n["widgets_values"] = [2048, 1152, 1]
        print("EmptyLatentImage -> 2048x1152")

json.dump(wf, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Saved", dst)
