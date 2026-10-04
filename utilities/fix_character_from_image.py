# -*- coding: utf-8 -*-
"""
1. Find the 2BZ character-sheet workflow file.
2. Fix all 10 R2V prompts: <Subject 1> now references the character FROM THE
   IMAGE (Image_00001_ = monochrome character sheet), not from text description.
3. Re-wire the prompts into the 9 R2V workflows.
"""
import os, glob, json

# --- 1. Find the 2BZ workflow ---
print("=== Finding 2BZ workflow ===")
search_dirs = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows",
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user",
    r"D:\models\vsCodeMcp",
]
found_2bz = []
for root in search_dirs:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git", "models", "output", "input", "keyframes", "obj_refs", "v1", "v2", "v3", "v4", "v5", "v7", "v8", "v9", "base", "kf2_headset", "obj_refs")]
        for fn in filenames:
            if fn.lower().endswith(".json") and ("2bz" in fn.lower() or "character_sheet" in fn.lower()):
                p = os.path.join(dirpath, fn)
                found_2bz.append(p)
                print("  FOUND:", p)

if not found_2bz:
    print("  NOT FOUND in standard dirs. Searching all .json in workflows folder...")
    wfdir = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
    for fn in os.listdir(wfdir):
        if fn.lower().endswith(".json"):
            p = os.path.join(wfdir, fn)
            try:
                s = open(p, encoding="utf-8", errors="ignore").read()
                if "2BZ" in s or "character_sheet" in s.lower():
                    found_2bz.append(p)
                    print("  FOUND (content):", p)
            except Exception:
                pass

print()

# --- 2. Fix the prompts: character from image, not text ---
print("=== Fixing prompts: character from image ===")
PROMPTS_DIR = r"D:\models\vsCodeMcp\Jaisal-intro\prompts"

# The character reference image (monochrome character sheet)
CHAR_REF = "Image_00001_"

# For each shot, the character identity comes from the reference image.
# We replace the text description with a reference to the image.
# The <Picture N> tags already point to the actual images, so we just need
# to make <Subject 1> reference the character FROM the image.

# Read the current prompts and fix the character description
for key in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
    path = os.path.join(PROMPTS_DIR, "shot_%s.txt" % key)
    if not os.path.exists(path):
        print("  MISSING: %s" % path)
        continue
    with open(path, encoding="utf-8") as f:
        text = f.read()
    
    # Replace the character description with a reference to the image
    # Old: "<Subject 1> is Jaisal, a young man - short dark hair, a rose-pink collared shirt, full-length black trousers, a black school bag"
    # New: "<Subject 1> is the young boy shown in the reference images (identity from image, not text)"
    
    # Find and replace the character description line
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("<Subject 1> is"):
            # Replace with image-reference
            new_lines.append("<Subject 1> is the young boy shown in the reference images - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.")
        else:
            new_lines.append(line)
    
    new_text = "\n".join(new_lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("  fixed %s" % key)

print()

# --- 3. Re-wire the prompts into the 9 R2V workflows ---
print("=== Re-wiring prompts into workflows ===")
WFDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
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
    prompt_path = os.path.join(PROMPTS_DIR, "shot_%s.txt" % key)
    wf_path = os.path.join(WFDIR, wf)
    if not os.path.exists(prompt_path):
        print("  MISSING prompt: %s" % prompt_path)
        continue
    with open(prompt_path, encoding="utf-8") as f:
        text = f.read().strip()
    with open(wf_path, encoding="utf-8") as f:
        d = json.load(f)
    wired = False
    for n in d["nodes"]:
        if n["type"] == "PrimitiveStringMultiline":
            n["widgets_values"] = [text]
            wired = True
            print("  wired %s -> %s (%d chars)" % (key, wf, len(text)))
            break
    if not wired:
        print("  NO prompt node in %s" % wf)
        continue
    with open(wf_path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)

print()
print("=== DONE ===")
print("Character identity now comes from the reference image, not text.")
print("2BZ workflow found:", found_2bz if found_2bz else "NOT FOUND")
