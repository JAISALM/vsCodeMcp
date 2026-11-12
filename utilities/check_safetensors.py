#!/usr/bin/env python
"""Safetensors integrity checker (2026-11-12, lessons from the half-file incident).

Why this exists:
  "size match after a move" is NOT an integrity check. A faithful move of a
  half-file passes size matching. 2026-11-12: the whole 84.4 GB comfy_models
  archive batch (10 files) were half-files (headers describing ~2x the
  physical size) or source-truncated uploads — every one failed this check.

File layout observed (ai-toolkit / ComfyUI / HF exports):
  [8-byte LE header length][JSON header][tensor data][optional trailing
  copy of the header]. The `data_offsets` in these files are ABSOLUTE
  (from file start, header included) — NOT relative to the data start,
  contrary to the vanilla safetensors reading. A known-good active LoRA
  satisfies max(off+sz) + H == size EXACTLY (verified on krea2 LoRAs that
  load daily in ComfyUI).

Verdicts per file:
  COMPLETE      max(off+sz) + H == size          (trailing header copy)
  COMPLETE      max(off+sz) == size              (no trailing header)
  OK            data complete, trailing header partially cut
  TRUNCATED     max(off+sz) > size               (tail tensor data missing)
  HALF-FILE     max(off+sz) ~ 2x size            (dual-layout header, only
                                                 one copy present)

Usage:
  python check_safetensors.py <path> [path2 ...]
  (paths may be files or directories; directories are scanned recursively
  for *.safetensors)
Exit code: 0 = all OK/COMPLETE, 1 = at least one TRUNCATED/HALF/UNREADABLE.
"""
import glob
import json
import os
import struct
import sys


def check(path):
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        (hlen,) = struct.unpack("<Q", f.read(8))
        header = json.loads(f.read(hlen))
    H = 8 + hlen
    A = 0
    for k, v in header.items():
        if k == "__metadata__":
            continue
        off, sz = v["data_offsets"]
        A = max(A, off + sz)
    if A + H == size or A == size:
        verdict = "COMPLETE"
    elif A < size < A + H:
        verdict = "OK (data complete, trailing header cut)"
    elif A > size:
        if A > 1.9 * size:
            verdict = "HALF-FILE (header ~2x physical size)"
        else:
            verdict = "TRUNCATED (missing %d bytes)" % (A + H - size)
    else:
        verdict = "UNUSUAL (A+H=%d vs size=%d)" % (A + H, size)
    good = verdict.startswith("COMPLETE") or verdict.startswith("OK")
    return "%-52s %8.2f GB  tensors=%-5d %s" % (
        os.path.basename(path), size / 1e9, len(header) - 1, verdict), good


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    files = []
    for p in sys.argv[1:]:
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, "**", "*.safetensors"), recursive=True))
        elif os.path.isfile(p):
            files.append(p)
        else:
            print("NOT FOUND: %s" % p)
            return 1
    any_bad = False
    for f in files:
        try:
            line, good = check(f)
        except Exception as e:  # unreadable header = broken file
            line, good = "UNREADABLE (%s)" % type(e).__name__, False
        any_bad = any_bad or not good
        print(line)
    return 1 if any_bad else 0


if __name__ == "__main__":
    sys.exit(main())
