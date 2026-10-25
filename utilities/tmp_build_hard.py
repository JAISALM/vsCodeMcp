import json

J = ("a 26-year-old young Malayali man, warm medium-brown natural skin, round youthful face, "
     "MEDIUM-LENGTH WAVY dark hair worn down and loose, a short patchy beard, lean and fit, "
     "wearing a plain dark t-shirt")
Z = ("a young South Indian man, warm medium-brown natural skin, round full-cheeked face, "
     "short black halal haircut with very short faded sides, a full short dark beard neatly trimmed and shaped, "
     "lean and slim, wearing a plain white t-shirt")
END = ("He looks like a real young man in his mid-20s: youthful fresh face, natural young skin, no wrinkles, no aging. "
       "Candid unposed snapshot caught in a real moment, natural ambient light, looks like a real photo someone took "
       "on their phone, slight natural imperfections, a real ordinary person, NOT a studio portrait, NOT a headshot, "
       "NOT a stock photo, NOT a professional photo.")

J4 = J.replace("wearing a plain dark t-shirt", "wearing a plain white football kit and black football boots")

p = []
p.append("jeskvman, " + J + " EXTREME LEFT PROFILE, his face fully in side view, sharp jawline and nose silhouette "
         "clearly readable, looking out over a low stone wall, overcast daylight, candid phone snapshot from the side. " + END)
p.append("jeskvman, " + J + " EXTREME CLOSE-UP, his face fills the entire frame, sharp focus on his eyes and iris, "
         "the patchy beard and natural skin texture clearly visible, a slight relaxed smile, soft window light. " + END)
p.append("jeskvman, " + J + " SLIGHT LOW ANGLE looking up at him, he stands with arms crossed, serious expression, "
         "backlit golden evening light, rim light on his wavy hair, candid phone snapshot. " + END)
p.append("jeskvman, " + J4 + " FULL BODY, running at full sprint on a green football pitch, ball at his feet, "
         "background in motion blur, dynamic low angle, overcast daylight, candid phone snapshot. " + END)
p.append("jeskvman, " + J + " standing in a dense crowd of men at a stadium after a match, many other faces around him, "
         "he is the clear focus, shallow depth of field, camera flashes in the darkness, candid phone snapshot. " + END)
p.append("dlorman, " + Z + " EXTREME RIGHT PROFILE, walking toward the camera on a wet street at night, full body visible, "
         "streetlight reflections on the pavement, rain droplets in the air, his short crop and full beard clearly readable "
         "in the side view, candid phone snapshot. " + END)
p.append("dlorman, " + Z + " CLOSE-UP, laughing with his mouth open, eyes crinkled with joy, natural warm evening light, "
         "candid phone snapshot. " + END)
p.append("jeskvman and dlorman playing a casual football match on a floodlit pitch at night. "
         "The first man (jeskvman): 26-year-old young Malayali, warm medium-brown natural skin, round youthful face, "
         "MEDIUM-LENGTH WAVY dark hair worn down, short patchy beard, lean and fit, wearing a plain dark t-shirt. "
         "The second man (dlorman): young South Indian man, round full-cheeked face, short black halal haircut with faded sides, "
         "full short dark beard neatly trimmed, lean and slim, wearing a plain white t-shirt. "
         "The first man passes the ball to the second man, both in motion, both faces clearly visible and distinguishable, "
         "stadium floodlights, wet grass, candid phone snapshot, slight natural imperfections, NOT a studio photo, NOT a stock photo.")

assert len(p) == 8
heads = [x[:14] for x in p]
json.dump(p, open(r"D:\models\vsCodeMcp\utilities\hard_test_prompts.json", "w", encoding="utf-8"), indent=1)
open(r"D:\models\vsCodeMcp\utilities\hard_test_8_prompts_paste.txt", "w", encoding="utf-8").write("\r\n".join(p) + "\r\n")
print("HARD TEST SET (compact identity descriptions, 8 prompts):")
labels = ["Jaisal EXTREME LEFT PROFILE", "Jaisal EXTREME CLOSE-UP", "Jaisal low-angle arms crossed",
          "Jaisal FULL-BODY sprint pitch", "Jaisal CROWD stadium", "Zidhan night profile full-body",
          "Zidhan laughing close-up", "BOTH football action night"]
for i, (x, l) in enumerate(zip(p, labels), 1):
    print(f"  [{i}] {l:32s} | {x[:44]}")
