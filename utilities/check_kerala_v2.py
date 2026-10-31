# -*- coding: utf-8 -*-
"""check_kerala_v2.py — full verification battery on
prompts\v91_dataset_prompts_kerala_v2.md (Claude's Kerala rewrite)."""
import re
import collections

p = r"D:\models\vsCodeMcp\prompts\v91_dataset_prompts_kerala_v2.md"
txt = open(p, encoding="utf-8").read()
lines = txt.split("\n")
print("total lines:", len(lines), "chars:", len(txt))

EXPECT = {257: 20, 258: 20, 259: 25, 2770: 25, 2842: 25, 2843: 20, 260: 25, 2772: 7}

# 1) structure + bodies
blocks = {}
cur = None
infence = False
for l in lines:
    m = re.match(r"### LIST \d+ — node (\d+) \((Jaisal|Zidhan)\) — (\d+) lines", l.strip())
    if m:
        cur = (m.group(2), int(m.group(1)))
        blocks[cur] = []
        infence = False
        continue
    if cur is None:
        continue
    if l.strip() == "```":
        infence = not infence
        continue
    if infence and l.strip():
        blocks[cur].append(l.rstrip())

print("sections found:", len(blocks))
print("--- line counts vs expected (20/20/25/25/25/20/25/7 per char) ---")
ok = True
for ch in ("Jaisal", "Zidhan"):
    for nid in (257, 258, 259, 2770, 2842, 2843, 260, 2772):
        ls = blocks.get((ch, nid), [])
        exp = EXPECT[nid]
        flag = "OK" if len(ls) == exp else "*** MISMATCH"
        if len(ls) != exp:
            ok = False
        print("  %s node %d: %d (expected %d) %s" % (ch, nid, len(ls), exp, flag))
print("COUNTS ALL OK" if ok else "COUNT PROBLEMS FOUND")

# 2) identity block at line start + character-specific words
print()
JA_HEAD = "Kerala (South Indian) man"
for ch in ("Jaisal", "Zidhan"):
    allp = [l for nid in EXPECT for l in blocks[(ch, nid)]]
    withhead = sum(1 for l in allp if l.strip().startswith(JA_HEAD))
    withbeard = sum(1 for l in allp if "beard" in l.lower())
    wavy = sum(1 for l in allp if "wavy" in l.lower())
    darkskin = sum(1 for l in allp if "dark brown skin" in l.lower())
    print("%s: %d/%d start with Kerala identity head | dark-brown-skin lines: %d | beard: %d | wavy: %d"
          % (ch, withhead, len(allp), darkskin, withbeard, wavy))

# 3) forbidden words
print()
badwords = ["blonde", "blond", "fair skin", "fair complexion", "fair-complexion",
            "white skin", "pale skin", "light skin", "caucasian", "european",
            "american look", "western face"]
found_any = False
for ch in ("Jaisal", "Zidhan"):
    allp = [l for nid in EXPECT for l in blocks[(ch, nid)]]
    for w in badwords:
        hits = [l for l in allp if w in l.lower()]
        if hits:
            found_any = True
            print("%s FORBIDDEN [%s] x%d e.g.: %s" % (ch, w, len(hits), hits[0][:110]))
if not found_any:
    print("forbidden-word scan: CLEAN")

# 4) D137 rule + global suffix + relative-skin check
print()
for ch in ("Jaisal", "Zidhan"):
    allp = [l for nid in EXPECT for l in blocks[(ch, nid)]]
    withrule = sum(1 for l in allp if "no other people" in l.lower() and "no duplicates" in l.lower())
    withsuffix = sum(1 for l in allp if "photorealistic" in l.lower())
    rel = [l for l in allp if "same as the reference" in l.lower() or "same as reference" in l.lower()]
    print("%s: D137-rule %d/%d | suffix %d/%d | relative-skin lines: %d"
          % (ch, withrule, len(allp), withsuffix, len(allp), len(rel)))

# 5) duplicates + european residue + kerala presence
allp_all = [l for ch in ("Jaisal", "Zidhan") for nid in EXPECT for l in blocks[(ch, nid)]]
c = collections.Counter(allp_all)
print()
print("unique prompt lines: %d of %d | duplicated values: %d"
      % (len(c), len(allp_all), sum(1 for v in c.values() if v > 1)))
resid = ["penthouse", "cashmere", "antique", "rembrandt", "silk scarf", "seductive",
         "mirror selfie", "cleavage", "high heel", "jewel", "lipstick", "makeup", "glitter"]
print("--- european/glamour residue ---")
for w in resid:
    hits = [l for l in allp_all if w in l.lower()]
    if hits:
        print("RESIDUE [%s] x%d e.g.: %s" % (w, len(hits), hits[0][:110]))
ker = ["kerala", "backwater", "paddy", "coconut", "monsoon", "kochi", "veranda",
       "laterite", "houseboat", "malabar", "keralite", "temple"]
print("--- kerala presence ---")
for w in ker:
    n = sum(1 for l in allp_all if w in l.lower())
    if n:
        print("KERALA [%s] x%d" % (w, n))
