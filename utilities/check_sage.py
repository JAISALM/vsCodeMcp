import importlib, subprocess, sys

PY = r'E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe'

print("=== installed sageattention ===")
try:
    import sageattention
    print("sageattention version:", getattr(sageattention, '__version__', 'unknown'))
    print("sageattention file:", getattr(sageattention, '__file__', '?'))
except Exception as e:
    print("sageattention import FAILED:", e)

print("\n=== pip show sageattention ===")
r = subprocess.run([PY, '-m', 'pip', 'show', 'sageattention'], capture_output=True, text=True)
print(r.stdout)
print(r.stderr)

print("=== CUDA arch detection (torch) ===")
try:
    import torch
    print("torch:", torch.__version__)
    print("cuda available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("device:", torch.cuda.get_device_name(0))
        print("capability:", torch.cuda.get_device_capability(0))
except Exception as e:
    print("torch check failed:", e)

print("\n=== sageattention arch support ===")
try:
    import sageattention
    # try to see what archs it knows
    import sageattention._qgemm  # noqa
    print("qgemm module present")
except Exception as e:
    print("arch probe:", e)
