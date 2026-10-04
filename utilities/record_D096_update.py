import io

# ---- DECISIONS.md: append D096 update ----
p = r'd:\models\vsCodeMcp\project-memory\DECISIONS.md'
s = io.open(p, encoding='utf-8').read()
add = '''
### D096 update — G_revolt extended to 15s + GRADUAL disappearance (2026-09-28)
- **User verdict on the 11s G_revolt run: "that was good"** — the sequential one-action-at-a-time structure WORKED (objects on their words, character at the table makes sense).
- **Changes (user's ask):** (1) length 11s → **15s (360f)**; (2) fix the SUDDEN removal of the character AND the plant — give both proper gradual detail; (3) second 14 = bulb flicker, second 15 = COMPLETE BLACK; (4) everything else stays the same.
- **New timing (15s):** 00:00–00:01 question → 00:01–00:02 "പറഞ്ഞപോലെ..." → 00:02–00:03 PAPERS ("കഥകൾ") → 00:03–00:04 MIC ("രാഷ്ട്രീയം") → 00:04–00:05 BAT+BALL ("കായികം") → 00:05–00:06 "പിന്നെ..." → 00:06–00:07 SMILEY PAPER ("fantasy") → 00:07–00:08 "ഇതൊക്കെയാണ് ഉദ്ദേശിക്കുന്നത്" → 00:08–00:09 "നടക്കുമോ എന്നറിയില്ല..." → **00:09–00:10 "നോക്കാം" — Jaisal BEGINS to come apart (outline softens, edges turn into paper sheets, form loses solidity — NOT a sudden pop)** → **00:10–00:11 disappearance COMPLETES (silhouette thins into final sheets, chair empty — SLOW, DETAILED, GRADUAL over 2s)** → 00:11–00:12 camera guy "നോക്കാം" → 00:12–00:13 still beat → **00:13–00:14 bulb FLICKERS once** → **00:14–00:15 COMPLETE BLACK, CUT TO BLACK**.
- **PLANT BEHAVIOR section added:** dead plants SLOWLY CRUMBLE and WITHER throughout the shot (leaves curl to dust, stems bend and sink) — gradual, detailed, NOT a single-frame vanish; they crumble away as the new objects appear.
- **CHARACTER DISAPPEARANCE section added:** dedicated 2-beat gradual unraveling (00:09–00:11) with explicit "NOT a sudden pop / NOT a single-frame cut / NOT a teleport" wording.
- **Negatives added:** `Jaisal vanishing in a single frame, Jaisal popping out suddenly, the plants vanishing in a single frame, the plants popping out suddenly, the plants disappearing before the character`.
- **Prompt:** `Jaisal-intro/prompts/shot_G_revolt_15s.txt` (14353 chars). Workflow `jaisal_intro_G_revolt.json` updated in place (length 264→360, prompt swapped). Validates clean (0 errors, 29 nodes).
- **KEY LESSON:** when a disappearance looks "sudden", give it a DEDICATED 2-second gradual process with per-second detail (outline softens → edges turn to paper → silhouette thins → chair empty) + negatives for single-frame vanish/pop-out/teleport. Same for plants: crumble/wither over the whole shot, not a single-frame vanish.
'''
if 'D096 update' not in s:
    s = s.rstrip() + '\n' + add
    io.open(p, 'w', encoding='utf-8').write(s)
    print('DECISIONS D096 update added')
else:
    print('already present')

# ---- CURRENT_TASK.md ----
p2 = r'd:\models\vsCodeMcp\project-memory\CURRENT_TASK.md'
s2 = io.open(p2, encoding='utf-8').read()
s2 = s2.replace(
    'Last Updated: 2026-09-28 (G = single 11s SEQUENTIAL take G_revolt, built + validated; G1/G2 split superseded)',
    'Last Updated: 2026-09-28 (G_revolt 11s run GOOD → extended to 15s + gradual character/plant disappearance, built + validated)'
)
entry = '''- **2026-09-28 (LATEST) — G_revolt 11s RUN GOOD → EXTENDED TO 15s + GRADUAL DISAPPEARANCE (D096 update) — BUILT + VALIDATED, AWAITING USER RUN:** user: "that was good. we can increase the timing to 15 second maybe, it was 10. the issues are the sudden removal of the character and the plant, so lets give them proper details. and the 15 second should be complete black, second 14 light flickering. rest we can keep same, only the sudden disappearing where we need to work. i think we are about to reach there." **DONE (in-place update of `jaisal_intro_G_revolt.json`):** (1) length 264→**360 (15s)**; (2) **CHARACTER DISAPPEARANCE = 2-beat GRADUAL unraveling** — 00:09–00:10 "നോക്കാം": body BEGINS to come apart (outline softens, edges turn into paper sheets, form loses solidity — NOT a sudden pop); 00:10–00:11 COMPLETES (silhouette thins into final sheets, chair empty — SLOW, DETAILED, GRADUAL over 2s); (3) **PLANT BEHAVIOR section** — dead plants SLOWLY CRUMBLE and WITHER throughout the shot (leaves curl to dust, stems bend and sink), NOT a single-frame vanish; (4) **new tail:** 00:11–00:12 camera guy "നോക്കാം" → 00:12–00:13 still beat → **00:13–00:14 bulb FLICKERS once** → **00:14–00:15 COMPLETE BLACK, CUT TO BLACK**; (5) negatives += `Jaisal vanishing in a single frame, Jaisal popping out suddenly, the plants vanishing in a single frame, the plants popping out suddenly, the plants disappearing before the character`. **Prompt: `Jaisal-intro/prompts/shot_G_revolt_15s.txt` (14353 chars). Validates clean (0 errors, 29 nodes).** **NEXT (user, stop Qwen first, fresh tab):** (1) `Stop-Process -Name "llama-server" -Force`; (2) stage F2's last frame if not already (G's ref_image_0 = `kf7a_v4.png`); (3) run **G_revolt** (fresh tab) → judge: objects still one-at-a-time on their words? **character disappearance GRADUAL (2s unravel, not a pop)?** **plants crumble gradually (not a single-frame vanish)?** bulb flicker at ~14s? complete black at 15s? → `clip_00008`; (4) `Start-Process "D:\\models\\qwen\\Qwen3.827BMTP.bat"`. **THEN FINAL ASSEMBLY:** concatenate A→B→C→D→E→F1→F2→G (Trim removes 22 pinned head frames) → single 2K upscale (4x-UltraSharp non-generative) → post audio (ambient + dubs, **NO MUSIC D041**). **RULES:** NO MUSIC (D041); user runs GPU jobs (I never stop Qwen); artifacts in `Jaisal-intro\\`; fresh tabs; check `Get-Process llama-server` before any run.

'''
marker = '## RESUME POINT (read this first)\n'
if marker in s2:
    s2 = s2.replace(
        '- **2026-09-28 (LATEST) — G = SINGLE 11s SEQUENTIAL take `jaisal_intro_G_revolt.json` (D096) — BUILT + VALIDATED, AWAITING USER RUN:**',
        '- **2026-09-28 — G = SINGLE 11s SEQUENTIAL take `jaisal_intro_G_revolt.json` (D096) — 11s RUN GOOD, EXTENDED TO 15s (D096 update):**'
    )
    s2 = s2.replace(marker, marker + '\n' + entry)
    io.open(p2, 'w', encoding='utf-8').write(s2)
    print('CURRENT_TASK updated')
else:
    print('marker not found')
