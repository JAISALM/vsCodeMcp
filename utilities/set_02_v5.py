"""02 v5 — character SHEETS in normal weather (no rain, no boat), V2-LoRA @1.0,
kr2realism trigger tag (from civitai V2-LoRA examples), explicit clothing (NSFW-safe base).
Usage: python set_02_v5.py <jaisal|zidane>
Settings: 10 steps, 2MP 16:9, g768, ref_boost 4, V2 LoRA 1.0, seeds 42/77.
"""
import json, sys

char = sys.argv[1]
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json"
j = json.load(open(p, encoding="utf-8"))

INSTR = {
"jaisal": ("kr2realism, candid photograph of a slim 26-year-old Indian man standing on a quiet "
           "residential street. Medium-length wavy black hair, thin patchy beard, wearing a "
           "plain black t-shirt and dark trousers, fully clothed. Soft natural overcast "
           "daylight, clean simple background of modest houses, no rain. Calm relaxed "
           "expression, looking just off camera. Shot on a 50mm lens, natural skin texture "
           "with visible pores and fine skin detail, shallow depth of field, ONLY ONE "
           "character, no other people, looks like a real unposed photograph."),
"zidane": ("kr2realism, candid photograph of an athletic muscular 26-year-old Indian man "
           "sitting on a low wooden bench on a quiet residential street. Neat short "
           "halal-style haircut, short on the sides with a natural short top, NO wavy "
           "hair, thin patchy beard, wearing a plain white t-shirt and dark trousers, "
           "fully clothed. Soft natural daylight, clean simple background, no rain. "
           "Relaxed expression with a small easy half-smile, looking just off camera. "
           "Shot on a 50mm lens, natural skin texture with visible pores and fine skin "
           "detail, shallow depth of field, ONLY ONE character, no other people, looks "
           "like a real unposed photograph."),
}
CFG = {
"jaisal": {"seed": 42, "ref": "jaisal_ref.png", "prefix": "char_v5/jaisal_v2lora"},
"zidane": {"seed": 77, "ref": "zidane_ref.png", "prefix": "char_v5/zidane_v2lora"},
}
c = CFG[char]
for n in j["nodes"]:
    wv = n.get("widgets_values")
    if n["id"] == 53 and wv:
        wv[0] = c["seed"]; wv[2] = 10
    if n["id"] == 83 and wv:
        wv[0] = "16:9 (Widescreen)"; wv[1] = 2; wv[2] = 8
    if n["id"] == 84 and wv:
        wv[0] = INSTR[char]; wv[1] = 768
    if n["id"] == 72 and wv: wv[0] = c["ref"]
    if n["id"] == 97 and wv: wv[1] = 1.0     # V2 LoRA ON
    if n["id"] == 29 and wv: wv[0] = c["prefix"]
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print(f"02 v5 set: {char} — V2 LoRA 1.0, 2MP, 10 steps, seed {c['seed']}, normal weather, prefix {c['prefix']}")
