#!/usr/bin/env python
"""11_sheet_composite.json — combine MULTIPLE images into ONE (sheet layout).

User request (2026-10-20): "give me the workflow for combining multiple images
into one" — for the character-sheet stage (face + top-right + bottom-right ->
the 3-panel composite that 09j/09k LoadImage reads).

Layout (matches the 09j/09k PE spec: 2304x1536 3:2, 16px gaps, white canvas):
  - LEFT panel = image A (face), scaled to FULL canvas height (aspect preserved)
  - TOP-RIGHT = image B (crest), 760x760
  - BOTTOM-RIGHT = image C (kit), 760x760, vertically centered in the right column

Nodes (all CORE — no custom packs):
  EmptyImage (white 2304x1536 canvas)
  LoadImage x3 (native shape: image COMBO + upload IMAGEUPLOAD, widgets [file,"image"])
  ImageScale x3 (lanczos, exact slot sizes, crop center)
  ImageCompositeMasked x3 (destination=canvas/prev, source=scaled, x/y placement,
  resize_source=False — sources are pre-scaled to their slot size)
  SaveImage (root prefix SHEET_COMPOSITE — no slashes allowed)

The face panel width fw is COMPUTED from the actual face aspect:
fw = round(CANVAS_H * w/h). For 1152x2048 -> 864.
Right column: x = fw+16, width = CANVAS_W - x, squares centered:
xoff = (col_w - SQ)//2.
"""
import json, os, shutil
from PIL import Image

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"
WF = os.path.join(BASE, "user", "default", "workflows", "11_sheet_composite.json")

CANVAS_W, CANVAS_H = 2304, 1536
GAP, SQ = 16, 760
WHITE = 0xFFFFFF

# slot files (input dir — LoadImage reads from input/)
FACE = "zidane_portrait_front.png"   # staged from output\FACEFRONTAL2_ZIDANE_c_00012_.png
TOP = "zidane_crest_ref.png"
BOT = "zidane_kit_ref.png"

# 1. stage the picked face into input/ (LoadImage reads input/)
src = os.path.join(BASE, "output", "FACEFRONTAL2_ZIDANE_c_00012_.png")
dst = os.path.join(BASE, "input", FACE)
assert os.path.exists(src), "face source missing: " + src
shutil.copyfile(src, dst)
w, h = Image.open(src).size
print(f"face {w}x{h} staged -> input\\{FACE}")

# 2. layout math
fw = round(CANVAS_H * w / h)
col_x = fw + GAP
col_w = CANVAS_W - col_x
cx = (col_w - SQ) // 2
face_x, face_y = 0, 0
top_x, top_y = col_x + cx, 0
bot_x, bot_y = col_x + cx, SQ + GAP
assert bot_y + SQ <= CANVAS_H, "bottom square overflows canvas"
print(f"face {fw}x{CANVAS_H} @ ({face_x},{face_y}) | top {SQ}² @ ({top_x},{top_y}) | "
      f"bot {SQ}² @ ({bot_x},{bot_y}) | canvas {CANVAS_W}x{CANVAS_H}")

def load_image(nid, fname, pos):
    return {"id": nid, "type": "LoadImage", "pos": pos, "size": [282.78, 322],
            "flags": {}, "mode": 0,
            "inputs": [
                {"localized_name": "image", "name": "image", "type": "COMBO",
                 "widget": {"name": "image"}, "link": None},
                {"localized_name": "choose file to upload", "name": "upload",
                 "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None}],
            "outputs": [
                {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None},
                {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None}],
            "properties": {"Node name for S&R": "LoadImage"},
            "widgets_values": [fname, "image"]}

def img_scale(nid, slot, ww, hh, pos):
    return {"id": nid, "type": "ImageScale", "pos": pos, "size": [270, 126],
            "flags": {}, "mode": 0,
            "inputs": [{"localized_name": "image", "name": "image", "type": "IMAGE", "link": None}],
            "outputs": [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None}],
            "properties": {"Node name for S&R": "ImageScale"},
            "widgets_values": ["lanczos", ww, hh, "center"], "_slot": slot}

def composite(nid, x, y, pos):
    return {"id": nid, "type": "ImageCompositeMasked", "pos": pos, "size": [270, 126],
            "flags": {}, "mode": 0,
            "inputs": [
                {"localized_name": "destination", "name": "destination", "type": "IMAGE", "link": None},
                {"localized_name": "source", "name": "source", "type": "IMAGE", "link": None},
                {"localized_name": "mask", "name": "mask", "type": "MASK", "link": None}],
            "outputs": [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None}],
            "properties": {"Node name for S&R": "ImageCompositeMasked"},
            "widgets_values": [x, y, False], "_slot": None}

nodes = [
    {"id": 60, "type": "EmptyImage", "pos": [40, 560], "size": [270, 110], "flags": {}, "mode": 0,
     "inputs": [],
     "outputs": [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None}],
     "properties": {"Node name for S&R": "EmptyImage"},
     "widgets_values": [CANVAS_W, CANVAS_H, 1, WHITE]},
    load_image(61, FACE, [40, 40]),
    load_image(62, TOP, [40, 400]),
    load_image(63, BOT, [40, 760]),
    img_scale(64, "face", fw, CANVAS_H, [360, 40]),
    img_scale(65, "top", SQ, SQ, [360, 400]),
    img_scale(66, "bot", SQ, SQ, [360, 760]),
    composite(67, face_x, face_y, [700, 40]),
    composite(68, top_x, top_y, [700, 400]),
    composite(69, bot_x, bot_y, [700, 760]),
    {"id": 70, "type": "SaveImage", "pos": [1020, 400], "size": [270, 250], "flags": {}, "mode": 0,
     "inputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "link": None}],
     "outputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "links": None}],
     "properties": {"Node name for S&R": "SaveImage"},
     "widgets_values": ["SHEET_COMPOSITE"]},
]

# 3. links (from, to_slot, to, to_slot, type)
links = [
    (61, 0, 64, 0, "IMAGE"),   # face -> scale
    (62, 0, 65, 0, "IMAGE"),   # top  -> scale
    (63, 0, 66, 0, "IMAGE"),   # bot  -> scale
    (60, 0, 67, 0, "IMAGE"),   # canvas -> comp1.destination
    (64, 0, 67, 1, "IMAGE"),   # face_scaled -> comp1.source
    (67, 0, 68, 0, "IMAGE"),   # comp1 -> comp2.destination
    (65, 0, 68, 1, "IMAGE"),   # top_scaled -> comp2.source
    (68, 0, 69, 0, "IMAGE"),   # comp2 -> comp3.destination
    (66, 0, 69, 1, "IMAGE"),   # bot_scaled -> comp3.source
    (69, 0, 70, 0, "IMAGE"),   # comp3 -> save
]
for i, l in enumerate(links, 100):
    links[i - 100] = [i] + list(l)

# 4. fan link ids into input link fields + output links lists
by_id = {n["id"]: n for n in nodes}
for link_id, f, fs, t, ts, _t in links:
    node = by_id[t]
    if node["type"] == "SaveImage":
        node["inputs"][ts]["link"] = link_id
    elif node["type"] == "ImageScale":
        node["inputs"][0]["link"] = link_id
    elif node["type"] == "ImageCompositeMasked":
        node["inputs"][ts]["link"] = link_id
    src = by_id[f]
    if src["type"] == "LoadImage":
        src["outputs"][0]["links"] = [link_id]
    else:
        src["outputs"][0]["links"] = (src["outputs"][0].get("links") or []) + [link_id]
for n in nodes:
    n.pop("_slot", None)

wf = {"id": "11_sheet_composite", "version": 0.4, "last_node_id": 70,
      "nodes": nodes, "links": links,
      "options": {"nodeSnapSize": 10, "canvasGridSize": 10, "zoom": 0.7, "offset": [0, 0]},
      "status": {"last_group_id": None, "last_group_selected": False, "last_node_id": 70,
                 "last_link_id": 109, "version": 1},
      "extra": {"ds": {"scale": 0.7, "offset": [0, 0]}}}

json.dump(wf, open(WF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"saved {WF} | nodes: {len(nodes)} | links: {len(links)}")
