"""Dump full port bindings + internal links of the engine subgraphs."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))

for s in j.get("definitions", {}).get("subgraphs", []):
    sgid = str(s.get("id", "?"))
    if not any(x in sgid for x in ("e015af7a", "32ae36f6", "caf99728")):
        continue
    print(f"== subgraph {sgid} ==")
    print("  inputs:", json.dumps(s.get("inputs"), indent=2)[:1500])
    print("  outputs:", json.dumps(s.get("outputs"), indent=2)[:800])
    print("  internal links:", s.get("links"))
    print("  node ids:", [n["id"] for n in s.get("nodes", [])])
    print()
