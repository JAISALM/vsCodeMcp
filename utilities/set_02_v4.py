"""02 v4 — candid EMOTIONAL moments (fix: wooden/expressionless faces) + hair specs.
Usage: python set_02_v4.py <jaisal|zidane>
Locked settings from the sweep: 10 steps euler/simple cfg 1, grounding 768, ref_boost 4.
Jaisal: 4MP (clean there), seed 42.  Zidane: 2MP (4MP duplicates on this ref), seed 77.
"""
import json, sys

char = sys.argv[1]
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json"
j = json.load(open(p, encoding="utf-8"))

INSTR = {
"jaisal": ("A candid cinematic shot of a slim 26-year-old Indian man standing on a stone bridge "
           "over a quiet backwater in Kerala. Medium-length wavy black hair, thin patchy beard, "
           "plain black t-shirt and black trousers. Caught in a quiet moment: a soft, tired, "
           "thoughtful expression, eyes a little distant as if he is about to say something, "
           "head turned slightly to the side, not posing. Moody overcast light, rain streaks in "
           "the air, coconut palms in the distance. Shot on a 50mm lens, natural skin texture "
           "with visible pores, shallow depth of field, ONLY ONE character, no other people, "
           "looks like a real unposed photograph."),
"zidane": ("A candid cinematic shot of an athletic muscular 26-year-old Indian man sitting on the "
           "edge of a wooden boat on a calm backwater at golden hour. Neat short halal-style "
           "haircut, short on the sides with a natural short top, NO wavy hair, thin patchy "
           "beard, plain white t-shirt. Relaxed and at ease: a small easy half-smile, soft warm "
           "eyes, as if someone off camera just said something, head turned slightly, not "
           "posing. Coconut palms in the background, warm golden light on the water. Shot on a "
           "50mm lens, natural skin texture with visible pores, shallow depth of field, ONLY "
           "ONE character, no other people, looks like a real unposed photograph."),
}
CFG = {
"jaisal": {"mp": 4, "seed": 42, "ref": "jaisal_ref.png", "prefix": "char_v4/jaisal"},
"zidane": {"mp": 2, "seed": 77, "ref": "zidane_ref.png", "prefix": "char_v4/zidane"},
}
c = CFG[char]
for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["id"] == 53 and wv:
        wv[0] = c["seed"]; wv[2] = 10
    if n["id"] == 83 and wv:
        wv[0] = "16:9 (Widescreen)"; wv[1] = c["mp"]; wv[2] = 8
    if n["id"] == 84 and wv:
        wv[0] = INSTR[char]; wv[1] = 768
    if n["id"] == 72 and wv: wv[0] = c["ref"]
    if n["id"] == 97 and wv: wv[1] = 0.0
    if n["id"] == 29 and wv: wv[0] = c["prefix"]
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print(f"02 v4 set: {char} — {c['mp']}MP, 10 steps, seed {c['seed']}, grounding 768, prefix {c['prefix']}")
