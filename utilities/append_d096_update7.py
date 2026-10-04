import io

p = r'd:\models\vsCodeMcp\project-memory\DECISIONS.md'
s = open(p, encoding='utf-8').read()
anchor = 'Inpaint only works when the region is small/localized.**'
i = s.find(anchor)
assert i > 0, 'anchor not found'
i += len(anchor)

new = """

### D096 update 7 — small-mic end ref = Krea2 IDENTITY EDIT v1.2 (user-chosen, supersedes update 6 t2i) (2026-09-28)
- **User rejected t2i-from-scratch:** "this is the reason why i was against creating newly, it completely misses out the basic... we need to give the base image and then do the I2I with identity... the current one has lots of changes especially the table environment etc, keep the identity transfer workflow, don't forget things." t2i threw away the scene (table, papers, chair, bulb, composition).
- **CORRECT TOOL = Krea2 Identity Edit v1.2** (`krea2_identity_edit.json`): takes the BASE image (`mic+paper.png`) and regenerates it keeping the scene identity, applying only the instruction. **Built `krea2_identity_edit_small_mic.json` via `utilities/build_krea2_identity_small_mic.py` (clones `krea2_identity_edit.json`, validates clean 0 errors/0 warnings, 15 nodes):** node 72 LoadImage = `mic+paper.png` (base scene); node 84 = instruction ("Make the microphone SMALL and COMPACT, on a SHORT LOW stand... ONLY ONE microphone... Keep EVERYTHING ELSE exactly the same: papers, table, empty chair, bare bulb, black void, B&W cinematic. Preserve the entire original image exactly. No other changes. No people."); node 85 = negative ("large/tall mic, two mics, color, people, extra objects..."); node 29 SaveImage = `jaisal_cut/mic_small_id`; node 95 (Typnosis typography LoRA) BYPASSED (mode 4, not needed for a mic edit). **Kept the proven identity params:** node 79 `Krea2EditModelPatch` ref_boost=4 (fidelity dial) fit_mode=fit, node 83 `ResolutionSelector` 16:9 2MP, node 53 KSampler 10 steps cfg 1 euler/simple denoise 1, node 71 `LoraLoaderModelOnly` `krea2_identity_edit_v1_2.safetensors` @1.0, UNET `krea2_turbo_fp8_scaled.safetensors`, CLIP `qwen3vl_4b_fp8_scaled.safetensors` type `krea2`, VAE `qwen_image_vae.safetensors`. All krea2edit nodes confirmed LIVE in `/object_info`; identity LoRA present.
- **RULE: to change ONE attribute of a scene while keeping the scene (table/papers/chair/bulb/composition), use the Krea2 Identity Edit v1.2 workflow (base image in node 72 + plain-English instruction in node 84, ref_boost=4) — NOT t2i-from-scratch (loses the scene) and NOT inpaint (region-shape prior). This is the project's standard scene-preserving edit tool (D023).**
"""

s = s[:i] + new + s[i:]
open(p, 'w', encoding='utf-8').write(s)
print('DECISIONS.md updated with D096 update 7')
