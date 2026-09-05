"""Submit jaisal_sketch_title_audio.json to ComfyUI with NAMED inputs.

Bypasses the UI->API converter's positional widgets_values misalignment by
mapping each node's widgets_values to the server's /object_info widget names
explicitly. Link inputs are wired from the workflow's links array.

Usage:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\submit_controlfoley.py"
"""
import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8188"
WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_sketch_title_audio.json"

# Input types that are LINKS (wired from other nodes), not widgets.
LINK_TYPES = {
    "CONTROLFOLEY_MODEL", "CONTROLFOLEY_VIDEO", "CONTROLFOLEY_AUDIO_FILE",
    "CONTROLFOLEY_VIDEO_FILE", "VIDEO", "IMAGE", "AUDIO", "MASK",
}


def get_object_info(node_type: str) -> dict:
    with urllib.request.urlopen(f"{BASE}/object_info/{node_type}", timeout=20) as r:
        return json.load(r)[node_type]["input"]


def main() -> int:
    wf = json.load(open(WF, encoding="utf-8"))
    links = {l[0]: l for l in wf["links"]}  # link_id -> [id, from_node, from_slot, to_node, to_slot, type]

    prompt = {}
    for n in wf["nodes"]:
        nid = str(n["id"])
        ntype = n["type"]
        info = get_object_info(ntype)
        required = info.get("required", {})

        # Widget inputs = required keys that are NOT link types, in /object_info order.
        def _type_of(v):
            if isinstance(v, list) and v and isinstance(v[0], str):
                return v[0]
            return None

        widget_names = [k for k, v in required.items() if _type_of(v) not in LINK_TYPES]

        inputs = {}
        wv = n.get("widgets_values", [])
        for i, name in enumerate(widget_names):
            if i < len(wv):
                inputs[name] = wv[i]

        # Link inputs from the node's inputs array.
        for inp in n.get("inputs", []):
            link_id = inp.get("link")
            if link_id is None:
                continue
            l = links.get(link_id)
            if l is None:
                continue
            inputs[inp["name"]] = [str(l[1]), l[2]]

        prompt[nid] = {"class_type": ntype, "inputs": inputs}
        print(f"[node {nid}] {ntype}: {len(widget_names)} widgets, {sum(1 for v in inputs.values() if isinstance(v, list))} links")

    payload = json.dumps({"prompt": prompt, "client_id": "vscode-mcp"}).encode()
    req = urllib.request.Request(f"{BASE}/prompt", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.load(r)

    print("prompt_id:", resp.get("prompt_id"))
    print("status:", resp.get("status"))
    if resp.get("status", {}).get("status_code") == 400:
        print("ERRORS:", json.dumps(resp.get("status", {}).get("messages"), indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
