import comfy_kitchen, os, inspect
print("comfy_kitchen location:", os.path.dirname(comfy_kitchen.__file__))
print("version:", getattr(comfy_kitchen, "__version__", "?"))
print()
print("=== top-level attributes ===")
for name in dir(comfy_kitchen):
    if not name.startswith("__"):
        print("  ", name)
print()
# Try to find attention-related functions
print("=== attention-related ===")
for name in dir(comfy_kitchen):
    if any(k in name.lower() for k in ["attn","attention","kernel","int8","sdpa","flash"]):
        obj = getattr(comfy_kitchen, name)
        print("  ", name, type(obj).__name__)
