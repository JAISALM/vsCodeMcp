import struct, sys, os

def align(o, a=8):
    return (o + a - 1) // a * a

def decode(path, show_tensors=True):
    with open(path, "rb") as f:
        buf = f.read(1 << 20)  # 1 MB header is plenty
    if buf[:4] != b"GGUF":
        print(f"{path}: not a GGUF file"); return
    version = struct.unpack_from("<I", buf, 4)[0]
    n_tensors = struct.unpack_from("<Q", buf, 8)[0]
    n_kv = struct.unpack_from("<Q", buf, 16)[0]
    print(f"=== {os.path.basename(path)} ===")
    print(f"version={version} n_kv={n_kv} n_tensors={n_tensors} filesize={os.path.getsize(path)/1e6:.1f}MB")
    off = 24
    meta = {}
    # v3: key = u64 len + str (pad 8); value = u32 type + data (pad 8)
    for i in range(n_kv):
        klen = struct.unpack_from("<Q", buf, off)[0]; off += 8
        key = buf[off:off+klen].decode("utf-8", "replace"); off += klen
        off = align(off)
        vtype = struct.unpack_from("<I", buf, off)[0]; off += 4
        # Heuristic decode based on type; v3 string type observed = 16
        if vtype in (4, 16):
            slen = struct.unpack_from("<Q", buf, off)[0]
            val = buf[off+8:off+8+slen].decode("utf-8", "replace")
            off += 8 + slen
        elif vtype == 5:  # array: u64 count, then elements (type of elements)
            cnt = struct.unpack_from("<Q", buf, off)[0]; off += 8
            # element type u32
            etype = struct.unpack_from("<I", buf, off)[0]; off += 4
            items = []
            for _ in range(cnt):
                if etype in (4, 16):
                    slen = struct.unpack_from("<Q", buf, off)[0]
                    items.append(buf[off+8:off+8+slen].decode("utf-8","replace"))
                    off += 8 + slen
                elif etype in (0,1,2,3):
                    items.append(struct.unpack_from("<i" if etype==1 else "<f" if etype==2 else "<I", buf, off)[0])
                    off += 4
                elif etype in (6,7,8):
                    items.append(struct.unpack_from("<Q" if etype==6 else "<q" if etype==7 else "<d", buf, off)[0])
                    off += 8
                else:
                    items.append(f"<elem type {etype}>")
                    off += 8
            val = items
        elif vtype in (0,1,2,3):
            val = struct.unpack_from("<i" if vtype==1 else "<f" if vtype==2 else "<I", buf, off)[0]; off += 4
        elif vtype in (6,7,8):
            val = struct.unpack_from("<Q" if vtype==6 else "<q" if vtype==7 else "<d", buf, off)[0]; off += 8
        else:
            print(f"  !! unknown value type {vtype} for {key}, stopping meta")
            break
        off = align(off)
        meta[key] = val
    print("--- metadata ---")
    for k in sorted(meta):
        print(f"  {k} = {meta[k]!r}")
    if not show_tensors:
        return
    print("--- tensors ---")
    for i in range(n_tensors):
        tlen = struct.unpack_from("<Q", buf, off)[0]; off += 8
        name = buf[off:off+tlen].decode("utf-8","replace"); off += tlen
        off = align(off)
        ttype = struct.unpack_from("<I", buf, off)[0]
        ndims = struct.unpack_from("<I", buf, off+4)[0]
        dims = struct.unpack_from(f"<{ndims}Q", buf, off+8)[0] if ndims else ()
        off += 8 + 8*ndims
        ne = 1
        for d in dims: ne *= d
        print(f"  {name}  t={ttype} dims={list(dims)} ne={ne}")

for p in sys.argv[1:]:
    decode(p)
    print()
