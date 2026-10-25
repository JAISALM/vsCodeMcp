import io
base = r"D:\models\vsCodeMcp\project-memory"

exp = """
## 2026-10-23 - krea2_cine_v2 community recipe + 2-pass face lock (e6b8ea11, 20cc281e)
- **Context:** user REJECTED all 3 cine-max frames (3f88a7c2): "head looks cropped
  and pasted on a body, body proportion wrong, no realism". User pointed to the
  community knowledge base (E:\\Krea2\\notes - 348-round/2100-image notes + 2-pass
  workflow + identity-edit v1.2 screenshot) and ordered "loop engineering".
- **Root cause found:** the cine-max identity t2i (Krea2EditModelPatch ref_boost 4.0
  + empty canvas + denoise 1.0) hard-copies the reference FACE onto a freshly
  generated body/pose -> face orientation/crop never matches the new pose = the
  "pasted head" look. Identity t2i is an insert-person tool, NOT a face-harmonizer.
- **Community recipe (from E:\\Krea2\\notes, verified):** UNET krea2_raw_bf16 +
  LoRA krea2_turbo_lora_rank_64_bf16 @0.7 + Krea2-realism-V2 @0.8 (trigger r3alism,
  explicit clothing in prompt - NSFW checkpoint), VAE krea2RealVae_v10, CLIP
  qwen3vl_4b_fp8_scaled, 12 steps cfg 1 er_sde/simple, 2MP, ApplyKrea2NegPiP
  [1.0,false,0,27,1] in model chain, negative = ConditioningZeroOut (no neg text at
  cfg 1), prompting = medium first then subject then light, verbatim character
  clause in every shot. KSamplerSelect/SamplerCustom NOT needed.
- **Run e6b8ea11 (krea2_cine_v2.json, 3x 2MP 16:9):** data\\cine_v2_run\\ (000 =
  backwater wide, 001 = dusk street wide, 002 = monsoon close-up). QUALITY NOW
  EXCELLENT (real rain/mist/light, film grain, natural bodies, ZERO pasted-head
  look - face generated with the body). COST: face DRIFTED from the locked face
  (t2i limitation - notes confirm description locks archetype not person).
- **Face-lock i2i (20cc281e, krea2_face_lock.json):** i2i pass on the t2i frame:
  canvas = t2i frame (VAEEncode -> KSampler latent, denoise 0.5), face reference =
  jaisal_face_locked.png (VAEEncode -> Krea2EditModelPatch slot 2, ref_boost 2.5,
  ref_boost_a 1.0 off, fit_mode fit, source_image_b pixel path, grounding_px 768,
  turbo fp8 + identity LoRA 1.0, 10 steps cfg 1 euler/simple). Result
  data\\face_lock_run\\20cc281e_000.png: face pulled back toward Jaisal (rounder
  youthful face, shorter wavy hair, sparse beard) while pose/rain/background/T-shirt
  preserved, no seams. THE 2-PASS PIPELINE WORKS.
- **Pipeline decided (2-pass):** pass 1 = community-recipe t2i (natural scene),
  pass 2 = i2i face lock (denoise 0.5, ref_boost 2.5-3.5) on the chosen frame.
  Tune ref_boost up (3.0-3.5) for tighter face match if needed; can chain pass 2
  twice. 4MP ceiling: RAW bf16 26GB on 32GB VRAM = OOM-risky at 4MP; 2MP safe
  (community ran 4MP on int8 13GB / 24GB card).
- **Workflow files:** workflows\\krea2_cine_v2.json (3 branches),
  krea2_cine_v2_4mp.json (unrun - OOM risk), krea2_face_lock.json.
- **Status:** quality bar met for t2i; face-lock pass 1 accepted (needs user
  confirmation). Next: user verdict on face-lock frame -> tune/chain -> run all
  3 scenes through 2-pass -> Zidhan.
"""

with io.open(base + r"\EXPERIMENTS.md", "a", encoding="utf-8") as f:
    f.write(exp)

cur = """
## 2026-10-23 - quality loop (user back from isha)
- cine_v2 community-recipe t2i (e6b8ea11): quality fixed, pasted-head gone, face
  drifted. Face-lock i2i (20cc281e) pulls face back to Jaisal, scene preserved.
- E:\\Krea2 4.6GB image download STALLED at 1.5 MB after ~15 min - user to restart.
- 2-pass pipeline is the new anchor recipe (see EXPERIMENTS 2026-10-23 entry).
- TODO: user verdict on 20cc281e_000 (face-lock frame) -> tune ref_boost if
  needed -> all 3 scenes through 2-pass -> Zidhan face -> anchor sets.
"""
with io.open(base + r"\CURRENT_TASK.md", "a", encoding="utf-8") as f:
    f.write(cur)
print("memory updated")
