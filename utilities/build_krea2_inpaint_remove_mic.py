r"""Build krea2_inpaint_remove_mic.json — remove the EXTRA black mic from the
small-mic identity-edit output (mic_small_id_00001_.png), keep the small silver
mic on the short stand.

Mechanism (D096 update 5 — proven): LoadImage(base) + LoadImage(mask) ->
VAEEncode -> SetLatentNoiseMask -> KSampler -> VAEDecode -> SaveImage.
SetLatentNoiseMask restricts regeneration to the masked region; everything
outside stays pixel-identical.

USER DRAWS THE MASK: white = the extra black mic (head + stand + base + its
shadow), black = everything else. Mask MUST be the same size as the base
image (1920x1088). Save it to input\ as remove_mic_mask.png (or pick any
mask file in the LoadImage node).

Run:
  & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\build_krea2_inpaint_remove_mic.py"
"""
import json
import os

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
IN_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
OUT_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_cut"

BASE_IMG = "mic_small_id_00001_.png"   # the identity-edit output with 2 mics
MASK_IMG = "remove_mic_mask.png"       # user-drawn mask (white = extra black mic)

POS = ("Remove the extra black microphone on the left side of the table. "
       "Keep ONLY the small silver microphone on its short low stand, exactly as it is. "
       "The area where the black microphone was becomes plain empty weathered wooden table "
       "surface, matching the surrounding wood grain and lighting exactly. "
       "Keep everything else in the scene exactly the same: the wooden table, the empty chair, "
       "the floating sheets of paper, the bare bulb, the pure black void background. "
       "Black-and-white high-contrast cinematic style, fine film grain.")
NEG = ("microphone, mics, two microphones, extra microphone, black microphone, mic stand, "
       "large microphone, tall stand, broadcast mic, color, any color, people, a person, a boy, "
       "extra objects, text, watermark, glowing effects, holograms, fire, smoke")


def combo_input(name, link=None):
    wtype = "IMAGEUPLOAD" if name == "upload" else "COMBO"
    loc = "choose file to upload" if name == "upload" else name
    return {"localized_name": loc, "name": name, "type": wtype,
            "widget": {"name": name}, "link": link}


# Exact data types from the native v3 file (converter is picky about these)
IN_TYPES = {"pixels": "IMAGE", "vae": "VAE", "samples": "LATENT", "mask": "MASK",
            "model": "MODEL", "positive": "CONDITIONING", "negative": "CONDITIONING",
            "latent_image": "LATENT", "images": "IMAGE", "clip": "CLIP"}
OUT_TYPES = {"IMAGE": "IMAGE", "MASK": "MASK", "MODEL": "MODEL", "CLIP": "CLIP",
             "VAE": "VAE", "CONDITIONING": "CONDITIONING", "LATENT": "LATENT",
             "images": "IMAGE"}


def link_input(name, link):
    return {"localized_name": name, "name": name, "type": IN_TYPES[name], "link": link}


def out(name, links):
    return {"localized_name": name, "name": name, "type": OUT_TYPES[name], "links": links}


def node(id, ntype, pos, size, order, inputs, outputs, widgets, props=None):
    n = {"id": id, "type": ntype, "pos": pos, "size": size, "flags": {},
         "order": order, "mode": 0, "inputs": inputs, "outputs": outputs,
         "properties": props or {"Node name for S&R": ntype},
         "widgets_values": widgets}
    return n


def text_input():
    return {"localized_name": "text", "name": "text", "type": "STRING",
            "widget": {"name": "text"}, "link": None}


def widget_input(name, wtype):
    return {"localized_name": name, "name": name, "type": wtype,
            "widget": {"name": name}, "link": None}


nodes = [
    # 1: base image (the 2-mic identity-edit output)
    node(1, "LoadImage", [40, 200], [300, 320], 0,
         [combo_input("image"), combo_input("upload")],
         [out("IMAGE", [101]), out("MASK", None)],
         [BASE_IMG, "image"]),
    # 2: user-drawn mask (white = extra black mic)
    node(2, "LoadImage", [40, 560], [300, 320], 1,
         [combo_input("image"), combo_input("upload")],
         [out("IMAGE", None), out("MASK", [102])],
         [MASK_IMG, "image"]),
    # 3-5: loaders (same Krea2 stack as the proven v3 inpaint)
    node(3, "UNETLoader", [40, 920], [320, 80], 2,
         [combo_input("unet_name"), combo_input("weight_dtype")],
         [out("MODEL", [103])],
         ["krea2_turbo_bf16.safetensors", "default"]),
    node(4, "CLIPLoader", [40, 1040], [320, 100], 3,
         [combo_input("clip_name"), combo_input("type"), combo_input("device")],
         [out("CLIP", [104, 105])],
         ["qwen3vl_4b_bf16.safetensors", "krea2", "default"]),
    node(5, "VAELoader", [40, 1180], [320, 60], 4,
         [combo_input("vae_name")],
         [out("VAE", [106, 107])],
         ["qwen_image_vae.safetensors"]),
    # 6-7: prompts (text widget = type STRING, matching native)
    node(6, "CLIPTextEncode", [420, 200], [400, 260], 5,
         [link_input("clip", 104), text_input()],
         [out("CONDITIONING", [108])],
         [POS]),
    node(7, "CLIPTextEncode", [420, 520], [400, 260], 6,
         [link_input("clip", 105), text_input()],
         [out("CONDITIONING", [109])],
         [NEG]),
    # 8-9: encode + noise mask (the true-inpaint mechanism)
    node(8, "VAEEncode", [420, 840], [340, 100], 7,
         [link_input("pixels", 101), link_input("vae", 106)],
         [out("LATENT", [110])],
         []),
    node(9, "SetLatentNoiseMask", [420, 980], [340, 80], 8,
         [link_input("samples", 110), link_input("mask", 102)],
         [out("LATENT", [111])],
         []),
    # 10: sampler (native 7-value shape incl. hidden randomize; widget types match native)
    node(10, "KSampler", [860, 400], [320, 260], 9,
         [link_input("model", 103), link_input("positive", 108),
          link_input("negative", 109), link_input("latent_image", 111),
          widget_input("seed", "INT"), widget_input("steps", "INT"),
          widget_input("cfg", "FLOAT"), widget_input("sampler_name", "COMBO"),
          widget_input("scheduler", "COMBO"), widget_input("denoise", "FLOAT")],
         [out("LATENT", [112]), out("IMAGE", None)],
         [123456789, "randomize", 8, 1.0, "euler", "simple", 1.0]),
    # 11-12: decode + save
    node(11, "VAEDecode", [1220, 400], [220, 60], 10,
         [link_input("samples", 112), link_input("vae", 107)],
         [out("IMAGE", [113])],
         []),
    node(12, "SaveImage", [1460, 400], [320, 240], 11,
         [link_input("images", 113)],
         [out("images", None)],
         ["jaisal_cut/mic_single"]),
]

links = [
    [101, 1, 0, 8, 0, "IMAGE"],
    [102, 2, 1, 9, 1, "MASK"],
    [103, 3, 0, 10, 0, "MODEL"],
    [104, 4, 0, 6, 0, "CLIP"],
    [105, 4, 0, 7, 0, "CLIP"],
    [106, 5, 0, 8, 1, "VAE"],
    [107, 5, 0, 11, 1, "VAE"],
    [108, 6, 0, 10, 1, "CONDITIONING"],
    [109, 7, 0, 10, 2, "CONDITIONING"],
    [110, 8, 0, 9, 0, "LATENT"],
    [111, 9, 0, 10, 3, "LATENT"],
    [112, 10, 0, 11, 0, "LATENT"],
    [113, 11, 0, 12, 0, "IMAGE"],
]

wf = {"id": "krea2-inpaint-remove-mic", "version": 0.4,
      "last_node_id": 12, "last_link_id": 113,
      "nodes": nodes, "links": links}

out_path = os.path.join(WF_DIR, "krea2_inpaint_remove_mic.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(wf, f, indent=1, ensure_ascii=False)
print("WROTE", out_path)

# Stage the base image into input\ (workflows load from there)
src = os.path.join(OUT_DIR, BASE_IMG)
dst = os.path.join(IN_DIR, BASE_IMG)
if os.path.exists(src) and not os.path.exists(dst):
    import shutil
    shutil.copy2(src, dst)
    print("STAGED", dst)
elif os.path.exists(dst):
    print("ALREADY STAGED", dst)
else:
    print("WARN: base image not found at", src)

# Placeholder mask (same size as base) so the LoadImage node has a valid file.
# USER REPLACES THIS with their hand-drawn mask (white = extra black mic).
try:
    from PIL import Image
    base = Image.open(os.path.join(IN_DIR, BASE_IMG))
    w, h = base.size
    mask_path = os.path.join(IN_DIR, MASK_IMG)
    if not os.path.exists(mask_path):
        Image.new("L", (w, h), 0).save(mask_path)
        print("PLACEHOLDER MASK (all black) at", mask_path,
              f"({w}x{h}) — DRAW white over the extra black mic, save over this file")
    else:
        print("MASK ALREADY EXISTS", mask_path)
except Exception as e:
    print("MASK NOTE:", e)
