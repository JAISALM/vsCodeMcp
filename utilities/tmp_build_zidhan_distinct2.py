import json, io
src = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2c_jaisal_zidhan_v2.json", encoding="utf-8"))
shared = {55,56,57,82,85,90}
branch = {951,961,971,841,531,541,291}
keep = shared | branch
nodes = [n for n in src["nodes"] if n["id"] in keep]
for n in nodes:
    if n["id"] == 841:
        n["widgets_values"] = ["Photorealistic portrait of a 26-year-old young man from Kerala (a Keralite), warm medium TAN skin tone, ROUND face with fuller rounder cheeks (distinctly rounder than a slim oval face), broader wider nose, almond shaped eyes, slightly wider set ears, FULL short dense trimmed beard, short neat black hair in a clean halal fade crop, slim build, plain white t-shirt, SOLID PLAIN white studio background (uniform flat backdrop, NO pattern, NO texture, NO mosaic), soft even diffused light, natural film grain, photorealistic skin with real pores and subtle natural texture, high detail, sharp focus, ONLY ONE person, no other people, no duplicates"]
    if n["id"] == 531:
        n["widgets_values"] = [812,"fixed",12,1,"er_sde","simple",1]
    if n["id"] == 291:
        n["widgets_values"] = ["k2c_zidhan_distinct2"]
links = [lk for lk in src["links"] if lk[1] in keep and lk[3] in keep]
for n in nodes:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in links if lk[3]==n["id"] and lk[4]==j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in links if lk[1]==n["id"]] or None
w = {"id":"k2c-zidhan-distinct2","revision":0,"last_node_id":971,"last_link_id":max(l[0] for l in links),"nodes":nodes,"links":links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2c_zidhan_distinct2.json"
with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
