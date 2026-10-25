import struct

def align(o, a=8):
    return (o + a - 1) // a * a

def parse(path):
    with open(path, "rb") as f:
        buf = f.read(1 << 20)
    version = struct.unpack_from("<I", buf, 4)[0]
    n_tensors = struct.unpack_from("<Q", buf, 8)[0]
    n_kv = struct.unpack_from("<Q", buf, 16)[0]
    off = 24
    meta = {}
    for i in range(n_kv):
        # key: u64 len + bytes
        klen = struct.unpack_from("<Q", buf, off)[0]; off += 8
        key = buf[off:off+klen].decode("utf-8","replace"); off += klen
        # v3: value type u32 sits immediately after key bytes (no padding)
        vtype = struct.unpack_from("<I", buf, off)[0]; off += 4
        if vtype in (4, 8):  # string candidate
            slen = struct.unpack_from("<Q", buf, off)[0]
            val = buf[off+8:off+8+slen].decode("utf-8","replace")
            off += 8 + slen
        elif vtype == 5:
            cnt = struct.unpack_from("<Q", buf, off)[0]; off += 8
            etype = struct.unpack_from("<I", buf, off)[0]; off += 4
            items = []
            for _ in range(cnt):
                if etype in (4,8):
                    slen = struct.unpack_from("<Q", buf, off)[0]
                    items.append(buf[off+8:off+8+slen].decode("utf-8","replace")); off += 8+slen
                elif etype in (0,1,2,3):
                    items.append(struct.unpack_from("<i" if etype==1 else "<f" if etype==2 else "<I", buf, off)[0]); off += 4
                elif etype in (6,7,8):
                    items.append(struct.unpack_from("<Q" if etype==6 else "<q" if etype==7 else "<d", buf, off)[0]); off += 8
                else:
                    items.append(f"<t{etype}>"); off += 8
            val = items
        elif vtype in (0,1,2,3):
            val = struct.unpack_from("<i" if vtype==1 else "<f" if vtype==2 else "<I", buf, off)[0]; off += 4
        elif vtype in (6,7):
            val = struct.unpack_from("<Q" if vtype==6 else "<q", buf, off)[0]; off += 8
        else:
            # unknown: bail
            return meta, (f"unknown value type {vtype} at key {key!r}")
        off = align(off)
        meta[key] = val
    return meta, None

for p in [r"D:\models\Gemma\mtp-gemma-4-31B-it.gguf",
          r"D:\models\Gemma\Gemma4-31B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf",
          r"D:\models\Gemma\gemma-4-Ortenzya-The-Creative-Wordsmith-31B-it-uncensored-heretic-Q5_K_M.gguf"]:
    import os
    meta, err = parse(p)
    print("=" * 60)
    print(os.path.basename(p))
    if err:
        print(f"  PARSE STOPPED: {err}")
    interesting = ["general.architecture","general.name",
                   "gemma4.block_count","gemma4.hidden_size","gemma4.attention.head_count",
                   "gemma4.attention.head_count_kv","gemma4.vocab_size","gemma4.context_length",
                   "gemma4.expert_count","gemma4.expert_count_used","gemma4.expert_frequency",
                   "gemma4.mtp_block_count","gemma4.mtp_head_count","gemma4.n_layer","gemma4.n_embd",
                   "llama.block_count","llama.hidden_size","llama.vocab_size","llama.context_length"]
    for k in sorted(meta):
        if k in interesting or "mtp" in k.lower() or "block_count" in k or "vocab" in k.lower() or "hidden" in k.lower() or "context" in k.lower() or "head_count" in k.lower():
            print(f"  {k} = {meta[k]!r}")
