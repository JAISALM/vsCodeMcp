#!/usr/bin/env python
"""Ubu al-Amal — "Actions are by intentions" — 40 s Template B video.

TIMING PRINCIPLE (user, 2026-11-18): the length serves the CONTENT, not a
format goal. The first version padded 5 beats to 60 s; the beats now run
tight — 40 s total, no dead air.

CITATION (USER-VERIFIED before publish):
  "Innamal a'malu bin niyyat, wa li-kulli maridhin ma nawaa..."
  (Actions are by intentions; each person will have what they intended;
   whoever's hijrah was for Allah and His Messenger, his hijrah was to
   Allah and His Messenger.) — SAHIH AL-BUKHARI 1 (also Muslim 1907).
  Note: this is the FIRST hadith of Sahih al-Bukhari.

AUDIO: Mode B target — text + natural sound (no voice, NO music, D041).
  Stage after render: ControlFoley TC-V2A on this video (user queues, D192) —
  suggested ambient in story order: quiet room tone, soft night wind, gentle
  footsteps, a soft whoosh at the door, calm night ambience.

Run:  python utilities\\lesson_shorts_ubu_al_amal.py
Out:  data\\refanim\\ubu_al_amal.mp4
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lesson_shorts_template_b import (render, encode, figure, road, lantern,
                                      coin, arrow_up, ring_circle, door, W)

CARD = [60, 880, 960, 600]      # card frame (x, y, w, h)
FEET = 1380                     # road / feet line (global y = card_y 880 + local 500)
FXL, FXR = 390, 690            # left / right figure x


def card_scene(t0, t1, label, label_fade, elements, text, card_fade=None, fadeout=None):
    """fadeout [a,b] = the scene's exit window. Consecutive scenes OVERLAP by that
    window, so cards dissolve into each other instead of hard-cutting."""
    return dict(t0=t0, t1=t1, card=CARD, card_fade=card_fade or [t0 + 0.4, t0 + 0.9],
                fadeout=fadeout or [t1 - 0.7, t1],
                elements=elements, label_gold=label, label_sub="", label_fade=label_fade,
                text=text)


def T(s, t0, t1, y, mode="slide"):
    """mode="slide" (default) = eased slide-up + fade, the ref's text motion."""
    return dict(s=s, t0=t0, t1=t1, font="caption", color="white", align="center",
                x=W // 2, y=y, mode=mode)


def spec():
    return dict(
        duration=40.0, fps=30, handle="@yourhandle", handle_fade=[1.5, 2.1],
        text=[],
        scenes=[
            # ---- S0 hook (0-4.5) — two lines, no padding line; dissolves into S1 ----
            dict(t0=0, t1=4.5, fadeout=[3.9, 4.5], text=[
                dict(s="TWO PEOPLE.", t0=0.7, t1=1.9, font="big", align="center",
                     x=W // 2, y=800),
                dict(s="THE SAME WORK.", t0=1.7, t1=2.9, font="big", align="center",
                     x=W // 2, y=890),
            ]),
            # ---- S1 the same action (3.8-12, overlaps S0 by 0.7 s) ----
            card_scene(3.8, 12, "THE SAME ACTION", [5.3, 5.9],
                       road(120, 960, FEET, 4.9)
                       + figure(FXL, FEET, 5.2, pose="walk")
                       + figure(FXR, FEET, 5.5, pose="walk"),
                       [T("They prayed the same prayers.", 5.8, 7.8, 560),
                        T("They worked the same hours.", 7.6, 9.6, 640)],
                       fadeout=[11.3, 12.0]),
            # ---- S2 two intentions (11.3-22) ----
            card_scene(11.3, 22, "TWO INTENTIONS", [12.8, 13.4],
                       road(120, 960, FEET, 11.9, 12.05)
                       + figure(FXL, FEET, 11.9, pose="carry_L", instant=True)
                       + figure(FXR, FEET, 11.9, pose="carry_R", instant=True)
                       + lantern(FXL - 52, FEET - 112, 13.8)
                       + coin(FXR + 52, FEET - 112, 15.8),
                       [T("But one worked for Allah.", 16.5, 18.5, 560),
                        T("One worked for the world.", 18.3, 20.3, 640)],
                       fadeout=[21.3, 22.0]),
            # ---- S3 the outcome (21.3-30) ----
            card_scene(21.3, 30, "THE PROMISE", [22.8, 23.4],
                       road(120, 960, FEET, 21.9, 22.05)
                       + figure(FXL, FEET, 21.9, pose="carry_L", instant=True)
                       + figure(FXR, FEET, 21.9, pose="carry_R", instant=True)
                       + arrow_up(FXL, FEET - 265, 55, 23.8)
                       + ring_circle(FXR, FEET - 302, 26, 25.0, color="dim"),
                       [T("\u201cEach person will have", 25.5, 27.5, 560),
                        T("what they intended.\u201d", 27.3, 29.3, 640)],
                       fadeout=[29.3, 30.0]),
            # ---- S4 the hijrah example (29.3-36) ----
            card_scene(29.3, 36, "THE EXAMPLE \u00b7 HIJRAH", [31.2, 31.8],
                       door(620, 1100, 740, FEET, 30.4, beam=True)
                       + figure(680, FEET, 31.5, pose="walk"),
                       [T("\u201cWhoever\u2019s hijrah was for Allah \u2014", 31.8, 33.8, 560),
                        T("his hijrah was to Allah.\u201d", 33.6, 35.6, 640)],
                       fadeout=[35.3, 36.0]),
            # ---- S5 closing (35.3-40) ----
            dict(t0=35.3, t1=40, text=[
                dict(s="ACTIONS ARE BY", t0=36.3, t1=37.1, font="close", align="center",
                     x=W // 2, y=820),
                dict(s="INTENTIONS.", t0=36.8, t1=37.6, font="close", align="center",
                     x=W // 2, y=906),
                dict(s="SAHIH AL-BUKHARI \u00b7 1", t0=37.8, t1=38.6, font="cite",
                     color="gold", align="center", x=W // 2, y=1000, spacing=5),
            ]),
        ],
    )


def main():
    root = r"D:\models\vsCodeMcp\data\refanim"
    out = os.path.join(root, "ubu_al_amal.mp4")
    frames_dir = os.path.join(root, "ubu_al_amal_frames")
    sp = spec()
    frames_dir, n, fps = render(sp, frames_dir)
    print(f"[render] {n} frames @ {fps} fps -> {frames_dir}")
    encode(frames_dir, n, fps, out)
    print(f"[done] {out}  (Mode B target — ambient via ControlFoley next, D041 no music)")


if __name__ == "__main__":
    main()
