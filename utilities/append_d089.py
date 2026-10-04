import io
p = r"d:\models\vsCodeMcp\project-memory\DECISIONS.md"
t = open(p, encoding="utf-8").read()
if "D089" in t:
    print("D089 already present, skipping")
else:
    add = """

## D089 — Shot D = CONTINUATION from C's last frame (reverse dropped) (2026-09-15)

**Decision:** the script's Shot 4 "PERFECT REVERSE" (everything reverses, 180 head
twist undone) is DROPPED — shot C no longer has the twist (D086/D087 made it a
static medium shot), so there is nothing to reverse. **Shot D is now a
CONTINUATION:** Jaisal stays seated in exactly C's last frame; the camera guy
(off-screen) asks "What's the purpose of this channel?"; Jaisal gives a subtle
LISTENING reaction (eyes shift, thoughtful expression, brief pause, tiny head
tilt). **The camera guy's line is DUBBED IN POST** (Midhun voice, D055) — the
video itself = Jaisal listening + ambient, NO in-video dialogue, NO music (D041).

**Config (`jaisal_intro_D_reverse.json`, via `utilities/setup_shot_D_continuation.py`,
validates clean 0 errors):** ref_image_0 = ref_image_1 = `shot_C_lastframe.png`
(C's last frame as BOTH start and end anchor — locks the pose, seamless cut).
Prompt = listening shot (node 138). Length 175 frames (~7.3s, script 0:18-0:25).
1344x768, 1 MP.

**Reason:** a single shared anchor (C's exact last frame) makes the cut seamless
and keeps the pose locked; a listening beat is the natural bridge to shot E
(plants grow). The off-screen question is audio-only (post dub) so MiniMax is
not asked to render a second person or in-video dialogue.

**Status:** ACTIVE. **RULE: shot D = continuation + listening reaction; camera
guy's line dubbed in post.**
"""
    open(p, "w", encoding="utf-8").write(t + add)
    print("appended D089")
