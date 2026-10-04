#!/usr/bin/env python
"""Shot D (jaisal_intro_D_reverse.json) v2 -> HARD SILENT-AUDIO LOCK.

WHY: even with the dialogue removed, H3's AUDIO PRIOR (a person facing the
camera = talking) leaked speech-like GIBBERISH. Per the R2V prompting guide
("No dialogue/text if not wanted: state 'No dialogue, no text, no subtitles'"),
we make the audio a HARD SILENT lock: overall_soundscape = ambient ONLY,
non_diegetic_music + negatives forbid ALL human voice/speech/words/gibberish.

Only node 138 (the prompt) is changed. Refs/length/anchors untouched.
NOTE: the camera guy's line is DUBBED IN POST (D055/D089/D090), so the H3 audio
is throwaway - if any speech still leaks, strip it in post (ffmpeg -an).
"""
import json, io

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json"

PROMPT = """subject_definitions:
<Subject 1> is the young boy shown in the reference image - identity, face, hair, clothing and build come from the attached reference image, NOT from this text description. <Subject 1> is the ONLY person in the frame. <Subject 1> is COMPLETELY SILENT - his mouth stays CLOSED, his lips NEVER move, he makes NO sound, NO speech, NO talking, NO vocalization of any kind.

<Picture 1> is the FIRST frame: the young boy ALREADY seated at the table, both hands resting on the table edge, facing the camera.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take, 4 seconds. The young boy (<Subject 1>) is ALREADY seated at the table in the FIRST frame, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose. He is COMPLETELY SILENT and makes NO sound - his mouth stays CLOSED and his lips NEVER move the entire shot. He only shows a subtle, natural facial reaction: his eyes shift slightly, a small thoughtful expression, a quiet breath, a very small natural head movement. a dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same as the reference frame so the cut from the previous shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference image. <Subject 1> is the ONLY person in the frame - NO other people, NO second person, NO duplicates, NO extra figures. <Subject 1> is COMPLETELY SILENT - mouth CLOSED, lips NEVER move, NO speech, NO sound.
<Picture 1> (first frame): fully_preserved - the opening frame, the boy is ALREADY seated in this pose from the very first frame.

detailed_description:
The shot BEGINS with the young boy (<Subject 1>) ALREADY seated at the table, both hands on the table edge, facing the camera - exactly as in <Picture 1>. He does NOT move into this pose; he is already there from the very first frame. His mouth stays CLOSED and his lips NEVER move - he is COMPLETELY SILENT the entire shot and makes NO sound.
[0-1s] The boy sits still, facing the camera, quiet, mouth closed.
[1-2s] His eyes shift slightly, a small thoughtful expression forms on his face, his gaze stays forward, his mouth stays CLOSED.
[2-3s] A quiet breath, a very small natural head movement, a subtle reaction. His mouth stays CLOSED.
[3-4s] He holds the pose - still seated, hands on the table, facing the camera, mouth CLOSED, a calm thoughtful expression.
The camera is a MEDIUM shot (50mm), eye level, COMPLETELY STILL - no pan, no orbit, no zoom, no push-in. The shot ends naturally on the boy still seated at the table, hands on the table, facing the camera, mouth CLOSED.

overall_soundscape:
COMPLETE SILENCE except a faint natural ambient bed - low room tone and the very faint electric hum of a bare bulb. There is NO human voice, NO speech, NO talking, NO mouth sounds, NO vocalization, NO words, NO gibberish. The boy makes NO sound at all.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. NO human voice, NO speech, NO talking, NO dialogue, NO words. Natural ambient sounds only - absolutely no music and no voice of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a visible second person, the boy speaking, the boy talking, the boy's mouth open, the boy's lips moving, the boy's mouth moving, lip movement, the boy's lips opening, the boy's mouth opening, the boy's jaw moving, any speech, any voice, any dialogue, any words, any gibberish, any vocalization, the boy moving into the pose, the boy standing up, the boy walking, pose change, camera movement, camera pan, camera orbit, camera zoom, camera push-in"""


def main():
    with io.open(WF, "r", encoding="utf-8") as f:
        wf = json.load(f)
    node = next(n for n in wf["nodes"] if n["id"] == 138)
    node["widgets_values"][0] = PROMPT
    if "widgets_values_named" in node and node["widgets_values_named"]:
        node["widgets_values_named"]["prompt"] = PROMPT
    with io.open(WF, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)
    print("node 138 prompt -> HARD SILENT-AUDIO LOCK (v2).")
    print("has <d>:", "<d>" in PROMPT, "| has <Subject 2>:", "<Subject 2>" in PROMPT)


if __name__ == "__main__":
    main()
