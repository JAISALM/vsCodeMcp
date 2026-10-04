import json, os, shutil

E_PATH = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_E_plants.json"
BAK_DIR = r"d:\models\vsCodeMcp\workflow_backups"
PROMPT_SAVE = r"d:\models\vsCodeMcp\Jaisal-intro\prompts\shot_E_plants_grow_v3.txt"
os.makedirs(BAK_DIR, exist_ok=True)

PROMPT = """🚨 HARD AUDIO RULE — NO MUSIC 🚨
AUDIO MUST BE 100% DIEGETIC. ABSOLUTELY ZERO MUSIC OF ANY KIND. NO score, NO soundtrack, NO drone, NO pad, NO synth, NO melody, NO chords, NO rhythm, NO beat, NO percussion, NO instruments, NO guitar, NO piano, NO strings, NO drums, NO singing, NO humming, NO musical tones. ONLY natural diegetic sounds.

subject_definitions:
<Subject 1> is the young boy shown in the reference images — identity, face, hair, clothing and build come from the attached reference image, NOT from this text description.
<Picture 1> is the FIRST frame: the young boy shown in the reference images seated at the table, the table surface bare.
<Picture 2> is the LAST frame: the young boy shown in the reference images seated at the table, small plants and a rose now growing on the table surface.

summary:
[reference generation] A single continuous black & white, high contrast, fine film grain, 24fps take that animates smoothly from <Picture 1> (Jaisal seated, bare table) to <Picture 2> (Jaisal seated, plants and a rose growing on the table). Plants GROW (not fade in): one tiny stem pushes through the table surface, another follows, a rose slowly opens, small plants populate the table. Jaisal SPEAKS throughout — his mouth moves clearly with natural micro-expressions. A dark near-black room, a simple wooden table, one chair, a single bare bulb hanging directly above as the ONLY light source, casting a hard top-down shadow, everything outside the bulb's light pool fading to pure black. The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.

retention_analysis:
<Subject 1> (appears in this shot): fully_preserved - the young boy shown in the reference images. There is ONLY ONE character - the young boy shown in the reference images - NO other people, NO second person, NO duplicates, NO extra figures.
<Picture 1> (first frame): fully_preserved - the opening frame.
<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.

detailed_description:
The shot BEGINS from <Picture 1> (Jaisal seated, bare table). The camera is a MEDIUM to CLOSE push (50mm to 85mm) — a slow, smooth push-in that tightens the frame from a medium shot to a close-up over the whole take.
[Shot 1] 00:00–00:03 — Jaisal's eyes shift first, his gaze dropping to the table. He begins to speak, his lips moving naturally and clearly, his expression soft and thoughtful. <Subject 1> (S1) says, <d>[English] <breath> No real purpose. <pause> Just telling stories. <pause> Sharing stories. </d>
[Shot 1] 00:03–00:08 — a tiny green stem pushes UP through the wooden table surface on his left, then another on his right. The growth is slow and organic — the stems physically EMERGE and rise, NOT a fade-in. Jaisal's eyes follow the stem as it rises, a small breath catching in his chest, his head tilting very slightly. He continues speaking, <d>[English] The stories happening around us, <pause> the ones we lived, <breath> the ones we know by hearsay. </d>
[Shot 1] 00:08–00:13 — the stems grow into white roses that slowly open and bloom. The camera finishes its slow push-in to a close-up. The shot ends EXACTLY on <Picture 2>: plants fully grown and blooming on the table, Jaisal still seated, hands on the table, finishing his line with a quiet, thoughtful look, <d>[English] <long pause> I'll share them with people in an interesting way... <pause> or even if it's not. <breath> I'll just share them. </d>

overall_soundscape:
A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, a soft breath, the faint electric hum of a bare bulb, a subtle dry rustle as the plants grow, and Jaisal's calm natural voice as he speaks. Only these natural sounds, edge to edge.

non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely no music of any kind.

negative: color, multiple people, second person, duplicate character, extra chairs, extra figures, AI glow, holograms, glowing particles, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person, static character, frozen face, no mouth movement, silent character, fade-in plants, camera shake, fast zoom, sudden jump.

FINAL GENERATION REQUIREMENT:
ONE continuous take, ONE character (Jaisal) who SPEAKS with clear mouth movement and natural micro-expressions (eyes shift first, gaze follows the growing stem, a small breath), a SLOW MEDIUM-to-CLOSE push-in (50mm to 85mm), the table goes from EMPTY (first frame) to PLANTS GROWN AND BLOOMING (final frame), plants GROW (not fade in), ZERO music, diegetic audio only."""

with open(E_PATH, "r", encoding="utf-8") as f:
    wf = json.load(f)
shutil.copy(E_PATH, os.path.join(BAK_DIR, "jaisal_intro_E_plants.json.pre_v3_dialogue_pushin.bak"))

def find(nid):
    for n in wf["nodes"]:
        if n["id"] == nid: return n
    raise KeyError(nid)

find(138)["widgets_values"] = [PROMPT]

with open(E_PATH, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False)
os.makedirs(os.path.dirname(PROMPT_SAVE), exist_ok=True)
with open(PROMPT_SAVE, "w", encoding="utf-8") as f:
    f.write(PROMPT)
print("E prompt v3 written (dialogue + push-in camera). Backup in", BAK_DIR)
print("Prompt saved", PROMPT_SAVE)
