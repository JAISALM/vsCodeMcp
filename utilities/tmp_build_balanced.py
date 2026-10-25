import json
src = r"D:\models\vsCodeMcp\utilities\tmp_fair_test_prompts.json"
p = json.load(open(src, encoding="utf-8"))
p0, p1, p5, p6, p7 = p[0], p[1], p[5], p[6], p[7]
z_start = p6.index("A candid phone snapshot")
scene_idx = p6.index("He is sitting alone on a simple wooden Kerala houseboat")
appearance = p6[z_start:scene_idx]
ending = p6[p6.index("He looks like a real young man"):]
assert appearance.rstrip().endswith("wavy-hair man.")
J1, J2, J3 = p0, p1, p5
Z1 = "dlorman, " + appearance + (
  "He is walking alone along a narrow Kerala backwater path during the monsoon. "
  "The camera is behind him at a slight three-quarter angle as he naturally looks back over one shoulder, "
  "his short cropped hair and trimmed beard clearly visible. He is wearing a plain white t-shirt. "
  "Lush tropical vegetation, soft mist, wet damp surfaces, subdued overcast daylight, humid monsoon atmosphere. "
  + ending)
Z2 = p6
Z3 = "dlorman, " + appearance + (
  "He is sitting in the back seat of an auto-rickshaw, street and market life blurred behind him, "
  "candid phone-shot framing ONLY ONE man in focus, no other people in the foreground, no text, no subtitles, "
  "no captions, no watermark, no logo, no speech bubbles, no dialogue text. " + ending)
P1 = p7
P2 = ("jeskvman and dlorman walking side by side along a narrow Kerala backwater path during the monsoon, "
  "lush tropical vegetation, soft mist, wet damp surfaces, subdued overcast daylight, medium shot from the waist up, "
  "both faces clearly visible, both in focus, natural ambient light, a real candid phone snapshot. "
  "The first man (jeskvman): 26-year-old young Malayali, warm medium-brown natural skin, ROUND youthful face, "
  "MEDIUM-LENGTH WAVY dark hair worn DOWN and loose around his neck and ears, a short PATCHY BEARD on his chin and jaw "
  "(uneven sparse dark patches), lean and fit, wearing a plain dark t-shirt. "
  "The second man (dlorman): young South Indian man, face round and full-cheeked with a short strong jaw, hair a short black "
  "halal haircut, very short faded sides and back, a short neat crop on top, no waves, no bun, a full short dark beard, "
  "neatly trimmed and shaped, dense on the chin, jawline and upper lip, lean and slim, wearing a plain white t-shirt. "
  "ONLY these two men, no other people, candid unposed snapshot, slight natural imperfections, NOT a studio portrait, "
  "NOT a stock photo.")
new = [J1, J2, J3, Z1, Z2, Z3, P1, P2]
assert len(new) == 8
json.dump(new, open(src, "w", encoding="utf-8"), indent=1)
open(r"D:\models\vsCodeMcp\utilities\fair_test_8_prompts_paste.txt", "w", encoding="utf-8").write("\r\n".join(new) + "\r\n")
print("NEW BALANCED SET (3 Jaisal / 3 Zidhan / 2 combined):")
for i, x in enumerate(new, 1):
    print(f"  [{i}] {x[:56]}")
