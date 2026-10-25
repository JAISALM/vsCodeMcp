import json, io
w = json.load(open(r"D:\models\vsCodeMcp\utilities\official_image_krea2_turbo_t2i.json", encoding="utf-8"))
nodes = {n["id"]: n for n in w["nodes"]}
inst = nodes[30]
print("=== instance node 30 ===")
print("type:", inst["type"])
print("widgets_values:", inst.get("widgets_values"))
print("widgets_values_named:", json.dumps(inst.get("widgets_values_named"), indent=1)[:1500])
print("inputs:")
for i, inp in enumerate(inst.get("inputs", [])):
    print("  slot", i, inp.get("name"), "type", inp.get("type"), "link", inp.get("link"))
print("outputs:")
for i, o in enumerate(inst.get("outputs", [])):
    print("  slot", i, o.get("name"), "type", o.get("type"), "links", o.get("links"))
# internal wiring of the subgraph
sub = w["definitions"]["subgraphs"][0]
sn = {n["id"]: n for n in sub["nodes"]}
print("=== internal links (prompt-related) ===")
for L in sub.get("links", []):
    lid, fn, fs, tn, ts, t = L
    if t in ("STRING", "BOOLEAN") or tn in (6, 16, 17, 21, 22, 27, 28):
        print("  link", lid, "node", fn, "out", fs, "-> node", tn, "in", ts, t)
# widget shapes of the prompt nodes
for nid in (18, 19, 23, 24, 16, 17, 27):
    n = sn[nid]
    print(nid, n["type"], "widgets:", n.get("widgets_values"), "named:", json.dumps(n.get("widgets_values_named"))[:200])
