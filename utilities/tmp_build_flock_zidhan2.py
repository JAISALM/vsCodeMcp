import json, io, copy, os
wf_dir = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
base = json.load(open(os.path.join(wf_dir, "krea2_face_lock_zidhan_hd.json"), encoding="utf-8"))
w = copy.deepcopy(base)
w["id"] = "krea2-face-lock-zidhan-hd-2"
byid = {n["id"]: n for n in w["nodes"]}
byid[84]["widgets_values"] = [
 "The man in the first image must have EXACTLY the face and facial hair of the man in the second reference image: "
 "warm medium-brown skin, short clean halal fade crop haircut, FULL short dense trimmed beard covering the jaw, chin and cheeks (dense, dark, neatly trimmed, NOT a light shadow), soft rounded nose. "
 "Keep the first image's pose, background, lighting, clothing and composition EXACTLY the same. Change only the face and beard. "
 "ONLY ONE person. Natural realistic skin with real pores, face fully integrated, no face-swap seam.", 768, ""]
byid[53]["widgets_values"] = [913, "fixed", 12, 1, "euler", "simple", 0.45]
byid[29]["widgets_values"] = ["krea2_fl_zidhan_hd2"]
p = os.path.join(wf_dir, "krea2_face_lock_zidhan_hd2.json")
with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", p)
