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
T = " natural film grain, photorealistic skin with real pores and subtle natural texture, high detail, sharp focus, ONLY ONE person, no other people, no duplicates"
JAIS = ("Photorealistic portrait of a 26-year-old young man from Kerala (a Keralite), warm medium TAN skin tone "
"(healthy tanned Keralite complexion, NOT a fair American look, NOT a dark generic Tamilian), slim oval face, "
"soft rounded nose, short neat black hair swept to one side, clean-shaven with a very faint light stubble shadow, "
"slim build, plain black t-shirt, clean light neutral studio background, soft even diffused light," + T)
ZID = ("Photorealistic portrait of a 26-year-old young man from Kerala (a Keralite), warm medium TAN skin tone, "
"ROUND face with fuller rounder cheeks (distinctly rounder than a slim oval face), broader wider nose, almond "
"shaped eyes, slightly wider set ears, FULL short dense trimmed beard, short neat black hair in a clean halal "
"fade crop, slim build, plain white t-shirt, clean light neutral studio background, soft even diffused light," + T)
# (prompt, seed, prefix)
branches = [
 (JAIS, 810, "k2c_jaisal_tan"),
 (ZID,  811, "k2c_zidhan_distinct"),
]
nodes = []
nodes.append(shape("UNETLoader",55,[-500,-900],["krea2_turbo_fp8_scaled.safetensors","default"]))
nodes.append(shape("CLIPLoader",56,[-500,-700],["qwen3vl_4b_fp8_scaled.safetensors","krea2","default"]))
nodes.append(shape("VAELoader",57,[-500,-500],["qwen_image_vae.safetensors"]))
nodes.append(shape("EmptySD3LatentImage",82,[700,-950],[1440,2560,1]))
nodes.append(shape("CLIPTextEncode",85,[1100,-950],[""]))
nodes.append(shape("ConditioningZeroOut",90,[1500,-950],[]))
for i,(prompt,seed,name) in enumerate(branches):
    y = -400 + i*450
    nodes.append(shape("LoraLoaderModelOnly",950+i,[0,y],["krea2_turbo_lora_rank_64_bf16.safetensors",0.7]))
    nodes.append(shape("LoraLoaderModelOnly",960+i,[400,y],["Krea2-realism-V2.safetensors",0.8]))
    nodes.append(shape("ApplyKrea2NegPiP",970+i,[800,y],[1.0,False,0,27,1]))
    nodes.append(shape("CLIPTextEncode",840+i,[1100,y],[prompt]))
    nodes.append(shape("KSampler",530+i,[1950,y],[seed,"fixed",12,1,"er_sde","simple",1]))
    nodes.append(shape("VAEDecode",540+i,[2400,y],[]))
    nodes.append(shape("SaveImage",290+i,[2800,y],[name]))
links = []; lid = 0
def L(frm,fs,to,ts,t):
    global lid; lid += 1; links.append([lid,frm,fs,to,ts,t])
L(56,0,85,0,"CLIP"); L(85,0,90,0,"CONDITIONING")
for i in range(2):
    L(55,0,950+i,0,"MODEL"); L(950+i,0,960+i,0,"MODEL"); L(960+i,0,970+i,0,"MODEL"); L(970+i,0,530+i,0,"MODEL")
    L(56,0,970+i,1,"CLIP")
    L(56,0,840+i,0,"CLIP"); L(840+i,0,530+i,1,"CONDITIONING"); L(90,0,530+i,2,"CONDITIONING")
    L(82,0,530+i,3,"LATENT"); L(530+i,0,540+i,0,"LATENT"); L(57,0,540+i,1,"VAE"); L(540+i,0,290+i,0,"IMAGE")
for n in nodes:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in links if lk[3]==n["id"] and lk[4]==j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in links if lk[1]==n["id"]] or None
w = {"id":"k2c-jaisal-zidhan-v2","revision":0,"last_node_id":971,"last_link_id":lid,"nodes":nodes,"links":links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2c_jaisal_zidhan_v2.json"
with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
