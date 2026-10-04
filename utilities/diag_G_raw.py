"""Dump RAW links (all fields incl. type) + raw inputs for the MiniMax node in G_revolt."""
import json

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json"
d = json.load(open(P, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}
mm = [n for n in d["nodes"] if n["type"] == "MiniMaxH3ReferenceToVideo"][0]

print("=== RAW INPUTS (index / name / type / link) ===")
for i, inp in enumerate(mm.get("inputs", [])):
    print(f"  [{i:2d}] {inp.get('name'):32s} type={inp.get('type'):8s} link={inp.get('link')}")

print()
print("=== RAW LINKS touching node 136 (id, from, from_slot, to, to_slot, type) ===")
for l in d.get("links", []):
    lid, fn, fs, tn, ts = l[0], l[1], l[2], l[3], l[4]
    if fn == 136 or tn == 136:
        ltype = l[5] if len(l) > 5 else "?"
        ftype = nodes[fn]["type"] if fn in nodes else "?"
        print(f"  link {lid}: {fn}({ftype}) s{fs} -> {tn} s{ts}  [type={ltype}]")
