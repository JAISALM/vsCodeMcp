# -*- coding: utf-8 -*-
"""
Shot C (jaisal_intro_C_starting_2ref.json) - REMOVE the in-video title flash.

User direction (2026-09-15): the in-video white "The Jaisal Kut" flash did NOT
go well - the face got distorted (too much pressure on MiniMax: text + face +
speech at once). The title will be done in POST: the user takes the LAST FRAME
of the video, creates a new image with the text added, and uses that.

Changes:
  1. Remove the TITLE FLASH section from the prompt (node 138).
  2. Remove the text from the timeline (7-8s beat is now just a still beat).
  3. Add a FACE CLARITY lock (face sharp/clear/in-focus in every frame, no
     distortion/morph/blur, exactly as in <Picture 1>).
  4. Add NO text/letters/words/title/watermark to the background lock (so the
     model does not hallucinate text on its own).
  5. Keep: single static medium shot, single ref, 240 frames (10s), 1344x768.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\rebuild_C_static_notext.py"
"""
import json
import shutil
import os

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_starting_2ref.json"
PROMPT_OUT = r"D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_C_static_notext.txt"

PROMPT = """subject_definitions:
<Subject 1> is the boy in <Picture 1>. His identity, face, hair, clothing and build come ENTIRELY from the reference image - do not alter his appearance in any way.
<Picture 1> is the ONLY frame anchor: the boy seated at the table, facing the camera, hands resting on the table edge.

summary:
[reference generation] A 10-second STATIC medium shot. <Subject 1> is seated at the table, facing the camera, hands on the table edge. The camera is COMPLETELY STILL - no orbit, no pan, no zoom, no movement. The boy stays in the same seated pose the whole time, speaking four quiet lines with clear lip movement.

retention_analysis:
<Subject 1> (all frames): fully_preserved - his appearance is identical in every frame, exactly as in <Picture 1>.
<Picture 1> (the whole shot): fully_preserved - the boy's pose, the table, the chair and the lighting are identical in every frame.

detailed_description:
MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: ONE single STATIC medium shot - the camera is COMPLETELY STILL (no orbit, no pan, no zoom, no push-in, no movement of any kind). NO cuts, NO jump cuts, NO morphing. The boy stays in the SAME seated pose the entire 10 seconds - only his mouth moves (speaking) and his eyes shift subtly. His body, shoulders, arms and hands stay fixed.
FACE CLARITY (top priority): the boy's FACE is SHARP, CLEAR, IN FOCUS and HIGH DETAIL in every single frame - the face is the sharpest thing in the frame. The face does NOT distort, does NOT blur, does NOT morph, does NOT change shape, does NOT melt. The face stays EXACTLY as in <Picture 1> - same features, same proportions, same identity.
Black & white cinematic photography, high contrast, subtle fine film grain, 50mm medium shot, eye level. A single bare bulb hangs directly above the boy, the only light source. The background is a PURE BLACK VOID - featureless darkness. NO room, NO wall, NO door, NO ceiling, NO furniture, NO architecture, NO objects, NO environmental details, NO text, NO letters, NO words, NO title, NO watermark, NO graphics. ONLY ONE boy, no duplicates.

TIMELINE (one state per second):
[0.00-1.00s] Static medium shot. The boy is seated, facing the camera, hands on the table edge. Almost completely still. His eyes shift subtly toward the lens. He says, quiet and natural, with clear lip movement: (S1) <d>[English] I don't know what to say. </d>
[1.00-2.00s] A small pause. He is still, looking at the camera. His eyes hold the lens.
[2.00-3.00s] He says: (S1) <d>[English] I don't know where to start. </d>
[3.00-4.00s] A beat. He is still, looking at the camera.
[4.00-5.00s] He says: (S1) <d>[English] But... this is where I start. </d>
[5.00-6.00s] A beat. He is still, looking at the camera.
[6.00-7.00s] He says: (S1) <d>[English] So welcome to the Jaisal Kut. </d>
[7.00-8.00s] A beat. He is still, facing the camera.
[8.00-9.00s] He is still, facing the camera.
[9.00-10.00s] The boy holds his pose, facing the camera, hands on the table edge.

overall_soundscape:
Continuous natural ambient sound from edge to edge - quiet room tone, faint bare-bulb hum, the boy's breathing, his quiet voice. No other sounds.

non_diegetic_music:
NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient sounds only.
"""


def main():
    bak = WF + ".bak_notext"
    if not os.path.exists(bak):
        shutil.copy(WF, bak)
        print("backup ->", bak)

    with open(WF, encoding="utf-8") as f:
        d = json.load(f)

    nodes = {n["id"]: n for n in d["nodes"]}
    p = nodes[138]
    p["widgets_values"] = [PROMPT]
    if "widgets_values_named" in p:
        p["widgets_values_named"] = {"value": PROMPT}
    print("rewrote prompt node 138 (len %d)" % len(PROMPT))

    with open(WF, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("saved", WF)

    os.makedirs(os.path.dirname(PROMPT_OUT), exist_ok=True)
    with open(PROMPT_OUT, "w", encoding="utf-8") as f:
        f.write(PROMPT)
    print("saved prompt ->", PROMPT_OUT)


if __name__ == "__main__":
    main()
