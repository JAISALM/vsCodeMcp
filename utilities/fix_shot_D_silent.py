#!/usr/bin/env python
"""Shot D (jaisal_intro_D_reverse.json) -> PURE SILENT REACTION SHOT.

WHY: take 00004 still animated the boy's mouth (lip-sync) even with the
<Subject 2> off-screen voice + lip-lock. H3 sees a dialogue line and moves the
visible person's lips. The reliable fix = REMOVE the in-video dialogue entirely.
The boy is a pure SILENT listener/reactor (eyes shift, thoughtful expression,
quiet breath, tiny head movement). The camera guy's line is DUBBED IN POST
(D089). No <d> line = no reason for the model to move his mouth.

Only node 138 (the prompt) is changed. Refs/length/anchors are untouched.
"""
import json, io, sys

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json"

PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference image - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description. <Subject 1> is the ONLY person in the frame. <Subject 1> is COMPLETELY SILENT in this shot - his mouth stays CLOSED and his lips NEVER move, he does NOT speak, he does NOT talk, he makes NO speech sound.

<Picture 1> is the FIRST frame: the young boy ALREADY seated at the table, both hands resting on the table edge, facing the camera.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take, 4 seconds. The young boy (<Subject 1>) is ALREADY seated at the table in the FIRST frame, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose. He is COMPLETELY SILENT - his mouth stays CLOSED and his lips NEVER move the entire shot. He is LISTENING to an off-screen question (the question is NOT heard in this take - it is added in post) and gives only a subtle, natural REACTION: his eyes shift slightly, a small thoughtful expression, a quiet breath, a very small natural head movement. a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same as the reference frame so the cut from the previous shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference image. <Subject 1> is the ONLY person in the frame - NO other people, NO second person, NO duplicates, NO extra figures. <Subject 1> is COMPLETELY SILENT - mouth CLOSED, lips NEVER move, NO speech.
<Picture 1> (first frame): fully_preserved - the opening frame, the boy is ALREADY seated in this pose from the very first frame.

detailed_description:
The shot BEGINS with the young boy (<Subject 1>) ALREADY seated at the table, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose; he is already there from the very first frame. His mouth stays CLOSED and his lips NEVER move - he is COMPLETELY SILENT the entire shot.
[0-1s] The boy sits still, facing the camera, quiet, mouth closed, listening.
[1-2s] The boy LISTENS - his eyes shift slightly, a small thoughtful expression forms on his face, his gaze stays forward, his mouth stays CLOSED.
[2-3s] A quiet breath, a very small natural head movement, a subtle listening reaction. His mouth stays CLOSED.
[3-4s] He holds the pose - still seated, hands on the table, facing the camera, mouth CLOSED, a calm thoughtful expression.
The camera is a MEDIUM shot (50mm), eye level, COMPLETELY STILL - no pan, no orbit, no zoom, no push-in. The shot ends naturally on the boy still seated at the table, hands on the table, facing the camera, mouth CLOSED.

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, the faint electric hum of a bare bulb, the quiet creak of the chair, the boy's soft breath. There is NO voice and NO speech in this take - the boy makes NO speech sound and no off-screen voice is heard.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a visible second person, the boy speaking, the boy talking, the boy's mouth open, the boy's lips moving, the boy's mouth moving, lip movement, the boy's lips opening, the boy's mouth opening, the boy's jaw moving, any speech, any voice, any dialogue, the boy moving into the pose, the boy standing up, the boy walking, pose change, camera movement, camera pan, camera orbit, camera zoom, camera push-in"""


def main():
    with io.open(WF, "r", encoding="utf-8") as f:
        wf = json.load(f)

    node = next(n for n in wf["nodes"] if n["id"] == 138)
    old = node["widgets_values"][0]
    node["widgets_values"][0] = PROMPT
    # keep named in sync if present
    if "widgets_values_named" in node and node["widgets_values_named"]:
        node["widgets_values_named"]["prompt"] = PROMPT

    with io.open(WF, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)

    print("node 138 prompt replaced.")
    print("old had <d> line:", "<d>" in old)
    print("new has <d> line:", "<d>" in PROMPT)
    print("new has off-screen voice subject:", "<Subject 2>" in PROMPT)


if __name__ == "__main__":
    main()
