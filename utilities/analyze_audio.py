"""Diagnose audio content: per-second RMS energy + spectral centroid.

Reveals whether an audio file is a CONSTANT NOISE BED (high, flat RMS across all
seconds) or has DISCRETE SOUNDS (low baseline with peaks at specific seconds).

Usage:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\analyze_audio.py" <wav-or-mp4> [more files...]
"""
import sys
import tempfile
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf


def load_audio(path: str) -> tuple[np.ndarray, int]:
    p = Path(path)
    if p.suffix.lower() in {".mp4", ".mp3", ".m4a", ".mov"}:
        # Extract audio to a temp wav via ffmpeg.
        tmp = Path(tempfile.gettempdir()) / (p.stem + "_probe.wav")
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(p), "-vn", "-ac", "1", "-ar", "44100", str(tmp)],
            capture_output=True,
        )
        data, sr = sf.read(str(tmp))
    else:
        data, sr = sf.read(p)
    if data.ndim > 1:
        data = data.mean(axis=1)
    return data, sr


def analyze(path: str) -> None:
    data, sr = load_audio(path)
    dur = len(data) / sr
    print(f"\n=== {Path(path).name}  ({dur:.2f}s, sr={sr}) ===")

    # Per-second RMS (dB).
    n_sec = int(np.ceil(dur))
    print("per-second RMS (dB):")
    for s in range(n_sec):
        seg = data[s * sr:(s + 1) * sr]
        if len(seg) == 0:
            continue
        rms = np.sqrt(np.mean(seg ** 2))
        db = 20 * np.log10(rms + 1e-9)
        bar = "#" * max(0, int((db + 60) / 2))
        print(f"  {s:>2}-{s + 1:>2}s  {db:6.1f} dB  {bar}")

    # Overall spectral centroid (high centroid = noisy/bright; low = tonal).
    from numpy.fft import rfft, rfftfreq
    # Use a middle chunk to avoid edge effects.
    mid = len(data) // 2
    chunk = data[mid - sr:mid + sr]
    spec = np.abs(rfft(chunk))
    freqs = rfftfreq(len(chunk), 1 / sr)
    centroid = np.sum(freqs * spec) / (np.sum(spec) + 1e-9)
    print(f"  spectral centroid (mid): {centroid:.0f} Hz  "
          f"({'NOISY/bright' if centroid > 3000 else 'tonal/low' if centroid < 800 else 'mid'})")

    # Peak-to-RMS ratio (high = discrete transients; low ~1 = steady noise).
    rms_all = np.sqrt(np.mean(data ** 2))
    peak = np.max(np.abs(data))
    print(f"  peak/RMS ratio: {peak / (rms_all + 1e-9):.2f}  "
          f"({'discrete transients' if peak / (rms_all + 1e-9) > 4 else 'steady bed' if peak / (rms_all + 1e-9) < 2 else 'mixed'})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: analyze_audio.py <file> [more files...]")
        raise SystemExit(1)
    for f in sys.argv[1:]:
        analyze(f)
