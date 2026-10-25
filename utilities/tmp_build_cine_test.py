import json, io

base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_raw_qtest.json"
out  = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_cine_test.json"

P1 = ("jeskvman, cinematic film still, close-up portrait of a 26-year-old young Malayali man, warm medium-brown "
"natural skin with visible pores and natural skin texture, round youthful face, MEDIUM-LENGTH WAVY dark hair "
"worn down and loose, a short patchy beard, wearing a plain dark t-shirt. He stands on a narrow backwater "
"path in Kerala, a houseboat far behind him. Composition: tight close-up, his face fills the frame, 85mm "
"lens, shallow depth of field, soft creamy bokeh. Lighting: low golden hour sun rim-lighting the waves of his "
"hair and the edge of his jaw, warm amber highlights, cool blue undertones in the shadows. Mood: quiet, "
"introspective, a real young man in his mid-20s. Medium: 35mm film photograph, Kodak Portra 400 color "
"science, visible film grain, muted cinematic color grade.")
P2 = ("jeskvman, cinematic film still, extreme left profile of a 26-year-old young Malayali man, warm "
"medium-brown natural skin, round youthful face, MEDIUM-LENGTH WAVY dark hair worn down and loose, a short "
"patchy beard, wearing a plain dark t-shirt. He looks out over a low stone wall toward a misty backwater at "
"overcast morning. Composition: full side view, tele compression flattening the distant palms, rule of "
"thirds with his face on the right, deep atmospheric perspective. Lighting: soft overcast diffuse light, long "
"soft shadows, muted teal-and-amber palette. Mood: contemplative, still. Medium: 35mm film photograph, "
"analog film grain, muted desaturated grade, shallow depth of field on the face.")
P3 = ("jeskvman and dlorman, cinematic film still of a casual football match on a floodlit pitch at night. "
"The first man (jeskvman): 26-year-old young Malayali, warm medium-brown natural skin, round youthful face, "
"MEDIUM-LENGTH WAVY dark hair worn down, short patchy beard, plain dark t-shirt. The second man (dlorman): "
"young South Indian man, round full-cheeked face, short black halal haircut with faded sides, full short dark "
"beard neatly trimmed, plain white t-shirt. The first man passes the ball to the second man, both in motion, "
"both faces clearly visible and distinguishable. Composition: wide medium shot, low camera angle, stadium "
"floodlights towering behind them, wet grass reflecting the lights. Lighting: hard white floodlight from "
"above, volumetric light beams cutting through night haze, deep shadows. Mood: raw, kinetic. Medium: 35mm "
"film photograph at night, high ISO grain, muted cinematic grade, slight motion blur on the ball.")

w = json.load(open(base, encoding="utf-8"))
state = {"version":2, "prompts":[P1, P2, P3], "text":"", "split":"line", "expand":True, "trim":True, "skipEmpty":True, "cap":200, "wiredAt":"after"}
blob = json.dumps(state, separators=(",", ":"))
for n in w["nodes"]:
    if n["id"] == 55:
        n["widgets_values"] = ["krea2_turbo_fp8_scaled.safetensors", "default"]
    elif n["id"] == 53:
        n["widgets_values"] = [42, "randomize", 10, 1, "euler", "simple", 1]
    elif n["id"] == 82:
        n["widgets_values"] = [1920, 1080, 1]
    elif n["id"] == 200:
        n["widgets_values"] = [blob]
        n["widgets_values_named"] = {"prompteach": blob}
    elif n["id"] == 29:
        n["widgets_values"] = ["krea2_cine_test"]
with io.open(out, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", out)
