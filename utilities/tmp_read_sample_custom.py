import io
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\comfy\sample.py"
c = io.open(p, encoding="utf-8", errors="replace").read()
i = c.find("def sample_custom")
print(c[i:i+1500])
