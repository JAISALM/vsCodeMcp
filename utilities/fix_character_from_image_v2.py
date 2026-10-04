# -*- coding: utf-8 -*-
"""
Properly fix all 10 R2V prompts: remove ALL character appearance text
(face, hair, clothing, build). The character identity comes from the
reference images, not from text. <Subject 1> = "the young boy shown in
the reference images". <Picture N> tags point to the actual images.
"""
import os, re

PROMPTS_DIR = r"D:\models\vsCodeMcp\Jaisal-intro\prompts"

# Character appearance patterns to remove
CHAR_PATTERNS = [
    r"Jaisal, a young man - short dark hair, a rose-pink collared shirt, full-length black trousers, a black school bag",
    r"Jaisal, a young man - short dark hair, a rose-pink collared shirt, full-length black trousers, a black school bag,",
    r"short dark hair, a rose-pink collared shirt, full-length black trousers, a black school bag",
    r"face, short dark hair, rose-pink shirt, black trousers, black bag retained",
    r"the single young man <Subject 1>",
    r"the single boy <Subject 1>",
]

# Replacement: just reference the character from the image
CHAR_REF = "the young boy shown in the reference images"

for key in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
    path = os.path.join(PROMPTS_DIR, "shot_%s.txt" % key)
    if not os.path.exists(path):
        print("MISSING: %s" % path)
        continue
    with open(path, encoding="utf-8") as f:
        text = f.read()
    
    # Remove character appearance descriptions
    for pattern in CHAR_PATTERNS:
        text = re.sub(pattern, CHAR_REF, text)
    
    # Fix the retention_analysis line
    text = re.sub(r"fully_preserved - face, short dark hair, rose-pink shirt, black trousers, black bag retained",
                  "fully_preserved - identity, face, hair, clothing and build come from the reference images", text)
    
    # Fix "the single young man <Subject 1>" -> "the single young boy <Subject 1>"
    text = text.replace("the single young man <Subject 1>", "the single young boy <Subject 1>")
    text = text.replace("the single boy <Subject 1>", "the single young boy <Subject 1>")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("fixed %s" % key)

print("\n=== Verify shot_A.txt ===")
with open(os.path.join(PROMPTS_DIR, "shot_A.txt"), encoding="utf-8") as f:
    print(f.read()[:800])
