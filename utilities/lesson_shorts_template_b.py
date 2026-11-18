#!/usr/bin/env python
"""Template B — neon line-art lesson-short renderer (data-driven, fully offline).

The @aiishadahir-style contrast card: dark-green ground, white single-stroke line-art
scenes inside rounded cards, gold glow accents, serif caption with typewriter reveal,
gold citation line, series label + progress ring, handle watermark.

Everything is GEOMETRY (lines/circles/rects/dots/text) — no AI generation, so the brand
is pixel-identical across the whole series and renders offline (D228-safe).

Usage:
  python utilities\\lesson_shorts_template_b.py --out data\\refanim\\template_b_demo.mp4
  python utilities\\lesson_shorts_template_b.py --out out.mp4 --audio narration.wav
  python utilities\\lesson_shorts_template_b.py --spec scene.json --out out.mp4

--spec JSON schema: {"duration": 9.0, "fps": 30, "handle": "@yourhandle",
 "caption": ["line1", "line2"], "citation": "SURAH AT-TALAQ  65:3",
 "cards": [ {"frame": [x,y,w,h], "label_gold": "WITHOUT TAWAKKUL",
            "label_sub": "carrying it alone", "elements": [ ... ],
            "ring": true, "label_fade": [t0,t1]} ],
 "caption_timings": {"line1": [t0,t1], "line2": [t0,t1], "citation": [t0,t1]},
 "handle_fade": [t0,t1]}
Element: {"kind": "line"|"circle"|"rect"|"dot", "geom": [...], "color": "line"|"dim"|"gold"|"white",
          "width": 3, "t0": 0.0, "t1": 0.4, "glow": 1.0, "fill": false, "pulse": false}
  line  geom = [[x0,y0],[x1,y1],...]
  circle geom = [cx,cy,r]
  rect  geom = [x0,y0,x1,y1]
  dot   geom = [x,x,y,r]

Demo scene (no --spec): the TAWAKKUL contrast card (9 s), matching the reference layout.
Encode: PNG sequence -> ffmpeg libx264 yuv420p crf 19; optional --audio mux (Mode A
narration / Mode B ambient — D041: NO music ever).
"""
import argparse
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FFMPEG = r"D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffmpeg.exe"

BG_TOP = (10, 26, 18)
BG_BOT = (5, 13, 9)
CARD_BG = (14, 33, 24)
CARD_BORDER = (38, 70, 54)
LINE = (232, 240, 233)
DIM = (140, 158, 148)
GOLD = (212, 169, 78)
WHITE = (238, 242, 238)
MUTED = (150, 165, 155)

F_SERIF = "C:/Windows/Fonts/georgia.ttf"
F_SERIF_B = "C:/Windows/Fonts/georgiab.ttf"
F_LABEL = "C:/Windows/Fonts/arialbd.ttf"
F_HANDLE = "C:/Windows/Fonts/arial.ttf"

COLORS = {"line": LINE, "dim": DIM, "gold": GOLD, "white": WHITE, "muted": MUTED}


def ramp(t, t0, t1):
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return max(0.0, min(1.0, (t - t0) / (t1 - t0)))


def poly_len(pts):
    return [sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))]


def partial_polyline(pts, f):
    """First f (0..1) of the polyline by arc length."""
    if f >= 1.0:
        return pts
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(segs)
    target = total * f
    out = [pts[0]]
    acc = 0.0
    for i, s in enumerate(segs):
        if acc + s <= target:
            out.append(pts[i + 1])
            acc += s
        else:
            rem = target - acc
            if s > 0:
                k = rem / s
                a, b = pts[i], pts[i + 1]
                out.append([a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k])
            return out
    return out


def rect_perimeter_pts(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]


def partial_circle(cx, cy, r, f, start_deg=-90.0):
    """Circle/arc from start_deg covering f*360 degrees; returns arc bbox+angles or full."""
    if f >= 1.0:
        return dict(cx=cx, cy=cy, r=r, full=True)
    span = 360.0 * f
    return dict(cx=cx, cy=cy, r=r, full=False, a0=start_deg, a1=start_deg + span)


def stroke_overlay(ov, kind, geom, color, width, f, glow=1.0, alpha=255, fill=False):
    """Draw one element at reveal fraction f onto RGBA overlay (glow pass + core pass)."""
    if f <= 0.0:
        return
    col = COLORS.get(color, LINE)
    d = ImageDraw.Draw(ov)
    ga = int(55 * glow) * alpha // 255
    ca = int(235 * alpha) // 255

    def passes(w_extra, a):
        if a <= 0:
            return
        if kind == "line":
            pts = partial_polyline(geom, f)
            if len(pts) >= 2:
                d.line(pts, fill=(col[0], col[1], col[2], a), width=w_extra,
                       joint="curve")
        elif kind == "circle":
            cx, cy, r = geom
            c = partial_circle(cx, cy, r, f)
            if c["full"]:
                d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(col[0], col[1], col[2], a),
                          width=w_extra)
            else:
                d.arc([cx - r, cy - r, cx + r, cy + r], c["a0"], c["a1"],
                      fill=(col[0], col[1], col[2], a), width=w_extra)
        elif kind == "rect":
            x0, y0, x1, y1 = geom
            pts = partial_polyline(rect_perimeter_pts(x0, y0, x1, y1), f)
            d.line(pts, fill=(col[0], col[1], col[2], a), width=w_extra, joint="curve")
            if fill and f >= 1.0:
                d.rectangle([x0, y0, x1, y1], fill=(col[0], col[1], col[2], max(0, a - 120)))
        elif kind == "dot":
            x, y, r = geom[0], geom[1], geom[2] * f
            if r > 0.3:
                d.ellipse([x - r, y - r, x + r, y + r], fill=(col[0], col[1], col[2], a))

    if glow > 0:
        passes(width + 7, ga)
        if glow > 1.5:
            passes(width + 12, max(0, ga - 30))
    passes(width, ca)


def text_overlay(ov, xy, s, font, color, alpha=255, spacing=0, center=False):
    if alpha <= 0 or not s:
        return
    col = COLORS.get(color, WHITE)
    d = ImageDraw.Draw(ov)
    if spacing:
        x, y = xy
        for ch in s:
            wch = d.textlength(ch, font=font)
            d.text((x, y), ch, font=font, fill=(col[0], col[1], col[2], alpha))
            x += wch + spacing
    else:
        if center:
            tw = d.textlength(s, font=font)
            xy = (xy[0] - tw / 2, xy[1])
        d.text(xy, s, font=font, fill=(col[0], col[1], col[2], alpha))


def make_bg():
    bg = np.zeros((H, W, 3), dtype=np.uint8)
    top, bot = np.array(BG_TOP, np.float32), np.array(BG_BOT, np.float32)
    for y in range(H):
        bg[y, :] = (top + (bot - top) * (y / H)).astype(np.uint8)
    return Image.fromarray(bg)


def make_stars():
    rng = np.random.default_rng(7)
    stars = []
    for _ in range(46):
        stars.append(dict(x=float(rng.uniform(30, W - 30)), y=float(rng.uniform(40, H - 120)),
                          r=float(rng.uniform(1.2, 2.4)), phase=float(rng.uniform(0, 2 * math.pi)),
                          freq=float(rng.uniform(0.25, 0.55)), base=float(rng.uniform(50, 110))))
    return stars


def rounded_card(d, x, y, w, h, r, fill, outline, width=2, alpha=255):
    if alpha <= 0:
        return
    if fill:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r,
                            fill=(fill[0], fill[1], fill[2], alpha))
    if outline:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r,
                            outline=(outline[0], outline[1], outline[2], alpha), width=width)


def demo_spec():
    # ---- top card scene: carrying it alone (clock, window+moon, figure+box, 3 locked doors)
    top = [
        dict(kind="line", geom=[[60, 520], [900, 520]], color="dim", width=3, t0=0.3, t1=0.9),
        dict(kind="circle", geom=[150, 120, 36], color="line", width=3, t0=0.5, t1=1.0),
        dict(kind="line", geom=[[150, 120], [150, 92]], color="line", width=3, t0=0.9, t1=1.1),
        dict(kind="line", geom=[[150, 120], [172, 132]], color="line", width=3, t0=0.9, t1=1.1),
        dict(kind="rect", geom=[620, 70, 800, 210], color="line", width=3, t0=0.9, t1=1.5),
        dict(kind="line", geom=[[710, 70], [710, 210]], color="dim", width=2, t0=1.4, t1=1.6),
        dict(kind="line", geom=[[620, 140], [800, 140]], color="dim", width=2, t0=1.4, t1=1.6),
        dict(kind="dot", geom=[760, 110, 16], color="white", t0=1.5, t1=1.8),
        # figure carrying box
        dict(kind="circle", geom=[300, 300, 22], color="line", width=3, t0=1.0, t1=1.3),
        dict(kind="line", geom=[[300, 322], [310, 420]], color="line", width=3, t0=1.1, t1=1.4),
        dict(kind="line", geom=[[305, 345], [362, 372]], color="line", width=3, t0=1.2, t1=1.45),
        dict(kind="rect", geom=[362, 352, 432, 422], color="line", width=3, t0=1.3, t1=1.6),
        dict(kind="line", geom=[[310, 420], [288, 520]], color="line", width=3, t0=1.2, t1=1.45),
        dict(kind="line", geom=[[310, 420], [332, 520]], color="line", width=3, t0=1.2, t1=1.45),
        # 3 locked doors
        dict(kind="rect", geom=[560, 240, 650, 520], color="dim", width=3, t0=1.5, t1=1.9),
        dict(kind="rect", geom=[690, 240, 780, 520], color="dim", width=3, t0=1.6, t1=2.0),
        dict(kind="rect", geom=[820, 240, 910, 520], color="dim", width=3, t0=1.7, t1=2.1),
        dict(kind="dot", geom=[605, 390, 5], color="dim", t0=1.9, t1=2.1),
        dict(kind="dot", geom=[735, 390, 5], color="dim", t0=2.0, t1=2.2),
        dict(kind="dot", geom=[865, 390, 5], color="dim", t0=2.1, t1=2.3),
    ]
    # ---- bottom card scene: standing, glowing, first door open in gold
    bot = [
        dict(kind="line", geom=[[60, 440], [900, 440]], color="dim", width=3, t0=6.4, t1=6.9),
        dict(kind="circle", geom=[300, 140, 22], color="line", width=3, t0=6.5, t1=6.8, glow=2),
        dict(kind="line", geom=[[300, 162], [300, 300]], color="line", width=3, t0=6.6, t1=6.9, glow=2),
        dict(kind="line", geom=[[300, 200], [258, 246]], color="line", width=3, t0=6.7, t1=6.95, glow=2),
        dict(kind="line", geom=[[300, 200], [342, 246]], color="line", width=3, t0=6.7, t1=6.95, glow=2),
        dict(kind="line", geom=[[300, 300], [280, 440]], color="line", width=3, t0=6.75, t1=7.05, glow=2),
        dict(kind="line", geom=[[300, 300], [320, 440]], color="line", width=3, t0=6.75, t1=7.05, glow=2),
        # open door (gold) + two closed (card-local; right edge <= 930 to stay inside)
        dict(kind="rect", geom=[560, 160, 650, 440], color="gold", width=3, t0=6.9, t1=7.3,
             fill=True, glow=2),
        dict(kind="rect", geom=[700, 160, 790, 440], color="dim", width=3, t0=7.1, t1=7.4),
        dict(kind="rect", geom=[840, 160, 930, 440], color="dim", width=3, t0=7.2, t1=7.5),
    ]
    return dict(
        duration=9.0, fps=30, handle="@yourhandle", handle_fade=[2.2, 2.8],
        caption=["“Whoever relies upon Allah,”", "He is sufficient for him.”"],
        citation="SURAH AT-TALAQ  65:3",
        caption_timings={"line1": [2.0, 4.4], "line2": [4.2, 5.8], "citation": [5.9, 6.5]},
        cards=[
            dict(frame=[60, 140, 960, 600], elements=top,
                 label_gold="WITHOUT TAWAKKUL", label_sub="carrying it alone",
                 label_fade=[1.9, 2.5], ring=False, card_fade=[0.0, 0.4]),
            dict(frame=[60, 1250, 960, 520], elements=bot,
                 label_gold="WITH TAWAKKUL", label_sub="04 · FUTURE",
                 label_fade=[7.4, 8.0], ring=True, ring_fade=[6.5, 7.0], card_fade=[5.8, 6.4]),
        ],
    )


def render(spec, out_dir, skip_frames=False):
    fps = spec["fps"]
    dur = spec["duration"]
    nframes = int(round(dur * fps))
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    bg = make_bg()
    stars = make_stars()
    f_serif = ImageFont.truetype(F_SERIF, 58)
    f_cit = ImageFont.truetype(F_LABEL, 30)
    f_lab = ImageFont.truetype(F_LABEL, 30)
    f_sub = ImageFont.truetype(F_HANDLE, 26)
    f_hand = ImageFont.truetype(F_HANDLE, 34)

    for fi in range(nframes):
        t = fi / fps
        img = bg.copy()
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # stars (twinkle)
        for s in stars:
            a = int(s["base"] + 55 * math.sin(2 * math.pi * (t * s["freq"]) + s["phase"]))
            a = max(12, min(170, a))
            r = s["r"]
            ImageDraw.Draw(ov).ellipse([s["x"] - r, s["y"] - r, s["x"] + r, s["y"] + r],
                                       fill=(200, 215, 205, a))
        # cards + elements
        for card in spec["cards"]:
            cx, cy, cw, ch = card["frame"]
            cf = ramp(t, *card.get("card_fade", [0.0, 0.4]))
            if cf > 0:
                ca = int(255 * cf)
                rounded_card(ImageDraw.Draw(ov), cx, cy, cw, ch, 26, CARD_BG, CARD_BORDER, 2, ca)
            for el in card["elements"]:
                f = ramp(t, el["t0"], el["t1"])
                if f <= 0:
                    continue
                geom = list(el["geom"])
                # card-local coords -> global
                if el["kind"] == "line":
                    geom = [[p[0] + cx, p[1] + cy] for p in geom]
                elif el["kind"] == "circle":
                    geom = [geom[0] + cx, geom[1] + cy, geom[2]]
                elif el["kind"] == "rect":
                    geom = [geom[0] + cx, geom[1] + cy, geom[2] + cx, geom[3] + cy]
                elif el["kind"] == "dot":
                    geom = [geom[0] + cx, geom[1] + cy, geom[2]]
                alpha = 255
                if el.get("pulse") and f >= 1.0:
                    alpha = int(255 * (0.85 + 0.15 * math.sin(2 * math.pi * t * 0.8)))
                stroke_overlay(ov, el["kind"], geom, el["color"], el.get("width", 3), f,
                               el.get("glow", 1.0), alpha, el.get("fill", False))
            # card label
            lf = ramp(t, *card.get("label_fade", [0.0, 0.5]))
            if lf > 0:
                a = int(255 * lf)
                lab = card["label_gold"]
                x = cx + 30
                y = cy + ch - 52
                text_overlay(ov, (x, y), lab, f_lab, "gold", a)
                if card.get("label_sub"):
                    wlab = ImageDraw.Draw(ov).textlength(lab, font=f_lab)
                    text_overlay(ov, (x + wlab + 18, y + 3), card["label_sub"], f_sub,
                                 "muted", a)
            # progress ring (top-right of card)
            if card.get("ring"):
                rf = ramp(t, *card.get("ring_fade", [0.0, 0.5]))
                if rf > 0:
                    rcx, rcy, rr = cx + cw - 50, cy + 50, 22
                    ImageDraw.Draw(ov).ellipse([rcx - rr, rcy - rr, rcx + rr, rcy + rr],
                                               outline=(60, 85, 72, int(200 * rf)), width=4)
                    prog = ramp(t, 6.5, 8.6)
                    if prog > 0:
                        start = -90 + 360 * (t * 0.15)
                        ImageDraw.Draw(ov).arc([rcx - rr, rcy - rr, rcx + rr, rcy + rr],
                                              start, start + 360 * prog,
                                              fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * rf)),
                                              width=5)
        # caption typewriter
        ct = spec.get("caption_timings", {})
        for i, line in enumerate(spec.get("caption", [])):
            key = f"line{i + 1}"
            t0, t1 = ct.get(key, [1.0, 3.0])
            f = ramp(t, t0, t1)
            if f <= 0:
                continue
            n = int(len(line) * f)
            shown = line[:n]
            a = 255
            y = 890 + i * 78
            text_overlay(ov, (140, y), shown, f_serif, "white", a)
            if 0 < f < 1:
                wch = ImageDraw.Draw(ov).textlength(shown, font=f_serif)
                ImageDraw.Draw(ov).rectangle([140 + wch + 4, y + 8, 140 + wch + 10, y + 56],
                                             fill=(GOLD[0], GOLD[1], GOLD[2], 230))
        # citation
        if spec.get("citation"):
            a = int(255 * ramp(t, *ct.get("citation", [5.5, 6.1])))
            text_overlay(ov, (142, 1075), spec["citation"], f_cit, "gold", a, spacing=4)
        # handle
        a = int(255 * ramp(t, *spec.get("handle_fade", [2.0, 2.6])))
        text_overlay(ov, (W // 2, 1846), spec["handle"], f_hand, "muted", a, center=True)
        img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"))
        if not skip_frames or not os.path.exists(os.path.join(frames_dir, f"frame_{fi:04d}.png")):
            img.save(os.path.join(frames_dir, f"frame_{fi:04d}.png"))
    return frames_dir, nframes, fps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", help="scene spec JSON (default: built-in TAWAKKUL demo)")
    ap.add_argument("--out", default=r"data\refanim\template_b_demo.mp4")
    ap.add_argument("--audio", help="optional wav (Mode A narration / Mode B ambient)")
    ap.add_argument("--frames-dir", help="frames output dir (default: <out>_frames)")
    ap.add_argument("--skip-frames", action="store_true")
    args = ap.parse_args()

    spec = json.load(open(args.spec, encoding="utf-8")) if args.spec else demo_spec()
    out = os.path.abspath(args.out)
    frames_dir = os.path.abspath(args.frames_dir or os.path.splitext(out)[0] + "_frames")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    frames_dir, n, fps = render(spec, frames_dir, args.skip_frames)
    print(f"[render] {n} frames @ {fps} fps -> {frames_dir}")

    silent = frames_dir + os.path.sep + "silent.mp4"
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-framerate", str(fps),
           "-i", os.path.join(frames_dir, "frame_%04d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "slow", silent]
    subprocess.run(cmd, check=True)
    print(f"[encode] silent -> {silent}")
    if args.audio:
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", silent, "-i",
               os.path.abspath(args.audio), "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
               "-shortest", out]
        subprocess.run(cmd, check=True)
    else:
        os.replace(silent, out)
    print(f"[done] {out}  (D041: NO music — audio = narration or natural ambient only)")


if __name__ == "__main__":
    main()
