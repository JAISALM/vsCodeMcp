import json, os

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_E_plants.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_F_plants_die.json"
PROMPT_SAVE = r"d:\models\vsCodeMcp\Jaisal-intro\prompts\shot_F_plants_die.txt"

PROMPT = """🚨 HARD AUDIO RULE — NO MUSIC 🚨
AUDIO MUST BE 100% DIEGETIC. ABSOLUTELY ZERO MUSIC OF ANY KIND. NO score, NO soundtrack, NO drone, NO pad, NO synth, NO melody, NO chords, NO rhythm, NO beat, NO percussion, NO instruments, NO guitar, NO piano, NO strings, NO drums, NO singing, NO humming, NO musical tones. ONLY natural diegetic sounds.

VISUAL / CHARACTER DEFINITIONS
<Subject 1> is the young man shown in the reference images — his identity, face, hair and clothing are EXACTLY as in <Picture 1>. He is the ONLY person VISIBLE in the frame.
<Subject 2> is a calm adult male voice (the camera guy). He is NOT visible in the frame — only his voice is heard, coming from OFF-SCREEN. He is NOT <Subject 1>.
<Picture 1> is the FIRST frame: Jaisal seated at the wooden table, both hands resting flat on the table, small plants and white roses GROWN and BLOOMING on the table (one on each side of his hands), a single bare bulb hangs directly above, pure black void background.
<Picture 2> is the FINAL frame: the SAME scene, but the plants have WILTED — the roses are drooping and closing, the leaves are dry and bent, the table looks empty and lifeless.

SHOT
[Shot 1] At 00:00.000 — the shot begins EXACTLY on <Picture 1>: Jaisal seated, hands on the table, plants blooming, bare bulb above, black void. The camera is a STATIC medium shot (50mm, eye level), COMPLETELY LOCKED — no movement, no pan, no zoom, no orbit.
[Shot 1] 00:00–00:03 — Jaisal is still, listening. His eyes are downcast, his expression quiet. The OFF-SCREEN male voice (<Subject 2>) asks, <d>[English] <breath> Why did you feel like doing this using AI? </d>
[Shot 1] 00:03–00:06 — Jaisal does NOT answer immediately. A breath. His gaze drops to the plant on his left. <Subject 1> (S1) says, <d>[English] <long pause> Cinema... <pause> or if you want to tell a story... </d>
[Shot 1] 00:06–00:10 — as he speaks, a leaf falls from the left plant, and the plant slowly bends. Jaisal's eyes follow the falling leaf, his face thoughtful. <Subject 1> (S1) says, <d>[English] You need effort. <pause> Or you need one or two people with you. </d>
[Shot 1] 00:10–00:14 — the right rose begins to close and droop. Jaisal's shoulders drop slightly, a quiet, honest look. <Subject 1> (S1) says, <d>[English] I'm alone right now. <long pause> So there are some limitations to what I can do. </d>
[Shot 1] 00:14–00:18 — the plants are now fully wilted, the table looks empty and lifeless. Jaisal looks up, a small, determined glint in his eyes. <Subject 1> (S1) says, <d>[English] And I'm hoping AI can help me get past some of those limitations. <breath> That's why I came to the conclusion... let's try this show using AI. </d>

CAMERA
STATIC medium shot, 50mm, eye level, COMPLETELY LOCKED. No camera movement of any kind — no pan, no tilt, no orbit, no dolly, no zoom. The camera does not move at all.

VISUAL STYLE
Black & white, high contrast, fine film grain, deep blacks, 24fps, 16:9. Single bare bulb top-down, hard shadow, no fill light.

CHARACTER CONSISTENCY
Only ONE person VISIBLE (Jaisal, <Subject 1>). No other people, no duplicates. His face, hair and clothing stay EXACTLY as in <Picture 1> the entire shot. <Subject 2> is a VOICE ONLY — never shown.

AUDIO — FINAL HARD OVERRIDE
Diegetic ONLY: room tone, the bare bulb's faint electrical hum, the OFF-SCREEN camera guy's voice (<Subject 2>), Jaisal's voice as he speaks (natural, calm, honest), and a very subtle dry rustle as the plants wilt. NO music, NO instruments, NO melody, NO beat, NO soundtrack. If uncertain, OMIT the sound. Silence is ALWAYS preferable to music.

NEGATIVE
music, soundtrack, score, melody, beat, rhythm, instruments, guitar, piano, strings, drums, singing, humming, any musical tone, color, camera movement, pan, zoom, orbit, dolly, multiple people visible, duplicate character, face distortion, the camera guy visible, the camera guy in frame, glowing effects, holograms, AI glow, fire, smoke, static character, frozen face, no mouth movement.

FINAL GENERATION REQUIREMENT
ONE static medium shot, ONE visible character (Jaisal) who SPEAKS with clear mouth movement and natural micro-expressions (eyes shift first, gaze follows the falling leaf, a quiet honest look), an OFF-SCREEN male voice (<Subject 2>) asks the opening question, the plants go from BLOOMING (first frame) to WILTED (final frame) — leaf falls, plant bends, rose closes, room empties slowly, ZERO music, diegetic audio only, NO AI glow or holograms."""

with open(SRC, "r", encoding="utf-8") as f:
    wf = json.load(f)

def find(nid):
    for n in wf["nodes"]:
        if n["id"] == nid: return n
    raise KeyError(nid)

# refs: start = blooming (E's end), end = dead
find(137)["widgets_values"] = ["kf5_plants_alive_v9_00004_.png", "image"]
find(139)["widgets_values"] = ["kf6_plants_dead_v9_00004_.png", "image"]
# length: 312 -> 432 (18s)
find(136)["widgets_values"][3] = 432
# prompt
find(138)["widgets_values"] = [PROMPT]
# chain: load clip 5 (E), save clip 6
find(161)["widgets_values"] = ["h3_context", 5]
find(164)["widgets_values"] = ["h3_context/clip", 6]
# save prefix
find(92)["widgets_values"][0] = "jaisal_intro_F_plants_die"

with open(DST, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False)
os.makedirs(os.path.dirname(PROMPT_SAVE), exist_ok=True)
with open(PROMPT_SAVE, "w", encoding="utf-8") as f:
    f.write(PROMPT)
print("Built", DST)
print("Prompt saved", PROMPT_SAVE)
