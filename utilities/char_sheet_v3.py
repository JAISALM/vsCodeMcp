"""char sheet v3 — FACE-ONLY close-ups. No background/scene words at all (user directive).
Usage: python char_sheet_v3.py char1|char2   (sets 01 prompt + seed + prefix)
"""
import json, sys

char = sys.argv[1]
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\01_character_sheet.json"
j = json.load(open(p, encoding="utf-8"))

PROMPTS = {
"char1": {
 "pos": ("Close-up portrait of a 26-year-old Indian man, looking at the camera. "
         "Shoulder-length messy wavy black hair falling over the forehead, slight five-o'clock "
         "shadow, warm tanned skin, narrow face, serious calm expression, plain black cotton "
         "t-shirt. Natural even light, natural skin texture with visible pores and "
         "imperfections, shot on a 50mm lens, shallow depth of field, ONLY ONE character, "
         "looks like a real unposed photograph."),
 "neg": ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, "
         "cartoon, illustration, duplicate character, multiple people, watermark, logo, "
         "deformed face, bad eyes, extra fingers, bulky body, muscular, beard, full beard"),
 "seed": 42,
},
"char2": {
 "pos": ("Close-up portrait of a 26-year-old Indian man, looking at the camera. "
         "Wavy black hair tied in a loose top bun, rounder full face, light olive skin, "
         "clean-shaven, thick eyebrows, relaxed expression with slightly parted lips, plain "
         "white cotton t-shirt. Natural even light, natural skin texture with visible pores "
         "and imperfections, shot on a 50mm lens, shallow depth of field, ONLY ONE "
         "character, looks like a real unposed photograph."),
 "neg": ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, "
         "cartoon, illustration, duplicate character, multiple people, watermark, logo, "
         "deformed face, bad eyes, extra fingers, bulky body, muscular, beard, stubble, "
         "full beard"),
 "seed": 77,
},
}
data = PROMPTS[char]
for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["id"] == 300 and wv: wv[0] = data["pos"]; print(f"01 prompt -> {char} (face-only v3)")
    if n["id"] == 301 and wv: wv[0] = data["neg"]; print(f"01 negatives -> {char}")
    if n["id"] == 29 and wv: wv[0] = f"char_sheet/{char}"; print(f"01 prefix -> char_sheet/{char}")
    if n["id"] == 53 and wv and len(wv) >= 1: wv[0] = data["seed"]; print(f"01 seed -> {data['seed']} (headless needs explicit seed)")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved")
