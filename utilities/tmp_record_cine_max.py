import io

# EXPERIMENTS.md - after the krea2_realism_2mp entry
f = r"D:\models\vsCodeMcp\project-memory\EXPERIMENTS.md"
lines = io.open(f, encoding="utf-8").read().split("\n")
idx = next(i for i, l in enumerate(lines) if "R2V per shot." in l)
block = """
## 2026-10-23 - krea2_cine_max (cine-max stack, face-locked, 2K)
- **Goal:** top-quality Krea2 cinematic frames, face-locked to the final Jaisal
  face (krea2_realism_2mp_4, D172 resolved), "push limits to max on 5090".
- **Config (krea2_cine_max.json, validated 0/0):** turbo BF16 (not fp8) +
  Krea2 identity-edit LoRA @1.0 + Krea2_Cinematic_Artstyle @0.8 + Krea2T-
  Enhancer-Advanced (text_scale 1.5) + Krea2EditModelPatch (source_image+VAE
  blur-proof path, ref_boost 4, fit) + Krea2TurboReferenceSigmaSchedulerFrom-
  Latent (official mu=1.15, 8 steps) -> SamplerCustom + KSamplerSelect(euler),
  2048x1152 16:9, 3 cinematic briefs (35mm/50mm/40mm film-still style), neg =
  plastic/waxy-skin list. Ref: input\\jaisal_face_locked.png.
- **Result:** 3/3 completed (prompt 3f88a7c2-9f84-4fca-846f-7d09b4aafb12) in
  data\\cine_max_run\\ (000 = golden-hour backwater 35mm, 002 = monsoon close-up
  50mm, 001 = dusk street 40mm). Face HELD in all three (closest match in the
  close-up). 2K 16:9 HD, cinematic grade, real skin texture - the best Krea2
  output on this system to date.
- **Wiring lessons:** KSamplerAdvanced has NO sigmas input here - use
  SamplerCustom (model/positive/negative/sampler(SAMPLER)/sigmas(SIGMAS)/
  latent_image; widgets [add_noise, noise_seed, cfg]); sampler input MUST come
  from KSamplerSelect (the only core SAMPLER-output node); TEnhancer class name
  is HYPHENATED (Krea2T-Enhancer-Advanced). Krea2EditGroundedEncode = the
  Krea2-edit CLIP encode (clip + image + image_b + prompt/grounding_px/
  system_prompt).
- **Conclusion:** the cine-max stack is the anchor-frame recipe for the movie.
  Next: Zidhan face lock, anchor sets per character, R2V."""
lines = lines[:idx+1] + block.split("\n") + lines[idx+1:]
io.open(f, "w", encoding="utf-8").write("\n".join(lines))
print("EXPERIMENTS.md updated")

# CURRENT_TASK.md - after the RUN COMPLETE note
f2 = r"D:\models\vsCodeMcp\project-memory\CURRENT_TASK.md"
lines = io.open(f2, encoding="utf-8").read().split("\n")
idx = next(i for i, l in enumerate(lines) if "settles D172" in l)
block = """- **D172 RESOLVED + CINE-MAX STACK (D182):** user picked krea2_realism_2mp_4
  (campus frontal) as Jaisal's FINAL face (v2 proposal closed). Built + ran
  krea2_cine_max.json (0/0): turbo BF16 + identity-edit + Cinematic_Artstyle@0.8
  + TEnhancer(text_scale 1.5) + Krea2EditModelPatch blur-proof path + OFFICIAL
  turbo sigma schedule (pack node) + SamplerCustom, 2048x1152 16:9, 3 cinematic
  briefs - 3/3 frames in data\\cine_max_run\\, face held in all 3. This is the
  anchor-frame recipe. NEXT: Zidhan face lock -> anchor sets -> R2V (no music)."""
lines = lines[:idx+1] + block.split("\n") + lines[idx+1:]
io.open(f2, "w", encoding="utf-8").write("\n".join(lines))
print("CURRENT_TASK.md updated")
