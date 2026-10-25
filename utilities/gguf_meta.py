import struct, os, sys

# v3 value type -> fixed size (bytes). 'string' = u64 len + bytes. Fully packed.
TYPESIZE = {0:4, 1:4, 2:4, 3:1, 4:4, 5:4, 6:4, 7:8, 9:8, 10:8, 11:8, 12:8, 13:8}

def parse(path):
    with open(path, "rb") as f:
        buf = f.read(1 << 24)  # 16 MB
    version = struct.unpack_from("<I", buf, 4)[0]
    n_tensors = struct.unpack_from("<Q", buf, 8)[0]
    n_kv = struct.unpack_from("<Q", buf, 16)[0]
    off = 24
    meta = {}
    for i in range(n_kv):
        klen = struct.unpack_from("<Q", buf, off)[0]; off += 8
        if klen > 512:
            return meta, None, f"bad klen {klen} at KV {i} (off {off-8})"
        key = buf[off:off+klen].decode("utf-8","replace"); off += klen
        vtype = struct.unpack_from("<I", buf, off)[0]; off += 4
        if vtype == 8:  # string
            slen = struct.unpack_from("<Q", buf, off)[0]
            if slen > 512:
                return meta, None, f"bad slen {slen} for {key} (off {off-8})"
            val = buf[off+8:off+8+slen].decode("utf-8","replace"); off += 8+slen
        elif vtype in TYPESIZE:
            sz = TYPESIZE[vtype]
            if vtype == 6:
                val = struct.unpack_from("<f", buf, off)[0]
            elif vtype == 7:
                val = struct.unpack_from("<q", buf, off)[0]
            elif vtype in (0, 4, 9, 10, 11, 12, 13):
                val = struct.unpack_from("<q" if sz==8 else "<i", buf, off)[0]
            else:
                val = buf[off:off+sz].hex()
            off += sz
        else:
            return meta, None, f"unknown type {vtype} for {key} (off {off-4})"
        meta[key] = val
    tensors = []
    for i in range(n_tensors):
        tlen = struct.unpack_from("<Q", buf, off)[0]; off += 8
        if tlen > 512:
            return meta, tensors, f"bad tlen {tlen} at tensor {i} (off {off-8})"
        name = buf[off:off+tlen].decode("utf-8","replace"); off += tlen
        ttype = struct.unpack_from("<I", buf, off)[0]; off += 4
        ndims = struct.unpack_from("<I", buf, off)[0]; off += 4
        dims = struct.unpack_from(f"<{ndims}Q", buf, off)[0] if ndims else ()
        off += 8*ndims
        tensors.append((name, ttype, dims))
    return meta, tensors, None

fields = ["general.architecture","general.name","general.size_label",
          "gemma4.block_count","gemma4.hidden_size","gemma4.attention.head_count",
          "gemma4.attention.head_count_kv","gemma4.vocab_size","gemma4.context_length",
          "gemma4.expert_count","gemma4.expert_count_used","gemma4.feed_forward_length",
          "gemma4.attention.key_length","gemma4.attention.value_length",
          "gemma4.expert_shared_frequency","gemma4.attention.sliding_window",
          "gemma4-assistant.block_count","gemma4-assistant.embedding_length",
          "gemma4-assistant.context_length","gemma4-assistant.feed_forward_length",
          "gemma4-assistant.attention.head_count","gemma4-assistant.attention.head_count_kv",
          "gemma4-assistant.attention.key_length","gemma4-assistant.attention.value_length",
          "gemma4-assistant.vocab_size","gemma4-assistant.rope.freq_base"]

for p in sys.argv[1:]:
    meta, tensors, err = parse(p)
    print("="*66)
    print(os.path.basename(p))
    if err: print(f"  STOPPED: {err}")
    for f in fields:
        if f in meta:
            print(f"  {f} = {meta[f]!r}")
    arch = meta.get("general.architecture","?")
    archkeys = sorted(k for k in meta if k.startswith(arch + "."))
    extra = [k for k in archkeys if k not in fields]
    if extra:
        print(f"  [other {arch}.* keys:]")
        for k in extra[:25]:
            print(f"    {k} = {meta[k]!r}")
    if tensors:
        print(f"  [tensors: {len(tensors)}] sample:")
        for t in tensors[:5]:
            print(f"    {t[0]} t={t[1]} dims={list(t[2])}")
        if len(tensors) > 9:
            print("    ...")
        for t in tensors[-3:]:
            print(f"    {t[0]} t={t[1]} dims={list(t[2])}")
    print()
