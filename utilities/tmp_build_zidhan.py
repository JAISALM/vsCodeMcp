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
ZID = ("a 26-year-old young Indian man, short clean halal fade crop haircut, full short dense trimmed beard, "
"warm medium-brown skin, plain white t-shirt")
STREET = ("r3alism, cinematic film still, 40mm, 16:9. Medium shot of " + ZID + ", standing on a narrow Kerala village "
"street at golden hour. Warm amber side light, whitewashed walls and banana leaves beside him, long soft shadows. "
"Natural film grain, cinematic warm amber grade, photorealistic, high detail.")
briefs = [(401, STREET, "krea2_zidhan_v3_a"), (402, STREET, "krea2_zidhan_v3_b"), (403, STREET, "krea2_zidhan_v3_c")]
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
w = {"id":"krea2-zidhan-v3","revision":0,"last_node_id":843,"last_link_id":lid,"nodes":nodes,"links":links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_zidhan_v3.json"
with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE zidhan t2i:", p)

# ---- face_lock_zidhan: clone face_lock_v2, swap face ref + face desc + save prefix ----
fl = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock_v2.json", encoding="utf-8"))
POS = ("The man in the first image must have EXACTLY the face of the man in the second reference image: "
"short clean halal fade crop haircut, full short dense trimmed beard, warm medium-brown skin. "
"Keep the first image's scene, pose, lighting, clothing and composition EXACTLY the same. Change only the face. "
"ONLY ONE person. Natural realistic skin with pores, face fully integrated, no face-swap seam.")
for n in fl["nodes"]:
    if n["id"] == 113:
        n["widgets_values"] = ["zidhan_face_ref.png","image"]
    if n["id"] == 84:
        n["widgets_values"] = [POS,768,""]
    if n["id"] == 29:
        n["widgets_values"] = ["krea2_face_lock_zidhan"]
    if n["id"] == 53:
        n["widgets_values"] = [427182930471293,"randomize",10,1,"euler","simple",0.35]
p2 = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock_zidhan.json"
with io.open(p2,"w",encoding="utf-8") as f: f.write(json.dumps(fl, indent=1))
print("WROTE face_lock_zidhan:", p2)
