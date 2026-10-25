"""Diff a pack-import result JSON against the pre-update baseline capture.

Usage:
  python diff_pack_import.py [baseline_txt] [new_json]

Defaults:
  baseline_txt = data/pack_import_baseline_037_20261025.txt
                 (UTF-16 PS-redirect capture; BOM auto-detected)
  new_json     = data/pack_import_results.json

The baseline is a messy PS capture (ANSI codes, banner art) — pack lines are
extracted with a non-anchored regex `"<pack>": "<OK|FAIL...>"`.
Interpretation rules (2026-10-25, v0.42.5 update):
- REGRESSION (OK -> FAIL) = the only red flag;
- FAIL -> OK can be a REAL fix (nvvfx 0.2.0.0 -> ComfyUI_Nvidia_VFX_Nodes)
  OR an entry-selection artifact of the test harness;
- class-count N -> 0 across most packs is a harness artifact of the rebuilt
  entry-point selection, NOT a real regression — the status comparison is the
  signal; the authoritative check is the real server startup log.
"""
import codecs, json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = sys.argv[1] if len(sys.argv) > 1 else r"D:\models\vsCodeMcp\data\pack_import_baseline_037_20261025.txt"
NEW = sys.argv[2] if len(sys.argv) > 2 else r"D:\models\vsCodeMcp\data\pack_import_results.json"

with open(BASE, "rb") as f:
    head = f.read(4)
enc = "utf-16" if head[:2] in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE) else "utf-8"
base_raw = open(BASE, encoding=enc, errors="replace").read()
base_raw = re.sub(r"\u001B\[[0-9;]*m", "", base_raw)
base = {}
for m in re.finditer(r'"([^"]{2,60})"\s*:\s*"((?:OK|FAIL|SKIP)[^"]*)"', base_raw):
    base[m.group(1)] = m.group(2)

new = json.load(open(NEW, encoding="utf-8"))
new = {k: v for k, v in new.items() if k != "__pycache__" and not k.startswith(".")}


def status(s):
    return "OK" if s.startswith("OK") else ("FAIL" if s.startswith("FAIL") else "OTHER")


print(f"baseline packs: {len(base)}   new packs: {len(new)}")
print()
regr, fixed, missing, added, count_diff = [], [], [], [], []
for p in sorted(set(base) | set(new)):
    b, n = base.get(p), new.get(p)
    if b is None:
        added.append(p)
    elif n is None:
        missing.append(p)
    elif status(b) == "OK" and status(n) != "OK":
        regr.append((p, b, n))
    elif status(b) != "OK" and status(n) == "OK":
        fixed.append((p, b, n))
    elif status(b) == "OK" and status(n) == "OK":
        mb, mn = re.search(r"OK \((\d+) classes\)", b), re.search(r"OK \((\d+) classes\)", n)
        if mb and mn and mb.group(1) != mn.group(1):
            count_diff.append((p, mb.group(1), mn.group(1)))

print("=== REGRESSIONS (was OK before, now not) ===")
for p, b, n in regr:
    print(f"  {p}\n    before: {b}\n    after:  {n}")
print(f"  ({len(regr)} total)")
print()
print("=== FIXED (was FAIL before, now OK) ===")
for p, b, n in fixed:
    print(f"  {p}: {b} -> {n}")
print(f"  ({len(fixed)} total)")
print()
print("=== class-count differences (OK -> OK; harness caveat — see docstring) ===")
for p, cb, cn in count_diff:
    print(f"  {p}: {cb} -> {cn}")
print(f"  ({len(count_diff)} total)")
print()
print("=== still FAILING (same on both) ===")
for p in sorted(set(base) & set(new)):
    b, n = base[p], new[p]
    if status(b) != "OK" and status(n) != "OK":
        print(f"  {p}: {n[:150]}")
print()
print("=== added / missing ===")
print("  added:", added)
print("  missing from new run:", missing)
