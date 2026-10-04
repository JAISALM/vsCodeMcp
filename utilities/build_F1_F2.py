"""Build jaisal_intro_F1_plants_listen.json + jaisal_intro_F2_plants_wither.json
from jaisal_intro_F_plants_die.json.

F1 (10s = 240f): E's ending (blooming) -> first leaf droops.
  refs: ref_image_0 = kf5_plants_alive_v9 (start), ref_image_1 = kf6_plants_dead_v9 (end direction)
  latent: Load clip 5 -> Save clip 6
F2 (12s = 288f): first leaf drooping -> fully wilted.
  refs: ref_image_0 = shot_F1_lastframe.png (user stages after F1 run), ref_image_1 = kf6_plants_dead_v9
  latent: Load clip 6 -> Save clip 7
G (unchanged): Load clip 7 -> Save clip 8  (G's LoadLatent clip_index must be bumped 6 -> 7)
"""
import json, copy, sys

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
PROMPT_DIR = r"d:\models\vsCodeMcp\Jaisal-intro\prompts"

def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def save(p, wf):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, indent=1)

def find(wf, nid):
    for n in wf["nodes"]:
        if n["id"] == nid:
            return n
    raise KeyError(nid)

def set_widget(node, idx, val):
    node["widgets_values"][idx] = val

def main():
    base = load(f"{WF_DIR}\\jaisal_intro_F_plants_die.json")

    # ---------- F1 ----------
    f1 = copy.deepcopy(base)
    f1["name"] = "jaisal_intro_F1_plants_listen"
    n136 = find(f1, 136)
    set_widget(n136, 3, 240)          # length frames: 10s @ 24fps
    n132 = find(f1, 132)
    set_widget(n132, 0, 10)           # PrimitiveFloat (math node input, keep consistent)
    n138 = find(f1, 138)
    with open(f"{PROMPT_DIR}\\shot_F1_plants_listen.txt", "r", encoding="utf-8") as f:
        n138["widgets_values"] = [f.read().strip()]
    # refs stay: 137 = kf5_plants_alive_v9 (start), 139 = kf6_plants_dead_v9 (end)
    # latent chain stays: 161 Load clip 5, 164 Save clip 6
    save(f"{WF_DIR}\\jaisal_intro_F1_plants_listen.json", f1)
    print("F1 written")

    # ---------- F2 ----------
    f2 = copy.deepcopy(base)
    f2["name"] = "jaisal_intro_F2_plants_wither"
    n136 = find(f2, 136)
    set_widget(n136, 3, 288)          # length frames: 12s @ 24fps
    n132 = find(f2, 132)
    set_widget(n132, 0, 12)
    n138 = find(f2, 138)
    with open(f"{PROMPT_DIR}\\shot_F2_plants_wither.txt", "r", encoding="utf-8") as f:
        n138["widgets_values"] = [f.read().strip()]
    # ref_image_0 -> F1's last frame (user stages after F1 run)
    n137 = find(f2, 137)
    set_widget(n137, 0, "shot_F1_lastframe.png")
    # ref_image_1 stays kf6_plants_dead_v9 (node 139)
    # latent chain: Load clip 6, Save clip 7
    n161 = find(f2, 161)
    set_widget(n161, 1, 6)
    n164 = find(f2, 164)
    set_widget(n164, 1, 7)
    save(f"{WF_DIR}\\jaisal_intro_F2_plants_wither.json", f2)
    print("F2 written")

    # ---------- G: bump LoadLatent 6 -> 7, SaveLatent 7 -> 8 ----------
    g = load(f"{WF_DIR}\\jaisal_intro_G_papers.json")
    changed = False
    for n in g["nodes"]:
        if n["type"] == "MiniMaxH3MotionContextLoadLatent" and n.get("widgets_values") == ["h3_context", 6]:
            n["widgets_values"][1] = 7
            changed = True
            print("G LoadLatent 6 -> 7")
        if n["type"] == "MiniMaxH3MotionContextSaveLatent" and n.get("widgets_values") == ["h3_context/clip", 7]:
            n["widgets_values"][1] = 8
            changed = True
            print("G SaveLatent 7 -> 8")
    if changed:
        save(f"{WF_DIR}\\jaisal_intro_G_papers.json", g)
    else:
        print("G: no clip-index change found (check manually)")

    print("done")

if __name__ == "__main__":
    main()
