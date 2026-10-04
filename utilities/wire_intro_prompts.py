# -*- coding: utf-8 -*-
"""
Wire the 10 generated R2V prompts (Jaisal-intro\\prompts\\shot_<X>.txt) into the
matching intro shot workflows, replacing the buggy hand-crafted prompt node.

The prompt node is the PrimitiveStringMultiline node (node 138 in the R2V
templates). We set its widgets_values[0] to the new prompt text.

Shot C is the CAMERA NODE workflow - its prompt is camera-driven, so we skip it
(its prompt node, if any, is left as-is).

Run:
    cmd /c "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe D:\\models\\vsCodeMcp\\utilities\\wire_intro_prompts.py"
"""
import json, os

WFDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
PROMPTS = r"D:\models\vsCodeMcp\Jaisal-intro\prompts"

# shot key -> workflow filename
# NOTE: shot C is the CAMERA NODE (jaisal_intro_C_headtwist_180.json) — its prompt
# is the H3LocalCameraEditor `instruction` widget, set by
# update_C_camera_instruction.py (NOT this script). The R2V fallback
# (jaisal_intro_C_headtwist_180_r2v.json) is NOT wired here.
SHOTS = {
    "A": "jaisal_intro_A_walkin.json",
    "B": "jaisal_intro_B_setup.json",
    "D": "jaisal_intro_D_reverse.json",
    "E": "jaisal_intro_E_plants_grow.json",
    "F": "jaisal_intro_F_plants_die.json",
    "G": "jaisal_intro_G_vanish_burst.json",
    "H": "jaisal_intro_H_mic_paper.json",
    "I": "jaisal_intro_I_mic_alone.json",
    "J": "jaisal_intro_J_objects_join.json",
}

for key, wf in SHOTS.items():
    prompt_path = os.path.join(PROMPTS, "shot_%s.txt" % key)
    wf_path = os.path.join(WFDIR, wf)
    if not os.path.exists(prompt_path):
        print("MISSING prompt: %s" % prompt_path)
        continue
    with open(prompt_path, encoding="utf-8") as f:
        text = f.read().strip()
    with open(wf_path, encoding="utf-8") as f:
        d = json.load(f)
    # Find the PrimitiveStringMultiline node (the prompt node).
    wired = False
    for n in d["nodes"]:
        if n["type"] == "PrimitiveStringMultiline":
            n["widgets_values"] = [text]
            wired = True
            print("wired %s -> %s (node %d, %d chars)" % (key, wf, n["id"], len(text)))
            break
    if not wired:
        print("NO prompt node found in %s" % wf)
        continue
    with open(wf_path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)

print("\nDone. 9 R2V shots wired. Shot C = camera node (see update_C_camera_instruction.py).")
