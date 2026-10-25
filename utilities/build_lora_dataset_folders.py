# build_lora_dataset_folders.py
# Builds Fizgig-ready training folders for the 2-subject LoRA Isolation run (D167):
#   D:\lora_training\jaisal\NN_slug.png + NN_slug.txt
#   D:\lora_training\zidane\NN_slug.png + NN_slug.txt
# Images = copies of output\Dataset\{Jaisal,zidane}\Image_NNNNN_.png (order = the
# 20-prompt list embedded in node 377 of "1 Click Dataset (Klein 9b).json").
# Captions follow docs/lora-tools/fizgig_MULTI_PERSON.md:
#   "<trigger>, a man, <scene/pose/clothing/light — NO identity words>"
# Triggers (verified vs Krea 2 text encoder per the guide): jaisal=jeskv, zidane=dlor.

import os, shutil, sys

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\Dataset"
DST = r"D:\lora_training"

TRIGGERS = {"jaisal": "jeskv", "zidane": "dlor"}

# (slug, caption) — caption = prompt N rewritten in caption style (scene only, no identity)
PROMPTS = [
 ("frontal_headshot_85mm_white_bg",
  "frontal headshot, neutral expression, head tilted slightly to the right, close-up, 85mm lens f/2.8, sharp focus on the eyes, high-key studio lighting, seamless white background, detailed skin texture"),
 ("city_street_35mm_black_jeans",
  "walking down a busy city street in the afternoon, head turned slightly toward the camera, candid expression, medium shot, 35mm wide-angle lens f/4.0, urban bokeh background, natural sunlight, soft lens flare, wearing a black t-shirt and black jeans"),
 ("tpose_50mm_white_bg_bathrobe",
  "standing in a neutral T-pose, looking directly into the lens, wide full-body shot, 50mm lens f/8.0, clean white background, even professional lighting, wearing a purple bathrobe"),
 ("neon_alley_profile_35mm",
  "standing in a dark alleyway, head turned in a sharp profile toward a light source, illuminated by pink and blue neon signs, strong rim lighting, medium shot, 35mm lens f/1.8, high-contrast cinematic atmosphere"),
 ("industrial_loft_24mm_black_outfit",
  "standing in a dimly lit industrial loft, head angled three-quarters away from the camera, full-body shot, 24mm lens, natural light streaks from a high side window, deep shadows, dramatic chiaroscuro, wearing black clothing"),
 ("profile_golden_hour_105mm",
  "true profile view of the head, chin tilted slightly upward, close-up, 105mm telephoto lens, compressed background, golden hour sunlight from behind, glowing halo effect on hair and silhouette"),
 ("wooden_stool_85mm_grey_bg",
  "sitting on a simple wooden stool, head tilted slightly downward, eyes looking up at the camera, medium shot, 85mm lens f/4.0, soft butterfly lighting, subtle shadows under the nose and chin, neutral grey-white background"),
 ("rooftop_night_35mm_city_bokeh",
  "standing on a rooftop at night, body facing away, head turned back over the shoulder toward the camera, half-body shot, 35mm lens f/2.8, blurred city skyline bokeh, cool blue moonlight"),
 ("subway_50mm_fluorescent",
  "riding a subway train, head bowed slightly as if in thought, medium shot, 50mm lens f/2.8, harsh flickering overhead fluorescent lighting, realistic skin texture, matte black t-shirt"),
 ("foggy_forest_50mm_light_beam",
  "standing in a foggy forest at night, head tilted back looking up into a beam of light, medium shot, 50mm lens f/1.4, a single bright volumetric beam from above, moody cinematic look, soft diffused edges"),
 ("artist_studio_85mm_warm_lamp",
  "in a messy artist studio, head tilted slightly to the left, curious expression, close-up, 85mm prime lens f/1.8, creamy bokeh, paintbrushes and canvases in the background, warm golden lamp light on the side of the face, cinematic color grading"),
 ("skatepark_35mm_midday_sun",
  "sitting on a concrete ramp at a sun-bleached skatepark, head turned away from the sun toward the horizon, medium shot, 35mm lens f/5.6, oversized skater clothes, harsh midday sun, sharp dark shadows on the concrete"),
 ("arms_crossed_50mm_white_bg",
  "standing with arms crossed against a seamless white background, looking directly at the camera, slight chin tuck, wide full-body shot, 50mm lens f/8.0, baggy outfit, black flip-flops, even high-detail studio lighting"),
 ("low_angle_24mm_orange_teal",
  "low-angle shot looking up, head tilted down toward the lens, confident gaze, medium shot, 24mm wide-angle lens, slightly heroic perspective, orange and teal stylized studio lighting, strong rim light defining the silhouette"),
 ("green_park_35mm_dappled",
  "walking through a lush green park, head turned in a three-quarter view as if looking at something in the distance, full-body shot, 35mm lens f/2.8, dappled sunlight through the tree canopy, spotted light effect, oversized shirt"),
 ("screen_glow_50mm_dark_room",
  "face illuminated solely by the glow of a computer screen in a pitch-black room, head angled slightly upward, blue light reflecting off the face features and eyes, close-up face shot, 50mm lens f/1.2, extreme skin detail, intense focused expression"),
 ("record_store_35mm_amber",
  "standing in a cozy cluttered record store, viewed from a profile angle looking at a shelf, medium shot, 35mm lens f/2.0, warm amber-toned interior lighting, nostalgic soft atmosphere, oversized skater outfit"),
 ("rainy_streetlamp_50mm",
  "standing under a single flickering street lamp in the rain, head bowed slightly, face partially in shadow, half-body medium shot, 50mm lens f/2.8, dramatic backlighting, bright outline around hair and shoulders, wet pavement reflections, raindrops in the air"),
 ("beach_pier_sunset_85mm",
  "standing on a wooden beach pier during sunset, head tilted back slightly, eyes closed, enjoying the breeze, medium shot, 85mm lens f/2.2, sky in a deep orange and purple gradient, soft warm glow on the face and the fabric"),
 ("purple_bg_north_light_50mm",
  "relaxed three-quarter view, standing against a neutral purple background, head turned slightly off-camera, medium shot, 50mm lens f/4.0, soft diffused north-light style illumination, natural shape of facial features, no harsh shadows"),
]

def main():
    total = 0
    for char in ("jaisal", "zidane"):
        src_dir = os.path.join(SRC, "Jaisal" if char == "jaisal" else "zidane")
        dst_dir = os.path.join(DST, char)
        os.makedirs(dst_dir, exist_ok=True)
        trig = TRIGGERS[char]
        for i, (slug, cap) in enumerate(PROMPTS, start=1):
            src = os.path.join(src_dir, "Image_%05d_.png" % i)
            if not os.path.exists(src):
                print("MISSING source:", src); continue
            base = "%02d_%s" % (i, slug)
            dst_img = os.path.join(dst_dir, base + ".png")
            shutil.copy2(src, dst_img)
            with open(os.path.join(dst_dir, base + ".txt"), "w", encoding="utf-8") as f:
                f.write("%s, a man, %s\n" % (trig, cap))
            total += 1
    # verify
    for char in ("jaisal", "zidane"):
        d = os.path.join(DST, char)
        imgs = [f for f in os.listdir(d) if f.endswith(".png")]
        txts = [f for f in os.listdir(d) if f.endswith(".txt")]
        print(char, "->", len(imgs), "images,", len(txts), "captions")
    print("copied+captioned:", total)

if __name__ == "__main__":
    main()
