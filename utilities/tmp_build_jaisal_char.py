import json, io, copy
src = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_backwater_v3.json", encoding="utf-8"))
shapes = {}
for n in src["nodes"]:
    if n["type"] not in shapes: shapes[n["type"]] = n
def shape(t, nid, pos, widgets):
    n = copy.deepcopy(shapes[t]); n["id"] = nid; n["pos"] = pos; n["widgets_values"] = widgets
    n.pop("widgets_values_named", None)
    for inp in n.get("inputs", []): inp["link"] = None
    for o in n.get("outputs", []): o["links"] = None
    n.pop("title", None); return n
CHAR = ("a 26-year-old young Malayali man, slim face (not chubby, not round), warm medium-brown skin, "
"soft rounded nose (not sharp), short-to-medium wavy black hair worn forward and down, "
"very short level-1 trimmed dark stubble that reads only as a faint dark shadow on the jaw and chin "
"(essentially clean-shaven with a shadow, NOT a full beard), slim build, plain black t-shirt")
A = ("r3alism, cinematic film still, 85mm, 16:9. Frontal close-up portrait of " + CHAR + ". Calm neutral expression, "
"looking straight at the camera. Soft warm even light, clean blurred background. Natural film grain, "
"photorealistic skin with real pores, high detail.")
B = ("r3alism, cinematic film still, 85mm, 16:9. Three-quarter angle close-up portrait of " + CHAR + ", "
"head turned slightly, relaxed slight smile. Soft warm side light, clean blurred background. Natural film grain, "
"photorealistic skin with real pores, high detail.")
C = ("r3alism, cinematic film still, 50mm, 16:9. Medium shot of " + CHAR + ", standing, slim build, "
"relaxed pose. Soft warm light, clean blurred background. Natural film grain, photorealistic, high detail.")
briefs = [(601,A,"krea2_jaisal_char_a"),(602,B,"krea2_jaisal_char_b"),(603,C,"krea2_jaisal_char_c")]
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
w = {"id":"krea2-jaisal-char","revision":0,"last_node_id":843,"last_link_id":lid,"nodes":nodes,"links":links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_char.json"
with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
