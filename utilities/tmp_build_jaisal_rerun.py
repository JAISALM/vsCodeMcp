import json, io
BASE_ID = "a 26-year-old young man from Kerala (a Keralite), warm medium TAN skin tone, slim build, short black hair, plain black t-shirt"
SKIN = "Natural photorealistic skin with real pores and subtle natural texture, natural film grain, high detail, sharp focus, ONLY ONE single person in the frame, no other people, no duplicates, no second person"
prompts = {
 "S2_house":   BASE_ID + ". He stands BEHIND A NORMAL KERALA HOUSE (traditional Kerala house with a sloped tiled roof, wooden structure, coconut and areca palm trees around, rural setting, overcast light). " + SKIN,
 "S3_interior":BASE_ID + ". He stands INSIDE A KERALA HOUSE (traditional Kerala home interior, wooden beams, tiled floor, warm interior light, simple wooden furniture, a window with a green view, rural Kerala). " + SKIN,
 "S4_bike":    BASE_ID + ". He is SITTING ON A MOTORCYCLE (a typical Kerala bike, rural Kerala road, green paddy fields and coconut trees around, overcast light). " + SKIN,
 "S5_7sfoot":  BASE_ID + ". He stands on a SMALL MINIMAL LOCAL 7'S FOOTBALL GROUND (a small local 7-a-side football pitch, green grass, small goals about 12 feet wide, white line markings, a low fence around the pitch, a few benches, NOT a big stadium, rural Kerala setting, overcast light). " + SKIN,
}
branches = [
 ("S2", 951, 961, 971, 531, 541, 291, 841, 9101, "k2v_jaisal_S2_house_r2", "S2_house"),
 ("S3", 952, 962, 972, 532, 542, 292, 842, 9102, "k2v_jaisal_S3_interior_r2", "S3_interior"),
 ("S4", 953, 963, 973, 533, 543, 293, 843, 9103, "k2v_jaisal_S4_bike_r2", "S4_bike"),
 ("S5", 954, 964, 974, 534, 544, 294, 844, 9104, "k2v_jaisal_S5_7sfoot_r2", "S5_7sfoot"),
]
def node(nid, ntype, pos, size, widgets, inputs=None, outputs=None, props=None):
    return {"id": nid, "type": ntype, "pos": pos, "size": size, "flags": {}, "order": 0, "mode": 0,
            "inputs": inputs or [], "outputs": outputs or [], "properties": props or {"Node name for S&R": ntype},
            "widgets_values": widgets}
nodes = []
nodes.append(node(55, "UNETLoader", [100,100], [280,90], ["krea2_turbo_fp8_scaled.safetensors","default"],
    outputs=[{"name":"MODEL","type":"MODEL","links":None}]))
nodes.append(node(56, "CLIPLoader", [100,250], [280,110], ["qwen3vl_4b_fp8_scaled.safetensors","krea2","default"],
    outputs=[{"name":"CLIP","type":"CLIP","links":None}]))
nodes.append(node(57, "VAELoader", [100,420], [280,70], ["qwen_image_vae.safetensors"],
    outputs=[{"name":"VAE","type":"VAE","links":None}]))
nodes.append(node(85, "CLIPTextEncode", [100,570], [400,200], [""],
    inputs=[{"name":"clip","type":"CLIP","widget":{"name":"clip"},"link":1}],
    outputs=[{"name":"CONDITIONING","type":"CONDITIONING","links":None}]))
nodes.append(node(90, "ConditioningZeroOut", [100,820], [280,60], [],
    inputs=[{"name":"conditioning","type":"CONDITIONING","widget":{"name":"conditioning"},"link":2}],
    outputs=[{"name":"CONDITIONING","type":"CONDITIONING","links":None}]))
nodes.append(node(82, "EmptySD3LatentImage", [100,940], [280,120], [1440,2560,1],
    outputs=[{"name":"LATENT","type":"LATENT","links":None}]))
for i,(name, turbo, realism, negpip, ksam, vdec, save, posid, seed, prefix, key) in enumerate(branches):
    y = 100 + i * 250
    nodes.append(node(turbo, "LoraLoaderModelOnly", [420,y], [300,100], ["krea2_turbo_lora_rank_64_bf16.safetensors",0.7],
        inputs=[{"name":"model","type":"MODEL","widget":{"name":"model"},"link":None}],
        outputs=[{"name":"MODEL","type":"MODEL","links":None}]))
    nodes.append(node(realism, "LoraLoaderModelOnly", [740,y], [300,100], ["Krea2-realism-V2.safetensors",0.8],
        inputs=[{"name":"model","type":"MODEL","widget":{"name":"model"},"link":None}],
        outputs=[{"name":"MODEL","type":"MODEL","links":None}]))
    nodes.append(node(negpip, "ApplyKrea2NegPiP", [1060,y], [300,140], [1.0,False,0,27,1],
        inputs=[{"name":"model","type":"MODEL","widget":{"name":"model"},"link":None},{"name":"clip","type":"CLIP","widget":{"name":"clip"},"link":None}],
        outputs=[{"name":"MODEL","type":"MODEL","links":None}]))
    nodes.append(node(posid, "CLIPTextEncode", [420,y+180], [420,220], [prompts[key]],
        inputs=[{"name":"clip","type":"CLIP","widget":{"name":"clip"},"link":None}],
        outputs=[{"name":"CONDITIONING","type":"CONDITIONING","links":None}]))
    nodes.append(node(ksam, "KSampler", [1380,y], [300,220], [seed,"fixed",12,1,"er_sde","simple",1],
        inputs=[{"name":"model","type":"MODEL","widget":{"name":"model"},"link":None},
                {"name":"positive","type":"CONDITIONING","widget":{"name":"positive"},"link":None},
                {"name":"negative","type":"CONDITIONING","widget":{"name":"negative"},"link":None},
                {"name":"latent_image","type":"LATENT","widget":{"name":"latent_image"},"link":None}],
        outputs=[{"name":"LATENT","type":"LATENT","links":None}]))
    nodes.append(node(vdec, "VAEDecode", [1700,y], [260,90], [],
        inputs=[{"name":"samples","type":"LATENT","widget":{"name":"samples"},"link":None},
                {"name":"vae","type":"VAE","widget":{"name":"vae"},"link":None}],
        outputs=[{"name":"IMAGE","type":"IMAGE","links":None}]))
    nodes.append(node(save, "SaveImage", [1980,y], [300,160], [prefix],
        inputs=[{"name":"images","type":"IMAGE","widget":{"name":"images"},"link":None}],
        outputs=[]))
links = []
lid = 0
def L(f, fs, t, ts, typ):
    global lid
    lid += 1
    links.append([lid, f, fs, t, ts, typ])
    return lid
L(56,0,85,0,"CLIP"); L(85,0,90,0,"CONDITIONING")
for (name, turbo, realism, negpip, ksam, vdec, save, posid, seed, prefix, key) in branches:
    L(55,0,turbo,0,"MODEL"); L(turbo,0,realism,0,"MODEL"); L(realism,0,negpip,0,"MODEL")
    L(negpip,0,ksam,0,"MODEL"); L(56,0,negpip,1,"CLIP"); L(56,0,posid,0,"CLIP")
    L(posid,0,ksam,1,"CONDITIONING"); L(90,0,ksam,2,"CONDITIONING"); L(82,0,ksam,3,"LATENT")
    L(ksam,0,vdec,0,"LATENT"); L(57,0,vdec,1,"VAE"); L(vdec,0,save,0,"IMAGE")
for nk in nodes:
    for inp in nk["inputs"]:
        for lk in links:
            if lk[3] == nk["id"] and lk[4] == [i["name"] for i in nk["inputs"]].index(inp["name"]):
                inp["link"] = lk[0]
for nk in nodes:
    for out in nk["outputs"]:
        outs = [l for l in links if l[1] == nk["id"] and l[2] == [o["name"] for o in nk["outputs"]].index(out["name"])]
        out["links"] = [l[0] for l in outs] if outs else None
w = {"id":"k2v-jaisal-scenes-rerun","version":0.4,"last_node_id":974,"last_link_id":lid,"nodes":nodes,"links":links}
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2v_jaisal_scenes_rerun.json"
with io.open(out,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", out, "nodes:", len(nodes), "links:", len(links))
