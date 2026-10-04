# -*- coding: utf-8 -*-
"""
Write the 10 Jaisal Kut intro R2V prompts (hand-crafted, 2026-09-14).

Fixes the three problems the user called out:
  1. Character = OUR character (Jaisal), specific + consistent - not a generic
     "school kid".
  2. <Picture N> tags match the ACTUAL reference images for that shot, in order.
  3. Proper 6-section H3 R2V structure, tight (no 500-word bloat).

NO MUSIC (D041). Refs ONLY from the keyframes folder (D069). 2-3 refs per shot
(D020). Output: Jaisal-intro\\prompts\\shot_<X>.txt
"""
import os

OUT = r"D:\models\vsCodeMcp\Jaisal-intro\prompts"
os.makedirs(OUT, exist_ok=True)

# --- Shared blocks -------------------------------------------------------
CHAR = ("Jaisal, a young man - short dark hair, a rose-pink collared "
        "shirt, full-length black trousers, a black school bag")
SCENE = ("a dark near-black room, a simple wooden table, one chair, a single "
         "bare bulb hanging directly above as the ONLY light source, casting a "
         "hard top-down shadow, everything outside the bulb's light pool fading "
         "to pure black")
LOOK = "black & white, high contrast, fine film grain, 24fps"
NOMUSIC = ("NO music, NO instrumental music, NO musical instruments, NO melody, "
           "NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient sounds only.")
ONECHAR = ("There is ONLY ONE character - the single young man <Subject 1> - NO other "
           "people, NO second person, NO duplicates, NO extra figures.")


def prompt(subject_defs, summary, retention, detailed, soundscape, negative):
    return (
        "subject_definitions:\n" + subject_defs + "\n\n"
        "summary:\n" + summary + "\n\n"
        "retention_analysis:\n" + retention + "\n\n"
        "detailed_description:\n" + detailed + "\n\n"
        "overall_soundscape:\n" + soundscape + "\n\n"
        "non_diegetic_music: " + NOMUSIC + "\n\n"
        "negative: " + negative
    )


P = {}

# --- A | THE WALK IN (5s) ------------------------------------------------
P["A"] = prompt(
    "<Subject 1> is " + CHAR + ", seated at a simple wooden table.\n"
    "<Picture 1> is the FIRST frame: the empty dark room - " + SCENE + ", NO person.\n"
    "<Picture 2> is the LAST frame: " + CHAR + " seated at the table, both hands resting on the table edge.",
    "[reference generation] A single continuous " + LOOK + " take that animates smoothly from "
    "<Picture 1> (the empty dark room, no person) to <Picture 2> (Jaisal seated at the table). "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Subject 1> (appears in this shot): fully_preserved - face, short dark hair, rose-pink shirt, black trousers, black bag retained. "
    + ONECHAR + "\n"
    "<Picture 1> (first frame): fully_preserved - the opening frame.\n"
    "<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.",
    "The shot BEGINS from <Picture 1> (the empty dark room, no person). The bare bulb swings gently; a chair scrapes across the floor; "
    "Jaisal <Subject 1> enters from the darkness, drags the chair, and sits down, hands coming to rest on the table edge. "
    "He does NOT stand, does NOT leave, is NOT duplicated. "
    "Camera: a WIDE STATIC eye-level shot (35mm), the camera is locked and does NOT move, push, drift, tilt, pan or zoom. "
    "The shot ENDS exactly on <Picture 2> (Jaisal seated at the table, hands on the table edge).",
    "room tone, a soft chair scrape, a gentle breath.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, bright wall, white wall, cream wall, "
    "visible ceiling, text, subtitles, watermark, logo, the man standing, the man leaving, a second person"
)

# --- B | SETUP (3s) ------------------------------------------------------
P["B"] = prompt(
    "<Subject 1> is " + CHAR + ", seated at a simple wooden table.\n"
    "<Picture 1> is the FIRST frame: " + CHAR + " seated at the table, hands still low.\n"
    "<Picture 2> is the LAST frame: " + CHAR + " seated at the table, both hands resting ON the table edge (visible above the edge).",
    "[reference generation] A single continuous " + LOOK + " take that animates smoothly from "
    "<Picture 1> (Jaisal seated, hands low) to <Picture 2> (Jaisal seated, both hands resting on the table edge). "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Subject 1> (appears in this shot): fully_preserved - face, short dark hair, rose-pink shirt, black trousers, black bag retained. "
    + ONECHAR + "\n"
    "<Picture 1> (first frame): fully_preserved - the opening frame.\n"
    "<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.",
    "The shot BEGINS from <Picture 1> (Jaisal seated, hands low). Jaisal settles calmly; both hands come up and rest ON the table edge, "
    "visible above the edge, NOT under it. He is still and composed. "
    "Camera: a MEDIUM shot (50mm), slight low angle, the camera is locked and does NOT move, push, drift, tilt, pan or zoom. "
    "The shot ENDS exactly on <Picture 2> (Jaisal seated, both hands on the table edge).",
    "room tone, a soft breath, a faint bulb hum.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, hands under the table, bright wall, white wall, "
    "cream wall, visible ceiling, text, subtitles, watermark, logo, a second person"
)

# --- C | THE HOOK - SLOW HEAD TWIST (camera node, ~10s) ------------------
P["C"] = prompt(
    "<Subject 1> is " + CHAR + ", seated at a simple wooden table, bulb directly above his head.\n"
    "<Picture 1> is the FIRST frame: " + CHAR + " seated, head facing the LEFT-BACK side, body lit the same.",
    "[reference generation] A single continuous " + LOOK + " take that animates from <Picture 1> (Jaisal seated, head facing the left-back "
    "side) as his head rotates SLOWLY 180 degrees toward the camera while his body stays still and lit the same. "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Subject 1> (appears in this shot): fully_preserved - face, short dark hair, rose-pink shirt, black trousers, black bag retained. "
    + ONECHAR + "\n"
    "<Picture 1> (first frame): fully_preserved - the opening frame.",
    "The shot BEGINS from <Picture 1> (Jaisal seated, head facing the left-back side). Silence. Jaisal's eyes shift first. "
    "His head begins to rotate SLOWLY 180 degrees toward the camera while his body does NOT react and stays lit the same. "
    "The camera rotates and pushes in at exactly the same rate as the head turns. "
    "Camera: a CLOSE UP (85mm), eye level, the camera rotates and pushes in at the same rate as the head turn. "
    "The shot ENDS with Jaisal's head fully turned toward the camera.",
    "room tone, a faint bulb hum, a slow breath.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, body turning, body reacting, bright wall, white wall, "
    "cream wall, visible ceiling, text, subtitles, watermark, logo, a second person"
)

# --- D | PERFECT REVERSE (7s) -------------------------------------------
P["D"] = prompt(
    "<Subject 1> is " + CHAR + ", seated at a simple wooden table.\n"
    "<Picture 1> is the FIRST frame: " + CHAR + " seated, head turned 180 degrees toward the camera.\n"
    "<Picture 2> is the LAST frame: " + CHAR + " seated normally, both hands resting on the table edge.",
    "[reference generation] A single continuous " + LOOK + " take that animates smoothly from "
    "<Picture 1> (Jaisal seated, head turned 180 degrees) to <Picture 2> (Jaisal seated normally, hands on the table). "
    "Everything REVERSES: the head rotation reverses, the camera rotation reverses, clothing motion reverses. "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Subject 1> (appears in this shot): fully_preserved - face, short dark hair, rose-pink shirt, black trousers, black bag retained. "
    + ONECHAR + "\n"
    "<Picture 1> (first frame): fully_preserved - the opening frame.\n"
    "<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.",
    "The shot BEGINS from <Picture 1> (Jaisal seated, head turned 180 degrees). Everything reverses perfectly: the head rotation reverses, "
    "the camera rotation reverses, clothing motion reverses. We land on ordinary seated Jaisal, hands on the table. "
    "The weird version was his mind. "
    "Camera: a MEDIUM REVERSE shot (50mm), the camera rotation reverses. "
    "The shot ENDS exactly on <Picture 2> (Jaisal seated normally, both hands on the table edge).",
    "room tone, a soft breath, a faint bulb hum.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, bright wall, white wall, cream wall, "
    "visible ceiling, text, subtitles, watermark, logo, a second person"
)

# --- E | DREAM - PLANTS GROW (13s) --------------------------------------
P["E"] = prompt(
    "<Subject 1> is " + CHAR + ", seated at a simple wooden table.\n"
    "<Picture 1> is the FIRST frame: " + CHAR + " seated at the table, the table surface bare.\n"
    "<Picture 2> is the LAST frame: " + CHAR + " seated at the table, small plants and a rose now growing on the table surface.",
    "[reference generation] A single continuous " + LOOK + " take that animates smoothly from "
    "<Picture 1> (Jaisal seated, bare table) to <Picture 2> (Jaisal seated, plants and a rose growing on the table). "
    "Plants GROW (not fade in): one tiny stem pushes through the table surface, another follows, a rose slowly opens, small plants populate the table. "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Subject 1> (appears in this shot): fully_preserved - face, short dark hair, rose-pink shirt, black trousers, black bag retained. "
    + ONECHAR + "\n"
    "<Picture 1> (first frame): fully_preserved - the opening frame.\n"
    "<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.",
    "The shot BEGINS from <Picture 1> (Jaisal seated, bare table). Plants GROW (not fade in): one tiny stem pushes through the table surface, "
    "another follows, a rose slowly opens, small plants populate the table. The room is created by the story. "
    "Camera: a MEDIUM to CLOSE push (50mm to 85mm), a slow push-in. "
    "The shot ENDS exactly on <Picture 2> (Jaisal seated, plants and a rose growing on the table).",
    "room tone, a soft breath, a faint bulb hum, a subtle rustle as the plants grow.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, AI glow, holograms, glowing particles, "
    "bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person"
)

# --- F | LIMIT - PLANTS DIE SLOW (18s) ----------------------------------
P["F"] = prompt(
    "<Subject 1> is " + CHAR + ", seated at a simple wooden table with small plants and a rose on it.\n"
    "<Picture 1> is the FIRST frame: " + CHAR + " seated at the table, small plants and a rose alive on the table surface.\n"
    "<Picture 2> is the LAST frame: " + CHAR + " seated at the table, the plants now dead and withered on the table surface.",
    "[reference generation] A single continuous " + LOOK + " take that animates smoothly from "
    "<Picture 1> (Jaisal seated, plants alive) to <Picture 2> (Jaisal seated, plants dead and withered). "
    "While Jaisal admits limitation, a leaf falls, the plant bends, the rose closes, the room empties slowly. "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Subject 1> (appears in this shot): fully_preserved - face, short dark hair, rose-pink shirt, black trousers, black bag retained. "
    + ONECHAR + "\n"
    "<Picture 1> (first frame): fully_preserved - the opening frame.\n"
    "<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame.",
    "The shot BEGINS from <Picture 1> (Jaisal seated, plants alive). Jaisal does not answer immediately; he breathes, looks at the plant. "
    "While he admits limitation, a leaf falls, the plant bends, the rose closes, the room empties slowly. No AI glow, no holograms - just limitation. "
    "Camera: a CLOSE UP (85mm), the camera is locked and does NOT move, push, drift, tilt, pan or zoom. "
    "The shot ENDS exactly on <Picture 2> (Jaisal seated, plants dead and withered).",
    "room tone, a slow breath, a faint bulb hum, a soft leaf falling.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, AI glow, holograms, glowing particles, "
    "bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person"
)

# --- G | REVOLT - VANISH BURST (3s) -------------------------------------
P["G"] = prompt(
    "<Subject 1> is " + CHAR + ", seated at a simple wooden table with dead plants on it.\n"
    "<Picture 1> is the FIRST frame: " + CHAR + " seated at the table, dead plants on the table surface.\n"
    "<Picture 2> is the LAST frame: the table with dead plants, DOZENS of loose sheets of paper floating in the air, a microphone among them, "
    "and NO person - Jaisal has VANISHED.",
    "[reference generation] A single continuous " + LOOK + " take that animates smoothly from "
    "<Picture 1> (Jaisal seated, dead plants) to <Picture 2> (the table with dead plants, dozens of loose sheets of paper floating, a microphone "
    "among them, and NO person - Jaisal has vanished). "
    "DOZENS of loose sheets of paper begin to float in from the darkness behind him, drifting forward. A microphone emerges from the dark and "
    "settles among the papers. Some papers drift back and vanish. JAISAL himself VANISHES - he is gone, replaced by the floating papers. "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Subject 1> (appears in the FIRST frame, then VANISHES): fully_preserved in the first frame, then ABSENT in the last frame. "
    + ONECHAR + " (in the first frame only).\n"
    "<Picture 1> (first frame): fully_preserved - the opening frame.\n"
    "<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame; Jaisal is NOT visible, only the papers and the microphone.",
    "The shot BEGINS from <Picture 1> (Jaisal seated, dead plants). DOZENS of loose sheets of paper begin to float in from the darkness behind "
    "him, drifting forward through the room. A microphone emerges from the dark and settles among the papers. Some papers drift back and vanish "
    "into the darkness. JAISAL himself VANISHES - he is gone, replaced by the floating papers. "
    "Camera: a MEDIUM WIDE shot (35mm), the camera is locked and does NOT move, push, drift, tilt, pan or zoom. "
    "The shot ENDS exactly on <Picture 2> (the table with dead plants, dozens of loose sheets of paper floating, a microphone among them, NO person).",
    "room tone, a soft paper rustle, a faint bulb hum, a gentle whoosh as the papers drift in.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, fire, smoke, glowing particles, futuristic AI effects, "
    "holograms, colorful effects, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a second person"
)

# --- H | MIC + PAPER (3s) ------------------------------------------------
P["H"] = prompt(
    "<Picture 1> is the FIRST frame: the table with dead plants, dozens of loose sheets of paper floating, a microphone among them, NO person.\n"
    "<Picture 2> is the LAST frame: the table with dead plants, the floating papers and the microphone now settled into a calm arrangement in the light, NO person.",
    "[reference generation] A single continuous " + LOOK + " take that animates smoothly from "
    "<Picture 1> (the table with dead plants, papers floating, a microphone among them, no person) to "
    "<Picture 2> (the table with dead plants, the papers and the microphone settled into a calm arrangement in the light, no person). "
    "The floating papers and the microphone settle into a calm arrangement in the light. A few papers drift. "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Picture 1> (first frame): fully_preserved - the opening frame.\n"
    "<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame; NO person is visible.",
    "The shot BEGINS from <Picture 1> (the table with dead plants, papers floating, a microphone among them, no person). The floating papers "
    "and the microphone settle into a calm arrangement in the light. A few papers drift. "
    "Camera: a MEDIUM shot (35mm), the camera is locked and does NOT move, push, drift, tilt, pan or zoom. "
    "The shot ENDS exactly on <Picture 2> (the table with dead plants, the papers and the microphone settled into a calm arrangement in the light, no person).",
    "room tone, a soft paper rustle, a faint bulb hum.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, fire, smoke, glowing particles, futuristic AI effects, "
    "holograms, colorful effects, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a person, a young man"
)

# --- I | MIC ALONE (2.3s) ------------------------------------------------
P["I"] = prompt(
    "<Picture 1> is the FIRST frame: the table with dead plants, the papers and the microphone settled in the light, NO person.\n"
    "<Picture 2> is the LAST frame: the table with dead plants, ONLY the microphone alone in the light, NO person, NO papers.",
    "[reference generation] A single continuous " + LOOK + " take that animates smoothly from "
    "<Picture 1> (the table with dead plants, the papers and the microphone settled in the light, no person) to "
    "<Picture 2> (the table with dead plants, ONLY the microphone alone in the light, no person, no papers). "
    "The papers drift away and vanish into the darkness, leaving only the microphone alone in the light. "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Picture 1> (first frame): fully_preserved - the opening frame.\n"
    "<Picture 2> (last frame): fully_preserved - the shot ENDS exactly on this frame; ONLY the microphone is visible, NO person, NO papers.",
    "The shot BEGINS from <Picture 1> (the table with dead plants, the papers and the microphone settled in the light, no person). The papers "
    "drift away and vanish into the darkness, leaving only the microphone alone in the light. "
    "Camera: a MEDIUM shot (35mm), the camera is locked and does NOT move, push, drift, tilt, pan or zoom. "
    "The shot ENDS exactly on <Picture 2> (the table with dead plants, ONLY the microphone alone in the light, no person, no papers).",
    "room tone, a faint bulb hum, a soft paper rustle as the papers drift away.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, fire, smoke, glowing particles, futuristic AI effects, "
    "holograms, colorful effects, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a person, a young man, papers"
)

# --- J | OBJECTS JOIN (3s) ----------------------------------------------
# NOTE: J has exactly 4 reference images (mic-alone start + 3 object refs).
# The END state (assembled objects) has NO keyframe, so it is described in
# words - never tag a <Picture N> that has no matching image.
P["J"] = prompt(
    "<Picture 1> is the FIRST frame: the table with dead plants, ONLY the microphone alone in the light, NO person, NO papers.\n"
    "<Picture 2> is a reference for the CRICKET BAT object (a vertical cricket bat on a pure black background).\n"
    "<Picture 3> is a reference for the SOCCER BALL object (a round soccer ball on a pure black background).\n"
    "<Picture 4> is a reference for the PAPER SMILEY object (a paper with a simple curved smile line on a pure black background).",
    "[reference generation] A single continuous " + LOOK + " take that animates from "
    "<Picture 1> (the table with dead plants, ONLY the microphone alone in the light, no person, no papers). "
    "A cricket bat matching <Picture 2> and cricket stumps fly into the light, and a round soccer ball matching <Picture 3> rolls in "
    "underneath them. One paper matching <Picture 4> (a simple curved smile line) settles on top of the bat as a crude head. "
    "The objects are fragments of Jaisal's ideas. The shot ENDS on the assembled objects in the light, NO person. "
    + SCENE + ". The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless.",
    "<Picture 1> (first frame): fully_preserved - the opening frame.\n"
    "<Picture 2> (cricket bat reference): fully_preserved - the cricket bat object.\n"
    "<Picture 3> (soccer ball reference): fully_preserved - the soccer ball object.\n"
    "<Picture 4> (paper smiley reference): fully_preserved - the paper smiley object.",
    "The shot BEGINS from <Picture 1> (the table with dead plants, ONLY the microphone alone in the light, no person, no papers). A cricket "
    "bat matching <Picture 2> and cricket stumps fly into the light, and a round soccer ball matching <Picture 3> rolls in underneath them. "
    "One paper matching <Picture 4> (a simple curved smile line) settles on top of the bat as a crude head. The objects are fragments of "
    "Jaisal's ideas. "
    "Camera: a MEDIUM WIDE shot (35mm), the camera is locked and does NOT move, push, drift, tilt, pan or zoom. "
    "The shot ENDS on the assembled objects in the light (microphone, cricket bat with the smiley paper on top, soccer ball underneath), NO person.",
    "room tone, a faint bulb hum, a soft paper rustle, a gentle thud as the objects settle.",
    "color, multiple people, second person, duplicate character, extra chairs, extra figures, fire, smoke, glowing particles, futuristic AI effects, "
    "holograms, colorful effects, bright wall, white wall, cream wall, visible ceiling, text, subtitles, watermark, logo, a person, a young man"
)

# --- Write all -----------------------------------------------------------
for key, text in P.items():
    path = os.path.join(OUT, "shot_%s.txt" % key)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print("wrote %s (%d chars)" % (path, len(text)))

print("\nAll 10 prompts written to %s" % OUT)
