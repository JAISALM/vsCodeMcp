# -*- coding: utf-8 -*-
"""build_v91_jaisal.py (2026-10-31)

Build krea2_v91_dataset_jaisal.json — machine-adapted copy of the proven
v91 pro-grade dataset workflow (Civitai 2805529, author lonecatone23):

1. Remove 4 nodes whose class is NOT installed (Fast Bypasser x2, Label,
   Node Collector — author-local pack) + their 6 links. Verified safe:
   they are the author's dead experimental post menu (feed no save node).
   Live chain intact: decode -> (denoise/color-match BYPASSED in author
   file) -> clarity -> adjust -> LCSaveImage + LCBatchImageComparer +
   LC123SaveText + LCAdvancedFolder.
2. Node 171 identity LoRA -> krea2_identity_edit_v1_2.safetensors (ours).
3. LoadImage 1 + 2782 -> jaisal_final_ref.png (face ref + body ref).
4. Node 2888 LCOptimizer -> 13-value widget shape (current 12-widget
   definition + spectrum) with ★ Recommended auto-picks on this machine.
5. Node 2843 CR Prompt List body -> Jaisal's 10 setting prompts (one per
   line = one prompt per line, CR_PromptList splits on \n). LCIndexSwitch
   [5, 8] = 0-based index 5 -> slot any_06 -> node 2843 (slot order
   257,258,259,2770,2842,2843,260,2772) — verified, no switch change.
"""
import json

W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
SRC = W + r"\ref_krea2_v91_prograde_dataset.json"
DST = W + r"\krea2_v91_dataset_jaisal.json"
DSJ = W + r"\lora_dataset_jaisal.json"

d = json.load(open(SRC, encoding="utf-8"))

# 1) Jaisal's 10 setting prompts from our dataset node 200 state blob
dsj = json.load(open(DSJ, encoding="utf-8"))
n200 = next(n for n in dsj["nodes"] if n["id"] == 200)
state = json.loads(n200["widgets_values"][0])
prompts = state["prompts"]
assert len(prompts) == 10, "expected 10 prompts, got %d" % len(prompts)

# 2) surgery: dead nodes + their links
dead = {2845, 2785, 2805, 2852}
dead_links = {41778, 41765, 41767, 41773, 41800, 41656}
d["nodes"] = [n for n in d["nodes"] if n["id"] not in dead]
d["links"] = [l for l in d["links"] if l[0] not in dead_links]
nodes = {n["id"]: n for n in d["nodes"]}
for nid, strip in ((2839, {41765}), (2833, {41767}), (2853, {41800})):
    for o in nodes[nid]["outputs"]:
        o["links"] = [x for x in (o.get("links") or []) if x not in strip]
for o in nodes[2784]["outputs"]:
    o["links"] = [x for x in (o.get("links") or []) if x != 41656]

# 3) widget fixes
n171 = nodes[171]
assert n171["type"] == "LoraLoaderModelOnly", n171["type"]
n171["widgets_values"][0] = "krea2_identity_edit_v1_2.safetensors"

n1 = nodes[1]
assert n1["type"] == "LoadImage", n1["type"]
assert len(n1["widgets_values"]) == 2, n1["widgets_values"]
n1["widgets_values"][0] = "jaisal_final_ref.png"

n2782 = nodes[2782]
assert n2782["type"] == "LoadImage", n2782["type"]
n2782["widgets_values"][0] = "jaisal_final_ref.png"

n2888 = nodes[2888]
assert n2888["type"] == "LCOptimizer", n2888["type"]
# 12 required widgets in definition order + optional spectrum
n2888["widgets_values"] = [
    "Krea 2 (Turbo)",   # base_model
    "Optimal",          # goal
    "\u2605 Recommended",  # model_file
    "\u2605 Recommended",  # text_encoder
    "\u2605 Recommended",  # vae
    "Auto",             # speed_ups
    "auto",             # attention
    "auto",             # fp16_accumulation
    "auto",             # step_cache
    "off",              # torch_compile
    "auto",             # qwen21_cache
    "auto",             # clip_type
    "auto",             # spectrum (optional)
]

n2843 = nodes[2843]
assert "CR" in n2843["type"], n2843["type"]
n2843["widgets_values"] = ["Jaisal - 10 settings", "\n".join(prompts), "", 0, 1000]

n2876 = nodes[2876]
assert n2876["type"] == "LCIndexSwitch", n2876["type"]
assert n2876["widgets_values"][:2] == [5, 8], n2876["widgets_values"]

# 4) counters
max_nid = max(n["id"] for n in d["nodes"])
max_lid = max(l[0] for l in d["links"])
d["last_node_id"] = max(d.get("last_node_id", 0), max_nid)
d["last_link_id"] = max(d.get("last_link_id", 0), max_lid)

with open(DST, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print("saved", DST)
print("nodes:", len(d["nodes"]), "links:", len(d["links"]),
      "last_node_id:", d["last_node_id"], "last_link_id:", d["last_link_id"])
print("prompts embedded:", len(prompts))
print("--- prompts ---")
for i, p in enumerate(prompts, 1):
    print("%2d. %s" % (i, p[:70]))
