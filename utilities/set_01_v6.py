"""01 v6 — clean character sheets via t2i (NO reference => no rain/scene carry-over).
V2 LoRA @1.0 (node 96), kr2realism trigger, explicit clothing (NSFW-safe base),
8 steps (author's t2i range, stronger adherence), 2MP 16:9.
Usage: python set_01_v6.py <jaisal|zidane>
"""
import json, sys

char = sys.argv[1]
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\01_character_sheet.json"
j = json.load(open(p, encoding="utf-8"))

INSTR = {
"jaisal": ("kr2realism, candid photograph of a slim 26-year-old Indian man standing on a quiet "
           "residential street. Medium-length wavy black hair, thin patchy beard, sharp "
           "cheekbones, clean jawline, light olive skin, wearing a plain black t-shirt and "
           "dark trousers, fully clothed. Soft natural overcast daylight, clean simple "
           "background of modest houses, clear dry weather, no rain. Calm relaxed expression, "
           "looking just off camera. Shot on a 50mm lens, natural skin texture with visible "
           "pores and fine skin detail, shallow depth of field, ONLY ONE character, no other "
           "people, looks like a real unposed photograph."),
"zidane": ("kr2realism, candid photograph of an athletic muscular 26-year-old Indian man "
           "sitting on a low wooden bench on a quiet residential street. Neat short "
           "halal-style haircut, short on the sides with a natural short top, no wavy hair, "
           "thin patchy beard, light olive skin, wearing a plain white t-shirt and dark "
           "trousers, fully clothed. Soft natural daylight, clean simple background, clear "
           "dry weather, no rain. Relaxed expression with a small easy half-smile, looking "
           "just off camera. Shot on a 50mm lens, natural skin texture with visible pores "
           "and fine skin detail, shallow depth of field, ONLY ONE character, no other "
           "people, looks like a real unposed photograph."),
}
SEED = {"jaisal": 42, "zidane": 77}

for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["id"] == 96 and wv: wv[1] = 1.0            # V2 LoRA ON
    if n["id"] == 82 and wv: wv = [2048, 1152, 1]  # 16:9 2MP landscape
    if n["id"] == 300 and wv: wv[0] = INSTR[char]
    if n["id"] == 53 and wv:
        wv[0] = SEED[char]; wv[2] = 8
    if n["id"] == 29 and wv: wv[0] = f"char_v6/{char}_v2lora"
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print(f"01 v6 set: {char} — t2i, V2 LoRA 1.0, 8 steps, 2MP 16:9, seed {SEED[char]}")
