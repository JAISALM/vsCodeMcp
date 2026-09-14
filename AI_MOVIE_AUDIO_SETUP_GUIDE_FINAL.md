Here is the **Final, Refined Agent Specification**.

This version incorporates all the safety checks, removes authoritative "guesswork" commands, fixes the directory structure, and adds the critical "Stop on Failure" protocol. It is designed specifically to work with a reasoning model like **Qwen 3.8 27B** that needs clear guardrails to avoid dependency hell.

Save this as **`FINAL_AGENT_SPEC.md`** and give it to your agent.

---

# 🎬 FINAL AI MOVIE AUDIO & LIP-SYNC PIPELINE (Windows + WSL2)
**Target Hardware:** NVIDIA RTX 5090 (32GB VRAM)
**Execution Environment:** WSL2 (Ubuntu 22.04)
**Goal:** Generate consistent multi-character Malayalam dialogue, lip-sync to H3 video, and mix in DaVinci Resolve.

## ⚠️ CRITICAL EXECUTION RULES FOR THE AGENT

1.  **WSL2 is the required execution environment.** Do not attempt the pipeline in native Windows Python unless a repository's current official documentation explicitly supports it.
2.  **DO NOT blindly install packages.** Before installing `torch`, `IndicF5`, or `LatentSync`, inspect the **current official GitHub/Hugging Face documentation** to determine the required Python/PyTorch/CUDA versions.
3.  **IndicF5 First.** Do **not** install generic F5-TTS. Use `ai4bharat/IndicF5` which is specifically optimized for Indian languages including Malayalam.
4.  **Verify APIs.** Do not invent function signatures. Inspect the repository to find the actual inference entry point and required arguments.
5.  **Separate Environments if Necessary.** If `LatentSync` and `IndicF5` have conflicting dependency requirements, create two separate Conda environments. Do not force them into one if it breaks.
6.  **No Batch Automation Yet.** Do **not** write `batch_generate.py` until **ONE** complete H3 shot + **ONE** Malayalam line successfully completes the entire pipeline (TTS → Process → Lip Sync → Verify).
7.  **Native Script First.** Use native Malayalam script for TTS input. Only use transliteration/IPA if the pronunciation is demonstrably poor.
8.  **Test Both Lip Syncers.** Do not assume LatentSync is universally superior. Test LatentSync 1.6 first. If it fails on a specific shot, test Wav2Lip as a fallback.
9.  **Log Everything.** Keep a record of every installed version and command so the environment can be reproduced.
10. **Audio Validation is Mandatory.** You must validate audio levels/silence. The specific resampling/normalization parameters must match the requirements of the downstream model (LatentSync). Do not assume 16kHz is required unless the model documentation states it.
11. **VRAM Management.** LatentSync uses ~18-20GB VRAM. Close all other GPU-heavy apps (Chrome, other AI tools) before running inference.
12. **STOP ON FAILURE.**
    *   If a dependency, model download, or inference command fails:
        *   Do **not** randomly install packages.
        *   Do **not** downgrade/upgrade unrelated packages.
        *   Inspect the error message.
        *   Consult the official repository documentation.
        *   Explain the problem to the user.
        *   Propose the smallest corrective action.
        *   **Wait for confirmation** before making destructive environment changes (like uninstalling PyTorch).

---

## Phase 0: Windows Prerequisites (Do This on Windows First)

1.  **Install WSL2:**
    *   Open PowerShell as Administrator.
    *   Run: `wsl --install -d Ubuntu-22.04`
    *   Restart your PC.
    *   Set up your Ubuntu username/password.
2.  **NVIDIA Drivers:**
    *   Ensure you have the latest **Windows** NVIDIA drivers installed (from nvidia.com). WSL2 uses the Windows driver to access the GPU.
    *   Do **not** install Linux CUDA drivers inside WSL2.
3.  **File Structure:**
    *   Create a folder on your Windows drive, e.g., `C:\Projects\ai-movie`.
    *   **Inside WSL2**, you can access this at `\\wsl$\Ubuntu-22.04\home\YOUR_USER\` OR mount the C drive.
    *   **Recommendation:** Keep your project **inside WSL2** (`~/ai-movie`) for best performance, and copy final outputs to Windows for Resolve.

---

## Phase 1: WSL2 Environment Setup (Inside Ubuntu Terminal)

Open your **Ubuntu Terminal** inside WSL2.

### 1. Update System & Install Basics
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git curl wget
sudo apt install -y ffmpeg
```

### 2. Install Miniconda
```bash
# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install
bash Miniconda3-latest-Linux-x86_64.sh

# Restart shell
source ~/.bashrc

# Verify
conda --version
```

### 3. Create Conda Environments

**Environment 1: TTS (IndicF5)**
```bash
conda create -n tts_env python=3.10 -y
conda activate tts_env
pip install --upgrade pip
```

**Environment 2: Lip Sync (LatentSync)**
```bash
conda create -n sync_env python=3.10 -y
conda activate sync_env
pip install --upgrade pip
```

---

## Phase 2: Voice Identity Setup

Create the directory structure **inside WSL2**:

```text
~/ai-movie/
├── 01_visuals/          # H3 Video Outputs (Locked Master)
├── 02_audio_raw/        # Generated TTS WAV files (unprocessed)
├── 03_audio_processed/  # Normalized/Trimmed WAV files (for Lip Sync)
├── 04_lipsync/          # LatentSync Output Videos
├── 05_final/            # Ready for DaVinci Resolve
├── references/          # Character Voice Samples
│   ├── char_a/
│   │   ├── ref_malayalam.wav  (5-10 sec, clean, mono)
│   │   └── ref_transcript.txt (Exact text spoken in ref)
│   ├── char_b/
│   ├── char_c/
│   └── char_d/
├── models/              # Downloaded Weights
└── scripts/             # Python utilities
```

**Action:**
1.  Copy your 4 reference audio files (`ref_malayalam.wav`) into `references/char_a/`, etc.
2.  Create `ref_transcript.txt` for each character with the **exact text** spoken in the reference clip.

*Example `references/char_a/ref_transcript.txt`:*
```text
നമസ്കാരം, എന്റെ പേര് ചരിട്ടർ ആണ്.
```

---

## Phase 3: TTS Generation (IndicF5)

We will use `ai4bharat/IndicF5`.

### 1. Install IndicF5 (in `tts_env`)
```bash
conda activate tts_env
cd ~/ai-movie

# Clone the official IndicF5 repository
git clone https://github.com/ai4bharat/IndicF5.git
cd IndicF5

# Install dependencies (Check README for specific torch version)
pip install -r requirements.txt

# Download the IndicF5 Model Weights
huggingface-cli download ai4bharat/IndicF5 --local-dir ../models/IndicF5
```

### 2. Test TTS Generation

**DO NOT execute the command below yet.**

**First inspect the current official IndicF5 repository/model card and determine:**
*   Actual inference entry point (script name).
*   Required arguments.
*   Model loading method.
*   Reference audio requirements (sample rate, duration).
*   Reference transcript requirements.
*   Malayalam language handling (does it use a specific flag?).

**Then run the smallest official/example inference supported by the current version.**

*Example concept (verify against docs):*
```text
python [inference_script] \
    --model_path ../models/IndicF5 \
    --reference_audio references/char_a/ref_malayalam.wav \
    --reference_text "നമസ്കാരം, എന്റെ പേര് ചരിട്ടർ ആണ്." \
    --target_text "ഇന്ന് വേനൽ ചൂട്." \
    --target_lang ml \
    --output 02_audio_raw/test_char_a.wav
```

**✅ Success Criteria:**
1.  Does it sound like the reference voice?
2.  Is the Malayalam pronunciation correct?
3.  Is it natural?

**❌ If it fails:**
*   Check if `ref_transcript.txt` matches the audio exactly.
*   Try a different 10-second sample.
*   If IndicF5 still struggles, fall back to **Svara-TTS** (See Appendix A).

---

## Phase 4: Audio Processing (Validation & Normalization)

Raw TTS output often has inconsistent volume and leading/trailing silence.

**Action:**
1.  **Inspect LatentSync documentation** to determine its required audio input specifications (sample rate, format).
2.  **Process the audio** using `ffmpeg` to match those specifications.

**Concept (Adjust based on model requirements):**
```bash
# Example: Normalize loudness and trim silence
# Verify if 16kHz is actually required by the model
ffmpeg -i 02_audio_raw/test_char_a.wav \
    -af "loudnorm=I=-23:LRA=7:TP=-2, silenceremove=1:0:-50dB" \
    -ar [MODEL_SAMPLE_RATE] \
    03_audio_processed/test_char_a_processed.wav
```

**✅ Success Criteria:**
*   Listen to the processed file. Does it sound punchy and consistent?
*   Check length: Is the silence trimmed?

---

## Phase 5: Lip Sync (LatentSync)

We will use `ByteDance/LatentSync`.

### 1. Install LatentSync (in `sync_env`)
```bash
conda activate sync_env
cd ~/ai-movie

# Clone LatentSync
git clone https://github.com/ByteDance/LatentSync.git
cd LatentSync

# Install dependencies
# NOTE: Check README for specific PyTorch version. Do NOT assume 2.1.0.
pip install -r requirements.txt

# Download LatentSync Checkpoints
huggingface-cli download ByteDance/LatentSync --local-dir ./weights
```

### 2. Test Lip Sync

**DO NOT execute the command below yet.**

**First inspect the current official LatentSync repository documentation and determine:**
*   The exact inference script name.
*   Required arguments for video/audio input.
*   Checkpoint path requirements.
*   Any additional flags for face detection or enhancement.

**Then run the smallest official/example inference supported by the current version.**

*Example concept (verify against docs):*
```text
python [inference_script] \
    --video 01_visuals/test_video.mp4 \
    --audio 03_audio_processed/test_char_a_processed.wav \
    --output 04_lipsync/test_char_a_synced.mp4 \
    --checkpoint weights/[model_file]
```

**✅ Success Criteria (Lip Sync Checklist):**
1.  **Sync:** Are the lips moving with the audio? (Play at 0.5x speed).
2.  **Stability:** Are there any "jittery" mouth movements?
3.  **Warping:** Is the face warping or morphing?
4.  **Expression:** Does the character's expression match the emotion?

**❌ If quality is poor:**
*   Try a different video clip (frontal faces work best).
*   Fall back to **Wav2Lip** for that specific shot.

---

## Phase 6: Final Assembly (DaVinci Resolve on Windows)

1.  **Copy Output:**
    *   Copy `04_lipsync/test_char_a_synced.mp4` from WSL2 to your Windows drive (`C:\Projects\ai-movie\04_lipsync\`).
2.  **Open DaVinci Resolve 21 (Free)** on Windows.
3.  **Edit Page:**
    *   Import the synced video.
4.  **Fairlight Page:**
    *   Add Ambience/Music.
5.  **Deliver Page:**
    *   Export as H.264.

---

## Appendix A: Fallback TTS (Svara-TTS)

If IndicF5 produces poor Malayalam quality, use **Svara-TTS**.

```bash
# Install Svara-TTS in tts_env
git clone https://github.com/sarvam-ai/svara-tts.git
cd svara-tts
pip install -r requirements.txt

# Download Malayalam Model
huggingface-cli download sarvam-ai/svara-tts-ml --local-dir ../models/svara-ml
```

*Usage:* Svara-TTS uses pre-built speaker profiles (`ml_speaker_1`, `ml_speaker_2`). This is less "custom" than cloning but often more stable for Indic languages.

---

## 📋 Agent Checklist (Copy & Paste)

**Task:** Set up the `IndicF5` + `LatentSync` pipeline **inside WSL2**.

1.  **WSL2 Check:** Ensure WSL2 is installed and Ubuntu is running.
2.  **System Setup:** Update Ubuntu, install `build-essential`, `git`, `curl`, `wget`, `ffmpeg`.
3.  **Conda:** Install Miniconda. Create `tts_env` and `sync_env` (Python 3.10).
4.  **TTS:** Clone `ai4bharat/IndicF5`. Inspect README. Install deps. Download `ai4bharat/IndicF5` weights to `./models/`.
5.  **Lip Sync:** Clone `ByteDance/LatentSync`. Inspect README. Install deps. Download `ByteDance/LatentSync` weights to `./LatentSync/weights/`.
6.  **Test TTS:**
    *   I will provide `references/char_a/ref_malayalam.wav` and `ref_transcript.txt`.
    *   Inspect IndicF5 docs to determine the correct inference command.
    *   Run the generation script to output `test_char_a.wav`.
    *   Verify the audio is generated.
7.  **Test Processing:**
    *   Inspect LatentSync docs for audio requirements.
    *   Run `ffmpeg` on `test_char_a.wav` to output `test_char_a_processed.wav`.
8.  **Test Sync:**
    *   I will provide `01_visuals/test_video.mp4`.
    *   Inspect LatentSync docs to determine the correct inference command.
    *   Run LatentSync inference to output `test_char_a_synced.mp4`.
9.  **Report:** Tell me if both steps completed without errors. Do **not** write the batch automation script yet.

---

### 💡 Why This Is Better

1.  **Safety First:** The "Stop on Failure" rule prevents dependency hell.
2.  **Documentation-Driven:** The agent is forced to verify current APIs instead of guessing.
3.  **Correct Directory Structure:** Clean separation of concerns.
4.  **Conditional Audio Processing:** Ensures the audio matches the downstream model's requirements.
5.  **Scalable:** Once the "One Shot" works, the JSON batch script is trivial to add.

Give this file to your agent. It is ready to execute.