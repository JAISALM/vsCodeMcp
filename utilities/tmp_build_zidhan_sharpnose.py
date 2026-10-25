import json, io
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock_v2.json"
w = json.load(open(p, encoding="utf-8"))
INSTR = ("Keep the man's face, full short dense beard, and identity EXACTLY the same as the reference image. "
"SHARPEN the nose to a sharp, straight, well-defined prominent angular nose (a sharp pointed nose, NOT broad or "
"wide, NOT flat). Keep the full short dense beard. Enhance crisp photorealistic skin detail with real pores and "
"natural texture (NOT plastic, NOT airbrushed). Keep the plain white t-shirt, plain background, and lighting EXACTLY "
"the same. Change only the nose shape. ONLY ONE person, natural realistic skin with pores, face fully integrated, "
"no face-swap seam.")
NEG = ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, different face, wrong face, "
"changed face, face swap seam, duplicate character, multiple people, deformed hands, mutated limbs, bad anatomy, "
"extra fingers, watermark, text, logo")
for n in w["nodes"]:
    if n["id"] == 72:
        n["widgets_values"] = ["zidhan_ref_beard.png", "image"]
    if n["id"] == 113:
        n["widgets_values"] = ["zidhan_ref_beard.png", "image"]
    if n["id"] == 84:
        n["widgets_values"] = [INSTR, 768, ""]
    if n["id"] == 85:
        n["widgets_values"] = [NEG, 768, ""]
    if n["id"] == 53:
        n["widgets_values"] = [90101,"fixed",10,1,"euler","simple",0.4]
    if n["id"] == 29:
        n["widgets_values"] = ["k2f_zidhan_sharpnose"]
w["id"] = "k2f-zidhan-sharpnose"
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2f_zidhan_sharpnose.json"
with io.open(out,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", out)
