# -*- coding: utf-8 -*-
"""Ubu al-Amal PIPELINE (captured 2026-11-18, user: "this is done, capture the
pipeline"). One command reproduces the full 40 s deliverable set:

  1. retime the 48 s content spec to 40 s (uniform 5/6 scale — D241)
  2. render 2400 frames @ 60 fps (Template B engine, 2x supersample, ~35 min)
  3. encode x264 -> ubu_al_amal_40.mp4
  4. synthesize per-action SFX bed at the RETIMED beat times (synth_ambient.py)
  5. mix -> ubu_al_amal_40_sfx.mp4
  6. distribution cuts (user, 2026-11-18): 20 s + 20 s WhatsApp status + 40 s Instagram
     -> ubu_40s_part1.mp4 / ubu_40s_part2.mp4
  7. ffprobe verification of every deliverable

Run:  python utilities\\build_ubu_al_amal.py
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lesson_shorts_template_b as tb
import lesson_shorts_ubu_al_amal as content
from synth_ambient import synth

ROOT = r"D:\models\vsCodeMcp\data\refanim"
FFMPEG = r"D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffmpeg.exe"
FFPROBE = r"D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffprobe.exe"
K = 5.0 / 6.0          # 48 s -> 40 s

# beat times in the 48 s source, scaled to 40 s
DOOR = 33.6 * K        # 28.0  door creak
WHOOSH = 34.3 * K      # 28.58 door whoosh (beam beat)
STEPS_S1 = [5.2 * K, 5.6 * K]                     # figures arrive
STEPS_S4 = [34.9 * K, 35.4 * K, 35.9 * K]        # walk to door


def probe(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,codec_name",
                        "-of", "default=nw=1", path], capture_output=True, text=True)
    return r.stdout.strip().replace("\n", "  ")


def main():
    # 1-3. retime + render + encode
    sp = content.rescale(content.spec(), K)
    assert abs(sp["duration"] - 40.0) < 0.01
    frames_dir = os.path.join(ROOT, "ubu_40_frames")
    frames_dir, n, fps = tb.render(sp, frames_dir)
    print(f"[1-3] {n} frames @ {fps} fps")
    v40 = os.path.join(ROOT, "ubu_al_amal_40.mp4")
    tb.encode(frames_dir, n, fps, v40)
    print(f"[1-3] {v40}")

    # 4-5. per-action SFX bed at retimed beats + mix
    bed = os.path.join(ROOT, "ambient_40.wav")
    stereo = synth(40.0, whoosh_times=[WHOOSH], seed=7, gain=1.0, door=DOOR,
                   steps=STEPS_S1 + STEPS_S4)
    import wave
    with wave.open(bed, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(44100)
        w.writeframes(stereo.tobytes())
    sfx = os.path.join(ROOT, "ubu_al_amal_40_sfx.mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", v40, "-i", bed,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "160k", "-shortest", sfx], check=True)
    print(f"[4-5] {sfx}")

    # 6. distribution cuts (exact 20 s boundaries — re-encode part 2)
    p1 = os.path.join(ROOT, "ubu_40s_part1.mp4")
    p2 = os.path.join(ROOT, "ubu_40s_part2.mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", sfx, "-t", "20",
                    "-c", "copy", p1], check=True)
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "20", "-i", sfx,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19",
                    "-c:a", "aac", "-b:a", "160k", p2], check=True)
    print(f"[6] {p1}\n[6] {p2}")

    # 7. verify
    for p in (v40, sfx, p1, p2):
        print("[verify]", os.path.basename(p), "->", probe(p))
    print("[done] pipeline complete")


if __name__ == "__main__":
    main()
