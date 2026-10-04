# -*- coding: utf-8 -*-
"""Detect speech windows (voice activity) inside each intro clip.

Uses ffmpeg to dump mono 16 kHz PCM, computes per-0.5s RMS, and reports the
contiguous windows where speech is present. This is a PROXY for where the
Malayalam dub will sit (the H3-generated audio occupies the same windows), so
subtitles can be timed to the actual words rather than spread evenly.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\analyze_speech_windows.py"
"""
import subprocess, struct, math, os, sys

FFMPEG = r"D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffmpeg.exe"
DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_intro_final"
CLIPS = [
    ("A",  "jaisal_intro_A_walkin_2k.mp4"),
    ("B",  "jaisal_intro_B_setup_00007_2k.mp4"),
    ("C",  "jaisal_intro_C_starting_2ref_00007_2k.mp4"),
    ("D",  "jaisal_intro_D_reverse_00007_2k.mp4"),
    ("E",  "jaisal_intro_E_plants_00002_2k.mp4"),
    ("F1", "jaisal_intro_F_plants_die_00005_2k.mp4"),
    ("F2", "jaisal_intro_F_plants_die_00007_2k.mp4"),
    ("G",  "jaisal_intro_G_papers_00008_2k.mp4"),
]
SR = 16000
WIN = 0.5


def rms_windows(path):
    cmd = [FFMPEG, "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"]
    data = subprocess.run(cmd, capture_output=True).stdout
    n = len(data) // 2
    if n == 0:
        return []
    samples = struct.unpack("<%dh" % n, data[: n * 2])
    win_n = int(SR * WIN)
    rms = []
    for i in range(0, n, win_n):
        chunk = samples[i : i + win_n]
        if len(chunk) < win_n // 2:
            break
        s = sum(x * x for x in chunk) / len(chunk)
        rms.append(math.sqrt(s))
    return rms


def find_speech(rms):
    if not rms:
        return []
    mx = max(rms)
    thr = max(mx * 0.20, 250)
    speech = [i for i, r in enumerate(rms) if r >= thr]
    if not speech:
        return []
    groups = []
    start = prev = speech[0]
    for i in speech[1:]:
        if i == prev + 1:
            prev = i
        else:
            groups.append((start, prev))
            start = prev = i
    groups.append((start, prev))
    merged = [groups[0]]
    for g in groups[1:]:
        if g[0] - merged[-1][1] <= 1:
            merged[-1] = (merged[-1][0], g[1])
        else:
            merged.append(g)
    return [(round(a * WIN, 1), round((b + 1) * WIN, 1)) for a, b in merged]


def main():
    print("clip | dur(s) | max_rms | speech windows (start-end within clip)")
    for name, f in CLIPS:
        p = os.path.join(DIR, f)
        if not os.path.exists(p):
            print(f"{name}: MISSING {f}")
            continue
        rms = rms_windows(p)
        if not rms:
            print(f"{name}: no audio")
            continue
        mx = max(rms)
        sw = find_speech(rms)
        print(f"{name} | {len(rms)*WIN:.1f}s | {mx:.0f} | {sw}")


if __name__ == "__main__":
    main()
