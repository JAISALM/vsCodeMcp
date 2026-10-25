"""Switch 01 to the char2 sheet (char1 run already done)."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\01_character_sheet.json"
j = json.load(open(p, encoding="utf-8"))
for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["id"] == 300 and wv:
        wv[0] = ("Character sheet photograph of a 26-year-old Indian man, black hair tied in a loose top bun, "
                 "slim build, clean-shaven, wearing a plain white t-shirt and black trousers, sitting on the "
                 "edge of a wooden boat on a calm backwater at golden hour, natural skin texture, realistic "
                 "fabric, cinematic photograph, warm rim light, ONLY ONE character, no other people, no duplicates")
        print("01 prompt -> char2")
    if n["id"] == 29 and wv:
        wv[0] = "char_sheet/char2"
        print("01 save prefix -> char_sheet/char2")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved")
