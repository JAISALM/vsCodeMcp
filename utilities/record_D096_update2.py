import io

# ---- DECISIONS.md ----
p = r'd:\models\vsCodeMcp\project-memory\DECISIONS.md'
s = io.open(p, encoding='utf-8').read()
add = '''
### D096 update 2 — G_revolt v2: camera-guy voice timing + LOW mic (2026-09-28)
- **User verdict on the 15s G run: "we're almost there"** — two corrections: (1) the FIRST dialogue (the question) should come from the CAMERA MAN (off-screen), not be mouthed by Jaisal; (2) the mic should settle a LITTLE LOWER so Jaisal's face stays visible.
- **Fix 1 — camera-guy voice (the PROVEN F1 timing-mimic workaround, UPDATE 4):** (a) question gets a FULL 3s off-screen beat (00:00–00:03) with Jaisal's mouth COMPLETELY CLOSED (he only listens); (b) Jaisal's first line starts IMMEDIATELY after the question (00:03, "പറഞ്ഞപോലെ... കഥകൾ...") — NO long silent gap (a long silent beat + heavy lip-lock makes H3 mouth the question); (c) dedicated SPEAKER ATTRIBUTION (CRITICAL) block: two distinct speakers, <Subject 2> is AUDIO ONLY, Jaisal's mouth moves ONLY for his own lines; (d) negatives: `Jaisal speaking the question, the visible character speaking the off-screen line, lip-sync to the off-screen voice, Jaisal's lips opening before 00:03, a long silent gap between the question and Jaisal's first line`.
- **Fix 2 — LOW mic:** the microphone settles LOW on the table — its top stays BELOW Jaisal's face level so his face remains fully visible and unobstructed (stated in the 00:05–00:06 beat, the CHARACTER CONSISTENCY section, and negatives `the microphone blocking Jaisal's face, the microphone rising above Jaisal's face level`).
- **Timing shift:** everything after the question shifts +2s (question 00:00–00:03 → papers 00:03–00:05 → mic 00:05–00:06 → bat+ball 00:06–00:07 → "പിന്നെ" 00:07–00:08 → fantasy 00:08–00:09 → "ഇതൊക്കെ..." 00:09–00:10 → "നടക്കുമോ..." 00:10–00:11 → "നോക്കാം" + disappearance begins 00:11–00:12 → completes 00:12–00:13 → camera guy "നോക്കാം" 00:13–00:14 → bulb flicker + COMPLETE BLACK 00:14–00:15).
- **Prompt:** `Jaisal-intro/prompts/shot_G_revolt_15s_v2.txt` (15290 chars), synced into `jaisal_intro_G_revolt.json` node 138. Validates clean (0 errors, 29 nodes).
- **RULE:** for an off-screen question + character response, use the F1 timing-mimic (3s question beat, mouth closed, first line IMMEDIATELY after, no long silent gap) — this is the proven workaround. Keep objects LOW so they don't block the character's face.
'''
if 'D096 update 2' not in s:
    s = s.rstrip() + '\n' + add
    io.open(p, 'w', encoding='utf-8').write(s)
    print('DECISIONS D096 update 2 added')
else:
    print('already present')

# ---- CURRENT_TASK.md ----
p2 = r'd:\models\vsCodeMcp\project-memory\CURRENT_TASK.md'
s2 = io.open(p2, encoding='utf-8').read()
s2 = s2.replace(
    'Last Updated: 2026-09-28 (G_revolt 11s run GOOD → extended to 15s + gradual character/plant disappearance, built + validated)',
    'Last Updated: 2026-09-28 (G_revolt 15s v2: camera-guy voice timing-mimic + LOW mic, built + validated)'
)
entry = '''- **2026-09-28 (LATEST) — G_revolt 15s v2: CAMERA-GUY VOICE (timing-mimic) + LOW MIC (D096 update 2) — BUILT + VALIDATED, AWAITING USER RUN:** user: "we're almost there. the first dialogue should come from the camera man, and the mic should be a little lower so we can see the character's face. that's the only correction. we already have a proven workaround for camera man voice right?" **DONE (in-place update of `jaisal_intro_G_revolt.json`, prompt `Jaisal-intro/prompts/shot_G_revolt_15s_v2.txt` 15290 chars):** (1) **CAMERA-GUY VOICE = the PROVEN F1 timing-mimic workaround** — question gets a FULL 3s off-screen beat (00:00–00:03, Jaisal's mouth COMPLETELY CLOSED, he only listens) + Jaisal's first line starts IMMEDIATELY after (00:03, "പറഞ്ഞപോലെ... കഥകൾ...", NO long silent gap) + dedicated SPEAKER ATTRIBUTION (CRITICAL) block (<Subject 2> = AUDIO ONLY, Jaisal's mouth moves ONLY for his own lines) + negatives `Jaisal speaking the question, lip-sync to the off-screen voice, Jaisal's lips opening before 00:03, a long silent gap between the question and Jaisal's first line`; (2) **LOW MIC** — the microphone settles LOW on the table, its top BELOW Jaisal's face level so his face stays fully visible (00:05–00:06 beat + CHARACTER CONSISTENCY + negatives `the microphone blocking Jaisal's face, the microphone rising above Jaisal's face level`); (3) **timing shift:** everything after the question shifts +2s (papers 00:03–00:05 → mic 00:05–00:06 → bat+ball 00:06–00:07 → fantasy 00:08–00:09 → "നോക്കാം" + disappearance 00:11–00:13 → camera guy "നോക്കാം" 00:13–00:14 → bulb flicker + COMPLETE BLACK 00:14–00:15). **Validates clean (0 errors, 29 nodes).** **NEXT (user, stop Qwen first, fresh tab):** (1) `Stop-Process -Name "llama-server" -Force`; (2) stage F2's last frame if not already (G's ref_image_0 = `kf7a_v4.png`); (3) run **G_revolt** (fresh tab) → judge: **question from OFF-SCREEN (Jaisal's mouth closed during it)?** Jaisal's first line immediately after? **mic LOW (face visible)?** objects one-at-a-time? gradual disappearance? bulb flicker + black? → `clip_00008`; (4) `Start-Process "D:\\models\\qwen\\Qwen3.827BMTP.bat"`. **THEN FINAL ASSEMBLY:** concatenate A→B→C→D→E→F1→F2→G (Trim removes 22 pinned head frames) → single 2K upscale (4x-UltraSharp non-generative) → post audio (ambient + dubs, **NO MUSIC D041**). **RULES:** NO MUSIC (D041); user runs GPU jobs (I never stop Qwen); artifacts in `Jaisal-intro\\`; fresh tabs; check `Get-Process llama-server` before any run.

'''
marker = '## RESUME POINT (read this first)\n'
if marker in s2:
    s2 = s2.replace(
        '- **2026-09-28 (LATEST) — G_revolt 11s RUN GOOD → EXTENDED TO 15s + GRADUAL DISAPPEARANCE (D096 update) — BUILT + VALIDATED, AWAITING USER RUN:**',
        '- **2026-09-28 — G_revolt 11s RUN GOOD → EXTENDED TO 15s + GRADUAL DISAPPEARANCE (D096 update) — 15s RUN "ALMOST THERE", v2 = camera-guy voice + LOW MIC (D096 update 2):**'
    )
    s2 = s2.replace(marker, marker + '\n' + entry)
    io.open(p2, 'w', encoding='utf-8').write(s2)
    print('CURRENT_TASK updated')
else:
    print('marker not found')
