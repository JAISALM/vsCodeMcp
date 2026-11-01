"""Drop-in replacement for safetensors.torch.load_file that avoids the huge-commit
mmap failure on 26 GB files (Windows ERROR 1455 / access violation).

Reads the header, then reconstitutes each tensor from the raw mmap bytes:
  F32/F16/F64 -> np.frombuffer directly
  BF16        -> uint16 view -> torch .view(torch.bfloat16)
  I64/I32/I16/I8/U8/BOOL -> numpy int/uint types
Zero extra commit: the mmap is file-backed and lazy.
"""
import json
import mmap
import struct

import numpy as np
import torch

_NP_DTYPES = {
    "F64": np.float64,
    "F32": np.float32,
    "F16": np.float16,
    "I64": np.int64,
    "I32": np.int32,
    "I16": np.int16,
    "I8": np.int8,
    "U8": np.uint8,
    "BF16": np.uint16,
    "BOOL": np.uint8,
}


def load_file_low_commit(path: str, device: str = "cpu") -> dict:
    with open(path, "rb") as f:
        n = struct.unpack("<Q", f.read(8))[0]
        header = json.loads(f.read(n))
        data_start = 8 + n

    tensors = {k: v for k, v in header.items() if k != "__metadata__"}
    # detect offset semantics: absolute (>= data_start) or relative to data start
    offs = [v["data_offsets"][0] for v in tensors.values()]
    base = 0
    if offs and min(offs) >= data_start:
        base = 0  # absolute offsets
    else:
        base = data_start  # relative offsets

    result = {}
    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        for k, v in tensors.items():
            o0, o1 = v["data_offsets"]
            raw = mm[o0 + base : o1 + base]
            dt = v["dtype"]
            np_dt = _NP_DTYPES[dt]
            arr = np.frombuffer(raw, dtype=np_dt)
            if dt == "BF16":
                t = torch.from_numpy(arr.copy()).view(torch.bfloat16)
            elif dt == "BOOL":
                t = torch.from_numpy(arr.copy()).view(torch.bool)
            else:
                t = torch.from_numpy(arr.copy())
            if v["shape"]:
                t = t.reshape(v["shape"])
            if device != "cpu":
                t = t.to(device)
            result[k] = t
        mm.close()
    return result


if __name__ == "__main__":
    import time

    p = r"E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\krea2_raw_bf16.safetensors"
    t0 = time.time()
    sd = load_file_low_commit(p)
    dt = time.time() - t0
    print(f"loaded {len(sd)} tensors in {dt:.0f}s", flush=True)
    bf16 = sum(1 for t in sd.values() if t.dtype == torch.bfloat16)
    f32 = sum(1 for t in sd.values() if t.dtype == torch.float32)
    print(f"dtype counts: bf16={bf16} f32={f32} other={len(sd) - bf16 - f32}", flush=True)
    k0 = next(iter(sd))
    print(f"first: {k0} {tuple(sd[k0].shape)} {sd[k0].dtype}", flush=True)
    # sanity: a bf16 weight should have finite values
    w = next(t for t in sd.values() if t.dtype == torch.bfloat16)
    print(f"bf16 sample sum={w.float().sum().item():.2f} min={w.float().min().item():.4f} max={w.float().max().item():.4f}", flush=True)
    print("LOW-COMMIT LOAD OK", flush=True)
