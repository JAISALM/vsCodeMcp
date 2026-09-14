# Audio & Lip-Sync Pipeline Plan (Draft, 2026-09-06)

## VOICE PIPELINE DECISION — VC FOR MOVIE, TTS FOR FUTURE (2026-09-08, D050)
**USER DECISION (2026-09-08):** For the **15-character bilingual movie**, use **VOICE CONVERSION (VC), NOT TTS**. The user performs ALL 15 characters' dialogue themselves (alone in the project, has the script). VC preserves the user's performance (emotion, timing, Malayalam pronunciation) and only changes the voice identity (timbre). For **future kids videos** (where natural voice isn't needed), use **TTS** (IndicF5/S2 Pro).

**WHY VC (not TTS) for the movie:** TTS (Fish S2 Pro) Malayalam output sounds non-native (Tamilian accent, flat flow) — a general multilingual model approximating Malayalam. VC sidesteps that: the USER speaks the Malayalam (correct pronunciation, natural emotion), and the VC tool just changes the voice color. User: "without it it feels like we are doing some blind translation... 15 voice overs i can do that because only i have the script."

**VC tool: RVC (primary) over OpenVoice (fallback).** RVC preserves prosody (rhythm, pitch contour, emotion) while changing only timbre. OpenVoice is a pure timbre swap that keeps the user's skeleton (confirmed: output "still sounds like me"). RVC trains a per-character model from 10+ min clean audio.

**TWO-TRACK SYSTEM:**
| Track | Tool | Use case |
|-------|------|----------|
| **VC (movie)** | RVC (primary) / OpenVoice (fallback) | 15-character movie — user performs, VC changes voice |
| **TTS (future)** | IndicF5 (ML) / Fish S2 Pro (multilingual) | Kids videos, content where natural voice not needed |

**RVC SETUP (2026-09-08):** repo cloned to `D:\models\ai-movie\repos\rvc-webui` (RVC-Project/Retrieval-based-Voice-Conversion-WebUI). **Requires Python 3.12** (requirements = `requirments_cu128_py312.txt`). Setup script `scripts\setup_rvc.ps1` creates venv `envs\rvc` (py3.12) + installs torch 2.7.1+cu128 (RVC needs torch <2.8) + all deps. **RVC workflow (per character):** (1) 10+ min clean target-voice audio → (2) train RVC model (F0 via RMVPE + HuBERT + FAISS index) → (3) user dubs lines → (4) `clean_audio.py` → (5) RVC convert → (6) LatentSync → DaVinci. **Key params:** `--f0_method rmvpe`, `--protect 0.3-0.5`, `--alpha 0.1-0.2`. **Reference audio for Midhun:** `D:\models\ai-movie\references\mithun\` (5 clean clips, 56-124s each — enough for training).

**RVC vs OpenVoice (both already have the user's dub pipeline):** OpenVoice = zero-shot (no training, `convert_character.py`), RVC = trained (per-character model, higher quality ceiling). **Start with RVC for the movie; keep OpenVoice as the fast zero-shot fallback.**

## MALAYALAM TTS A/B COMPARISON (2026-09-08, PARKED — both TTS tools working, RVC is the movie path)
**STATUS (2026-09-08, user-confirmed):** **BOTH TTS TOOLS NOW WORKING + PARKED.** The movie voice path is **RVC VC (D050)**, NOT TTS. IndicF5 and Fish S2 Pro are functional and available for **future kids-content / non-Malayalam TTS** use. Do NOT re-invest in TTS for the movie.

**Models in the A/B:**
| Model | Malayalam focus | Midhun's voice | Status |
|-------|----------------|----------------|--------|
| Fish S2 Pro | 80+ multilingual (approximates ML) | ✅ zero-shot ref | ✅ WORKING → `fishs2_chennai_mithun.wav` (262 tok, 22.84 GB VRAM). Malayalam sounds non-native (Tamilian accent) — fine for non-ML content, NOT for the movie. **PARKED.** |
| IndicF5 (ai4bharat) | 11 Indian langs, ML-native | ✅ ref audio | ✅ WORKING → `indicf5_direct_test.py` + 8s ref (`MITHUN_AUDIO_MALAYALAM_2_ref8s.wav`). Reference-bleed fixed by using a short (8s) ref. **PARKED** (movie uses RVC). |
| Sarvam Bulbul v3 | Indian-language focused, `ml-IN` | ❌ stock voices (shubh/pooja) | 📝 script ready (`sarvam_bulbul_chennai_test.py`). Cloud API, needs `SARVAM_API_KEY`. **DEPRECATED** (user rejected cloud). |
| Sarvam Dubbing | Indian-language, `voice_cloning=true` | ✅ preserves speaker identity | 📝 separate experiment. **DEPRECATED** (cloud). |

**IndicF5 working recipe (2026-09-08):** `indicf5_direct_test.py` (bypasses transformers — fixes the meta-device crash) + **8s reference** (`MITHUN_AUDIO_MALAYALAM_2_ref8s.wav` + `_ref8s_transcript.txt`). **KEY LESSONS:** (1) F5-TTS `infer_process` is designed for refs ≤25s — a 42s ref makes `max_chars` negative → chunking breaks → ~3s output. (2) A SHORT reference (8s) reduces reference-content bleed into the generated line. (3) `sf.read(always_2d=True)` returns `(frames, channels)` — duration is `shape[0]/sr`. (4) `infer_process` reads the ref via `soundfile` (patched from `torchaudio.load`).

**KEY LEARNING (2026-09-08):** Fish S2 Pro's Malayalam output sounds non-native (Tamilian accent, flat flow) — it's a general multilingual model approximating Malayalam, NOT a native-ML model. **Do NOT spend time forcing S2 Pro to sound native.** For the movie, **RVC VC** (user performs, VC changes voice) is the path.

**Scripts (all in `D:\models\ai-movie\scripts\`):**
- `indicf5_chennai_test.py` — real IndicF5 (loads by repo id `ai4bharat/IndicF5` from HF cache; dynamo disabled). Run: `run_indicf5_only.ps1` (stops Qwen → run → restart Qwen).
- `fishs2_chennai_test.py` — S2 Pro CLI (prosody tags). DONE.
- `sarvam_bulbul_chennai_test.py` — Sarvam REST API (`POST https://api.sarvam.ai/text-to-speech`, header `api-subscription-key`, body `{text, language_code:"ml-IN", model:"bulbul:v3", speaker:"shubh", speech_sample_rate:24000}` → base64 wav). Run: `run_sarvam.ps1` (cloud, NO GPU, Qwen can stay running).
- `run_ab.ps1` — full A/B (stop Qwen → loralib → IndicF5 → S2 Pro → restart Qwen).

**IndicF5 crash fix (2026-09-08):** `model.py` wraps vocoder+DiT in `torch.compile()`; on torch 2.11 dynamo fake-tensor propagation crashes inside MelSpectrogram filterbank ("Tensor on device cpu is not on the expected device meta"). **FIX:** in `indicf5_chennai_test.py`, `import torch._dynamo; torch._dynamo.config.disable = True; torch.compile = lambda fn,*a,**k: fn` BEFORE `AutoModel.from_pretrained`. (Env var `TORCHDYNAMO_DISABLE=1` alone did NOT work.)

**S2 Pro fixes (2026-09-08):** (1) missing `loralib` → installed. (2) `encode_audio()` `torchaudio.load()` → patched to `soundfile` (torchcodec not installed). (3) test script sets `PYTHONPATH=repo` (runs without heavy `pip install -e .`). Lean deps installed: transformers<=4.57.3, einops, loguru, click, hydra-core, omegaconf, safetensors, descript-audio-codec, descript-audiotools, loralib.

**IndicF5 local files:** `D:\models\ai-movie\models\IndicF5\` (config.json, model.py, model.safetensors 1.4GB, checkpoints/vocab.txt, f5_tts/, prompts/). venv `envs\indicf5ml` (transformers 5.16.1, f5-tts.egg-link → repos\IndicF5, vocos, pydub).

## F5-TTS TEST RAN + OUTPUTS (2026-09-08)
**F5-TTS (indicf5 venv) TEST RAN SUCCESSFULLY — 2 outputs produced for the user to judge:**
- `D:\models\ai-movie\03_audio_processed\indicf5_mithun_test_en.wav` (1.00 s, 24 kHz mono) — English line "Hello, this is a test. I am speaking clearly in my own voice." in Midhun's voice.
- `D:\models\ai-movie\03_audio_processed\indicf5_mithun_test_ml.wav` (18.74 s, 24 kHz mono) — Malayalam line "നമസ്കാരം, എന്റെ പേര് മിഥുനാണ്" in Midhun's voice.
**BUG FIXED (2026-09-08):** torchaudio 2.11's `torchaudio.load()` now routes through `torchcodec` (NOT installed) → `ImportError: TorchCodec is required`. **FIX:** patched `envs\indicf5\lib\site-packages\f5_tts\infer\utils_infer.py` line 376 — replaced `audio, sr = torchaudio.load(ref_audio)` with a `soundfile`-based load (`import soundfile as _sf; _ref,_sr=_sf.read(ref_audio, always_2d=True); audio=torch.from_numpy(_ref.T.copy()).float(); sr=_sr`). `soundfile` 0.14.0 already present. **Model loads clean (CUDA, torch 2.11.0+cu128).**
**USER TO JUDGE:** does the EN line sound like Midhun (not the user)? does the ML line pronounce Malayalam correctly? (Note: the EN output is only 1.0 s — the line may have been clipped/short; if too short, re-run with a longer line.)
**FISH S2 PRO (2026-09-08):** repo cloned to `D:\models\ai-movie\repos\fish-speech` (fishaudio/fish-speech, v2.0.0). **Native Windows install IN PROGRESS** (user preference: native pip first, Docker fallback): venv `D:\models\ai-movie\envs\fishs2` (py3.12) + `torch==2.8.0`/`torchaudio==2.8.0` cu128 + `pip install -e .`. **S2 Pro = 4B params, 80+ langs incl. `ml` Malayalam (global tier), 15K+ emotion tags, zero-shot 10-30 s ref, research license.** Official install = conda/uv + `pip install -e .[cu129]` (Linux/WSL) or Docker; native Windows is the fallback path we're trying. **Comparison plan:** same Midhun ref + same Malayalam line through F5-TTS AND Fish S2 Pro → user picks the winner.

## F5-TTS / WSL2 STATE (2026-09-08, POST-REBOOT RESUME)
**F5-TTS (indicf5 venv) — ALL BUGS FIXED, model LOADS:** (1) CUDA torch 2.11.0+cu128 installed (was CPU-only). (2) `utils_infer.py` `load_model` patched (added `ckpt_file` param + enabled `load_checkpoint` — the pip package had a mismatched/older `utils_infer.py` vs `api.py`). (3) `vocab.txt` downloaded to `envs\indicf5\lib\site-packages\f5_tts\infer\examples\vocab.txt` (from `SWivid/F5-TTS` GitHub `src/f5_tts/infer/examples/vocab.txt`). (4) `scripts\indicf5_test.py` `get_ref_text(audio_path, transcript_path)` fixed (was transcribing the .txt path as audio). **Model loads ("Model loaded.") — just re-run the script.** **WSL2: INSTALLED (2.7.13 + VirtualMachinePlatform) but NOT REBOOTED — reboot required before WSL/Docker work.** Post-reboot: `wsl --version` + `wsl -l -v` (install Ubuntu distro if missing) → start Docker Desktop → `docker run --rm hello-world` → re-run F5-TTS test → Fish S2 Pro comparison (native pip first, Docker fallback). **Fish S2 Pro = `fishaudio/fish-speech` (4B, 80+ langs incl. `ml` Malayalam in global tier, 15K+ emotion tags `[sigh]`/`[exhale]`/`[panting]`, zero-shot 10-30s ref, research license). Maya1 = English-only (dropped). GPT-SoVITS Malayalam NOT officially listed (test before committing).**

## RESUME POINT (2026-09-06, AFTER the two-way test RAN)
**Where we are:** OpenVoice two-way voice-conversion test is **BUILT + RUN + SUCCEEDED** (2026-09-06).
- **Outputs (valid, verified via ffprobe):** `D:\prem_audio\out_prem_in_jaisal.wav` (10.62 s, 22050 Hz mono) + `D:\prem_audio\out_jaisal_in_prem.wav` (5.94 s, 22050 Hz mono).
- **USER CONFIRMED (2026-09-06): the timbre swap is GOOD** ("this is actually good"). The zero-shot OpenVoice VC path is VALIDATED.
- **MORE SAMPLES = BETTER:** the tone-color embedding is an average over the reference clip; the test clips were short (10.6 s / 5.96 s) → a bit noisy. For production use **30 s–1 min clean mono per character** (quiet room, 16-bit WAV, no music/reverb) and the **SAME reference for all of a character's lines** → consistent voice across the movie.

## VOICE STRATEGY (2026-09-06, user direction — CONFIRM reference-sourcing approach)
- **User wants to CREATE OUR OWN character voices** (not rely on 15 friends' voices). Female voices included. MUST be non-robotic.
- **Approach:** curate a small set of DISTINCT reference voices (~4–6: young male, older male, young female, older female) → assign one per character (similar characters can share) → clone each character's lines onto their reference (OpenVoice now, RVC/GPT-SoVITS for final).
- **Reference sourcing — DECIDED (2026-09-07): (a) REAL samples from VOICE NOTES.** The user will record/forward voice notes (WhatsApp/Telegram .ogg/.m4a) for each distinct voice type. **Voice notes are PROVEN** — the first successful test used `prem_1.ogg` + `jaisal reference.ogg` (both Opus voice notes) and the user confirmed the result was good. Opus compression is fine for OpenVoice. (b) TTS profiles and (c) public datasets remain fallbacks only.
- **Collection workflow (BUILT + TESTED 2026-09-07):** (1) user drops voice notes into a folder (e.g. `D:\voice_notes\`); (2) `scripts\collect_references.py <folder> -o references\raw` batch-cleans them (denoise + loudnorm + trim + 16 kHz mono) → `<stem>_clean.wav` per file, with a duration summary (flags <10 s as SHORT); (3) user picks the best clean clip per voice → `references\char_XX\ref_clean.wav`; (4) per line: user dubs (headset) → `scripts\clean_audio.py` → `scripts\convert_character.py --dub <line_clean.wav> --ref <char_ref_clean.wav> -o <out.wav>` (OpenVoice timbre swap, `--tau` 0.3 default, 0.5 if weak). **All run with the openvoice venv python.**
- **New scripts (2026-09-07):** `scripts\collect_references.py` (batch-clean a folder of voice notes → reference-ready 16 kHz mono files + duration summary), `scripts\convert_character.py` (per-character dub→reference-voice conversion, reuses the OpenVoice V1 checkpoint). `clean_audio.py` refactored to expose a reusable `clean_file()` function. **TESTED:** collect on `D:\prem_audio` (4 files → clean wavs, summary OK); convert_character (prem dub → jaisal voice → `03_audio_processed\test_prem_in_jaisal.wav`, 10.39 s, valid).
- **Non-robotic GUARANTEE:** OpenVoice/RVC do a pure TIMBRE SWAP — they keep the USER'S actual performance (pace/emotion/expression = the acting) and only change the voice color. The user's dub is the "soul"; the reference only provides the color. Since the user dubs well, output inherits that.
- **User dubs ALL 15 characters** (Malayalam + English) in their own voice; we swap the timbre per character.

## STATUS UPDATE (2026-09-06)
- **Title video DONE** (user uploaded it today — "feat 1"). Upscaling of it is the NEXT upscaler task (SeedVR2 models ready).
- **INTRO is now the next visual target** (Track A): natural-face H3 clip (close-up + medium shot) + user's channel monologue (Malayalam + English) → VC → process → LatentSync lip-sync → DaVinci mix. This is the first full end-to-end pipeline test.
- **Pending (bilingual movie):** (1) character voice references [user]; (2) user's dubs all 15 chars ML+EN [user]; (3) VC pipeline [me, ready]; (4) LatentSync lip-sync [me, needs WSL2]; (5) WSL2 install [user, admin+restart]; (6) intro video [both]; (7) SeedVR2 upscale [me, ready]; (8) DaVinci assembly [user]; (9) NO MUSIC D041 [rule]; (10) D045 no LatentSync while ComfyUI active [rule].
- **Checkpoint gotcha (IMPORTANT):** the OpenVoice **V2 S3 bucket is GONE** (`checkpoints_v2_0417.zip` → 404, both `myshell-public-repo-host.s3.amazonaws.com` and the regional variant). Used the **V1 checkpoint from Hugging Face** instead: `myshell-ai/OpenVoice` → `checkpoints/converter/{config.json,checkpoint.pth}` (125 MB, 22050 Hz). **V1 works for our use case** — `convert()`/`extract_se()` are version-agnostic (pure audio-to-audio timbre swap); V2's improvements were only in the TTS *text* path, which we do NOT use. `run_conversion.py` now auto-detects (`checkpoints_v2` first, falls back to `checkpoints`).
- **Fixes applied to make it run (2026-09-06):** (1) **librosa was broken** — `ModuleNotFoundError: No module named 'pkg_resources'` because the venv had setuptools 84.0.0 (which removed pkg_resources); fixed with `pip install "setuptools<81"`. (2) **`api.py` bug** — `ToneColorConverter.__init__` forwarded `enable_watermark` to `super().__init__()` which doesn't accept it → `TypeError`; fixed by `kwargs.pop('enable_watermark', True)` before `super()` (backup `api.py.bak_comfyfix`). (3) **text-path deps** installed (the `openvoice.api` import pulls `openvoice.text`): `inflect==7.0.0 eng_to_ipa==0.0.2 pypinyin==0.50.0 cn2an==0.5.22 jieba==0.42.1`. (4) torch in the venv is **CPU-only** (2.14.0+cpu) — conversion ran on CPU (fine for short clips; avoids GPU contention per D045).
- **Nothing is lost:** all scripts + this plan are on disk (see VC tooling section below).

Source guide: `d:\models\vsCodeMcp\AI_MOVIE_AUDIO_SETUP_GUIDE_FINAL.md` (WSL2 + IndicF5 + LatentSync + DaVinci Resolve).
Target: Jaisal Cut channel-intro monologue — natural-face close-up/medium shot, Malayalam dialogue, lip-sync to H3 video.

## VERIFIED FACTS (from official docs, 2026-09-06 — do NOT re-research)

### IndicF5 (ai4bharat/IndicF5)
- Install: `conda create -n indicf5 python=3.10 -y` + `pip install git+https://github.com/ai4bharat/IndicF5.git`
- **It is a transformers Python API, NOT a CLI script:**
  `model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True)`
  `audio = model(text, ref_audio_path="...", ref_text="...")`
- Output sample rate: **24 kHz** (`sf.write(..., samplerate=24000)`).
- Supports **Malayalam** (11 Indian languages). Inputs: target text + reference audio + reference transcript.
- Weights: `huggingface-cli download ai4bharat/IndicF5` (or loaded directly via `from_pretrained`).

### LatentSync (ByteDance/LatentSync)
- Setup: `source setup_env.sh` (bash → **WSL2 required**, confirmed).
- Checkpoints: `latentsync_unet.pt` + `whisper/tiny.pt` from `ByteDance/LatentSync-1.6`.
- Inference: `python gradio_app.py` (GUI) or `./inference.sh` (CLI).
- Params: `inference_steps` 20–50 (higher = better quality, slower), `guidance_scale` 1.0–3.0 (higher = better sync, more distortion risk).
- **VRAM: v1.5 = 8 GB, v1.6 = 18 GB** (fits 32 GB RTX 5090).
- **Audio = 16 kHz** (confirmed by its data-processing pipeline). Video = 25 fps. Faces **512×512** (v1.6; v1.5 = 256×256).
- **Works on photorealistic faces ONLY — NOT line-art/sketch.** Lip-sync target = the natural-face intro video, NOT the Jaisal Cut sketch.

### Guide corrections (vs AI_MOVIE_AUDIO_SETUP_GUIDE_FINAL.md)
1. IndicF5 has NO CLI inference script — it's the `model(...)` transformers API (guide's "inspect entry point" step resolved).
2. LatentSync v1.6 = 512×512 (guide implied 256×256, which is v1.5).
3. 16 kHz audio IS required by LatentSync (guide's "don't assume 16 kHz" resolved: it is).
4. WSL2 is justified (setup_env.sh is bash).

## ENVIRONMENT STATE (2026-09-06)
- **WSL2: NOT installed** (`wsl.exe` present but no distro; `wsl -l -v` → "not installed"). Install = `wsl --install -d Ubuntu-22.04` (ADMIN + RESTART).
- **NVIDIA driver: present** (nvidia-smi works) — WSL2 uses the Windows driver. ✓
- **SeedVR2 download IN PROGRESS** (7B Sharp FP16 done; 3B FP16 + 7B FP8 mixed resuming) → **DO NOT RESTART until it finishes** (restart kills the download).

## DIVISION OF LABOR
| This agent (me) | User |
|---|---|
| Drive entire WSL2 setup via `wsl.exe` from Windows (apt, conda, clone, pip, huggingface-cli) | **Install WSL2** (admin + restart — I cannot elevate) |
| Create directory structure + scripts | **Provide reference audio** (5–10 s clean mono WAV + exact transcript per character) |
| Run TTS + LatentSync inference, verify outputs (length, sample rate via ffprobe) | **Listen** to TTS quality (I cannot hear audio) |
| | **DaVinci Resolve** final assembly |

## DRAFT EXECUTION PLAN (phased)
- **Phase 0 (USER, after SeedVR2 download finishes):** `wsl --install -d Ubuntu-22.04` (admin) → restart → set Ubuntu username/password.
- **Phase 1 (ME, via `wsl.exe`):** `sudo apt update && sudo apt upgrade`, install `build-essential git curl wget ffmpeg`; install Miniconda; create `tts_env` (py3.10) + `sync_env` (py3.10).
- **Phase 2 (ME + USER):** create `~/ai-movie/` structure (01_visuals, 02_audio_raw, 03_audio_processed, 04_lipsync, 05_final, references/char_X, models, scripts). USER drops reference WAVs + `ref_transcript.txt` per character.
- **Phase 3 (ME):** IndicF5 — `pip install git+...IndicF5.git` in tts_env; test TTS with `model(text, ref_audio_path, ref_text)`; output 24 kHz WAV to 02_audio_raw.
- **Phase 4 (ME):** audio processing — `ffmpeg` resample 24 kHz → **16 kHz** + loudnorm + trim silence → 03_audio_processed (match LatentSync's 16 kHz).
- **Phase 5 (ME):** LatentSync — `source setup_env.sh` in sync_env (downloads checkpoints); test lip-sync on a natural-face H3 clip → 04_lipsync.
- **Phase 6 (USER):** DaVinci Resolve — import synced video, add ambience (NO MUSIC — D041), export H.264.

## REFINED GOAL (2026-09-06, user clarified TWICE)
- A **movie with 15 characters**, each with a **distinct voice**.
- **USER (an artist) dubs ALL 15 characters in their OWN voice** (Malayalam), with **different pace/expression per character** (the acting). The user CANNOT produce 15 different voices.
- **USER'S PLAN (confirmed direction):** get a **friend's voice message** (WhatsApp/Telegram) per character → **VOICE CONVERT** the user's dub into that friend's voice. **The user's performance (pace/expression) is preserved; only the timbre changes.**
- **This is VOICE CONVERSION (VC), NOT TTS.** IndicF5 (TTS) is a FALLBACK only (for characters with no friend reference, or if VC underperforms).
- **Malayalam AND English** audio. VC is language-agnostic (keeps the user's words, changes the voice).

### VC tooling (2026-09-06)
- **Zero-shot (quick test):** **OpenVoice v2** (easiest, `pip install`, works from 30 s–1 min ref) or **Seed-VC**.
- **Trained (best quality, for final):** **RVC** or **GPT-SoVITS** (need 1–2 min clean audio per friend).
- **Caveat:** WhatsApp/Telegram audio is compressed — fine for a TEST, but get a cleaner 1–2 min reference (16-bit WAV, quiet room) for the FINAL.
- **Consistency:** use the SAME friend reference for all of that character's lines → consistent voice.
- **LatentSync (lip-sync)** is a later stage (WSL2).

## TWO-TRACK SCOPE (2026-09-06, user clarified)
**Track A — CURRENT VIDEO (intro monologue):** TWO audio files for the video we're generating — `intro_malayalam.wav` + `intro_english.wav` (user's dubs, both languages). Process → lip-sync → final mix.
**Track B — 15-CHARACTER MOVIE:** user's dub → friend's voice (VC) per character.
Both tracks share the same pipeline: `02_audio_raw` (dubs) → `03_audio_processed` (16 kHz mono for LatentSync) → `04_lipsync` → `05_final` (DaVinci).
**Scripts ready:** `scripts\clone_voice.py` (IndicF5 TTS fallback), `scripts\process_audio.py` (loudnorm -16 LUFS + silence trim + 16 kHz mono, uses `D:\ffmpeg\...\ffmpeg.exe`).
**IndicF5 install: COMPLETE** (venv `d:\models\ai-movie\envs\indicf5`, f5_tts + torch 2.14.0 + transformers 5.16.1). First `from_pretrained("ai4bharat/IndicF5")` downloads weights from HF.
**VC tooling: OpenVoice V2 (myshell-ai) — chosen for zero-shot audio-to-audio timbre swap.**
- Repo cloned: `d:\models\ai-movie\repos\OpenVoice` (myshell-ai/OpenVoice).
- **Key API fact:** `ToneColorConverter.convert(audio_src, src_se, tgt_se)` is a PURE TIMBRE SWAP — keeps the source's actual words/content, only changes the voice. So it works for ANY language (Malayalam OK). The V2 "native languages" list (EN/ES/FR/ZH/JA/KO) only limits the MeloTTS *text* path, which we do NOT use.
- **Two-way test (user's request):** `D:\prem_audio\prem_1.ogg` (10.64s) + `jaisal reference.ogg` (5.96s), both Opus 48kHz mono. Convert prem→jaisal voice AND jaisal→prem voice.
- **Scripts ready:** `scripts\setup_openvoice.py` (downloads V2 checkpoint — **STALE: the V2 S3 URL is 404**; use the HF V1 checkpoint instead, see RESUME POINT), `scripts\run_conversion.py` (ogg→wav via ffmpeg, `extract_se` per speaker, `convert` both ways → `D:\prem_audio\out_prem_in_jaisal.wav` + `out_jaisal_in_prem.wav`; **auto-detects the checkpoint dir** `checkpoints_v2`→`checkpoints`), `scripts\run_test.ps1` (one-shot — **STALE**, points at the dead V2 URL; the test was run manually instead), `scripts\clean_audio.py` (**recording-cleanup**: denoise + loudnorm + trim + 16 kHz mono — see RECORDING-CLEANUP PIPELINE section).
- **Checkpoint actually used (2026-09-06):** HF `myshell-ai/OpenVoice` → `checkpoints/converter/{config.json,checkpoint.pth}` (V1, 125 MB, 22050 Hz). Downloaded to `repos\OpenVoice\checkpoints\converter\`.
- **Minimal deps for audio-to-audio** (skip MeloTTS/gradio/whisper): `torch librosa==0.9.1 pydub==0.25.1 numpy==1.22.0 unidecode==1.3.7` + `pip install -e repos/OpenVoice`.
- **`se_extractor.get_se`** needs faster-whisper + whisper-timestamped (VAD) — but `run_conversion.py` bypasses it by calling `conv.extract_se([wav])` directly (clips are short/clean, no VAD needed).
- **Status:** scripts written; NOT yet run (agent terminal wedged). User runs `run_test.ps1` in own terminal.
- **RVC/GPT-SoVITS** = trained option for final quality (needs ~1-2 min clean ref per friend + training run). OpenVoice = quick zero-shot test first.

## RECORDING-CLEANUP PIPELINE (2026-09-06, BUILT + TESTED)
The user records dubs on a **PC headset** → raw files have background noise/hiss/hum/room noise. They need a cleanup stage BEFORE using a recording as a reference or dub.
- **Script: `scripts\clean_audio.py`** (run with the openvoice venv python `D:\models\ai-movie\envs\openvoice\Scripts\python.exe`). Pipeline: (1) any format (wav/ogg/m4a/mp3) → mono at native rate; (2) **neural denoise via DeepFilterNet** (removes background noise/hiss/hum/keyboard/room — the key step for a headset recording); (3) loudness-normalize to target LUFS (default -16) + trim leading/trailing silence; (4) resample to **16 kHz mono** (matches LatentSync + OpenVoice).
- **Outputs:** `<stem>_clean.wav` (16 kHz mono, the one to use) + `<stem>_denoised_native.wav` (denoised at original rate, for A/B listening).
- **Usage:** `python clean_audio.py <raw_recording> [-o OUT_DIR] [--lufs -16]`.
- **Deps (installed in openvoice venv):** `deepfilternet` (module imports as **`df`**, class `DfNet`, high-level API `from df.enhance import init_df, enhance`; default model "DeepFilterNet3" auto-downloads from GitHub on first run), `torchaudio` (CPU, matching torch 2.14.0+cpu).
- **Gotcha fixed:** torchaudio 2.11 removed `torchaudio.backend.common.AudioMetaData` which `df/io.py` imports → patched `df/io.py` with a try/except fallback (annotation-only use). `DeepFilterNet` is NOT a top-level export — use `from df.deepfilternet import DfNet` or the `init_df`/`enhance` API.
- **TESTED (2026-09-06):** `jaisal reference.ogg` (48 kHz, 5.95 s) → `jaisal reference_clean.wav` (16 kHz mono, 5.30 s, silence trimmed) + `jaisal reference_denoised_native.wav` (48 kHz, 5.95 s). Both valid.
- **RECOMMENDED FLOW for the user:** record on headset → drop the raw file → `clean_audio.py` → use `<stem>_clean.wav` as the reference/dub. For a CHARACTER REFERENCE, record 30 s–1 min clean mono (see VOICE STRATEGY).

## ENGLISH + MALAYALAM CONVERTER (2026-09-06, CLARIFIED)
- **Voice CONVERSION (timbre swap) is LANGUAGE-AGNOSTIC** — OpenVoice `convert()` keeps the source's actual words/content and only changes the voice color. So the SAME OpenVoice pipeline handles BOTH English and Malayalam dubs (the user's words in either language, swapped to the target character's voice). **No separate "English converter" vs "Malayalam converter" is needed for the VC stage.**
- **TTS (text→speech) is where language matters:** IndicF5 (installed) handles Malayalam + 10 other Indian languages; for English TTS use a different model (e.g. the OpenVoice MeloTTS text path is EN/ES/FR/ZH/JA/KO only). But TTS is only a FALLBACK (for characters with no reference) — the primary path is the user's dub + VC.
- **So the "converter for English and Malayalam" = the same OpenVoice VC pipeline (language-agnostic) + IndicF5 as the Malayalam TTS fallback.** The user is NOT doing TTS now (they dub themselves) — this is just kept ready.

## JAISAL VOICE TEST (2026-09-07, BUILT + RUN — USER TO LISTEN)
The user placed 9 Jaisal voice notes in `D:\voice_notes\Jaisal_audio\` (jaisal_1..9.ogg) + 2 movie Malayalam clips (`D:\voice_notes\reference.ogg`, `reference_2.ogg`). **Goal: prove we can generate speech in Jaisal's voice for random English + Malayalam prompts.**
- **Jaisal reference built:** all 9 notes cleaned (`references\jaisal\jaisal_N_clean.wav`, 5.5–34 s each) → **combined `references\jaisal\jaisal_ref_combined.wav` (158 s, 16 kHz mono)** — the most stable embedding. Use this as Jaisal's reference.
- **Malayalam test (audio→audio, movie dialogue → Jaisal's voice):** `convert_character.py --dub <movie clip> --ref jaisal_ref_combined.wav` →
  - `03_audio_processed\ml_reference_in_jaisal.wav` (17.55 s)
  - `03_audio_processed\ml_reference_2_in_jaisal.wav` (19.53 s)
- **English test (text→speech→Jaisal's voice):** NEW `scripts\english_test.py` — Stage 1 `BaseSpeakerTTS` (EN base speaker, `speaker='default'`) synthesizes the text in a neutral base voice; Stage 2 `ToneColorConverter` swaps it to Jaisal's voice. Footballer hat-trick line →
  - `03_audio_processed\en_footballer_in_jaisal_base.wav` (8.68 s, base voice, A/B)
  - `03_audio_processed\en_footballer_in_jaisal.wav` (8.67 s, **Jaisal's voice**)
- **Gotchas fixed (2026-09-07):** (1) EN base speaker was missing → downloaded from HF `myshell-ai/OpenVoice` → `checkpoints\base_speakers\EN\{checkpoint.pth (156 MB),config.json,en_default_se.pth,en_style_se.pth}`. (2) `tts(speaker='EN')` failed (`'HParams' object has no attribute 'EN'`) — the config's `speakers` dict uses `default=1, friendly=9, cheerful, excited, sad, angry, ...` → use **`speaker='default'`**. (3) TTS sentence-splitter prints IPA chars (`\u0259`) that crash the Windows cp1252 console → `english_test.py` sets `sys.stdout.reconfigure(encoding='utf-8')`.
- **USER TO LISTEN (the direction-setting test):** (a) `ml_reference_in_jaisal.wav` + `ml_reference_2_in_jaisal.wav` — does the movie dialogue now sound like Jaisal? (b) `en_footballer_in_jaisal.wav` — does the English footballer line sound like Jaisal? (A/B against `en_footballer_in_jaisal_base.wav` = the neutral base voice). **If it works → proceed to the intro scripting.** If the voice isn't Jaisal enough → re-run with `--tau 0.5`.

### JAISAL VOICE TEST — v2 FIX (2026-09-07, user: "the voices are too poor... it felt like a robotic voice, whereas the previous swap between jaisal's audio and prem's audio was actually good")
**ROOT CAUSE (diagnosed, not guessed):** the v1 test used a SINGLE 158 s reference (`jaisal_ref_combined.wav` = all 9 notes hard-concatenated). `ToneColorConverter.extract_se(ref_wav_list)` is designed to take a **LIST** of clips — it computes a per-clip tone-color embedding (each on a short coherent utterance) then AVERAGES them. The `ref_enc` encoder was trained on short coherent utterances (~5–10 s). Feeding it one 158 s heterogeneous file (different gain/noise/content/cuts) produced ONE blurry embedding that does not cleanly represent the timbre → with tau=0.3 the output stayed close to the SOURCE voice with only a muddy tint → the "robotic / forcing a different audio" feel. The GOOD prem↔jaisal test used a SINGLE ~6 s clean clip → clean embedding → good result.
**FIX:** pass the individual clean clips as a LIST (per-clip embeddings averaged). New scripts (openvoice venv python, CPU torch): `scripts\convert_multi_ref.py` (`--dub DUB.wav --ref REF1.wav REF2.wav ... -o OUT.wav [--tau 0.3]`) + `scripts\english_test_multi.py` (`--text "..." --ref REF1.wav ... -o OUT.wav`).
**v2 outputs (in `03_audio_processed\`):** `ml_reference_in_jaisal_v2.wav` (17.81 s, movie ML dialogue → Jaisal, multi-ref) + `en_footballer_in_jaisal_v2.wav` (8.78 s) + `_base.wav` (A/B). **USER TO A/B:** v2 vs v1 (same source) — is the timbre cleaner / more Jaisal?
**KEY LIMITATION (English/TTS path):** the robotic feel in the ENGLISH test is largely the SOURCE — Stage 1 is MeloTTS (`BaseSpeakerTTS`), a robotic neural TTS. `convert()` changes VOICE COLOR but keeps the source PROSODY → robotic base = robotic output with a different color. For a NATURAL English line, the best source is a REAL human dub (the user's own voice), NOT TTS. The Malayalam test (audio→audio, real movie dialogue as source) is the clean diagnostic of the reference fix.
**RULE: for OpenVoice timbre swap, ALWAYS use multiple short clean clips as a LIST (per-clip embeddings averaged), never one long concatenated file. For natural output, prefer a real human dub as the source over TTS.**

### JAISAL VOICE TEST — v3 SOURCE-CLEANUP FIX (2026-09-07, user: "ml_reference_in_jaisal_v2 this has only humming kind of sound; en_..._base this one has nothing, its just a foreigner speaking; en_..._v2 some sound is matching but its feeling like robotic")
**DIAGNOSIS (spectral analysis, `scripts\analyze_source.py`):** the pipeline is FINE (the good prem↔jaisal test proves the timbre-swap works). The problem is the SOURCES:
- **`reference.ogg` (movie clip) has a MUSIC BED baked in** — spectral flatness 0.0132 (very tonal), RMS std only 2.6 dB (steady bed). Timbre-swap keeps the source's CONTENT and only changes voice color → the **music comes through as humming**, burying the speech. That's the "only humming" in `ml_reference_in_jaisal_v2`.
- **`en_..._base` = MeloTTS** (robotic neural TTS) — centroid 2600 Hz, flatness 0.067 (bright/robotic) → "just a foreigner speaking".
- **`en_..._v2`** = timbre swap on the robotic TTS → "some matching but robotic" (the swap keeps the source PROSODY, only swaps color).
**FIX (Malayalam): separate vocals from music FIRST, then convert.** Installed **Demucs 4.1.0** into the openvoice venv (`pip install demucs`). Ran `python -m demucs --device cpu --two-stems=vocals -o 02_audio_raw\separated D:\voice_notes\reference.ogg` → `02_audio_raw\separated\htdemucs\reference\vocals.wav` (clean speech: centroid 2764 Hz, RMS std 4.6 dB) + `no_vocals.wav` (the music bed: centroid 1315 Hz, flatness 0.001). Then `convert_multi_ref.py --dub vocals.wav --ref <9 jaisal clips> -o 03_audio_processed\ml_reference_vocals_in_jaisal_v3.wav` → **clean speech output** (RMS std 5.4 dB, speech-like, NO humming).
**RULE: for movie/source audio with music, ALWAYS run Demucs vocal separation FIRST (`--two-stems=vocals`), then convert the clean vocals. For English, use a REAL human dub as the source (not MeloTTS) — the swap keeps source prosody, so a robotic TTS base = robotic output.**
**v3 output (USER TO LISTEN):** `03_audio_processed\ml_reference_vocals_in_jaisal_v3.wav` (17.81 s) — movie dialogue (music removed) in Jaisal's voice. Compare vs v2 (`ml_reference_in_jaisal_v2.wav` = humming). **NEXT:** (1) user listens to v3 — is the humming gone + does it sound like Jaisal? (2) for a NATURAL English line, user dubs it (headset) → `clean_audio.py` → `convert_multi_ref.py` (real dub as source). (3) if v3 voice is weak → `--tau 0.5`.

### JAISAL VOICE TEST — v4 WORD-CLARITY LIMITATION (2026-09-07, user: "ml_reference_vocals_in_jaisal_v3 the flow is good but we are not able to cleanly say the words... the words are not clear and non-recognizable at all, it feels like gibberish, the same tone we can keep but the sound is changed thats good thing now fix the wording part")
**DIAGNOSIS:** the timbre swap WORKS (flow + tone are correct = Jaisal's voice). But the WORDS are garbled because the movie audio is a **DIRTY SOURCE** for a timbre swap. Even after Demucs (music removal) + DeepFilterNet (denoise), the movie audio still has: (1) **REVERB** (movie audio is recorded in a room/studio with reverb), (2) **the original actor's articulation** (their specific way of saying the words). OpenVoice's `convert()` preserves the source's CONTENT (words + prosody) and only swaps the TIMBRE. When the source is reverb-laden and has another actor's articulation, the "content" (words) gets distorted — the model can't cleanly separate the words from the reverb/artifacts, so they come out garbled. **That's why the flow/tone is right but the words are gibberish.**
**v4 (built + run):** Demucs-separated vocals → **DeepFilterNet denoise** (`clean_audio.py` on `vocals.wav` → `vocals_clean.wav`) → `convert_multi_ref.py` → `03_audio_processed\ml_reference_vocals_clean_in_jaisal_v4.wav` (17.55 s). The denoise removes residual music/noise artifacts, so the source is cleaner than v3. **But the fundamental issue (reverb + original actor's articulation) remains** — v4 should be slightly better than v3 but may not fully fix the garbled words.
**THE REAL FIX FOR CLEAR WORDS:** use a **CLEAN SOURCE** — the user's own dub of the line (headset, quiet room, dry). Then the timbre swap preserves the user's clear articulation and only changes the color. The words will be clear because the source is clean. **Pipeline:** (1) user speaks the line on headset → `clean_audio.py` → clean 16 kHz mono; (2) `convert_multi_ref.py --dub <your_clean_dub> --ref <9 jaisal clips>` → your words in Jaisal's voice, **clear**.
**RULE: the movie→Jaisal path (audio→audio) is good for TESTING the timbre, but NOT for production-quality words. For production, dub the line yourself (clean source) → timbre swap → clear words in Jaisal's voice. The timbre swap preserves the source's content (words + prosody) and only swaps the timbre — a dirty source (reverb, music, another actor's articulation) = garbled words.**

## VOICE STRATEGY PIVOT (2026-09-08 — IndicF5 for Malayalam words)
**USER VERDICT (2026-09-08):** "the voice is good, we can see change, but the wordings are not correct... the dialogue lacks the perfection of the letters they speak in malayalam... maybe because of the way we are converting it? or maybe lack of words recognition?"
**CONFIRMED DIAGNOSIS:** OpenVoice is an **English-centric timbre swap** — it does NOT understand Malayalam words, it only swaps voice color in the frequency domain. For Malayalam (retroflex consonants, allophonic variations, complex consonant combinations), that swap **distorts the phonemes** → voice changes correctly but WORDS get mangled. **Flipping the direction does NOT fix this** (tool limitation, not direction).
**THE FIX:** **IndicF5** (Malayalam-native TTS, proper G2P) generates the words CORRECTLY first, then **OpenVoice** swaps the voice color. Pipeline: user dubs line → `clean_audio.py` → Whisper transcribe → IndicF5 speaks text in character's voice (ML) / OpenVoice or GPT-SoVITS (EN).
**MIDHUN AUDIO (2026-09-08):** `D:\voice_notes\mithun_audio\` (3 EN + 2 ML, comprehensive 56–124 s). **Prem audio CANNOT be used** (no permission). Cleaned → `references\mithun\*_clean.wav`.
**v7 outputs (`03_audio_processed\`):** `ml_ref1_in_mithun_v7.wav` (17.81 s), `ml_ref2_in_mithun_v7.wav` (19.53 s), `jaisal_1_in_mithun_v7.wav` (11.18 s), `mithun_ml1_in_jaisal_v7.wav` (78.53 s).
**BATCH JAISAL→MIDHUN (2026-09-08):** NEW `scripts\batch_jaisal_to_mithun.py` (loads converter ONCE, extracts Midhun tone-color ONCE from 5 clips, converts all 9 Jaisal dubs) → `03_audio_processed\jaisal_1..9_in_mithun_batch.wav` (all 9 done). **USER TO LISTEN.**
**IN PROGRESS (2026-09-08):** (1) Whisper "medium" transcription (`scripts\transcribe_ml.py`, IndicF5 venv, GPU) — movie dialogue → `02_audio_raw\movie_dialogue_ml.txt` + Midhun ML ref → `references\mithun\mithun_ml1_transcript.txt`. (2) **NEXT: IndicF5 test** — `model(movie_dialogue_text, ref_audio=Midhun ML ref, ref_text=Midhun transcript)` → movie dialogue spoken CORRECTLY in Midhun's voice (the proof of the fix).
**BEST-OPTION RECOMMENDATION (production house):** (1) **IndicF5 = Malayalam workhorse** (only Malayalam-native tool; zero-shot `model(text, ref_audio, ref_text)`). (2) **GPT-SoVITS = English workhorse** (production-ready; Malayalam uncertain — test first). (3) **Main character (user) = clean dub directly** (no conversion).
**USER'S 52-LETTER IDEA (validated):** record 5 files covering all 52 Malayalam letters per character → more complete voice embedding → better conversion.
**USER'S VISION (2026-09-08): alone warrior, aiming for Cannes — everything else (image/video) is in place, VOICE is the last piece.**
**HARD RULE ADDED to AGENTS.md (2026-09-08): CONTINUOUS MEMORY UPDATES — update memory files IMMEDIATELY after every significant action, do NOT batch to session end.**

## DIALOGUE → VIDEO PLAN (2026-09-06, user will write the script)
The user will **think of the dialogue + write a script**, then we build the video. Pipeline per shot/character:
1. **User writes the script** (dialogue per character, Malayalam + English).
2. **User records dubs** (headset) → `clean_audio.py` → clean 16 kHz mono dubs.
3. **VC (optional):** swap each character's dub to their reference voice (OpenVoice, language-agnostic).
4. **Generate the video** (natural-face H3 clip per shot — close-up/medium; character consistency via ComfyUI-Continuity).
5. **Lip-sync** (LatentSync, WSL2) the clean dub onto the video.
6. **Assemble** (DaVinci Resolve) — NO MUSIC (D041), natural ambience only.
- **First target = the INTRO** (channel monologue, natural face, close-up + medium) as the end-to-end test before batching 15 characters.

## ENVIRONMENT DECISION (2026-09-06)
- **IndicF5 runs on NATIVE WINDOWS** (pure Python transformers model) — **NO WSL2 needed** for the TTS/voice-cloning stage. Set up in a Python 3.10 venv at `d:\models\ai-movie\envs\indicf5`.
- **WSL2 is ONLY needed for LatentSync** (lip-sync, bash `setup_env.sh`). Defer WSL2 install until the lip-sync stage.
- **Project root: `d:\models\ai-movie\`** — structure created: `01_visuals, 02_audio_raw, 03_audio_processed, 04_lipsync, 05_final, models, scripts, references/char_01..char_15`.
- **Scripts:** `scripts\clone_voice.py` (single-character voice-clone test — `--char char_01 --text "..."`), `references\README.md` (what to drop per character).
- **IndicF5 install:** `pip install git+https://github.com/ai4bharat/IndicF5.git` into the venv (pulls torch ~2 GB). First `from_pretrained("ai4bharat/IndicF5")` downloads weights from HF.

## OPEN DECISIONS (waiting on user — not blocking)
1. **Reference dubs:** USER to provide `references/char_XX/ref_malayalam.wav` (5–10 s clean mono dub, their voice in that character's tone) + `ref_transcript.txt` (exact words) for each of the 15 characters.
2. **Test video:** which natural-face H3 clip for the first lip-sync test (close-up works best for LatentSync).
3. **TTS language flag:** IndicF5 handles Malayalam via the reference audio + text (no explicit `--lang` flag seen in README — verify at install time).
4. **Restart timing:** WSL2 (for LatentSync) after the SeedVR2 download finishes (it's now DONE — all 5 SeedVR2 files verified GB-scale).

## HARD RULES (apply)
- **D041 NO MUSIC:** audio = dialogue + natural ambience only. No score/instruments in the Resolve mix.
- **D045:** do NOT run LatentSync (18 GB VRAM) while ComfyUI is active — close ComfyUI first.
- **STOP ON FAILURE:** if a dep/model/inference fails — inspect the error, consult the repo docs, explain, propose the smallest fix, wait for confirmation before destructive env changes.
- **No batch automation** until ONE complete shot (TTS → process → lip-sync → verify) succeeds.
