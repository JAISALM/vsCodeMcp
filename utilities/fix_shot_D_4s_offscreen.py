"""Shot D v3: 4s, OFF-SCREEN camera-guy voice, Jaisal only REACTS.

User: "i dont think we need 7 seconds, the current one spits a gibberish out of
nowhere. 'What's the purpose of this channel?' is the only dialogue, we just need
the reaction, maybe 4 seconds will be enough. update the prompt, this is something
the character DOESN'T say - just a voice alone. let minimax do this and we will
see how it works. add expression tags properly, use the minimax prompting guide."

Changes to jaisal_intro_D_reverse.json:
  - node 136 (R2V) length widget (index 3): 175 -> 96 frames (4s @ 24fps)
  - node 138 (prompt): rewritten -
      * the CAMERA GUY's line is an OFF-SCREEN male voice (NOT the character,
        NOT visible in frame) - MiniMax generates it
      * Jaisal does NOT speak - he only REACTS (listening micro-expressions)
      * 4-second per-second timeline
      * NO MUSIC (D041)
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json"

PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference image - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy ALREADY seated at the table, both hands resting on the table edge, facing the camera.
<Off-screen voice> is a calm adult male voice (the camera guy) - he is NOT visible in the frame, only his voice is heard.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take, 4 seconds. The young boy is ALREADY seated at the table in the FIRST frame, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose and he does NOT speak. An OFF-SCREEN male voice (the camera guy, not visible in the frame) asks a question, and the boy just LISTENS - subtle, natural micro-expressions: his eyes shift slightly, a small thoughtful expression, a quiet breath, a very small natural head movement. a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same as the reference frame so the cut from the previous shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference image. There is ONLY ONE character visible - the young boy shown in the reference image - NO other people, NO second person, NO duplicates, NO extra figures, NO visible camera guy.
<Picture 1> (first frame): fully_preserved - the opening frame, the boy is ALREADY seated in this pose from the very first frame.

detailed_description:
The shot BEGINS with the young boy ALREADY seated at the table, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose; he is already there from the very first frame. He does NOT speak in this shot.
[0-1s] The boy sits still, facing the camera, quiet.
[1-2s] An OFF-SCREEN male voice (the camera guy, NOT visible in the frame, calm adult male voice, close to the mic) asks: <d>[English] <breath> What's the purpose of this channel? </d>
[2-3s] The boy LISTENS - his eyes shift slightly, a small thoughtful expression forms on his face, his gaze stays forward.
[3-4s] A quiet breath, a very small natural head movement, a subtle listening reaction. He stays seated, hands on the table, facing the camera.
The camera is a MEDIUM shot (50mm), eye level, COMPLETELY STILL - no pan, no orbit, no zoom, no push-in. The shot ends naturally on the boy still seated at the table, hands on the table, facing the camera.

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, the faint electric hum of a bare bulb, the quiet creak of the chair, the boy's soft breath. The off-screen male voice is the ONLY speech in this shot.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a visible second person, the camera guy visible in frame, the boy speaking, the boy's mouth moving, the boy moving into the pose, the boy standing up, the boy walking, pose change, camera movement, camera pan, camera orbit, camera zoom, camera push-in"""

d = json.load(open(WF, encoding="utf-8"))
for n in d["nodes"]:
    if n["id"] == 136:
        # widgets_values = [prompt, width, height, length, ref_image_size]
        n["widgets_values"][3] = 96  # 4s @ 24fps
    elif n["id"] == 138:
        n["widgets_values"][0] = PROMPT

json.dump(d, open(WF, "w", encoding="utf-8"), indent=1)
print("UPDATED", WF)
print("node 136 length = 96 frames (4s @ 24fps)")
print("node 138 prompt = off-screen camera-guy voice + Jaisal listening reaction")
