#!/usr/bin/env python
"""Ubu al-Amal — "Actions are by intentions" — 60 s Template B video.

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


def card_scene(t0, t1, label, label_fade, elements, text):
    return dict(t0=t0, t1=t1, card=CARD, card_fade=[5.9, 6.4], elements=elements,
                label_gold=label, label_sub="", label_fade=label_fade, text=text)


def T(s, t0, t1, y, mode="type"):
    return dict(s=s, t0=t0, t1=t1, font="caption", color="white", align="center",
                x=W // 2, y=y, mode=mode)


def spec():
    return dict(
        duration=60.0, fps=30, handle="@yourhandle", handle_fade=[1.5, 2.1],
        text=[],
        scenes=[
            # ---- S0 hook (0-6) ----
            dict(t0=0, t1=6, text=[
                dict(s="TWO PEOPLE.", t0=0.8, t1=2.6, font="big", align="center",
                     x=W // 2, y=780, mode="type"),
                dict(s="THE SAME WORK.", t0=2.6, t1=4.4, font="big", align="center",
                     x=W // 2, y=866, mode="type"),
                dict(s="A HADITH IN ONE MINUTE", t0=4.6, t1=5.4, font="small",
                     color="gold", align="center", x=W // 2, y=970, spacing=5),
            ]),
            # ---- S1 the same action (6-16) ----
            card_scene(6, 16, "THE SAME ACTION", [7.8, 8.4],
                       road(120, 960, FEET, 6.4)
                       + figure(FXL, FEET, 6.8, pose="walk")
                       + figure(FXR, FEET, 7.1, pose="walk"),
                       [T("They prayed the same prayers.", 8.2, 10.2, 560),
                        T("They worked the same hours.", 10.0, 12.0, 640)]),
            # ---- S2 two intentions (16-30) ----
            card_scene(16, 30, "TWO INTENTIONS", [18.5, 19.1],
                       road(120, 960, FEET, 15.9, 16.05)
                       + figure(FXL, FEET, 15.9, pose="carry_L", instant=True)
                       + figure(FXR, FEET, 15.9, pose="carry_R", instant=True)
                       + lantern(FXL - 52, FEET - 112, 17.5)
                       + coin(FXR + 52, FEET - 112, 19.5),
                       [T("But one worked for Allah.", 20.5, 22.5, 560),
                        T("One worked for the world.", 22.3, 24.3, 640)]),
            # ---- S3 the outcome (30-44) ----
            card_scene(30, 44, "THE PROMISE", [31.0, 31.6],
                       road(120, 960, FEET, 29.9, 30.05)
                       + figure(FXL, FEET, 29.9, pose="carry_L", instant=True)
                       + figure(FXR, FEET, 29.9, pose="carry_R", instant=True)
                       + arrow_up(FXL, FEET - 265, 55, 31.0)
                       + ring_circle(FXR, FEET - 302, 26, 32.5, color="dim"),
                       [T("\u201cEach person will have", 33.0, 35.0, 560),
                        T("what they intended.\u201d", 34.8, 36.8, 640)]),
            # ---- S4 the hijrah example (44-54) ----
            card_scene(44, 54, "THE EXAMPLE \u00b7 HIJRAH", [47.5, 48.1],
                       door(620, 1100, 740, FEET, 45.0, beam=True)
                       + figure(680, FEET, 46.5, pose="walk"),
                       [T("\u201cWhoever\u2019s hijrah was for Allah \u2014", 48.5, 50.5, 560),
                        T("his hijrah was to Allah.\u201d", 50.3, 52.3, 640)]),
            # ---- S5 closing (54-60) ----
            dict(t0=54, t1=60, text=[
                dict(s="ACTIONS ARE BY", t0=54.4, t1=55.2, font="big", align="center",
                     x=W // 2, y=820),
                dict(s="INTENTIONS.", t0=54.9, t1=55.7, font="big", align="center",
                     x=W // 2, y=906),
                dict(s="SAHIH AL-BUKHARI \u00b7 1", t0=55.9, t1=56.7, font="cite",
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
