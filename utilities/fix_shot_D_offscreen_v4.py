"""Shot D v4: make the OFF-SCREEN voice unambiguous so the boy does NOT talk.

User: "we didnt mention clearly enough, the character is talking. prompt better way."

WHY the boy talked: the previous prompt used a custom `<Off-screen voice>` tag that
H3 doesn't recognize, so the single `<d>` line got attributed to the only person in
frame (the boy).

BETTER WAY (per the micro-expressions guide): use a proper `<Subject 2>` tag for the
off-screen voice so the model sees TWO distinct speakers, tie the `<d>` line to
`<Subject 2>` (not the boy), and add HARD "lips stay closed / mouth does not open"
constraints in the visual description + negatives.

Changes to jaisal_intro_D_reverse.json:
  - node 138 (prompt) -> rewritten with <Subject 2> = off-screen voice, boy's lips
    locked closed.
  - length stays 96 frames (4s @ 24fps).
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json"

PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference image - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description. <Subject 1> is the ONLY person VISIBLE in the frame. <Subject 1> does NOT speak in this shot - his lips stay CLOSED the entire shot.
<Subject 2> is a calm adult male voice (the camera guy). <Subject 2> is NOT visible in the frame - only his voice is heard, coming from OFF-SCREEN. <Subject 2> is NOT the boy.
<Picture 1> is the FIRST frame: the young boy ALREADY seated at the table, both hands resting on the table edge, facing the camera.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take, 4 seconds. The young boy (<Subject 1>) is ALREADY seated at the table in the FIRST frame, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose and he does NOT speak - his lips stay CLOSED the entire shot. An OFF-SCREEN male voice (<Subject 2>, NOT visible in the frame) asks a question, and the boy just LISTENS - subtle, natural micro-expressions: his eyes shift slightly, a small thoughtful expression, a quiet breath, a very small natural head movement. a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same as the reference frame so the cut from the previous shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference image. <Subject 1> is the ONLY person VISIBLE in the frame - NO other people, NO second person, NO duplicates, NO extra figures, NO visible camera guy. <Subject 1> does NOT speak - his lips stay CLOSED.
<Subject 2> (off-screen voice only): NOT visible in the frame - only his voice is heard.
<Picture 1> (first frame): fully_preserved - the opening frame, the boy is ALREADY seated in this pose from the very first frame.

detailed_description:
The shot BEGINS with the young boy (<Subject 1>) ALREADY seated at the table, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose; he is already there from the very first frame. His lips stay CLOSED the entire shot - he does NOT speak.
[0-1s] The boy sits still, facing the camera, quiet, lips closed.
[1-2s] The OFF-SCREEN male voice (<Subject 2>, NOT visible in the frame, calm adult male voice, close to the mic) says, <d>[English] <breath> What's the purpose of this channel? </d> The boy's lips stay CLOSED - he does NOT speak, he only listens.
[2-3s] The boy LISTENS - his eyes shift slightly, a small thoughtful expression forms on his face, his gaze stays forward, his lips stay CLOSED.
[3-4s] A quiet breath, a very small natural head movement, a subtle listening reaction. He stays seated, hands on the table, facing the camera, lips CLOSED.
The camera is a MEDIUM shot (50mm), eye level, COMPLETELY STILL - no pan, no orbit, no zoom, no push-in. The shot ends naturally on the boy still seated at the table, hands on the table, facing the camera, lips CLOSED.

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, the faint electric hum of a bare bulb, the quiet creak of the chair, the boy's soft breath. The boy makes NO speech sound. The ONLY voice in this shot is the OFF-SCREEN male voice (<Subject 2>).

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a visible second person, the camera guy visible in frame, the boy speaking, the boy talking, the boy's mouth open, the boy's lips moving, the boy's mouth moving, lip movement, the boy's lips opening, the boy moving into the pose, the boy standing up, the boy walking, pose change, camera movement, camera pan, camera orbit, camera zoom, camera push-in"""

d = json.load(open(WF, encoding="utf-8"))
for n in d["nodes"]:
    if n["id"] == 138:
        n["widgets_values"][0] = PROMPT

json.dump(d, open(WF, "w", encoding="utf-8"), indent=1)
print("UPDATED", WF)
print("node 138 prompt = <Subject 2> off-screen voice + boy's lips locked CLOSED")
