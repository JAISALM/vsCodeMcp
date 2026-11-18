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


def smooth_gate(gate, sr, attack_s=0.004, release_s=0.012):
    """Box-smooth a 0/1 gate so chirp edges don't click."""
    k_a = max(1, int(attack_s * sr))
    k_r = max(1, int(release_s * sr))
    kernel = np.ones(k_r - k_a + 1) / (k_r - k_a + 1)
    sm = np.convolve(gate, kernel, mode="same")
    # slight exponential tails at the burst boundaries
    sm = np.clip(sm, 0.0, 1.0)
    return sm


def crickets(n, sr, seed):
    """Distant crickets = STRUCTURED sound (pitched carriers + burst rhythm), not noise.
    Each 'insect': sine carrier with a slight downward drift, amplitude-modulated by a
    chirp pulse train (4 ms on / off at its own rate), grouped into bursts of 0.3-0.6 s
    with random 0.5-1.8 s gaps. Softened with a one-pole LP so it reads distant, not harsh.
    Returns (left, right) float arrays."""
    rng = np.random.default_rng(seed)
    t = np.arange(n) / sr
    # (carrier Hz, amplitude, pan 0=full L..1=full R, chirp rate Hz)
    voices = [
        (5200.0, 0.010, 0.12, 34.0),
        (5900.0, 0.007, 0.88, 29.0),
        (6500.0, 0.0045, 0.45, 38.0),
    ]
    left = np.zeros(n)
    right = np.zeros(n)
    for fc, amp, pan, rate in voices:
        # burst mask: on 0.3-0.6 s, off 0.5-1.8 s, random walk (never repeating)
        burst = np.zeros(n, dtype=np.float32)
        i = int(rng.uniform(0.5, 2.5) * sr)
        while i < n:
            end = min(n, i + int(rng.uniform(0.3, 0.6) * sr))
            burst[i:end] = 1.0
            i = end + int(rng.uniform(0.5, 1.8) * sr)
        # chirp pulse train at this cricket's own rate
        period = 1.0 / rate
        pulse = ((t / period) % 1.0) < (0.004 / period)
        gate = smooth_gate(burst * pulse.astype(np.float32), sr)
        # carrier with a gentle downward drift (real crickets dip)
        drift_hz = 60.0 * np.sin(2 * np.pi * 0.11 * t + rng.uniform(0, 6.28))
        sig = np.sin(2 * np.pi * (fc * t + drift_hz * t / (2 * np.pi)))
        sig = lowpass(sig, 8500.0)
        sig = sig * gate * amp
        g = np.cos(pan * np.pi / 2)
        d = np.sin(pan * np.pi / 2)
        left += sig * g
        right += sig * d
    return left, right


def footstep(bed, n, sr, t_c, amp=0.05):
    """ONE soft distant footstep at exact time t_c (per-action, not random):
    bandpassed body (100-600 Hz) + low thump (65 Hz, fast decay), 12 ms attack / 60 ms decay."""
    i0 = max(0, int((t_c - 0.03) * sr))
    i1 = min(n, int((t_c + 0.09) * sr))
    m = i1 - i0
    if m <= 0:
        return
    rng = np.random.default_rng(1000 + int(round(t_c * 100)))
    tt = np.arange(m) / sr
    body = bandpass(rng.standard_normal(m), 100, 600)
    body = body / (np.max(np.abs(body)) + 1e-9)
    thump = np.sin(2 * np.pi * 65 * tt) * np.exp(-tt / 0.035)
    atk = 0.012
    env = np.zeros(m)
    mm = tt < atk
    env[mm] = tt[mm] / atk
    env[~mm] = np.exp(-(tt[~mm] - atk) / 0.06)
    bed[i0:i1] += (body * 0.5 + thump) * env * amp


def door_creak(bed, n, sr, t0, dur=1.3, amp=0.045):
    """Door creak at exact time t0: ~95 Hz carrier with 17 Hz 'creak' wobble + faint
    190 Hz partial, slow swell (0.5 s) then decay. LOW band only — reads as wood, not static."""
    i0 = max(0, int(t0 * sr))
    i1 = min(n, int((t0 + dur) * sr))
    m = i1 - i0
    if m <= 0:
        return
    tt = np.arange(m) / sr
    car = np.sin(2 * np.pi * 95 * tt) + 0.4 * np.sin(2 * np.pi * 190 * tt)
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 17 * tt)
    env = np.clip(tt / 0.5, 0.0, 1.0) * np.exp(-np.maximum(tt - 0.5, 0.0) / 0.5)
    bed[i0:i1] += car * am * env * amp


def synth(duration, whoosh_times=(), seed=7, gain=1.0, door=None, steps=()):
    """NIGHT bed v3 (user: v2 'feels like static noise' — filtered white noise is
    static under close listening). Real nature STRUCTURE instead:
      - 3 distant crickets (pitched, rhythmic, desynced — the unmistakable summer night)
      - barely-there low wind RUMBLE (<90 Hz — low enough to read as air, not noise)
      - faint room-tone floor
    No broadband hiss anywhere -> no static."""
    n = int(duration * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(seed)

    drift = slow_drift(duration, seed)
    # deep wind rumble — LOW band only (no high frequencies = no 'static' perception)
    rumble = lowpass(rng.standard_normal(n), 90.0)
    rumble = rumble / (np.max(np.abs(rumble)) + 1e-9) * 0.016 * drift
    # room-tone floor
    tone = lowpass(rng.standard_normal(n), 300.0)
    tone = tone / (np.max(np.abs(tone)) + 1e-9) * 0.003

    left = rumble + tone
    right = rumble + tone
    cl, cr = crickets(n, SR, seed)
    left += cl
    right += cr
    bed = (left + right) / 2.0   # mono bed -> stereo identical (keep it simple)

    # --- very soft whoosh at each beat time: LOW band (250-900 Hz = air, not hiss)
    for wt in whoosh_times:
        i0, i1 = int((wt - 0.2) * SR), int((wt + 0.9) * SR)
        i0 = max(0, i0)
        i1 = min(n, i1)
        seg = rng.standard_normal(i1 - i0)
        seg = bandpass(seg, 250, 900)
        seg = seg / (np.max(np.abs(seg)) + 1e-9)
        tt = np.arange(i1 - i0) / SR
        e = np.zeros_like(tt)
        atk = 0.3
        m = tt < atk
        e[m] = (tt[m] / atk) ** 2
        e[~m] = np.exp(-(tt[~m] - atk) / 0.5)
        bed[i0:i1] += seg * e * 0.035

    # --- ACTION SFX at exact timeline times (per-action, not random)
    if door is not None:
        door_creak(bed, n, SR, door)
    for st in steps:
        footstep(bed, n, SR, st)

    # gentle fades + overall gain
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
    ap.add_argument("--door", type=float, default=None,
                    help="door-beat time — adds a low wood creak there (the whoosh is separate)")
    ap.add_argument("--steps", default=None,
                    help="comma-separated exact footstep times, e.g. 5.2,5.6,34.9,35.4,35.9")
    ap.add_argument("--out", required=True)
    ap.add_argument("--video", default=None, help="mix the bed under this video")
    ap.add_argument("--mix-out", default=None)
    a = ap.parse_args()

    whoosh = a.whoosh if a.whoosh else []
    steps = [float(x) for x in a.steps.split(",")] if a.steps else ()
    stereo = synth(a.duration, whoosh, a.seed, a.gain, door=a.door, steps=steps)

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
