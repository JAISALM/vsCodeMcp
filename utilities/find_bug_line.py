r"""Find the exact flash_attn bug line in transformers import_utils.py"""
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Lib\site-packages\transformers\utils\import_utils.py"
lines = open(p, encoding="utf-8").read().splitlines()
for i, l in enumerate(lines):
    if 'PACKAGE_DISTRIBUTION_MAPPING["flash_attn"]' in l:
        print("LINE", i + 1, ":", repr(l))
        # show context
        for j in range(max(0, i - 3), min(len(lines), i + 4)):
            print(j + 1, repr(lines[j]))
