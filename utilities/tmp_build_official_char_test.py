import json, io

src = r"D:\models\vsCodeMcp\utilities\official_image_krea2_turbo_t2i.json"
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_official_char_test.json"
w = json.load(open(src, encoding="utf-8"))

PROMPT = ("A high-resolution amateur shot of a 26-year-old young Malayali man, warm medium-brown natural skin, "
          "round youthful face, medium-length wavy dark hair worn down and loose, a short patchy beard, "
          "wearing a plain dark t-shirt. He stands on a narrow backwater path in Kerala at golden hour, "
          "a houseboat far behind him.")

nodes = {n["id"]: n for n in w["nodes"]}
inst = nodes[30]
wv = inst["widgets_values"]
assert len(wv) == 14, len(wv)
wv[0]  = PROMPT
wv[1]  = True
wv[2]  = False
wv[3]  = 512
# wv[4], wv[5] = width/height (linked to ResolutionSelector)
wv[6]  = 42
wv[7]  = True
wv[8]  = "krea2fp_v2_ep64.safetensors"
wv[9]  = 1.0
wv[10] = "jeskvman"

nodes[29]["widgets_values"] = ["krea2_official_char_test"]

sub = w["definitions"]["subgraphs"][0]
sn = {n["id"]: n for n in sub["nodes"]}
sn[15]["widgets_values"] = ["krea2fp_v2_ep64.safetensors", 1.0]
sn[19]["widgets_values"] = [PROMPT]
sn[27]["widgets_values"] = ["", "jeskvman", ", "]
sn[23]["widgets_values"] = [True]

with io.open(out, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", out)
