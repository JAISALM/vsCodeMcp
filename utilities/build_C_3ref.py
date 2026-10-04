# -*- coding: utf-8 -*-
"""
Build shot C as a SINGLE 3-ref R2V head turn (user direction 2026-09-14):

  ref_image_0 = jaisal_with_hand_on_table.png   (normal frontal, B's end frame)
  ref_image_1 = jaisal_head_left_back_side.png  (90-degree left-back, MIDDLE anchor)
  ref_image_2 = jaisal_head_180_dergree.png     (180-degree back-twist, END)

- LOCKED camera (no camera node) - the head does all the motion.
- 240 frames (~10s): the turn happens in the first ~5s (eyes shift first, head
  rotates SLOWLY to the LEFT through the 90-degree anchor), then the head HOLDS
  at 180 degrees (back to camera, face turned back over the shoulder) while he
  speaks the Malayalam dialogue in the second ~5s.
- Direction fix: the head turns to the LEFT (toward his left shoulder), NOT right.

Reuses shot B's proven R2V model chain.

Run:
    cmd /c "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe D:\\models\\vsCodeMcp\\utilities\\build_C_3ref.py"
"""
import json
from pathlib import Path

WFDIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC = WFDIR / "jaisal_intro_B_setup.json"
DST = WFDIR / "jaisal_intro_C_headturn_3ref.json"

PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference images - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy shown in the reference images seated at the table, facing the camera, hands on the table edge.
<Picture 2> is the MIDDLE frame: the young boy shown in the reference images seen from the LEFT-BACK side, head turned to the left.
<Picture 3> is the LAST frame: the young boy shown in the reference images with his BACK to the camera, but his FACE turned back toward the camera over his shoulder.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take that animates from <Picture 1> (Jaisal seated, facing the camera, hands on the table) through <Picture 2> (Jaisal seen from the left-back side) to <Picture 3> (Jaisal's back to the camera, face turned back toward the camera). a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference images. There is ONLY ONE character - the young boy shown in the reference images - NO other people, NO second person, NO duplicates, NO extra figures.
<Picture 1> (first frame): fully_preserved - the opening frame.
<Picture 2> (middle frame): fully_preserved - the head passes through this position at about the 5 second mark.
<Picture 3> (last frame): fully_preserved - the shot ENDS exactly on this frame.

detailed_description:
The shot BEGINS from <Picture 1> (Jaisal seated, facing the camera, hands on the table). A beat of silence. Jaisal's EYES shift first - his gaze turns to the LEFT before anything else moves. Then his head begins to rotate SLOWLY, deliberately, to the LEFT (toward his left shoulder, NOT to the right), passing through the left-back side position of <Picture 2> at about the 5 second mark, while his BODY stays still and lit the same. His eyes stay LOCKED on the lens the whole turn. By about the 5 second mark his head has completed the 180 degree turn - his BACK is to the camera, but his FACE is turned back toward the camera over his shoulder, exactly matching <Picture 3>. From about the 5 second mark to the end, his head HOLDS at that 180 degree position, and he speaks, his voice quiet and a little uncertain: <Subject 1> (S1) says, <d>[Malayalam] <breath> \u0d10\u0d28\u0d4d\u0d24\u0d3e \u0d2a\u0d3e\u0d31\u0d10\u0d4d\u0d2f\u0d47\u0d28\u0d4d\u0d24\u0d4d \u0d12\u0d31\u0d3f\u0d2f\u0d3f\u0d33\u0d4d\u0d33... <pause> \u0d09\u0d4d\u0d35\u0d3f\u0d21\u0d41\u0d28\u0d4d\u0d28\u0d3e \u0d24\u0d41\u0d1f\u0d02\u0d17\u0d47\u0d28\u0d4d\u0d24\u0d4d \u0d09\u0d23\u0d3f\u0d31\u0d3f\u0d33\u0d4d\u0d33. <long pause> \u0d2a\u0d3e\u0d15\u0d4d\u0d37\u0d47... <inhale> \u0d07\u0d24\u0d3e\u0d28\u0d4d\u0d31 \u0d09\u0d1f\u0d23\u0d47 \u0d1f\u0d41\u0d21\u0d3e\u0d15\u0d02. <pause> \u0d38\u0d4b \u0d35\u0d47\u0d33\u0d4d\u0d15\u0d02 \u0d1f\u0d41 \u0d26\u0d3f \u0d1c\u0d3f\u0d33\u0d33\u0d4d \u0d15\u0d1f\u0d4d\u0d31\u0d4d. </d> Camera: a LOCKED CLOSE UP (85mm), eye level, the camera does NOT move, push, drift, tilt, pan or zoom - only the head moves. The shot ENDS exactly on <Picture 3> (Jaisal's back to the camera, face turned back toward the camera).

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, the faint electric hum of a bare bulb, a slow breath, the faint creak of the chair as the head turns, his quiet voice in the second half. Only these natural sounds, edge to edge.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, body turning, body reacting, body moving, head turning to the right, head turning right, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person"""


def main() -> int:
    d = json.loads(SRC.read_text(encoding="utf-8"))

    # 1. Swap the two existing LoadImage refs.
    swapped = []
    for n in d["nodes"]:
        if n["type"] == "LoadImage":
            cur = n["widgets_values"][0]
            if cur == "jaisal_hand_under_the_table.png":
                n["widgets_values"][0] = "jaisal_with_hand_on_table.png"
                swapped.append(("ref0", "jaisal_with_hand_on_table.png"))
            elif cur == "jaisal_with_hand_on_table.png":
                n["widgets_values"][0] = "jaisal_head_left_back_side.png"
                swapped.append(("ref1", "jaisal_head_left_back_side.png"))
    print("Swapped refs:", swapped)
    assert len(swapped) == 2, "Expected to swap exactly 2 LoadImage refs"

    # 2. Add a new LoadImage node for the 180-degree end frame -> ref_image_2.
    new_node_id = 152
    new_link_id = 307
    d["nodes"].append({
        "id": new_node_id,
        "type": "LoadImage",
        "pos": [450, 620],
        "size": [282.78, 322],
        "flags": {},
        "order": 5,
        "mode": 0,
        "inputs": [
            {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
            {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [new_link_id]},
            {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
        ],
        "properties": {"Node name for S&R": "LoadImage"},
        "widgets_values": ["jaisal_head_180_dergree.png", "image"],
    })
    d["links"].append([new_link_id, new_node_id, 0, None, 2, "IMAGE"])
    # Fix the link's target node id (R2V node) after we find it.
    r2v = next(n for n in d["nodes"] if n["type"] == "MiniMaxH3ReferenceToVideo")
    d["links"][-1][3] = r2v["id"]
    # Wire the ref_image_2 input's link field (slot index 2).
    for i in r2v["inputs"]:
        if i["name"] == "ref_images.ref_image_2":
            i["link"] = new_link_id
            print("Wired ref_image_2 -> link", new_link_id, "(node %d)" % new_node_id)
            break

    # 3. Set the R2V length widget (index 3) to 240 frames (~10s).
    r2v["widgets_values"][3] = 240
    print("R2V length -> 240 frames (~10s); widgets:", r2v["widgets_values"])

    # 4. Set the prompt node.
    for n in d["nodes"]:
        if n["type"] == "PrimitiveStringMultiline":
            n["widgets_values"] = [PROMPT]
            print("Prompt set (%d chars)" % len(PROMPT))

    # 5. Set the SaveVideo prefix.
    for n in d["nodes"]:
        if n["type"] == "SaveVideo":
            n["widgets_values"][0] = "jaisal_intro_C_headturn_3ref"
            print("SaveVideo prefix -> jaisal_intro_C_headturn_3ref")

    DST.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    print("Wrote", DST.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
