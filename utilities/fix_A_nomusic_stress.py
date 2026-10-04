"""Shot A: STRESS the no-music lock (user 2026-09-27: a guitar tone leaked into
jaisal_intro_A_walkin_00007_). H3's audio prior leaks instruments even with the
generic no-music list. Strengthen all three audio sections with EXPLICIT
instrument naming (guitar, strings, plucked strings, etc.).

Edits node 138 of jaisal_intro_A_walkin.json.
Backup: workflow_backups/jaisal_intro_A_walkin.json.pre_nomusic_stress.bak
"""
import json
import shutil

WF_A = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin.json"
BAK = r"d:\models\vsCodeMcp\workflow_backups\jaisal_intro_A_walkin.json.pre_nomusic_stress.bak"

shutil.copy(WF_A, BAK)
wf = json.load(open(WF_A, encoding="utf-8"))
node = next(n for n in wf["nodes"] if n["id"] == 138)
p = node["widgets_values"][0]

# 1. soundscape: name the ONLY allowed sounds + explicitly forbid instruments
old1 = ("overall_soundscape:\n"
        "A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, "
        "the faint electric hum of a bare bulb, a soft chair scrape on wood, a gentle breath, "
        "the quiet creak of the chair settling. Only these natural sounds, edge to edge.")
new1 = ("overall_soundscape:\n"
        "A continuous natural ambient bed fills the ENTIRE shot with no gaps - low room tone, "
        "the faint electric hum of a bare bulb, a soft chair scrape on wood, a gentle breath, "
        "the quiet creak of the chair settling. ONLY these natural sounds, edge to edge. "
        "ABSOLUTELY NO instruments of any kind - NO guitar, NO plucked strings, NO strumming, "
        "NO strings, NO piano, NO keys, NO drums, NO beat, NO melody, NO humming, NO singing, "
        "NO voice, NO speech. The audio is PURELY ambient room sound.")
assert old1 in p, "soundscape block not found"
p = p.replace(old1, new1)

# 2. non_diegetic_music: exhaustive instrument list
old2 = ("non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, "
        "NO beat, NO rhythm, NO soundtrack, NO song, NO score, NO background music, NO ambient "
        "music, NO cinematic score, NO soundtrack bed. Natural ambient sounds only - absolutely "
        "no music of any kind.")
new2 = ("non_diegetic_music: NO music of ANY kind. NO instrumental music, NO musical instruments, "
        "NO guitar, NO acoustic guitar, NO electric guitar, NO plucked strings, NO strumming, "
        "NO string instruments, NO violin, NO cello, NO piano, NO keyboard, NO drums, NO "
        "percussion, NO melody, NO tune, NO beat, NO rhythm, NO humming, NO singing, NO song, "
        "NO score, NO soundtrack, NO background music, NO ambient music, NO cinematic score, "
        "NO soundtrack bed, NO musical tone of any kind. Natural ambient sounds ONLY.")
assert old2 in p, "non_diegetic_music block not found"
p = p.replace(old2, new2)

# 3. negative: add instrument terms
old3 = ("bulb swinging, bulb oscillating, bulb flickering, moving light, swinging bulb, "
        "flickering light")
new3 = (old3 + ", guitar, guitar sound, plucked strings, strumming, any instrument, any "
        "instrumental sound, melody, musical tone, humming, singing, music")
assert old3 in p, "negative tail not found"
p = p.replace(old3, new3)

node["widgets_values"][0] = p
with open(WF_A, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=1)
print("A prompt no-music lock STRESSED. Backup:", BAK)
