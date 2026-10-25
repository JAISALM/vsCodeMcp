import json

for name in ["01_character_sheet", "02_identity_refset"]:
    p = rf"D:\models\vsCodeMcp\challenge\consistent-short\workflows\{name}.json"
    j = json.load(open(p, encoding="utf-8"))
    print(f"=== {name} ===")
    for n in j["nodes"]:
        t = n["type"]
        if t in ("KSampler", "CLIPTextEncode", "LoadImage", "SaveImage", "UNETLoader", "LoraLoaderModelOnly", "LoraLoader", "EmptySD3LatentImage", "Krea2EditGroundedEncode", "Krea2EditModelPatch", "GroundedEncode"):
            wv = n.get("widgets_values")
            if wv and isinstance(wv, list) and len(wv) > 300:
                wv = [ (x[:120] + "...") if isinstance(x, str) and len(x) > 120 else x for x in wv ]
            print(f"  {n['id']:>4} {t:<22} {wv}")
