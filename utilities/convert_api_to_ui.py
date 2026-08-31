"""
Convert ComfyUI workflow files from API/prompt format to UI format.

API format:  { "<node_id>": {"class_type": "...", "inputs": {...}}, ... }
UI format:   { "nodes": [...], "links": [...], "version": 0.4, ... }

The ComfyUI UI only renders UI format; API-format files show an empty canvas.
UI format is the universal format (works in the UI AND in MCP, which converts
UI->API internally).

This script:
  - backs up each original as <name>.api.bak.json
  - reconstructs nodes (id/type/pos/size/inputs/outputs/widgets_values/named)
  - reconstructs links
  - uses object_info schemas for input/output types and widget ordering
"""
import json, os, sys

W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
OI = json.load(open(r"d:\models\vsCodeMcp\data\object_info_cache.json", encoding="utf-8"))

# Link-type inputs (these come from other nodes, not widgets)
LINK_TYPES = {"MODEL","CLIP","VAE","CONDITIONING","LATENT","IMAGE","MASK","AUDIO","VIDEO",
              "GUIDER","SAMPLER","SIGMAS","NOISE","INT","FLOAT","BOOLEAN","STRING",
              "COMBO","IMAGE_LIST","MASK_LIST","AUDIO_LIST","VIDEO_LIST"}

def schema(ct):
    return OI.get(ct)

def output_types(ct):
    s = schema(ct)
    if not s: return []
    out = s.get("output", [])
    return out if isinstance(out, list) else [out]

def input_schema(ct):
    s = schema(ct)
    if not s: return {}, {}
    inp = s.get("input", {})
    return inp.get("required", {}), inp.get("optional", {})

def input_type(ct, key):
    req, opt = input_schema(ct)
    if key in req: return req[key][0]
    if key in opt: return opt[key][0]
    return "STRING"

def is_link(value):
    # a link is [node_id, slot] where node_id is str/int and slot is int
    return (isinstance(value, list) and len(value) == 2
            and isinstance(value[1], int)
            and isinstance(value[0], (str, int)))

def schema_order_keys(nid, keys, class_types):
    """Order input keys by the node's schema input_order (required first),
    preserving any unknown keys at the end in original order."""
    ct = class_types[nid]
    s = schema(ct)
    io = s.get("input_order", {}).get("required", []) if s else []
    known = [k for k in io if k in keys]
    extra = [k for k in keys if k not in io]
    return known + extra

def convert(path):
    with open(path, encoding="utf-8") as f:
        api = json.load(f)
    if isinstance(api.get("nodes"), list):
        return None  # already UI format

    node_ids = list(api.keys())
    class_types = {nid: api[nid]["class_type"] for nid in node_ids}

    # --- build links ---
    # to_slot = index of this link input among the node's link inputs (in schema order),
    # which is exactly its position in the node's inputs array (link inputs come first).
    links = []
    link_id = 0
    link_for = {}
    out_links = {nid: {} for nid in node_ids}
    for nid in node_ids:
        link_input_keys = [k for k, v in api[nid]["inputs"].items() if is_link(v)]
        ordered_link_keys = schema_order_keys(nid, link_input_keys, class_types)
        for to_slot, key in enumerate(ordered_link_keys):
            src, slot = api[nid]["inputs"][key][0], api[nid]["inputs"][key][1]
            link_id += 1
            src_out = output_types(class_types.get(src, ""))
            ltype = src_out[slot] if slot < len(src_out) else "LINK"
            links.append([link_id, src, slot, nid, to_slot, ltype])
            link_for[(nid, key)] = link_id
            out_links[src].setdefault(slot, []).append(link_id)

    # --- build nodes ---
    nodes = []
    # topological-ish order: sort by (number of incoming links) so loaders come first
    incoming = {nid: 0 for nid in node_ids}
    for nid in node_ids:
        for key, val in api[nid]["inputs"].items():
            if is_link(val):
                incoming[nid] += 1
    ordered = sorted(node_ids, key=lambda n: (incoming[n], n))

    for idx, nid in enumerate(ordered):
        ct = class_types[nid]
        req, opt = input_schema(ct)
        # widget keys = inputs that are NOT links
        widget_keys = [k for k, v in api[nid]["inputs"].items() if not is_link(v)]
        link_keys = [k for k, v in api[nid]["inputs"].items() if is_link(v)]

        # order: link inputs first (schema order), then widget inputs (schema order)
        ordered_link_keys = schema_order_keys(nid, link_keys, class_types)
        ordered_widget_keys = schema_order_keys(nid, widget_keys, class_types)

        inputs_arr = []
        # link inputs
        for key in ordered_link_keys:
            inputs_arr.append({
                "localized_name": key, "name": key,
                "type": input_type(ct, key),
                "link": link_for[(nid, key)],
            })
        # widget inputs
        for key in ordered_widget_keys:
            inputs_arr.append({
                "localized_name": key, "name": key,
                "type": input_type(ct, key),
                "widget": {"name": key},
                "link": None,
            })

        # outputs
        outs = output_types(ct)
        outputs_arr = []
        for slot, oname in enumerate(outs):
            outputs_arr.append({
                "localized_name": oname, "name": oname,
                "type": oname,
                "links": out_links[nid].get(slot, []),
            })

        # widgets_values (positional, widget order) + named
        widgets_values = [api[nid]["inputs"][k] for k in ordered_widget_keys]
        widgets_values_named = {k: api[nid]["inputs"][k] for k in ordered_widget_keys}

        # layout: grid by index
        col, row = idx % 4, idx // 4
        node = {
            "id": nid,
            "type": ct,
            "pos": [col * 420, row * 320],
            "size": [340, 180],
            "flags": {},
            "order": idx,
            "mode": 0,
            "inputs": inputs_arr,
            "outputs": outputs_arr,
            "properties": {"Node name for S&R": ct},
            "widgets_values": widgets_values,
            "widgets_values_named": widgets_values_named,
        }
        nodes.append(node)

    # top-level
    numeric_ids = [int(n["id"]) for n in nodes if str(n["id"]).isdigit()]
    last_node_id = max(numeric_ids) if numeric_ids else 0
    out = {
        "id": "converted-" + os.path.basename(path).replace(".json", ""),
        "revision": 0,
        "last_node_id": last_node_id,
        "last_link_id": link_id,
        "nodes": nodes,
        "links": links,
        "groups": [],
        "config": {},
        "extra": {},
        "version": 0.4,
    }
    return out

def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else None
    if files is None:
        files = [f for f in os.listdir(W) if f.endswith(".json") and f != ".index.json"]
    converted, skipped, errors = [], [], []
    for fn in files:
        p = os.path.join(W, fn)
        try:
            with open(p, encoding="utf-8") as f:
                probe = json.load(f)
            if isinstance(probe.get("nodes"), list):
                skipped.append(fn)
                continue
            result = convert(p)
            if result is None:
                skipped.append(fn)
                continue
            # backup original
            bak = p + ".api.bak"
            if not os.path.exists(bak):
                os.replace(p, bak)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=1)
            converted.append((fn, len(result["nodes"]), len(result["links"])))
        except Exception as e:
            errors.append((fn, str(e)))
    print("CONVERTED:")
    for fn, nn, nl in converted:
        print("  %s  (%d nodes, %d links)" % (fn, nn, nl))
    print("SKIPPED (already UI):", skipped)
    print("ERRORS:")
    for fn, e in errors:
        print("  %s: %s" % (fn, e))

if __name__ == "__main__":
    main()
