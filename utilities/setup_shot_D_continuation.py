"""Set up shot D (jaisal_intro_D_reverse.json) as a CONTINUATION from shot C's last frame.

The "perfect reverse" (180° head twist) was DROPPED (D086/D087) — shot C is now a
static medium shot. So shot D is no longer a reverse; it CONTINUES from C's last
frame: Jaisal stays seated (exactly C's end frame), the camera guy (off-screen)
asks "What's the purpose of this channel?", Jaisal gives a subtle listening
reaction. The camera guy's line is DUBBED IN POST (Midhun's voice) — the video
itself = Jaisal listening + ambient, NO in-video dialogue, NO music (D041).

Changes to jaisal_intro_D_reverse.json:
  - node 137 (ref_image_0) -> shot_C_lastframe.png  (C's last frame = START)
  - node 139 (ref_image_1) -> shot_C_lastframe.png  (SAME frame = END, locks pose)
  - node 138 (prompt)      -> rewritten for the listening shot
  - length stays 175 frames (~7.3s, matches script 0:18-0:25)

The user places C's last frame at input\shot_C_lastframe.png (or picks it from
the LoadImage dropdown in the UI).
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json"

PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference images - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy seated at the table, both hands resting on the table edge, facing the camera.
<Picture 2> is the LAST frame: the SAME young boy in the SAME seated pose, both hands on the table edge, facing the camera - only a subtle change in expression.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take. The young boy stays seated at the table, both hands on the table edge, facing the camera. He is LISTENING to an off-screen question - a subtle, thoughtful reaction: his eyes shift slightly, a small thoughtful expression, a brief pause, maybe a tiny head tilt. The body and hands stay still. a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same as the reference frame so the cut from the previous shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference images. There is ONLY ONE character - the young boy shown in the reference images - NO other people, NO second person, NO duplicates, NO extra figures.
<Picture 1> (first frame): fully_preserved - the opening frame.
<Picture 2> (last frame): fully_preserved - the shot ENDS on this frame.

detailed_description:
The shot BEGINS from <Picture 1> (the young boy seated, hands on the table, facing the camera). He is LISTENING to an off-screen question. A subtle, thoughtful reaction: his eyes shift slightly, a small thoughtful expression forms, a brief pause, maybe a tiny head tilt. The body and hands stay STILL on the table. The camera is a MEDIUM shot (50mm), eye level, COMPLETELY STILL - no pan, no orbit, no zoom. The shot ENDS exactly on <Picture 2> (the same seated pose, hands on the table).

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, a soft breath, the faint electric hum of a bare bulb, the quiet creak of the chair. Only these natural sounds, edge to edge. NO dialogue in this shot (the off-screen question is added in post).

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person, camera movement, camera pan, camera orbit, camera zoom"""

d = json.load(open(WF, encoding="utf-8"))
for n in d["nodes"]:
    if n["id"] == 137:
        n["widgets_values"][0] = "shot_C_lastframe.png"
    elif n["id"] == 139:
        n["widgets_values"][0] = "shot_C_lastframe.png"
    elif n["id"] == 138:
        n["widgets_values"][0] = PROMPT

json.dump(d, open(WF, "w", encoding="utf-8"), indent=1)
print("UPDATED", WF)
print("node 137 (ref_image_0) = shot_C_lastframe.png")
print("node 139 (ref_image_1) = shot_C_lastframe.png")
print("node 138 (prompt)      = listening shot")
