# -*- coding: utf-8 -*-
r"""
Batch-generate all 10 Jaisal Kut intro R2V prompts using the H3 prompt model
(port 8104). Each shot's refs are listed in <Picture N> order (first = start
frame, last = end frame), so the model tags them correctly and describes the
ACTUAL character/scene from the images (not a generic "school kid").

PREREQ: the H3 prompt model is running on port 8104:
    D:\models\Writing\Qwen\run-minimax-h3-heretic.bat

RUN (after the model is up):
    & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "D:\models\vsCodeMcp\utilities\gen_all_h3_prompts.py"

Output: D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_<X>.txt  (one per shot)
Then paste each into the matching workflow's prompt node (or I can wire them in).
"""
import os, subprocess, sys

PY = r"E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe"
GEN = r"D:\models\vsCodeMcp\utilities\gen_h3_prompt.py"
KF = r"D:\models\vsCodeMcp\Jaisal-intro\keyframes"
OUT = r"D:\models\vsCodeMcp\Jaisal-intro\prompts"
DESC = r"D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_descriptions.txt"

# shot -> (description key, [ref filenames in <Picture N> order])
# Refs come ONLY from the keyframes folder (D069). 2-3 refs per shot (D020).
SHOTS = {
    "A": ("A", ["table empty.png", "jaisal_hand_under_the_table.png"]),
    "B": ("B", ["jaisal_hand_under_the_table.png", "jaisal_with_hand_on_table.png"]),
    # C is the CAMERA NODE shot (H3LocalCameraEditor) - its prompt is camera-driven.
    # We still generate a reference prompt for it (single ref = the start frame).
    "C": ("C", ["jaisal_head_left_back_side.png"]),
    "D": ("D", ["jaisal_head_180_dergree.png", "jaisal_with_hand_on_table.png"]),
    "E": ("E", ["jaisal_with_hand_on_table.png", "plants_Alive.png"]),
    "F": ("F", ["plants_Alive.png", "plants_dead.png"]),
    "G": ("G", ["plants_dead.png", "jaisal_gone_papers_alone.png"]),
    "H": ("H", ["jaisal_gone_papers_alone.png", "mic+paper_2k.png"]),
    "I": ("I", ["mic+paper_2k.png", "mic_without paper_final scene.png"]),
    "J": ("J", ["mic_without paper_final scene.png",
                 "obj_cricket_bat_00002_.png",
                 "obj_soccer_ball_00002_.png",
                 "obj_paper_smiley_00002_.png"]),
}


def parse_descriptions(path):
    """Parse the === X | ... === blocks into {key: text}."""
    blocks = {}
    cur = None
    buf = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("=== "):
                if cur:
                    blocks[cur] = "\n".join(buf).strip()
                key = line.split("|")[0].replace("===", "").strip()
                cur = key
                buf = []
            elif cur:
                buf.append(line)
    if cur:
        blocks[cur] = "\n".join(buf).strip()
    return blocks


def main():
    os.makedirs(OUT, exist_ok=True)
    descs = parse_descriptions(DESC)
    only = sys.argv[1:] if len(sys.argv) > 1 else list(SHOTS.keys())
    for key in only:
        if key not in SHOTS:
            print(f"skip {key} (not in SHOTS)")
            continue
        dkey, refs = SHOTS[key]
        desc = descs.get(dkey, "")
        if not desc:
            print(f"ERROR: no description for {dkey}")
            continue
        ref_paths = [os.path.join(KF, r) for r in refs]
        for rp in ref_paths:
            if not os.path.exists(rp):
                print(f"ERROR: missing ref {rp}")
                return
        out = os.path.join(OUT, f"shot_{key}.txt")
        descfile = os.path.join(OUT, f"_desc_{key}.txt")
        with open(descfile, "w", encoding="utf-8") as f:
            f.write(desc)
        print(f"\n===== {key} ({len(refs)} refs) =====")
        cmd = [PY, GEN, "--desc-file", descfile, "--refs", *ref_paths, "--out", out]
        r = subprocess.run(cmd)
        if r.returncode != 0:
            print(f"FAILED {key} (rc={r.returncode})")
    print("\nAll done. Prompts in:", OUT)


if __name__ == "__main__":
    main()
