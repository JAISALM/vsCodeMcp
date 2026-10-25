#!/usr/bin/env python
"""Malayalam speech-to-text — LOCAL Whisper (no cloud, no API keys, private).

Usage:
    python transcribe_malayalam.py <file.wav|folder> [more files...]

- No args + a "dubs" folder next to this file is NOT assumed — pass the
  audio files or folder explicitly.
- Formats: wav, mp3, m4a, ogg, flac.
- Output: <name>.ml.txt next to each file — Malayalam script lines with
  [mm:ss] timestamps (timestamps ready for the subtitle pipeline).
- First run auto-installs faster-whisper and downloads the large-v3 model
  (~1.5 GB, cached in the HF cache after that).
- GPU: uses CUDA when available (RTX 5090 -> multiple times realtime);
  falls back to CPU int8 otherwise (fine for short clips).

Pipeline fit (movie project):
  1. Speak the scene/lines in Audacity (mono 16-bit 48kHz WAV, the same
     settings used for the dubbing pipeline).
  2. Run this script on the recording.
  3. Whisper large-v3 outputs Malayalam SCRIPT directly (not Manglish) —
     paste straight into the script; run prompts\manglish_to_malayalam.txt
     only if a section came out in Latin.
  4. Same recording can feed the dubbing pipeline (dub -> clean -> sync).

Run with the project's embedded Python:
  & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\transcribe_malayalam.py" <audio>
"""
import sys
from pathlib import Path


def get_transcriber():
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("faster-whisper not found — installing (first run only)...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "faster-whisper"])
        from faster_whisper import WhisperModel

    device, compute = "cpu", "int8"
    try:
        import torch
        if torch.cuda.is_available():
            device, compute = "cuda", "float16"
    except ImportError:
        pass  # CPU int8 path
    print(f"Loading whisper large-v3 on {device} ({compute})...")
    return WhisperModel("large-v3", device=device, compute_type=compute)


def transcribe_file(model, path: Path) -> Path:
    segments, info = model.transcribe(str(path), language="ml", beam_size=5, vad_filter=True)
    lines = []
    for seg in segments:
        ts = f"{int(seg.start // 60):02d}:{int(seg.start % 60):02d}"
        lines.append(f"[{ts}] {seg.text.strip()}")
    out = path.with_name(path.stem + ".ml.txt")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  -> {out.name}  ({len(lines)} lines, lang={info.language} p={info.language_probability:.2f})")
    return out


def main():
    files = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.is_dir():
            files += sorted(f for ext in ("wav", "mp3", "m4a", "ogg", "flac")
                            for f in p.glob(f"*.{ext}"))
        elif p.exists():
            files.append(p)
        else:
            print(f"NOT FOUND: {arg}")
    if not files:
        print("No audio files given. Record with Audacity (mono/16-bit/48kHz WAV), then run:")
        print(f'  python {Path(__file__).name} <file.wav or folder>')
        return
    model = get_transcriber()
    for f in files:
        print(f"Transcribing {f.name} ...")
        transcribe_file(model, f)
    print(f"Done — {len(files)} file(s).")


if __name__ == "__main__":
    main()
