# -*- coding: utf-8 -*-
"""
Build shot C as a 2-STEP head turn (R2V), for continuity + reliability.

Shot C must START from shot B's last frame (jaisal_with_hand_on_table.png = normal
frontal) for a seamless cut. A full 180-degree head turn in one take is a big ask,
so we split it into two 90-degree steps (each more reliable), sharing the 90-degree
frame as the anchor:

  C1 (normal -> 90deg):  jaisal_with_hand_on_table.png  -> jaisal_head_left_back_side.png
  C2 (90deg -> 180deg):  jaisal_head_left_back_side.png -> jaisal_head_180_dergree.png

The Malayalam dialogue goes in C2 (the creepy reveal, when the face turns back).

Both reuse shot B's proven R2V model chain.

Run:
    cmd /c "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe D:\\models\\vsCodeMcp\\utilities\\build_C1_C2.py"
"""
import json
from pathlib import Path

WFDIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC = WFDIR / "jaisal_intro_B_setup.json"

C1 = WFDIR / "jaisal_intro_C1_headturn_90.json"
C2 = WFDIR / "jaisal_intro_C2_headturn_180.json"

C1_PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference images - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy shown in the reference images seated at the table, facing the camera, hands on the table edge.
<Picture 2> is the LAST frame: the young boy shown in the reference images seen from the LEFT-BACK side, head turned to the left, body staying still.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take that animates from <Picture 1> (Jaisal seated, facing the camera, hands on the table) to <Picture 2> (Jaisal seen from the left-back side, head turned left). a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference images. There is ONLY ONE character - the young boy shown in the reference images - NO other people, NO second person, NO duplicates, NO extra figures.
<Picture 1> (first frame): fully_preserved - the opening frame.
<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.

detailed_description:
The shot BEGINS from <Picture 1> (Jaisal seated, facing the camera, hands on the table). A beat of silence. Jaisal's EYES shift first - his gaze turns to the left before anything else moves. Then his head begins to rotate SLOWLY, deliberately, toward the LEFT-BACK side, while his BODY stays still and lit the same. His eyes stay LOCKED on the lens. The camera orbits slowly to the left at the same rate as the head turns. Camera: a CLOSE UP (85mm), eye level, the camera orbits left at the same rate as the head turn. The shot ENDS exactly on <Picture 2> (Jaisal seen from the left-back side, head turned left).

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, the faint electric hum of a bare bulb, a slow breath, the faint creak of the chair as the head turns. Only these natural sounds, edge to edge.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, body turning, body reacting, body moving, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person"""

C2_PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference images - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy shown in the reference images seen from the LEFT-BACK side, head turned to the left.
<Picture 2> is the LAST frame: the young boy shown in the reference images with his BACK to the camera, but his FACE turned back toward the camera over his shoulder.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take that animates from <Picture 1> (Jaisal seen from the left-back side) to <Picture 2> (Jaisal's back to the camera, face turned back toward the camera). a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference images. There is ONLY ONE character - the young boy shown in the reference images - NO other people, NO second person, NO duplicates, NO extra figures.
<Picture 1> (first frame): fully_preserved - the opening frame.
<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.

detailed_description:
The shot BEGINS from <Picture 1> (Jaisal seen from the left-back side, head turned left). His head continues to rotate SLOWLY, deliberately, completing the turn to 180 degrees - his BACK ends up facing the camera, but his FACE turns back toward the camera over his shoulder. His BODY stays still and lit the same. His eyes stay LOCKED on the lens the whole turn. As the head completes the turn, he speaks, his voice quiet and a little uncertain: <Subject 1> (S1) says, <d>[Malayalam] <breath> \u0d10\u0d28\u0d4d\u0d24\u0d3e \u0d2a\u0d3e\u0d31\u0d10\u0d4d\u0d2f\u0d47\u0d28\u0d4d\u0d24\u0d4d \u0d12\u0d31\u0d3f\u0d2f\u0d3f\u0d33\u0d4d\u0d33... <pause> \u0d09\u0d4d\u0d35\u0d3f\u0d21\u0d41\u0d28\u0d4d\u0d28\u0d3e \u0d24\u0d41\u0d1f\u0d02\u0d17\u0d47\u0d28\u0d4d\u0d24\u0d4d \u0d09\u0d23\u0d3f\u0d31\u0d3f\u0d33\u0d4d\u0d33. <long pause> \u0d2a\u0d3e\u0d15\u0d4d\u0d37\u0d47... <inhale> \u0d07\u0d24\u0d3e\u0d28\u0d4d\u0d31 \u0d09\u0d1f\u0d23\u0d47 \u0d1f\u0d41\u0d21\u0d3e\u0d15\u0d02. <pause> \u0d38\u0d4b \u0d35\u0d47\u0d33\u0d4d\u0d15\u0d02 \u0d1f\u0d41 \u0d26\u0d3f \u0d1c\u0d3f\u0d33\u0d33\u0d4d \u0d15\u0d1f\u0d4d\u0d31\u0d4d. </d> The camera orbits slowly to the left at the same rate as the head turns. Camera: a CLOSE UP (85mm), eye level, the camera orbits left at the same rate as the head turn. The shot ENDS exactly on <Picture 2> (Jaisal's back to the camera, face turned back toward the camera).

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, the faint electric hum of a bare bulb, a slow breath, the faint creak of the chair as the head turns, his quiet voice. Only these natural sounds, edge to edge.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, body turning, body reacting, body moving, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person"""


def build(dst: Path, start_ref: str, end_ref: str, prompt: str, length: int, prefix: str) -> None:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    swapped = []
    for n in d["nodes"]:
        if n["type"] == "LoadImage":
            cur = n["widgets_values"][0]
            if cur == "jaisal_hand_under_the_table.png":
                n["widgets_values"][0] = start_ref
                swapped.append(("start", start_ref))
            elif cur == "jaisal_with_hand_on_table.png":
                n["widgets_values"][0] = end_ref
                swapped.append(("end", end_ref))
    assert len(swapped) == 2, "Expected to swap exactly 2 LoadImage refs, got %s" % swapped
    for n in d["nodes"]:
        if n["type"] == "MiniMaxH3ReferenceToVideo":
            n["widgets_values"][3] = length
        if n["type"] == "PrimitiveStringMultiline":
            n["widgets_values"] = [prompt]
        if n["type"] == "SaveVideo":
            n["widgets_values"][0] = prefix
    dst.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    print("Wrote %s (start=%s, end=%s, length=%d, prefix=%s)" % (dst.name, start_ref, end_ref, length, prefix))


def main() -> int:
    # C1: normal (B's end frame) -> 90deg (left-back side)
    build(C1, "jaisal_with_hand_on_table.png", "jaisal_head_left_back_side.png",
          C1_PROMPT, 120, "jaisal_intro_C1_headturn_90")
    # C2: 90deg (left-back side) -> 180deg (back-twisted, face turned back)
    build(C2, "jaisal_head_left_back_side.png", "jaisal_head_180_dergree.png",
          C2_PROMPT, 120, "jaisal_intro_C2_headturn_180")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
