import json

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

def load(f):
    return json.load(open(f"{BASE}\\{f}", encoding="utf-8"))

def get_loadimage(wf):
    for n in wf["nodes"]:
        if n["type"] == "LoadImage":
            return n
    return None

native = get_loadimage(load("mini-max-refrance-to-video-1.json"))
conv = get_loadimage(load("krea2_jaisal_medium.json"))

def dump(tag, n):
    print(f"########## {tag} (id={n['id']}) ##########")
    print("top-level keys:", list(n.keys()))
    print("widgets_values:", n.get("widgets_values"))
    print("has widgets_values_named:", "widgets_values_named" in n)
    print("--- inputs ---")
    for i in n.get("inputs", []):
        t = i.get("type")
        if isinstance(t, list):
            print(f"   {i.get('name'):10} type=LIST(len={len(t)}) first3={t[:3]} widget={i.get('widget')} link={i.get('link')}")
        else:
            print(f"   {i.get('name'):10} type={t!r} widget={i.get('widget')} link={i.get('link')}")
    print("--- outputs ---")
    for o in n.get("outputs", []):
        print(f"   {o.get('name'):10} type={o.get('type')} links={o.get('links')}")
    print()

dump("NATIVE", native)
dump("CONVERTED", conv)

# Key comparison on the image input
def img_input(n):
    for i in n.get("inputs", []):
        if i.get("name") == "image":
            return i
    return None

ni = img_input(native)
ci = img_input(conv)
print("=== image input comparison ===")
print("native type is list:", isinstance(ni.get("type"), list), "len:", len(ni.get("type", [])) if isinstance(ni.get("type"), list) else "N/A")
print("conv   type is list:", isinstance(ci.get("type"), list), "len:", len(ci.get("type", [])) if isinstance(ci.get("type"), list) else "N/A")
print("native widget:", ni.get("widget"))
print("conv   widget:", ci.get("widget"))
print("native link:", ni.get("link"))
print("conv   link:", ci.get("link"))
