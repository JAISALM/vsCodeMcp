"""char sheet v2 — author's recipe (raw/candid, natural language, distinct face per character).
Usage: python char_sheet_v2.py char1|char2   (sets 01 prompt + negatives + prefix)
"""
import json, sys

char = sys.argv[1]
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\01_character_sheet.json"
j = json.load(open(p, encoding="utf-8"))

PROMPTS = {
"char1": {
 "pos": ("Unposed candid photograph of a 26-year-old Indian man standing in the middle of a "
         "rain-soaked village road in Kerala at dusk. He has shoulder-length messy wavy black "
         "hair falling over his forehead, a slight five-o'clock shadow, warm tanned skin, a "
         "narrow face and a serious quiet expression, wearing a plain black cotton t-shirt that "
         "is slightly wet from the rain. Wet asphalt with puddle reflections, rain streaks in "
         "the air, old painted buildings and coconut palms on both sides, soft overcast light. "
         "Shot on a 50mm lens, natural skin texture with visible pores, shallow depth of field, "
         "ONLY ONE character, no other people, looks like a real unposed photograph."),
 "neg": ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, "
         "cartoon, illustration, duplicate character, multiple people, watermark, logo, "
         "deformed face, bad eyes, extra fingers, bulky body, muscular"),
},
"char2": {
 "pos": ("Unposed candid photograph of a 26-year-old Indian man standing on a wet city street "
         "in South India during rain. He has wavy black hair swept up into a loose top bun, a "
         "rounder full face, light olive skin, clean-shaven, thick eyebrows, and a relaxed "
         "expression with slightly parted lips, wearing a plain white cotton t-shirt and black "
         "trousers. Rain streaks in the air, brick buildings, parked bicycles and green plants "
         "in the background, soft overcast light. Shot on a 50mm lens, natural skin texture "
         "with visible pores, shallow depth of field, ONLY ONE character, no other people, "
         "looks like a real unposed photograph."),
 "neg": ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, 3d render, "
         "cartoon, illustration, duplicate character, multiple people, watermark, logo, "
         "deformed face, bad eyes, extra fingers, bulky body, muscular, beard, stubble"),
},
}
data = PROMPTS[char]
for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["id"] == 300 and wv: wv[0] = data["pos"]; print(f"01 prompt -> {char}")
    if n["id"] == 301 and wv: wv[0] = data["neg"]; print(f"01 negatives -> {char}")
    if n["id"] == 29 and wv: wv[0] = f"char_sheet/{char}"; print(f"01 prefix -> char_sheet/{char}")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved")
