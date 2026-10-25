"""05 Qwen 2.1 character SHEET (LEEBLAAB workflow from reddit 1wsee1y, saved in
user\default\workflows\character sheet\). Copies the author's file into the app's
workflows folder as 05_qwen21_char_sheet.json and points it at our locked v6 sheets.
Usage: python set_qwen_sheet.py <jaisal|zidane>
Fixes: UNET int8_convrot -> bf16 (only variant installed); SaveImageAdvanced path
-> this machine; seeds 42/77 (headless lesson).
"""
import json, shutil, sys

char = sys.argv[1]
src = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\character sheet\LEEBLAAB-QwenImage21-Character-SHEET.json"
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\05_qwen21_char_sheet.json"
shutil.copyfile(src, p)
j = json.load(open(p, encoding="utf-8"))

PROMPT = {
"jaisal": ("1. 3:2 landscape composition on warm off-white paper with a thin ink-black border "
           "inset 3% from every edge and signature-gradient corner ticks in amber-brown to pale "
           "silver; seven zones defined as Zone A left metadata column x 0-18%, Zone B central "
           "hero x 18-58%, Zone C top-right turnaround row y 8-34%, Zone D mid-right expression "
           "row y 38-62%, Zone E bottom-left wardrobe panel y 66-95%, Zone F bottom-right notes "
           "strip y 66-95% x 58-97%, hairline ink-black rules between zones. "
           "2. Zone B central hero: full-body standing pose of the character from the reference "
           "image, a slim 26-year-old Indian man with medium-length wavy black hair and a thin "
           "patchy beard, light olive skin, wearing a plain black t-shirt and black trousers, "
           "relaxed confident stance, calm expression, soft even studio daylight. "
           "3. Zone C top-right turnaround row: three head-and-shoulders views of the exact same "
           "character, front view, three-quarter view, side profile view, identical face hair "
           "and skin tone in all three, small crisp labels beneath each reading \"FRONT\", "
           "\"3/4\", \"PROFILE\". "
           "4. Zone D mid-right expression row: four face close-ups of the exact same character "
           "showing calm, tired, smiling, and serious expressions, the face identical in all "
           "four, labels beneath reading \"CALM\", \"TIRED\", \"SMILING\", \"SERIOUS\". "
           "5. Zone E bottom-left wardrobe panel: full-body front view of the same character in "
           "the plain black t-shirt and black trousers outfit, arms relaxed at his sides, label "
           "above reading \"WARDROBE\". "
           "6. Zone A left metadata column: vertical title \"JAISAL\" in clean sans-serif "
           "capitals at the top, below it a small crisp data list reading \"AGE: 26\", \"BUILD: "
           "SLIM\", \"HAIR: MEDIUM WAVY BLACK\", \"BEARD: THIN PATCHY\", \"OUTFIT: BLACK TEE + "
           "BLACK TROUSERS\", every string legible and perfectly spelled. "
           "7. Zone F bottom-right notes strip: three short lines of small text reading "
           "\"IDENTITY: LOCKED TO REFERENCE\", \"SCENE: KERALA BACKWATER\", \"MOOD: QUIET "
           "CANDLELIT NIGHT\" in neat small-caps sans-serif. "
           "8. Design style: clean semi-realistic character design sheet, crisp ink linework "
           "with soft painterly shading, consistent proportions and an identical face across "
           "every single panel, no cluttered background, pure warm off-white paper. "
           "9. Lighting and palette: even soft studio daylight on every panel with no harsh "
           "shadows, warm off-white paper, ink-black linework, amber-brown accents, natural "
           "skin tone matching the reference image exactly. "
           "10. Quality: production-ready character design sheet, every panel perfectly "
           "consistent with the reference identity, ONLY ONE character appears in the entire "
           "sheet, no other people, no duplicates, no watermark."),
"zidane": ("1. 3:2 landscape composition on warm off-white paper with a thin ink-black border "
           "inset 3% from every edge and signature-gradient corner ticks in amber-brown to pale "
           "silver; seven zones defined as Zone A left metadata column x 0-18%, Zone B central "
           "hero x 18-58%, Zone C top-right turnaround row y 8-34%, Zone D mid-right expression "
           "row y 38-62%, Zone E bottom-left wardrobe panel y 66-95%, Zone F bottom-right notes "
           "strip y 66-95% x 58-97%, hairline ink-black rules between zones. "
           "2. Zone B central hero: full-body standing pose of the character from the reference "
           "image, an athletic muscular 26-year-old Indian man with a neat short halal-style "
           "haircut, short sides and natural short top, no wavy hair, thin patchy beard, light "
           "olive skin, wearing a plain white t-shirt and black trousers, relaxed easy stance "
           "with a small half-smile, soft even studio daylight. "
           "3. Zone C top-right turnaround row: three head-and-shoulders views of the exact same "
           "character, front view, three-quarter view, side profile view, identical face hair "
           "and skin tone in all three, small crisp labels beneath each reading \"FRONT\", "
           "\"3/4\", \"PROFILE\". "
           "4. Zone D mid-right expression row: four face close-ups of the exact same character "
           "showing calm, tired, smiling, and serious expressions, the face identical in all "
           "four, labels beneath reading \"CALM\", \"TIRED\", \"SMILING\", \"SERIOUS\". "
           "5. Zone E bottom-left wardrobe panel: full-body front view of the same character in "
           "the plain white t-shirt and black trousers outfit, arms relaxed at his sides, label "
           "above reading \"WARDROBE\". "
           "6. Zone A left metadata column: vertical title \"ZIDANE\" in clean sans-serif "
           "capitals at the top, below it a small crisp data list reading \"AGE: 26\", \"BUILD: "
           "ATHLETIC MUSCULAR\", \"HAIR: SHORT HALAL CUT\", \"BEARD: THIN PATCHY\", \"OUTFIT: "
           "WHITE TEE + BLACK TROUSERS\", every string legible and perfectly spelled. "
           "7. Zone F bottom-right notes strip: three short lines of small text reading "
           "\"IDENTITY: LOCKED TO REFERENCE\", \"SCENE: KERALA BACKWATER\", \"MOOD: WARM "
           "GOLDEN HOUR\" in neat small-caps sans-serif. "
           "8. Design style: clean semi-realistic character design sheet, crisp ink linework "
           "with soft painterly shading, consistent proportions and an identical face across "
           "every single panel, no cluttered background, pure warm off-white paper. "
           "9. Lighting and palette: even soft studio daylight on every panel with no harsh "
           "shadows, warm off-white paper, ink-black linework, amber-brown accents, natural "
           "skin tone matching the reference image exactly. "
           "10. Quality: production-ready character design sheet, every panel perfectly "
           "consistent with the reference identity, ONLY ONE character appears in the entire "
           "sheet, no other people, no duplicates, no watermark."),
}
REF = {"jaisal": "char1_sheet.png", "zidane": "char2_sheet.png"}
SEED = {"jaisal": 42, "zidane": 77}

for n in j["nodes"]:
    t = n.get("type")
    if t == "LoadImage" and n["id"] == 470:
        n["widgets_values"] = [REF[char], "image"]
    if t == "SaveImageAdvanced" and n["id"] == 461:
        n["widgets_values"] = [f"char_sheet_qwen/{char}", "png", "8-bit", "sRGB"]
    if t == "bc1c967a-7f6a-4be9-a372-dad16e4f28e3" and n["id"] == 459:
        wv = n["widgets_values"]
        wv[0] = PROMPT[char]
        wv[7] = SEED[char]
        wv[8] = "qwen_image_2.1_bf16.safetensors"   # int8_convrot not installed; bf16 is
        named = n.get("widgets_values_named", {})
        named["prompt"] = PROMPT[char]
        named["seed"] = SEED[char]
        named["unet_name"] = "qwen_image_2.1_bf16.safetensors"
        n["widgets_values_named"] = named
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print(f"05 qwen21 sheet set: {char} — ref {REF[char]}, seed {SEED[char]}, UNET bf16, save -> char_sheet_qwen/{char}")
