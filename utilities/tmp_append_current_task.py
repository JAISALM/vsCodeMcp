import io
f = r"D:\models\vsCodeMcp\project-memory\CURRENT_TASK.md"
lines = io.open(f, encoding="utf-8").read().split("\n")
idx = next(i for i, l in enumerate(lines) if "leaner 2MP set" in l or "char-LoRA 2MP set" in l)
print("anchor at index", idx)
block = """- **PROMPT WIRING FIX + CORRUPT FILE FOUND (D181):** user: "i didnt even ran
  krea2_t2i_face / image_krea2_turbo_t2i because the prompt is bad/old ... the
  prompt update and wiring update youre doing is not working properly fix that
  goddamint ... just give me workflow names and i will generate." Root cause:
  the 5 good 2MP images (krea2_t2i_face_00013..17) came from CORRUPT archived
  file workflows_archive\\2026-10-18\\krea2_t2i_character.json - prompteach EMPTY,
  pos encode empty, VAEDecode + FameGridColorFinish MISSING (but 1152x2048,
  realism@1.0 + famegrid@0.7, 10/cfg1, neg = plastic/waxy skin list). Images were
  made with prompts PASTED INTO CANVAS, not from the file. **NEW PERMANENT RULE:
  all test workflows = one KSampler branch per prompt, each with a VISIBLE
  CLIPTextEncode holding the text - NO prompteach, nothing to paste.** Rebuilt
  `krea2_realism_2mp.json` (0/0, 37 nodes/57 links): old recipe verbatim, 6
  visible-prompt branches, 1152x2048, seeds 42-47, neg = plastic/waxy list.
  HANDOFF LIST (names only, open fresh tab, queue): krea2_realism_2mp (main A/B),
  krea2_official_char_test, krea2_control_test. Every handoff: dump the file's
  text widgets and confirm prompts on disk BEFORE telling user it's ready."""
lines = lines[:idx+1] + block.split("\n") + lines[idx+1:]
io.open(f, "w", encoding="utf-8").write("\n".join(lines))
print("inserted; total lines now", len(lines))
