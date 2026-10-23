# CHARACTERS — Jaisal & Zidhan (2026-10-23, D171)

Single source of truth for the two movie characters: final face references,
descriptions, and ready-to-use prompts. Prompts below were **picked from the
workflows that generated the final face sheets** (not invented):

- Jaisal face sheet ← `10a_frontal_base_jaisal.json` (node 300/313/318 = positive, node 301 = negative)
- Zidhan face sheet ← `10a_frontal_base_zidane.json` (node 300 = positive, node 301 = negative)

All outputs in: `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\`

---

## FINAL REFERENCES (locked, 2026-10-23)

| Character | Trigger | Final reference (THE face) | Generator workflow |
|---|---|---|---|
| **Jaisal** (char1) | `jeskv` / `jeskvman` | `FACEFRONTAL_JAISAL_b_00001_.png` | `10a_frontal_base_jaisal.json` |
| **Zidhan** (char2) | `dlor` / `dlorman` | `FACEFRONTAL2_ZIDANE_c_00012_.png` | `10a_frontal_base_zidane.json` |

Character LoRA (both): `krea2fp_v2_ep64.safetensors` @ 1.0 (Krea2 family, rank 32,
2-subject isolation). Reality finish: `Krea2-realism-V2.safetensors` @ 1.0.
Old top-bun char2 canonical (`krea2_char2_face_*`, D137) is **DEPRECATED** —
never prompt "top bun / topknot" for Zidhan.

---

## JAISAL — description (verified against `FACEFRONTAL_JAISAL_b_00001_`)

26-year-old young Malayali man from Kerala, South Indian facial features, warm
medium-brown natural skin, ROUND youthful face with softer rounded features and a
masculine jaw, **MEDIUM-LENGTH WAVY dark hair worn DOWN and loose** around his
neck and ears (natural, slightly messy — NOT tied up, NOT a bun, NOT a topknot,
NOT a short haircut), **a sparse short BEARD on his chin and jaw** (sparse uneven
dark patches, more than stubble, NOT clean-shaven, NOT a dense full beard), lean
and fit, NOT bulky, wearing a **plain dark t-shirt**. His face is clearly
different from a man-bun man.

### Jaisal face-frontal prompt (verbatim from `10a_frontal_base_jaisal.json` node 300)

```
A candid phone snapshot of a 26-year-old young Malayali man from Kerala, India, South Indian facial features, warm medium-brown natural skin, a young MAN (male only), with a ROUND youthful face, softer rounded features and a masculine jaw, MEDIUM-LENGTH WAVY dark hair worn DOWN and loose around his neck and ears (wavy, natural, slightly messy, hair is NOT tied up, NOT in a bun, NOT a topknot, NOT a short haircut), a sparse short BEARD on his chin and jaw (sparse uneven dark patches you can see on his face, more than stubble, NOT clean-shaven, NOT a dense full beard), a lean and fit young man, NOT bulky, NOT muscular, wearing a plain dark t-shirt, his face completely frontal. He is standing alone, facing the camera directly, dead-center, head and shoulders framing, both eyes fully open and symmetric, looking straight into the lens, calm neutral relaxed expression, face completely frontal, NO side angle, NO profile, NO three-quarter view. His wavy hair is down and loose, the sparse beard visible on his chin and jaw. Sharp focus on the man's face, his face is the main subject, in focus, crisp facial detail, detailed iris and eye texture. He looks like a real young man in his mid-20s: youthful fresh face, natural young skin, no wrinkles, no aging, no grey hair. Candid unposed snapshot caught in a real moment, natural ambient light, looks like a real photo someone took on their phone, slight natural imperfections, a real ordinary person, ONLY ONE character, no other people, NOT a studio portrait, NOT a headshot, NOT a stock photo, NOT a professional photo.
```

### Jaisal negative (verbatim from node 301)

```
studio portrait, studio lighting, posed portrait, headshot, professional photoshoot, fashion photography, model, celebrity, stock photo, beauty campaign, perfect skin, airbrushed skin, plastic skin, waxy skin, artificial skin, generic AI face, western facial features, northern Indian appearance, older man, mature man, 30s, 40s, 50s, aged face, wrinkles, grey hair, bald, short haircut, bulky body, muscular body, bodybuilder, clean-shaven, no beard, missing beard, full long beard, perfectly groomed beard, duplicate character, multiple people, crowd, woman, women, girl, female, second person, extra person, person in background, text, words, letters, subtitles, captions, dialogue, speech bubble, readable sign, logo, watermark, label, social media overlay, screenshot, UI, deformed face, bad eyes, crossed eyes, extra fingers, malformed hands, distorted anatomy, oversaturated skin, over-processed image, excessive bokeh, artificial cinematic poster, professional camera look, fake environment, saree, sari, traditional dress, nose ring, feminine features, anime, cartoon, illustration, painting, drawing, sketch, stylized, 3d render, cgi, mixed art styles
```

---

## ZIDHAN — description (verified against `FACEFRONTAL2_ZIDANE_c_00012_`)

Young South Indian man, face **round and full-cheeked** — wide, soft, with a
short strong jaw — warm medium-brown skin with natural pores and a healthy
flush. Hair: **short black halal haircut — very short faded sides and back, a
short neat crop on top, no waves, no bun**. **A full short dark beard, neatly
trimmed and shaped, dense on the chin, jawline and upper lip.** Lean and slim,
wearing a **plain white t-shirt**.

### Zidhan face-frontal prompt (verbatim from `10a_frontal_base_zidane.json` node 300)

```
kr2realism. Close-up photo of a young South Indian man facing the camera dead-on, his face filling most of the frame. His face is round and full-cheeked — wide, soft, with a short strong jaw — warm medium-brown skin with natural pores and a healthy flush. His hair is a short black halal haircut: very short faded sides and back, a short neat crop on top, no waves, no bun. A full short dark beard, neatly trimmed and shaped, dense on the chin, jawline and upper lip. He is lean and slim, wearing a plain white t-shirt. He looks straight into the camera with a relaxed half-smile. Natural even daylight, a plain off-white wall behind him, sharp focus on the face, looks like a real unposed phone photo, one person only, no other people.
```

(`kr2realism.` = style trigger of that face-sheet chain — drop it when composing
new prompts on the standard Krea2 t2i chain.)

### Zidhan negative (verbatim from node 301)

```
duplicate character, multiple people, watermark, logo, deformed face, bad eyes, extra fingers, profile view, three-quarter view, head turned to the side, head tilted, looking away from camera, long hair, wavy hair, man-bun, topknot, ponytail, clean-shaven, no beard, missing beard
```

---

## READY-TO-USE PROMPTS (trigger + description built in)

### 1. Jaisal solo — scene template

```
jeskvman, a candid phone snapshot of a 26-year-old young Malayali man from Kerala, South Indian facial features, warm medium-brown natural skin, a young MAN (male only), with a ROUND youthful face, softer rounded features and a masculine jaw, MEDIUM-LENGTH WAVY dark hair worn DOWN and loose around his neck and ears (NOT tied up, NOT in a bun, NOT a topknot, NOT a short haircut), a sparse short BEARD on his chin and jaw (sparse uneven dark patches, more than stubble, NOT clean-shaven, NOT a dense full beard), a lean and fit young man, NOT bulky, NOT muscular, wearing a plain dark t-shirt, his face clearly different from a man-bun man. [SCENE — pose, action, place, shot size, lighting]. He looks like a real young man in his mid-20s: youthful fresh face, natural young skin, no wrinkles, no aging, no grey hair. Candid unposed snapshot caught in a real moment, natural ambient light, looks like a real photo someone took on his phone, slight natural imperfections, a real ordinary person, ONLY ONE character, no other people, NOT a studio portrait, NOT a headshot, NOT a stock photo, NOT a professional photo.
```

### 2. Zidhan solo — scene template

```
dlorman, a candid phone snapshot of a young South Indian man, warm medium-brown natural skin, face round and full-cheeked — wide, soft, with a short strong jaw — his hair a short black halal haircut: very short faded sides and back, a short neat crop on top, no waves, no bun, a full short dark beard, neatly trimmed and shaped, dense on the chin, jawline and upper lip, lean and slim, wearing a plain white t-shirt, his face clearly different from a wavy-hair man. [SCENE — pose, action, place, shot size, lighting]. He looks like a real young man in his mid-20s: youthful fresh face, natural young skin, no wrinkles, no aging, no grey hair. Candid unposed snapshot caught in a real moment, natural ambient light, looks like a real photo someone took on his phone, slight natural imperfections, a real ordinary person, ONLY ONE character, no other people, NOT a studio portrait, NOT a headshot, NOT a stock photo, NOT a professional photo.
```

### 3. FAIR TEST — both men in ONE picture (combined)

```
jeskvman and dlorman standing side by side on a narrow rainy village street in Kerala, light rain falling, wet pavement, palms and houses in the background, medium shot from the waist up, both faces clearly visible, both in focus, natural ambient light, a real candid phone snapshot. The first man (jeskvman): 26-year-old young Malayali, warm medium-brown natural skin, ROUND youthful face, MEDIUM-LENGTH WAVY dark hair worn DOWN and loose around his neck and ears, a sparse short BEARD on his chin and jaw, lean and fit, wearing a plain dark t-shirt. The second man (dlorman): young South Indian man, face round and full-cheeked with a short strong jaw, hair a short black halal haircut — very short faded sides and back, a short neat crop on top, no waves, no bun — a full short dark beard, neatly trimmed and shaped, dense on the chin, jawline and upper lip, lean and slim, wearing a plain white t-shirt. ONLY these two men, no other people, candid unposed snapshot, slight natural imperfections, NOT a studio portrait, NOT a stock photo.
```

---

## Rules

- Triggers go FIRST (`jeskvman` / `dlorman`), description second. The user's
  detailed descriptions already carry identity on their own — the trigger adds
  the LoRA binding on top.
- NEVER "top bun / topknot" for Zidhan (D171). NEVER "bun / topknot" for Jaisal
  (his hair is DOWN).
- Prompts edited in the ComfyUI UI must be SAVED (Ctrl+S) so the on-disk file
  = what actually runs (10/23 lesson).
- Dataset folders: `D:\lora_training\jaisal` (`jeskv,` captions) and
  `D:\lora_training\zidane` (`dlor,` captions) — both faces match the finals
  above (verified 10/23).
