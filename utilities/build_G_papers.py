import json, os

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_F_plants_die.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_papers.json"
PROMPT_SAVE = r"d:\models\vsCodeMcp\Jaisal-intro\prompts\shot_G_papers.txt"

PROMPT = """🚨 HARD AUDIO RULE — NO MUSIC 🚨
AUDIO MUST BE 100% DIEGETIC. ABSOLUTELY ZERO MUSIC OF ANY KIND. NO score, NO soundtrack, NO drone, NO pad, NO synth, NO melody, NO chords, NO rhythm, NO beat, NO percussion, NO instruments, NO guitar, NO piano, NO strings, NO drums, NO singing, NO humming, NO musical tones. ONLY natural diegetic sounds.

VISUAL / CHARACTER DEFINITIONS
<Subject 1> is the young man shown in the reference images — his identity, face, hair and clothing are EXACTLY as in <Picture 1>. He is the ONLY person VISIBLE in the frame.
<Subject 2> is a calm adult male voice (the camera guy). He is NOT visible in the frame — only his voice is heard, coming from OFF-SCREEN. He is NOT <Subject 1>.
<Picture 1> is the FIRST frame: Jaisal seated at the wooden table, hands resting on the table, a single bare bulb hangs directly above, pure black void background. A few loose sheets of paper are beginning to float in from the darkness behind him.
<Picture 2> is the FINAL frame: Jaisal is GONE (vanished), replaced by dozens of loose sheets of paper floating in the air around the table, and a MICROPHONE on a stand has emerged and settled on the table among the papers. The bare bulb still hangs above. Pure black void.

SHOT
[Shot 1] At 00:00.000 — the shot begins on <Picture 1>: Jaisal seated at the table, bare bulb above, black void. The camera is a STATIC medium-wide shot (35mm, eye level), COMPLETELY LOCKED — no movement, no pan, no zoom, no orbit.
[Shot 1] 00:00–00:02 — Jaisal is seated, listening. Loose sheets of paper begin to float in from the darkness BEHIND him, drifting forward through the room.
[Shot 1] 00:02–00:04 — the OFF-SCREEN male voice (<Subject 2>) asks, <d>[English] <breath> What can people expect from this channel? </d>
[Shot 1] 00:04–00:07 — more papers drift forward. A MICROPHONE on a stand emerges from the dark and settles on the table. Jaisal's eyes shift to the papers, a small thoughtful look. <Subject 1> (S1) says, <d>[English] As I said... <pause> stories, politics, sports, <pause> and a little bit of fantasy. </d>
[Shot 1] 00:07–00:09 — some papers drift back and VANISH into the darkness. Jaisal's expression is quiet, honest. <Subject 1> (S1) says, <d>[English] I don't know if it'll work... <long pause> Let's see. </d>
[Shot 1] 00:09–00:11 — JAISAL himself VANISHES — he is gone, replaced by the floating papers. The microphone settles among the papers. The OFF-SCREEN voice (<Subject 2>) says, <d>[English] Let's see. </d> The shot ends on <Picture 2>: papers floating, mic on the table, Jaisal gone.

CAMERA
STATIC medium-wide shot, 35mm, eye level, COMPLETELY LOCKED. No camera movement of any kind — no pan, no tilt, no orbit, no dolly, no zoom. The camera does not move at all.

VISUAL STYLE
Black & white, high contrast, fine film grain, deep blacks, 24fps, 16:9. Single bare bulb top-down, hard shadow, no fill light.

CHARACTER CONSISTENCY
Only ONE person VISIBLE (Jaisal, <Subject 1>) until he VANISHES in the final beat. No other people, no duplicates. <Subject 2> is a VOICE ONLY — never shown.

AUDIO — FINAL HARD OVERRIDE
Diegetic ONLY: room tone, the bare bulb's faint electrical hum, the OFF-SCREEN camera guy's voice (<Subject 2>), Jaisal's voice as he speaks (natural, calm, honest), and a subtle soft rustle of paper drifting. NO music, NO instruments, NO melody, NO beat, NO soundtrack. If uncertain, OMIT the sound. Silence is ALWAYS preferable to music.

NEGATIVE
music, soundtrack, score, melody, beat, rhythm, instruments, guitar, piano, strings, drums, singing, humming, any musical tone, color, camera movement, pan, zoom, orbit, dolly, multiple people visible, duplicate character, face distortion, the camera guy visible, the camera guy in frame, glowing effects, holograms, AI glow, fire, smoke, colorful effects, static character, frozen face, no mouth movement.

FINAL GENERATION REQUIREMENT
ONE static medium-wide shot, ONE visible character (Jaisal) who SPEAKS with clear mouth movement and natural micro-expressions, an OFF-SCREEN male voice (<Subject 2>) asks the opening question and the closing line, loose sheets of paper float in from the darkness, a microphone emerges and settles on the table, Jaisal VANISHES in the final beat (replaced by the floating papers), ZERO music, diegetic audio only, NO AI glow or holograms or colorful effects."""

with open(SRC, "r", encoding="utf-8") as f:
    wf = json.load(f)

def find(nid):
    for n in wf["nodes"]:
        if n["id"] == nid: return n
    raise KeyError(nid)

# refs: start = Jaisal + paper, end = mic + papers (Jaisal gone)
find(137)["widgets_values"] = ["kf7a_v4.png", "image"]
find(139)["widgets_values"] = ["mic+paper.png", "image"]
# length: 432 -> 264 (11s)
find(136)["widgets_values"][3] = 264
# prompt
find(138)["widgets_values"] = [PROMPT]
# chain: load clip 6 (F), save clip 7
find(161)["widgets_values"] = ["h3_context", 6]
find(164)["widgets_values"] = ["h3_context/clip", 7]
# save prefix
find(92)["widgets_values"][0] = "jaisal_intro_G_papers"

with open(DST, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False)
os.makedirs(os.path.dirname(PROMPT_SAVE), exist_ok=True)
with open(PROMPT_SAVE, "w", encoding="utf-8") as f:
    f.write(PROMPT)
print("Built", DST)
print("Prompt saved", PROMPT_SAVE)
