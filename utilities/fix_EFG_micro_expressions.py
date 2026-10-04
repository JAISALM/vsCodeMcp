import json, os, shutil

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
BAK_DIR = r"d:\models\vsCodeMcp\workflow_backups"
PROMPT_DIR = r"d:\models\vsCodeMcp\Jaisal-intro\prompts"
os.makedirs(BAK_DIR, exist_ok=True)
os.makedirs(PROMPT_DIR, exist_ok=True)

NO_MUSIC = """🚨 HARD AUDIO RULE — NO MUSIC 🚨
AUDIO MUST BE 100% DIEGETIC. ABSOLUTELY ZERO MUSIC OF ANY KIND. NO score, NO soundtrack, NO drone, NO pad, NO synth, NO melody, NO chords, NO rhythm, NO beat, NO percussion, NO instruments, NO guitar, NO piano, NO strings, NO drums, NO singing, NO humming, NO musical tones. ONLY natural diegetic sounds.

"""

# ---------------- E (wonder, push-in 50->85mm) ----------------
E_PROMPT = NO_MUSIC + """subject_definitions:
<Subject 1> is the young boy shown in the reference images — identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy shown in the reference images seated at the table, the table surface bare.
<Picture 2> is the LAST frame: the young boy shown in the reference images seated at the table, small plants and a rose now growing on the table surface.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take that animates smoothly from <Picture 1> (Jaisal seated, bare table) to <Picture 2> (Jaisal seated, plants and a rose growing on the table). Plants GROW (not fade in): one tiny stem pushes through the table surface, another follows, a rose slowly opens, small plants populate the table. Jaisal SPEAKS throughout with clear mouth movement and natural micro-expressions of WONDER. A dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference images. There is ONLY ONE character - the young boy shown in the reference images - NO other people, NO second person, NO duplicates, NO extra figures.
<Picture 1> (first frame): fully_preserved - the opening frame.
<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.

detailed_description:
The shot BEGINS from <Picture 1> (Jaisal seated, bare table). The camera is a MEDIUM to CLOSE push (50mm to 85mm) — a slow, smooth push-in that tightens the frame from a medium shot to a close-up over the whole take.
[Shot 1] 00:00–00:03 — his eyes shift FIRST, his gaze dropping to the bare table, a small breath of surprise catching in his chest as he begins to speak, his lips moving naturally and clearly. <Subject 1> (S1) says, <d>[English] <breath> No real purpose. <pause> Just telling stories. <pause> Sharing stories. </d>
[Shot 1] 00:03–00:08 — a tiny green stem pushes UP through the wooden table surface on his left, then another on his right; the growth is slow and organic — the stems physically EMERGE and rise, NOT a fade-in. His eyes FOLLOW the stem as it pushes through, a slight, softening smile forming at the corner of his mouth, a small breath of wonder. He continues speaking, <d>[English] The stories happening around us, <pause> the ones we lived, <breath> the ones we know by hearsay. </d>
[Shot 1] 00:08–00:13 — the stems grow into white roses that slowly open and bloom; the camera finishes its slow push-in to a close-up. His gaze lifts from the rose, a quiet, thoughtful, almost tender look settling on his face as he finishes his line, <d>[English] <long pause> I'll share them with people in an interesting way... <pause> or even if it's not. <breath> I'll just share them. </d> The shot ends EXACTLY on <Picture 2>: plants fully grown and blooming on the table, Jaisal still seated, hands on the table.

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, a soft breath, the faint electric hum of a bare bulb, a subtle dry rustle as the plants grow, and Jaisal's calm natural voice as he speaks. Only these natural sounds, edge to edge.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, AI glow, holograms, glowing particles, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person, static character, frozen face, no mouth movement, silent character, fade-in plants, camera shake, fast zoom, sudden jump.

FINAL GENERATION REQUIREMENT:
ONE continuous take, ONE character (Jaisal) who SPEAKS with clear mouth movement and natural micro-expressions of WONDER (eyes shift first, gaze follows the rising stem, a slight softening smile, a small breath of surprise), a SLOW MEDIUM-to-CLOSE push-in (50mm to 85mm), the table goes from EMPTY (first frame) to PLANTS GROWN AND BLOOMING (final frame), plants GROW (not fade in), ZERO music, diegetic audio only."""

# ---------------- F (weight of limitation, static 50mm) ----------------
F_PROMPT = NO_MUSIC + """VISUAL / CHARACTER DEFINITIONS
<Subject 1> is the young man shown in the reference images — his identity, face, hair and clothing are EXACTLY as in <Picture 1>. He is the ONLY person VISIBLE in the frame.
<Subject 2> is a calm adult male voice (the camera guy). He is NOT visible in the frame — only his voice is heard, coming from OFF-SCREEN. He is NOT <Subject 1>.
<Picture 1> is the FIRST frame: Jaisal seated at the wooden table, both hands resting flat on the table, small plants and white roses GROWN and BLOOMING on the table (one on each side of his hands), a single bare bulb hangs directly above, pure black void background.
<Picture 2> is the FINAL frame: the SAME scene, but the plants have WILTED — the roses are drooping and closing, the leaves are dry and bent, the table looks empty and lifeless.

SHOT
[Shot 1] At 00:00.000 — the shot begins EXACTLY on <Picture 1>: Jaisal seated, hands on the table, plants blooming, bare bulb above, black void. The camera is a STATIC medium shot (50mm, eye level), COMPLETELY LOCKED — no movement, no pan, no zoom, no orbit.
[Shot 1] 00:00–00:03 — Jaisal is still, listening. His eyes are downcast, his expression quiet and heavy. The OFF-SCREEN male voice (<Subject 2>) asks, <d>[English] <breath> Why did you feel like doing this using AI? </d>
[Shot 1] 00:03–00:06 — Jaisal does NOT answer immediately. A slow breath, his gaze dropping to the plant on his left, a subtle frown forming at the corner of his mouth as he gathers his words. <Subject 1> (S1) says, <d>[English] <long pause> Cinema... <pause> or if you want to tell a story... </d>
[Shot 1] 00:06–00:10 — as he speaks, a leaf falls from the left plant, and the plant slowly bends; his eyes follow the falling leaf, a slow breath, his shoulders dropping slightly with the weight of it. <Subject 1> (S1) says, <d>[English] You need effort. <pause> Or you need one or two people with you. </d>
[Shot 1] 00:10–00:14 — the right rose begins to close and droop; his gaze follows it, a quiet, honest, almost tired look settling on his face, his shoulders dropping a little more. <Subject 1> (S1) says, <d>[English] I'm alone right now. <long pause> So there are some limitations to what I can do. </d>
[Shot 1] 00:14–00:18 — the plants are now fully wilted, the table looks empty and lifeless. Jaisal looks up, a small, determined glint returning to his eyes, a quiet resolve. <Subject 1> (S1) says, <d>[English] And I'm hoping AI can help me get past some of those limitations. <breath> That's why I came to the conclusion... let's try this show using AI. </d>

CAMERA
STATIC medium shot, 50mm, eye level, COMPLETELY LOCKED. No camera movement of any kind — no pan, no tilt, no orbit, no dolly, no zoom. The camera does not move at all.

VISUAL STYLE
Black & white, high contrast, fine film grain, deep blacks, 24fps, 16:9. Single bare bulb top-down, hard shadow, no fill light.

CHARACTER CONSISTENCY
Only ONE person VISIBLE (Jaisal, <Subject 1>). No other people, no duplicates. His face, hair and clothing stay EXACTLY as in <Picture 1> the entire shot. <Subject 2> is a VOICE ONLY — never shown.

AUDIO — FINAL HARD OVERRIDE
Diegetic ONLY: room tone, the bare bulb's faint electrical hum, the OFF-SCREEN camera guy's voice (<Subject 2>), Jaisal's voice as he speaks (natural, calm, honest, a little tired), and a very subtle dry rustle as the plants wilt. NO music, NO instruments, NO melody, NO beat, NO soundtrack. If uncertain, OMIT the sound. Silence is ALWAYS preferable to music.

NEGATIVE
music, soundtrack, score, melody, beat, rhythm, instruments, guitar, piano, strings, drums, singing, humming, any musical tone, color, camera movement, pan, zoom, orbit, dolly, multiple people visible, duplicate character, face distortion, the camera guy visible, the camera guy in frame, glowing effects, holograms, AI glow, fire, smoke, static character, frozen face, no mouth movement.

FINAL GENERATION REQUIREMENT
ONE static medium shot, ONE visible character (Jaisal) who SPEAKS with clear mouth movement and natural micro-expressions of the WEIGHT OF LIMITATION (a slow breath, gaze dropping to the plant, a subtle frown, shoulders dropping as the plant bends, a quiet honest look, then a small determined glint), an OFF-SCREEN male voice (<Subject 2>) asks the opening question, the plants go from BLOOMING (first frame) to WILTED (final frame) — leaf falls, plant bends, rose closes, room empties slowly, ZERO music, diegetic audio only, NO AI glow or holograms."""

# ---------------- G (wry honest half-smile, static 35mm) ----------------
G_PROMPT = NO_MUSIC + """VISUAL / CHARACTER DEFINITIONS
<Subject 1> is the young man shown in the reference images — his identity, face, hair and clothing are EXACTLY as in <Picture 1>. He is the ONLY person VISIBLE in the frame.
<Subject 2> is a calm adult male voice (the camera guy). He is NOT visible in the frame — only his voice is heard, coming from OFF-SCREEN. He is NOT <Subject 1>.
<Picture 1> is the FIRST frame: Jaisal seated at the wooden table, hands resting on the table, a single bare bulb hangs directly above, pure black void background. A few loose sheets of paper are beginning to float in from the darkness behind him.
<Picture 2> is the FINAL frame: Jaisal is GONE (vanished), replaced by dozens of loose sheets of paper floating in the air around the table, and a MICROPHONE on a stand has emerged and settled on the table among the papers. The bare bulb still hangs above. Pure black void.

SHOT
[Shot 1] At 00:00.000 — the shot begins on <Picture 1>: Jaisal seated at the table, bare bulb above, black void. The camera is a STATIC medium-wide shot (35mm, eye level), COMPLETELY LOCKED — no movement, no pan, no zoom, no orbit.
[Shot 1] 00:00–00:02 — Jaisal is seated, listening. Loose sheets of paper begin to float in from the darkness BEHIND him, drifting forward through the room. His eyes track the first paper as it drifts in, a small, curious look.
[Shot 1] 00:02–00:04 — the OFF-SCREEN male voice (<Subject 2>) asks, <d>[English] <breath> What can people expect from this channel? </d>
[Shot 1] 00:04–00:07 — more papers drift forward. A MICROPHONE on a stand emerges from the dark and settles on the table. A faint, wry, honest half-smile forms at the corner of Jaisal's mouth as his eyes shift to the strange objects, a small shrug of his shoulders. <Subject 1> (S1) says, <d>[English] As I said... <pause> stories, politics, sports, <pause> and a little bit of fantasy. </d>
[Shot 1] 00:07–00:09 — some papers drift back and VANISH into the darkness. His expression softens into a quiet, honest, almost uncertain look, a small breath. <Subject 1> (S1) says, <d>[English] I don't know if it'll work... <long pause> Let's see. </d>
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
ONE static medium-wide shot, ONE visible character (Jaisal) who SPEAKS with clear mouth movement and natural micro-expressions (a small curious look as the first paper drifts in, a faint wry honest half-smile and a small shrug as he looks at the strange objects, a quiet honest uncertain look), an OFF-SCREEN male voice (<Subject 2>) asks the opening question and the closing line, loose sheets of paper float in from the darkness, a microphone emerges and settles on the table, Jaisal VANISHES in the final beat (replaced by the floating papers), ZERO music, diegetic audio only, NO AI glow or holograms or colorful effects."""

TARGETS = [
    ("jaisal_intro_E_plants.json", E_PROMPT, "shot_E_plants_grow_v4_micro.txt", "pre_v4_micro.bak"),
    ("jaisal_intro_F_plants_die.json", F_PROMPT, "shot_F_plants_die_v2_micro.txt", "pre_v2_micro.bak"),
    ("jaisal_intro_G_papers.json", G_PROMPT, "shot_G_papers_v2_micro.txt", "pre_v2_micro.bak"),
]

for fname, prompt, pfile, bak in TARGETS:
    path = os.path.join(BASE, fname)
    with open(path, "r", encoding="utf-8") as f:
        wf = json.load(f)
    shutil.copy(path, os.path.join(BAK_DIR, fname + "." + bak))
    for n in wf["nodes"]:
        if n["id"] == 138:
            n["widgets_values"] = [prompt]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False)
    with open(os.path.join(PROMPT_DIR, pfile), "w", encoding="utf-8") as f:
        f.write(prompt)
    print("Updated", fname, "->", pfile)

print("DONE. Backups in", BAK_DIR)
