r"""
prep_swap_run.py — one-command prep for character-swap / seamless-vlog workflows.

Clones a template workflow and swaps in the manual-labour parts (video,
reference image(s), SAM3 tracking word, main prompt, audio dir) so the
result is READY TO QUEUE. The template file is never modified.

Usage examples:
  # video-in character swap (MiniMax-H3-Character-Swap-Mask_LOCAL.json)
  python prep_swap_run.py ^
      --template "E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\MiniMax-H3-Character-Swap-Mask_LOCAL.json" ^
      --out charswap_zidhan_scene3.json ^
      --video scene3.mp4 --sheet char2_sheet.png --track man

  # seamless vlog (withers_has_big_nattys_LOCAL.json)
  python prep_swap_run.py ^
      --template "...\withers_has_big_nattys_LOCAL.json" ^
      --out vlog_zidhan.json ^
      --ref0 zidhan_face_a.png --ref1 zidhan_scene.png --ref2 zidhan_anchor.png ^
      --audio-dir zidhan

Rules (D192: this only WRITES FILES — it never queues/runs anything):
  * writes a NEW file; the template is untouched
  * only widget values change (widgets_values + widgets_values_named);
    node/link structure is preserved exactly (verified after edit)
  * --prompt-file replaces the main prompt wholesale; otherwise the
    template prompt keeps its text and only the old tracking word is
    re-substituted with --track
  * --list-images shows candidate reference images from the output dirs
"""
import json, sys, os, argparse, datetime

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
OUT = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output"
IMG_DIRS = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\char_refset",
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\char_sheet",
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\refset_v7",
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\refset_v6",
]


def find_node(d, node_type):
    return [nd for nd in d["nodes"] if nd.get("type") == node_type]


def set_widget(nd, old_val, new_val, label):
    """Replace a widget value in BOTH widgets_values (positional) and
    widgets_values_named (dict) if present. Returns # of replacements."""
    n = 0
    wv = nd.get("widgets_values")
    if isinstance(wv, list):
        for i, v in enumerate(wv):
            if v == old_val:
                wv[i] = new_val
                n += 1
    elif isinstance(wv, dict):
        for k in list(wv.keys()):
            if wv[k] == old_val:
                wv[k] = new_val
                n += 1
    wvn = nd.get("widgets_values_named")
    if isinstance(wvn, dict):
        for k in list(wvn.keys()):
            if wvn[k] == old_val:
                wvn[k] = new_val
                n += 1
    if n == 0:
        raise SystemExit(f"ERROR: widget value {old_val!r} not found in node {nd.get('id')} ({label})")
    return n


def widget_strings(nd):
    """All string values in a node's widgets_values (list or dict form)."""
    wv = nd.get("widgets_values")
    if isinstance(wv, list):
        return [v for v in wv if isinstance(v, str)]
    if isinstance(wv, dict):
        return [v for v in wv.values() if isinstance(v, str)]
    return []


def link_map(d):
    m = {}
    for L in d.get("links", []):
        if isinstance(L, (list, tuple)) and L:
            m[L[0]] = (list(L)[1:5] + [None] * 4)[:4]
    return m  # id -> (from_node, from_slot, to_node, to_slot)


def main():
    ap = argparse.ArgumentParser(description="Prep a swap/vlog workflow variant (never runs it)")
    ap.add_argument("--template", required=True, help="template workflow JSON")
    ap.add_argument("--out", required=True, help="output workflow JSON (new file)")
    ap.add_argument("--video", help="source video filename for VHS_LoadVideo")
    ap.add_argument("--sheet", help="character sheet filename for the single-LoadImage swap template")
    ap.add_argument("--track", help="SAM3 tracking word (e.g. woman / man / 'the man in white')")
    ap.add_argument("--prompt-file", help="full replacement for the main prompt node")
    ap.add_argument("--ref0", help="reference image for ref_image_0")
    ap.add_argument("--ref1", help="reference image for ref_image_1")
    ap.add_argument("--ref2", help="reference image for ref_image_2")
    ap.add_argument("--audio-dir", help="subdir under output/prepped_audio for LoadAudioBatchFromDir")
    ap.add_argument("--list-images", action="store_true", help="list candidate reference images and exit")
    a = ap.parse_args()

    if a.list_images:
        for d in IMG_DIRS:
            if os.path.isdir(d):
                print(f"== {d} ==")
                for f in sorted(os.listdir(d)):
                    if f.lower().endswith((".png", ".jpg", ".jpeg")):
                        print("  ", f)
        return

    d = json.load(open(a.template, encoding="utf-8"))
    n_nodes, n_links = len(d["nodes"]), len(d.get("links", []))
    lm = link_map(d)

    # --- video (VHS_LoadVideo) ---
    if a.video:
        vnodes = find_node(d, "VHS_LoadVideo")
        if not vnodes:
            raise SystemExit("ERROR: no VHS_LoadVideo node in template")
        nd = vnodes[0]
        old = None
        for v in widget_strings(nd):
            if v.lower().endswith((".mp4", ".mov", ".webm")):
                old = v
                break
        if old is None:
            raise SystemExit(f"ERROR: no video filename found in node {nd['id']}")
        set_widget(nd, old, a.video, "video")
        print(f"video: {old} -> {a.video}")

    # --- character sheet (single LoadImage in swap templates) ---
    if a.sheet:
        inodes = find_node(d, "LoadImage")
        if not inodes:
            raise SystemExit("ERROR: no LoadImage node in template")
        nd = inodes[0]
        old = None
        for v in widget_strings(nd):
            if v.lower().endswith((".png", ".jpg", ".jpeg")):
                old = v
                break
        if old is None:
            raise SystemExit(f"ERROR: no image filename found in node {nd['id']}")
        set_widget(nd, old, a.sheet, "sheet")
        print(f"sheet: {old} -> {a.sheet}")

    # --- SAM3 tracking word (CLIPTextEncode feeding SAM3_VideoTrack) ---
    old_track = None
    if a.track:
        tnodes = find_node(d, "SAM3_VideoTrack")
        if not tnodes:
            raise SystemExit("ERROR: no SAM3_VideoTrack node in template")
        tn = tnodes[0]
        src_id = None
        for inp in tn.get("inputs", []):
            if inp.get("link") is not None:
                src = lm.get(inp["link"])
                if src and src[0] is not None:
                    # find the CLIPTextEncode output feeding the prompt/track input
                    for on in find_node(d, "CLIPTextEncode"):
                        for out in on.get("outputs", []):
                            if inp["link"] in (out.get("links") or []):
                                src_id = on["id"]
        if src_id is None:
            raise SystemExit("ERROR: could not find CLIPTextEncode feeding SAM3_VideoTrack")
        on = next(x for x in d["nodes"] if x["id"] == src_id)
        old_track = on.get("widgets_values", [None])[0]
        set_widget(on, old_track, a.track, "track")
        print(f"track: {old_track!r} -> {a.track!r}")

    # --- reference images (LoadImageCrop -> R2V ref_image_N) ---
    for slot, arg in ((0, a.ref0), (1, a.ref1), (2, a.ref2)):
        if not arg:
            continue
        r2v = find_node(d, "MiniMaxH3ReferenceToVideo")
        if not r2v:
            raise SystemExit("ERROR: no MiniMaxH3ReferenceToVideo node in template")
        target_link = None
        for inp in r2v[0].get("inputs", []):
            nm = inp.get("name", "")
            if nm == f"ref_image_{slot}" or nm.endswith(f".ref_image_{slot}"):
                target_link = inp.get("link")
                break
        if target_link is None:
            raise SystemExit(f"ERROR: no ref_image_{slot} input on R2V node")
        src = lm.get(target_link)
        if not src or src[0] is None:
            raise SystemExit(f"ERROR: ref_image_{slot} has no source link")
        on = next((x for x in d["nodes"] if x["id"] == src[0]), None)
        if on is None:
            raise SystemExit(f"ERROR: source node {src[0]} for ref_image_{slot} missing")
        old = None
        for v in widget_strings(on):
            if v.lower().endswith((".png", ".jpg", ".jpeg")):
                old = v
                break
        if old is None:
            raise SystemExit(f"ERROR: no image filename in node {on['id']}")
        set_widget(on, old, arg, f"ref_image_{slot}")
        print(f"ref_image_{slot}: {old} -> {arg}")

    # --- audio dir (LoadAudioBatchFromDir + paired PrimitiveNode) ---
    if a.audio_dir:
        newdir = os.path.join(OUT, "prepped_audio", a.audio_dir.replace("\\", "/"))
        anodes = find_node(d, "LoadAudioBatchFromDir")
        if not anodes:
            raise SystemExit("ERROR: no LoadAudioBatchFromDir node in template")
        an = anodes[0]
        # directory widget value = first string ending in a path separator or with drive
        old = None
        for v in widget_strings(an):
            if ("\\" in v) or ("/" in v):
                old = v
                break
        if old is None:
            raise SystemExit(f"ERROR: no directory value in node {an['id']}")
        set_widget(an, old, newdir, "audio dir")
        print(f"audio dir: {old} -> {newdir}")
        # paired PrimitiveNode feeding the directory input (same old value)
        for inp in an.get("inputs", []):
            if inp.get("name") == "directory" and inp.get("link") is not None:
                src = lm.get(inp["link"])
                if src and src[0] is not None:
                    on = next((x for x in d["nodes"] if x["id"] == src[0]), None)
                    if on and old in widget_strings(on):
                        set_widget(on, old, newdir, "audio dir (primitive)")
                        print(f"audio dir primitive synced")
        os.makedirs(newdir, exist_ok=True)
        with open(os.path.join(newdir, "README.txt"), "w", encoding="utf-8") as f:
            f.write(f"Prepped audio for {a.audio_dir} (one file per vlog clip, alphabetical order; D041: no music).\n")

    # --- main prompt (longest text widget in PrimitiveStringMultiline / String Literal) ---
    if a.prompt_file or (a.track and old_track):
        cands = []
        for t in ("PrimitiveStringMultiline", "String Literal"):
            for nd in find_node(d, t):
                for v in (nd.get("widgets_values") or []):
                    if isinstance(v, str) and len(v) > 100:
                        cands.append((nd, v))
        if not cands:
            if a.prompt_file:
                raise SystemExit("ERROR: no main prompt node found")
        else:
            nd, old_prompt = max(cands, key=lambda c: len(c[1]))
            if a.prompt_file:
                new_prompt = open(a.prompt_file, encoding="utf-8").read().rstrip("\n")
            else:
                new_prompt = old_prompt.replace(old_track, a.track)
            set_widget(nd, old_prompt, new_prompt, "main prompt")
            print(f"prompt: {len(old_prompt)} -> {len(new_prompt)} chars")

    # --- write new file, verify structure unchanged ---
    out_path = a.out
    if not os.path.isabs(out_path):
        out_path = os.path.join(WF, out_path)
    json.dump(d, open(out_path, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    d2 = json.load(open(out_path, encoding="utf-8"))
    assert len(d2["nodes"]) == n_nodes, "node count changed!"
    assert len(d2.get("links", [])) == n_links, "link count changed!"
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\nWRITTEN: {out_path}")
    print(f"(template untouched; {n_nodes} nodes / {n_links} links preserved; {stamp})")
    print("QUEUE THIS FILE in the ComfyUI UI (D192: user runs workflows).")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
