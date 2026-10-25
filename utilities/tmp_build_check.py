import json, sys
sys.path.insert(0, r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Pixaroma\nodes")
import _prompt_each_helpers as h
wf = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_fair_test.json", encoding="utf-8"))
node = [n for n in wf["nodes"] if n["type"] == "PixaromaPromptEach"][0]
blob = node["widgets_values"][0]
# exact replication of PixaromaPromptEach.build() with text=None (input not wired)
state = h.parse_state(blob)
pieces = list(state["prompts"])
if not pieces and state["text"]:
    pieces = h.split_text(state["text"], state["split"])
wired = ""
result = h.build_from_pieces(pieces, expand=state["expand"], trim=state["trim"], skip_empty=state["skipEmpty"], cap=state["cap"])
print("RUNNER VERDICT: one Run queues", len(result.prompts), "images (truncated:", result.truncated, ")")
for i, p in enumerate(result.prompts, 1):
    print(f"  [{i}] {p[:54]}")
for inp in node.get("inputs", []):
    print("input:", inp.get("name"), "| type:", inp.get("type"), "| link:", inp.get("link"))
