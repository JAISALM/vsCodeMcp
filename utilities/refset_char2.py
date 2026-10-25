"""Switch 02 to char2: ref image + boat instruction + prefix."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json"
j = json.load(open(p, encoding="utf-8"))
for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["id"] == 84 and wv:
        wv[0] = ("Candid smartphone photo of the SAME person from the reference: a 26-year-old Indian man, "
                 "black hair tied in a loose top bun, slim build, clean-shaven, plain white t-shirt, sitting "
                 "on the edge of a wooden boat on a calm backwater at golden hour, coconut palms in the "
                 "background, looking off into the distance. ONLY ONE character, no other people, no "
                 "duplicates. Natural unposed look, real skin texture with pores and imperfections, warm "
                 "natural lighting, slight motion blur, deep depth of field, looks like a real photo someone "
                 "already took.")
        print("02 instruction -> char2 boat")
    if n["id"] == 72 and wv:
        wv[0] = "char2_sheet.png"; print("02 ref -> char2_sheet.png")
    if n["id"] == 29 and wv:
        wv[0] = "char_refset/char2"; print("02 save prefix -> char_refset/char2")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved")
