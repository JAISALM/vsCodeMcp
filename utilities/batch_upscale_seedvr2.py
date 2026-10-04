"""SeedVR2 batch upscaler — upscale every .mp4 in a folder at TWO resolutions.

Purpose (2026-09-29): the user puts the 8 Jaisal clips (A-G) in one folder, runs
this script, and gets two output folders:
  <input>_1080p/   (1920x1080)
  <input>_1440p/   (2560x1440)
so they can compare HD vs 2K and lock the production pipeline for future videos.
4K is out of scope.

How it works:
  - Uses the numz SeedVR2 CLI (inference_cli.py) in DIRECTORY mode — the model is
    loaded ONCE per resolution pass and reused across all clips (efficient).
  - Two passes: 1080p then 1440p.
  - Source fps is preserved (the CLI reads cap.get(CAP_PROP_FPS) — 24fps clips
    stay 24fps).
  - Model: seedvr2_ema_7b_sharp_fp16.safetensors (max quality, proven).

RUN (user, stop Qwen first):
  Stop-Process -Name "llama-server" -Force
  & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\batch_upscale_seedvr2.py" "D:\models\vsCodeMcp\Jaisal-intro\upscale_input"
  Start-Process "D:\models\qwen\Qwen3.827BMTP.bat"

TEST ONE CLIP FIRST (recommended): put a single .mp4 in the folder, run, check
the output, then add the rest.
"""
import subprocess, sys, os, time, argparse
from pathlib import Path

COMFY = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"
PY = r"E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe"
CLI = os.path.join(COMFY, "custom_nodes", "seedvr2_videoupscaler", "inference_cli.py")
MODEL_DIR = os.path.join(COMFY, "models", "SEEDVR2")
DEFAULT_MODEL = "seedvr2_ema_7b_sharp_fp16.safetensors"


def run_pass(input_dir, out_dir, resolution, max_res, model, log):
    """Run one SeedVR2 CLI pass (directory mode) at a given resolution."""
    cmd = [
        PY, CLI, input_dir,
        "--dit_model", model,
        "--resolution", str(resolution),
        "--max_resolution", str(max_res),
        "--batch_size", "1",
        "--color_correction", "lab",
        "--model_dir", MODEL_DIR,
        "--output", out_dir,
        "--output_format", "mp4",
    ]
    log(f"\n{'='*70}\nPASS {resolution}p (max {max_res})\n{'='*70}")
    log("CMD: " + " ".join(cmd))
    t0 = time.time()
    r = subprocess.run(cmd, cwd=COMFY)
    dt = time.time() - t0
    log(f"exit={r.returncode}  time={dt:.0f}s ({dt/60:.1f} min)")
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description="SeedVR2 batch upscaler (1080p + 1440p)")
    ap.add_argument("input_dir", help="Folder containing the .mp4 clips to upscale")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"DiT model (default {DEFAULT_MODEL})")
    ap.add_argument("--res1", type=int, default=1080, help="First target short-side (default 1080)")
    ap.add_argument("--res2", type=int, default=1440, help="Second target short-side (default 1440)")
    ap.add_argument("--only", choices=["1", "2", "both"], default="both",
                    help="Run only one resolution pass (default both)")
    args = ap.parse_args()

    input_dir = Path(args.input_dir).resolve()
    if not input_dir.is_dir():
        print(f"ERROR: input dir not found: {input_dir}")
        sys.exit(1)
    clips = sorted(input_dir.glob("*.mp4"))
    if not clips:
        print(f"ERROR: no .mp4 files in {input_dir}")
        sys.exit(1)
    print(f"Found {len(clips)} clips in {input_dir}:")
    for c in clips:
        print(f"  - {c.name}")

    base = input_dir.name
    parent = input_dir.parent
    out1 = parent / f"{base}_{args.res1}p"
    out2 = parent / f"{base}_{args.res2}p"
    # 16:9 long side, rounded to even (SeedVR2 step=2)
    max1 = int(round(args.res1 * 16 / 9 / 2) * 2)
    max2 = int(round(args.res2 * 16 / 9 / 2) * 2)

    log_path = input_dir / f"upscale_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    log_lines = []

    def log(msg):
        print(msg)
        log_lines.append(msg)

    log(f"Input: {input_dir}")
    log(f"Model: {args.model}")
    log(f"Pass 1: {args.res1}p -> {out1}")
    log(f"Pass 2: {args.res2}p -> {out2}")

    t_start = time.time()
    if args.only in ("1", "both"):
        rc1 = run_pass(str(input_dir), str(out1), args.res1, max1, args.model, log)
    if args.only in ("2", "both"):
        rc2 = run_pass(str(input_dir), str(out2), args.res2, max2, args.model, log)

    total = time.time() - t_start
    log(f"\n{'='*70}\nDONE in {total:.0f}s ({total/60:.1f} min)\n{'='*70}")
    log(f"Outputs:\n  {out1}\n  {out2}")

    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"\nLog: {log_path}")


if __name__ == "__main__":
    main()
