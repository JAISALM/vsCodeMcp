import json, io, copy
from PIL import Image
import os
in_dir = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
wf_dir = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
# downscale HD refs to 1152 wide (9:16 -> 1152x2048, matches proven face-ref size)
for src, dst in [("jaisal_hd_ref.png","jaisal_hd_ref_sm.png"),("zidhan_hd_ref.png","zidhan_hd_ref_sm.png")]:
    im = Image.open(os.path.join(in_dir, src)).convert("RGB")
    w,h = im.size
    nw = 1152; nh = int(h*nw/w)
    im = im.resize((nw,nh))
    im.save(os.path.join(in_dir,dst))
    print("downscaled", src, "->", dst, im.size)
JAIS_PROMPT = ("The man in the first image must have EXACTLY the face of the man in the second reference image: "
"slim face (not chubby), warm medium-brown skin, short-to-medium wavy black hair worn forward and down, "
"very short level-1 trimmed dark stubble (a faint shadow on the jaw and chin, NOT a full beard), soft rounded nose. "
"Keep the first image's pose, background, lighting, clothing and composition EXACTLY the same. Change only the face. "
"ONLY ONE person. Natural realistic skin with real pores, face fully integrated, no face-swap seam.")
ZID_PROMPT = ("The man in the first image must have EXACTLY the face of the man in the second reference image: "
"warm medium-brown skin, short clean halal fade crop haircut, full short dense trimmed beard, soft rounded nose. "
"Keep the first image's pose, background, lighting, clothing and composition EXACTLY the same. Change only the face. "
"ONLY ONE person. Natural realistic skin with real pores, face fully integrated, no face-swap seam.")
base = json.load(open(os.path.join(wf_dir, "krea2_face_lock_v2.json"), encoding="utf-8"))
def build(out_id, out_file, canvas, fref, posprompt, prefix, seed):
    w = copy.deepcopy(base)
    w["id"] = out_id
    byid = {n["id"]: n for n in w["nodes"]}
    byid[72]["widgets_values"] = [canvas, "image"]
    byid[113]["widgets_values"] = [fref, "image"]
    byid[84]["widgets_values"] = [posprompt, 768, ""]
    byid[29]["widgets_values"] = [prefix]
    byid[53]["widgets_values"] = [seed, "fixed", 10, 1, "euler", "simple", 0.35]
    p = os.path.join(wf_dir, out_file)
    with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
    print("WROTE", p)
build("krea2-face-lock-jaisal-hd","krea2_face_lock_jaisal_hd.json","fl_jaisal_base.png","jaisal_hd_ref_sm.png",JAIS_PROMPT,"krea2_fl_jaisal_hd",911)
build("krea2-face-lock-zidhan-hd","krea2_face_lock_zidhan_hd.json","fl_zidhan_base.png","zidhan_hd_ref_sm.png",ZID_PROMPT,"krea2_fl_zidhan_hd",912)
