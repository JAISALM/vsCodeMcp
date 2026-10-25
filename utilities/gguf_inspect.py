#!/usr/bin/env python3
"""GGUF header inspector: metadata, tensor names/shapes, file integrity.

Usage: gguf_inspect.py <file.gguf> [more files...]
Reads only the header (first 256 MB); verifies file size against
header + tensor data sizes (completeness check) using os.path.getsize.
"""
import os
import struct
import sys

VTYPES = {0: "UINT32", 1: "INT32", 2: "FLOAT32", 3: "BOOL", 4: "STRING",
          5: "ARRAY", 6: "UINT64", 7: "INT64", 8: "FLOAT64"}
# quant type element sizes (common)
TSIZE = {9: 8, 10: 6, 11: 5, 12: 4, 13: 4, 14: 5, 15: 4, 16: 5,
         17: 5, 18: 6, 19: 8, 20: 8, 21: 4, 22: 4, 23: 4, 24: 4}

def align(off, a):
    return (off + a - 1) // a * a

def read_u32(b, o): return struct.unpack_from("<I", b, o)[0]
def read_i32(b, o): return struct.unpack_from("<i", b, o)[0]
def read_u64(b, o): return struct.unpack_from("<Q", b, o)[0]
def read_i64(b, o): return struct.unpack_from("<q", b, o)[0]
def read_f32(b, o): return struct.unpack_from("<f", b, o)[0]
def read_f64(b, o): return struct.unpack_from("<d", b, o)[0]

def read_str(b, o, u64=False):
    n = read_u64(b, o) if u64 else read_u32(b, o)
    o += 8 if u64 else 4
    if n > 1000000:
        raise ValueError(f"implausible string length {n} at {o}")
    return b[o:o+n].decode("utf-8", "replace"), o + n

def read_value(b, o, u64=False):
    vtype = read_u32(b, o); o += 4
    t = VTYPES.get(vtype, f"quant{vtype}")
    if vtype in (0, 1):   return t, read_i32(b, o), o + 4
    if vtype == 2:        return t, read_f32(b, o), o + 4
    if vtype == 3:        return t, bool(read_u32(b, o)), o + 4
    if vtype == 4:        s, o = read_str(b, o, u64); return t, s, o
    if vtype == 5:
        cnt = read_u64(b, o); o += 8
        arr = []
        for _ in range(cnt):
            _, v, o = read_value(b, o, u64)
            arr.append(v)
        return t, arr, o
    if vtype == 6:        return t, read_u64(b, o), o + 8
    if vtype == 7:        return t, read_i64(b, o), o + 8
    if vtype == 8:        return t, read_f64(b, o), o + 8
    raise ValueError(f"unsupported metadata value type {vtype} at {o}")

def parse(path, str_u64=False):
    actual = os.path.getsize(path)
    with open(path, "rb") as f:
        buf = f.read(256 * 1024 * 1024)
    if buf[:4] != b"GGUF":
        return {"error": f"bad magic {buf[:4]!r}"}
    version = read_u32(buf, 4)
    n_tensors = read_u64(buf, 8)
    n_kv = read_u64(buf, 16)
    r = {"version": version, "n_tensors": n_tensors, "n_kv": n_kv}
    if n_tensors > 100000 or n_kv > 100000:
        r["error"] = f"implausible n_tensors={n_tensors} n_kv={n_kv}"
        return r
    off = 24
    meta = {}
    ok = True
    for i in range(n_kv):
        key, off = read_str(buf, off, str_u64)
        off = align(off, 8)  # key string padded to 8
        if not all(32 <= ord(c) < 127 for c in key) or len(key) > 200:
            r["error"] = f"desync at KV {i} (offset {off}): key={key[:60]!r}"
            ok = False
            break
        _, val, off = read_value(buf, off, str_u64)
        off = align(off, 8)  # value (type+data) padded to 8
        meta[key] = val
    if not ok:
        return r
    tensors = []
    for _ in range(n_tensors):
        name, off = read_str(buf, off, str_u64)
        off = align(off, 8)
        ttype = read_u32(buf, off); off += 4
        nd = read_u32(buf, off); off += 4
        dims = [read_u64(buf, off + 8*i) for i in range(nd)]
        off += 8 * nd
        tensors.append((name, ttype, dims))
    r["meta"] = meta
    r["tensors"] = tensors
    total = 0
    for name, ttype, dims in tensors:
        ne = 1
        for d in dims:
            ne *= d
        total += align(ne * TSIZE.get(ttype, 4), 32)
    r["header_end"] = off
    r["data_bytes"] = total
    r["expected_size"] = off + total
    r["actual_size"] = actual
    r["complete"] = actual >= off + total
    return r

def main():
    for path in sys.argv[1:]:
        print("=" * 72)
        print(path)
        r = parse(path)
        if r.get("error"):
            print(f"  PARSE FAILED: {r['error']}")
            print("  retrying with GGUF v3 style (uint64 string lengths)...")
            r = parse(path, str_u64=True)
            if r.get("error"):
                print(f"  STILL FAILED: {r['error']}")
                continue
        print(f"  version={r['version']}  n_kv={r['n_kv']}  n_tensors={r['n_tensors']}")
        print(f"  header_end={r['header_end']}  data={r['data_bytes']}  "
              f"expected={r['expected_size']}  actual={r['actual_size']}")
        print(f"  integrity: {'OK (file complete)' if r['complete'] else 'TRUNCATED by %d bytes' % (r['expected_size'] - r['actual_size'])}")
        print("  --- metadata ---")
        for k in sorted(r["meta"]):
            v = r["meta"][k]
            if isinstance(v, str) and len(v) > 90:
                v = v[:90] + "..."
            if isinstance(v, list) and len(v) > 10:
                v = v[:5] + [f"... {len(v)} items"]
            print(f"    {k} = {v!r}")
        print(f"  --- tensors ({len(r['tensors'])}) ---")
        for name, ttype, dims in r["tensors"][:30]:
            print(f"    {name}  type={ttype} dims={dims}")
        if len(r["tensors"]) > 30:
            print(f"    ... and {len(r['tensors']) - 30} more")

if __name__ == "__main__":
    main()
