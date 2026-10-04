"""Fix shot D: the video was DRIFTING TOWARD the reference instead of STARTING on it.

User: "we are moving towards the first image, but the starting should be the first
image, and then we should just listen. when the camera guy says the dialogue, the
next shot is jaisal telling dialogue."

Fix: the FIRST frame = exactly the reference (C's last frame). The boy is ALREADY
seated there - he does NOT move into the pose. He just LISTENS (very subtle,
near-still). Camera completely still. The camera guy's line is dubbed in post;
the NEXT shot (E) is Jaisal speaking.

Changes to jaisal_intro_D_reverse.json:
  - node 138 (prompt) -> rewritten: "already seated from frame 1, hold the pose,
    just listen, near-still, camera completely still" + negatives against
    moving-into-pose / pose-change / head-turn.
  - anchors unchanged: ref_image_0 = ref_image_1 = shot_C_lastframe.png
    (same frame as start AND end = locks the pose, no drift).
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json"

PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference image - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy ALREADY seated at the table, both hands resting on the table edge, facing the camera. This is the exact pose he holds for the ENTIRE shot.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take. The young boy is ALREADY seated at the table in the FIRST frame, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose; he is already there from the very first frame. He just LISTENS to an off-screen question - a very subtle, almost still expression. The body and hands stay COMPLETELY STILL. a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same as the reference frame so the cut from the previous shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference image. There is ONLY ONE character - the young boy shown in the reference image - NO other people, NO second person, NO duplicates, NO extra figures.
<Picture 1> (first frame): fully_preserved - the opening frame, the boy is ALREADY seated in this pose from the very first frame.

detailed_description:
The shot BEGINS with the young boy ALREADY seated at the table, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose; he is already there from the very first frame. He just LISTENS to an off-screen question - a very subtle, almost still expression, maybe the faintest change in the eyes. The body and hands stay COMPLETELY STILL on the table. The camera is a MEDIUM shot (50mm), eye level, COMPLETELY STILL - no pan, no orbit, no zoom, no push-in. The shot ENDS on the SAME pose (the boy still seated, hands on the table, facing the camera).

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, a soft breath, the faint electric hum of a bare bulb, the quiet creak of the chair. Only these natural sounds, edge to edge. NO dialogue in this shot (the off-screen question is added in post).

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person, camera movement, camera pan, camera orbit, camera zoom, camera push-in, the boy moving into the pose, the boy standing up, the boy walking, motion toward the reference, pose change, head tilt, head turn, the boy speaking, mouth moving"""

d = json.load(open(WF, encoding="utf-8"))
for n in d["nodes"]:
    if n["id"] == 138:
        n["widgets_values"][0] = PROMPT

json.dump(d, open(WF, "w", encoding="utf-8"), indent=1)
print("UPDATED", WF)
print("node 138 (prompt) = hold-the-pose listening shot (no drift into pose)")
