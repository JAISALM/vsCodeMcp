import json, io
w = json.load(open(r"D:\models\vsCodeMcp\utilities\official_image_krea2_turbo_t2i.json", encoding="utf-8"))
print("top-level keys:", list(w.keys()))
print("version:", w.get("version"))
nodes = w.get("nodes", [])
print("top-level nodes:", len(nodes))
for n in nodes:
    print("  node", n["id"], n["type"], "pos", n.get("pos"))
subs = w.get("definitions", {}).get("subgraphs", [])
print("subgraphs:", len(subs))
for s in subs:
    print(" subgraph id:", s.get("id"), "nodes inside:", len(s.get("nodes", [])))
    for n in s.get("nodes", []):
        print("   sub-node", n["id"], n["type"], "widgets:", [x for x in n.get("widgets_values", []) if not isinstance(x, str) or len(x) < 70])
