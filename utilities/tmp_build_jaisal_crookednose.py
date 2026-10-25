import json, io
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_face_lock_v2.json"
w = json.load(open(p, encoding="utf-8"))
INSTR = ("Keep the man's face, MEDIUM WAVY black hair (falling to eyebrow length), identity, slim build, plain black "
"t-shirt, plain background, and lighting EXACTLY the same as the reference image. Change ONLY the nose: give him a "
"slightly CROOKED, naturally bent nose (a subtly deviated nose bridge, NOT perfectly straight, NOT a soft rounded "
"nose, NOT a sharp angular pointed nose). Keep the almond eyes, thin lips, clean-shaven faint stubble, and everything "
"else EXACTLY the same. ONLY ONE person, natural realistic skin with pores, face fully integrated, no face-swap seam.")
NEG = ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, different face, wrong face, "
"changed face, face swap seam, duplicate character, multiple people, deformed hands, mutated limbs, bad anatomy, "
"extra fingers, watermark, text, logo, beard, stubble beard")
for n in w["nodes"]:
    if n["id"] == 72:
        n["widgets_values"] = ["jaisal_ref.png", "image"]
    if n["id"] == 113:
        n["widgets_values"] = ["jaisal_ref.png", "image"]
    if n["id"] == 84:
        n["widgets_values"] = [INSTR, 768, ""]
    if n["id"] == 85:
        n["widgets_values"] = [NEG, 768, ""]
    if n["id"] == 53:
        n["widgets_values"] = [90201,"fixed",10,1,"euler","simple",0.4]
    if n["id"] == 29:
        n["widgets_values"] = ["k2f_jaisal_crookednose"]
w["id"] = "k2f-jaisal-crookednose"
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2f_jaisal_crookednose.json"
with io.open(out,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", out)
