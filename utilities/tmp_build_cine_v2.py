import json, io, copy

# ---- native shapes from community 2pass v15 file ----
src = json.load(open(r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json", encoding="utf-8"))
shapes = {}
for n in src["nodes"]:
    t = n["type"]
    if t not in shapes:
        shapes[t] = n
# EmptySD3LatentImage shape from a proven Krea2 file
src2 = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1.json", encoding="utf-8"))
for n in src2["nodes"]:
    if n["type"] == "EmptySD3LatentImage" and "EmptySD3LatentImage" not in shapes:
        shapes["EmptySD3LatentImage"] = n
    if n["type"] == "SaveImage" and "SaveImage" not in shapes:
        shapes["SaveImage"] = n
print("shapes available:", sorted(shapes.keys()))

def shape(t, nid, pos, widgets):
    n = copy.deepcopy(shapes[t])
    n["id"] = nid
    n["pos"] = pos
    n["widgets_values"] = widgets
    n["widgets_values_named"] = None
    for inp in n.get("inputs", []):
        inp["link"] = None
    for o in n.get("outputs", []):
        o["links"] = None
    n.pop("title", None)
    n.pop("color", None); n.pop("bgcolor", None)
    return n

CHAR = "a 26-year-old young Malayali man, round youthful face, warm medium-brown skin, medium-length wavy black hair worn down, sparse short beard, plain dark t-shirt"
briefs = [
"r3alism, cinematic film still, 40mm lens, 16:9. " + CHAR + ", standing at the edge of a Kerala backwater at golden hour. A wooden houseboat glides far behind him on calm water. Wide shot, warm amber side light, mist on the water, lush green banks, long shadows. Shallow depth of field, natural skin texture, natural film grain, muted teal-and-amber grade, photorealistic, high detail.",
"r3alism, cinematic film still, 50mm prime, 16:9. Close-up of " + CHAR + ", medium-length wavy black hair worn down and wet, in soft monsoon rain, looking past the camera into the rain. Overcast diffused light, water droplets on skin, misty grey-green palms behind. Very shallow depth of field, crisp facial detail, natural skin texture, natural film grain, cool desaturated grade with warm skin tones, photorealistic, high detail.",
"r3alism, cinematic film still, 40mm, 16:9. Medium shot of " + CHAR + ", walking a narrow Kerala village street at dusk. Warm street lamps glowing, wet asphalt reflections, whitewashed walls and banana leaves beside him. Warm tungsten key against blue dusk sky, shallow depth of field, natural film grain, cinematic teal-orange grade, photorealistic, high detail.",
]

def build(path, n_branches, width, height, prefix):
    nodes = []
    nodes.append(shape("UNETLoader", 55, [-400, -900], ["krea2_raw_bf16.safetensors", "default"]))
    nodes.append(shape("CLIPLoader", 56, [-400, -500], ["qwen3vl_4b_fp8_scaled.safetensors", "krea2", "default"]))
    nodes.append(shape("VAELoader", 57, [-400, -300], ["krea2RealVae_v10.safetensors"]))
    nodes.append(shape("LoraLoaderModelOnly", 71, [-50, -850], ["krea2_turbo_lora_rank_64_bf16.safetensors", 0.7]))
    nodes.append(shape("LoraLoaderModelOnly", 96, [-50, -650], ["Krea2-realism-V2.safetensors", 0.8]))
    nodes.append(shape("ApplyKrea2NegPiP", 97, [300, -650], [1.0, False, 0, 27, 1]))
    nodes.append(shape("EmptySD3LatentImage", 82, [300, -900], [width, height, 1]))
    nodes.append(shape("ConditioningZeroOut", 90, [300, -200], []))
    for i in range(n_branches):
        y = -150 + i*300
        nodes.append(shape("CLIPTextEncode", 840+i, [700, y], [briefs[i]]))
        nodes.append(shape("KSampler", 530+i, [1150, y], [42+i, "randomize", 12, 1, "er_sde", "simple", 1]))
        nodes.append(shape("VAEDecode", 540+i, [1550, y], []))
        nodes.append(shape("SaveImage", 290+i, [1950, y], [prefix + str(i+1)]))
    links = []
    lid = 0
    def L(frm, fs, to, ts, t):
        nonlocal lid
        lid += 1
        links.append([lid, frm, fs, to, ts, t])
    L(55,0,71,0,"MODEL"); L(71,0,96,0,"MODEL"); L(96,0,97,0,"MODEL"); L(56,0,97,1,"CLIP")
    for i in range(n_branches):
        L(97,0,530+i,0,"MODEL")
        L(840+i,0,530+i,1,"CONDITIONING")
        L(90,0,530+i,2,"CONDITIONING")
        L(82,0,530+i,3,"LATENT")
        L(530+i,0,540+i,0,"LATENT")
        L(57,0,540+i,1,"VAE")
        L(540+i,0,290+i,0,"IMAGE")
    # assign link fields
    for n in nodes:
        for j, inp in enumerate(n.get("inputs", [])):
            inp["link"] = next((lk[0] for lk in links if lk[3]==n["id"] and lk[4]==j), None)
        for o in n.get("outputs", []):
            o["links"] = [lk[0] for lk in links if lk[1]==n["id"]] or None
    def sanitize(x):
        if isinstance(x, str):
            return x.replace("\u00a0", " ").replace("\u2028", " ").replace("\u2029", " ")
        if isinstance(x, list):
            return [sanitize(v) for v in x]
        if isinstance(x, dict):
            return {k: sanitize(v) for k, v in x.items()}
        return x
    w = {"id": "krea2-cine-v2", "revision": 0, "last_node_id": 843, "last_link_id": lid,
         "nodes": nodes, "links": links}
    w = sanitize(w)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(w, indent=1))
    print("WROTE", path, "nodes:", len(nodes), "links:", len(links))

W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
build(W + r"\krea2_cine_v2.json", 3, 2048, 1152, "krea2_cine_v2_")
build(W + r"\krea2_cine_v2_4mp.json", 1, 2560, 1440, "krea2_cine_v2_4mp_")
