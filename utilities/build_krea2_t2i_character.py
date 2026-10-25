#!/usr/bin/env python
"""Build the Krea 2 TEXT-TO-IMAGE 1-click workflow (UI format).

Purpose: generate the character FROM SCRATCH with Krea 2 (maximum realism),
12 face candidates in one Run (PixaromaPromptEach) - 6 for the FULL-beard
character, 6 for the SHORT-patchy-beard character. Both lean-but-fit,
Kerala topical look, NOT well groomed. Pick the best face per character ->
those become the MASTER references for the identity-edit dataset.
Uses the Krea2-realism-V2 LoRA (RudySen) for photorealism + the FameGrid
Spice (iPhone look) LoRA for the natural phone-photo feel.

Chain:
  UNETLoader -> LoraLoaderModelOnly(Krea2-realism-V2 @1.0)
             -> LoraLoaderModelOnly(famegrid_spicy @0.7)
             -> KSampler -> VAEDecode -> SaveImage
  CLIPLoader -> CLIPTextEncode(positive, text from PixaromaPromptEach)
  CLIPLoader -> CLIPTextEncode(negative)
  EmptySD3LatentImage (1152x2048 portrait) -> KSampler
  PixaromaPromptEach.prompt -> positive encode text

No reference image, no identity LoRA - pure t2i.
"""
import json

OUT = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_character.json"

# Two characters (user 2026-10-08): both lean-but-fit (NOT bulky), both NOT
# well groomed, Kerala topical look.
CHAR_FULL = ("a 26-year-old Indian man from Kerala, short dark hair, a FULL "
             "unkempt beard (patchy, uneven, not well groomed), lean and fit "
             "build (NOT bulky, NOT muscular), wearing a plain dark t-shirt")
CHAR_SHORT = ("a 26-year-old Indian man from Kerala, short dark hair, a SHORT "
              "patchy beard (short length, sparse, not well groomed, not a "
              "full beard), lean and fit build (NOT bulky, NOT muscular), "
              "wearing a plain dark t-shirt")
REALISM = ("ONLY ONE character, no other people, no duplicates. Ultimate "
           "photorealism: real skin texture with visible pores and natural "
           "imperfections, realistic eyes with visible iris texture and "
           "catchlights, natural micro-expressions, lifelike and unposed, "
           "shot on a real camera, natural lighting, deep depth of field, "
           "no plastic skin, no airbrushing, no AI look, no waxy skin, "
           "no cartoon, no illustration, looks like a real photo someone "
           "already took.")
NEG = ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, "
       "3d render, cartoon, illustration, duplicate character, multiple "
       "people, watermark, logo, deformed face, bad eyes, extra fingers, "
       "bulky body, muscular, bodybuilder, clean-shaven, perfectly groomed "
       "beard")

CANDIDATES = [
    "A close-up headshot of {c}, frontal view, calm neutral expression, eyes looking directly at the camera. 85mm lens f/2.8, sharp focus on the eyes. Soft overcast daylight, plain muted background. {r}",
    "A three-quarter view of {c}, gentle natural smile, relaxed and candid. 85mm lens f/2.8. Warm golden-hour light from the side, soft background. {r}",
    "A true profile view of {c}, looking into the distance, thoughtful expression. 105mm telephoto f/4.0, compressed background. Moody overcast light. {r}",
    "A candid shot of {c} laughing naturally, head tilted slightly, eyes crinkled. 50mm f/2.0, bright daylight, outdoor street background. {r}",
    "A close-up of {c} looking slightly upward, eyes bright and curious, soft window light from the left. 85mm f/2.0, dim indoor background. {r}",
    "A full-body shot of {c} standing relaxed on a quiet street, weight on one leg, looking at the camera. 35mm f/4.0, head to toe, natural overcast daylight. {r}",
]
PROMPTS = ([s.format(c=CHAR_FULL, r=REALISM) for s in CANDIDATES]
           + [s.format(c=CHAR_SHORT, r=REALISM) for s in CANDIDATES])
assert len(PROMPTS) == 12

STATE = {
    "version": 2,
    "rows": [{"text": p, "enabled": True} for p in PROMPTS],
    "split": "line",
    "expand": True,
    "trim": True,
    "skipEmpty": True,
    "cap": 200,
    "wiredAt": "after",
}


def widget_input(name, type_="COMBO", link=None):
    return {"localized_name": name, "name": name, "type": type_,
            "widget": {"name": name}, "link": link}


def link_input(name, type_, link):
    return {"localized_name": name, "name": name, "type": type_, "link": link}


def out(name, type_, links):
    return {"localized_name": name, "name": name, "type": type_, "links": links}


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
    {"id": 82, "type": "EmptySD3LatentImage", "pos": [400, 350], "size": [320, 90], "flags": {}, "order": 4, "mode": 0,
     "inputs": [widget_input("width"), widget_input("height"), widget_input("batch_size")],
     "outputs": [out("LATENT", "LATENT", [8])],
     "properties": {"Node name for S&R": "EmptySD3LatentImage"},
     "widgets_values": [1152, 2048, 1]},
    # 200 PixaromaPromptEach (6 face candidates)
    {"id": 200, "type": "PixaromaPromptEach", "pos": [400, 470], "size": [420, 320], "flags": {}, "order": 5, "mode": 0,
     "inputs": [link_input("text", "STRING", None)],
     "outputs": [out("prompt", "STRING", [11]), out("index", "INT", None), out("total", "INT", None)],
     "properties": {"Node name for S&R": "PixaromaPromptEach", "promptEachState": STATE},
     "widgets_values": []},
    # 300 positive encode (text from PixaromaPromptEach)
    {"id": 300, "type": "CLIPTextEncode", "pos": [760, 220], "size": [400, 200], "flags": {}, "order": 6, "mode": 0,
     "inputs": [link_input("clip", "CLIP", 2), widget_input("text", "STRING", 11)],
     "outputs": [out("CONDITIONING", "CONDITIONING", [6])],
     "properties": {"Node name for S&R": "CLIPTextEncode"},
     "widgets_values": [""]},
    # 301 negative encode
    {"id": 301, "type": "CLIPTextEncode", "pos": [760, 460], "size": [400, 200], "flags": {}, "order": 7, "mode": 0,
     "inputs": [link_input("clip", "CLIP", 3), widget_input("text", "STRING")],
     "outputs": [out("CONDITIONING", "CONDITIONING", [7])],
     "properties": {"Node name for S&R": "CLIPTextEncode"},
     "widgets_values": [NEG]},
    # 53 KSampler
    {"id": 53, "type": "KSampler", "pos": [1120, 40], "size": [320, 160], "flags": {}, "order": 8, "mode": 0,
     "inputs": [link_input("model", "MODEL", 5), link_input("positive", "CONDITIONING", 6),
                link_input("negative", "CONDITIONING", 7), link_input("latent_image", "LATENT", 8),
                widget_input("seed"), widget_input("control_after_generate"), widget_input("steps"),
                widget_input("cfg"), widget_input("sampler_name"), widget_input("scheduler"),
                widget_input("denoise")],
     "outputs": [out("LATENT", "LATENT", [9])],
     "properties": {"Node name for S&R": "KSampler"},
     "widgets_values": [42, "randomize", 10, 1, "euler", "simple", 1]},
    # 54 VAEDecode
    {"id": 54, "type": "VAEDecode", "pos": [1480, 40], "size": [200, 60], "flags": {}, "order": 9, "mode": 0,
     "inputs": [link_input("samples", "LATENT", 9), link_input("vae", "VAE", 4)],
     "outputs": [out("IMAGE", "IMAGE", [10])],
     "properties": {"Node name for S&R": "VAEDecode"},
     "widgets_values": []},
    # 29 SaveImage
    {"id": 29, "type": "SaveImage", "pos": [1700, 40], "size": [320, 90], "flags": {}, "order": 10, "mode": 0,
     "inputs": [link_input("images", "IMAGE", 10), widget_input("filename_prefix")],
     "outputs": [out("images", "IMAGE", None)],
     "properties": {"Node name for S&R": "SaveImage"},
     "widgets_values": ["krea2_t2i_face"]},
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
    [10, 54, 0, 29, 0, "IMAGE"],
    [11, 200, 0, 300, 1, "STRING"],
    [12, 96, 0, 97, 0, "MODEL"],
]

wf = {
    "id": "krea2-t2i-character",
    "revision": 0,
    "last_node_id": 301,
    "last_link_id": 12,
    "nodes": nodes,
    "links": links,
    "groups": [],
    "config": {},
    "extra": {},
    "version": 0.4,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)
print("written:", OUT)
print("nodes:", len(nodes), "links:", len(links), "candidates:", len(PROMPTS))
