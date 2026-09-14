r"""Patch transformers import_utils.py flash_attn KeyError bug.

The 3 lines use PACKAGE_DISTRIBUTION_MAPPING["flash_attn"] which KeyErrors
when flash_attn is not installed. Replace with .get("flash_attn", []) so the
availability functions correctly return False. Backs up the original first.
"""
import shutil, os

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Lib\site-packages\transformers\utils\import_utils.py"
bak = p + ".flash_attn_bak"

if not os.path.exists(bak):
    shutil.copy(p, bak)
    print("backup ->", bak)

src = open(p, encoding="utf-8").read()
needle = 'PACKAGE_DISTRIBUTION_MAPPING["flash_attn"]'
count = src.count(needle)
src = src.replace(needle, 'PACKAGE_DISTRIBUTION_MAPPING.get("flash_attn", [])')
open(p, "w", encoding="utf-8").write(src)
print("replaced", count, "occurrences")
