import json, io
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows_archive\2026-10-18\krea2_t2i_character.json"
w = json.load(open(p, encoding="utf-8"))
for n in w["nodes"]:
    t = n["type"]
    wv = n.get("widgets_values")
    if t == "PixaromaPromptEach":
        blob = wv[0] if wv and isinstance(wv[0], str) and wv[0].startswith("{") else None
        if blob:
            state = json.loads(blob)
            print(n["id"], t, "STATE BLOB, prompts:", len(state.get("prompts", [])))
            for i, pr in enumerate(state.get("prompts", [])):
                print("   p%d: %s" % (i+1, pr[:100]))
        else:
            print(n["id"], t, "format:", type(wv).__name__, "len", len(wv or []))
            for i, pr in enumerate(wv or []):
                print("   p%d: %s" % (i+1, str(pr)[:100]))
    elif t in ("UNETLoader","CLIPLoader","VAELoader","LoraLoaderModelOnly","KSampler","EmptySD3LatentImage","EmptyLatentImage","SaveImage","FameGridColorFinish","ModelSamplingFlux","CLIPTextEncode"):
        s = str(wv)[:70]
        print(n["id"], t, s)
print("last_link_id:", w.get("last_link_id"), "last_node_id:", w.get("last_node_id"))
