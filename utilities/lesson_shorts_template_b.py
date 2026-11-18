#!/usr/bin/env python
"""Template B — neon line-art lesson-shorts ENGINE (data-driven, fully offline).

The @aiishadahir-style contrast card: dark-green ground, white single-stroke
line-art scenes inside rounded cards, gold glow accents, serif caption with
typewriter reveal, gold citation line, series label + progress ring, handle
watermark.

Everything is GEOMETRY (lines/circles/rects/dots/figures/text) — no AI
generation, so the brand is pixel-identical across the series and renders
offline (D228-safe).

USAGE AS AN ENGINE (one content file per video — see lesson_shorts_ubu_al_amal.py):
    from lesson_shorts_template_b import render, encode, figure, lantern, coin, ...
    spec = { "duration": 60.0, "fps": 30, "handle": "@yourhandle",
             "handle_fade": [1.5, 2.1],
             "text": [ ...global text... ],
             "scenes": [ {"t0":0,"t1":6, "card":[x,y,w,h], "card_fade":[...],
                          "elements":[...], "label_gold":"...", "label_sub":"...",
                          "label_fade":[...], "ring":False, "text":[...]} ] }
    render(spec, out_dir); encode(frames_dir, n, fps, out, audio)

TEXT ITEM: {"s": "...", "t0": 1.0, "t1": 3.0, "font": "big|caption|small|cite",
            "align": "left|center", "x": 140, "y": 560, "mode": "type|fade",
            "spacing": 0}

ELEMENT (absolute canvas coords unless the library says local):
  {"kind":"line"|"circle"|"rect"|"dot", "geom":[...], "color":"line|dim|gold|white|muted",
   "width":3, "t0":0.0, "t1":0.4, "glow":1.0, "fill":false, "alpha":255, "pulse":false}

STANDALONE: python utilities\\lesson_shorts_template_b.py = built-in 9 s TAWAKKUL demo.
"""
import argparse
import json
import math
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
SS = 2                       # supersampling: everything drawn at 2x, LANCZOS-downscaled
WW, HH = W * SS, H * SS      # -> anti-aliased lines and text (PIL itself has no AA)
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

F_SERIF = "C:/Windows/Fonts/palai.ttf"      # Palatino italic — matches the ref's italic-serif captions
F_SERIF_UP = "C:/Windows/Fonts/BASKVILL.TTF"  # upright high-contrast serif (closing line)
F_LABEL = "C:/Windows/Fonts/arialbd.ttf"
F_HANDLE = "C:/Windows/Fonts/arial.ttf"

COLORS = {"line": LINE, "dim": DIM, "gold": GOLD, "white": WHITE, "muted": MUTED}
FONT_SIZES = {"big": 64, "caption": 48, "small": 28, "cite": 30, "close": 60}


def ramp(t, t0, t1):
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return max(0.0, min(1.0, (t - t0) / (t1 - t0)))


def partial_polyline(pts, f):
    if f >= 1.0:
        return pts
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(segs)
    if total <= 0:
        return pts
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
    if f >= 1.0:
        return dict(cx=cx, cy=cy, r=r, full=True)
    return dict(cx=cx, cy=cy, r=r, full=False, a0=start_deg, a1=start_deg + 360.0 * f)


def stroke_overlay(ov, kind, geom, color, width, f, glow=1.0, alpha=255, fill=False):
    """All coords arrive in 1080x1920 space; drawn at SSx, downscaled -> AA."""
    if f <= 0.0:
        return
    col = COLORS.get(color, LINE)
    d = ImageDraw.Draw(ov)
    ga = int(30 * glow) * alpha // 255   # ONE subtle halo (wide halos made lines look doubled/muddy)
    ca = int(248 * alpha) // 255        # crisp full-brightness core

    def passes(w_extra, a):
        if a <= 0:
            return
        w_extra = max(2, int(round(w_extra * SS)))
        if kind == "line":
            pts = [[p[0] * SS, p[1] * SS] for p in partial_polyline(geom, f)]
            if len(pts) >= 2:
                d.line(pts, fill=(col[0], col[1], col[2], a), width=w_extra, joint="curve")
        elif kind == "circle":
            cx, cy, r = geom[0] * SS, geom[1] * SS, geom[2] * SS
            c = partial_circle(cx, cy, r, f)
            if c["full"]:
                d.ellipse([cx - r, cy - r, cx + r, cy + r],
                          outline=(col[0], col[1], col[2], a), width=w_extra)
            else:
                d.arc([cx - r, cy - r, cx + r, cy + r], c["a0"], c["a1"],
                      fill=(col[0], col[1], col[2], a), width=w_extra)
        elif kind == "rect":
            x0, y0, x1, y1 = geom[0] * SS, geom[1] * SS, geom[2] * SS, geom[3] * SS
            pts = partial_polyline(rect_perimeter_pts(x0, y0, x1, y1), f)
            d.line(pts, fill=(col[0], col[1], col[2], a), width=w_extra, joint="curve")
            if fill and f >= 1.0:
                d.rectangle([x0, y0, x1, y1], fill=(col[0], col[1], col[2], int(a * 0.45)))
        elif kind == "dot":
            x, y, r = geom[0] * SS, geom[1] * SS, geom[2] * SS * f
            if r > 0.3:
                d.ellipse([x - r, y - r, x + r, y + r], fill=(col[0], col[1], col[2], a))

    if glow > 0:
        passes(width + 4, ga)
    passes(width, ca)


def text_overlay(ov, xy, s, font, color, alpha=255, spacing=0, center=False):
    """xy in 1080x1920 space; fonts are loaded at SSx size."""
    if alpha <= 0 or not s:
        return
    col = COLORS.get(color, WHITE)
    d = ImageDraw.Draw(ov)
    x, y = xy[0] * SS, xy[1] * SS
    if spacing:
        for ch in s:
            d.text((x, y), ch, font=font, fill=(col[0], col[1], col[2], alpha))
            x += d.textlength(ch, font=font) + spacing * SS
    else:
        if center:
            x = xy[0] * SS - d.textlength(s, font=font) / 2
        d.text((x, y), s, font=font, fill=(col[0], col[1], col[2], alpha))


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
        d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=(fill[0], fill[1], fill[2], alpha))
    if outline:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r,
                            outline=(outline[0], outline[1], outline[2], alpha), width=width)


# ---------------------------------------------------------------------------
# scene-element LIBRARY (absolute canvas coords) — the reusable "drawing" kit
# ---------------------------------------------------------------------------
def road(x0, x1, y, t0, t1=None, color="dim"):
    t1 = t1 or t0 + 0.7
    return [dict(kind="line", geom=[[x0, y], [x1, y]], color=color, width=3, t0=t0, t1=t1)]


def bezier_cubic(p0, p1, p2, p3, n=22):
    """Sample a cubic bezier into a dense polyline (smooth flowing limbs)."""
    pts = []
    for i in range(n + 1):
        u = i / n
        w0, w1 = (1 - u) ** 3, 3 * (1 - u) ** 2 * u
        w2, w3 = 3 * (1 - u) * u ** 2, u ** 3
        pts.append([w0 * p0[0] + w1 * p1[0] + w2 * p2[0] + w3 * p3[0],
                    w0 * p0[1] + w1 * p1[1] + w2 * p2[1] + w3 * p3[1]])
    return pts


def figure(x, feet_y, t0, pose="stand", scale=1.0, color="line", glow=1.3, instant=False):
    """A clean single-stroke figure — FLOWING CURVED limbs (cubic bezier), rounded ends.
    pose: stand | walk | carry_L | carry_R.
    instant=True: fully drawn at scene start (continuity across cuts)."""
    s = scale
    head_r = 18 * s
    head_cy = feet_y - 242 * s
    neck_y = head_cy + head_r
    hip_y = feet_y - 108 * s
    sy = feet_y - 176 * s
    if instant:
        t1 = t0 + 0.03
    else:
        t1 = t0 + 0.4

    def el(kind, geom, dt, color_=color, glow_=glow, width=3):
        if instant:
            return dict(kind=kind, geom=geom, color=color_, width=width, t0=t0, t1=t1, glow=glow_)
        return dict(kind=kind, geom=geom, color=color_, width=width, t0=t0 + dt, t1=t0 + dt + 0.4,
                    glow=glow_)

    def limb(pts, dt):
        """limb (curved polyline) + rounded cap at its end."""
        cap_t0 = (t0 + dt + 0.35) if not instant else t0
        cap_t1 = (cap_t0 + 0.3) if not instant else t1
        return [el("line", pts, dt),
                dict(kind="dot", geom=[pts[-1][0], pts[-1][1], 1.9 * s],
                     color=color, width=3, t0=cap_t0, t1=cap_t1, glow=0.0)]

    def curve(p0, c1, c2, p3):
        return bezier_cubic(p0, c1, c2, p3)

    els = [
        el("circle", [x, head_cy, head_r], 0.0),
        el("line", [[x, neck_y + 3], [x, hip_y]], 0.15),          # straight spine
    ]
    if pose == "stand":
        a_l = curve([x - 3 * s, sy + 4 * s], [x - 13 * s, sy + 34 * s],
                    [x - 17 * s, sy + 58 * s], [x - 19 * s, sy + 84 * s])
        a_r = curve([x + 3 * s, sy + 4 * s], [x + 13 * s, sy + 34 * s],
                    [x + 17 * s, sy + 58 * s], [x + 19 * s, sy + 84 * s])
        leg_l = curve([x, hip_y], [x - 5 * s, hip_y + 45 * s],
                      [x - 13 * s, feet_y - 45 * s], [x - 13 * s, feet_y - 2 * s])
        leg_r = curve([x, hip_y], [x + 5 * s, hip_y + 45 * s],
                      [x + 13 * s, feet_y - 45 * s], [x + 13 * s, feet_y - 2 * s])
        els += limb(a_l, 0.3) + limb(a_r, 0.35) + limb(leg_l, 0.5) + limb(leg_r, 0.55)
    elif pose == "walk":
        a_l = curve([x - 3 * s, sy + 4 * s], [x - 14 * s, sy + 32 * s],
                    [x - 16 * s, sy + 56 * s], [x - 15 * s, sy + 80 * s])
        a_r = curve([x + 3 * s, sy + 4 * s], [x + 14 * s, sy + 32 * s],
                    [x + 16 * s, sy + 56 * s], [x + 15 * s, sy + 80 * s])
        leg_l = curve([x, hip_y], [x - 7 * s, hip_y + 40 * s],
                      [x - 24 * s, feet_y - 32 * s], [x - 27 * s, feet_y - 4 * s])
        leg_r = curve([x, hip_y], [x + 9 * s, hip_y + 36 * s],
                      [x + 24 * s, feet_y - 30 * s], [x + 25 * s, feet_y - 2 * s])
        els += limb(a_l, 0.3) + limb(a_r, 0.35) + limb(leg_l, 0.5) + limb(leg_r, 0.55)
    elif pose == "carry_L":  # left arm extended out, holding something
        a_l = curve([x - 3 * s, sy + 4 * s], [x - 20 * s, sy + 28 * s],
                    [x - 36 * s, sy + 46 * s], [x - 46 * s, sy + 58 * s])
        a_r = curve([x + 3 * s, sy + 4 * s], [x + 13 * s, sy + 34 * s],
                    [x + 17 * s, sy + 58 * s], [x + 19 * s, sy + 84 * s])
        leg_l = curve([x, hip_y], [x - 5 * s, hip_y + 45 * s],
                      [x - 13 * s, feet_y - 45 * s], [x - 13 * s, feet_y - 2 * s])
        leg_r = curve([x, hip_y], [x + 5 * s, hip_y + 45 * s],
                      [x + 13 * s, feet_y - 45 * s], [x + 13 * s, feet_y - 2 * s])
        els += limb(a_l, 0.3) + limb(a_r, 0.35) + limb(leg_l, 0.5) + limb(leg_r, 0.55)
    elif pose == "carry_R":
        a_l = curve([x - 3 * s, sy + 4 * s], [x - 13 * s, sy + 34 * s],
                    [x - 17 * s, sy + 58 * s], [x - 19 * s, sy + 84 * s])
        a_r = curve([x + 3 * s, sy + 4 * s], [x + 20 * s, sy + 28 * s],
                    [x + 36 * s, sy + 46 * s], [x + 46 * s, sy + 58 * s])
        leg_l = curve([x, hip_y], [x - 5 * s, hip_y + 45 * s],
                      [x - 13 * s, feet_y - 45 * s], [x - 13 * s, feet_y - 2 * s])
        leg_r = curve([x, hip_y], [x + 5 * s, hip_y + 45 * s],
                      [x + 13 * s, feet_y - 45 * s], [x + 13 * s, feet_y - 2 * s])
        els += limb(a_l, 0.3) + limb(a_r, 0.35) + limb(leg_l, 0.5) + limb(leg_r, 0.55)
    return els


def lantern(x, y, t0, t1=None):
    """Hanging lantern with a GLOWING GOLD core (the 'light for Allah' motif)."""
    t1 = t1 or t0 + 0.8
    return [
        dict(kind="line", geom=[[x - 13, y - 20], [x + 13, y - 20]], color="line", width=3, t0=t0, t1=t0 + 0.3),
        dict(kind="circle", geom=[x, y - 3, 13], color="line", width=3, t0=t0 + 0.2, t1=t1),
        dict(kind="line", geom=[[x - 9, y + 13], [x + 9, y + 13]], color="line", width=3, t0=t0 + 0.4, t1=t0 + 0.7),
        dict(kind="dot", geom=[x, y - 3, 18], color="gold", t0=t0 + 0.5, t1=t0 + 1.0, alpha=80, glow=0.0),
        dict(kind="dot", geom=[x, y - 3, 5.5], color="gold", t0=t0 + 0.5, t1=t0 + 0.8, pulse=True, glow=0.0),
    ]


def coin(x, y, t0, t1=None):
    """Worldly-gain motif: a coin (outer ring + inner ring)."""
    t1 = t1 or t0 + 0.8
    return [
        dict(kind="circle", geom=[x, y, 13], color="line", width=3, t0=t0, t1=t1),
        dict(kind="circle", geom=[x, y, 7], color="dim", width=2, t0=t0 + 0.3, t1=t0 + 0.7),
    ]


def arrow_up(x, y_bottom, height, t0, t1=None, glow=2.5):
    """Gold acceptance arrow (outcome motif)."""
    t1 = t1 or t0 + 0.9
    yt = y_bottom - height
    return [
        dict(kind="line", geom=[[x, y_bottom], [x, yt]], color="gold", width=4, t0=t0, t1=t0 + 0.5, glow=glow),
        dict(kind="line", geom=[[x - 13, yt + 17], [x, yt], [x + 13, yt + 17]], color="gold", width=4,
             t0=t0 + 0.4, t1=t1, glow=glow),
    ]


def ring_circle(x, y, r, t0, t1=None, color="dim", glow=0.0):
    t1 = t1 or t0 + 0.7
    return [dict(kind="circle", geom=[x, y, r], color=color, width=3, t0=t0, t1=t1, glow=glow)]


def door(x0, y0, x1, y1, t0, beam=False):
    """Doorframe + panel + knob (+ optional soft gold beam inside = the way through)."""
    els = [
        dict(kind="rect", geom=[x0, y0, x1, y1], color="line", width=3, t0=t0, t1=t0 + 0.7),
        dict(kind="rect", geom=[x0 + 8, y0 + 8, x1 - 8, y1], color="dim", width=2, t0=t0 + 0.3, t1=t0 + 0.9),
        dict(kind="dot", geom=[x1 - 16, (y0 + y1) / 2, 4], color="dim", t0=t0 + 0.8, t1=t0 + 1.0),
    ]
    if beam:
        els.append(dict(kind="rect", geom=[x0 + 4, y0 + 4, x1 - 4, y1], color="gold", width=2,
                        t0=t0 + 0.5, t1=t0 + 1.2, fill=True, alpha=150, glow=1.5))
    return els


# ---------------------------------------------------------------------------
# renderer
# ---------------------------------------------------------------------------
def render(spec, out_dir, skip_frames=False):
    fps = spec["fps"]
    dur = spec["duration"]
    nframes = int(round(dur * fps))
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    bg = make_bg().resize((WW, HH), Image.BILINEAR)
    stars = make_stars()
    FMAP = {"big": F_SERIF, "caption": F_SERIF, "close": F_SERIF_UP}
    fonts = {k: ImageFont.truetype(FMAP.get(k, F_LABEL), s * SS) for k, s in FONT_SIZES.items()}

    def draw_text_items(ov, items, t, fonts):
        for it in items:
            f = ramp(t, it["t0"], it["t1"])
            if f <= 0:
                continue
            font = fonts.get(it.get("font", "caption"), fonts["caption"])
            color = it.get("color", "white")
            mode = it.get("mode", "fade")
            x, y = it.get("x", W // 2), it.get("y", 800)
            s = it["s"]
            center = it.get("align", "center") == "center"
            a = int(255 * f)
            if mode == "type" and f < 1.0:
                # typing = the animation itself: FULL brightness, no grey ramp, no cursor bar
                shown = s[: int(len(s) * f)]
                text_overlay(ov, (x, y), shown, font, color, 255, it.get("spacing", 0), center)
            else:
                text_overlay(ov, (x, y), s, font, color, a, it.get("spacing", 0), center)

    for fi in range(nframes):
        t = fi / fps
        img = bg.copy()
        ov = Image.new("RGBA", (WW, HH), (0, 0, 0, 0))
        d_ov = ImageDraw.Draw(ov)
        for s in stars:
            a = max(12, min(170, int(s["base"] + 55 * math.sin(2 * math.pi * t * s["freq"] + s["phase"]))))
            r = s["r"] * SS
            d_ov.ellipse([s["x"] * SS - r, s["y"] * SS - r, s["x"] * SS + r, s["y"] * SS + r],
                         fill=(200, 215, 205, a))
        for scene in spec.get("scenes", []):
            if t < scene["t0"] or t >= scene["t1"]:
                continue
            if "card" in scene:
                cx, cy, cw, ch = scene["card"]
                cf = ramp(t, *scene.get("card_fade", [scene["t0"], scene["t0"] + 0.4]))
                if cf > 0:
                    rounded_card(d_ov, cx * SS, cy * SS, cw * SS, ch * SS, 26 * SS,
                                 CARD_BG, CARD_BORDER, max(3, 2 * SS), int(255 * cf))
                for el in scene.get("elements", []):
                    f = ramp(t, el["t0"], el["t1"])
                    if f <= 0:
                        continue
                    alpha = 255
                    if el.get("pulse") and f >= 1.0:
                        alpha = int(255 * (0.8 + 0.2 * math.sin(2 * math.pi * t * 0.8)))
                    alpha = alpha * el.get("alpha", 255) // 255
                    stroke_overlay(ov, el["kind"], el["geom"], el["color"], el.get("width", 3),
                                   f, el.get("glow", 1.0), alpha, el.get("fill", False))
                lf = ramp(t, *scene.get("label_fade", [scene["t0"], scene["t0"] + 0.5]))
                if lf > 0 and scene.get("label_gold"):
                    a = int(255 * lf)
                    cx, cy, ch = scene["card"][0], scene["card"][1], scene["card"][3]
                    # text_overlay scales coords itself — pass 1080x1920 space
                    x, y = cx + 30, cy + ch - 52
                    text_overlay(ov, (x, y), scene["label_gold"], fonts["small"], "gold", a)
                    if scene.get("label_sub"):
                        wlab = d_ov.textlength(scene["label_gold"], font=fonts["small"]) / SS
                        text_overlay(ov, (x + wlab + 18, y + 3),
                                     scene["label_sub"], fonts["small"], "muted", a)
                if scene.get("ring"):
                    rf = ramp(t, *scene.get("ring_fade", [scene["t0"], scene["t0"] + 0.5]))
                    if rf > 0:
                        cx, cy, cw = scene["card"][0], scene["card"][1], scene["card"][2]
                        rcx, rcy, rr = (cx + cw - 50) * SS, (cy + 50) * SS, 22 * SS
                        d_ov.ellipse([rcx - rr, rcy - rr, rcx + rr, rcy + rr],
                                     outline=(60, 85, 72, int(200 * rf)), width=4 * SS)
                        prog = ramp(t, *scene.get("ring_progress", [scene["t0"], scene["t1"]]))
                        if prog > 0:
                            start = -90 + 360 * (t * 0.15)
                            d_ov.arc([rcx - rr, rcy - rr, rcx + rr, rcy + rr], start, start + 360 * prog,
                                     fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * rf)), width=5 * SS)
            draw_text_items(ov, scene.get("text", []), t, fonts)
        draw_text_items(ov, spec.get("text", []), t, fonts)
        a = int(255 * ramp(t, *spec.get("handle_fade", [1.5, 2.1])))
        text_overlay(ov, (W // 2, 1846), spec.get("handle", "@yourhandle"), fonts["small"], "muted",
                     a, center=True)
        img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"))
        img = img.resize((W, H), Image.LANCZOS)          # 2x supersample -> clean AA
        if not skip_frames or not os.path.exists(os.path.join(frames_dir, f"frame_{fi:04d}.png")):
            img.save(os.path.join(frames_dir, f"frame_{fi:04d}.png"))
    return frames_dir, nframes, fps


def encode(frames_dir, nframes, fps, out, audio=None):
    silent = os.path.join(frames_dir, "silent.mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", str(fps),
                    "-i", os.path.join(frames_dir, "frame_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "slow",
                    silent], check=True)
    if audio:
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", silent, "-i", os.path.abspath(audio),
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
    else:
        os.replace(silent, out)
    return out


# ---------------------------------------------------------------------------
# built-in demo (TAWAKKUL contrast card, 9 s)
# ---------------------------------------------------------------------------
def demo_spec():
    top = [
        dict(kind="line", geom=[[60, 520], [900, 520]], color="dim", width=3, t0=0.3, t1=0.9),
        dict(kind="circle", geom=[150, 120, 36], color="line", width=3, t0=0.5, t1=1.0),
        dict(kind="line", geom=[[150, 120], [150, 92]], color="line", width=3, t0=0.9, t1=1.1),
        dict(kind="line", geom=[[150, 120], [172, 132]], color="line", width=3, t0=0.9, t1=1.1),
        dict(kind="rect", geom=[620, 70, 800, 210], color="line", width=3, t0=0.9, t1=1.5),
        dict(kind="line", geom=[[710, 70], [710, 210]], color="dim", width=2, t0=1.4, t1=1.6),
        dict(kind="line", geom=[[620, 140], [800, 140]], color="dim", width=2, t0=1.4, t1=1.6),
        dict(kind="dot", geom=[760, 110, 16], color="white", t0=1.5, t1=1.8),
        dict(kind="circle", geom=[300, 300, 22], color="line", width=3, t0=1.0, t1=1.3),
        dict(kind="line", geom=[[300, 322], [310, 420]], color="line", width=3, t0=1.1, t1=1.4),
        dict(kind="line", geom=[[305, 345], [362, 372]], color="line", width=3, t0=1.2, t1=1.45),
        dict(kind="rect", geom=[362, 352, 432, 422], color="line", width=3, t0=1.3, t1=1.6),
        dict(kind="line", geom=[[310, 420], [288, 520]], color="line", width=3, t0=1.2, t1=1.45),
        dict(kind="line", geom=[[310, 420], [332, 520]], color="line", width=3, t0=1.2, t1=1.45),
        dict(kind="rect", geom=[560, 240, 650, 520], color="dim", width=3, t0=1.5, t1=1.9),
        dict(kind="rect", geom=[690, 240, 780, 520], color="dim", width=3, t0=1.6, t1=2.0),
        dict(kind="rect", geom=[820, 240, 910, 520], color="dim", width=3, t0=1.7, t1=2.1),
        dict(kind="dot", geom=[605, 390, 5], color="dim", t0=1.9, t1=2.1),
        dict(kind="dot", geom=[735, 390, 5], color="dim", t0=2.0, t1=2.2),
        dict(kind="dot", geom=[865, 390, 5], color="dim", t0=2.1, t1=2.3),
    ]
    bot = [
        dict(kind="line", geom=[[60, 440], [900, 440]], color="dim", width=3, t0=6.4, t1=6.9),
        dict(kind="circle", geom=[300, 140, 22], color="line", width=3, t0=6.5, t1=6.8, glow=2),
        dict(kind="line", geom=[[300, 162], [300, 300]], color="line", width=3, t0=6.6, t1=6.9, glow=2),
        dict(kind="line", geom=[[300, 200], [258, 246]], color="line", width=3, t0=6.7, t1=6.95, glow=2),
        dict(kind="line", geom=[[300, 200], [342, 246]], color="line", width=3, t0=6.7, t1=6.95, glow=2),
        dict(kind="line", geom=[[300, 300], [280, 440]], color="line", width=3, t0=6.75, t1=7.05, glow=2),
        dict(kind="line", geom=[[300, 300], [320, 440]], color="line", width=3, t0=6.75, t1=7.05, glow=2),
        dict(kind="rect", geom=[560, 160, 650, 440], color="gold", width=3, t0=6.9, t1=7.3, fill=True, glow=2),
        dict(kind="rect", geom=[700, 160, 790, 440], color="dim", width=3, t0=7.1, t1=7.4),
        dict(kind="rect", geom=[840, 160, 930, 440], color="dim", width=3, t0=7.2, t1=7.5),
    ]
    # card-local -> global for the demo cards
    def shift(els, ox, oy):
        out = []
        for el in els:
            g = el["geom"]
            if el["kind"] == "line":
                g = [[p[0] + ox, p[1] + oy] for p in g]
            elif el["kind"] == "circle":
                g = [g[0] + ox, g[1] + oy, g[2]]
            elif el["kind"] == "rect":
                g = [g[0] + ox, g[1] + oy, g[2] + ox, g[3] + oy]
            else:
                g = [g[0] + ox, g[1] + oy, g[2]]
            e = dict(el)
            e["geom"] = g
            out.append(e)
        return out
    return dict(
        duration=9.0, fps=30, handle="@yourhandle", handle_fade=[2.2, 2.8],
        text=[
            dict(s="“Whoever relies upon Allah,”", t0=2.0, t1=4.4, font="caption", align="left",
                 x=140, y=890, mode="type"),
            dict(s="He is sufficient for him.”", t0=4.2, t1=5.8, font="caption", align="left",
                 x=140, y=968, mode="type"),
            dict(s="SURAH AT-TALAQ  65:3", t0=5.9, t1=6.5, font="cite", color="gold", align="left",
                 x=142, y=1075, spacing=4),
        ],
        scenes=[
            dict(t0=0, t1=9.0, card=[60, 140, 960, 600], card_fade=[0.0, 0.4],
                 elements=shift(top, 60, 140), label_gold="WITHOUT TAWAKKUL",
                 label_sub="carrying it alone", label_fade=[1.9, 2.5]),
            dict(t0=5.8, t1=9.0, card=[60, 1250, 960, 520], card_fade=[5.8, 6.4],
                 elements=shift(bot, 60, 1250), label_gold="WITH TAWAKKUL",
                 label_sub="04 · FUTURE", label_fade=[7.4, 8.0], ring=True,
                 ring_fade=[6.5, 7.0], ring_progress=[6.5, 8.6]),
        ],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", help="scene spec JSON")
    ap.add_argument("--out", default=r"data\refanim\template_b_demo.mp4")
    ap.add_argument("--audio", help="optional wav (Mode A narration / Mode B ambient)")
    ap.add_argument("--frames-dir", help="frames output dir")
    ap.add_argument("--skip-frames", action="store_true")
    args = ap.parse_args()

    spec = json.load(open(args.spec, encoding="utf-8")) if args.spec else demo_spec()
    out = os.path.abspath(args.out)
    frames_dir = os.path.abspath(args.frames_dir or os.path.splitext(out)[0] + "_frames")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    frames_dir, n, fps = render(spec, frames_dir, args.skip_frames)
    print(f"[render] {n} frames @ {fps} fps -> {frames_dir}")
    encode(frames_dir, n, fps, out, args.audio)
    print(f"[done] {out}  (D041: NO music — audio = narration or natural ambient only)")


if __name__ == "__main__":
    main()
