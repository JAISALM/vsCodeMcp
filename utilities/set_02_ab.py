"""02 A/B runner config. Usage: python set_02_ab.py <jaisal|zidane> <pure|v2>
pure = V2 LoRA strength 0.0 ; v2 = 1.0. Same seed per character (fair A/B).
"""
import json, sys

char, mode = sys.argv[1], sys.argv[2]
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json"
j = json.load(open(p, encoding="utf-8"))

INSTR = {
"jaisal": ("A cinematic shot of a slim 26-year-old Indian man standing on a stone bridge over a "
           "quiet backwater in Kerala, looking straight at the camera. Medium-length wavy black "
           "hair, thin patchy beard, wearing a plain black t-shirt and black trousers. Moody "
           "overcast light, rain streaks in the air, coconut palms in the distance. Shot on a "
           "50mm lens, natural skin texture with visible pores, shallow depth of field, ONLY "
           "ONE character, no other people, looks like a real unposed photograph."),
"zidane": ("A cinematic shot of an athletic muscular 26-year-old Indian man sitting on the edge "
           "of a wooden boat on a calm backwater at golden hour, looking off into the distance. "
           "Short military-style haircut, thin patchy beard, wearing a plain white t-shirt. "
           "Coconut palms in the background, warm golden light on the water. Shot on a 50mm "
           "lens, natural skin texture with visible pores, shallow depth of field, ONLY ONE "
           "character, no other people, looks like a real unposed photograph."),
}
SEED = {"jaisal": 42, "zidane": 77}
REF = {"jaisal": "jaisal_ref.png", "zidane": "zidane_ref.png"}

for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["id"] == 84 and wv: wv[0] = INSTR[char]
    if n["id"] == 72 and wv: wv[0] = REF[char]
    if n["id"] == 53 and wv and len(wv) > 0: wv[0] = SEED[char]
    if n["id"] == 97 and wv: wv[1] = 0.0 if mode == "pure" else 1.0
    if n["id"] == 29 and wv: wv[0] = f"char_ab/{char}_{mode}"
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print(f"02 set: {char} {mode} (ref={REF[char]}, seed={SEED[char]}, V2lora={'0.0' if mode=='pure' else '1.0'}, prefix=char_ab/{char}_{mode})")
