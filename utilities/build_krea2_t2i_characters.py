#!/usr/bin/env python
"""Build TWO Krea 2 TEXT-TO-IMAGE 1-click workflows (UI format), one per character.

User feedback (2026-10-08, 2nd round):
- Previous run still looked PLASTIC / STOCK-PHOTO / "average AI look".
- Root cause: the prompts were POSED STUDIO HEADSHOTS ("85mm f/2.8, sharp focus
  on the eyes, plain muted background") + over-emphasized "ultimate photorealism"
  -> the model renders a hyper-perfect, airbrushed, stock-photo face.
- Fix: CANDID, ENVIRONMENTAL, PHONE-SHOT framing in real Kerala settings
  (backwaters, monsoon, temple, houseboat, coconut grove, auto-rickshaw,
  college, village). No lens specs, no "plain background", no posed headshots.
- Hair (user): Char 1 = MEDIUM WAVY hair (loose, messy). Char 2 = LONG hair
  tied up in a loose man-bun / topknot (Gareth Bale 2018 style).
- The "Kerala touch" comes from the ENVIRONMENTS + physical features (warm
  medium-brown skin) + hair/beard - NOT from naming "Kerala" or any actor.

LoRA stack: UNET krea2_turbo_fp8_scaled -> Krea2-realism-V2 @1.0 (node 96)
-> famegrid_spicy (iPhone look) @0.7 (node 97) -> KSampler -> VAEDecode -> SaveImage.

Outputs:
  krea2_t2i_char1.json  - Character 1: medium wavy hair, FULL unkempt beard, round face
  krea2_t2i_char2.json  - Character 2: long hair tied up (man-bun), SHORT patchy beard, angular face
"""
import json

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

# --- shared prompt pieces -------------------------------------------------
YOUTH = ("He looks like he is in his mid-20s: youthful fresh face, smooth "
         "young skin, no wrinkles, no aging, no grey hair, young energetic "
         "look.")
CANDID = ("candid unposed snapshot caught in a real moment, NOT a posed "
          "studio portrait, NOT a headshot, natural ambient light, real "
          "environmental background, looks like a real photo someone took on "
          "their phone, slight natural imperfections, a real ordinary person, "
          "not a model, not a celebrity, not a stock photo, not a professional "
          "photo.")
NEG = ("studio portrait, posed, plain background, headshot, stock photo, "
       "professional photography, model, celebrity, shallow depth of field, "
       "bokeh, airbrushed, plastic, waxy skin, hyper-realistic, over-processed, "
       "AI look, generic AI face, western features, older man, 30s, 40s, 50s, "
       "aged face, mature face, grey hair, bulky body, muscular, bodybuilder, "
       "clean-shaven, perfectly groomed beard, duplicate character, multiple "
       "people, watermark, logo, deformed face, bad eyes, extra fingers")

# --- the TWO distinct characters (more hair per user) ----------------------
CHAR1 = ("a 26-year-old young Indian man with a round soft face, MEDIUM-LENGTH "
         "WAVY dark hair (loose, natural, a bit messy, NOT a short haircut), a "
         "FULL unkempt beard (patchy, uneven, not well groomed), lean and fit "
         "build (NOT bulky, NOT muscular), warm medium-brown natural skin, "
         "wearing a plain dark t-shirt")
CHAR2 = ("a 26-year-old young Indian man with an angular face and a defined "
         "jawline, LONG dark hair tied up in a loose man-bun / topknot (a young "
         "man who grows his hair out, natural, not styled), a SHORT patchy "
         "beard (short length, sparse, not well groomed, NOT a full beard), "
         "lean and fit build (NOT bulky, NOT muscular), warm medium-brown "
         "natural skin, wearing a plain white t-shirt")

# --- CANDID ENVIRONMENTAL shots (Kerala settings, no posed headshots) ------
CANDIDATES = [
    "A candid snapshot of {c} walking along a narrow backwater path, monsoon mist in the air, seen from behind at a slight angle, not looking at the camera. {y} {cand}",
    "A candid shot of {c} sitting on a wooden houseboat, looking out at the calm backwater, relaxed and natural. {y} {cand}",
    "A candid shot of {c} standing in a light monsoon rain on a small street, hair and beard a little wet, candid expression. {y} {cand}",
    "A candid shot of {c} walking through a college campus, mid-stride, looking ahead, natural. {y} {cand}",
    "A candid shot of {c} standing near an old temple wall, looking off to the side, thoughtful, soft natural light. {y} {cand}",
    "A candid shot of {c} sitting in the back of an auto-rickshaw, looking out the side, candid. {y} {cand}",
]

CHARACTERS = [
    ("krea2_t2i_char1", CHAR1, "krea2_char1_face"),
    ("krea2_t2i_char2", CHAR2, "krea2_char2_face"),
]


def widget_input(name, type_="COMBO", link=None):
    return {"localized_name": name, "name": name, "type": type_,
            "widget": {"name": name}, "link": link}


def link_input(name, type_, link):
    return {"localized_name": name, "name": name, "type": type_, "link": link}


def out(name, type_, links):
    return {"localized_name": name, "name": name, "type": type_, "links": links}


def build_wf(wf_id, char, prefix):
    prompts = [s.format(c=char, y=YOUTH, cand=CANDID) for s in CANDIDATES]
    state = {
        "version": 2,
        "rows": [{"text": p, "enabled": True} for p in prompts],
        "split": "line",
        "expand": True,
        "trim": True,
        "skipEmpty": True,
        "cap": 200,
        "wiredAt": "after",
    }
    nodes = [
        # 55 UNETLoader
        {"id": 55, "type": "UNETLoader", "pos": [40, 40], "size": [320, 70], "flags": {}, "order": 0, "mode": 0,
         "inputs": [widget_input("unet_name"), widget_input("weight_dtype")],
         "outputs": [out("MODEL", "MODEL", [1])],
         "properties": {"Node name for S&R": "UNETLoader"},
         "widgets_values": ["krea2_turbo_fp8_scaled.safetensors", "default"]},
        # 56 CLIPLoader
        {"id": 56, "type": "CLIPLoader", "pos": [40, 140], "size": [320, 100], "flags": {}, "order": 1, "mode": 0,
         "inputs": [widget_input("clip_name"), widget_input("type"), widget_input("device")],
         "outputs": [out("CLIP", "CLIP", [2, 3])],
         "properties": {"Node name for S&R": "CLIPLoader"},
         "widgets_values": ["qwen3vl_4b_fp8_scaled.safetensors", "krea2", "default"]},
        # 57 VAELoader
        {"id": 57, "type": "VAELoader", "pos": [40, 260], "size": [320, 50], "flags": {}, "order": 2, "mode": 0,
         "inputs": [widget_input("vae_name")],
         "outputs": [out("VAE", "VAE", [4])],
         "properties": {"Node name for S&R": "VAELoader"},
         "widgets_values": ["qwen_image_vae.safetensors"]},
        # 96 Krea2-realism-V2 LoRA (RudySen)
        {"id": 96, "type": "LoraLoaderModelOnly", "pos": [400, 40], "size": [320, 80], "flags": {}, "order": 3, "mode": 0,
         "inputs": [link_input("model", "MODEL", 1), widget_input("lora_name"), widget_input("strength_model")],
         "outputs": [out("MODEL", "MODEL", [12])],
         "properties": {"Node name for S&R": "LoraLoaderModelOnly"},
         "widgets_values": ["Krea2-realism-V2.safetensors", 1.0]},
        # 97 FameGrid Spice (iPhone look) LoRA, chained after 96
        {"id": 97, "type": "LoraLoaderModelOnly", "pos": [400, 140], "size": [320, 80], "flags": {}, "order": 4, "mode": 0,
         "inputs": [link_input("model", "MODEL", 12), widget_input("lora_name"), widget_input("strength_model")],
         "outputs": [out("MODEL", "MODEL", [5])],
         "properties": {"Node name for S&R": "LoraLoaderModelOnly"},
         "widgets_values": ["famegrid_spicy_3167060.safetensors", 0.7]},
        # 82 EmptySD3LatentImage (portrait 1152x2048)
        {"id": 82, "type": "EmptySD3LatentImage", "pos": [400, 350], "size": [320, 90], "flags": {}, "order": 5, "mode": 0,
         "inputs": [widget_input("width"), widget_input("height"), widget_input("batch_size")],
         "outputs": [out("LATENT", "LATENT", [8])],
         "properties": {"Node name for S&R": "EmptySD3LatentImage"},
         "widgets_values": [1152, 2048, 1]},
        # 200 PixaromaPromptEach (6 face candidates)
        {"id": 200, "type": "PixaromaPromptEach", "pos": [400, 470], "size": [420, 320], "flags": {}, "order": 6, "mode": 0,
         "inputs": [link_input("text", "STRING", None)],
         "outputs": [out("prompt", "STRING", [11]), out("index", "INT", None), out("total", "INT", None)],
         "properties": {"Node name for S&R": "PixaromaPromptEach", "promptEachState": state},
         "widgets_values": []},
        # 300 positive encode (text from PixaromaPromptEach)
        {"id": 300, "type": "CLIPTextEncode", "pos": [760, 220], "size": [400, 200], "flags": {}, "order": 7, "mode": 0,
         "inputs": [link_input("clip", "CLIP", 2), widget_input("text", "STRING", 11)],
         "outputs": [out("CONDITIONING", "CONDITIONING", [6])],
         "properties": {"Node name for S&R": "CLIPTextEncode"},
         "widgets_values": [""]},
        # 301 negative encode
        {"id": 301, "type": "CLIPTextEncode", "pos": [760, 460], "size": [400, 200], "flags": {}, "order": 8, "mode": 0,
         "inputs": [link_input("clip", "CLIP", 3), widget_input("text", "STRING")],
         "outputs": [out("CONDITIONING", "CONDITIONING", [7])],
         "properties": {"Node name for S&R": "CLIPTextEncode"},
         "widgets_values": [NEG]},
        # 53 KSampler
        {"id": 53, "type": "KSampler", "pos": [1120, 40], "size": [320, 160], "flags": {}, "order": 9, "mode": 0,
         "inputs": [link_input("model", "MODEL", 5), link_input("positive", "CONDITIONING", 6),
                    link_input("negative", "CONDITIONING", 7), link_input("latent_image", "LATENT", 8),
                    widget_input("seed"), widget_input("control_after_generate"), widget_input("steps"),
                    widget_input("cfg"), widget_input("sampler_name"), widget_input("scheduler"),
                    widget_input("denoise")],
         "outputs": [out("LATENT", "LATENT", [9])],
         "properties": {"Node name for S&R": "KSampler"},
         "widgets_values": [42, "randomize", 10, 1, "euler", "simple", 1]},
        # 54 VAEDecode
        {"id": 54, "type": "VAEDecode", "pos": [1480, 40], "size": [200, 60], "flags": {}, "order": 10, "mode": 0,
         "inputs": [link_input("samples", "LATENT", 9), link_input("vae", "VAE", 4)],
         "outputs": [out("IMAGE", "IMAGE", [10])],
         "properties": {"Node name for S&R": "VAEDecode"},
         "widgets_values": []},
        # 302 FameGrid Color Finish (the missing finishing node from the
        # Reddit release - applies the color/detail recipe that made the
        # sample images look good). color_strength 1.0, sharpen 0.6.
        {"id": 302, "type": "FameGridColorFinish", "pos": [1480, 140], "size": [240, 90], "flags": {}, "order": 11, "mode": 0,
         "inputs": [link_input("image", "IMAGE", 10), widget_input("color_strength"), widget_input("sharpen_strength")],
         "outputs": [out("image", "IMAGE", [13])],
         "properties": {"Node name for S&R": "FameGridColorFinish"},
         "widgets_values": [1.0, 0.6]},
        # 29 SaveImage
        {"id": 29, "type": "SaveImage", "pos": [1700, 40], "size": [320, 90], "flags": {}, "order": 12, "mode": 0,
         "inputs": [link_input("images", "IMAGE", 13), widget_input("filename_prefix")],
         "outputs": [out("images", "IMAGE", None)],
         "properties": {"Node name for S&R": "SaveImage"},
         "widgets_values": [prefix]},
    ]
    links = [
        [1, 55, 0, 96, 0, "MODEL"],
        [2, 56, 0, 300, 0, "CLIP"],
        [3, 56, 0, 301, 0, "CLIP"],
        [4, 57, 0, 54, 1, "VAE"],
        [5, 97, 0, 53, 0, "MODEL"],
        [6, 300, 0, 53, 1, "CONDITIONING"],
        [7, 301, 0, 53, 2, "CONDITIONING"],
        [8, 82, 0, 53, 3, "LATENT"],
        [9, 53, 0, 54, 0, "LATENT"],
        [10, 54, 0, 302, 0, "IMAGE"],
        [11, 200, 0, 300, 1, "STRING"],
        [12, 96, 0, 97, 0, "MODEL"],
        [13, 302, 0, 29, 0, "IMAGE"],
    ]
    wf = {
        "id": wf_id,
        "revision": 0,
        "last_node_id": 302,
        "last_link_id": 13,
        "nodes": nodes,
        "links": links,
        "groups": [],
        "config": {},
        "extra": {},
        "version": 0.4,
    }
    path = f"{WF_DIR}\\{wf_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(wf, f, indent=2, ensure_ascii=False)
    print("written:", path, "| nodes:", len(nodes), "| candidates:", len(prompts))


for wf_id, char, prefix in CHARACTERS:
    build_wf(wf_id, char, prefix)
print("done: 2 workflows (candid environmental framing)")
