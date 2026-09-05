"""Verify the ControlFoley node pack imports cleanly (so a ComfyUI restart registers the nodes)."""
import sys
import importlib

COMFY_ROOT = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"
NODE_DIR = COMFY_ROOT + r"\custom_nodes\comfyui-controlfoley-official"

sys.path.insert(0, COMFY_ROOT)
sys.path.insert(0, NODE_DIR)

try:
    import nodes as cf_nodes
    print("IMPORT OK")
    print("NODES:", list(cf_nodes.NODE_CLASS_MAPPINGS.keys()))
except Exception as e:
    import traceback
    print("IMPORT FAILED:", type(e).__name__, e)
    traceback.print_exc()
