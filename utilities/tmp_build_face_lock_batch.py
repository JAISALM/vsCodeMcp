import json, io, copy

src = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock.json", encoding="utf-8"))
shapes = {}
for n in src["nodes"]:
    if n["type"] not in shapes:
        shapes[n["type"]] = n

def shape(t, nid, pos, widgets):
    n = copy.deepcopy(shapes[t])
    n["id"] = nid
    n["pos"] = pos
    n["widgets_values"] = widgets
    n.pop("widgets_values_named", None)
    for inp in n.get("inputs", []):
        inp["link"] = None
    for o in n.get("outputs", []):
        o["links"] = None
    n.pop("title", None)
    return n

def scene_prompt(scene_desc):
    return ("Same " + scene_desc + ", same pose, same composition, same lighting and background as the first image. "
    "Keep the body, pose, background and lighting EXACTLY the same. Only change: the face must be EXACTLY the face "
    "of the man in the second reference image - round youthful face, warm medium-brown skin, medium-length wavy black "
    "hair worn down, sparse short beard. ONLY ONE person. Natural realistic skin texture with pores, real photo look, "
    "face fully integrated with the pose, no face-swap seam.")

NEG_PROMPT = ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, different face, wrong face, "
"changed face, face swap seam, duplicate character, multiple people, deformed hands, mutated limbs, bad anatomy, "
"extra fingers, watermark, text, logo")

branches = [
    # (scene_image, scene_desc, ids dict)
    ("face_lock_scene_wide.png",
     "Kerala backwater golden-hour scene with a wooden houseboat on misty calm water",
     {"load": 72, "enc": 73, "patch": 79, "pos": 84, "neg": 85, "sam": 53, "dec": 54, "save": 29, "seed": 42, "save_name": "krea2_face_lock_wide"}),
    ("face_lock_scene_street.png",
     "Kerala village street dusk scene with warm street lamps and wet asphalt reflections",
     {"load": 172, "enc": 173, "patch": 179, "pos": 184, "neg": 185, "sam": 153, "dec": 154, "save": 129, "seed": 43, "save_name": "krea2_face_lock_street"}),
]

nodes = []
nodes.append(shape("UNETLoader", 55, [60, -160], ["krea2_turbo_fp8_scaled.safetensors", "default"]))
nodes.append(shape("CLIPLoader", 56, [60, 30], ["qwen3vl_4b_fp8_scaled.safetensors", "krea2", "default"]))
nodes.append(shape("VAELoader", 57, [60, 220], ["qwen_image_vae.safetensors"]))
nodes.append(shape("LoraLoaderModelOnly", 71, [60, 370], ["krea2_identity_edit_v1_2.safetensors", 1.0]))
nodes.append(shape("LoadImage", 113, [682, 674], ["jaisal_face_locked.png", "image"]))
nodes.append(shape("VAEEncode", 92, [1250, 970], []))
links = []
lid = 0
def L(frm, fs, to, ts, t):
    global lid
    lid += 1
    links.append([lid, frm, fs, to, ts, t])

L(55, 0, 71, 0, "MODEL")
L(57, 0, 92, 1, "VAE")
L(113, 0, 92, 0, "IMAGE")

for scene_img, scene_desc, b in branches:
    y = -300 if b["load"] == 72 else 400
    nodes.append(shape("LoadImage", b["load"], [640, y], [scene_img, "image"]))
    nodes.append(shape("VAEEncode", b["enc"], [1260, y + 220], []))
    nodes.append(shape("Krea2EditModelPatch", b["patch"], [2320, y], [3.5, 1.0, "fit"]))
    nodes.append(shape("Krea2EditGroundedEncode", b["pos"], [1631, y - 16], [scene_prompt(scene_desc), 768, ""]))
    nodes.append(shape("Krea2EditGroundedEncode", b["neg"], [1620, y + 410], [NEG_PROMPT, 768, ""]))
    nodes.append(shape("KSampler", b["sam"], [2791, y - 10], [b["seed"], "randomize", 10, 1, "euler", "simple", 0.5]))
    nodes.append(shape("VAEDecode", b["dec"], [2810, y + 610], []))
    nodes.append(shape("SaveImage", b["save"], [3195, y - 134], [b["save_name"]]))
    L(71, 0, b["patch"], 0, "MODEL")
    L(57, 0, b["dec"], 1, "VAE")
    L(57, 0, b["enc"], 1, "VAE")
    L(57, 0, b["patch"], 4, "VAE")
    L(b["load"], 0, b["enc"], 0, "IMAGE")
    L(b["load"], 0, b["pos"], 1, "IMAGE")
    L(b["load"], 0, b["neg"], 1, "IMAGE")
    L(113, 0, b["pos"], 2, "IMAGE")
    L(113, 0, b["neg"], 2, "IMAGE")
    L(b["enc"], 0, b["patch"], 1, "LATENT")
    L(92, 0, b["patch"], 2, "LATENT")
    L(113, 0, b["patch"], 6, "IMAGE")
    L(b["enc"], 0, b["patch"], 10, "LATENT")
    L(56, 0, b["pos"], 0, "CLIP")
    L(56, 0, b["neg"], 0, "CLIP")
    L(b["patch"], 0, b["sam"], 0, "MODEL")
    L(b["pos"], 0, b["sam"], 1, "CONDITIONING")
    L(b["neg"], 0, b["sam"], 2, "CONDITIONING")
    L(b["enc"], 0, b["sam"], 3, "LATENT")
    L(b["sam"], 0, b["dec"], 0, "LATENT")
    L(b["dec"], 0, b["save"], 0, "IMAGE")

for n in nodes:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in links if lk[3] == n["id"] and lk[4] == j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in links if lk[1] == n["id"]] or None

w = {"id": "krea2-face-lock-batch", "revision": 0, "last_node_id": 185, "last_link_id": lid,
     "nodes": nodes, "links": links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock_batch.json"
with io.open(p, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
