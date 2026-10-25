import struct

for p in [r"D:\models\Gemma\mtp-gemma-4-31B-it.gguf",
          r"D:\models\Gemma\Gemma4-31B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf",
          r"D:\models\Gemma\gemma-4-Ortenzya-The-Creative-Wordsmith-31B-it-uncensored-heretic-Q5_K_M.gguf"]:
    with open(p, "rb") as f:
        buf = f.read(1024)
    magic = buf[:4]
    version = struct.unpack_from("<I", buf, 4)[0]
    n_tensors = struct.unpack_from("<Q", buf, 8)[0]
    n_kv = struct.unpack_from("<Q", buf, 16)[0]
    import os
    print(os.path.basename(p))
    print(f"  size={os.path.getsize(p)/1e6:.1f}MB magic={magic} version={version} "
          f"n_tensors={n_tensors} n_kv={n_kv}")
    print(f"  bytes 24-80: {buf[24:80].hex(' ')}")
