# -*- coding: utf-8 -*-
"""
Build shot C (the head-twist HOOK) as an R2V workflow.

The original shot C used the H3LocalCameraEditor (camera node), which FREEZES the
scene and only moves the camera - it CANNOT turn the subject's head. The hook is
the HEAD turning 180 degrees, so we convert shot C to an R2V workflow (like the
other 9 shots) which lets the head turn AND lets Jaisal speak the Malayalam dialogue.

We copy shot B's proven R2V model chain (UNET -> LoRA -> SLA -> guider -> sampler)
and swap:
  - ref_image_0 (start) -> jaisal_head_left_back_side.png  (head facing left-back)
  - ref_image_1 (end)   -> jaisal_head_180_dergree.png     (head turned 180 to camera)
  - prompt              -> the dramatic head-twist hook (micro-expressions + Malayalam)
  - length              -> 240 frames (~10s, matches the script 0:08-0:18)
  - SaveVideo prefix    -> jaisal_intro_C_headtwist_180

Run:
    cmd /c "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe D:\\models\\vsCodeMcp\\utilities\\build_C_r2v.py"
"""
import json
import shutil
from pathlib import Path

WFDIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC = WFDIR / "jaisal_intro_B_setup.json"
DST = WFDIR / "jaisal_intro_C_headtwist_180_r2v.json"

# The dramatic head-twist hook prompt (6-section H3 R2V style, Malayalam dialogue).
PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference images - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy shown in the reference images seated at the table, head facing the LEFT-BACK side, body lit the same.
<Picture 2> is the LAST frame: the young boy shown in the reference images seated at the table, head fully turned 180 degrees toward the camera.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take that animates from <Picture 1> (Jaisal seated, head facing the left-back side) to <Picture 2> (Jaisal seated, head fully turned toward the camera). a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference images. There is ONLY ONE character - the young boy shown in the reference images - NO other people, NO second person, NO duplicates, NO extra figures.
<Picture 1> (first frame): fully_preserved - the opening frame.
<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.

detailed_description:
The shot BEGINS from <Picture 1> (Jaisal seated, head facing the left-back side). A beat of silence. Jaisal's EYES shift first - his gaze turns toward the lens before anything else moves. Then his head begins to rotate SLOWLY, deliberately, 180 degrees toward the camera, while his BODY does NOT react and stays still and lit the same. His eyes stay LOCKED on the lens the whole turn. As the head completes the turn, he speaks, his voice quiet and a little uncertain: <Subject 1> (S1) says, <d>[Malayalam] <breath> എന്താ പറയേണ്ടത് അറിയില്ല... <pause> എവിടുന്നാ തുടങ്ങേണ്ടത് എന്നറിയില്ല. <long pause> പക്ഷേ... <inhale> ഇതാണ് എൻറെ തുടക്കം. <pause> സോ വെൽക്കം ടു ദി ജൈസൽ കട്ട്. </d> The camera rotates and pushes in at exactly the same rate as the head turns. Camera: a CLOSE UP (85mm), eye level, the camera rotates and pushes in at the same rate as the head turn. The shot ENDS exactly on <Picture 2> (Jaisal seated, head fully turned toward the camera, eyes on the lens).

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, the faint electric hum of a bare bulb, a slow breath, the faint creak of the chair as the head turns, his quiet voice. Only these natural sounds, edge to edge.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, body turning, body reacting, body moving, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person"""


def main() -> int:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in d["nodes"]}

    # 1. Swap the two LoadImage refs (match by the current shot-B filenames).
    swapped = []
    for n in d["nodes"]:
        if n["type"] == "LoadImage":
            cur = n["widgets_values"][0]
            if cur == "jaisal_hand_under_the_table.png":
                n["widgets_values"][0] = "jaisal_head_left_back_side.png"
                swapped.append(("start", "jaisal_head_left_back_side.png"))
            elif cur == "jaisal_with_hand_on_table.png":
                n["widgets_values"][0] = "jaisal_head_180_dergree.png"
                swapped.append(("end", "jaisal_head_180_dergree.png"))
    print("Swapped refs:", swapped)
    assert len(swapped) == 2, "Expected to swap exactly 2 LoadImage refs"

    # 2. Set the R2V length widget (index 3) to 240 frames (~10s).
    for n in d["nodes"]:
        if n["type"] == "MiniMaxH3ReferenceToVideo":
            n["widgets_values"][3] = 240
            print("R2V length -> 240 frames (~10s); widgets:", n["widgets_values"])

    # 3. Set the prompt node.
    for n in d["nodes"]:
        if n["type"] == "PrimitiveStringMultiline":
            n["widgets_values"] = [PROMPT]
            print("Prompt set (%d chars)" % len(PROMPT))

    # 4. Set the SaveVideo prefix.
    for n in d["nodes"]:
        if n["type"] == "SaveVideo":
            n["widgets_values"][0] = "jaisal_intro_C_headtwist_180"
            print("SaveVideo prefix -> jaisal_intro_C_headtwist_180")

    DST.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    print("Wrote", DST.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
