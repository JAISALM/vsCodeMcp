# -*- coding: utf-8 -*-
"""GENERIC DAILY EXPLAINER PIPELINE (Channel-1, D250 format — built 2026-11-19,
D252: "build the pipeline for ourself"). One command per day:

  python utilities\\build_daily.py 2026-11-26 --spec data\\daily\\2026-11-26\\spec.json

  1. loads the day's spec JSON (Template B schema — same as the Ubu spec)
  2. palette AUTO from the weekday (Mon=A_green … Sun=G_plum; launch day
     Wed 25th = C_amber = Ubu — verified against D244)
  3. renders 2400 frames @ 60 fps (2x supersample) -> encodes <slug>.mp4
  4. optional SFX bed (spec["sfx"] = {whoosh:[t], door:[t], steps:[t],
     seed, gain} -> synth_ambient; natural sounds only, D041)
  5. distribution cuts when duration ~= 40 s: <slug>_part1.mp4 (0-20 s,
     stream copy) + <slug>_part2.mp4 (20 s+, re-encode) — the 2026-11-18
     standard (2x 20 s WhatsApp status + 40 s Instagram)
  6. ffprobe verification of every output

Everything lands in data\\daily\\<date>\\. The day-1 instance (Ubu) is
reproduced by:  python utilities\\build_daily.py 2026-11-25 --spec
data\\daily\\2026-11-25\\spec.json  (spec = the Ubu spec, slug "ubu_al_amal")

Flags:  --frames-only  (render frames, skip encode/cuts)
        --preview T    (single-frame preview at time T, skip the full render)
        --palette NAME (override the weekday palette)
        --no-cuts      (skip the 20 s distribution cuts)
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lesson_shorts_template_b as tb

ROOT = r"D:\models\vsCodeMcp\data\daily"
FFMPEG = r"D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffmpeg.exe"
FFPROBE = r"D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffprobe.exe"

# weekday -> palette (D244: 7 palettes = 7 weekdays; launch Wed 25th = C_amber)
WEEKDAY_PALETTE = {
    "Mon": "A_green", "Tue": "B_indigo", "Wed": "C_amber", "Thu": "D_slate",
    "Fri": "E_teal", "Sat": "F_clay", "Sun": "G_plum",
}
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def probe(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,codec_name",
                        "-of", "default=nw=1", path], capture_output=True, text=True)
    return r.stdout.strip().replace("\n", "  ")


def main():
    if len(sys.argv) < 2 or not sys.argv[1][:4].isdigit():
        print(__doc__)
        sys.exit(1)
    date = sys.argv[1]
    spec_path = None
    palette = None
    frames_only = "--frames-only" in sys.argv
    no_cuts = "--no-cuts" in sys.argv
    preview_t = None
    for i, a in enumerate(sys.argv):
        if a == "--spec":
            spec_path = sys.argv[i + 1]
        elif a == "--palette":
            palette = sys.argv[i + 1]
        elif a == "--preview":
            preview_t = float(sys.argv[i + 1])
    if not spec_path:
        sys.exit("spec required: --spec data\\daily\\<date>\\spec.json")

    import datetime
    d = datetime.date.fromisoformat(date)
    pal = palette or WEEKDAY_PALETTE[DOW[d.weekday()]]
    print(f"[0] {date} ({DOW[d.weekday()]}) -> palette {pal}"
          + (f" (override: {palette})" if palette else " (auto)"))

    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    slug = spec.get("slug", date)
    outdir = os.path.join(ROOT, date)
    os.makedirs(outdir, exist_ok=True)

    # optional single-frame preview (fast palette/format check before a full render)
    if preview_t is not None:
        fn = os.path.join(outdir, f"{slug}_preview_t{preview_t}.png")
        tb.preview(spec, preview_t, fn, palette=pal)
        print(f"[preview] {fn} (palette {pal})")
        return

    # 1-3. render + encode
    frames_dir = os.path.join(outdir, f"{slug}_frames")
    frames_dir, n, fps = tb.render(spec, frames_dir, palette=pal)
    print(f"[1-3] {n} frames @ {fps} fps")
    if frames_only:
        print("[frames-only] stopping before encode")
        return
    full = os.path.join(outdir, f"{slug}.mp4")
    tb.encode(frames_dir, n, fps, full)
    print(f"[1-3] {full}")

    # 4. optional SFX bed at spec beats (natural sounds only — D041)
    src = full
    sfx_spec = spec.get("sfx")
    if sfx_spec:
        from synth_ambient import synth
        import wave
        dur = spec.get("duration", 40.0)
        stereo = synth(dur, whoosh_times=sfx_spec.get("whoosh", []),
                       seed=sfx_spec.get("seed", 7), gain=sfx_spec.get("gain", 1.0),
                       door=sfx_spec.get("door"), steps=sfx_spec.get("steps", []))
        bed = os.path.join(outdir, f"{slug}_bed.wav")
        with wave.open(bed, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(44100)
            w.writeframes(stereo.tobytes())
        sfx = os.path.join(outdir, f"{slug}_sfx.mp4")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", full, "-i", bed,
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                        "-b:a", "160k", "-shortest", sfx], check=True)
        src = sfx
        print(f"[4] {sfx}")

    # 5. distribution cuts (only for ~40 s videos)
    outs = [full] if sfx_spec is None else [full, src]
    dur = spec.get("duration", 40.0)
    if abs(dur - 40.0) < 0.05 and not no_cuts:
        p1 = os.path.join(outdir, f"{slug}_part1.mp4")
        p2 = os.path.join(outdir, f"{slug}_part2.mp4")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-t", "20",
                        "-c", "copy", p1], check=True)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "20", "-i", src,
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19",
                        "-c:a", "aac", "-b:a", "160k", p2], check=True)
        print(f"[5] {p1}\n[5] {p2}")
        outs += [p1, p2]

    # 6. verify
    for p in outs:
        print("[verify]", os.path.basename(p), "->", probe(p))
    print("[done] daily pipeline complete —", outdir)


if __name__ == "__main__":
    main()
