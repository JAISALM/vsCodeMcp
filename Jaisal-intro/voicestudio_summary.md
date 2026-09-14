# VoiceStudio — Summary (for asking DeepSeek / OpenAI for suggestions)

## What it is
- **VoiceStudio** (formerly OmniVoice-Studio) — open-source, fully-local
  **ElevenLabs alternative**.
- Repo: **https://github.com/debpalash/VoiceStudio**
- Website: https://voicestudio.sh/
- License: **AGPL-3.0** (app). Downloaded models keep their own upstream terms.
- Stars: ~23.8k. Latest release: **v0.5.2**.
- Tagline: "Clone voices, dub video, dictate, and produce long-form audio on
  your own hardware." No account, API key, subscription, or usage meter for the
  local workflow.

## Core capabilities
- **16 TTS engines · 11 ASR engines · 646-language catalogue.**
- Workflows: voice cloning (zero-shot from a 3–15 s clip), voice design
  (from age/accent/pitch/style instructions), video dubbing (transcribe →
  translate → preserve speakers → synthesize → export), stories/audiobooks,
  system-wide dictation widget, vocal isolation (Demucs), speaker diarization
  (pyannote/WhisperX), batch queue, model catalogue.
- Local-first: voices/projects/outputs stay on the machine by default.
- AudioSeal watermarking on by default (synthetic-speech provenance).

## Interfaces
- Desktop app (Tauri v2 / Rust + React).
- Local REST/SSE/WebSocket API on **localhost:3900**.
- **OpenAI-compatible audio API** at `http://localhost:3900/v1`
  (`POST /v1/audio/speech`, `POST /v1/audio/transcriptions`,
  `GET /v1/audio/voices`).
- **MCP server** at `http://localhost:3900/mcp` (tools: `generate_speech`,
  `clone_voice`, `transcribe`).
- Google Colab notebook for cloud trial.

## TTS engines (the ones that matter)
| Engine | Langs | Clone | Compute | License |
|---|---|---|---|---|
| **OmniVoice** (default, k2-fsa) | 600+ (incl. Malayalam) | Yes | CUDA/CPU | AGPL app · Apache-2.0 code · CC-BY-NC weights |
| CosyVoice 3 | 9 + 18 dialects | Yes | CUDA/CPU | Apache-2.0 |
| VoxCPM2 | 30 | Yes | CUDA/CPU | Apache-2.0 |
| GPT-SoVITS | 5 | Yes | CUDA/CPU | MIT |
| MOSS-TTS-Nano | 20 | Yes | CUDA/CPU | Apache-2.0 |
| KittenTTS | English | No | CPU | MIT |
| IndexTTS 2.5 | ZH/EN/JA/ES/AR | Yes | CUDA/CPU | Bilibili (gated >100M MAU) |
| PocketTTS | 6 | Yes | CPU | CC-BY-4.0 (gated) |

## ASR engines
- **WhisperX** (default, ~100 langs, word-level timing, dubbing/subtitles).
- **Faster-Whisper** (~100 langs, cross-platform, int8 fallback).
- Parakeet TDT (English + 25 EU), Moonshine (English, low-power),
  FunASR (50+), sherpa-onnx (streaming dictation).

## Recommended stack by hardware (from the repo)
- **NVIDIA GPU (8 GB+ VRAM):** OmniVoice + CosyVoice 3 (TTS) · WhisperX (ASR).
- Apple Silicon: MLX-Audio · OmniVoice (MPS) · MLX Whisper.
- Low VRAM / CPU-only: PocketTTS · Sherpa-ONNX · KittenTTS · Moonshine.

## Requirements
- OS: Windows 10/11 x64 (also macOS 13.3+ Apple Silicon, Linux x86_64).
- RAM: 8 GB min / 16 GB+ rec. Disk: 10 GB min / 20 GB+ SSD rec.
- GPU: optional (CPU supported); NVIDIA CUDA or Apple Silicon.
- VRAM: 4 GB with GPU / 8 GB+ rec; large optional engines need more.
- Python 3.11+ (from source).

## OUR SETUP (context for the AIs)
- **Hardware:** NVIDIA **RTX 5090 (32 GB VRAM)**, 64 GB RAM, Windows 11.
- **Goal:** clone voices for a **Malayalam + English short movie** ("Jaisal
  Cut"), 2 characters (JAISAL + CAMERA GUY). B&W cinematic.
- **Current voice arsenal (4):** RVC (`midhun_v2_40k`), OpenVoice, IndicF5,
  Fish S2 Pro.
- **Adding VoiceStudio as the 5th** option.
- **Installed:** VoiceStudio v0.5.2 (current-user MSI, no admin), backend on
  localhost:3900, compute = NVIDIA CUDA (auto).
- **Models active/downloading:** OmniVoice (default, active), Whisper large-v3
  (faster-whisper, downloading), Whisper large-v3 Turbo (downloading).
- **Our pick for the movie:** OmniVoice (600+ langs incl. Malayalam, zero-shot
  clone from a 5–15 s reference clip) + Whisper large-v3 (transcription for
  dubbing).

## Question for the AIs
Given this setup (RTX 5090, Malayalam+English movie, 2 characters, already
have RVC/OpenVoice/IndicF5/Fish S2 Pro), which VoiceStudio TTS engine gives the
best **Malayalam** zero-shot voice cloning, and is OmniVoice alone enough or
should we also pull CosyVoice 3 / VoxCPM2 as an A/B? Any engine we're missing
for high-quality Malayalam dialogue?
