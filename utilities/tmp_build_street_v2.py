import json, io, copy

src = json.load(open(r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json", encoding="utf-8"))
shapes = {}
for n in src["nodes"]:
    if n["type"] not in shapes:
        shapes[n["type"]] = n
src2 = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1.json", encoding="utf-8"))
for n in src2["nodes"]:
    if n["type"] == "EmptySD3LatentImage" and "EmptySD3LatentImage" not in shapes:
        shapes["EmptySD3LatentImage"] = n
    if n["type"] == "SaveImage" and "SaveImage" not in shapes:
        shapes["SaveImage"] = n

def shape(t, nid, pos, widgets):
    n = copy.deepcopy(shapes[t])
    n["id"] = nid; n["pos"] = pos; n["widgets_values"] = widgets
    n.pop("widgets_values_named", None)
    for inp in n.get("inputs", []): inp["link"] = None
    for o in n.get("outputs", []): o["links"] = None
    n.pop("title", None)
    return n

CHAR = "a 26-year-old young Malayali man, rounder youthful face, warm medium-brown skin, short-to-medium wavy black hair worn forward and down, short sparse stubble beard, plain black t-shirt"
P = ("r3alism, cinematic film still, 40mm, 16:9. Medium shot of " + CHAR + ", walking a narrow Kerala village street at dusk. "
"Warm street lamps glowing, wet asphalt reflections, whitewashed walls and banana leaves beside him. Warm tungsten key "
"against a blue dusk sky, shallow depth of field, natural film grain, cinematic teal-orange grade, photorealistic, high detail.")

seeds = [101, 102, 103]
nodes = []
nodes.append(shape("UNETLoader", 55, [-400, -900], ["krea2_raw_bf16.safetensors", "default"]))
nodes.append(shape("CLIPLoader", 56, [-400, -500], ["qwen3vl_4b_fp8_scaled.safetensors", "krea2", "default"]))
nodes.append(shape("VAELoader", 57, [-400, -300], ["krea2RealVae_v10.safetensors"]))
nodes.append(shape("LoraLoaderModelOnly", 71, [-50, -850], ["krea2_turbo_lora_rank_64_bf16.safetensors", 0.7]))
nodes.append(shape("LoraLoaderModelOnly", 96, [-50, -650], ["Krea2-realism-V2.safetensors", 0.8]))
nodes.append(shape("ApplyKrea2NegPiP", 97, [300, -650], [1.0, False, 0, 27, 1]))
nodes.append(shape("EmptySD3LatentImage", 82, [300, -900], [2048, 1152, 1]))
nodes.append(shape("ConditioningZeroOut", 90, [300, -200], []))
neg85 = shape("CLIPTextEncode", 85, [700, 200], [""])
nodes.append(neg85)
for i, sd in enumerate(seeds):
    y = -150 + i*300
    nodes.append(shape("CLIPTextEncode", 840+i, [700, y], [P]))
    nodes.append(shape("KSampler", 530+i, [1150, y], [sd, "fixed", 12, 1, "er_sde", "simple", 1]))
    nodes.append(shape("VAEDecode", 540+i, [1550, y], []))
    nodes.append(shape("SaveImage", 290+i, [1950, y], ["krea2_street_v2_%d" % (i+1)]))

links = []
lid = 0
def L(frm, fs, to, ts, t):
    global lid
    lid += 1
    links.append([lid, frm, fs, to, ts, t])
L(55,0,71,0,"MODEL"); L(71,0,96,0,"MODEL"); L(96,0,97,0,"MODEL"); L(56,0,97,1,"CLIP")
L(56,0,85,0,"CLIP"); L(85,0,90,0,"CONDITIONING")
for i in range(3):
    L(97,0,530+i,0,"MODEL")
    L(840+i,0,530+i,1,"CONDITIONING")
    L(90,0,530+i,2,"CONDITIONING")
    L(82,0,530+i,3,"LATENT")
    L(530+i,0,540+i,0,"LATENT")
    L(57,0,540+i,1,"VAE")
    L(540+i,0,290+i,0,"IMAGE")
for n in nodes:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in links if lk[3]==n["id"] and lk[4]==j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in links if lk[1]==n["id"]] or None
w = {"id": "krea2-street-v2", "revision": 0, "last_node_id": 843, "last_link_id": lid, "nodes": nodes, "links": links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_street_v2.json"
with io.open(p, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
