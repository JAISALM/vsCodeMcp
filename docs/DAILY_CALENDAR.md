# Channel-1 daily calendar — 40 s explainers (D250 format), launch 2026-11-25 (in sha Allah)

**Format (D250):** 0–5 s TODAY'S SCENARIO (current-affairs hook from the RAG news
store) · 5–13 s THE WORD (hadith/verse + source card) · 13–32 s THE EXPLANATION ·
32–40 s THE WARNING ("word of God — verify from the original") + @handle.
**NO recitation audio** (copyright — the reciter's recording is a copyrighted
performance). Natural ambient SFX only (D041).

**Distribution (D241):** `*_part1.mp4` (0–20 s) + `*_part2.mp4` (20–40 s) →
WhatsApp status ×2 · full 40 s → Instagram.

**Palette = weekday (D244):** Mon=A_green · Tue=B_indigo · Wed=C_amber ·
Thu=D_slate · Fri=E_teal · Sat=F_clay · Sun=G_plum. `build_daily.py` applies the
weekday palette automatically (override: `--palette NAME`).

## Week 1 (7 days, 7 palettes)

| Date | Weekday | Palette | Content | Status |
|---|---|---|---|---|
| Wed 2026-11-25 | Wed | C_amber | **Day 1 — Ubu al-Amal** (Actions are by intentions · Sahih al-Bukhari 1) | **DONE** (`data\refanim\ubu_al_amal_40_sfx.mp4` + 2×20 s cuts) |
| Thu 2026-11-26 | Thu | D_slate | Day 2 — topic TBC (scenario→hadith pairing from the RAG store) | spec template ready (`data\daily\2026-11-26\spec.template.json`) |
| Fri 2026-11-27 | Fri | E_teal | Day 3 — topic TBC | — |
| Sat 2026-11-28 | Sat | F_clay | Day 4 — topic TBC | — |
| Sun 2026-11-29 | Sun | G_plum | Day 5 — topic TBC | — |
| Mon 2026-11-30 | Mon | A_green | Day 6 — topic TBC | — |
| Tue 2026-12-01 | Tue | B_indigo | Day 7 — topic TBC | — |

Week 2+ cycles the palette table (Wed→C again).

## Per-day build (one command)

```
python utilities\build_daily.py <YYYY-MM-DD> --spec data\daily\<YYYY-MM-DD>\spec.json
```

- spec JSON = Template B schema (see `spec.template.json` in the day folder);
  `slug` names the outputs, `sfx` is optional (natural-sound beats, D041).
- outputs → `data\daily\<date>\`: `<slug>.mp4` · `<slug>_sfx.mp4` (if sfx) ·
  `<slug>_part1.mp4` · `<slug>_part2.mp4` — all ffprobe-verified.
- fast check before a full render: `--preview 19.6` (single frame, ~seconds).
- Day 1 is reproducible: `python utilities\build_daily.py 2026-11-25 --spec data\daily\2026-11-25\spec.json`.

## Upload checklist (per day, author ~5 min)

1. WhatsApp status ×2: `part1` then `part2` (morning / evening)
2. Instagram: full 40 s
3. (FB + X copies once the 8-account set exists — pending author's Gmail + handle spelling)

**Open items:** handle spelling (`…Dialy` → `…Daily`?) · author's Gmail (8 accounts) ·
Arabic calligraphy font (text-only cards until it lands — no Arabic script rendered yet)
