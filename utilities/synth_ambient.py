r"""Offline synthesized ambience beds — SFX without a model (D228-safe, no queue).

The proper route is ControlFoley TC-V2A (Mode B, user-queues per D192), but that
model is NOT installed (audio_encoders/ is empty) and the machine is offline until
2026-11-24. This helper makes a real ambient bed TODAY, fully offline:

  wind = lowpassed pink-ish noise with two slow gust LFOs
  tone = very low room-tone floor
  whoosh = bandpassed noise swell (for a door / transition beat)

Usage:
  python utilities\synth_ambient.py --duration 48 --whoosh 34.5 --out data\refanim\ambient_48.wav
  python utilities\synth_ambient.py --duration 48 --whoosh 34.5 --video data\refanim\ubu_al_amal.mp4 \
      --mix-out data\refanim\ubu_al_amal_sfx.mp4

D041: NO music — this is natural ambience only (wind + tone + whoosh).
"""
import argparse
import os
import subprocess
import sys

import numpy as np

FFMPEG = r"D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffmpeg.exe"
SR = 44100


def lowpass(x, fc):
    """One-pole lowpass (simple, good enough for beds)."""
    rc = 1.0 / (2 * np.pi * fc)
    dt = 1.0 / SR
    a = dt / (rc + dt)
    y = np.zeros_like(x)
    prev = 0.0
    for i in range(len(x)):
        prev = prev + a * (x[i] - prev)
        y[i] = prev
    return y


def bandpass(x, f0, f1):
    """Rough band: lowpass at f1 minus lowpass at f0 (one-pole each, -6 dB/oct)."""
    return lowpass(x, f1) - lowpass(x, f0)


def env_gust(t, sr, seed):
    rng = np.random.default_rng(seed)
    ph1, ph2 = rng.uniform(0, 2 * np.pi, 2)
    return (0.55 + 0.45 * np.sin(2 * np.pi * 0.07 * t + ph1) * np.sin(2 * np.pi * 0.13 * t + ph2))


def synth(duration, whoosh_times=(), seed=7):
    n = int(duration * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(seed)

    # room tone: lowpass white, very quiet
    tone = lowpass(rng.standard_normal(n), 500.0)
    tone = tone / (np.max(np.abs(tone)) + 1e-9) * 0.006          # ~ -44 dBFS

    # wind: pink-ish noise (LP 400 Hz) with gust envelope
    wind = lowpass(rng.standard_normal(n), 400.0)
    wind = wind / (np.max(np.abs(wind)) + 1e-9)
    gust = env_gust(t, SR, seed)
    wind = wind * gust * 0.06                                     # ~ -24 dBFS gust peaks

    bed = tone + wind

    # whoosh swells at each requested time
    for wt in whoosh_times:
        i0, i1 = int((wt - 0.2) * SR), int((wt + 1.2) * SR)
        i0 = max(0, i0)
        i1 = min(n, i1)
        seg = rng.standard_normal(i1 - i0)
        seg = bandpass(seg, 300, 1400)
        seg = seg / (np.max(np.abs(seg)) + 1e-9)
        tt = np.arange(i1 - i0) / SR
        e = np.zeros_like(tt)
        atk = 0.25
        m = tt < atk
        e[m] = (tt[m] / atk) ** 2
        e[~m] = np.exp(-(tt[~m] - atk) / 0.45)
        bed[i0:i1] += seg * e * 0.16                              # ~ -16 dBFS peak

    # headroom + gentle fades
    bed = bed / (np.max(np.abs(bed)) + 1e-9) * 0.85
    fi = int(1.0 * SR)
    fo = int(2.0 * SR)
    bed[:fi] *= np.linspace(0, 1, fi)
    bed[-fo:] *= np.linspace(1, 0, fo)

    pcm = (bed * 32767).astype(np.int16)
    stereo = np.repeat(pcm[:, None], 2, axis=1)
    return stereo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, default=48.0)
    ap.add_argument("--whoosh", type=float, action="append", default=None)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", required=True)
    ap.add_argument("--video", default=None, help="mix the bed under this video")
    ap.add_argument("--mix-out", default=None)
    a = ap.parse_args()

    whoosh = a.whoosh if a.whoosh else []
    stereo = synth(a.duration, whoosh, a.seed)

    import wave
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())
    print(f"[synth] {a.out}  {a.duration:.1f}s  whoosh={whoosh}")

    if a.video and a.mix_out:
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", a.video, "-i", a.out,
               "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
               "-b:a", "160k", "-shortest", a.mix_out]
        subprocess.run(cmd, check=True)
        print(f"[mix] {a.mix_out}")


if __name__ == "__main__":
    sys.exit(main())
