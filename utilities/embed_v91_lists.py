# -*- coding: utf-8 -*-
"""embed_v91_lists.py (2026-10-31)

Embed Claude's rewritten boy lists (prompts\v91_dataset_prompts_jaisal_zidhan.md)
into the v91 dataset workflows:
- krea2_v91_dataset_jaisal.json  <- 8 Jaisal lists
- krea2_v91_dataset_zidhan.json  <- 8 Zidhan lists + zidhan refs
CR Prompt List bodies (node 257/258/259/2770/2842/2843/260/2772) replaced;
LoadImage 1 + 2782 set to the character's final ref. Everything else kept.
"""
import json
import re

MD = r"D:\models\vsCodeMcp\prompts\v91_dataset_prompts_kerala_v2.md"  # Kerala v2 (2026-10-31, verified + dups fixed)
W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
SRC = W + r"\krea2_v91_dataset_jaisal.json"  # machine-adapted v91 (validated 0/0)

EXPECT = {257: 20, 258: 20, 259: 25, 2770: 25, 2842: 25, 2843: 20, 260: 25, 2772: 7}

# --- parse the MD: "### LIST n — node <id> (<Char>) — N lines" + fenced body
txt = open(MD, encoding="utf-8").read()
sections = {}
cur = None
infence = False
for line in txt.split("\n"):
    m = re.match(r"### LIST \d+ — node (\d+) \((Jaisal|Zidhan)\) — \d+ lines", line.strip())
    if m:
        cur = (m.group(2), int(m.group(1)))
        sections[cur] = []
        infence = False
        continue
    if cur is None:
        continue
    if line.strip() == "```":
        infence = not infence
        continue
    if infence and line.strip():
        sections[cur].append(line.rstrip())

for char in ("Jaisal", "Zidhan"):
    for nid, n in EXPECT.items():
        got = len(sections.get((char, nid), []))
        assert got == n, "%s node %d: expected %d lines, got %d" % (char, nid, n, got)
    rule = sum(1 for l in sections[(char, 257)] + sections[(char, 260)]
               if "no other people" in l.lower())
    print("%s: all 8 lists parsed, line counts OK, D137-rule lines in sample: %d/%d"
          % (char, rule, len(sections[(char, 257)]) + len(sections[(char, 260)])))

# --- embed Jaisal into the jaisal file
d = json.load(open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}
for nid in EXPECT:
    assert "CR" in nodes[nid]["type"], nodes[nid]["type"]
    nodes[nid]["widgets_values"][1] = "\n".join(sections[("Jaisal", nid)])
nodes[1]["widgets_values"][0] = "jaisal_final_ref.png"
nodes[2782]["widgets_values"][0] = "jaisal_final_ref.png"
with open(W + r"\krea2_v91_dataset_jaisal.json", "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("saved krea2_v91_dataset_jaisal.json (Jaisal lists embedded)")

# --- embed Zidhan into the zidhan twin (same machine fixes, swap lists + refs)
for nid in EXPECT:
    nodes[nid]["widgets_values"][1] = "\n".join(sections[("Zidhan", nid)])
nodes[1]["widgets_values"][0] = "zidhan_final_ref.png"
nodes[2782]["widgets_values"][0] = "zidhan_final_ref.png"
with open(W + r"\krea2_v91_dataset_zidhan.json", "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("saved krea2_v91_dataset_zidhan.json (Zidhan lists embedded)")
