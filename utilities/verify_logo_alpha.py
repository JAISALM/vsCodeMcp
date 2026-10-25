#!/usr/bin/env python
import sys
from PIL import Image

for p in [r"D:\models\vsCodeMcp\data\crests\logo_1fist_white_transparent.png",
          r"D:\models\vsCodeMcp\data\crests\logo_1fist_black_transparent.png"]:
    im = Image.open(p)
    a = im.getchannel("A")
    W, H = im.size
    apx = a.load()
    corners = [apx[2, 2], apx[W - 3, 2], apx[2, H - 3], apx[W - 3, H - 3]]
    top = [apx[x, 5] for x in (100, 300, 512, 700, 900)]
    # count fully-transparent vs opaque
    hist = a.histogram()
    n_trans = hist[0]
    n_opaq = hist[255]
    tot = W * H
    print(p.split("\\")[-1])
    print(f"  corners alpha {corners}  top-band {top}")
    print(f"  transparent {n_trans/tot:.1%}  opaque {n_opaq/tot:.1%}  (1024x1024)")
    # ring integrity: sample the top of the ring (y where ring top is ~ y=90? ring top near y=85-105 center x=512)
    for y in (95, 100, 105, 110):
        row = [apx[x, y] for x in (480, 512, 544)]
        print(f"  y={y} center-x alpha {row}")
