"""
VRAM/RAM monitor for MiniMax H3 runs.

Run this in a SEPARATE terminal while the workflow runs in ComfyUI.
It logs every 5s: GPU VRAM used/free, GPU util, ComfyUI python RAM, Qwen RAM.
Output: d:\models\vsCodeMcp\vram_monitor.csv  (+ live console)

WHY: to catch the DynamicVRAM offloading signature —
  VRAM pinned near 32 GB + ComfyUI RAM climbing = model offloaded to CPU.
Stop with Ctrl+C.
"""
import csv
import subprocess
import time
import os

OUT = r"d:\models\vsCodeMcp\data\vram_monitor.csv"
INTERVAL = 5


def gpu():
    try:
        r = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used,memory.free,utilization.gpu,power.draw",
             "--format=csv,noheader,nounits"], text=True, timeout=10
        ).strip().split()
        return int(r[0]), int(r[1]), int(r[2]), float(r[3])
    except Exception as e:
        return None, None, None, None


def proc_ram_mb(name):
    total = 0
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command",
             f"Get-Process -Name {name} -ErrorAction SilentlyContinue | "
             f"Measure-Object -Property WorkingSet64 -Sum | "
             f"Select-Object -ExpandProperty Sum"],
            text=True, timeout=15,
        ).strip()
        if out:
            total = int(out) // (1024 * 1024)
    except Exception:
        pass
    return total


def main():
    fields = ["t", "vram_used_mib", "vram_free_mib", "gpu_util_pct", "power_w",
              "comfyui_ram_mb", "qwen_ram_mb"]
    new_file = not os.path.exists(OUT)
    with open(OUT, "a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(fields)
        print(f"Monitoring -> {OUT}  (Ctrl+C to stop)")
        print("t(s)  vram_used  vram_free  util%  powerW  comfy_RAM  qwen_RAM")
        t0 = time.time()
        while True:
            used, free, util, power = gpu()
            comfy = proc_ram_mb("python")
            qwen = proc_ram_mb("llama-server")
            t = round(time.time() - t0, 0)
            w.writerow([t, used, free, util, power, comfy, qwen])
            f.flush()
            print(f"{t:5.0f}  {used}  {free}  {util}%  {power}W  {comfy}MB  {qwen}MB")
            time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
