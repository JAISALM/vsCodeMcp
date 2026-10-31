# Open Source Higgsfield challenge — results catalog (captured 2026-10-31)

Source: `jutsuhq/open-source-higgsfield` (55★, CC0, maintained by Jutsu Studio) +
reddit r/comfyui 1xjdalp (u/Visual_Tiger_2400): "90 open-source apps in two weeks".
Full machine list: `projects.json` (this dir). Category split: 24 all-in-one studios ·
15 camera/reshoot/previs · 13 character swap · 10 film/music-video · 9 effects ·
8 canvas/front ends · 7 ads/UGC · 4 character/dataset · 6 older alternatives.

## Challenge facts
- Announced 2026-10-16 by ComfyUI: "Higgsfield promised to open-source their platform.
  They didn't." $25K prizes (Comfy + NVIDIA + RunPod + MiniMax). Tracks: Cinematic
  Studio, Re-shoot a video, Openjutsu (character swap).
- 10-26: Comfy team's own entry **OPENjutsu** (D3voz/openjutsu, 656★, MIT — Genjutsu-style
  character/object swap, hair/clothes change, object removal, person relocation) +
  **comfy-openjutsu** (Comfy-Org, 68★ — clonable app template, 5–15 s clips).
- 10-29: **Higgsfield sent ComfyUI a cease-and-desist** demanding the challenge shut down.
- 10-30: submission deadline. Winners announced **11/6**.
- Our D134/D135 entry ("Story-Short" → "character-consistent short app",
  `challenge\consistent-short\`, obvpm-timeline, smoke test passed 10-18) was
  **DROPPED before submission — NOT in the 90-project catalog** (user-confirmed).

## Top of the catalog (by stars)
| Project | Stars | What |
|---|---|---|
| D3voz/openjutsu (OPENjutsu) | 656 | Comfy team's Genjutsu character/object swap |
| jtydhr88/ComfyArt | 405 | tldraw design canvas + design agent, local image/video/audio/3D |
| roadmaus/ComfyUI-Continuity | 138 | One node: prompt + @media → Render; 6 model families, all local |
| wexloops/openfield | 116 | Studio for video/stills/3D; every app = workflow + screen; open weights only |
| raph651/open-source-canvas | 89 | Node canvas running ComfyUI workflows |
| Comfy-Org/comfy-openjutsu | 68 | Official clonable character-swap app template |
| thePloggy/CreatorOS-Studio | 42 | One recurring character: one-line brief → finished reel (≈ our dropped Story-Short) |
| szprivate/agentY | 39 | Agent inside ComfyUI: describe → picks/builds workflow → runs; Ollama-local |
| Bambushu/h3-recast | — | **MiniMax H3 + BFS LoRA: swap up to 3 people in one pass**, motion/set/audio kept, optional FaceRefine lip pass, **16 GB VRAM + 64 GB RAM (fits our 32/66)** |
| Lightricks/LTX-Desktop | — | Official LTX local desktop app (beyond-challenge) |
| codyclack/opensfield | — | 146 Higgsfield tools in one app |

## Shortlist relevant to OUR movie pipeline
**Character / identity (D137):**
- `Bambushu/h3-recast` — H3 3-person swap with BFS LoRA + FaceRefine lip pass (reddit 1x9n0dl)
- `ToxicLizard99/Dataset-Forge` — "one face in, a full character LoRA dataset out" → our `lora_dataset_*` workflow
- `ZhuEvgeny/Character-lock-comfy` — "one reference image in, a locked character look out" → our krea2_identity_edit territory
- `fixed-42/comfyui-sameface` — node that measures where an edit moved face parts and moves them back
- `lvsas/OpenJutsuStudio` — characters into real footage; **reopens an H3 take to continue the story**; before/after reels

**Film / story (episode1):**
- `smithysw7/openreel` — one logline in → character-consistent short film out
- `bgstratt/seriesmith` — series config + markdown episode scripts in → finished episodes out, any shot on any model, local or Comfy cloud (≈ our `episode1\` pipeline)
- `thePloggy/CreatorOS-Studio` — camera moves, effects, talking avatars, motion transfer, video editor around ONE recurring character

**VFX (D169 LTX-2.5 pipeline):**
- `Zitroffi/comfyui-element-forge` — LTX-2.5 generates fire/lightning/smoke/particles, then TRACKS/LIGHTS/LAYERS them into real footage, stays editable
- `Kainotomic/one-take-vfx` — disintegrate/levitate/fire/portal/time-freeze on phone clips, LTX 2.5
- `TusharTechs/platelock` — plate-preserving VFX: add effect, keep original shot
- `jdnichollsc/seam` — two shots in → one AI transition out (smoke/water) → our shot-to-shot transitions
- `LaytonGott/open-cinema` — change the lens/DoF AFTER the render (LTX-2 + physically based DoF)

**Camera / QA:**
- `Tekholms-LW/ReAngle` — re-shoot any video from a new angle (LTX-2.5)
- `junco3/motion-guard` — checks AI video against its 3D motion reference BEFORE expensive upscale
- `soft-jelly/shotcheck` — CPU-only camera-motion checker (match/mismatch/inconclusive)
- `MVOlekhno/previz2shot` — Blender grey playblast → finished shot (FLUX.2 Klein + LTX-2.5)

**Studios / canvas:**
- `dougliell/Cheapsfield` — fully local Windows Higgsfield-style studio
- `crystalattice/CBI_RenderRepo` — local-first workflow package manager (discover/inspect/install while reusing your models/nodes)
- `doubletwisted/ComfyUI-Spool` — video timeline: queue per clip, review takes, assemble sequence (obvpm-adjacent)

## Takeaways (user: "lots of people pay closed-model subscriptions and build easily — compare")
1. **What paid Higgsfield users get that we now get open:** Genjutsu character swap (OPENjutsu 656★), one-tap VFX presets (element-forge/one-take-vfx), camera re-shoots (ReAngle/open-cinema), studio UIs (ComfyArt/opensfield/Comfield).
2. **Nobody in the catalog runs a persistent local LLM brain + ComfyUI swap** — the "agents" (agentY, Vision Orchestrator) are cloud-LLM or in-canvas Ollama; our Qwen-27B-brain topology is still unique (llama-swap/berth territory).
3. **Directly stealable ideas for episode 1:** h3-recast's BFS face-Lora-on-H3 + FaceRefine lip pass (we already hold BFS head LoRAs) · Dataset-Forge (auto LoRA datasets from one face — our tonight's dataset runs) · seriesmith (episode scripts → shots) · seam (AI transitions between our shots) · element-forge (editable LTX VFX on our plates) · shotcheck/motion-guard (QA before the upscale pass).
4. **D041 check:** several film/music-video entries are music-video-centric (Mondo Music Video, Xenoform) — their pipelines bake in score; any borrowed workflow MUST get the NO-music rule injected first.
5. **Winners 11/6** — check the list repo again after that date (stats refresh via `node scripts/build.mjs`).
