"""clean_audio.py — denoise + normalize a voice recording (file-level).

File-level equivalent of NVIDIA Broadcast's live noise removal:
  1. decode to mono float (ffmpeg)
  2. highpass ~80 Hz (kills rumble / low-end noise)
  3. spectral gating (STFT soft-gate — the same class of technique as
     Broadcast's AI noise removal, but deterministic and free)
  4. normalize to -1 dBFS
  5. write 48 kHz 16-bit WAV (for editing) + 16 kHz mono WAV (pipeline)

Usage:
  python clean_audio.py <input> [output_dir]

Output files: <stem>_cleaned_48k.wav and <stem>_cleaned_16k.wav
"""
import sys
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

FFMPEG = r"C:\Users\user\AppData\Local\VoiceStudio (Current User)\ffmpeg.exe"


def decode_to_mono(path: Path) -> tuple[np.ndarray, int]:
    """Decode any audio file to mono float32 via ffmpeg."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name
    subprocess.run(
        [FFMPEG, "-y", "-i", str(path), "-ac", "1", "-vn", tmp_path],
        check=True, capture_output=True,
    )
    data, sr = sf.read(tmp_path, dtype="float32")
    Path(tmp_path).unlink(missing_ok=True)
    return data, sr


def highpass(data: np.ndarray, sr: int, cutoff: float = 80.0) -> np.ndarray:
    sos = butter(4, cutoff, btype="high", fs=sr, output="sos")
    return sosfilt(sos, data)


def spectral_gate(data: np.ndarray, sr: int,
                  nperseg: int = 2048,
                  noise_percentile: float = 10.0,
                  over: float = 2.0,
                  floor_db: float = -60.0) -> np.ndarray:
    """STFT soft-gate: estimate noise floor from the quietest frames,
    suppress everything near the floor, keep speech intact."""
    n = len(data)
    hop = nperseg // 2
    n_frames = 1 + (n - nperseg) // hop
    win = np.hanning(nperseg).astype(np.float32)

    # frame energies for noise-floor selection
    frame_idx = np.arange(n_frames)
    energies = np.array([
        np.sum(np.abs(data[i * hop: i * hop + nperseg] * win) ** 2)
        for i in frame_idx
    ])
    threshold_idx = np.percentile(energies, noise_percentile)
    noise_frames = frame_idx[energies <= threshold_idx]
    if len(noise_frames) < 4:
        noise_frames = frame_idx[np.argsort(energies)[:max(4, n_frames // 10)]]

    # average noise spectrum (power)
    noise_spec = np.zeros(nperseg // 2 + 1, dtype=np.float32)
    for i in noise_frames:
        seg = data[i * hop: i * hop + nperseg] * win
        noise_spec += np.abs(np.fft.rfft(seg, nperseg)) ** 2
    noise_spec /= max(len(noise_frames), 1)
    noise_spec = np.maximum(noise_spec, 1e-12)

    # gate each frame
    out = np.zeros_like(data)
    out_count = np.zeros_like(data)
    floor = 10 ** (floor_db / 20.0)
    for i in frame_idx:
        seg = data[i * hop: i * hop + nperseg] * win
        spec = np.fft.rfft(seg, nperseg)
        power = np.abs(spec) ** 2
        # gain: 1 where signal >> noise, -> floor where signal ~ noise
        ratio = power / noise_spec
        gain = np.clip((ratio - 1.0) / over, floor, 1.0)
        spec_gated = spec * gain
        out_seg = np.fft.irfft(spec_gated, nperseg)
        start = i * hop
        out[start:start + nperseg] += out_seg
        out_count[start:start + nperseg] += 1
    mask = out_count > 0
    out[mask] /= out_count[mask]
    return out


def normalize(data: np.ndarray, target_dbfs: float = -1.0) -> np.ndarray:
    peak = np.max(np.abs(data))
    if peak < 1e-6:
        return data
    target = 10 ** (target_dbfs / 20.0)
    return data * (target / peak)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src.stem

    print(f"input: {src}")
    data, sr = decode_to_mono(src)
    print(f"decoded: {len(data) / sr:.2f}s @ {sr} Hz mono")

    # NOTE: file-level dereverb was tried and FAILED on speech-dominant clips
    # (eats the voice — the "quietest" frames still contain speech, so the
    # reverb estimate is wrong). Echo is fixed at the SOURCE instead: record
    # in a soft room (closet full of clothes, closed door, fan off).
    #
    # For background sound / echo MIXED INTO the voice (a gate can't remove
    # it — it only removes noise quieter than the voice), use DEMUCS vocal
    # separation (neural source split). Already installed in the VoiceStudio
    # venv (demucs 4.1.0, CUDA). Run it FIRST, then feed the vocals stem
    # through this script:
    #   python -m demucs --two-stems=vocals -d cuda -o <out> <input>
    #   -> <out>/htdemucs/<stem>/vocals.wav  (keep) + no_vocals.wav (discard)
    # Then: python clean_audio.py <...>/vocals.wav <out_dir>
    #
    # The gate below is still useful for pure noise-floor reduction on an
    # already-separated (or clean) take.
    cleaned = highpass(data, sr, 80.0)
    cleaned = spectral_gate(cleaned, sr)
    cleaned = normalize(cleaned, -1.0)

    suffix = "_cleaned"
    out48 = out_dir / f"{stem}{suffix}_48k.wav"
    out16 = out_dir / f"{stem}{suffix}_16k.wav"
    sf.write(out48, cleaned.astype(np.float32), sr, subtype="PCM_16")
    # downsample to 16 kHz for the LatentSync pipeline
    n16 = int(len(cleaned) * 16000 / sr)
    idx = (np.arange(n16) * sr / 16000).astype(int)
    sf.write(out16, cleaned[idx].astype(np.float32), 16000, subtype="PCM_16")
    print(f"written: {out48}")
    print(f"written: {out16}")


if __name__ == "__main__":
    main()
