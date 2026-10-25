import io

ct_add = """
### 23:3x IST - weather_v3 (4MP concrete-rain) + face_lock_v2 (denoise 0.35) - WIN
- User feedback on v2 frames: "somewhat okayish... rain droplets don't feel natural" +
  "dont rely on the outputs, just check the notes" + "stick to the other posts i shared"
  (community recipes, not guesses). E:\\Krea2 4.6GB download COMPLETED (2150 images,
  4.7GB). Read NOTES.md 348-round distill + SUMMARY.md.
- **Notes recipes applied:** concrete nouns win over poetic; weather+light = Krea2's best
  trick; native 4MP finals ("looks shot, not rendered"); rain realism = CONCRETE water
  cues (rain streaks in the air, droplets beaded on hair/skin catching the light, wet
  asphalt mirror reflections, droplets in lamp beams); identity drift is expected (seed
  locks layout not face); i2i face-lock at denoise 0.5 RE-RENDERED the rain (fake
  stippled droplets) -> drop to 0.35 to preserve the canvas's natural rain.
- **weather_v3** (krea2_weather_v3.json): krea2_turbo_fp8_scaled + turbo LoRA 0.7 +
  Krea2-realism-V2 0.8 + NegPiP, 12 steps cfg 1 er_sde/simple, NATIVE 4MP 2560x1440,
  6 branches (street x3 seeds 201-203 + monsoon x3 204-206), concrete-rain prompts.
  Run 80037527. WINNERS: street_b (80037527_000) + monsoon_b (80037527_004) - face
  close to Jaisal, NATURAL rain (streaks in lamp beams, droplets on skin/hair, wet
  reflections). The concrete-noun rain fixed the "unnatural droplets" complaint.
- **face_lock_v2** (krea2_face_lock_v2.json): i2i denoise 0.35 (preserves canvas
  rain/pose), ref_boost 4.0, face-ONLY prompt ("change only the face"), 10 steps
  euler/simple cfg 1, turbo fp8 + identity LoRA 1.0. Street face-lock =
  data\\face_lock_v2_run\\be651d88_000.png; monsoon face-lock =
  data\\face_lock_v2_run\\97aed4e5_000.png. Both: face pulled to Jaisal, natural rain +
  pose + scene fully preserved, no seam.
- **NEW CANONICAL JAISAL MOVIE FRAMES (4MP):** street = be651d88_000, monsoon =
  97aed4e5_000. Backwater wide (B1) still on old 2MP e6b8ea11_000 -> needs same
  weather_v3 treatment (concrete mist/water cues) + face_lock_v2.
- TODO: user verdict on the 2 new finals -> backwater v3 4MP -> Zidhan face (UNLOCKED)
  same 2-pass -> anchor sets -> MiniMax H3 R2V (NO music D041). Deadline Nov 22.
"""
p = r"D:\models\vsCodeMcp\project-memory\CURRENT_TASK.md"
with io.open(p, "a", encoding="utf-8") as f:
    f.write(ct_add)
print("CURRENT_TASK.md appended")

ex_add = """
## 2026-10-23 (2) - weather_v3 4MP concrete-rain t2i + face_lock_v2 (denoise 0.35)

**Goal:** fix "rain droplets don't feel natural" + face identity, per the community
knowledge base (NOTES.md 348-round distill from the user's 2000-image thread + the
reddit realism posts), not by guessing.

**Config:**
- t2i pass 1 = `krea2_weather_v3.json`: krea2_turbo_fp8_scaled UNET +
  krea2_turbo_lora_rank_64 0.7 + Krea2-realism-V2 0.8 + ApplyKrea2NegPiP, 12 steps
  cfg 1 er_sde/simple, NATIVE 4MP (2560x1440), 6 branches (street x3 seeds 201-203,
  monsoon x3 204-206). Prompts = concrete rain cues: "distinct rain streaks falling
  through the light, water droplets on his wet hair and beard, wet black asphalt with
  mirror reflections of the lamps, thin mist at ground level" (street); "individual
  raindrops in the air and beaded on his wet hair and along the beard, a few drops
  catching the overcast light" (monsoon).
- i2i pass 2 = `krea2_face_lock_v2.json`: canvas = best t2i frame (VAEEncode), face
  ref = jaisal_face_locked.png (VAEEncode -> Krea2EditModelPatch slot 2), ref_boost
  4.0 / ref_boost_a 1.0 off, grounding 768, KSampler denoise 0.35 (changed from 0.5),
  10 steps cfg 1 euler/simple, turbo fp8 + identity LoRA 1.0. Prompt = face-only
  ("change only the face", keep everything else exactly).

**Result (run 80037527 t2i; be651d88 + 97aed4e5 face-locks):**
- street_b (80037527_000) + monsoon_b (80037527_004) = winners: face close to Jaisal,
  NATURAL rain (streaks in lamp beams, droplets on skin/hair catching light, wet
  asphalt mirror reflections, mist).
- face_lock_v2 outputs: data\\face_lock_v2_run\\be651d88_000.png (street) +
  97aed4e5_000.png (monsoon) - face pulled to Jaisal (rounder face, shorter wavy hair,
  sparse beard) while the t2i's natural rain/pose/scene fully preserved, no seam.
- denoise 0.35 (vs 0.5) = the fix: 0.5 re-rendered the rain into a fake stippled
  texture; 0.35 preserves the canvas rain and only pulls the face.

**Conclusion:** the 2-pass pipeline at 4MP with concrete-noun rain cues + denoise 0.35
face-lock is the locked recipe for Jaisal movie frames. New canonical frames:
street = be651d88_000, monsoon = 97aed4e5_000.

**Next:** user verdict on the 2 finals -> backwater wide (B1) same treatment (it is
still old 2MP e6b8ea11_000) -> Zidhan (UNLOCKED) same 2-pass -> anchor sets ->
MiniMax H3 R2V (NO music D041). Deadline Nov 22.
"""
p2 = r"D:\models\vsCodeMcp\project-memory\EXPERIMENTS.md"
with io.open(p2, "a", encoding="utf-8") as f:
    f.write(ex_add)
print("EXPERIMENTS.md appended")
