"""char refset v2 — author's recipe. Usage: python refset_v2.py char1|char2
(sets 02 instruction + ref image + prefix)
"""
import json, sys

char = sys.argv[1]
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json"
j = json.load(open(p, encoding="utf-8"))

INSTR = {
"char1": ("Candid smartphone photo of the SAME person from the reference: a 26-year-old Indian "
          "man, shoulder-length messy wavy black hair, slight five-o'clock shadow, warm tanned "
          "skin, plain black t-shirt, standing on a stone bridge over a calm river, moody "
          "overcast light, looking at the camera. ONLY ONE character, no other people, no "
          "duplicates. Natural unposed look, real skin texture with pores and imperfections, "
          "natural overcast lighting, slight motion blur, deep depth of field, looks like a "
          "real photo someone already took."),
"char2": ("Candid smartphone photo of the SAME person from the reference: a 26-year-old Indian "
          "man, wavy black hair in a loose top bun, rounder full face, light olive skin, "
          "clean-shaven, plain white t-shirt, sitting on the edge of a wooden boat on a calm "
          "backwater at golden hour, coconut palms in the background, looking off into the "
          "distance. ONLY ONE character, no other people, no duplicates. Natural unposed look, "
          "real skin texture with pores and imperfections, warm natural lighting, slight "
          "motion blur, deep depth of field, looks like a real photo someone already took."),
}
for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["id"] == 84 and wv: wv[0] = INSTR[char]; print(f"02 instruction -> {char}")
    if n["id"] == 72 and wv: wv[0] = f"{char}_sheet.png"; print(f"02 ref -> {char}_sheet.png")
    if n["id"] == 29 and wv: wv[0] = f"char_refset/{char}"; print(f"02 prefix -> char_refset/{char}")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved")
