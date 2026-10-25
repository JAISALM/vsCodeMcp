#!/usr/bin/env python
"""Map the user's new Qwen 2.1 LLM-architect character-sheet workflow:
top-level nodes + subgraph instances + LoadImage widgets + ThinkingLLM subgraph internals."""
import json

j = json.load(open(r"E:\minimax_workflow\character_sheet\Qwen Image 2.1 Character Design Sheet.json", encoding="utf-8"))
print("top keys:", list(j.keys()))
nodes = j.get("nodes", [])
print(f"nodes: {len(nodes)}\n")
for n in nodes:
    w = n.get("widgets_values") or []
    ws = " | ".join(str(x)[:80] for x in w[:4])
    print(f"id={n['id']:>4} {n['type']:<38} widgets=[{ws}]")

print("\n=== subgraph definitions ===")
for key, sg in (j.get("definitions", {}).get("subgraphs") or {}).items():
    print(f"\n-- subgraph {key}: {len(sg.get('nodes', []))} nodes")
    for n in sg.get("nodes", []):
        w = n.get("widgets_values") or []
        ws = " | ".join(str(x)[:100] for x in w[:5])
        print(f"  id={n['id']:>4} {n['type']:<40} widgets=[{ws}]")
