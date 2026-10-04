"""Shot A: replace the prompt with the ChatGPT-verified no-music version
(user 2026-09-27: "this version from chatgpt had no music" — from
https://github.com/cushycrux/H3_LLM_Instructions).

Why this structure works (vs our 6-section prompt):
  - HARD AUDIO RULE at the VERY TOP (H3 weights first lines most)
  - short hard lines (one constraint per line)
  - explicit 5-sound WHITELIST + "silence is ALWAYS preferable"
  - double audio lock: top rule + "AUDIO — FINAL HARD OVERRIDE" at the end
  - huge negative list
  - bulb fully static (matches our 2026-09-26 decision)
  - camera locked, B&W, single character

ADAPTATION (user: "it had more foot sound which is not needed"):
  - added NO footsteps / foot sounds / walking sounds to the top rule,
    the final override, and the negative (character walks in -> H3
    inferred footsteps; they are NOT in the 5 permitted sounds).

Backup: workflow_backups/jaisal_intro_A_walkin.json.pre_chatgpt_prompt.bak
Also saved to: Jaisal-intro/prompts/shot_A_static_nomusic_v2.txt
"""
import json
import shutil

WF_A = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin.json"
BAK = r"d:\models\vsCodeMcp\workflow_backups\jaisal_intro_A_walkin.json.pre_chatgpt_prompt.bak"
PROMPT_SAVE = r"d:\models\vsCodeMcp\Jaisal-intro\prompts\shot_A_static_nomusic_v2.txt"

PROMPT = """\
🚨🚨🚨 HARD AUDIO RULE — NO MUSIC 🚨🚨🚨

AUDIO MUST BE 100% DIEGETIC.

ABSOLUTELY ZERO MUSIC OF ANY KIND.

Do NOT generate, add, infer, or suggest music under any circumstances.

NO score.
NO soundtrack.
NO background music.
NO cinematic music.
NO emotional music.
NO suspense music.
NO atmospheric music.
NO tension music.
NO musical bed.
NO drone.
NO pad.
NO synth.
NO melody.
NO harmony.
NO chords.
NO rhythm.
NO beat.
NO percussion.
NO instruments.
NO singing.
NO humming.
NO musical tones.
NO footsteps.
NO foot sounds.
NO walking sounds.

The scene may be cinematic, dramatic, mysterious, or emotionally intense, but NONE of those qualities may be represented using music.

ALL AUDIO MUST COME FROM PHYSICAL SOURCES THAT EXIST INSIDE THE SCENE.

ONLY these five sounds are permitted:

1. very quiet natural room tone
2. faint electrical buzz physically produced by the bare bulb
3. soft chair scraping against the wooden floor
4. one gentle natural breath from Jaisal
5. quiet natural creak of the chair settling after he sits
NO OTHER SOUND.

If the model is uncertain whether a sound is allowed, OMIT THE SOUND.

Silence is ALWAYS preferable to adding an unapproved sound.

This audio rule OVERRIDES every other instruction in this prompt.

# ============================================================
VISUAL / CHARACTER DEFINITIONS
subject_definitions:

<Subject 1>: the young boy shown in the reference images. His identity, face, hair, clothing and body build come ONLY from the attached reference image. Do NOT redesign or reinterpret him.

<Picture 1>: the FIRST FRAME — an empty, extremely dark room. A simple wooden table, one chair and one bare bulb hanging directly above the table. The bulb is the ONLY light source. Hard top-down lighting creates a strong shadow. Everything outside the bulb's light pool falls into near-total blackness. NO PERSON is present.

<Picture 2>: the FINAL FRAME — the young boy shown in the reference images is seated at the table, with both hands resting naturally on the edge of the table.

# ============================================================
SHOT
Create ONE continuous shot.

The shot begins EXACTLY on <Picture 1>.

The room is completely empty.

The table, chair and bare bulb remain in exactly the same positions throughout the entire shot.

The bulb is physically fixed in place.

The bulb NEVER swings.
The bulb NEVER oscillates.
The bulb NEVER moves.
The bulb NEVER flickers.
The light source remains completely steady.

After the opening empty-room moment, a soft chair scrape is heard.

Jaisal <Subject 1> enters naturally from the surrounding darkness.

He approaches the table.

He grabs the chair.

He drags the chair into position with one natural movement.

He sits down.

His movement is realistic and continuous.

After sitting, both of his hands come to rest naturally on the edge of the table.

He remains seated.

He does NOT stand back up.

He does NOT leave.

He does NOT disappear.

He does NOT duplicate.

There is ONLY ONE PERSON in the entire shot.

The shot ends EXACTLY on <Picture 2>.

# ============================================================
CAMERA
WIDE STATIC EYE-LEVEL CAMERA.

35mm lens.

The camera is completely locked off.

NO camera movement.

NO dolly.

NO push-in.

NO pull-out.

NO zoom.

NO pan.

NO tilt.

NO handheld movement.

NO camera drift.

NO reframing.

The composition remains stable from the first frame until the final frame.

# ============================================================
VISUAL STYLE
Black and white.

High contrast.

Fine natural film grain.

Photorealistic cinematic image.

Natural physical lighting.

Deep blacks.

The area outside the bulb's illumination remains extremely dark.

The visual mood comes ONLY from composition, lighting, performance and physical movement.

Do NOT create mood using music or artificial audio.

24fps.

16:9.

# ============================================================
CHARACTER CONSISTENCY
<Subject 1> is the ONLY human character.

Preserve the exact identity from the reference image.

Preserve face.

Preserve hair.

Preserve clothing.

Preserve body proportions.

Preserve overall appearance.

NO second person.

NO background person.

NO silhouette of another person.

NO duplicate.

NO clone.

NO reflection containing another person.

# ============================================================
AUDIO — FINAL HARD OVERRIDE
The final audio track must contain ONLY:

ROOM TONE
+
BARE BULB ELECTRICAL BUZZ
+
CHAIR SCRAPE
+
ONE NATURAL BREATH
+
CHAIR CREAK

Nothing else.

NO MUSIC.

NO SCORE.

NO SOUNDTRACK.

NO MUSICAL BACKGROUND.

NO INSTRUMENT.

NO MELODY.

NO DRONE.

NO PAD.

NO SYNTH.

NO RHYTHM.

NO BEAT.

NO MUSICAL HUMMING.

NO NON-DIEGETIC AUDIO.

NO FOOTSTEPS.

NO FOOT SOUNDS.

NO WALKING SOUNDS.

The electrical buzz must sound like a real electrical fixture, NOT a musical drone.

The room tone must sound like real physical room ambience, NOT an atmospheric music bed.

All sounds must be natural, subtle and physically grounded.

If necessary, use silence.

NEVER fill silence with music.

# ============================================================
NEGATIVE
music, score, soundtrack, background music, cinematic music,
emotional music, suspense music, atmospheric music, tension music,
horror music, musical bed, musical drone, drone, pad, synth,
melody, harmony, chord, rhythm, beat, pulse, percussion,
instrument, piano, guitar, violin, cello, strings, drums,
bass music, singing, humming, song, vocal music, soundtrack,
non-diegetic audio, artificial soundscape, musical ambience,
footsteps, foot sounds, walking sounds,

multiple people, second person, duplicate person, clone,
extra figure, background person, silhouette of another person,
extra chair, extra table,

standing after sitting, leaving the room, disappearing,
character duplication, character morphing,

bulb swinging, bulb oscillating, bulb moving, bulb flickering,
moving light, changing light, unstable light,

camera movement, zoom, pan, tilt, dolly, tracking shot,
handheld camera, camera shake, camera drift,

color, bright room, white wall, cream wall, visible ceiling,
text, subtitles, watermark, logo.

# ============================================================
FINAL GENERATION REQUIREMENT
ONE continuous shot.

ONE character.

ONE room.

ONE table.

ONE chair.

ONE fixed bulb.

ZERO music.

DIEGETIC SOUND ONLY.

The final frame must match <Picture 2>."""

shutil.copy(WF_A, BAK)
wf = json.load(open(WF_A, encoding="utf-8"))
node = next(n for n in wf["nodes"] if n["id"] == 138)
node["widgets_values"][0] = PROMPT
with open(WF_A, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=1)
with open(PROMPT_SAVE, "w", encoding="utf-8") as f:
    f.write(PROMPT)
print("A prompt REPLACED with the ChatGPT-verified no-music version (+footstep ban).")
print("Backup:", BAK)
print("Saved:", PROMPT_SAVE)
