# -*- coding: utf-8 -*-
"""
Rebuild Shot C (jaisal_intro_C_starting_2ref.json) as a SINGLE STATIC MEDIUM SHOT.

User direction (2026-09-15):
  - NO rotation / NO orbit / NO camera movement - just a static medium shot.
  - All 4 English lines in one take, clear lip movement.
  - At the "welcome to the Jaisal Kut" line, the words "The Jaisal Kut" FLASH in
    WHITE letters in the background BEHIND the character for a split second.

Changes:
  1. Delete node 139 (the 90deg ref LoadImage) + its link (301) - the orbit
     middle-checkpoint is no longer needed.
  2. Clear node 136 (R2V) ref_image_1 input link -> None (now single ref).
  3. Rewrite node 138 (prompt) to the static-shot + title-flash prompt.
  4. Keep 240 frames (10s), 1344x768.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\rebuild_C_static.py"
"""
import json
import shutil
import os

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_starting_2ref.json"
PROMPT_OUT = r"D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_C_static.txt"

PROMPT = """subject_definitions:
<Subject 1> is the boy in <Picture 1>. His identity, face, hair, clothing and build come ENTIRELY from the reference image - do not alter his appearance in any way.
<Picture 1> is the ONLY frame anchor: the boy seated at the table, facing the camera, hands resting on the table edge.

summary:
[reference generation] A 10-second STATIC medium shot. <Subject 1> is seated at the table, facing the camera, hands on the table edge. The camera is COMPLETELY STILL - no orbit, no pan, no zoom, no movement. The boy stays in the same seated pose the whole time, speaking four quiet lines with clear lip movement. In the final seconds, as he says his last line, the words "The Jaisal Kut" flash in WHITE letters in the background behind him for a split second.

retention_analysis:
<Subject 1> (all frames): fully_preserved - his appearance is identical in every frame, exactly as in <Picture 1>.
<Picture 1> (the whole shot): fully_preserved - the boy's pose, the table, the chair and the lighting are identical in every frame.

detailed_description:
MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: ONE single STATIC medium shot - the camera is COMPLETELY STILL (no orbit, no pan, no zoom, no push-in, no movement of any kind). NO cuts, NO jump cuts, NO morphing. The boy stays in the SAME seated pose the entire 10 seconds - only his mouth moves (speaking) and his eyes shift subtly. His body, shoulders, arms and hands stay fixed.
Black & white cinematic photography, high contrast, subtle fine film grain, 50mm medium shot, eye level. A single bare bulb hangs directly above the boy, the only light source. The background is a PURE BLACK VOID - featureless darkness. NO room, NO wall, NO door, NO ceiling, NO furniture, NO architecture, NO objects, NO environmental details. ONLY ONE boy, no duplicates.

TITLE FLASH (the key moment):
As the boy says his final line, the words "The Jaisal Kut" appear in clean WHITE letters in the background BEHIND the boy (in the black void, above and behind his head). The text is crisp, white, legible, centered in the upper background. It FLASHES in for a SPLIT SECOND (about one second) and is the only text in the whole shot. The spelling is EXACTLY: T-h-e J-a-i-s-a-l K-u-t. The boy stays in front of the text, unchanged.

TIMELINE (one state per second):
[0.00-1.00s] Static medium shot. The boy is seated, facing the camera, hands on the table edge. Almost completely still. His eyes shift subtly toward the lens. He says, quiet and natural, with clear lip movement: (S1) <d>[English] I don't know what to say. </d>
[1.00-2.00s] A small pause. He is still, looking at the camera. His eyes hold the lens.
[2.00-3.00s] He says: (S1) <d>[English] I don't know where to start. </d>
[3.00-4.00s] A beat. He is still, looking at the camera.
[4.00-5.00s] He says: (S1) <d>[English] But... this is where I start. </d>
[5.00-6.00s] A beat. He is still, looking at the camera.
[6.00-7.00s] He says: (S1) <d>[English] So welcome to the Jaisal Kut. </d>
[7.00-8.00s] As he finishes the line, the words "The Jaisal Kut" FLASH in WHITE letters in the background behind him for a split second.
[8.00-9.00s] The white text is gone. The boy is still, facing the camera.
[9.00-10.00s] The boy holds his pose, facing the camera, hands on the table edge.

overall_soundscape:
Continuous natural ambient sound from edge to edge - quiet room tone, faint bare-bulb hum, the boy's breathing, his quiet voice. No other sounds.

non_diegetic_music:
NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient sounds only.
"""


def main():
    # backup
    bak = WF + ".bak_static"
    if not os.path.exists(bak):
        shutil.copy(WF, bak)
        print("backup ->", bak)

    with open(WF, encoding="utf-8") as f:
        d = json.load(f)

    nodes = {n["id"]: n for n in d["nodes"]}

    # 1. delete node 139 (90deg ref)
    removed_node = None
    for n in list(d["nodes"]):
        if n["id"] == 139:
            removed_node = n["type"]
            d["nodes"].remove(n)
    print("removed node 139:", removed_node)

    # 2. delete link 301 (139 -> 136 slot 1)
    removed_links = []
    for l in list(d["links"]):
        if l[0] == 301 or l[1] == 139:
            removed_links.append(l[0])
            d["links"].remove(l)
    print("removed links:", removed_links)

    # 3. clear ref_image_1 link on node 136
    r2v = nodes[136]
    for i in r2v["inputs"]:
        if i.get("name") == "ref_images.ref_image_1":
            i["link"] = None
            print("cleared ref_image_1 link on 136")

    # 4. rewrite prompt node 138
    p = nodes[138]
    p["widgets_values"] = [PROMPT]
    if "widgets_values_named" in p:
        p["widgets_values_named"] = {"value": PROMPT}
    print("rewrote prompt node 138 (len %d)" % len(PROMPT))

    with open(WF, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("saved", WF)

    # save prompt to project folder
    os.makedirs(os.path.dirname(PROMPT_OUT), exist_ok=True)
    with open(PROMPT_OUT, "w", encoding="utf-8") as f:
        f.write(PROMPT)
    print("saved prompt ->", PROMPT_OUT)


if __name__ == "__main__":
    main()
