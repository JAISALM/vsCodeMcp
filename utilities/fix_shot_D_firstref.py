"""Shot D v2: FIRST REF ONLY + micro-expressions + NATURAL ending.

User: "this image has to be the one in first and last right or should we just add
first one alone and do some micro expressions and fetch a natural last frame out
of this workflow? THAT WILL BE BETTER RIGHT? otherwise it will feel like the same
old image again"

DECISION: first ref ONLY (C's last frame) + subtle listening micro-expressions.
Do NOT lock the last frame to the same image (that made it feel frozen / "same old
image"). The shot ENDS NATURALLY; then seedvr2_lastframe_2k.json grabs that
natural last frame for shot E.

Changes to jaisal_intro_D_reverse.json:
  - node 137 (ref_image_0) = shot_C_lastframe.png  (C's last frame = START)
  - node 139 (ref_image_1) -> BYPASSED (mode=4) + its link (301) removed from the
    R2V ref_image_1 input (link=None)  => FIRST REF ONLY
  - node 138 (prompt)      -> first frame = reference, then subtle listening
    micro-expressions, NATURAL ending (not locked to the same frame)
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json"

PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference image - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy ALREADY seated at the table, both hands resting on the table edge, facing the camera.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take. The young boy is ALREADY seated at the table in the FIRST frame, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose; he is already there from the very first frame. He just LISTENS to an off-screen question - subtle, natural micro-expressions: his eyes shift slightly, a small thoughtful expression, a quiet breath, a very small natural head movement. The body stays seated, hands stay on the table. a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same as the reference frame so the cut from the previous shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference image. There is ONLY ONE character - the young boy shown in the reference image - NO other people, NO second person, NO duplicates, NO extra figures.
<Picture 1> (first frame): fully_preserved - the opening frame, the boy is ALREADY seated in this pose from the very first frame.

detailed_description:
The shot BEGINS with the young boy ALREADY seated at the table, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose; he is already there from the very first frame. He just LISTENS to an off-screen question - subtle, natural micro-expressions: his eyes shift slightly, a small thoughtful expression forms, a quiet breath, a very small natural head movement. The body stays seated, hands stay on the table. The camera is a MEDIUM shot (50mm), eye level, COMPLETELY STILL - no pan, no orbit, no zoom, no push-in. The shot ends naturally on the boy still seated at the table, hands on the table, facing the camera.

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, a soft breath, the faint electric hum of a bare bulb, the quiet creak of the chair. Only these natural sounds, edge to edge. NO dialogue in this shot (the off-screen question is added in post).

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person, camera movement, camera pan, camera orbit, camera zoom, camera push-in, the boy moving into the pose, the boy standing up, the boy walking, pose change, the boy speaking, mouth moving, a second person"""

d = json.load(open(WF, encoding="utf-8"))

for n in d["nodes"]:
    if n["id"] == 137:
        n["widgets_values"][0] = "shot_C_lastframe.png"
    elif n["id"] == 139:
        # bypass the second LoadImage so only the FIRST ref is used
        n["mode"] = 4
    elif n["id"] == 138:
        n["widgets_values"][0] = PROMPT
    elif n["id"] == 136:
        # clear the ref_image_1 input link (index 4) -> first ref only
        for inp in n["inputs"]:
            if inp["name"] == "ref_images.ref_image_1":
                inp["link"] = None

# remove link 301 (node 139 -> R2V ref_image_1) from the links array
d["links"] = [l for l in d["links"] if not (l[0] == 301 and l[1] == 139)]

json.dump(d, open(WF, "w", encoding="utf-8"), indent=1)
print("UPDATED", WF)
print("node 137 (ref_image_0) = shot_C_lastframe.png (FIRST REF ONLY)")
print("node 139 (ref_image_1) = BYPASSED, link 301 removed")
print("node 138 (prompt)      = micro-expressions + NATURAL ending")
