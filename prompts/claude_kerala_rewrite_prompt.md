# Paste this prompt to Claude (attach v91_kerala_identity_brief_v2.md)

You are rewriting a character-prompt set for a Krea2 identity-edit workflow.

READ THE ATTACHED FILE FIRST — it is the full spec: `v91_kerala_identity_brief_v2.md`.
If you also have `v91_dataset_prompts_jaisal_zidhan.md` (your previous output), use it ONLY as a structural reference for the 8 list roles/shot types — do NOT reuse its European scenes or its character description. The v2 brief supersedes it completely.

TASK: Write 16 prompt blocks — all 8 lists for JAISAL, then all 8 lists for ZIDHAN.
Line counts per list, in order: 20, 20, 25, 25, 25, 20, 25, 7 (identical counts for both characters).

HARD RULES (from the v2 brief — non-negotiable):
1. Every line STARTS with the character's absolute identity block, verbatim:
   - Jaisal: "Kerala (South Indian) man, about 26 years old, warm dark brown skin with natural texture, medium wavy black hair falling to eyebrow length, slightly crooked naturally bent nose, dark brown almond eyes, thin lips, clean-shaven with faint stubble, lean slim build."
   - Zidhan: "Kerala (South Indian) man, about 26 years old, warm dark brown skin with natural texture, short neat black hair, full short dense black beard, dark brown eyes, lean slim build."
2. NEVER write blonde, fair, white, light, pale or European-looking skin anywhere. Skin words, when used, are only "warm dark brown skin" / "dark brown skin".
3. NEVER rely on "skin same as the reference image" — the identity block IS the anchor.
4. Clothing: Jaisal's base = plain black t-shirt; Zidhan's base = plain white t-shirt. For scene lines use natural Kerala/South Indian clothing: kurta, open-collar shirt, jeans, simple trousers, rolled sleeves. Kerala-style wear is welcome wherever natural. NO Western model-glamour (no silk scarves, no cashmere, no jewelry stacks, no seductive framing).
5. Scenes: Kerala-rooted only — paddy fields, backwaters and houseboats, coconut groves, laterite stone paths, monsoon village streets, Kochi old city, Marine Drive, home verandas, temple-town courtyards, fishing boats on the lagoon. Lighting: golden hour over water, soft monsoon overcast, rim light through rain, warm tungsten veranda light, dappled shade under coconut palms.
6. Keep the photographic craft from the previous version: 85mm f/1.8, shallow DOF, dutch angle, pov, creamy bokeh, high-detail natural skin texture with visible pores, film grain, editorial quality.
7. Every line ENDS with exactly: "ignore original clothing completely, photorealistic, high-detail natural skin texture with pores, soft natural lighting, sharp focus, ONLY ONE character, no other people, no duplicates."
8. Mood: grounded, natural, documentary South Indian look — everyday real moments (calm, thoughtful, faint smile, looking at the water, waiting in rain). NOT glossy Western male-model glamour.

OUTPUT FORMAT: one markdown file with 16 fenced code blocks in this EXACT order, each labelled:
LIST 1 — node 257 (Jaisal) — 20 lines
LIST 2 — node 258 (Jaisal) — 20 lines
LIST 3 — node 259 (Jaisal) — 25 lines
LIST 4 — node 2770 (Jaisal) — 25 lines
LIST 5 — node 2842 (Jaisal) — 25 lines
LIST 6 — node 2843 (Jaisal) — 20 lines
LIST 7 — node 260 (Jaisal) — 25 lines
LIST 8 — node 2772 (Jaisal) — 7 lines
LIST 1 — node 257 (Zidhan) — 20 lines
LIST 2 — node 258 (Zidhan) — 20 lines
LIST 3 — node 259 (Zidhan) — 25 lines
LIST 4 — node 2770 (Zidhan) — 25 lines
LIST 5 — node 2842 (Zidhan) — 25 lines
LIST 6 — node 2843 (Zidhan) — 20 lines
LIST 7 — node 260 (Zidhan) — 25 lines
LIST 8 — node 2772 (Zidhan) — 7 lines
One prompt per line, no blank lines inside a block.
