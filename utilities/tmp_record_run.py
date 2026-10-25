import io

# EXPERIMENTS.md
f = r"D:\models\vsCodeMcp\project-memory\EXPERIMENTS.md"
lines = io.open(f, encoding="utf-8").read().split("\n")
idx = next((i for i, l in enumerate(lines) if "MU_TEST FAILURE FORENSICS" in l), None)
if idx is None:
    idx = len(lines) - 1
block = """
## 2026-10-23 - krea2_realism_2mp file-driven run (MCP, no paste)
- **Goal:** verify old recipe end-to-end from FILE (no canvas, no paste): turbo fp8 +
  Krea2-realism-V2@1.0 + famegrid@0.7 + FameGridColorFinish(1.0/0.6), 10/cfg1/euler/
  simple, 1152x2048, 6 long candid-snapshot prompts, 6 visible-CLIPTextEncode
  branches (seeds 42-47).
- **Result:** 6/6 completed (prompt 2ca0eafc-3fb3-4bb2-b9b7-619d46c9fee0), outputs in
  data\\realism_2mp_run\\ (001=p1 backwater path, 004=p2 houseboat, 002=p3 monsoon
  street, 003=p4 campus, 000=p5 temple, 005=p6 auto-rickshaw). Identity CONSISTENT
  across all 6 (same man: wavy hair down, round young face, sparse beard, dark tee) -
  face matches D171 lock better than the char-LoRA set. Quality = amateur-phone-shot
  realism (real pores, natural light) - matches the "better" old set the user
  referenced. Minor: stray-hair artifacts (frames 1/5), slight inter-frame face
  softness drift (t2i, no ref lock).
- **Conclusion:** the recipe (realism + famegrid + finish + long-text identity) is the
  quality baseline - the missing ingredient in recent runs was the recipe, not the
  resolution. File-driven MCP runs work end-to-end (prompts applied from file, no
  canvas state involved). Next: user picks 3 anchor frames (suggested: 002 frontal +
  004 profile + 000 temple), face-lock via identity-edit, then R2V per shot.
"""
lines = lines[:idx+1] + block.split("\n") + lines[idx+1:]
io.open(f, "w", encoding="utf-8").write("\n".join(lines))
print("EXPERIMENTS.md updated")

# CURRENT_TASK.md
f2 = r"D:\models\vsCodeMcp\project-memory\CURRENT_TASK.md"
lines = io.open(f2, encoding="utf-8").read().split("\n")
idx = next(i for i, l in enumerate(lines) if "confirm prompts on disk BEFORE telling user it" in l)
block = """- **RUN COMPLETE (D181 follow-up):** agent RAN krea2_realism_2mp itself via MCP
  (prompt 2ca0eafc-3fb3-4bb2-b9b7-619d46c9fee0) - 6/6 outputs in
  data\\realism_2mp_run\\, identity consistent across all 6, face matches D171 lock,
  quality = the "better" old-recipe look. File-driven runs work end-to-end (no
  canvas/paste). AWAITING USER: (1) pick 3 anchor frames (suggested 002/004/000),
  (2) confirm this face = Jaisal final face (settles D172). Then: face-lock anchors
  (identity-edit) -> R2V per shot. Resolution chase CLOSED per user."""
lines = lines[:idx+1] + block.split("\n") + lines[idx+1:]
io.open(f2, "w", encoding="utf-8").write("\n".join(lines))
print("CURRENT_TASK.md updated")
