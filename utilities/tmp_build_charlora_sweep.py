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
W, H = 1440, 1080
K = (" young Keralite man, light-to-medium warm skin tone (NOT a dark generic Tamilian), slim face (not chubby), "
"soft rounded nose, ")
JAIS = ("jeskvman, a 26-year-old" + K + "short-to-medium wavy black hair worn forward and down, very short level-1 trimmed "
"dark stubble (a faint shadow on the jaw and chin, NOT a full beard), slim build, plain black t-shirt, clean light "
"neutral background, soft warm even light, natural film grain, photorealistic skin with real pores, high detail, "
"ONLY ONE person, no other people, no duplicates")
ZID = ("dlorman, a 26-year-old" + K + "short clean halal fade crop haircut, full short dense trimmed beard, slim build, "
"plain white t-shirt, clean light neutral background, soft warm even light, natural film grain, photorealistic skin "
"with real pores, high detail, ONLY ONE person, no other people, no duplicates")
# (char, prompt, strength, seed, prefix)
branches = [
 ("jaisal", JAIS, 1.0, 710, "k2l_jaisal_s100"),
 ("jaisal", JAIS, 0.7, 711, "k2l_jaisal_s070"),
 ("jaisal", JAIS, 0.5, 712, "k2l_jaisal_s050"),
 ("zidhan", ZID, 1.0, 713, "k2l_zidhan_s100"),
 ("zidhan", ZID, 0.7, 714, "k2l_zidhan_s070"),
 ("zidhan", ZID, 0.5, 715, "k2l_zidhan_s050"),
]
nodes = []
nodes.append(shape("UNETLoader",55,[-500,-900],["krea2_turbo_fp8_scaled.safetensors","default"]))
nodes.append(shape("CLIPLoader",56,[-500,-700],["qwen3vl_4b_fp8_scaled.safetensors","krea2","default"]))
nodes.append(shape("VAELoader",57,[-500,-500],["qwen_image_vae.safetensors"]))
nodes.append(shape("LoraLoaderModelOnly",96,[300,-700],["Krea2-realism-V2.safetensors",0.8]))
nodes.append(shape("ApplyKrea2NegPiP",97,[700,-700],[1.0,False,0,27,1]))
nodes.append(shape("EmptySD3LatentImage",82,[700,-950],[W,H,1]))
nodes.append(shape("CLIPTextEncode",85,[1100,-950],[""]))
nodes.append(shape("ConditioningZeroOut",90,[1500,-950],[]))
for i,(char,prompt,strength,seed,name) in enumerate(branches):
    y = -500 + i*380
    nodes.append(shape("LoraLoaderModelOnly",700+i,[0,y],["krea2fp_v2_ep64.safetensors",strength]))
    nodes.append(shape("LoraLoaderModelOnly",710+i,[400,y],["krea2_turbo_lora_rank_64_bf16.safetensors",0.7]))
    nodes.append(shape("CLIPTextEncode",840+i,[1100,y],[prompt]))
    nodes.append(shape("KSampler",530+i,[1550,y],[seed,"fixed",12,1,"er_sde","simple",1]))
    nodes.append(shape("VAEDecode",540+i,[1950,y],[]))
    nodes.append(shape("SaveImage",290+i,[2350,y],[name]))
links = []; lid = 0
def L(frm,fs,to,ts,t):
    global lid; lid += 1; links.append([lid,frm,fs,to,ts,t])
L(55,0,700,0,"MODEL")  # base (only for i=0 chain start)
# model chain: UNET -> charLoRA[i] -> turboLoRA[i] -> realism(96) -> NegPiP(97)
# But realism(96) is shared; chain charLoRA[i]->turboLoRA[i]->96? No, 96 is shared sink.
# Rebuild: each branch: UNET->charLoRA[i]; charLoRA[i]->turboLoRA[i]; turboLoRA[i]->96 (shared); 96->97
# But 96 shared by all branches -> 96 has 6 model inputs? No, LoraLoader model input is single.
# So each branch must feed 96 separately. Instead: turboLoRA[i]->97 (NegPiP) directly, and 96 into 97? 
# Simplest: chain UNET->charLoRA[i]->turboLoRA[i]->97 (NegPiP model), and realism 96 UNET->96->? 
# Let's keep it simple: per-branch chain UNET->char[i]->turbo[i]->97; realism skipped to avoid shared-node issue.
# Actually realism is important. Let me give each branch its own realism node.
# Rebuild nodes: remove shared 96/97; per-branch realism+NegPiP.
nodes = [n for n in nodes if n["type"] in ("UNETLoader","CLIPLoader","VAELoader","EmptySD3LatentImage","CLIPTextEncode","ConditioningZeroOut")]
for i,(char,prompt,strength,seed,name) in enumerate(branches):
    y = -500 + i*400
    nodes.append(shape("LoraLoaderModelOnly",700+i,[0,y],["krea2fp_v2_ep64.safetensors",strength]))
    nodes.append(shape("LoraLoaderModelOnly",710+i,[400,y],["krea2_turbo_lora_rank_64_bf16.safetensors",0.7]))
    nodes.append(shape("LoraLoaderModelOnly",960+i,[800,y],["Krea2-realism-V2.safetensors",0.8]))
    nodes.append(shape("ApplyKrea2NegPiP",970+i,[1200,y],[1.0,False,0,27,1]))
    nodes.append(shape("CLIPTextEncode",840+i,[1500,y],[prompt]))
    nodes.append(shape("KSampler",530+i,[1950,y],[seed,"fixed",12,1,"er_sde","simple",1]))
    nodes.append(shape("VAEDecode",540+i,[2400,y],[]))
    nodes.append(shape("SaveImage",290+i,[2800,y],[name]))
links = []; lid = 0
def L(frm,fs,to,ts,t):
    global lid; lid += 1; links.append([lid,frm,fs,to,ts,t])
L(55,0,96,0,"MODEL") if False else None  # no shared
for i in range(6):
    L(55,0,700+i,0,"MODEL"); L(700+i,0,710+i,0,"MODEL"); L(710+i,0,960+i,0,"MODEL"); L(960+i,0,970+i,0,"MODEL")
    L(56,0,970+i,1,"CLIP")
    L(56,0,85,0,"CLIP"); L(85,0,90,0,"CONDITIONING")
    L(970+i,0,530+i,0,"MODEL"); L(840+i,0,530+i,1,"CONDITIONING"); L(90,0,530+i,2,"CONDITIONING")
    L(82,0,530+i,3,"LATENT"); L(530+i,0,540+i,0,"LATENT"); L(57,0,540+i,1,"VAE"); L(540+i,0,290+i,0,"IMAGE")
    L(56,0,840+i,0,"CLIP")
for n in nodes:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in links if lk[3]==n["id"] and lk[4]==j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in links if lk[1]==n["id"]] or None
w = {"id":"krea2-charlora-sweep","revision":0,"last_node_id":975,"last_link_id":lid,"nodes":nodes,"links":links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_charlora_sweep.json"
with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
