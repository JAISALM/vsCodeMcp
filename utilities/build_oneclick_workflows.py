"""Build Krea2 Film Studio one-click movie-shot workflows from the pack's SHIPPED V.01 template.

Template: custom_nodes\\ComfyUI-Krea2-FilmStudio-Vionex\\workflows\\Vionex - Krea 2 Film (V.01).json
Node 13 = Krea2OneNode (single JSON config widget). We fill the config with per-character,
per-scene settings; the pack's own expansion code carries the sampler/VAE/LoRA wiring.

Usage:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" build_oneclick_workflows.py

Outputs (user\\default\\workflows\\):
  k2f_<char>_<scene>_16x9_oneclick.json

NO RUNS — D192: agent builds + validates only; the USER queues these after the shared
ComfyUI restart (loads the FilmStudio pack).
"""
import json
import os

BASE_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"
TEMPLATE = os.path.join(BASE_DIR, r"custom_nodes\ComfyUI-Krea2-FilmStudio-Vionex\workflows\Vionex - Krea 2 Film (V.01).json")
OUT_DIR = os.path.join(BASE_DIR, r"user\default\workflows")

PROMPTS = {
    "S1_paddy": (
        "place him in a flooded paddy field in Kerala after harvest - golden rice stubble, "
        "standing water, light rain falling, a farmer with a hat bending in the far distance. "
        "Dusk, overcast moody light, soft natural light on his face."
    ),
    "S2_house": (
        "place him behind a normal Kerala house - whitewashed walls, sloping clay-tile roof, "
        "coconut palms, a narrow dirt lane, clay pots, lush greenery around. Early morning, "
        "soft overcast light, soft natural light on his face."
    ),
    "S3_interior": (
        "place him inside a normal Kerala home - dark wooden beams, a brass kettuvilakku oil "
        "lamp, an open wooden window with lush greenery outside, natural window light falling "
        "on him. Warm moody interior light."
    ),
    "S4_bike": (
        "place him sitting on a classic Kerala motorcycle on a rural red laterite road - "
        "coconut palm-lined road, paddy fields on both sides, distant homes. Late afternoon "
        "golden light."
    ),
    "S5_7s_ground": (
        "place him on a minimal local 7-a-side football ground - a small grassy patch, small "
        "metal-frame goals, a low fence, a wooden bench, a worn football. Evening light."
    ),
    "S6_village": (
        "place him in a rural Kerala village - paddy fields, scattered homes with clay-tile "
        "roofs, coconut palms, a red laterite lane. Dusk, overcast moody light, soft natural "
        "light on his face."
    ),
}

IDENTITY = {
    "jaisal": (
        "Keep the man's face, medium wavy black hair (falling to eyebrow length), his "
        "naturally CROOKED bent nose, identity, slim build, and plain black t-shirt EXACTLY "
        "the same as the reference image. Change ONLY the setting: "
    ),
    "zidhan": (
        "Keep the man's rounder face, his SHARP ANGULAR prominent nose, his FULL short dense "
        "beard, short neat black hair, identity, and plain white t-shirt EXACTLY the same as "
        "the reference image. Change ONLY the setting: "
    ),
}

REF_FILE = {
    "jaisal": "jaisal_final_ref.png",
    "zidhan": "zidhan_final_ref.png",
}

NEGATIVE = (
    "low quality, blurry, pixelated, bad anatomy, deformed body, extra limbs, malformed hands, "
    "extra fingers, distorted face, asymmetrical eyes, duplicate subjects, warped background, "
    "incorrect perspective, cropped limbs, plastic skin, unrealistic lighting, oversaturated, "
    "text, watermark, logo, CGI, cartoon, motion blur, flicker, jitter, morphing, "
    "temporal inconsistency"
)

SEEDS = {
    ("jaisal", "S1_paddy"): 90201,
    ("jaisal", "S2_house"): 90202,
    ("jaisal", "S3_interior"): 90203,
    ("jaisal", "S4_bike"): 90204,
    ("jaisal", "S5_7s_ground"): 90205,
    ("jaisal", "S6_village"): 90206,
    ("zidhan", "S1_paddy"): 90301,
}


def make_config(char: str, scene: str) -> dict:
    return {
        "version": 4,
        "mode": "i2i",
        "preset": "Fast",
        "prompt": IDENTITY[char] + PROMPTS[scene] +
        " Cinematic 35mm movie still, shallow depth of field, photorealistic, natural color "
        "grade, no text, no watermark.",
        "negative_prompt": NEGATIVE,
        "width": 1928, "height": 1088, "alignment": 8, "aspect_ratio": "16:9",
        "megapixels": 2.0, "custom_resolution": True,
        "batch_size": 1,
        "steps": 8, "cfg": 1.0,
        "seed": SEEDS[(char, scene)], "randomize_seed": False,
        "sampler": "euler", "scheduler": "simple", "denoise": 1.0,
        "res4lyf": {"enabled": True},
        "gguf": {"enabled": False, "model": "", "clip_enabled": False, "clip": ""},
        "model": "krea2_turbo_bf16.safetensors",
        "clip": "qwen3vl_4b_fp8_scaled.safetensors",
        "vae": "wan_2.1_vae.safetensors",
        "weight_dtype": "default", "clip_device": "default",
        "loras": [
            {"name": "Krea 2\\canon_krea2.safetensors", "strength_model": 1,
             "strength_clip": 1, "enabled": True, "managed": True},
            {"name": "Krea 2\\cinematic_movie_still_krea2.safetensors", "strength_model": 1,
             "strength_clip": 1, "enabled": True, "managed": True},
        ],
        "dismissed_managed_loras": [],
        "advanced": True, "auto_save": True, "save_path": "",
        "scroll_zoom": False, "compare_enabled": False,
        "cinematic_style": "",
        "reference_downscale_mp": 1.0,
        "vae_decode": {"mode": "auto", "tile_size": 512, "overlap": 64},
        "refinement": {"enabled": True, "steps": 3, "cfg": 1.0, "sampler": "euler",
                       "scheduler": "simple", "denoise": 0.27},
        "diversity": {"enabled": False, "strength": 0.08, "eta": 0.75},
        "enhancer": {"enabled": False, "behavior": "balanced", "max_length": 256,
                     "temperature": 0.7, "top_k": 64, "top_p": 0.95,
                     "repetition_penalty": 1.05, "seed": 0, "thinking": False},
        "i2i": {"pipeline": "identity_edit", "denoise": 0.65, "fit_mode": "fit",
                "identity_lora": "", "ref_boost": 4.0, "ref_boost_a": 1.0,
                "grounding_px": 768},
        "multi_reference": {
            "vision_megapixels": 0.3, "vision_position": "before prompt",
            "system_prompt": "Study every numbered reference image, preserve the requested "
            "identity, object, wardrobe, style, lighting, and environment cues, then combine "
            "them into one coherent new shot that follows the user's spatial instructions. "
            "Treat Image N and Picture N as the same reference."},
        "control": {"lora": "", "strength": 1.0, "resize": "match_latent_size",
                    "upscale_method": "lanczos", "crop": "center", "channel_mode": "rgb",
                    "normalize": "none", "invert": False, "preprocessor": "none",
                    "preprocessor_resolution": 1024},
        "external": {"model": False, "clip": False, "vae": False},
        "uploads": {"image": REF_FILE[char], "image_2": "", "image_3": "", "image_4": ""},
        "stats": {"images_generated": 0, "renders_completed": 0, "total_render_ms": 0.0,
                  "last_render_ms": 0.0, "last_batch": 0, "last_completed_at": ""},
    }


def main():
    template = json.load(open(TEMPLATE, encoding="utf-8"))
    jobs = [
        ("jaisal", "S1_paddy"), ("jaisal", "S2_house"), ("jaisal", "S3_interior"),
        ("jaisal", "S4_bike"), ("jaisal", "S5_7s_ground"), ("jaisal", "S6_village"),
        ("zidhan", "S1_paddy"),
    ]
    for char, scene in jobs:
        d = json.loads(json.dumps(template))  # deep copy
        n13 = [n for n in d["nodes"] if n["type"] == "Krea2OneNode"][0]
        n13["widgets_values"] = [json.dumps(make_config(char, scene), ensure_ascii=False)]
        for n in d["nodes"]:
            if n.get("pos"):
                n["pos"] = [0, 0] if n["id"] == 13 else [0, 1200]
        out = os.path.join(OUT_DIR, f"k2f_{char}_{scene}_16x9_oneclick.json")
        json.dump(d, open(out, "w", encoding="utf-8"), indent=1)
        print("WROTE", out)


if __name__ == "__main__":
    main()
