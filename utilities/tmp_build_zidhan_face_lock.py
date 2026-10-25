import json, io
face_ref = "zidhan_final_ref.png"
instruction = "The man in the first image must have EXACTLY the face, short neat black hair (halal fade crop), identity, and slim build of the man in the second reference image: a ~26-year-old Keralite man, rounder face, SHARP ANGULAR prominent nose (Dulquer-Salman-style), fuller lips, FULL short dense beard, warm Keralite tan skin. Keep the first image's pose, scene, background, clothing, and lighting EXACTLY the same. Change ONLY the face to match the second reference (including the FULL short dense beard). ONLY ONE person, no duplicates, natural realistic skin with pores, face fully integrated, no face-swap seam."
negative = "plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, different face, wrong face, changed face, face swap seam, duplicate character, multiple people, deformed hands, mutated limbs, bad anatomy, extra fingers, watermark, text, logo, clean-shaven, no beard, missing beard"
branches = [
 ("S1","zidhan_scene_S1_paddy.png",9401,"k2f_zidhan_S1_paddy"),
 ("S2","zidhan_scene_S2_house.png",9402,"k2f_zidhan_S2_house"),
 ("S3","zidhan_scene_S3_interior.png",9403,"k2f_zidhan_S3_interior"),
 ("S4","zidhan_scene_S4_bike.png",9404,"k2f_zidhan_S4_bike"),
 ("S5","zidhan_scene_S5_7sfoot.png",9405,"k2f_zidhan_S5_7sfoot"),
 ("S6","zidhan_scene_S6_rural.png",9406,"k2f_zidhan_S6_rural"),
]
def node(nid, ntype, pos, size, widgets, inputs, outputs):
    return {"id": nid, "type": ntype, "pos": pos, "size": size, "flags": {}, "order": 0, "mode": 0,
            "inputs": inputs, "outputs": outputs, "properties": {"Node name for S&R": ntype}, "widgets_values": widgets}
def inp(name, typ, link): return {"name": name, "type": typ, "widget": {"name": name}, "link": link}
nodes = []
nodes.append(node(55,"UNETLoader",[100,100],[280,90],["krea2_turbo_fp8_scaled.safetensors","default"],[],[{"name":"MODEL","type":"MODEL","links":None}]))
nodes.append(node(56,"CLIPLoader",[100,250],[280,110],["qwen3vl_4b_fp8_scaled.safetensors","krea2","default"],[],[{"name":"CLIP","type":"CLIP","links":None}]))
nodes.append(node(57,"VAELoader",[100,400],[280,70],["qwen_image_vae.safetensors"],[],[{"name":"VAE","type":"VAE","links":None}]))
for i,(name, base, seed, prefix) in enumerate(branches):
    off = i*20
    identity=101+off; patch=102+off; ksam=103+off; vdec=104+off; save=105+off
    vbase=106+off; vref=107+off; pos=108+off; neg=109+off; lbase=110+off; lref=111+off
    y=100+i*280
    nodes.append(node(lbase,"LoadImage",[420,y],[282,322],[base,"image"],
        [inp("image","COMBO",None),inp("upload","IMAGEUPLOAD",None)],[{"name":"IMAGE","type":"IMAGE","links":None},{"name":"MASK","type":"MASK","links":None}]))
    nodes.append(node(lref,"LoadImage",[420,y+240],[282,322],[face_ref,"image"],
        [inp("image","COMBO",None),inp("upload","IMAGEUPLOAD",None)],[{"name":"IMAGE","type":"IMAGE","links":None},{"name":"MASK","type":"MASK","links":None}]))
    nodes.append(node(vbase,"VAEEncode",[740,y],[260,90],[],[inp("pixels","IMAGE",None),inp("vae","VAE",None)],[{"name":"LATENT","type":"LATENT","links":None}]))
    nodes.append(node(vref,"VAEEncode",[740,y+240],[260,90],[],[inp("pixels","IMAGE",None),inp("vae","VAE",None)],[{"name":"LATENT","type":"LATENT","links":None}]))
    nodes.append(node(identity,"LoraLoaderModelOnly",[1040,y],[300,100],["krea2_identity_edit_v1_2.safetensors",1.0],
        [inp("model","MODEL",None),inp("lora_name","COMBO",None),inp("strength_model","FLOAT",None)],[{"name":"MODEL","type":"MODEL","links":None}]))
    nodes.append(node(patch,"Krea2EditModelPatch",[1360,y],[300,140],[4.0,1.0,"fit"],
        [inp("model","MODEL",None),inp("source_latent","LATENT",None),inp("source_latent_b","LATENT",None),inp("ref_boost_mask","MASK",None),
         inp("vae","VAE",None),inp("source_image","IMAGE",None),inp("source_image_b","IMAGE",None),inp("ref_boost","FLOAT",None),
         inp("ref_boost_a","FLOAT",None),inp("fit_mode","COMBO",None),inp("target_latent","LATENT",None)],[{"name":"MODEL","type":"MODEL","links":None}]))
    nodes.append(node(pos,"Krea2EditGroundedEncode",[1040,y+240],[420,220],[instruction,768,""],
        [inp("clip","CLIP",None),inp("image","IMAGE",None),inp("image_b","IMAGE",None),inp("prompt","STRING",None),inp("grounding_px","INT",None),inp("system_prompt","STRING",None)],[{"name":"CONDITIONING","type":"CONDITIONING","links":None}]))
    nodes.append(node(neg,"Krea2EditGroundedEncode",[1360,y+240],[420,220],[negative,768,""],
        [inp("clip","CLIP",None),inp("image","IMAGE",None),inp("image_b","IMAGE",None),inp("prompt","STRING",None),inp("grounding_px","INT",None),inp("system_prompt","STRING",None)],[{"name":"CONDITIONING","type":"CONDITIONING","links":None}]))
    nodes.append(node(ksam,"KSampler",[1700,y],[300,220],[seed,"fixed",10,1,"euler","simple",0.4],
        [inp("model","MODEL",None),inp("positive","CONDITIONING",None),inp("negative","CONDITIONING",None),inp("latent_image","LATENT",None),
         inp("seed","INT",None),inp("steps","INT",None),inp("cfg","FLOAT",None),inp("sampler_name","COMBO",None),inp("scheduler","COMBO",None),inp("denoise","FLOAT",None)],[{"name":"LATENT","type":"LATENT","links":None}]))
    nodes.append(node(vdec,"VAEDecode",[2020,y],[260,90],[],[inp("samples","LATENT",None),inp("vae","VAE",None)],[{"name":"IMAGE","type":"IMAGE","links":None}]))
    nodes.append(node(save,"SaveImage",[2300,y],[300,160],[prefix],[inp("images","IMAGE",None)],[]))
links=[]; lid=0
def L(f,fs,t,ts,typ):
    global lid
    lid+=1
    links.append([lid,f,fs,t,ts,typ]); return lid
for i,(name, base, seed, prefix) in enumerate(branches):
    off=i*20
    identity=101+off; patch=102+off; ksam=103+off; vdec=104+off; save=105+off
    vbase=106+off; vref=107+off; pos=108+off; neg=109+off; lbase=110+off; lref=111+off
    L(55,0,identity,0,"MODEL"); L(identity,0,patch,0,"MODEL"); L(patch,0,ksam,0,"MODEL")
    L(56,0,pos,0,"CLIP"); L(56,0,neg,0,"CLIP")
    L(57,0,vdec,1,"VAE"); L(57,0,vbase,1,"VAE"); L(57,0,vref,1,"VAE"); L(57,0,patch,4,"VAE")
    L(lbase,0,vbase,0,"IMAGE"); L(lref,0,vref,0,"IMAGE")
    L(lbase,0,pos,1,"IMAGE"); L(lbase,0,neg,1,"IMAGE")
    L(lref,0,pos,2,"IMAGE"); L(lref,0,neg,2,"IMAGE")
    L(vbase,0,patch,1,"LATENT"); L(vref,0,patch,2,"LATENT"); L(lref,0,patch,6,"IMAGE"); L(vbase,0,patch,10,"LATENT")
    L(pos,0,ksam,1,"CONDITIONING"); L(neg,0,ksam,2,"CONDITIONING"); L(vbase,0,ksam,3,"LATENT")
    L(ksam,0,vdec,0,"LATENT"); L(vdec,0,save,0,"IMAGE")
for nk in nodes:
    for inp in nk["inputs"]:
        for lk in links:
            if lk[3]==nk["id"] and lk[4]==[i["name"] for i in nk["inputs"]].index(inp["name"]):
                inp["link"]=lk[0]
for nk in nodes:
    for out in nk["outputs"]:
        outs=[l for l in links if l[1]==nk["id"] and l[2]==[o["name"] for o in nk["outputs"]].index(out["name"])]
        out["links"]=[l[0] for l in outs] if outs else None
w={"id":"k2f-zidhan-scenes","version":0.4,"last_node_id":211,"last_link_id":lid,"nodes":nodes,"links":links}
out=r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2f_zidhan_scenes.json"
with io.open(out,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", out, "nodes:", len(nodes), "links:", len(links))
