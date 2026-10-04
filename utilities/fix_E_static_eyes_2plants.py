import json, os, shutil

E_PATH = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_E_plants.json"
BAK_DIR = r"d:\models\vsCodeMcp\workflow_backups"
PROMPT_SAVE = r"d:\models\vsCodeMcp\Jaisal-intro\prompts\shot_E_plants_grow_v5_static_eyes_2plants.txt"
os.makedirs(BAK_DIR, exist_ok=True)

REPLACEMENTS = [
    # 1. CAMERA: push-in -> STATIC
    ("The camera is a MEDIUM to CLOSE push (50mm to 85mm) — a slow, smooth push-in that tightens the frame from a medium shot to a close-up over the whole take.",
     "The camera is a STATIC medium shot (50mm, eye level), COMPLETELY LOCKED — no movement, no pan, no zoom, no push-in, no orbit. The frame size NEVER changes for the whole take."),
    # 2. EYES: downcast -> visible + soft eye contact
    ("his eyes shift FIRST, his gaze dropping to the bare table, a small breath of surprise catching in his chest as he begins to speak",
     "his eyes are VISIBLE and directed toward the camera — a soft, natural eye contact (NOT fully staring, NOT looking down, NOT looking at the table — his eyes are clearly visible and level), a small breath of surprise catching in his chest as he begins to speak"),
    # 3. PLANTS: exactly 2, matching the reference
    ("a tiny green stem pushes UP through the wooden table surface on his left, then another on his right; the growth is slow and organic — the stems physically EMERGE and rise, NOT a fade-in. His eyes FOLLOW the stem as it pushes through",
     "EXACTLY TWO small plants grow — one tiny stem pushes UP through the wooden table surface on his left, then one on his right (matching the reference image — NO more than two plants, NO four plants, NO extra stems); the growth is slow and organic — the stems physically EMERGE and rise, NOT a fade-in. His eyes stay VISIBLE and level toward the camera, glancing at the stem as it pushes through"),
    # 4. beat 3: camera still + eyes visible
    ("the stems grow into white roses that slowly open and bloom; the camera finishes its slow push-in to a close-up. His gaze lifts from the rose",
     "the two plants grow into white roses that slowly open and bloom; the camera stays COMPLETELY STILL. His eyes stay visible, directed toward the camera"),
    # 5. summary: 2 plants lock
    ("one tiny stem pushes through the table surface, another follows, a rose slowly opens, small plants populate the table",
     "EXACTLY TWO small plants (one on each side of his hands, matching the reference image — NO more, NO less) grow: one tiny stem pushes through the table surface, the other follows, a rose slowly opens"),
    # 6. negatives: add zoom/plant-count/eyes-down
    ("fade-in plants, camera shake, fast zoom, sudden jump.",
     "fade-in plants, four plants, extra plants, more than two plants, extra stems, multiple stems, camera movement, zoom in, push-in, dolly, camera shake, fast zoom, sudden jump, looking down, eyes downcast, eyes hidden, face turned down, head bowed, gaze at the table."),
    # 7. FINAL REQUIREMENT: static + eyes + 2 plants
    ("natural micro-expressions of WONDER (eyes shift first, gaze follows the rising stem, a slight softening smile, a small breath of surprise), a SLOW MEDIUM-to-CLOSE push-in (50mm to 85mm), the table goes from EMPTY (first frame) to PLANTS GROWN AND BLOOMING (final frame), plants GROW (not fade in)",
     "natural micro-expressions of WONDER (eyes VISIBLE and directed toward the camera, a slight softening smile, a small breath of surprise), a STATIC medium shot (50mm, completely locked, NO zoom), his eyes VISIBLE and directed toward the camera (soft eye contact, NOT looking down), the table goes from EMPTY (first frame) to EXACTLY TWO PLANTS GROWN AND BLOOMING (final frame, matching the reference image), plants GROW (not fade in)"),
]

with open(E_PATH, "r", encoding="utf-8") as f:
    wf = json.load(f)
shutil.copy(E_PATH, os.path.join(BAK_DIR, "jaisal_intro_E_plants.json.pre_v5_static_eyes_2plants.bak"))

for n in wf["nodes"]:
    if n["id"] == 138:
        p = n["widgets_values"][0]
        for old, new in REPLACEMENTS:
            if old not in p:
                print("!! NOT FOUND:", old[:70])
            else:
                p = p.replace(old, new)
        n["widgets_values"] = [p]

with open(E_PATH, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False)
with open(PROMPT_SAVE, "w", encoding="utf-8") as f:
    f.write(p)
print("E v5 written. Backup in", BAK_DIR)
print("Prompt saved", PROMPT_SAVE)
