# MiniMax H3-IMAGE Cinematic Playbook (2026-11-28)

Consolidated from four raw research reports (all fetched 2026-11-28): `session_tmp\research_h3image\reddit_h3image.md`, `civitai_h3image.md`, `x_h3image.md`, `comfyui_docs_h3image.md`. Every claim keeps its source URL. **VERIFIED** = read in a fetched page; **HEARSAY** = store/snippet metadata only; **(unverified)** = not corroborated. Video-model findings are labeled **[VIDEO MODEL]** and are NOT H3-IMAGE.

## Verdict summary

- **All four raw sources were present and non-empty** (Reddit 9/9 stealth fetches, Civitai 19 model pages via public API, X 10/10 stealth fetches, official docs/GitHub/local-source reads). No source had to be reported as missing.
- **Community consensus: H3-IMAGE is primarily an editing model** — one checkpoint does t2i + edit with up to 16 references (https://huggingface.co/MiniMaxAI/MiniMax-H3-Image, https://x.com/DidoofficialM/status/2126519005523374147), and "shines as an editing model, perhaps even better than any other model currently in existence" (https://www.reddit.com/comments/1xw0eb6). For cinematic *stills* it is valued for real photographic physics: "Ideogram 4 and Minimax H3 are the only open source models out there that adhere to actual photography physics" (https://www.reddit.com/comments/1xvesum).
- **For cinematic work specifically, the look comes from prompting, not from a LoRA** — there is **no H3-IMAGE "cinematic" LoRA on Civitai**; the only two LoRAs named "Cinematic" are trained on the **video** model (TuTu_1018, see [VIDEO MODEL] table below) (https://civitai.com/models/2890588, https://civitai.com/models/2908686). Official guidance is explicit that the word "cinematic" alone does not determine anything in the prompt-enhancer — the film look must be written as **visible physical details** (light direction, grain, palette, lens) (https://huggingface.co/MiniMaxAI/MiniMax-H3-Image-PE, `prompt/t2i/system_prompt.txt`).
- **The single biggest t2i quality lever the community found is the ≥64-vision-token "edit mode" trigger**: plug a small empty black/white image into the reference slot (or use KJ's "H3 Prompt Weight" node) and the crusty default-t2i artifacts (moles, flaky skin) largely disappear (https://www.reddit.com/comments/1xuj7b9, https://www.reddit.com/comments/1xwbo1h).
- **Resolution doctrine:** native ~16 MP; community advice is "do not use at 1024/4MP" (4MP output looks like a stretched 1MP), generate at 16 MP and downscale to 4K for the natural look (https://www.reddit.com/comments/1xsqz2h, https://www.reddit.com/comments/1y3tdzk). Officially: 2K = 4,194,304 px area, 4K = 16,777,216 px area, default = 4K; custom sizes 655,360–20,000,000 px, edges multiples of 32 (https://platform.minimax.io/docs/api-reference/image-generation-h3-generations.md, https://docs.comfy.org/tutorials/image/minimax/minimax-h3-image).

## Prompting style

### Structure (official, VERIFIED)

From the official `h3-image-prompt-writing` skill + README "Prompting Tips" (https://github.com/MiniMax-AI/MiniMax-H3-Image, `skills/h3-image-prompt-writing/SKILL.md`, fetched 2026-11-28) and the Civitai base page (https://civitai.com/models/3045541):

1. **Task before style** — open with what the image is/who is in it; style comes after.
2. **Layout before details** — number of subjects, positions, angle, whitespace first.
3. **Style through visible details** — "soft side light, metallic reflections, clean whitespace" beats "premium feel".
4. **Quote every word that appears** (language, spacing, position, line breaks); for no text: *"The image contains no text, letters or numbers."*
5. **Give each reference image a role** (identity / color / layout / pose).
6. **Say what changes and what stays** — *"Change the cup on the left to blue, keeping its shape, material, position and size."*
7. **Grids as "2 rows and 3 columns"**, never "2x3" (can flip).
8. **Edit prompts = one continuous paragraph**: source definitions → target overview + relationships → changed/new details; narrate the final state, don't issue commands.

The official edit-PE contract is a **3-part caption**: definitions (`<Subject 1>` = "The red cup at the left of `<Picture 1>`"), four relationship types (`fully preserved` / `partially preserved` / `attribute transfer` / `weak reference`), then only changed/new details (https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_minimax_h3_image_edit.json, fetched 2026-11-28). Reference tags: API/ComfyUI-native use `<Picture N>` in upload order; the **partner node** uses `@ImageN` in connection order; PE uses `<Subject N>` for reusable content (https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3-Image/main/skills/h3-image-prompt-writing/references/edit-en.txt, LOCAL `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\comfy_api_nodes\nodes_minimax.py`). This is the image-model analogue of our H3-video R2V `<Picture N>`/`<Subject N>` convention, minus timed shots/audio (our `docs/MINIMAX_H3_R2V_PROMPTING_GUIDE.md`).

### Community prompting guidance (VERIFIED)

- "Short prompts give the glossy doll face. **Write it long and describe it like a phone photo: camera, light, skin.**" (https://www.reddit.com/comments/1xwbo1h)
- Community temperament note: model "feels like it's trained on a lot of 'cinematic/film' footage… creatures almost look like really great oldschool practical effects… very good at highly dynamic poses… pretty good at horror and gore" (https://www.reddit.com/comments/1xt9yzt).
- "Do not plug the image to the prompt enhancer" (https://www.reddit.com/comments/1xuj7b9).
- Realism-LoRA convention: they "add noise/grain, imperfect composition and lighting, and some smear/artifacts to simulate lower quality lenses or sensors" (u/ptwonline, https://www.reddit.com/comments/1xvesum).
- X A/B test prompt pattern (partial, tail truncated at 2000 chars): "Ultra-realistic cinematic street portrait of a beautiful young woman with short, messy dark brown bob hair, natural freckles across her nose and cheeks…" — subject-detail chains beat abstract style words (https://x.com/harboriis/status/2121947709406117898, fetched 2026-11-28).
- Title-space rule for our film work: "Keep approximately the top quarter quiet for later typography, and do not generate a title, logo, or text in the current image" (official showcase, https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3-Image/main/showcase/game-worlds.md).

### Cinematic vocabulary that recurs in official material (VERIFIED)

- **Documentary look**: "shot like a documentary still", "like an ordinary moment… captured by a documentary photographer with a standard lens on film", "nothing staged".
- **Lighting**: "Natural light, no artificial lighting at all", "Fully diffused light, almost no shadows", "Low-key exposure overall", "strongly directional sunlight and limited ground bounce".
- **Grain/texture**: "medium film grain", "fine-grain film texture", "moderate 35 mm film grain, gentle highlight bloom", "fine colored digital noise in the shadows, slight color bleeding and compression artifacts" (MiniDV look).
- **Color**: "Cool tones, blue-green overall and leaning gray, low saturation", "muted teal midtones, and deep-indigo shadows… restrained cool palette", "realistic cinematic color grading".
- **Optics**: "standard 35mm to 50mm focal length", "focal length 85–105mm; aperture f/2.0–f/2.8", "focal length about 40mm, aperture about f/4, shutter about 1/250 s, ISO 400", "24 mm wide-angle", "widescreen ratio approximately 2.5:1".
- **Depth/atmosphere**: "shallow depth of field", "volumetric fog", "atmospheric perspective / recession", "natural vignetting", "high dynamic range".
- **Anti-AI-look**: "natural skin texture with no smoothing", "avoid heavy skin smoothing, oversharpening, and strong beauty filters", "Avoid cheap-looking CG, plastic skin, excessive sharpening, HDR halos" (official showcase + design.minimax.io FAQ, https://design.minimax.io/tools/h3-image).
- All from https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3-Image/main/showcase/real-world.md and `showcase/game-worlds.md` (fetched 2026-11-28).

### Verbatim example prompts

**1. Community cinematic prompt (Reddit, VERIFIED)** — u/Certain-Report-3833, "H3 Image is wildly creative" (https://www.reddit.com/comments/1xt9yzt):

> "digital cinema footage filmed inside a derelict industrial spaceship. An enormous near-black lean fleshy six-armed six-legged creature climbs up from ceiling pipes into a narrow maintenance corridor, long sinewy angular limbs bracing opposite walls, elongated pendulous abdomen twisting, small recessed head with 8 shining small black eyes, thin webbing stretched between arms and flanks. Wet charcoal-black skin remains black, smoky translucency only in the thinnest membrane edges. A single off-camera flashlight from the center cuts a hard oblique beam across its face and its abdomen; most of the creature and corridor disappear into darkness, with subtle readable shadow detail. Camera caught mid-retreat, imperfect off-center framing, subtle high-ISO sensor noise, shallow focus and subdued desaturated colors. Bolted pipes and oily steel visible only inside the beam, photographed physical creature effects rather than polished concept art, no text or camera overlays heavy atmospheric fog, strong backlighting"

Reusable look-words: `digital cinema footage`, `high-ISO sensor noise`, `shallow focus`, `subdued desaturated colors`, `imperfect off-center framing`, `strong backlighting`, `heavy atmospheric fog`, `photographed physical effects rather than polished concept art`.

**2. Official documentary film photo (VERIFIED)** — https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3-Image/main/showcase/real-world.md:

> "A real rural documentary photograph in portrait format, like an ordinary moment on a farm captured by a documentary photographer with a standard lens on film. Natural light, no artificial lighting at all, nothing staged. … A foggy day, perhaps with fine snowflakes or drizzle drifting down … Fully diffused light, almost no shadows. … A full shot from a roughly eye-level camera, slightly low … A standard 35mm to 50mm focal length, natural perspective, no distortion. Medium depth of field … Cool tones, blue-green overall and leaning gray, low saturation … Contrast is moderate to low, highlights in the fog are slightly overexposed to white, and the image has a soft, diffused feel and medium film grain. No text, watermarks, or interface elements anywhere in the image."

**3. Official cinematic film-style portrait (VERIFIED, same source)**:

> "A realistic cinematic film-style portrait close-up … low to medium contrast, soft highlights, fine grain, slight fading and soft focus … overall aspect ratio about 16:9; inner image ratio about 7:5; shot size: extreme close-up; focal length 85–105mm; aperture f/2.0–f/2.8; shallow depth of field; warm white balance; low saturation; soft contrast; fine-grain film texture; slight motion blur in the hair; natural skin texture; avoid heavy skin smoothing, oversharpening, and strong beauty filters."

**4. Our own env-plate prompt (LOCAL, for the A/B test)** — `h3image_t2i_env_pilot.json`: "A vast 1950 concrete football stadium bowl under a heavy overcast sky… shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour" (E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\h3image_t2i_env_pilot.json).

### Do / Don't

**Do:**
- Write long, literal, physically-specified prompts (light direction, material texture, lens, grain, palette) — this is what the PE/enhanced caption style expects (https://huggingface.co/MiniMaxAI/MiniMax-H3-Image, official enhanced-caption example).
- Use the PE ratio ladder for aspect: 3:2/2:3 for photographic direction, 16:9/9:16 for strong direction, 21:9 for banners/panoramas (https://huggingface.co/MiniMaxAI/MiniMax-H3-Image-PE).
- Keep "cinematic" as a secondary word; carry the look with visible details.
- Leave the top quarter quiet for title compositing in post.
- For edits: one continuous paragraph, final-state narration, `<Picture N>`/`<Subject N>` tags.

**Don't:**
- Don't use short prompts (→ glossy doll face, https://www.reddit.com/comments/1xwbo1h).
- Don't use a negative prompt — **not supported, rejected** (API, https://platform.minimax.io/docs/api-reference/image-generation-h3-generations.md); write avoids into the positive.
- Don't write "2x3" for grids; don't rely on seeds for determinism (seed is a re-run trigger only, LOCAL `nodes_minimax.py` tooltip).
- Don't wire reference images into the prompt-enhancer node (https://www.reddit.com/comments/1xuj7b9).
- Don't generate at 4MP/1024 for detail (https://www.reddit.com/comments/1xsqz2h).
- Don't expect `enhance_prompt` off + `auto` ratio to work — fixed ratio required or HTTP 400 (API docs above).

## Resolution & size

### Official spec (VERIFIED)

From https://platform.minimax.io/docs/api-reference/image-generation-h3-generations.md + https://docs.comfy.org/tutorials/image/minimax/minimax-h3-image + GitHub README (all fetched 2026-11-28):

| Level | Area |
|---|---|
| 1K | 1024×1024 = **1,048,576 px** (drafts) |
| 2K | 2048×2048 = **4,194,304 px** (faster/cheaper) |
| 4K | 4096×4096 = **16,777,216 px** (default; "4K gives the best results") |

- **Custom size**: `width×height`, total area **655,360–20,000,000 px**, aspect **1:3–3:1 inclusive**, no scaling or rounding applied; all edges multiples of **32 px** (docs.comfy.org). Partner-node custom widget: default 2048, min 512, max 7680, step 16 (LOCAL `nodes_minimax.py`).
- **Pixel math (16 MP-class sizes, ≈16.8 MP target area per ratio, edges snapped):**

| Aspect | Size | Area (computed) |
|---|---|---|
| 1:1 | 4096×4096 | 16,777,216 |
| 4:3 / 3:4 | 4736×3552 / 3552×4736 | 16,822,272 |
| 3:2 / 2:3 | 5024×3360 / 3360×5024 | 16,880,640 |
| 16:9 / 9:16 | 5472×3072 / 3072×5472 | 16,809,984 |
| 21:9 | 6272×2688 | 16,858,176 |

(Source table: HF sizes section, https://huggingface.co/MiniMaxAI/MiniMax-H3-Image#sizes; docs.comfy.org. All five land at ≈16.8 MP — the model is *built* for 4K-class output; 2K is a cheaper area target, not a native scale.)
- **2K at 16:9 = 2720×1536 = 4,177,920 px** (API docs example, edges multiples of 16).
- For other ratios the area target is kept and edges snapped: `size_for('5:4')` → 4576×3648 (README).
- `min_generation_area` default 4,194,304 (= 2K) for the self-hosted server (README).
- Local ComfyUI templates: `ResolutionSelector` defaults to **16 MP** (4–16 MP, multiple 32); template prompt-node default canvas 3104×3104 (~9.6 MP) — our `h3image_t2i_cine.json` carries that default (docs.comfy.org).
- **Edit workflows upscale the input to the canvas first** — "effective range is about 4 MP to 20 MP"; reference preprocessing: 32-px grid, vision short edge 1024, VAE short edge clamped 1024–2048 (docs.comfy.org).
- Sampling: **6 steps, CFG 1.0, euler + simple, denoise 1, no negative** (CFG-distilled checkpoint; negative is a `Conditioning Zero Out`, never read) (docs.comfy.org).

### Community resolution guidance (VERIFIED)

- "Trained around 16 MP, so I use 3552×4736 for a portrait. The default 4 MP is where the broken teeth come from. Going 4 to 16 MP only added about 9 seconds of sampling." (https://www.reddit.com/comments/1xwbo1h)
- "Do not use model at 1024"; "if you want detail, you need to raise the actual resolution to compensate"; 4 MP "looks like a 1 MP image got resized to 4 MP without any upscale effort" (https://www.reddit.com/comments/1xsqz2h, https://www.reddit.com/comments/1y3tdzk).
- "I generate images at 16 megapixels and then resize them down to 8 (4K). … The detail in a higher-resolution image that is subsequently downscaled is always robust and plentiful. … At very high resolutions they look artificial, whereas at more modest resolutions as 4K, they look perfect." (u/m4ddok, https://www.reddit.com/comments/1y3tdzk)
- **Editing**: "the max practical resolution tops out at 6 MP. Anything higher doesn't add any new detail, it just resizes the output which causes blurry/soft image." (https://www.reddit.com/comments/1y3tdzk)
- 20 MP outputs "still barely 2–3 MP quality wise" (https://www.reddit.com/comments/1xt9ocv); counterpoint "Generate images at 48 MP, the quality is then incredible! (156 seconds on 5080)" (u/Altruistic_Print717, same thread).
- HEARSAY (card title only): "Native 100 megapixel (no upscaling) … on 5090 @ 240 seconds" (https://www.reddit.com/comments/1xu3dum, store 2026-11-14).
- X confirms the ceiling: "native 4K high-definition output, with a maximum of 20 million pixels", 16 ref images (https://x.com/jiahao9527/status/2126532034038255624, fetched 2026-11-28). No explicit "2K size option" or aspect enumeration was found in any fetched X text — **2K not confirmed on X (gap)** (https://x.com/_0xIDARA/status/2126526994619810153 is the API-mechanics post; 2K option unverified there).

### When to use custom size

- Use `custom` when you need an exact frame for compositing (e.g. our 2560×1440 plates, 3872×5056 ≈ 19.6 MP — both satisfy the 32-multiple + 20 MP ceiling; LOCAL saved workflows).
- Use `4K` (default) for best quality; `2K` for fast iteration/drafts; `1K` for cheap drafts.
- With `enhance_prompt` **off**, a fixed ratio (exact size or `X:Y`) is **required** or the API returns 400.
- Low-VRAM: enable the `Resize Image/Mask` node and lower its megapixels before sampling (docs.comfy.org).

## LoRA & model shortlist

**Key finding: no H3-IMAGE "cinematic" LoRA exists on Civitai (as of 2026-11-28)** — the two "Cinematic" LoRAs are VIDEO-model (below). H3-IMAGE cinematic look = prompting (§Prompting style) + the style LoRAs in this table. Civitai free-text search "minimax h3 image" returned "No results" (browser head, 2026-11-28) — the model is indexed only under the "MiniMax H3 Image" base-model filter.

### H3-IMAGE LoRAs (Civitai, all VERIFIED via Civitai public API 2026-11-28)

| Name | Author | Link | What it adds | Trigger words |
|---|---|---|---|---|
| MiniMax H3 Image Outpaint LoRA | AusBoss | https://civitai.com/models/3064644 | Outpaint/uncrop at ~4 MP (short side ≤2048), pad gray #808080; above ~4 MP H3 drifts | `Outpaint <Picture 1>: replace the solid gray areas…` (455 dl) |
| [H3 image]pwni style | cosca69226 | https://civitai.com/models/3059877 | Experimental **anime** style on pruned-int8 H3 Image | `pwni style`, weight <1.0 (0.6–0.8) (233 dl) |
| [H3 image]rurudo style (るるど) | KaleidRuby | https://civitai.com/models/3054448 | Flat anime color, explicitly H3 IMAGE (not video) | `@rurudo`, 16 MP cfg=1 step=6, strength 0.8–1.5; total LoRA strength >2.0 degrades → raise steps 6→12 (235 dl) |
| MiniMax H3: IMAGE – Polyhedron: Better Hair | Polyhedron_AI | https://civitai.com/models/3058358 | Hair quality; pairs with "text with empty image" trick | `ha8ir`, `perfect hair`, `thick hair`, `airy volume`, `natural waves`, `soft flyaways`, `hair subsurface scattering` (531 dl) |
| H3I Dark Fantasy | Adel_AI | https://civitai.com/models/3064347 | Dark-fantasy style (ComfyUI + workflow) | `Bradhamel art style.` (190 dl) |
| H3I Aurora | Adel_AI | https://civitai.com/models/3062941 | Aurora style (ComfyUI + workflow) | `Bradhamel art style.` (0 dl) |
| Minimax H3 Image Upscaler (LORA + Workflow & Batch) | JonXL | https://civitai.com/models/2924512 | Upscale to 1920×1920 (upscaler, **not** a detailer); 24-frame quality + 1-frame speed variants | none (2,472 dl) |
| MiniMax-H3-Image-Character-Swap-LoRA (`h3_image_character_swap_v1.safetensors`, rank-16, 155 MB) | akatz-ai | https://huggingface.co/akatz-ai/MiniMax-H3-Image-Character-Swap-LoRA | Character swap from a reference sheet (face/costume/style), keeps pose/framing/lighting; **the only LoRA named by any official guide** — used by the official character-swap template at strength 1.0 | none stated (HF store 2026-11-26: 4,802 dl / 86 likes) |
| Minimax-H3-Image-Pose-Transfer-Lora | supermansundies | https://huggingface.co/supermansundies/Minimax-H3-Image-Pose-Transfer-Lora | Pose transfer | (unverified — no trigger stated; 6 dl / 34 likes, HF store 2026-11-26) |

Also from X (VERIFIED via X-store snippet, 2026-11-26/27): **akhaliq/MiniMax-H3-Image-Character-Swap** — add at strength 1.0 to the Edit workflow (https://huggingface.co/akhaliq/MiniMax-H3-Image-Character-Swap, https://x.com/PhotogenicWeekE/status/2122043541027430821); akatz_ai's "H3 Image Character Swap V1" X post (https://x.com/akatz_ai/status/2124202173143880172). **Fizgig** H3 Image Standard training preset (v9.6.0/9.7.0, 0.25 MP, 30 epochs, AdaFace ViT likeness) for training your own character LoRAs — https://github.com/shootthesound/Fizgig, https://www.reddit.com/comments/1xufdvb; community recipe: 6 photos, 0.5 MP, rank 32, ~90 epochs, generate at 16 MP, strength 1.0–1.1 (https://www.reddit.com/comments/1xwbo1h).

**Not on Civitai / caveats:** no H3-IMAGE face/identity LoRA on Civitai (face consistency is done via workflow character sheets instead); H3-IMAGE LoRA training is not available on-site on Civitai (base page, https://civitai.com/models/3045541). "No loras on h3" is the community perception on X (https://x.com/NiiColaVT/status/2126247015415730481 thread) — contradicted by the Civitai entries above (those LoRAs exist for the image model; the X thread discussed the video model). **H3 VIDEO LoRAs do NOT work on H3-IMAGE** ("MiniMax H3 Image doesn't support the MiniMax H3 LoRA", https://x.com/PhotogenicWeekE/status/2122043541027430821).

**Generic cinematic LoRAs (SDXL/FLUX/Pony bases — NOT H3-IMAGE-compatible, listed so they aren't mistaken for H3 assets)**: Cinematic Shot (ZyloO, https://civitai.com/models/432586), Cinematic Photography Style XL + F1D (EauDeNoire, https://civitai.com/models/214956), Cinematic Tools (Zovya, https://civitai.com/models/225364), Kodak Film Grain (EauDeNoire, https://civitai.com/models/365274), IMAX 70mm (EauDeNoire, https://civitai.com/models/1249970), Anamorphic (EauDeNoire, https://civitai.com/models/520524), Warm/Cool Light (EauDeNoire, 290860/290864), color grading (EauDeNoire, https://civitai.com/models/541698), Cinematic Hard Cut (neph1, https://civitai.com/models/2088559), Cinematic Dark Lighting (vizsumit, https://civitai.com/models/2477155), Cinematic Fantasy (Nugus, https://civitai.com/models/2957855) — all VERIFIED tags 2026-11-28.

### [VIDEO MODEL] — Cinematic H3 video LoRAs (NOT H3-IMAGE-compatible, clearly labeled)

| Name | Author | Link | What it adds | Trigger |
|---|---|---|---|---|
| Minimax H3 Cinematic V2 | TuTu_1018 | https://civitai.com/models/2890588 | Cinematic look for H3 **video**: fixes plastic look/over-sharpening/harsh lighting/"AI feel"; enhances natural lighting, color depth, DOF, skin texture, lens character; strength 0.85 | none stated (10,023 dl) |
| Minimax H3 Cinematic Look (No Tensor Errors) | TuTu_1018 | https://civitai.com/models/2908686 | Same goal, tensor-error-fixed build; strength 0.7 (0.5 high-motion) | `DY` (5,497 dl) |
| Minimax H3 Photorealistic Image Generator | JonXL | https://civitai.com/models/2884206 | Photoreal images up to 3840×2176 from the **video** model (first+last frame of a 22-frame clip) | `ph0t0r34l` (6,550 dl) |
| MiniMaxH3_Enhancers | vrgamedevgirl | https://civitai.com/models/3025511 | Beauty/clarity enhancer for H3 video (Epoch 5 lighter / Epoch 10 stronger) | none (4,827 dl) |
| Minimax H3 Turbo LoRAs | tsolful | https://civitai.com/models/2837571 | Speed distillation (NOT style) — larryvrh/dmad/taomate/lightx2v/pika-h3-flex | 6–8 steps (62,127 dl) |

### Official weights & templates (VERIFIED 2026-11-28)

- Base: https://huggingface.co/MiniMaxAI/MiniMax-H3-Image (BF16 DiT 68.65 GB) · PE prompt-expander: https://huggingface.co/MiniMaxAI/MiniMax-H3-Image-PE (NVFP4, 17.9 GB; official T2I system prompts at `prompt/t2i/`).
- ComfyUI-native: https://huggingface.co/Comfy-Org/MiniMax-H3-Image — `minimax_h3_image_pruned_int8_convrot.safetensors` (~21 GB), `minimax_h3_image_pruned_w4a8.safetensors` (~12.5 GB), `minimax_h3_image_vae_fp16.safetensors` (~1.17 GB), `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` (~25 GB) or `qwen3.5_9b_w4a8_gptq.safetensors` (6.84 GB), `qwen3.8_27b_minimax_h3_image_pe_w4a8_gptq.safetensors` (Comfy-Org-recommended PE).
- Quant checkpoints (Civitai): tsolful INT8/INT6/INT4 (https://civitai.com/models/3045867, 2,149 dl), xiaoyueblandon205 full INT8 QKV-fixed (https://civitai.com/models/3046884), Thasmodius fp8/nvfp4/GGUF (https://civitai.com/models/3045918), ZoeJoe Exact-adaLN NVFP4 (https://civitai.com/models/3057968).
- VAE alternatives (community): PrunaAI **P-H3 VAE** (https://huggingface.co/PrunaAI/P-H3-Image-Comfy, quality helper per https://www.reddit.com/comments/1xuj7b9), ostris **decoder-only VAE finetune** (https://huggingface.co/ostris/ostris_h3_image_vae, https://x.com/ostris VAE posts 2125689235558760633 / 2125757126689825231).
- Official ComfyUI templates (need ComfyUI 0.45.0+; template pack 0.11.104+): `image_minimax_h3_image_t2i.json`, `…_edit.json`, `…_character_swap.json` — https://github.com/Comfy-Org/workflow_templates (character-swap template: source scaled to 864×1152 = 1 MP, PE off, LoRA strength 1.0).
- Notable Civitai workflows: AusBoss AIO "Generate, Edit + Upscale | 8 Pictures" with Grain cleanup Light/Strong + SeedVR2 upscale (https://civitai.com/models/3046048, 6,892 dl), TPStudio "H3 Image Panel" SFW control panel (https://civitai.com/models/3063091), AusBoss 16 MP character sheet (https://civitai.com/models/3049206), juiceman868 Character Sheet Builder (https://civitai.com/models/3046576), foxydits Pose Studio 9-ref (https://civitai.com/models/3045966), ArtGourieff 17+ MP (https://civitai.com/models/3053127).

## enhance_prompt guidance

Facts (all VERIFIED, 2026-11-28):

- **API**: field `disable_prompt_enhanced`, **default `false` = enhance ON** (https://platform.minimax.io/docs/api-reference/image-generation-h3-generations.md). **T2I**: ON by default, can be disabled — **when disabled a fixed ratio is required** (exact `size` or `aspect_ratio`), else HTTP 400. **Edits: enhancement always applied** (API doc: "Image edits always apply prompt enhancement").
- **Partner node `MinimaxH3ImageNode`**: `enhance_prompt` Boolean, **default True**; tooltip: "Image editing is always enhanced. When off, pick an aspect ratio or custom size." `disable_prompt_enhanced = None if image_urls else not enhance_prompt` (LOCAL `nodes_minimax.py`).
- **Local templates**: `Boolean (Enable PE?)` ON by default, PE = `TextGenerateV2` + 9B W4A8 or the 27B PE (https://github.com/Comfy-Org/workflow_templates, docs.comfy.org).
- **Prompt-length reality**: prompt max 32,000 chars; **when enhance is OFF only the first ~4,096 tokens are effective** (API + README). Partner node with refs: 8,000-char prompt cap (LOCAL).
- **`revised_prompt`** is returned per image = the enhanced caption actually used — log it in every run.
- **Self-hosted server**: no built-in expansion — a full literal prompt (or our local 27B PE LLM via `TextGenerate`, `D:\models\qwen\Qwen3.8-27B-NVFP4-MTP-LOW.gguf` is a GGUF of the 27B PE family) substitutes (README "Request parameters", LOCAL).
- **Reddit**: **no thread discusses `enhance_prompt` on/off** (9 threads checked). Only guidance: "Do not plug the image to the prompt enhancer" (https://www.reddit.com/comments/1xuj7b9), and the long-prompt style substitutes for enhancement ("write it long… like a phone photo", https://www.reddit.com/comments/1xwbo1h). The KJ "H3 Prompt Weight" node (edit-mode flip) is the active community quality tool, not the template's enhance toggle. **X: zero mentions of `enhance_prompt` in any fetched text (documented gap).**

**When ON:** t2i with short/medium prompts where you want the model's caption-expansion; all edit work (always ON anyway). **When OFF:** when your prompt is already a long, literal, physically-specified description (it may saturate what the enhancer adds), when you need exact composition control (PE can shift framing), or for fair A/B comparison (see below). **Cost note**: enhance ON also changes billing text-token range (900–5000 vs 0–300 without refs, LOCAL `nodes_minimax.py`).

**For A/B fairness (Krea2 vs H3IMAGE):**
1. Run the **primary comparison with `enhance_prompt` OFF** on the H3 side (exact prompt as written = Krea2's situation; Krea2 has no enhancer, so enhance-ON H3 is not a like-for-like). Set a **fixed ratio** (e.g. 16:9) since OFF + `auto` = 400.
2. Run a **secondary H3-internal column with enhance ON** (same prompt, same fixed ratio) to see whether the enhancer changes the verdict — capture `revised_prompt` to diff against the input.
3. Keep the **edit-mode trigger ON on both sides of the H3 test** (dummy black/white image on `image_0`, or KJ Prompt Weight node) — community consensus makes this the dominant quality factor; it is an H3-specific setting, so note it as an H3 advantage, don't try to emulate it on Krea2.
4. Keep prompts **≤ ~4,096 tokens** when enhance is OFF (effective window).
5. Log `revised_prompt`, seeds, and node settings for every cell of the matrix.

## Failure modes & community-reported pitfalls

All VERIFIED (Reddit bodies fetched 2026-11-28) unless marked:

1. **Crusty/artifact t2i output** (moles, pimples, dry flaky skin, crusty splotches) on pure t2i default settings — fixed by the ≥64-vision-token "edit mode" trigger (dummy reference image or KJ Prompt Weight node); one counterpoint: "it does nothing for me quality wise, made it much worse in fact" (u/detailteufel, empty black 1024 px) (https://www.reddit.com/comments/1xuj7b9, https://www.reddit.com/comments/1xwbo1h).
2. **VAE-derived softness/artifacts at all resolutions** — video-inherited high-compression VAE: "the H3 VAE is based on the requirements of a video model where compression needs to be very high, leading to less detail"; "godawful artifacting, a lot of it coming from VAE"; textures "don't resemble film grain or the noise you'd get from a digital camera sensor" (https://www.reddit.com/comments/1y3tdzk, https://www.reddit.com/comments/1xvesum). Mitigations: LCM + P-H3 VAE (https://www.reddit.com/comments/1xuj7b9), ostris VAE finetune (HF link above).
3. **High-MP = upscaled low-MP**: 20 MP "barely 2–3 MP quality wise"; >6 MP editing just resizes → blurry/soft (https://www.reddit.com/comments/1xt9ocv, https://www.reddit.com/comments/1y3tdzk, https://www.reddit.com/comments/1xw0eb6). "It's like a camera that pushes megapixels with a tiny sensor."
4. **Body horror / face-anatomy failures** on complex non-photographic subjects — "inherited from the video model" (https://www.reddit.com/comments/1xt9ocv).
5. **Face-transfer weakness in edit mode** — produces "a relative", not the person; mitigations: multiple face refs + small face LoRA (https://www.reddit.com/comments/1y3tdzk).
6. **Identity breakage on pose/angle change** in edit mode (https://www.reddit.com/comments/1xw0eb6).
7. **Glossy doll faces** from short prompts (https://www.reddit.com/comments/1xwbo1h).
8. **Reference-image side effects**: horizontal/vertical smeared lines in smooth/blurred areas after enabling reference mode; edit-mode pattern suddenly appearing at step 4–5 (https://www.reddit.com/comments/1xuj7b9).
9. **Iteration time** ~1:15 cold start (video-model base); mitigations: int8_convrot ("significantly faster while differing only negligibly in quality") and keeping the workflow open/in memory (https://www.reddit.com/comments/1y3tdzk).
10. **Low-res degradation**: 4 MP outputs look like stretched 1 MP; "the low-res performance gets significantly worse" as models generalize on 2k+ detail (https://www.reddit.com/comments/1y3tdzk, https://www.reddit.com/comments/1xsqz2h).
11. **Default ComfyUI template underperforms**: "pretty bad at showcasing the model's capabilities"; default edit workflow resizes the input (decent but blurry) (https://www.reddit.com/comments/1xt9ocv, https://www.reddit.com/comments/1xsqz2h).
12. **IP references silently stop working** — fix: re-reference them (https://www.reddit.com/comments/1xt9ocv).
13. **LoRA weakness (base model)**: "tried some loras trained for it specifically, terrible experience… can't remove the slop look"; "both of them [Krea2, H3] are nearly impossible to train well" (https://www.reddit.com/comments/1y3tdzk). (Counterpoint: the Civitai style LoRAs in the shortlist exist and are active — §LoRA.)
14. **Style sameness / "slop" faces**: "why do they all look the same", "anime→real slop face" (https://www.reddit.com/comments/1xw0eb6).
15. **Seeds are not determinism controls** — API supports no user seeds; partner-node tooltip: "results are non-deterministic regardless of the seed" (LOCAL `nodes_minimax.py`).
16. **`enhance_prompt` OFF + `auto` ratio → HTTP 400** — fixed ratio mandatory (API docs).
17. **Total LoRA strength > 2.0 degrades H3 Image** — fix by raising steps 6→12 (rurudo page, https://civitai.com/models/3054448).
18. **No negative prompt** — rejected; write avoids into the positive (API + README).
19. **Streaming endpoint not idempotent** — billed for successful images even on client timeout; set `max_retries=0` (API docs).
20. **License caveats**: community license — separate written authorization required if annualized revenue > $1M or you provide a hosted service (https://github.com/MiniMax-AI/MiniMax-H3-Image); a secondary Civitai description claims outputs unavailable in EU/UK/KR/US and may not train other models — **treat the official HF LICENSE as authoritative** (https://huggingface.co/MiniMaxAI/MiniMax-H3-Image).
21. **People-editing vs Qwen**: "At least if editing images of people… for everyday use, I think Qwen [Edit 2.1] does a better job" (https://www.reddit.com/comments/1xwbo1h).
22. **People-editing face drift** and "Fibo and qwen 2.1 have been vastly better for me" — the community is split on H3-IMAGE vs Qwen-Image-2.1 for pure generation; H3's edge is editing + speed (https://www.reddit.com/comments/1xw0eb6, https://www.reddit.com/comments/1xufdvb: "i find h3 image faster than moss").

## A/B protocol for our Krea2-vs-H3IMAGE env-plate test

Context: our saved H3 side is `h3image_t2i_env_pilot.json` (`MinimaxH3ImageConditioning` local-node path; 2K, 16:9, `enhance_prompt=false`, seed 42/randomize). Per project hard rule D192 the agent does NOT queue workflows — this protocol is for the user to run.

**The 5 plates** = five environment/establishing plates (no people — faceless plates sidestep failure modes #4/#5/#6 and match the "environment-plate" purpose). Use the prompt set from `d:\models\vsCodeMcp\prompts\` (e.g. `jaisal_ref_prompts.txt` environment entries) or the five plates already drafted in the env-pilot prompt file. Each plate's prompt follows the structure in §Prompting style: task → layout → light → textures → optics → grain/grade → "no people, no humans, no text, top quarter quiet".

**Fairness matrix — 2 rows × 5 plates:**

| Cell | H3-IMAGE settings | Krea2 settings |
|---|---|---|
| Primary | `enhance_prompt` OFF, **fixed 16:9**, edit-mode trigger ON (empty black/white image on `image_0` or KJ Prompt Weight node), 6 steps / cfg 1 / euler / simple / denoise 1, no negative, **size 2K 16:9 = 2720×1536** | Same prompt verbatim, standard Krea2 sampler settings (document them), matching 16:9 output size (Krea2 native or 2720×1536) |
| Secondary (H3-internal) | Same as primary but `enhance_prompt` ON (fixed 16:9 required), capture `revised_prompt` | — (Krea2 has no enhancer; this column answers "does the enhancer change the verdict", not the cross-model comparison) |

**Fairness rules:**
1. **Identical prompt text on both sides** — one long structured prompt per plate (the long-prompt style is H3's known remedy for the glossy-doll look, https://www.reddit.com/comments/1xwbo1h; keep it ≤ ~4,096 tokens since enhance OFF only reads that window, API docs).
2. **Resolution parity**: primary comparison at matched area (2K-class, 16:9). Optionally add a 16 MP 16:9 (5472×3072) H3 pass and downscale both models to a common delivery size (e.g. 2560×1440 or 3840×2160) for the final visual comparison — the community 16 MP→downscale doctrine (https://www.reddit.com/comments/1y3tdzk) says the downscale looks more natural than direct 2K.
3. **H3-specific settings stay ON and are recorded as H3 advantages**: the edit-mode trigger and int8_convrot quant (both documented H3-side fixes). Do not attempt to emulate them on Krea2.
4. **Seeds**: H3 seed is a re-run trigger only, not a determinism control (LOCAL node tooltip) — run **2–3 seeds per plate per model**, keep the best, and also note the "first-try success" rate as a fairness metric.
5. **No music / no-people note**: image plates carry no audio, so the NO-MUSIC rule is not triggered; keep plates faceless by design.

**What to compare (fixed scoring axes, 1–5 each, blind — strip filenames before scoring):**
- Prompt adherence (layout/camera/whitespace as written)
- Light physics & shadow plausibility (H3's claimed strength, https://www.reddit.com/comments/1xvesum)
- Grain/texture realism: genuine film-grain feel vs VAE smear/artifacts (failure mode #2)
- Color grade fidelity to the prompt's palette words
- Structure/geometry accuracy of the environment (props, architecture, no warped geometry)
- Cleanliness: no unwanted text/watermarks/overlays; top-quarter title space preserved
- "AI look": smoothing/oversharpening/plastic skin-or-surface artifacts
- Practical: iteration time per plate (H3 ~30–60 s at 16 MP on a 4070 Ti-class GPU per https://www.reddit.com/comments/1y3tdzk vs Krea2's 3-second-class renders per the same thread), and cost (local GPU time both sides; partner-node billing if the `MinimaxH3ImageNode` API path is used — 4K bills 16,777,216 image tokens, LOCAL `nodes_minimax.py`)

**Record for each cell**: prompt file, exact node settings + seed(s), `revised_prompt` (enhance-ON cells), output path, scores. Verdict per plate = which model wins on which axes; update `project-memory/EXPERIMENTS.md` + `CURRENT_TASK.md` in the same turn (project memory hard rule).

## Sources

**Fetch date for all sources: 2026-11-28** (stated store dates noted where later/earlier).

### Verdict / model overview
- https://huggingface.co/MiniMaxAI/MiniMax-H3-Image — official repo + sizes table (store metadata 2026-11-12/15)
- https://huggingface.co/Comfy-Org/MiniMax-H3-Image — ComfyUI-native weights (store 2026-11-12/15)
- https://huggingface.co/Abiray/MiniMax-H3-Image-GGUF — GGUF port (store 2026-11-16/17)
- https://huggingface.co/PrunaAI/P-H3-Image-Comfy — pruned port + P-H3 VAE (store 2026-11-08/11)
- https://x.com/MiniMax_AI/status/2120179737695826420 — official announcement (X store 2026-11-26)
- https://x.com/jiahao9527/status/2126532034038255624 — standard vs Highspeed variants, B.AI availability, 4K/20 MP/16-ref ceiling
- https://x.com/DidoofficialM/status/2126518882772877745 — lineup positioning (H3-Image = editing)
- https://x.com/DidoofficialM/status/2126519005523374147 — model links
- https://x.com/_0xIDARA/status/2126526994619810153 — B.AI API mechanics (t2i vs edit endpoints)
- https://www.minimax.io/blog/minimax-h3-image — official blog (speed/pricing)
- https://www.minimax-h3.app — video-model product page (HEARSAY snippet, video-model)
- https://www.minimax.io/h3-family — HEARSAY snippet (video-model family)

### Prompting style
- https://github.com/MiniMax-AI/MiniMax-H3-Image — README "Prompting Tips" + `skills/h3-image-prompt-writing/SKILL.md` + `references/t2i-en.txt`, `edit-en.txt`
- https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3-Image/main/showcase/real-world.md — official cinematic/documentary showcase prompts
- https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3-Image/main/showcase/game-worlds.md — official game-world/cinematic key-art prompts + title-space rule
- https://huggingface.co/MiniMaxAI/MiniMax-H3-Image-PE — PE system prompts (`prompt/t2i/`): ratio ladder, "cinematic does not determine orientation", orientation policy
- https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_minimax_h3_image_edit.json — edit-PE 3-part caption contract + official edit example
- https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3-Image/main/skills/h3-image-prompt-writing/references/edit-en.txt — reference-tag syntax (`@Picture 1` ≡ `<Picture 1>`)
- https://civitai.com/models/3045541 — base page "How to prompt it (tips from MiniMax)"
- https://huggingface.co/MiniMaxAI/MiniMax-H3-Image (README examples) — official short vs enhanced-caption T2I + edit examples
- https://www.reddit.com/comments/1xt9yzt — verbatim cinematic spaceship prompt + temperament quotes
- https://www.reddit.com/comments/1xwbo1h — long-prompt "phone photo" guidance + Fizgig training recipe + workflow links (pastebin/pixelailabs)
- https://www.reddit.com/comments/1xvesum — photographic-physics quotes, realism-LoRA convention, in-thread H3-video char-sheet mention [VIDEO MODEL]
- https://x.com/harboriis/status/2121947709406117898 — Seedream 5.5 vs H3-IMAGE A/B prompt (partial)
- https://x.com/SeaArt_Ai/status/2121830553049866439 — H3-IMAGE character + Seedance 2.5 motion pipeline (prompt in comments, not fetched)
- https://x.com/PrometheanAIX/status/2122119473603768344 — cinematic tone-variation usage
- https://x.com/opener_ai/status/2122130622646988913 — character expression collage
- https://x.com/PixelAigc/status/2121603585796706789 — Wong Kar-wai-style prompt [VIDEO MODEL — vocabulary only, NOT an H3-IMAGE result]
- https://x.com/ou_zhen599/status/2121674049634148854 + https://x.com/ou_zhen599/status/2121875591104545002 — R2V prompt examples [VIDEO MODEL]
- LOCAL: `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\h3image_*.json` — our own env-pilot/pose/world prompts

### Resolution & size
- https://platform.minimax.io/docs/api-reference/image-generation-h3-generations.md — 1K/2K/4K areas, custom size limits, ratio rules, enhance-off fixed-ratio rule, `min_generation_area`, 2K 16:9 = 2720×1536
- https://platform.minimax.io/docs/api-reference/image-generation-h3-edits.md — edit endpoint
- https://docs.comfy.org/tutorials/image/minimax/minimax-h3-image — native ~16 MP, template defaults, edit upscaling, 32-px edges, Resize node, 6-step sampling
- https://huggingface.co/MiniMaxAI/MiniMax-H3-Image#sizes — 16 MP size table
- https://github.com/MiniMax-AI/MiniMax-H3-Image (README) — request parameters, `size_for('5:4')` example
- https://www.reddit.com/comments/1xsqz2h — "recommended sizes" thread (no-1024, low internal resolution, 3072×2560 speed)
- https://www.reddit.com/comments/1y3tdzk — 16 MP→4K downscale, 4 MP softness, 6 MP edit ceiling, int8_convrot, speed
- https://www.reddit.com/comments/1xt9ocv — 20 MP quality ceiling, 48 MP counterpoint, Kijai sampler settings
- https://www.reddit.com/comments/1xu3dum — 100 MP @ 5090 (HEARSAY card title, store 2026-11-14)
- https://www.reddit.com/comments/1xvjsog — 60 MP editing (HEARSAY card title)
- LOCAL `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\comfy_api_nodes\nodes_minimax.py` — partner-node size widgets (512–7680 step 16), aspect list, billing areas

### LoRA & model shortlist
- Civitai (all fetched via public API 2026-11-28): https://civitai.com/models/3064644 (Outpaint), https://civitai.com/models/3059877 (pwni), https://civitai.com/models/3054448 (rurudo), https://civitai.com/models/3058358 (Better Hair), https://civitai.com/models/3064347 (Dark Fantasy), https://civitai.com/models/3062941 (Aurora), https://civitai.com/models/2924512 (Upscaler), https://civitai.com/models/3046048 (AIO), https://civitai.com/models/3051415 (uncensored vision), https://civitai.com/models/3049206 + https://civitai.com/models/3046576 (character sheets), https://civitai.com/models/3045966 (Pose Studio), https://civitai.com/models/3055836 (AIO 4–16 MP), https://civitai.com/models/3063091 (Panel), https://civitai.com/models/2833301 (Simple edit), https://civitai.com/models/3047310 (1girl T2I/I2I), https://civitai.com/models/3041484 (Fixed face), https://civitai.com/models/3053127 (17+ MP), https://civitai.com/models/3045867 / 3046884 / 3045918 / 3057968 (quants)
- [VIDEO MODEL]: https://civitai.com/models/2890588 (Cinematic V2), https://civitai.com/models/2908686 (Cinematic Look), https://civitai.com/models/2884206 (Photorealistic), https://civitai.com/models/3025511 (Enhancers), https://civitai.com/models/2837571 (Turbo)
- Non-H3 cinematic LoRAs (excluded from use): https://civitai.com/models/432586, 214956, 225364, 365274, 1249970, 520524, 290860, 290864, 541698, 2088559, 2477155, 2957855
- https://huggingface.co/akatz-ai/MiniMax-H3-Image-Character-Swap-LoRA (store 2026-11-26) · https://huggingface.co/supermansundies/Minimax-H3-Image-Pose-Transfer-Lora (store 2026-11-26) · https://huggingface.co/akhaliq/MiniMax-H3-Image-Character-Swap
- https://x.com/PhotogenicWeekE/status/2122043541027430821 (akhaliq repost + "video LoRAs don't work on image") · https://x.com/akatz_ai/status/2124202173143880172 (char-swap V1)
- https://github.com/shootthesound/Fizgig — training presets v9.6.0/9.7.0
- https://www.reddit.com/comments/1xufdvb — Fizgig likeness results · https://www.reddit.com/comments/1xvz8m9 — char-swap LoRA post (HEARSAY) · https://www.reddit.com/comments/1y05mo5 — Civitai model filter (HEARSAY)
- https://huggingface.co/ostris/ostris_h3_image_vae (+ X posts 2125689235558760633, 2125757126689825231)
- HEARSAY (HF store names only, 2026-11-26): tuanlai001/H3-IMAGE-PE-HERETIC-NVFP4-COMFYUI, Wuli-art/Gemma4-for-MiniMax-H3-Prompt-Extend, H3-Tiny/MiniMax-H3-Tiny-ComfyUI, lightx2v/Minimax-H3-Turbo-Fusion [VIDEO], ReDiverse/ReDiverse-MiniMax-H3 [VIDEO]
- https://www.reddit.com/comments/1y3tdzk — LoRA-experience quotes (base-model slop, training difficulty)

### enhance_prompt
- https://platform.minimax.io/docs/api-reference/image-generation-h3-generations.md — `disable_prompt_enhanced` default, fixed-ratio-when-off, edit-always-enhanced, `revised_prompt`, 4,096-token effective window
- https://github.com/MiniMax-AI/MiniMax-H3-Image (README) — 4,096-token server-side truncation
- LOCAL `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\comfy_api_nodes\nodes_minimax.py` — partner-node `enhance_prompt` widget/tooltips, edit-always-enhanced behavior, billing text-token ranges
- https://github.com/Comfy-Org/workflow_templates (t2i template) — `Boolean (Enable PE?)` default ON, PE model choice
- https://www.reddit.com/comments/1xuj7b9 — "Do not plug the image to the prompt enhancer" (only Reddit-verified enhance guidance)
- X: zero `enhance_prompt` mentions in fetched text (gap, documented in x_h3image.md §7)

### Failure modes
- https://www.reddit.com/comments/1xuj7b9 — crusty t2i, empty-image fix, KJ node, side effects (lines, step 4–5 pattern), P-H3 VAE, seeds_2
- https://www.reddit.com/comments/1xwbo1h — empty-image confirmation, LCM noise 0.9, int8_convrot, 1:15 speed, Qwen people-edit comparison
- https://www.reddit.com/comments/1y3tdzk — VAE detail criticism, face-transfer, LoRA experience, int8_convrot, speed, 16 MP downscale
- https://www.reddit.com/comments/1xvesum — VAE artifacting, non-film-grain textures, realism-LoRA convention
- https://www.reddit.com/comments/1xt9ocv — body horror, IP refs, 20 MP ceiling, noise-reduction with LCM
- https://www.reddit.com/comments/1xw0eb6 — identity under pose change, slop faces, Qwen comparisons, apology thread
- https://www.reddit.com/comments/1xsqz2h — low-res degradation, default-template resizing, VAE 2048 criticism
- https://civitai.com/models/3054448 — LoRA strength >2.0 degradation
- https://x.com/jacl0e/status/2126519210738065813 + https://x.com/NiiColaVT/status/2126247015415730481 — "No loras on h3", Krea 2 filter-bypass LoRA, [VIDEO MODEL] turbo/FL/ref2va + edge-fraying
- API docs (above) — no negative prompt, non-idempotent streaming, license

### A/B protocol
- LOCAL: `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\h3image_t2i_env_pilot.json` (our H3 side baseline), `d:\models\vsCodeMcp\prompts\` (plate prompt sets)
- Resolution/quality anchors: https://platform.minimax.io/docs/api-reference/image-generation-h3-generations.md (2K 16:9 = 2720×1536), https://www.reddit.com/comments/1y3tdzk (16 MP→downscale, speed), https://www.reddit.com/comments/1xuj7b9 (edit-mode trigger)

**[VIDEO MODEL] sources (adjacent context only, not H3-IMAGE):** https://www.reddit.com/comments/1xvesum (char-sheet workflow claim), https://x.com/ou_zhen599/... (R2V prompts), https://x.com/jacl0e/... + https://x.com/NiiColaVT/... (H3-video + Krea 2 pipeline), https://www.minimax-h3.app (HEARSAY), Civitai V1–V5 LoRA pages above, Reddit card-tier titles (1xu3dum etc. as listed).
