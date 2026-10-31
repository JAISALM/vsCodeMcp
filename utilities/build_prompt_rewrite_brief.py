# -*- coding: utf-8 -*-
"""build_prompt_rewrite_brief.py (2026-10-31)

Assembles prompts\v91_dataset_prompts_boy_rewrite.md:
- all 8 CR Prompt List bodies from the untouched v91 file (VERBATIM)
- global suffix (LCPositive 2836) + generation settings
- our character descriptions (verbatim from our own approved prompts)
- rewrite task brief for ChatGPT / powerful model
"""
import json

W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
DST = r"D:\models\vsCodeMcp\prompts\v91_dataset_prompts_boy_rewrite.md"

d = json.load(open(W + r"\ref_krea2_v91_prograde_dataset.json", encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}

def first_prompt(fname):
    dd = json.load(open(W + "\\" + fname, encoding="utf-8"))
    n200 = [n for n in dd["nodes"] if n["id"] == 200][0]
    return json.loads(n200["widgets_values"][0])["prompts"][0]

jaisal_p1 = first_prompt("lora_dataset_jaisal.json")
zidhan_p1 = first_prompt("lora_dataset_zidhan.json")

# character description = our approved wording (from prompt 1, up to the
# "Change ONLY the setting" instruction part)
def char_desc(p):
    head = p.split("Change ONLY the setting and pose:")[0].strip()
    # strip the leading "Keep the man's face, " for a clean description
    if head.startswith("Keep the man's face, "):
        head = "Man, " + head[len("Keep the man's face, "):]
    return head

jaisal_desc = char_desc(jaisal_p1)
zidhan_desc = char_desc(zidhan_p1)

pos = nodes[2836].get("widgets_values", [""])[0]

LISTS = [257, 258, 259, 2770, 2842, 2843, 260, 2772]

def body_lines(nid):
    w = nodes[nid].get("widgets_values", ["", ""])
    return [ln for ln in w[1].split("\n") if ln.strip()]

out = []
A = out.append
A("# v91 Pro-Grade Dataset — Prompt Rewrite Brief (boy versions)")
A("")
A("Source: proven workflow `krea2IDEditProGradeCharacterDataset_v91VisionAssistant` (Civitai model 2805529, author lonecatone23).")
A("The 8 prompt lists below were written for the author's character — a young blonde woman (\"Anika\").")
A("We need the SAME lists for OUR characters (below). Keep the richness, structure, line counts and technical vocabulary — change the character, not the craft.")
A("")
A("## TASK FOR THE REWRITING MODEL")
A("")
A("1. For EACH of the 8 lists below, write a boy version: SAME number of lines, SAME order, each line a complete standalone prompt.")
A("2. Use the character descriptions verbatim (below). Jaisal is the PRIMARY — write all 8 lists for Jaisal unless a list is marked for Zidhan.")
A("3. Keep every technical element: camera terms (85mm f/1.8, shallow DOF, dutch angle, pov), lighting (golden hour, overcast rim light), skin texture (visible pores), color grade, bokeh, lens feel. Only change the character + anything inherently feminine.")
A("4. Inherently-feminine lines (lace bra/panties, bikini, dress, cleavage, jewelry) → replace with the best MALE equivalent that keeps the same SHOT TYPE and mood (e.g. \"red lace bra and panties, luxury penthouse\" → \"rolled-up white shirt, open collar, luxury penthouse\"; \"beach micro bikini, wet hair\" → \"beach, black t-shirt, wet hair, golden hour\").")
A("5. EVERY line must end with (or include): `ONLY ONE character, no other people, no duplicates.` — Krea2 has a known quirk of duplicating the subject (our own rule, D137).")
A("6. Every line should include the global suffix text below (it is also wired into the workflow, but the author re-states style words per line — keep both).")
A("7. Hair rules (Krea2 identity): face is LOCKED by the identity conditioning — prompts may re-state hair/build (author style, harmless) but must NOT fight the reference. Describe hair EXACTLY as in the character description.")
A("")
A("## CHARACTER DESCRIPTIONS (use verbatim)")
A("")
A("### Jaisal (char1 — PRIMARY)")
A("")
A("```")
A(jaisal_desc)
A("```")
A("")
A("### Zidhan (char2)")
A("")
A("```")
A(zidhan_desc)
A("```")
A("")
A("## GLOBAL SUFFIX (wired into the workflow — LCPositive node)")
A("")
A("```")
A(pos)
A("```")
A("")
A("## GENERATION SETTINGS (workflow-locked — do NOT change in prompts)")
A("")
A("- Base: Krea 2 Turbo (10 steps, cfg 1, euler/simple, denoise 1.0 = t2i)")
A("- Identity: krea2_identity_edit LoRA @1.0 + Krea2EditModelPatch ref_boost 2.0 / ref_boost_a 0.9 / fit + grounded encodes (768px)")
A("- References: `jaisal_final_ref.png` (face) + full-body ref → both pass through background-removal (BiRefNet) before the patch")
A("- Output: 1080x1350 (Instagram Portrait 4:5), seed FIXED at 13 (deterministic — same line + same seed = same image)")
A("- Post-chain: clarity pass + image adjust + auto-save to Dataset folder + .txt caption per image + face-similarity compare")
A("- Text cleanup (LCTextRemove): author's find-slots are EMPTY = no text removal active")
A("")
A("---")
A("")
A("## THE 8 AUTHOR LISTS (verbatim — rewrite each for Jaisal)")
A("")
for i, nid in enumerate(LISTS, 1):
    lines = body_lines(nid)
    A("### LIST %d — node %d — %d lines" % (i, nid, len(lines)))
    A("")
    A("```")
    A("\n".join(lines))
    A("```")
    A("")
    A("<!-- REWRITE FOR: -->")
    A("")
A("---")
A("")
A("## OUTPUT FORMAT (what to hand back)")
A("")
A("One block per list, same order, labelled `LIST n — node <id> (Jaisal)`, each line a complete prompt ending with the ONLY-ONE-character rule. Paste-ready: the lines go directly into the CR Prompt List node body (one prompt per line).")
A("")

with open(DST, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("saved", DST)
print("Jaisal desc:", jaisal_desc[:100], "...")
print("Zidhan desc:", zidhan_desc[:100], "...")
for i, nid in enumerate(LISTS, 1):
    print("LIST %d (node %d): %d lines" % (i, nid, len(body_lines(nid))))
