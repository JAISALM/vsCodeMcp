# -*- coding: utf-8 -*-
"""Inspect the H3 GGUF: architecture, layer count, and whether the output head
(lm_head / output_norm) is present. Determines if it's a full chat model or a
pruned text-encoder-only model."""
import os, re

FP = r"D:\models\Writing\Qwen\Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49-Q4_K_M.gguf"
data = open(FP, "rb").read()
print("File size: %.2f GB" % (len(data) / 1e9))

# 1. Architecture string (near the start, in metadata)
m = re.search(rb"qwen3[a-z0-9_]*", data[:2_000_000], re.I)
print("Arch hint (first match):", m.group(0).decode() if m else "none")

# 2. Search for key tensor-name byte strings anywhere in the file
for needle in [b"output_norm", b"lm_head", b"blk.49.", b"blk.50.", b"blk.48.",
               b"blk.0.", b"vision", b"model.layers", b"embed_tokens"]:
    cnt = data.count(needle)
    print("  %-16s count=%d" % (needle.decode(), cnt))

# 3. Find the highest blk.N layer index present (to confirm pruning at 49)
layers = set()
for m in re.finditer(rb"blk\.(\d+)\.", data):
    layers.add(int(m.group(1)))
if layers:
    print("Layer indices found: min=%d max=%d count=%d" % (min(layers), max(layers), len(layers)))
else:
    print("No blk.N layer tensors found (naming may differ)")

# 4. Look for the arch metadata value specifically
for m in re.finditer(rb"arch\x00\x00([a-z0-9_]{3,40})\x00\x00", data[:5_000_000]):
    print("arch metadata:", m.group(1).decode())
    break
