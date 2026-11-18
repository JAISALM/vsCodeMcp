#!/usr/bin/env python
"""Ubu al-Amal — "Actions are by intentions" — 48 s Template B video.

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
    # v7 pace fix (user: "pace is off, its 30s video i think" = v6 felt rushed):
    # every caption line now takes 2.8 s (was 2.0 s), beats get real holds, total
    # falls to 48 s — same five beats, no padding, just breathing room.
    return dict(
        duration=48.0, fps=30, handle="@yourhandle", handle_fade=[1.5, 2.1],
        text=[],
        scenes=[
            # ---- S0 hook (0-5.0) ----
            dict(t0=0, t1=5.0, fadeout=[4.4, 5.0], text=[
                dict(s="TWO PEOPLE.", t0=0.9, t1=3.7, font="big", align="center",
                     x=W // 2, y=800),
                dict(s="THE SAME WORK.", t0=2.0, t1=4.8, font="big", align="center",
                     x=W // 2, y=890),
            ]),
            # ---- S1 the same action (4.3-13.0) ----
            card_scene(4.3, 13.0, "THE SAME ACTION", [5.7, 6.3],
                       road(120, 960, FEET, 4.7)
                       + figure(FXL, FEET, 5.0, pose="walk")
                       + figure(FXR, FEET, 5.3, pose="walk"),
                       [T("They prayed the same prayers.", 6.8, 9.6, 560),
                        T("They worked the same hours.", 9.4, 12.2, 640)],
                       fadeout=[12.3, 13.0]),
            # ---- S2 two intentions (12.3-23.6) ----
            card_scene(12.3, 23.6, "TWO INTENTIONS", [13.5, 14.1],
                       road(120, 960, FEET, 12.7, 12.85)
                       + figure(FXL, FEET, 13.1, pose="carry_L", instant=True)
                       + figure(FXR, FEET, 13.1, pose="carry_R", instant=True)
                       + lantern(FXL - 52, FEET - 112, 14.5)
                       + coin(FXR + 52, FEET - 112, 16.5),
                       [T("But one worked for Allah.", 17.4, 20.2, 560),
                        T("One worked for the world.", 20.0, 22.8, 640)],
                       fadeout=[22.9, 23.6]),
            # ---- S3 the outcome (22.9-32.8) ----
            card_scene(22.9, 32.8, "THE PROMISE", [24.1, 24.7],
                       road(120, 960, FEET, 23.3, 23.45)
                       + figure(FXL, FEET, 23.7, pose="carry_L", instant=True)
                       + figure(FXR, FEET, 23.7, pose="carry_R", instant=True)
                       + arrow_up(FXL, FEET - 265, 55, 24.9)
                       + ring_circle(FXR, FEET - 302, 26, 26.3, color="dim"),
                       [T("\u201cEach person will have", 26.5, 29.3, 560),
                        T("what they intended.\u201d", 29.3, 32.1, 640)],
                       fadeout=[32.1, 32.8]),
            # ---- S4 the hijrah example (32.1-41.0) ----
            card_scene(32.1, 41.0, "THE EXAMPLE \u00b7 HIJRAH", [34.4, 35.0],
                       door(620, 1100, 740, FEET, 33.6, beam=True)
                       + figure(680, FEET, 34.7, pose="walk"),
                       [T("\u201cWhoever\u2019s hijrah was for Allah \u2014", 34.8, 37.6, 560),
                        T("his hijrah was to Allah.\u201d", 37.4, 40.2, 640)],
                       fadeout=[40.3, 41.0]),
            # ---- S5 closing (40.3-48.0) ----
            dict(t0=40.3, t1=48.0, text=[
                dict(s="ACTIONS ARE BY", t0=40.8, t1=41.8, font="close", align="center",
                     x=W // 2, y=820),
                dict(s="INTENTIONS.", t0=41.4, t1=42.4, font="close", align="center",
                     x=W // 2, y=906),
                dict(s="SAHIH AL-BUKHARI \u00b7 1", t0=42.6, t1=43.4, font="cite",
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
