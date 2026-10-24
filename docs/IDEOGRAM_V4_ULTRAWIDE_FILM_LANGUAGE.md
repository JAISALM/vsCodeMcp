# Ideogram v4 Ultrawide Cinematic — Film Language (P9 item 7, reddit 1ucdyvr)

**Source:** reddit 1ucdyvr (u/LongjumpingGur7623, "Ultrawide cinematic shots Ideogram v4 — No Lora, No JSON prompts!") → Civitai [2674413](https://civitai.com/models/2674413) (v3.0 workflow, 2026-10-24). Workflow reference copy: `E:\minimax_workflow\ideogramV4Workflow_v30.json` (NOT copied to runnable workflows — see rule below).

**USER RULE (2026-10-24, verbatim): KEEP prompts/film language ONLY — do NOT apply their settings — adapt for Krea2.** The workflow's sampler/resolution/upscale settings are NOT applied to any of our workflows. The Ideogram-4 model set (Comfy-Org `Ideogram-4`: ideogram4_fp8_scaled + qwen3vl_8b + gemma4_e4b + flux2-vae) is NOT downloaded. The HF prompt dataset (`a3xrfgb/ideogram-v4-Json-prompts`) is **DELETED** (404) — the examples below are what survived (workflow widgets + Civitai description).

## 1. The structured JSON prompt schema (their prompting technique)

```json
{
  "high_level_description": "",
  "style_description": {
    "aesthetics": "",
    "lighting": "",
    "photo": "",
    "medium": "",
    "color_palette": []   // hex values
  },
  "compositional_deconstruction": {
    "background": "",
    "elements": [
      { "type": "obj",  "bbox": [y_min, x_min, y_max, x_max], "desc": "", "color_palette": [] },
      { "type": "text", "text": "the text to render", "bbox": [y_min, x_min, y_max, x_max],
        "desc": "", "color_palette": [] }
    ]
  }
}
```

- `bbox` = **spatial control** on a 0–1000 normalized grid (y first, x second). This is Ideogram v4's killer feature — the model places each described element at its box.
- `type: "text"` = in-image TEXT rendering (title cards, signage) with its own box + palette.
- The KJNodes `Ideogram4PromptBuilderKJ` node assembles these sections; the workflow also carries a long **negative prompt** (below).

## 2. Complete example prompt (Civitai description — seashell editorial portrait)

```json
{
  "high_level_description": "A striking, editorial portrait features a woman whose eyes are obscured by a carefully arranged, overlapping composition of large, pale, fan-like seashells, set against a bright, diffused outdoor backdrop.",
  "style_description": {
    "aesthetics": "editorial portraiture, surreal",
    "lighting": "soft, natural daylight, diffused, creating gentle highlights on the shells and skin",
    "photo": "medium close-up portrait, high resolution",
    "medium": "digital photograph",
    "color_palette": ["#A08D6B", "#D4C19A", "#2C3E50", "#E0E0E0"]
  },
  "compositional_deconstruction": {
    "background": "The background is an outdoor, slightly blurred scene suggesting a bright day near water, featuring soft tones of pale blue and muted grey-green.",
    "elements": [
      { "type": "obj", "bbox": [0, 0, 400, 1000],
        "desc": "The distant background, showing a soft horizon line where muted blue sky meets a lighter, indistinct body of water or atmosphere, creating a shallow depth of field effect.",
        "color_palette": ["#A9B8C2", "#DDEEFF", "#B0C4DE"] },
      { "type": "obj", "bbox": [270, 0, 820, 1000],
        "desc": "The woman's visible skin, covering her neck, shoulders, and mouth area. Her skin tone is deep and rich, with subtle highlights catching the light on her collarbone and cheekbones.",
        "color_palette": ["#3D271D", "#5A382C", "#7A5A4E"] },
      { "type": "obj", "bbox": [100, 50, 670, 480],
        "desc": "A large, fan-shaped seashell positioned over the woman's left eye area. The shell is pale cream/beige, showing intricate, radiating ridges and a natural, organic texture. It is positioned slightly angled towards the viewer.",
        "color_palette": ["#D4C19A", "#A08D6B", "#E0E0E0"] },
      { "type": "obj", "bbox": [150, 350, 670, 920],
        "desc": "A second, overlapping fan-shaped seashell positioned over the woman's right eye area. This shell is slightly larger and more centrally placed than the first, exhibiting similar pale, creamy tones and detailed radial ribbing.",
        "color_palette": ["#D4C19A", "#A08D6B", "#B0A080"] }
    ]
  }
}
```

## 3. Film language embedded in the v3.0 workflow (extracted verbatim)

**Subject (PromptBuilder section 1):**
> A central female figure in a rich, textured gown stands amidst an immersive, reflective environment filled with numerous rectangular panels displaying ghostly, shadowy portraits, suggesting a grand, memory-laden hall

**Background (section 2):**
> The background is composed of repeating, vertical, rectangular panels that appear to be highly reflective glass or polished material, each containing a faded, shadowy portrait of a person, creating a sense of endless depth and memory.

**Camera (section 3):**
> wide-angle shot with a shallow depth of field effect on the background elements, drawing focus to the central subject.

**Lighting (section 4):**
> low-key, warm, and highly reflective, with numerous scattered bokeh-like lights creating a magical, deep atmosphere.

**Long-form natural-language example (`easy promptList` widget):**
> A man is depicted in a medium, profile shot, positioned in the left and center of the frame, looking down and toward the right. He appears to be a man in his 20s or 30s, with a medium skin tone. His hair is dark, cut relatively short, and appears textured. His facial expression is focused, and his gaze is directed downward toward the object in front of him. He is wearing a garment that appears to be a t-shirt or casual top, visible on his left shoulder and upper chest, which is a light gray color with a visible, subtle mottled or textured pattern. On his visible right hand, he is holding a thin implement, possibly a brush or stylus, which is positioned over a large, illuminated surface. …

**Negative prompt (reference — 2176 chars, image + temporal + anatomy):**
> blurry, low quality, jpeg artifacts, compression artifacts, watermark, signature, worst quality, bad quality, low resolution, pixelated, noisy, grainy, oversharpened, overexposed, underexposed, flat lighting, washed out, dull colors, bright colors, oversaturated, color banding, soft focus, out of focus, flicker, frame flicker, temporal flicker, stutter, choppy motion, jitter, shaky camera, camera wobble, rolling shutter, ghosting, motion blur, smeared motion, warped motion, duplicated frames, dropped frames, frozen frame, jump cuts, inconsistent motion, unnatural motion, bad interpolation, lagging movement, rubbery movement, teleporting, popping, clipping, intersecting objects, floating objects, melting, morphing errors, deformed, distorted, disfigured, malformed, mutated, bad anatomy, extra limbs, extra fingers, fused fingers, missing fingers, bad hands, wrong anatomy, twisted limbs …

**Audio line (LTXV video-extension branch — D041-safe speech-only example):**
> the camera dolly out and the man speaks to the camera with gesture with american accent "I hope you guys enjoyed this pixel painting session."

## 4. Ultrawide resolution ladder (reference only — NOT applied)

1280-class: 1280×1280 (1:1) · 1440×1120 (9:7) · 1472×1104 (4:3) · 1536×1024 (3:2) · **1536×864 (16:9)** · **1680×720 (21:9)** · 864×1536 (9:16) · 720×1680 (9:21)
1536-class: 2048×1152 (16:9) · **2016×864 (21:9)** · 1152×2048 (9:16)
Ultrawide ladders: **UWHD 2560×1080 · UWQHD 3440×1440 · UWQHD+ 3840×1600 · UW4K 5120×2160**

## 5. Krea2 ADAPTATION (our pipeline — prompts only, no settings)

Krea2 (our one-click Krea2 batch) is a t2i model — **no bbox feature, no hex palette input, no video branch**. Convert the structured JSON into **natural-language blocks**:

| Their JSON field | Krea2 natural-language form |
|---|---|
| `high_level_description` | First sentence(s) of the prompt — the one-line "what is this image" |
| `style_description.aesthetics` | `Style: {aesthetics}.` (e.g. "editorial portraiture, surreal") |
| `style_description.lighting` | `Lighting: {lighting}.` |
| `style_description.photo` + `medium` | `Framing: {photo}. Medium: {medium}.` |
| `color_palette` (hex) | **Translate hex → color WORDS** ("warm sand-beige and slate-blue palette, pale cream highlights") — Krea2 takes no hex |
| `compositional_deconstruction.background` | `Background: {background}.` |
| `elements[].bbox` (0–1000) | **Spatial language**: y-band → top/middle/bottom third; x-band → left/center/right ("upper-left region", "lower-right of the frame") |
| `elements[].desc` | `In the {position}: {desc}.` |
| `type: "text"` elements | `Render the text "{text}" in the {position}.` (Krea2 renders text in-prompt) |
| ultrawide aspect | Set the **aspect widget to 21:9** (or 32:13-style ultrawide) on the one-click Krea2 workflow — cinematic shots |

**Template (paste-ready pattern for our Krea2 prompts):**

```
{high_level_description}.
Style: {aesthetics}. Lighting: {lighting}. Framing: {photo}. Medium: {medium}.
Palette: {color words, no hex}.
Background: {background}.
In the {spatial position}: {element desc}. (repeat per element)
{Optional: render the text "..." in the {position}.}
ONLY ONE character, no other people, no duplicates.   ← our Krea2 quirk rule
```

**Movie relevance:** the "memory-laden hall / ghostly portrait panels" example is the strongest candidate for a Jaisal/Zidhan cinematic ultrawide shot (21:9), and the long-form natural-language style matches how our Krea2 identity-edit instructions already read. Adapt when the Krea2 batch is next run (user: "adapt for Krea2 later").

## 6. Community notes

- **Settings tip (NOT APPLIED — user rule):** author says use **Euler** instead of `res_multistep` or you get noise artifacts — recorded for completeness only.
- **Prompt source:** most example images are in the Civitai gallery post [29358642](https://civitai.com/posts/29358642) — **PNGs carry the full prompt in their metadata** (download a PNG → metadata tab = the exact structured prompt). The HF dataset that held the full prompt collection is deleted.
- No-LoRA, no-JSON-prompts claim in the post is contradicted by the post's own Civitai link (which IS json prompts) — the "no JSON" likely means no *hand-written* JSON for the gallery shots; the workflow uses the builder node.
- Workflow architecture (reference only): Ideogram-4 + `Ideogram4PromptBuilderKJ` + optional LTXV image→video extension (speech audio) + RTX upscale. Based on the Comfy-Org day-0 Ideogram-4 support post.
