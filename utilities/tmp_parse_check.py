import json, sys
sys.path.insert(0, r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Pixaroma\nodes")
import _prompt_each_helpers as h
wf = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_fair_test.json", encoding="utf-8"))
node = [n for n in wf["nodes"] if n["type"] == "PixaromaPromptEach"][0]
blob = node["widgets_values"][0]
state = h.parse_state(blob)
pieces = h.build_from_pieces(state)
print("parse_state OK: version", state.get("version"))
print("prompts in state:", len(state["prompts"]))
print("expanded pieces (what one Run queues):", len(pieces))
for i, p in enumerate(pieces, 1):
    print(f"  [{i}] {p[:44]}")
print("named == positional blob:", node.get("widgets_values_named", {}).get("prompteach") == blob)
