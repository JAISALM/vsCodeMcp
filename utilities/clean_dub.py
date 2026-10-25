"""clean_dub.py — full dub cleaning chain: Demucs vocal separation + clean_audio.

The proper cleaner for phone recordings with background sound / echo mixed
into the voice (2026-10-05, D104). A spectral gate (clean_audio.py alone)
only removes noise QUIETER than the voice; Demucs (neural source separation)
removes background + echo MIXED INTO the voice.

Chain:
  1. demucs --two-stems=vocals (CUDA, ~2s per line) -> vocals.wav
  2. clean_audio.py on the vocals stem -> highpass + gate + normalize
     -> <stem>_cleaned_48k.wav (editing) + <stem>_cleaned_16k.wav (pipeline)

Usage:
  python clean_dub.py <input> [output_dir]

Output (in output_dir, default = input's folder):
  <stem>_demucs_vocals_48k.wav   <- Demucs vocals, normalized (the dub)
  <stem>_cleaned_48k.wav         <- full chain (demucs + gate + normalize)
  <stem>_cleaned_16k.wav         <- 16 kHz pipeline version
  <stem>_no_vocals_48k.wav       <- what was removed (bg + echo), for A/B

Uses the VoiceStudio venv python (has demucs + torch CUDA).
"""
import subprocess
import sys
from pathlib import Path

VS_PY = r"C:\Users\user\AppData\Local\com.debpalash.omnivoice-studio\project\.venv\Scripts\python.exe"
CLEAN_AUDIO = Path(__file__).parent / "clean_audio.py"
PORTABLE_PY = r"E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src.stem

    # 1. Demucs vocal separation (CUDA)
    demucs_out = out_dir / "demucs"
    print(f"[1/2] demucs two-stems=vocals (cuda): {src}")
    subprocess.run(
        [VS_PY, "-m", "demucs", "--two-stems=vocals", "-d", "cuda",
         "-o", str(demucs_out), str(src)],
        check=False,  # demucs exits 1 on HF warnings; check the files instead
    )
    vocals = demucs_out / "htdemucs" / stem / "vocals.wav"
    no_vocals = demucs_out / "htdemucs" / stem / "no_vocals.wav"
    if not vocals.exists():
        print(f"ERROR: demucs did not produce {vocals}")
        sys.exit(1)

    # 2. clean_audio.py on the vocals stem (gate + normalize + 16k).
    # clean_audio.py names outputs after the INPUT stem ("vocals"), so
    # rename them back to the original take name.
    print(f"[2/2] clean_audio.py on {vocals.name}")
    subprocess.run([PORTABLE_PY, str(CLEAN_AUDIO), str(vocals), str(out_dir)],
                   check=True)
    import shutil
    for suffix in ("_cleaned_48k.wav", "_cleaned_16k.wav"):
        tmp = out_dir / f"vocals{suffix}"
        if tmp.exists():
            dest = out_dir / f"{stem}{suffix}"
            dest.unlink(missing_ok=True)
            tmp.rename(dest)

    # 3. Copy the demucs-vocals (pre-gate) + no_vocals versions for A/B
    shutil.copy(vocals, out_dir / f"{stem}_demucs_vocals_48k.wav")
    if no_vocals.exists():
        shutil.copy(no_vocals, out_dir / f"{stem}_no_vocals_48k.wav")

    print(f"\nDone. Files in {out_dir}:")
    for f in sorted(out_dir.glob(f"{stem}_*.wav")):
        print(f"  {f.name}  ({f.stat().st_size // 1024} KB)")
    print(f"\nA/B: {stem}_demucs_vocals_48k.wav (demucs only) vs "
          f"{stem}_cleaned_48k.wav (demucs + gate + normalize)")


if __name__ == "__main__":
    main()
