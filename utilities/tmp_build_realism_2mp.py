import json, io, copy

src = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1.json"
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_realism_2mp.json"
w = json.load(open(src, encoding="utf-8"))

# 1. collect the 6 old prompts verbatim
pe = next(n for n in w["nodes"] if n["type"] == "PixaromaPromptEach")
prompts = list(pe["widgets_values"])
assert len(prompts) == 6

# 2. rebuild prompteach in state-blob format (the reliable format)
blob = json.dumps({"version": 2, "prompts": prompts, "text": "", "split": "line",
                   "expand": True, "trim": True, "skipEmpty": True, "cap": 200,
                   "wiredAt": "after"}, ensure_ascii=False)
pe["widgets_values"] = [blob]
nvn = pe.get("widgets_values_named")
if isinstance(nvn, dict):
    nvn["prompteach"] = blob
else:
    pe["widgets_values_named"] = {"prompteach": blob}

# 3. resolution: 896x1120 -> 1152x2048 (2MP portrait, same as the user's t2i_face run)
el = next(n for n in w["nodes"] if n["type"] == "EmptySD3LatentImage")
el["widgets_values"] = [1152, 2048, 1]

# 4. save prefix
si = next(n for n in w["nodes"] if n["type"] == "SaveImage")
si["widgets_values"] = ["krea2_realism_2mp"]

with io.open(out, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", out, "nodes:", len(w["nodes"]))
print("latent:", el["widgets_values"], "prefix:", si["widgets_values"])

# paste file (6 prompts, one per line)
with io.open(r"D:\models\vsCodeMcp\utilities\realism_2mp_prompts_paste.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(prompts) + "\n")
print("paste file written")
