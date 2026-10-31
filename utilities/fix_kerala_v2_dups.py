# -*- coding: utf-8 -*-
"""fix_kerala_v2_dups.py (2026-10-31) — line-index based.

LIST 8 (node 2772) lines 3-4 are verbatim copies of LIST 4 (node 2770) lines 20-21
in BOTH characters -> fixed seed 13 + same prompt = same image = 4 redundant dataset
images. Replace ONLY the LIST 8 lines 3-4 (line-index surgery) with distinct Kerala
scenes; identity block + craft + suffix + D137 rule preserved.
"""
import re

p = r"D:\models\vsCodeMcp\prompts\v91_dataset_prompts_kerala_v2.md"
lines = open(p, encoding="utf-8").read().split("\n")

JA3 = ("Kerala (South Indian) man, about 26 years old, warm dark brown skin with natural "
       "texture, medium wavy black hair falling to eyebrow length, slightly crooked "
       "naturally bent nose, dark brown almond eyes, thin lips, clean-shaven with faint "
       "stubble, lean slim build. Standing in the doorway of an old laterite-walled home, "
       "one hand resting on the wooden doorframe, plain black t-shirt and dark trousers, "
       "face half in shadow half in warm lamplight, soft evening glow spilling out onto "
       "the veranda. ignore original clothing completely, photorealistic, high-detail "
       "natural skin texture with pores, soft natural lighting, sharp focus, ONLY ONE "
       "character, no other people, no duplicates.")
JA4 = ("Kerala (South Indian) man, about 26 years old, warm dark brown skin with natural "
       "texture, medium wavy black hair falling to eyebrow length, slightly crooked "
       "naturally bent nose, dark brown almond eyes, thin lips, clean-shaven with faint "
       "stubble, lean slim build. Seated on a low wooden stool beside a brass "
       "filter-coffee setup, mid-sip, plain black t-shirt, warm tungsten kitchen light, "
       "steam rising off a small glass cup, high-detail natural skin texture with "
       "visible pores, 85mm f/1.8, gentle film grain. ignore original clothing "
       "completely, photorealistic, high-detail natural skin texture with pores, soft "
       "natural lighting, sharp focus, ONLY ONE character, no other people, no "
       "duplicates.")
ZI3 = ("Kerala (South Indian) man, about 26 years old, warm dark brown skin with natural "
       "texture, short neat black hair, full short dense black beard, dark brown eyes, "
       "lean slim build. Sitting on the carved wooden bench of an old Kerala houseboat "
       "deck, elbows on knees, white t-shirt and dark trousers, quiet thoughtful gaze "
       "across the backwater, late afternoon light on the water, high-detail natural "
       "skin texture with visible pores, 85mm f/1.8, gentle film grain. ignore "
       "original clothing completely, photorealistic, high-detail natural skin texture "
       "with pores, soft natural lighting, sharp focus, ONLY ONE character, no other "
       "people, no duplicates.")
ZI4 = ("Kerala (South Indian) man, about 26 years old, warm dark brown skin with natural "
       "texture, short neat black hair, full short dense black beard, dark brown eyes, "
       "lean slim build. Standing in a narrow monsoon-damp lane in old Kochi, just "
       "after a shower, white t-shirt and rolled-up jeans, wet cobbles reflecting warm "
       "window light, soft diffused overcast light, high-detail natural skin texture "
       "with visible pores, 85mm f/1.8, gentle film grain. ignore original clothing "
       "completely, photorealistic, high-detail natural skin texture with pores, soft "
       "natural lighting, sharp focus, ONLY ONE character, no other people, no "
       "duplicates.")

# locate LIST 8 (node 2772) headings, then their block body line indices
targets = []  # (char, [body line indices in `lines`])
i = 0
while i < len(lines):
    m = re.match(r"### LIST \d+ — node 2772 \((Jaisal|Zidhan)\) — 7 lines", lines[i].strip())
    if m:
        # find opening fence after heading
        j = i + 1
        while lines[j].strip() != "```":
            j += 1
        body = list(range(j + 1, j + 8))  # 7 body lines
        assert all(lines[k].strip() for k in body), "unexpected blank inside LIST 8 body"
        targets.append((m.group(1), body))
        i = j + 8
    else:
        i += 1
assert len(targets) == 2, "expected 2 LIST-8 sections, found %d" % len(targets)

repl = {"Jaisal": (JA3, JA4), "Zidhan": (ZI3, ZI4)}
for ch, body in targets:
    new3, new4 = repl[ch]
    print("%s old line3: %s" % (ch, lines[body[2]][:90]))
    print("%s old line4: %s" % (ch, lines[body[3]][:90]))
    # sanity: old lines must be the duplicated scenes
    assert "Sitting on the floor against a wall" in lines[body[2]], lines[body[2]][:80]
    assert "festival string lights" in lines[body[3]], lines[body[3]][:80]
    lines[body[2]] = new3
    lines[body[3]] = new4
    print("%s NEW line3: %s" % (ch, new3[90:190]))

open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("saved — LIST 8 lines 3-4 replaced for both characters")
