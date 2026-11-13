#!/usr/bin/env python
"""Safetensors integrity checker — v2, CORRECTED 2026-11-13.

FORMAT (verified against known-good active files + the safetensors spec):
  File layout: [8-byte LE header length][JSON header][tensor data]
               [OPTIONAL trailing copy of the header, exactly H = 8+hlen bytes]
  `data_offsets` is a PAIR [start, end] of ABSOLUTE file-relative offsets
  (header INCLUDED) — NOT [offset, size]. A tensor occupies bytes
  [start, end). A complete file therefore satisfies:
      max(end) + H == size          (trailing header present)
      max(end) == size              (no trailing header)
  Verified: active krea2 LoRA last tensor end == size - H exactly (to the byte),
  and Comfy-Org gemma fp8_scaled (13.2 GB) fits the same way.

HISTORY — why v2 exists (2026-11-12..13, the half-file incident):
  v1 (11-12) computed end as off + sz, i.e. it treated data_offsets[1] as a
  SIZE. For good files that produced max ≈ 2x physical size, which was
  (wrongly) read as "dual-layout header / half-file" and led to deleting
  ~115 GB of archive files that were most likely COMPLETE. Both the offset
  arithmetic AND the loader test were wrong that day (safetensors API is
  .get_tensor(), not .get() — a .get() test fails every key with
  AttributeError and masquerades as "all tensors truncated").
  LESSONS: (1) data_offsets = [start, end], absolute, header-inclusive;
  (2) completeness = max(end) vs size, never off+sz; (3) a loader test must
  call .get_tensor() — verify the method name before believing a failure;
  (4) size-match after a move is not an integrity check either.

Usage:
  python check_safetensors.py <path> [path2 ...]   (files or dirs, recursive)
  python check_safetensors.py --load <file>        (ground truth: read EVERY
      tensor via safetensors .get_tensor(); slow, ~1x full-file read)
Exit code: 0 = all good, 1 = any broken/failed.
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
    end = 0
    for k, v in header.items():
        if k == "__metadata__":
            continue
        s, e = v["data_offsets"]
        end = max(end, e)
    if end + H == size:
        verdict = "COMPLETE (trailing header, exact fit)"
    elif end == size:
        verdict = "COMPLETE (no trailing header)"
    elif end < size < end + H:
        verdict = "OK (data complete, trailing header partially cut)"
    elif end > size:
        verdict = "TRUNCATED (last tensor ends %d bytes past EOF)" % (end - size)
    else:  # end < size - H
        verdict = "GAP (%d bytes between last tensor and trailing header)" % (size - end - H)
    good = verdict.startswith(("COMPLETE", "OK"))
    return "%-52s %8.2f GB  tensors=%-5d max_end=%d  %s" % (
        os.path.basename(path), size / 1e9, len(header) - 1, end, verdict), good


def load_check(path):
    """Ground truth: read every tensor with the real safetensors loader."""
    from safetensors import safe_open
    with safe_open(path, framework="pt") as f:
        keys = list(f.keys())
    ok, bad = 0, []
    with safe_open(path, framework="pt") as f:
        for k in keys:
            try:
                f.get_tensor(k)
                ok += 1
            except Exception as e:
                bad.append((k, type(e).__name__))
    if ok == len(keys):
        verdict = "LOAD OK (%d/%d tensors)" % (ok, len(keys))
        good = True
    else:
        verdict = "LOAD FAIL %d/%d: %s" % (len(bad), len(keys), bad[:8])
        good = False
    return "%-52s %8.2f GB  %s" % (
        os.path.basename(path), os.path.getsize(path) / 1e9, verdict), good


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    any_bad = False
    if sys.argv[1] == "--load":
        files = list(sys.argv[2:])
        for f in files:
            try:
                line, good = load_check(f)
            except Exception as e:
                line, good = "UNREADABLE (%s: %s)" % (type(e).__name__, e), False
            any_bad = any_bad or not good
            print(line)
        return 1 if any_bad else 0
    files = []
    for p in sys.argv[1:]:
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, "**", "*.safetensors"), recursive=True))
        elif os.path.isfile(p):
            files.append(p)
        else:
            print("NOT FOUND: %s" % p)
            return 1
    for f in files:
        try:
            line, good = check(f)
        except Exception as e:
            line, good = "UNREADABLE (%s: %s)" % (type(e).__name__, e), False
        any_bad = any_bad or not good
        print(line)
    return 1 if any_bad else 0


if __name__ == "__main__":
    sys.exit(main())
