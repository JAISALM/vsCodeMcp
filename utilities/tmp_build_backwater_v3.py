import json, io, copy
src = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_weather_v3.json", encoding="utf-8"))
shapes = {}
for n in src["nodes"]:
    if n["type"] not in shapes: shapes[n["type"]] = n
def shape(t, nid, pos, widgets):
    n = copy.deepcopy(shapes[t]); n["id"] = nid; n["pos"] = pos; n["widgets_values"] = widgets
    n.pop("widgets_values_named", None)
    for inp in n.get("inputs", []): inp["link"] = None
    for o in n.get("outputs", []): o["links"] = None
    n.pop("title", None); return n
CHAR = "a 26-year-old young Malayali man, rounder youthful face, warm medium-brown skin, short-to-medium wavy black hair worn forward and down, short sparse stubble beard, plain black t-shirt"
BW = ("r3alism, cinematic film still, 40mm lens, 16:9. Wide shot of " + CHAR + ", standing at the edge of a Kerala backwater at golden hour. "
"A wooden houseboat glides far behind him on glassy calm water. Warm amber side light from a low sun, long golden reflections of the "
"houseboat and palm trees on the water, a thin layer of mist drifting over the water surface, lush green banks. Natural film grain, "
"cinematic warm amber grade, photorealistic, high detail.")
briefs = [(301, BW, "krea2_backwater_v3_a"), (302, BW, "krea2_backwater_v3_b"), (303, BW, "krea2_backwater_v3_c")]
nodes = []
nodes.append(shape("UNETLoader",55,[-400,-600],["krea2_turbo_fp8_scaled.safetensors","default"]))
nodes.append(shape("CLIPLoader",56,[-400,-400],["qwen3vl_4b_fp8_scaled.safetensors","krea2","default"]))
nodes.append(shape("VAELoader",57,[-400,-200],["qwen_image_vae.safetensors"]))
nodes.append(shape("LoraLoaderModelOnly",71,[-50,-550],["krea2_turbo_lora_rank_64_bf16.safetensors",0.7]))
nodes.append(shape("LoraLoaderModelOnly",96,[-50,-350],["Krea2-realism-V2.safetensors",0.8]))
nodes.append(shape("ApplyKrea2NegPiP",97,[300,-350],[1.0,False,0,27,1]))
nodes.append(shape("EmptySD3LatentImage",82,[300,-600],[2560,1440,1]))
nodes.append(shape("CLIPTextEncode",85,[700,600],[""]))
nodes.append(shape("ConditioningZeroOut",90,[1100,600],[]))
for i,(sd,prompt,name) in enumerate(briefs):
    y = -150 + i*300
    nodes.append(shape("CLIPTextEncode",840+i,[700,y],[prompt]))
    nodes.append(shape("KSampler",530+i,[1150,y],[sd,"fixed",12,1,"er_sde","simple",1]))
    nodes.append(shape("VAEDecode",540+i,[1550,y],[]))
    nodes.append(shape("SaveImage",290+i,[1950,y],[name]))
links = []; lid = 0
def L(frm,fs,to,ts,t):
    global lid; lid += 1; links.append([lid,frm,fs,to,ts,t])
L(55,0,71,0,"MODEL"); L(71,0,96,0,"MODEL"); L(96,0,97,0,"MODEL"); L(56,0,97,1,"CLIP")
L(56,0,85,0,"CLIP"); L(85,0,90,0,"CONDITIONING")
for i in range(3):
    L(97,0,530+i,0,"MODEL"); L(840+i,0,530+i,1,"CONDITIONING"); L(90,0,530+i,2,"CONDITIONING")
    L(82,0,530+i,3,"LATENT"); L(530+i,0,540+i,0,"LATENT"); L(57,0,540+i,1,"VAE"); L(540+i,0,290+i,0,"IMAGE")
    L(56,0,840+i,0,"CLIP")
for n in nodes:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in links if lk[3]==n["id"] and lk[4]==j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in links if lk[1]==n["id"]] or None
w = {"id":"krea2-backwater-v3","revision":0,"last_node_id":843,"last_link_id":lid,"nodes":nodes,"links":links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_backwater_v3.json"
with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
