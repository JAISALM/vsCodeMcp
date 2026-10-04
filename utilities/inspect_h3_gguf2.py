# -*- coding: utf-8 -*-
import re
FP = r"D:\models\Writing\Qwen\Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49-Q4_K_M.gguf"
d = open(FP, "rb").read()
print("File size: %.2f GB" % (len(d) / 1e9))
print("output_norm:", d.count(b"output_norm"))
print("lm_head:", d.count(b"lm_head"))
print("blk.49:", d.count(b"blk.49."))
print("blk.50:", d.count(b"blk.50."))
print("blk.48:", d.count(b"blk.48."))
L = set(int(m.group(1)) for m in re.finditer(rb"blk\.(\d+)\.", d))
print("layers: %d to %d, count %d" % (min(L), max(L), len(L)))
print("vision:", d.count(b"vision"))
print("embed_tokens:", d.count(b"embed_tokens"))
print("norm.:", d.count(b"norm."))
