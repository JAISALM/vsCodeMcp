import json, io

POS = ("candid photorealistic photograph of the SAME man from the reference image - keep his face, hair and beard "
"EXACTLY identical to the reference, now standing on a narrow monsoon street in Kerala, light rain falling, wet "
"pavement, lush green palms, natural ambient light, realistic skin texture with visible pores and natural "
"imperfections, 85mm lens look, shallow depth of field, looks like a real photo someone took on their phone, "
"NOT a studio portrait, NOT a headshot")
NEG = ("painting, illustration, 3d render, cgi, cartoon, anime, plastic skin, waxy skin, airbrushed skin, overly "
"smooth skin, deformed face, wrong face, different person, bad eyes, extra fingers, malformed hands, text, words, "
"watermark, logo, studio lighting, posed portrait")

# --- link id plan ---
# 1  UNET(51)  -> KSampler(65).model
# 2  UNET(51)  -> KSampler(73).model
# 3  CLIP(52)  -> CLIPTextEncode(63).clip
# 4  CLIP(52)  -> CLIPTextEncode(64).clip
# 5  CLIP(52)  -> CLIPTextEncode(71).clip
# 6  CLIP(52)  -> CLIPTextEncode(72).clip
# 7  VAE(53)   -> VAEDecode(66).vae
# 8  VAE(53)   -> VAEDecode(74).vae
# 9  LoadImg(61) -> KSampler(65).latent_image
# 10 KSampler(65) -> VAEDecode(66).samples
# 11 VAEDecode(66) -> SaveImage(67).images
# 12 VAEDecode(66) -> Preview(68).images
# 13 CLIPTextEncode(63) -> KSampler(65).positive
# 14 CLIPTextEncode(64) -> KSampler(65).negative
# 15 LoadImg(62) -> KSampler(73).latent_image
# 16 KSampler(73) -> VAEDecode(74).samples
# 17 VAEDecode(74) -> SaveImage(75).images
# 18 VAEDecode(74) -> Preview(76).images
# 19 CLIPTextEncode(71) -> KSampler(73).positive
# 20 CLIPTextEncode(72) -> KSampler(73).negative

def clip_node(idn, pos, text, clip_link, cond_link):
    return {"id": idn, "type": "CLIPTextEncode", "pos": [pos[0], pos[1]], "size": [400, 200],
            "flags": {}, "order": 0, "mode": 0,
            "inputs": [
              {"localized_name": "clip", "name": "clip", "type": "CLIP", "widget": None, "link": clip_link},
              {"localized_name": "text", "name": "text", "type": "STRING", "widget": {"name": "text"}, "link": None}],
            "outputs": [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [cond_link], "slot_index": 0}],
            "properties": {"Node name for S&R": "CLIPTextEncode"}, "widgets_values": [text]}

def loadimg(idn, fname, pos, out_link):
    return {"id": idn, "type": "LoadImage", "pos": [pos[0], pos[1]], "size": [282, 322], "flags": {}, "order": 4, "mode": 0,
      "inputs": [
        {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
        {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None}],
      "outputs": [
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [out_link], "slot_index": 0},
        {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None, "slot_index": 0}],
      "properties": {"Node name for S&R": "LoadImage"}, "widgets_values": [fname, "image"]}

def ksampler(idn, pos, model_link, pos_link, neg_link, img_link, out_link):
    return {"id": idn, "type": "KSampler", "pos": [pos[0], pos[1]], "size": [300, 200], "flags": {}, "order": 0, "mode": 0,
      "inputs": [
        {"localized_name": "model", "name": "model", "type": "MODEL", "widget": None, "link": model_link},
        {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "widget": None, "link": pos_link},
        {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "widget": None, "link": neg_link},
        {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT_IMAGE", "widget": None, "link": img_link}],
      "outputs": [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [out_link], "slot_index": 0},
                  {"localized_name": "ALPHA", "name": "ALPHA", "type": "IMAGE", "links": None, "slot_index": 0}],
      "properties": {"Node name for S&R": "KSampler"},
      "widgets_values": [42, "randomize", 25, 1, "euler", "simple", 0.55]}

def vaedecode(idn, pos, samples_link, vae_link, out_links):
    return {"id": idn, "type": "VAEDecode", "pos": [pos[0], pos[1]], "size": [200, 100], "flags": {}, "order": 0, "mode": 0,
      "inputs": [{"localized_name": "samples", "name": "samples", "type": "LATENT_IMAGE", "widget": None, "link": samples_link},
                 {"localized_name": "vae", "name": "vae", "type": "VAE", "widget": None, "link": vae_link}],
      "outputs": [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": out_links, "slot_index": 0}],
      "properties": {"Node name for S&R": "VAEDecode"}, "widgets_values": []}

def saveimage(idn, pos, img_link, prefix):
    return {"id": idn, "type": "SaveImage", "pos": [pos[0], pos[1]], "size": [300, 250], "flags": {}, "order": 0, "mode": 0,
      "inputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "widget": None, "link": img_link},
                 {"localized_name": "filename_prefix", "name": "filename_prefix", "type": "STRING", "widget": {"name": "filename_prefix"}, "link": None}],
      "outputs": [], "properties": {"Node name for S&R": "SaveImage"}, "widgets_values": [prefix]}

def preview(idn, pos, img_link):
    return {"id": idn, "type": "PreviewImage", "pos": [pos[0], pos[1]], "size": [300, 240], "flags": {}, "order": 0, "mode": 0,
      "inputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "widget": None, "link": img_link}],
      "outputs": [], "properties": {"Node name for S&R": "PreviewImage"}, "widgets_values": []}

nodes = []
nodes.append({"id": 51, "type": "UNETLoader", "pos": [50, 60], "size": [300, 100], "flags": {}, "order": 1, "mode": 0,
  "inputs": [], "outputs": [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [1, 2], "slot_index": 0}],
  "properties": {"Node name for S&R": "UNETLoader"}, "widgets_values": ["qwen_image_2.1_bf16.safetensors", "default"]})
nodes.append({"id": 52, "type": "CLIPLoader", "pos": [50, 190], "size": [300, 130], "flags": {}, "order": 2, "mode": 0,
  "inputs": [], "outputs": [{"localized_name": "CLIP", "name": "CLIP", "type": "CLIP", "links": [3, 4, 5, 6], "slot_index": 0}],
  "properties": {"Node name for S&R": "CLIPLoader"}, "widgets_values": ["qwen3vl_8b_fp8_scaled.safetensors", "qwen_image", "default"]})
nodes.append({"id": 53, "type": "VAELoader", "pos": [50, 350], "size": [300, 80], "flags": {}, "order": 3, "mode": 0,
  "inputs": [], "outputs": [{"localized_name": "VAE", "name": "VAE", "type": "VAE", "links": [7, 8], "slot_index": 0}],
  "properties": {"Node name for S&R": "VAELoader"}, "widgets_values": ["qwen_image_2.1_vae_bf16.safetensors"]})
nodes.append(loadimg(61, "jaisal_face_frontal.png", [420, 60], 9))
nodes.append(loadimg(62, "zidane_face_frontal.png", [420, 480], 15))
nodes.append(clip_node(63, [760, 60], POS, 3, 13))
nodes.append(clip_node(64, [760, 280], NEG, 4, 14))
nodes.append(ksampler(65, [1140, 60], 1, 13, 14, 9, 10))
nodes.append(vaedecode(66, [1480, 60], 10, 7, [11, 12]))
nodes.append(saveimage(67, [1700, 60], 11, "qwen21_face_JAISAL"))
nodes.append(preview(68, [1700, 330], 12))
nodes.append(clip_node(71, [760, 480], POS, 5, 19))
nodes.append(clip_node(72, [760, 700], NEG, 6, 20))
nodes.append(ksampler(73, [1140, 480], 2, 19, 20, 15, 16))
nodes.append(vaedecode(74, [1480, 480], 16, 8, [17, 18]))
nodes.append(saveimage(75, [1700, 480], 17, "qwen21_face_ZIDANE"))
nodes.append(preview(76, [1700, 750], 18))

links = []
def L(lid, fn, fs, tn, ts, ltype):
    links.append([lid, fn, fs, tn, ts, ltype])

L(1, 51, 0, 65, 0, "MODEL"); L(2, 51, 0, 73, 0, "MODEL")
L(3, 52, 0, 63, 0, "CLIP"); L(4, 52, 0, 64, 0, "CLIP")
L(5, 52, 0, 71, 0, "CLIP"); L(6, 52, 0, 72, 0, "CLIP")
L(7, 53, 0, 66, 1, "VAE"); L(8, 53, 0, 74, 1, "VAE")
L(9, 61, 0, 65, 3, "IMAGE"); L(10, 65, 0, 66, 0, "LATENT_IMAGE"); L(11, 66, 0, 67, 0, "IMAGE"); L(12, 66, 0, 68, 0, "IMAGE")
L(13, 63, 0, 65, 1, "CONDITIONING"); L(14, 64, 0, 65, 2, "CONDITIONING")
L(15, 62, 0, 73, 3, "IMAGE"); L(16, 73, 0, 74, 0, "LATENT_IMAGE"); L(17, 74, 0, 75, 0, "IMAGE"); L(18, 74, 0, 76, 0, "IMAGE")
L(19, 71, 0, 73, 1, "CONDITIONING"); L(20, 72, 0, 73, 2, "CONDITIONING")

out = {"id": "qwen21_face_test", "last_node_id": 76, "last_link_id": 20,
       "nodes": nodes, "links": links, "version": 400}
path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\qwen21_face_test.json"
with io.open(path, "w", encoding="utf-8") as f:
    f.write(json.dumps(out, indent=1))
print("WROTE", path, "nodes:", len(nodes), "links:", len(links))
