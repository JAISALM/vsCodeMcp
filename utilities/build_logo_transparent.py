#!/usr/bin/env python
"""Build logo_transparent.json — LoadImage -> PixaromaRemoveBackground (BiRefNet) -> SaveImage/Preview.
Input: any logo PNG in input\\ (currently logo_1fist_mono.png). Output: transparent PNG
(LOGO_TRANSPARENT_<prefix>_*.png) usable on any t-shirt color.
"""
import json

OUT = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\logo_transparent.json"

note = ("TRANSPARENT LOGO (crest v3, D145-v3): removes the royal-blue background -> "
        "RGBA PNG usable on any shirt color (royal blue / dark green / white).\n"
        "To process a different logo: change the LoadImage file (e.g. a 3-fist variant "
        "copied into input\\) and the SaveImage prefix. Model: birefnet.safetensors "
        "(already installed in E:\\ComfyUI_windows_portable\\ComfyUI\\models\\background_removal).")

nodes = [
    {"id": 101, "type": "LoadImage", "pos": [40, 40], "size": [300, 350], "flags": {}, "order": 0, "mode": 0,
     "inputs": [
         {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": 1},
         {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
     ],
     "outputs": [
         {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [1]},
         {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
     ],
     "properties": {"Node name for S&R": "LoadImage"},
     "widgets_values": ["logo_1fist_mono.png", "image"]},

    {"id": 102, "type": "PixaromaRemoveBackground", "pos": [420, 40], "size": [320, 160], "flags": {}, "order": 1, "mode": 0,
     "inputs": [
         {"name": "image", "type": "IMAGE", "widget": None, "link": 1},
         {"name": "model", "type": "COMBO", "widget": {"name": "model"}, "link": None},
     ],
     "outputs": [
         {"name": "image", "type": "IMAGE", "links": [2, 3]},
         {"name": "mask", "type": "MASK", "links": None},
         {"name": "inverted_mask", "type": "MASK", "links": None},
     ],
     "widgets_values": ["birefnet.safetensors"]},

    {"id": 103, "type": "SaveImage", "pos": [820, 40], "size": [340, 350], "flags": {}, "order": 2, "mode": 0,
     "inputs": [
         {"localized_name": "images", "name": "images", "type": "IMAGE", "widget": None, "link": 2},
     ],
     "outputs": [],
     "properties": {"Node name for S&R": "SaveImage"},
     "widgets_values": ["LOGO_TRANSPARENT/logo_1fist"]},

    {"id": 104, "type": "PreviewImage", "pos": [820, 440], "size": [300, 240], "flags": {}, "order": 3, "mode": 0,
     "inputs": [
         {"name": "images", "type": "IMAGE", "widget": None, "link": 3},
     ],
     "outputs": [],
     "properties": {"Node name for S&R": "PreviewImage"},
     "widgets_values": None},

    {"id": 105, "type": "Note", "pos": [40, 440], "size": [360, 240], "flags": {}, "order": 4, "mode": 0,
     "inputs": [], "outputs": [],
     "widgets_values": [note]},
]

links = [
    [1, 101, 0, 102, 0, "IMAGE"],
    [2, 102, 0, 103, 0, "IMAGE"],
    [3, 102, 0, 104, 0, "IMAGE"],
]

j = {"last_node_id": 105, "last_link_id": 3, "id": "logo-transparent",
     "revision": 0, "version": 0.4, "wall": {}, "nodes": nodes, "links": links,
     "config": {}, "options": {}, "flags": {}, "extra": {}}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(j, f, indent=4, ensure_ascii=False)
print("wrote", OUT)
