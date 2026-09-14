🎬 Local AI Movie Audio & Lip-Sync Setup Guide
Target Hardware: NVIDIA RTX 5090 (or 3090/4090)
OS: Ubuntu 22.04+ / WSL2 (Ubuntu)
Goal: Generate consistent multi-character Malayalam dialogue using local voice cloning, sync lips, and mix in DaVinci Resolve.

1. Prerequisites (The "Before You Start" Checklist)
Before running any commands, ensure the following are installed:

NVIDIA Drivers: Ensure you have the latest drivers installed for your RTX 5090.
Check with nvidia-smi. You should see "CUDA Version: 12.x" or higher.
Python 3.10:
Do not use the system Python.
We will use conda to manage environments.
Git: Standard version control.
Hugging Face Access Token:
You need an account at huggingface.co.
Create a token: Go to Settings -> Access Tokens.
Create a Read token.
Keep it safe. We will call it HF_TOKEN.
2. Step 1: Environment Setup
Create a dedicated Conda environment to avoid dependency conflicts.

bash

# 1. Install Miniconda if not installed
# (Assumes you have conda. If not, install Miniconda from https://docs.conda.io/en/latest/miniconda.html)

# 2. Create a new environment named 'movie_audio'
conda create -n movie_audio python=3.10 -y
conda activate movie_audio

# 3. Upgrade pip
pip install --upgrade pip
3. Step 2: Install the TTS Engine (F5-TTS)
We will use F5-TTS because it is state-of-the-art for Zero-Shot Voice Cloning and supports custom language fine-tunes. We will specifically look for a model fine-tuned for Indian Languages/Malayalam.

Note: If a specific "Malayalam F5-TTS" model is not immediately available on Hugging Face, we will use the standard F5-TTS with high-quality Malayalam reference audio, or use IndicF5 which is tailored for Indic scripts.

For this guide, we will set up F5-TTS as the core engine.

bash

# 1. Clone the official F5-TTS repository
git clone https://github.com/SWivid/F5-TTS.git
cd F5-TTS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install TTS specific dependencies if needed
pip install torchaudio soundfile
Finding the Malayalam Model
Search Hugging Face for models like:

SWivid/F5-TTS (Base model - needs good reference audio)
siddharth/F5-TTS-Indic (If available for Indic languages)
Alternative: If F5-TTS struggles with Malayalam pronunciation, we will switch to Svara-TTS or IndicF5.
For now, let's download the base model to test the infrastructure:

bash

# Create a folder for models
mkdir -p ../models

# Download the base F5-TTS model (this is ~2GB, may take a while)
huggingface-cli download SWivid/F5-TTS --local-dir ../models/F5-TTS
4. Step 3: Prepare Character Reference Audio
CRITICAL: You cannot generate "Character A" without a reference.
You mentioned you will not use ElevenLabs. You will record yourself or friends.

Record 4 Audio Files:
ref_char_a.wav: 10 seconds of a male voice (you or friend) speaking Malayalam. Clear, no background noise.
ref_char_b.wav: 10 seconds of a different male voice (different pitch/tone).
ref_char_c.wav: 10 seconds of a female voice.
ref_char_d.wav: 10 seconds of an older female voice (use a filter or ask an older relative).
Format: Ensure they are .wav, 22kHz or 44.1kHz, mono or stereo.
Location: Save them in a folder named ./references/.
bash

mkdir -p references
# Place your 4 .wav files into ./references/
5. Step 4: Test Voice Cloning
Create a simple test script to verify that the model can clone your reference voice.

Create a file named test_tts.py inside the F5-TTS folder:

python

import torch
from f5_tts.model import F5TTS
import soundfile as sf

# 1. Load the Model
print("Loading Model...")
model = F5TTS.from_pretrained("../models/F5-TTS", device="cuda")
model.remove_weight_norm()
model.inference_session = None

# 2. Define Character Reference
ref_audio_path = "references/ref_char_a.wav"
target_text = "ഹലോ, എന്റെ പേര് ചരിട്ടർ എ ആണ്." # Example Malayalam text

# 3. Generate Audio
print(f"Generating audio for {target_text}...")
# Note: The exact function signature may vary slightly depending on the repo version.
# Check the README of F5-TTS for the exact generate() function.
# Typically it looks like:
# model.generate(text, ref_audio_path, output_path)

# *If the standard repo doesn't have a simple generate() function, 
# we might need to use the Gradio app or a specific inference script.*

# FOR NOW, let's use the provided gradio app to test manually first.
Better Approach for Testing:
Instead of writing a complex script immediately, use the Gradio Interface that comes with F5-TTS.

bash

# Run the local web server
python app.py --model_path ../models/F5-TTS --device cuda
Open http://localhost:7860 in your browser.
Upload references/ref_char_a.wav.
Type Malayalam text: "നമസ്കാരം, എനിക്കിത് പണിക്കുന്നു."
Click "Generate".
Listen: Does it sound like the reference voice? Is the Malayalam clear?
If the Malayalam is garbled, you need a model fine-tuned for Malayalam. See Section 7.

6. Step 5: Install Lip Sync (LatentSync)
Now that we have the audio, we need to sync it to the video. LatentSync is currently superior to Wav2Lip for quality.

bash

# Go back to the base directory (outside F5-TTS)
cd ..

# Clone LatentSync
git clone https://github.com/ByteDance/LatentSync.git
cd LatentSync

# Install dependencies
pip install -r requirements.txt

# Download the LatentSync model
# Check the Hugging Face page for ByteDance's LatentSync weights
huggingface-cli download ByteDance/LatentSync --local-dir ./weights
Note: If ByteDance's repo is not public or accessible, use Wav2Lip as a fallback:

bash

# Fallback: Wav2Lip
git clone https://github.com/Rudrabha/Wav2Lip.git
cd Wav2Lip
pip install -r requirements.txt
7. Step 6: The Malayalam Specificity (Crucial)
Standard English TTS models often fail at Malayalam phonemes (like the distinct 'ch', 'j', and vowel lengths).

If Step 4 produced bad Malayalam:

You need to switch to IndicF5 or Svara-TTS.

Option A: IndicF5 (Recommended for Indian Languages)
bash

cd ..
git clone https://github.com/[Find-IndicF5-Repo-URL].git
# *Note: You may need to search GitHub for "IndicF5" or "Hindi-F5-TTS" fine-tunes.*
# If no dedicated repo exists, you must use **Svara-TTS**.
Option B: Svara-TTS (Built for Indian Languages)
Svara-TTS has pre-built voices for 19 Indian languages.

bash

cd ..
git clone https://github.com/sarvam-ai/svara-tts.git
cd svara-tts
pip install -r requirements.txt

# Download the model for Malayalam
huggingface-cli download sarvam-ai/svara-tts-ml --local-dir ./models/ml
Using Svara-TTS is easier but less customizable than F5-TTS. It gives you fixed "Speaker 1", "Speaker 2" profiles. If you need specific character cloning, F5-TTS is better, but you must ensure the base model is good at Malayalam.

8. Step 7: Batch Generation Script (The "Agent" Task)
Create a folder ./scripts.
Create a file ./scripts/generate_dialogue.py.

This script will read a JSON file and generate all audio.

File: dialogue.json

json

[
    {
        "character": "char_a",
        "text": "കെട്ടിടം തുറന്നു.",
        "emotion": "calm"
    },
    {
        "character": "char_b",
        "text": "എന്താ അതെല്ലാ?!",
        "emotion": "angry"
    }
]
File: ./scripts/generate_dialogue.py

python

import json
import os
import subprocess
import sys

# CONFIG
REF_DIR = "references"
OUTPUT_DIR = "generated_audio"
TTS_MODEL = "../models/F5-TTS"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_single_audio(char_id, text, emotion):
    ref_file = f"{REF_DIR}/ref_{char_id}.wav"
    output_file = f"{OUTPUT_DIR}/{char_id}_{hash(text)}.wav"
    
    # This is a placeholder. 
    # You must replace this with the actual call to F5-TTS or Svara-TTS.
    # Example for F5-TTS (if it has a CLI or simple API):
    # cmd = f"python generate.py --model {TTS_MODEL} --ref {ref_file} --text '{text}' --out {output_file}"
    
    print(f"Generating {char_id}: {text}")
    # subprocess.run(cmd, shell=True)

def main():
    with open("dialogue.json", "r") as f:
        dialogues = json.load(f)
    
    for entry in dialogues:
        generate_single_audio(entry["character"], entry["text"], entry["emotion"])

if __name__ == "__main__":
    main()
Your Agent should modify this script to actually call the TTS library correctly based on the specific model installed.

9. Step 8: Lip Syncing the Video
You now have:

video_clip.mp4 (from H3)
char_a_line1.wav (from TTS)
Using Wav2Lip (Fallback/Easier)
bash

python Wav2Lip.py \
    --checkpoint_path Wav2Lip/checkpoints/wav2lip_gan.pth \
    --data_path video_clip.mp4 \
    --audio char_a_line1.wav \
    --output char_a_synced.mp4 \
    --pads 20 10 20 10 \
    --fps 25
Using LatentSync (Higher Quality)
Consult the LatentSync documentation for the exact command, as it may require a different interface.

10. Final Assembly (DaVinci Resolve)
Open DaVinci Resolve 21.
Media Pool: Import char_a_synced.mp4, char_b_synced.mp4, etc.
Timeline: Place them in sequence.
Fairlight Tab:
Add Ambience (rain, wind) to a separate track.
Add Music to a separate track.
Adjust levels so Dialogue is clear.
Export:
Deliver Page.
Format: H.264.
Resolution: Match your H3 output (e.g., 1080p or 4K).
🚀 Agent Instructions (Copy this to your Agent)
Task: Set up the local AI audio pipeline on this machine.

Check Hardware: Run nvidia-smi and confirm GPU is visible.
Install Conda: Ensure conda is in PATH.
Create Environment: conda create -n movie_audio python=3.10.
Clone F5-TTS: Clone the repo and install dependencies.
Download Models: Download SWivid/F5-TTS weights to ./models/.
Test TTS: Run the Gradio app (python app.py). Ask the user to provide 4 reference audio files (10 sec each) for characters A, B, C, D in Malayalam.
Verify Language: Generate a test Malayalam sentence. If pronunciation is poor, advise the user to switch to Svara-TTS (Install Svara-TTS and download Malayalam weights).
Install Lip Sync: Clone Wav2Lip (or LatentSync) and download checkpoints.
Create Script: Write a Python script that takes a JSON list of dialogue lines and generates the corresponding audio files using the character's reference voice.
Demo: Run a full end-to-end test:
Input: One video clip + one JSON line.
Output: One synced video clip.
Note on Malayalam Quality:
If F5-TTS fails at Malayalam, immediately pivot to Svara-TTS. Svara-TTS is specifically trained for Indian languages and has built-in speaker profiles, which is easier for multi-character consistency if zero-shot cloning is too unstable.