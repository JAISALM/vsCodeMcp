import json

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

def load(f):
    return json.load(open(f"{BASE}\\{f}", encoding="utf-8"))

def find_kSampler(wf):
    for n in wf["nodes"]:
        if n["type"] == "KSampler":
            return n
    return None

native = find_kSampler(load("krea2_jaisal_base.json"))   # native, named=False
conv = find_kSampler(load("krea2_jaisal_medium.json"))    # converted, named=True

def show(tag, n):
    print(f"########## {tag} (id={n['id']}) ##########")
    print("top-level keys:", list(n.keys()))
    print("widgets_values:", n.get("widgets_values"))
    print("widgets_values_named:", n.get("widgets_values_named"))
    print("--- inputs ---")
    for i in n.get("inputs", []):
        print(f"   {i.get('name'):14} type={str(i.get('type'))[:20]:20} link={i.get('link')} widget={i.get('widget')}")
    print("--- outputs ---")
    for o in n.get("outputs", []):
        print(f"   {o.get('name'):14} type={o.get('type')} links={o.get('links')}")
    print()

show("NATIVE base", native)
show("CONVERTED medium", conv)

# Field-by-field key diff
print("=== KEY DIFF (native vs converted) ===")
nk = set(native.keys()); ck = set(conv.keys())
print("only in native:", nk - ck)
print("only in converted:", ck - nk)
