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
  python utilities\synth_ambient.py --duration 48 --gain 0.5 --out out.wav   # half as loud

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


def slow_drift(duration, seed, tau=9.0, depth=0.4):
    """NON-repeating slow amplitude drift (v2 "keep it mild" fix).
    The old two-sine LFO (0.07/0.13 Hz) made a periodic swell that read like
    repeating waves/sea. Instead: random targets every 4 s, smoothed with a
    long one-pole (tau ~9 s) -> organic, never visibly repeating."""
    import math
    n = int(duration * SR)
    rng = np.random.default_rng(seed + 101)
    step = 4.0
    targets = rng.uniform(0.5, 1.0, int(duration / step) + 2)
    a = (1.0 / SR) / (tau + 1.0 / SR)
    y = np.empty(n)
    prev = float(targets[0])
    for i in range(n):
        tgt = targets[min(len(targets) - 1, int(i / SR / step))]
        prev = prev + a * (tgt - prev)
        y[i] = prev
    # center on 0.75, scale the wander to +/- depth
    y = 0.75 + (y - 0.75) * (depth / 0.5)
    return y


def synth(duration, whoosh_times=(), seed=7, gain=1.0):
    n = int(duration * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(seed)

    # --- MILD bed (v2): three quiet layers, all shaped by the non-repeating drift
    # deep rumble (LP 90 Hz) — night air, NOT wave-like
    rumble = lowpass(rng.standard_normal(n), 90.0)
    rumble = rumble / (np.max(np.abs(rumble)) + 1e-9) * 0.020
    # soft high hiss (1.2-3.2 kHz) — distant air movement
    hiss = bandpass(rng.standard_normal(n), 1200.0, 3200.0)
    hiss = hiss / (np.max(np.abs(hiss)) + 1e-9) * 0.012
    # room-tone floor (LP 400 Hz)
    tone = lowpass(rng.standard_normal(n), 400.0)
    tone = tone / (np.max(np.abs(tone)) + 1e-9) * 0.005

    drift = slow_drift(duration, seed)
    bed = (rumble + hiss + tone) * drift

    # --- very soft whoosh at each beat time (felt, not heard)
    for wt in whoosh_times:
        i0, i1 = int((wt - 0.2) * SR), int((wt + 0.9) * SR)
        i0 = max(0, i0)
        i1 = min(n, i1)
        seg = rng.standard_normal(i1 - i0)
        seg = bandpass(seg, 400, 1800)
        seg = seg / (np.max(np.abs(seg)) + 1e-9)
        tt = np.arange(i1 - i0) / SR
        e = np.zeros_like(tt)
        atk = 0.3
        m = tt < atk
        e[m] = (tt[m] / atk) ** 2
        e[~m] = np.exp(-(tt[~m] - atk) / 0.5)
        bed[i0:i1] += seg * e * 0.05                              # ~ -26 dBFS peak

    # gentle fades, then overall gain (target: a whisper bed, easy to focus over)
    fi = int(1.5 * SR)
    fo = int(2.5 * SR)
    bed[:fi] *= np.linspace(0, 1, fi)
    bed[-fo:] *= np.linspace(1, 0, fo)
    bed = bed * gain

    pcm = np.clip(bed * 32767, -32768, 32767).astype(np.int16)
    stereo = np.repeat(pcm[:, None], 2, axis=1)
    return stereo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, default=48.0)
    ap.add_argument("--whoosh", type=float, action="append", default=None)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--gain", type=float, default=1.0,
                    help="final bed multiplier (0.5 = half as loud; v2 default levels are already mild)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--video", default=None, help="mix the bed under this video")
    ap.add_argument("--mix-out", default=None)
    a = ap.parse_args()

    whoosh = a.whoosh if a.whoosh else []
    stereo = synth(a.duration, whoosh, a.seed, a.gain)

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
