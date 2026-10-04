# -*- coding: utf-8 -*-
"""Remove 'schoolboy' / stray 'boy' references from the character description in
write_intro_prompts.py. Jaisal is a YOUNG MAN, not a schoolboy."""
import re

fp = r"D:\models\vsCodeMcp\utilities\write_intro_prompts.py"
s = open(fp, encoding="utf-8").read()

repls = [
    ("the young schoolboy Jaisal", "Jaisal, a young man"),
    ("the single boy <Subject 1>", "the single young man <Subject 1>"),
    ("NO second boy, NO duplicates", "NO second person, NO duplicates"),
    ("second boy, duplicate character", "second person, duplicate character"),
    ("the boy standing, the boy leaving", "the man standing, the man leaving"),
    ("a person, a boy", "a person, a young man"),
]
for old, new in repls:
    n = s.count(old)
    s = s.replace(old, new)
    print("%-40s -> %s  (%d)" % (old, new, n))

open(fp, "w", encoding="utf-8").write(s)

remaining = re.findall(r"schoolboy|\bboy\b", s, re.I)
print("\nRemaining 'schoolboy'/'boy' in script:", remaining if remaining else "NONE")
