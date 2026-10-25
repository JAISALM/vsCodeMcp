import json, io, copy

src = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json"
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_cine_max.json"
w = json.load(open(src, encoding="utf-8"))
nodes = {n["id"]: n for n in w["nodes"]}

# drop old single-sampler branch + 2nd-ref + comparer
for nid in (53, 92, 113, 114):
    del nodes[nid]

# widget updates
nodes[55]["widgets_values"] = ["krea2_turbo_bf16.safetensors", "default"]
nodes[96]["widgets_values"] = ["Krea2_Cinematic_Artstyle.safetensors", 0.8]
nodes[72]["widgets_values"] = ["jaisal_face_locked.png", "image"]
nodes[29]["widgets_values"] = ["krea2_cine_max_1"]
neg = nodes[85]["widgets_values"][0]

briefs = [
"Cinematic film still, 35mm anamorphic, 16:9. A 26-year-old young Malayali man, medium-length wavy dark hair worn down, sparse short beard, plain dark t-shirt, stands at the edge of a Kerala backwater at golden hour, a wooden houseboat gliding far behind him. Wide shot, warm amber side light, mist on the water, lush green banks, long shadows. Shallow depth of field, natural film grain, muted teal-and-amber grade, Kodak 2383 film look, photorealistic, high detail.",
"Cinematic film still, 50mm prime, 16:9. Close-up of a 26-year-old young Malayali man in soft monsoon rain, medium-length wavy dark hair down and wet, sparse short beard, plain dark t-shirt, looking past the camera into the rain. Overcast diffused light, water droplets on skin, misty grey-green palms behind. Very shallow depth of field, crisp facial detail, natural skin texture, natural film grain, cool desaturated grade with warm skin tones, photorealistic, high detail.",
"Cinematic film still, 40mm, 16:9. Medium shot of a 26-year-old young Malayali man walking a narrow Kerala village street at dusk, medium-length wavy dark hair down, sparse short beard, plain dark t-shirt. Warm street lamps glowing, wet asphalt reflections, whitewashed wall and banana leaves beside him. Warm tungsten key against blue dusk sky, shallow depth of field, natural film grain, cinematic teal-orange grade, photorealistic, high detail.",
]
# old pos-encode (84) -> shared template for 3 branches; negative keeps id 85
enc_proto = nodes[84]
del nodes[84]
gpx, sysp = enc_proto["widgets_values"][1], enc_proto["widgets_values"][2]

new = []
for i in range(3):
    y = -156 + i*300
    enc = copy.deepcopy(enc_proto); enc["id"] = 840+i; enc["pos"] = [1631, y]
    enc["widgets_values"] = [briefs[i], gpx, sysp]
    sm = {"id": 530+i, "type": "SamplerCustom", "pos": [2791, -170 + i*300],
          "inputs": [
            {"name": "model", "localized_name": "model", "type": "MODEL", "link": None},
            {"name": "positive", "localized_name": "positive", "type": "CONDITIONING", "link": None},
            {"name": "negative", "localized_name": "negative", "type": "CONDITIONING", "link": None},
            {"name": "sampler", "localized_name": "sampler", "type": "SAMPLER", "link": None},
            {"name": "sigmas", "localized_name": "sigmas", "type": "SIGMAS", "link": None},
            {"name": "latent_image", "localized_name": "latent_image", "type": "LATENT", "link": None},
            {"name": "add_noise", "localized_name": "add_noise", "type": "BOOLEAN", "widget": {"name": "add_noise"}, "link": None},
            {"name": "noise_seed", "localized_name": "noise_seed", "type": "INT", "widget": {"name": "noise_seed"}, "link": None},
            {"name": "cfg", "localized_name": "cfg", "type": "FLOAT", "widget": {"name": "cfg"}, "link": None},
          ],
          "outputs": [{"name": "output", "localized_name": "output", "type": "LATENT", "links": None}],
          "widgets_values": [True, 42+i, 1.0]}
    vd = copy.deepcopy(nodes[54]); vd["id"] = 540+i; vd["pos"] = [2810, 440 + i*300]
    sv = copy.deepcopy(nodes[29]); sv["id"] = 290+i; sv["pos"] = [3195, -134 + i*300]
    if i == 0:
        sv["widgets_values"] = ["krea2_cine_max_1"]
    else:
        sv["widgets_values"] = ["krea2_cine_max_%d" % (i+1)]
    # 29 stays as branch0 save; remove duplicate 29 (kept as 290)
    for n in (enc, sm, vd, sv):
        for inp in n["inputs"]:
            inp["link"] = None
        for o in n["outputs"]:
            o["links"] = None
    new.extend([enc, sm, vd, sv])
del nodes[29]

ten = {"id": 98, "type": "Krea2TEnhancerAdvanced", "pos": [2320, 620],
       "inputs": [
         {"name": "model", "localized_name": "model", "type": "MODEL", "link": None},
         {"name": "enabled", "localized_name": "enabled", "type": "BOOLEAN", "widget": {"name": "enabled"}, "link": None},
         {"name": "strength", "localized_name": "strength", "type": "FLOAT", "widget": {"name": "strength"}, "link": None},
         {"name": "text_scale", "localized_name": "text_scale", "type": "FLOAT", "widget": {"name": "text_scale"}, "link": None},
         {"name": "debug", "localized_name": "debug", "type": "BOOLEAN", "widget": {"name": "debug"}, "link": None},
       ],
       "outputs": [{"name": "model", "localized_name": "model", "type": "MODEL", "links": None}],
       "widgets_values": [True, 1.0, 1.5, False]}
sig = {"id": 99, "type": "Krea2TurboReferenceSigmaSchedulerFromLatent", "pos": [2560, 880],
       "inputs": [
         {"name": "model", "localized_name": "model", "type": "MODEL", "link": None},
         {"name": "latent", "localized_name": "latent", "type": "LATENT", "link": None},
         {"name": "steps", "localized_name": "steps", "type": "INT", "widget": {"name": "steps"}, "link": None},
         {"name": "denoise", "localized_name": "denoise", "type": "FLOAT", "widget": {"name": "denoise"}, "link": None},
       ],
       "outputs": [
         {"name": "sigmas", "localized_name": "sigmas", "type": "SIGMAS", "links": None},
         {"name": "latent", "localized_name": "latent", "type": "LATENT", "links": None}],
       "widgets_values": [8, 1.0]}
new.extend([ten, sig])

allnodes = list(nodes.values()) + new
for n in allnodes:
    for inp in n.get("inputs", []):
        inp["link"] = None
    for o in n.get("outputs", []):
        o["links"] = None

links = []
lid = 600
def L(frm, fs, to, ts, t):
    global lid
    lid += 1
    links.append([lid, frm, fs, to, ts, t])

L(55, 0, 71, 0, "MODEL")
L(71, 0, 96, 0, "MODEL")
L(96, 0, 98, 0, "MODEL")
L(98, 0, 79, 0, "MODEL")
L(57, 0, 73, 1, "VAE")
L(72, 0, 73, 0, "IMAGE")
L(73, 0, 79, 1, "LATENT")
L(57, 0, 79, 4, "VAE")
L(72, 0, 79, 5, "IMAGE")
L(82, 0, 79, 10, "LATENT")
L(79, 0, 99, 0, "MODEL")
L(82, 0, 99, 1, "LATENT")
L(56, 0, 85, 0, "CLIP")
L(72, 0, 85, 1, "IMAGE")
for i in range(3):
    enc, sm, vd, sv = 840+i, 530+i, 540+i, 290+i
    L(56, 0, enc, 0, "CLIP")
    L(72, 0, enc, 1, "IMAGE")
    L(99, 0, sm, 4, "SIGMAS")
    L(99, 1, sm, 5, "LATENT")
    L(enc, 0, sm, 1, "CONDITIONING")
    L(85, 0, sm, 2, "CONDITIONING")
    L(sm, 0, vd, 0, "LATENT")
    L(57, 0, vd, 1, "VAE")
    L(vd, 0, sv, 0, "IMAGE")

for n in allnodes:
    for j, inp in enumerate(n["inputs"]):
        inp["link"] = next((lk[0] for lk in links if lk[3] == n["id"] and lk[4] == j), None)
    for o in n["outputs"]:
        o["links"] = [lk[0] for lk in links if lk[1] == n["id"]] or None

w["nodes"] = allnodes
w["links"] = links
w["last_node_id"] = 843
w["last_link_id"] = lid

with io.open(out, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", out)
print("nodes:", len(allnodes), "links:", len(links))
print("negative:", neg[:80])
print("branch enc prompts:", [next(n for n in allnodes if n["id"] == 840+i)["widgets_values"][0][:40] for i in range(3)])
