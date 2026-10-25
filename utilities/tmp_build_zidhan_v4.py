import json, io
src = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2d_jaisal_zidhan_v3.json", encoding="utf-8"))
keep = {55,56,57,82,85,90, 951,961,971,841,531,541,291}
nodes = [n for n in src["nodes"] if n["id"] in keep]
for n in nodes:
    if n["id"] == 841:
        n["widgets_values"] = ["Photorealistic portrait of a 26-year-old young man from Kerala (a Keralite), warm medium TAN skin tone, ROUND face with fuller rounder cheeks, BROAD WIDE nose (wider nose bridge, distinct from a narrow nose), ROUNDER WIDER set eyes (rounder than almond), FULLER THICKER lips, SHORT neat black hair (short crop, closely trimmed on the sides), a FULL DENSE DARK BEARD covering the entire jaw, chin and cheeks (thick connected beard and mustache, NOT clean-shaven, NOT just stubble), plain white t-shirt, SOLID PLAIN white studio background (uniform flat backdrop, NO pattern, NO texture, NO mosaic), soft even diffused light, natural film grain, photorealistic skin with real pores and subtle natural texture, high detail, sharp focus, ONLY ONE person, no other people, no duplicates"]
    if n["id"] == 531:
        n["widgets_values"] = [831,"fixed",12,1,"er_sde","simple",1]
    if n["id"] == 291:
        n["widgets_values"] = ["k2d_zidhan_v4"]
links = [lk for lk in src["links"] if lk[1] in keep and lk[3] in keep]
for n in nodes:
    for j, inp in enumerate(n.get("inputs", [])):
        inp["link"] = next((lk[0] for lk in links if lk[3]==n["id"] and lk[4]==j), None)
    for o in n.get("outputs", []):
        o["links"] = [lk[0] for lk in links if lk[1]==n["id"]] or None
w = {"id":"k2d-zidhan-v4","revision":0,"last_node_id":971,"last_link_id":max(l[0] for l in links),"nodes":nodes,"links":links}
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2d_zidhan_v4.json"
with io.open(p,"w",encoding="utf-8") as f: f.write(json.dumps(w, indent=1))
print("WROTE", p, "nodes:", len(nodes), "links:", len(links))
