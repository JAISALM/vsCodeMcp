import json, io, copy
src = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_charlora_v3.json", encoding="utf-8"))
shapes = {}
for n in src["nodes"]:
    if n["type"] not in shapes: shapes[n["type"]] = n
def shape(t, nid, pos, widgets):
    n = copy.deepcopy(shapes[t]); n["id"] = nid; n["pos"] = pos; n["widgets_values"] = widgets
    n.pop("widgets_values_named", None)
    for inp in n.get("inputs", []): inp["link"] = None
    for o in n.get("outputs", []): o["links"] = None
    n.pop("title", None); return n
P = ("Photorealistic portrait of a 26-year-old young man from Kerala (a Keralite), LIGHT FAIR skin tone "
"(fair to white complexion, NOT a dark-skinned generic Tamilian), slim oval face, soft rounded nose, "
"well-groomed short neat black hair, clean-shaven with a very faint light stubble shadow, slim build, "
"plain white t-shirt, clean light neutral studio background, soft even diffused light, natural film grain, "
"photorealistic skin with real pores and subtle natural texture, high detail, sharp focus, ONLY ONE person, "
"no other people, no duplicates")
nodes = []
nodes.append(shape("UNETLoader",55,[-500,-900],["krea2_turbo_fp8_scaled.safetensors","default"]))
nodes.append(shape("CLIPLoader",56,[-500,-700],["qwen3vl_4b_fp8_scaled.safetensors","krea2","default"]))
nodes.append(shape("VAELoader",57,[-500,-500],["qwen_image_vae.safetensors"]))
nodes.append(shape("LoraLoaderModelOnly",96,[300,-700],["Krea2-realism-V2.safetensors",0.8]))
nodes.append(shape("LoraLoaderModelOnly",95,[0,-700],["krea2_turbo_lora_rank_64_bf16.safetensors",0.7]))
nodes.append(shape("ApplyKrea2NegPiP",97,[700,-700],[1.0,False,0,27,1]))
nodes.append(shape("EmptySD3LatentImage",82,[700,-950],[1440,2560,1]))
nodes.append(shape("CLIPTextEncode",84,[1100,-400],[P]))
nodes.append(shape("CLIPTextEncode",85,[1100,-950],[""]))
nodes.append(shape("ConditioningZeroOut",90,[1500,-950],[]))
nodes.append(shape("KSampler",53,[1950,-400],[801,"fixed",12,1,"er_sde","simple",1]))
nodes.append(shape("VAEDecode",54,[2400,-400],[]))
nodes.append(shape("SaveImage",29,[2800,-400],["k2l_keralite_t2i"]))
links = []; lid = 0
def L(frm,fs,to,ts,t):
    global lid; lid += 1; links.append([lid,frm,fs,to,ts,t])
# UNET -> turbo(95) -> realism(96) -> NegPiP(97) -> KSampler
L(55,0,95,0,"MODEL"); L(95,0,96,0,"MODEL"); L(96,0,97,0,"MODEL"); L(97,0,53,0,"MODEL")
L(56,0,97,1,"CLIP")
L(56,0,84,0,"CLIP"); L(84,0,53,1,"CONDITIONING")
L(56,0,85,0,"CLIP"); L(85,0,90,0,"CONDITIONING"); L(90,0,53,2,"CONDITIONING")
L(82,0,53,3,"LATENT"); L(53,0,54,0,"LATENT"); L(57,0,54,1,"VAE"); L(54,0,29,0,"IMAGE")
for n in nodes:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in links if lk[3]==n["id"] and lk[4]==j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in links if lk[1]==n["id"]] or None
w = {"id":"k2l-keralite-t2i","revision":0,"last_node_id":97,"last_link_id":lid,"nodes":nodes,"links":links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2l_keralite_t2i.json"
with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
