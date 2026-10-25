"""Lock in Krea2Realism_V1 as the Krea2 base in app workflows 01/02 (consistent-short).
- Back up originals as *_oldturbo.json
- UNET krea2_turbo_fp8_scaled -> Krea2Realism_V1
- KSampler steps 10 -> 6 (author's Krea2Realism setting: euler/simple cfg 1)
- 01: Krea2-realism-V2 LoRA strength -> 0.0 (pure base = approved A/B output)
- 01: char1 sheet prompt + negatives + save prefix
- 02: char1 bridge instruction + save prefix + ref filename -> char1 sheet
Also report: node 113 (ref_person.png) mode/links, and whether its file exists.
"""
import json, shutil, os

base = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"
inp = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"

def load(name):
    return json.load(open(f"{base}\\{name}.json", encoding="utf-8"))

def save(name, j):
    json.dump(j, open(f"{base}\\{name}.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- 01 ----------
j = load("01_character_sheet")
shutil.copy(f"{base}\\01_character_sheet.json", f"{base}\\01_character_sheet_oldturbo.json")
nodes = {n["id"]: n for n in j["nodes"]}
for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["type"] == "UNETLoader" and wv and wv[0] == "krea2_turbo_fp8_scaled.safetensors":
        wv[0] = "Krea2Realism_V1.safetensors"; print("01 UNET swapped")
    if n["type"] == "KSampler" and wv and len(wv) >= 3:
        wv[2] = 6; print(f"01 KSampler steps -> 6 ({n['id']})")
    if n["type"] == "LoraLoaderModelOnly" and wv and wv[0] == "Krea2-realism-V2.safetensors":
        wv[1] = 0.0; print(f"01 V2 LoRA strength -> 0.0 ({n['id']})")
    if n["id"] == 300:
        wv[0] = ("Character sheet photograph of a 26-year-old Indian man, wavy wet black hair, "
                 "slim build, clean-shaven, wearing a plain black t-shirt and black trousers, "
                 "standing on a misty backwater path, natural skin texture, realistic fabric, "
                 "cinematic photograph, soft overcast light, ONLY ONE character, no other people, no duplicates")
        print("01 prompt -> char1")
    if n["id"] == 301:
        wv[0] = ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, "
                 "cartoon, illustration, duplicate character, multiple people, watermark, logo, "
                 "deformed face, bad eyes, extra fingers, bulky body, muscular, beard, stubble")
        print("01 negatives -> char1")
    if n["id"] == 29:
        wv[0] = "char_sheet/char1"
        print("01 save prefix -> char_sheet/char1")
save("01_character_sheet", j)

# ---------- 02 ----------
j = load("02_identity_refset")
shutil.copy(f"{base}\\02_identity_refset.json", f"{base}\\02_identity_refset_oldturbo.json")
for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["type"] == "UNETLoader" and wv and wv[0] == "krea2_turbo_fp8_scaled.safetensors":
        wv[0] = "Krea2Realism_V1.safetensors"; print("02 UNET swapped")
    if n["type"] == "KSampler" and wv and len(wv) >= 3:
        wv[2] = 6; print(f"02 KSampler steps -> 6 ({n['id']})")
    if n["id"] == 84 and wv:
        wv[0] = ("Candid smartphone photo of the SAME person from the reference: a 26-year-old Indian man, "
                 "wavy wet black hair, slim build, clean-shaven, plain black t-shirt, standing on a stone "
                 "bridge over a calm river, moody overcast light, looking at the camera. ONLY ONE character, "
                 "no other people, no duplicates. Natural unposed look, real skin texture with pores and "
                 "imperfections, natural overcast lighting, slight motion blur, deep depth of field, looks "
                 "like a real photo someone already took.")
        print("02 instruction -> char1 bridge")
    if n["id"] == 72 and wv:
        wv[0] = "char1_sheet.png"; print("02 ref -> char1_sheet.png")
    if n["id"] == 29 and wv:
        wv[0] = "char_refset/char1"; print("02 save prefix -> char_refset/char1")
    if n["id"] == 113:
        print(f"02 node 113 (ref_person.png): mode={n.get('mode')} links_out={n['outputs'][0].get('links') if n['outputs'] else None} widgets={wv}")
save("02_identity_refset", j)

print("ref_person exists:", os.path.exists(os.path.join(inp, "ref_person.png")))
print("ref_character exists:", os.path.exists(os.path.join(inp, "ref_character.png")))
print("saved")
