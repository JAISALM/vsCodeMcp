import io, re
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\nodes.py"
c = io.open(p, encoding="utf-8", errors="replace").read()
i = c.find("class SamplerCustom")
print(c[i:i+2200])
