#!/usr/bin/env python
"""Shot D (jaisal_intro_D_reverse.json) v3 -> AGGRESSIVE NON-SPEAKING (GPT prompt).

WHY: even with the dialogue removed + a hard silent-audio lock, H3 still leaked
speech-like motion. GPT's diagnosis (adopted):
  1. The NARRATIVE CONCEPT of "listening to an off-screen question" triggers
     speech-like facial motion -> REMOVE the listening concept entirely.
  2. "young boy" causes identity/facial drift -> use <Subject 1> and let the
     reference image define the person.
  3. Make the shot AGGRESSIVELY non-speaking (dedicated CRITICAL PERFORMANCE
     RULE block + comprehensive negative).

Tweaks vs GPT's draft:
  - dropped "before speaking" (the word "speaking" can trigger the prior)
  - negative "boy standing/walking/entering" -> "person standing/walking/entering"

Only node 138 (the prompt) is changed. Refs/length/anchors untouched.
NOTE: the camera guy's line is DUBBED IN POST (D055/D089/D090); if any speech
still leaks, strip the H3 audio in post (ffmpeg -an).
"""
import json, io

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json"

PROMPT = """subject_definitions:
<Subject 1> is the person shown in the reference image. His identity, face, hair, clothing, body proportions and physical appearance come ONLY from the attached reference image.
<Subject 1> is the ONLY person in the frame.
CRITICAL PERFORMANCE RULE:
<Subject 1> DOES NOT SPEAK IN THIS VIDEO.
There is NO dialogue.
There is NO vocal performance.
His mouth remains FULLY CLOSED from the first frame to the last frame.
His lips remain completely still.
His jaw remains completely still.
His teeth are never visible.
His mouth never opens even slightly.
He does not lip-sync.
He does not mouth words.
He does not whisper.
He does not form speech sounds.
He does not make any talking-like facial movement.
<Picture 1> is the exact FIRST FRAME.
<Subject 1> is already seated exactly as shown in <Picture 1>, with both hands resting naturally on the table edge and facing the camera.
The first frame must match <Picture 1> exactly.

summary:
[reference generation]
A single continuous 4-second black-and-white cinematic shot.
The shot begins with <Subject 1> already seated at the table exactly as shown in <Picture 1>.
He remains seated throughout the entire shot.
He remains silent throughout the entire shot.
His mouth stays completely closed and motionless.
Only extremely subtle natural eye and head movements occur.
The performance is calm, natural and restrained - a quiet moment of gathering his thoughts.
There is NO horror performance, NO supernatural behavior and NO exaggerated acting.
The environment remains identical to the reference: dark near-black room, simple wooden table, one chair, single bare bulb directly above, hard top-down shadow, everything outside the bulb's illumination fading into pure black.
The camera is completely static.
The shot exists only to capture a quiet natural moment; dialogue is added later in post-production.

retention_analysis:
<Subject 1>: fully_preserved. Identity, face, hair, clothing, body, hands and seated pose remain unchanged.
<Picture 1>: fully_preserved. It defines the exact opening composition and seated pose.
Environment: fully_preserved. Table, chair, bulb, lighting, shadows and black background remain unchanged.
Performance: SILENT. No speaking animation of any kind.

detailed_description:
MANDATORY:
This is a SILENT PERFORMANCE TAKE.
Do NOT generate speech.
Do NOT generate lip-sync.
Do NOT animate the mouth.
Do NOT animate the jaw.
Do NOT open the lips.
Do NOT create any speech-like facial movement.
The mouth remains CLOSED and visually unchanged for the entire 4 seconds.
[0-1s]
<Subject 1> is already seated exactly as in <Picture 1>. He faces the camera. Both hands remain resting on the table edge. He remains still and calm. Mouth completely closed. Lips completely still. Eyes relaxed.
[1-2s]
Only his eyes make a very small natural adjustment. His gaze subtly shifts toward the camera and settles. His facial expression remains neutral and thoughtful. Mouth completely closed. Jaw completely still. No speech movement.
[2-3s]
He takes one quiet natural breath. A very small natural movement of the head or eyes occurs. The movement is restrained and realistic. Mouth completely closed. Lips completely still. No speaking.
[3-4s]
He settles into stillness. He looks toward the camera with a calm, thoughtful expression. Both hands remain on the table. His mouth remains completely closed and motionless. The shot ends on this exact quiet pose.
CAMERA LOCK:
MEDIUM 50mm SHOT. Eye level. Camera completely stationary. NO PAN. NO TILT. NO ORBIT. NO DOLLY. NO PUSH-IN. NO PULL-OUT. NO ZOOM. NO CAMERA ROTATION.
The framing remains identical from first frame to last frame.

overall_soundscape:
Natural diegetic room tone only. Very quiet room ambience. Subtle electrical hum from the bare bulb. Very faint chair creak. One quiet natural breath from <Subject 1>.
ABSOLUTELY NO HUMAN VOICE. NO SPEECH. NO WORDS. NO MURMURING. NO WHISPERING. NO VOCALIZATION.
Dialogue will be added separately in post-production.

non_diegetic_music:
NO MUSIC. NO instrumental music. NO musical instruments. NO melody. NO beat. NO rhythm. NO soundtrack. NO song. NO score. NO background music. NO ambient music. NO cinematic music.
Natural diegetic ambience only.

negative:
speech, speaking, talking, dialogue, voice, vocalization, mumbling, murmuring, whispering, lip-sync, mouth animation, mouth movement, lip movement, moving lips, opening mouth, open mouth, parted lips, visible teeth, moving jaw, jaw animation, speech expression, talking expression, singing, breathing through open mouth, exaggerated acting, horror, fear, scared expression, supernatural expression, unnatural expression, forced expression, facial distortion, multiple people, second person, duplicate person, extra person, extra figure, person standing, person walking, person entering, pose transition, standing up, moving into pose, camera movement, camera pan, camera tilt, camera orbit, camera rotation, camera zoom, camera push-in, camera pull-out, color, bright room, visible walls, visible ceiling, door, window, architecture, text, subtitles, watermark, logo"""


def main():
    with io.open(WF, "r", encoding="utf-8") as f:
        wf = json.load(f)
    node = next(n for n in wf["nodes"] if n["id"] == 138)
    node["widgets_values"][0] = PROMPT
    if "widgets_values_named" in node and node["widgets_values_named"]:
        node["widgets_values_named"]["prompt"] = PROMPT
    with io.open(WF, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)
    print("node 138 prompt -> AGGRESSIVE NON-SPEAKING (v3, GPT prompt + tweaks).")
    print("has <d>:", "<d>" in PROMPT, "| has <Subject 2>:", "<Subject 2>" in PROMPT,
          "| has 'young boy':", "young boy" in PROMPT, "| has 'listening':", "listening" in PROMPT.lower())


if __name__ == "__main__":
    main()
