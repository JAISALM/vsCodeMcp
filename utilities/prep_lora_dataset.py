# -*- coding: utf-8 -*-
"""
prep_lora_dataset.py (2026-10-31)
Prepares per-character LoRA training datasets from the v91 v2 dataset run.

Source : E:\\comfyUi_latest\\...\\output\\You did not name me Dataset 21\\
         You did not name me_00001..00040.png/.txt
         (00001-00020 = Jaisal, 00021-00040 = Zidhan — user's 22:40/22:53 runs)
Target : E:\\comfyUi_latest\\...\\input\\lora_jaisal\\  (jaisal_NN.png/.txt, trigger jeskvman)
         E:\\comfyUi_latest\\...\\input\\lora_zidhan\\  (zidhan_NN.png/.txt, trigger dlorman)

Caption transform (training captions must be trigger-first, shorter than the
full v2 line):
    strip leading "You did not name me . "
    head  = identity block up to the first ". "
    scene = first clause(s) of the scene, cut at the first craft-suffix marker
    caption = "<trigger>, <head>, <scene>"
"""
import os, re, shutil, sys

ROOT = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"
SRC = os.path.join(ROOT, "output", "You did not name me Dataset 21")
PREFIX = "You did not name me"

CHARS = [
    # (char, first_src, count, trigger, dest_subfolder, dest_name_prefix)
    ("Jaisal", 1, 20, "jeskvman", "lora_jaisal", "jaisal"),
    ("Zidhan", 21, 20, "dlorman", "lora_zidhan", "zidhan"),
]

CRAFT_MARKERS = [
    "ignore original", "photorealistic", "high detail", "high-detail",
    "85mm", "35mm", "50mm", "shallow dof", "beauty shot", "cinematic",
    "high resolution", "detailed skin", "film grain", "8k", "ultra detailed",
]

def transform_caption(raw: str, trigger: str) -> str:
    txt = raw.strip()
    p = PREFIX + " ."
    if txt.startswith(p):
        txt = txt[len(p):].lstrip()
    # Normalize skin phrase to the user's target (22:40 Jaisal batch was
    # prompted "warm dark brown" from a pre-22:45 canvas; images render
    # medium-fair, so the training label must match the image).
    txt = txt.replace(
        "warm dark brown skin with natural texture",
        "medium fair skin with a soft natural tan and even complexion",
    )
    # head = identity block up to first ". "
    i = txt.find(". ")
    if i > 0 and "Kerala (South Indian) man" in txt[:i]:
        head = txt[:i]
        scene = txt[i + 2:]
    else:
        # fallback: keep first 200 chars as head
        head, scene = txt[:200], ""
    # scene = up to first craft marker (or 130 chars, trimmed at last comma)
    cut = len(scene)
    low = scene.lower()
    for m in CRAFT_MARKERS:
        j = low.find(m)
        if 0 < j < cut:
            cut = j
    if cut > 130:
        cut = 130
    scene_short = scene[:cut]
    # trim at last comma
    k = scene_short.rfind(",")
    if k > 40:
        scene_short = scene_short[:k]
    scene_short = scene_short.strip().rstrip(",").strip()
    return (trigger + ", " + head + (", " + scene_short if scene_short else "")).strip()

def main():
    made = 0
    for char, first, count, trigger, sub, namep in CHARS:
        dest = os.path.join(ROOT, "input", sub)
        os.makedirs(dest, exist_ok=True)
        samples = []
        for i in range(count):
            num = first + i
            src_png = os.path.join(SRC, f"{PREFIX}_{num:05d}.png")
            src_txt = os.path.join(SRC, f"{PREFIX}_{num:05d}.txt")
            if not (os.path.isfile(src_png) and os.path.isfile(src_txt)):
                print(f"MISSING source pair {num:05d} — check source folder")
                sys.exit(1)
            n = i + 1
            dst_png = os.path.join(dest, f"{namep}_{n:02d}.png")
            dst_txt = os.path.join(dest, f"{namep}_{n:02d}.txt")
            shutil.copyfile(src_png, dst_png)
            raw = open(src_txt, encoding="utf-8").read()
            cap = transform_caption(raw, trigger)
            open(dst_txt, "w", encoding="utf-8", newline="").write(cap)
            if n in (1, 10, 20):
                samples.append((n, cap))
        made += count
        print(f"=== {char} -> input\\{sub}\\ ({count} pairs)")
        for n, cap in samples:
            print(f"  [{namep}_{n:02d}] {cap[:170]}")
    print(f"\nDONE: {made} image/caption pairs prepared")

if __name__ == "__main__":
    main()
