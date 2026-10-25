import json, io, copy

src = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json", encoding="utf-8"))
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

POS_PROMPT = ("Same monsoon rain scene, same pose, same composition, same lighting and background as the first image. "
"Keep the body, pose, rain, background and lighting EXACTLY the same. Only change: the face must be EXACTLY the face "
"of the man in the second reference image - round youthful face, warm medium-brown skin, medium-length wavy black hair "
"worn down and wet, sparse short beard. ONLY ONE person. Natural realistic skin texture with pores, real photo look, "
"face fully integrated with the pose, no face-swap seam.")
NEG_PROMPT = ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, different face, wrong face, "
"changed face, face swap seam, duplicate character, multiple people, deformed hands, mutated limbs, bad anatomy, "
"extra fingers, watermark, text, logo")

nodes = []
nodes.append(shape("UNETLoader", 55, [60, -160], ["krea2_turbo_fp8_scaled.safetensors", "default"]))
nodes.append(shape("CLIPLoader", 56, [60, 30], ["qwen3vl_4b_fp8_scaled.safetensors", "krea2", "default"]))
nodes.append(shape("VAELoader", 57, [60, 220], ["qwen_image_vae.safetensors"]))
nodes.append(shape("LoraLoaderModelOnly", 71, [60, 370], ["krea2_identity_edit_v1_2.safetensors", 1.0]))
nodes.append(shape("LoadImage", 72, [640, -160], ["face_lock_scene.png", "image"]))
nodes.append(shape("LoadImage", 113, [682, 674], ["jaisal_face_locked.png", "image"]))
nodes.append(shape("VAEEncode", 73, [1260, 60], []))
nodes.append(shape("VAEEncode", 92, [1250, 970], []))
nodes.append(shape("Krea2EditModelPatch", 79, [2320, -160], [2.5, 1.0, "fit"]))
nodes.append(shape("Krea2EditGroundedEncode", 84, [1631, -156], [POS_PROMPT, 768, ""]))
nodes.append(shape("Krea2EditGroundedEncode", 85, [1620, 250], [NEG_PROMPT, 768, ""]))
nodes.append(shape("KSampler", 53, [2791, -170], [716856683708963, "randomize", 10, 1, "euler", "simple", 0.5]))
nodes.append(shape("VAEDecode", 54, [2810, 440], []))
nodes.append(shape("SaveImage", 29, [3195, -134], ["krea2_face_lock"]))

links = []
lid = 0
def L(frm, fs, to, ts, t):
    global lid
    lid += 1
    links.append([lid, frm, fs, to, ts, t])

L(55, 0, 71, 0, "MODEL")
L(71, 0, 79, 0, "MODEL")
L(56, 0, 84, 0, "CLIP")
L(56, 0, 85, 0, "CLIP")
L(57, 0, 54, 1, "VAE")
L(57, 0, 73, 1, "VAE")
L(57, 0, 92, 1, "VAE")
L(57, 0, 79, 4, "VAE")
L(72, 0, 73, 0, "IMAGE")
L(113, 0, 92, 0, "IMAGE")
L(72, 0, 84, 1, "IMAGE")
L(72, 0, 85, 1, "IMAGE")
L(113, 0, 84, 2, "IMAGE")
L(113, 0, 85, 2, "IMAGE")
L(73, 0, 79, 1, "LATENT")
L(92, 0, 79, 2, "LATENT")
L(113, 0, 79, 6, "IMAGE")
L(73, 0, 79, 10, "LATENT")
L(84, 0, 53, 1, "CONDITIONING")
L(85, 0, 53, 2, "CONDITIONING")
L(73, 0, 53, 3, "LATENT")
L(53, 0, 54, 0, "LATENT")
L(54, 0, 29, 0, "IMAGE")

for n in nodes:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in links if lk[3] == n["id"] and lk[4] == j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in links if lk[1] == n["id"]] or None

w = {"id": "krea2-face-lock", "revision": 0, "last_node_id": 113, "last_link_id": lid,
     "nodes": nodes, "links": links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock.json"
with io.open(p, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
