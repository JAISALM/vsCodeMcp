import importlib
mods = ['triton','sageattention','flash_attn','xformers','torch','comfy_kitchen','kitchen','comfy_kitchen_attention','sage_attn']
for m in mods:
    try:
        mod = importlib.import_module(m)
        v = getattr(mod, '__version__', 'OK')
        print(f"{m:28s} -> {v}")
    except Exception as e:
        print(f"{m:28s} -> MISSING ({type(e).__name__})")
