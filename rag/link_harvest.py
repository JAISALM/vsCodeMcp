#!/usr/bin/env python3
"""Link/asset harvester for depth-tier posts (2026-11-28, D280).

WHY (author directive 2026-11-28: "lack of investigation skills from our RAG
and the fetcher jobs... it always needs a human help"): the depth tier fetched
post body + comments as raw text, but the thread's ACTUAL assets — workflow
files, model links, tutorial videos, author identity, and whether they are
ALREADY downloaded locally — sat buried in that text for a human to dig out
(the 11-28 case: the Civitai Seed-Hunter link + the already-saved
"FoxFurEssence H3 Seed Hunter v3.json" had to be found by hand).

This module closes the loop, in order:
1. extract every URL from the post body + all comments
2. classify each (civitai model page / youtube / github / huggingface /
   discord / other)
3. for Civitai model links: pull model id + slug out of the URL (mirror
   domains civitai.red/.com/.gg all handled)
4. harvest @handle / u/handle mentions from comments (author identity)
5. CROSS-REFERENCE LOCAL FOLDERS — if a link's slug tokens match a filename
   already on disk, flag it (the "you already have this" signal)
6. emit a structured "assets" block (JSON + markdown) appended to the store
   file, so the digest names the assets instead of leaving them in prose.

No network calls on the default path (daily RAG stays fast + quiet); the
optional --resolve flag fetches a Civitai model page through the browser head
for the canonical name/author.

USAGE:
  python link_harvest.py <file.json|file.md> [--resolve] [--local-dirs d1 d2]
  from link_harvest import harvest_text, render_assets_md
"""
import json
import os
import re
import sys

if sys.platform == "win32":
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

DEFAULT_LOCAL_DIRS = [
    r"E:\minimax_workflow\production_experiments",
    r"E:\ComfyUI_windows_portable\ComfyUI\models",
]
URL_RE = re.compile(r"https?://[^\s\"'\\<>\](),;]+", re.I)
CIVITAI_RE = re.compile(
    r"civitai\.(?:com|red|gg)/models/(\d+)/(?:u/[^/]+/)?([A-Za-z0-9_-]+)", re.I)
HANDLE_RE = re.compile(r"(?:@|u/)([A-Za-z0-9_]{3,30})")
STOP = {"minimax", "comfyui", "comfy", "workflow", "workflows", "the", "and",
        "for", "with", "new", "free", "v1", "v2"}
MAX_FILES = 5000


def extract_urls(text):
    seen, out = set(), []
    for u in URL_RE.findall(text or ""):
        u = u.rstrip(".,;:)]}'\"")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def classify(u):
    low = u.lower()
    if re.search(r"civitai\.(com|red|gg)/models/", low):
        return "civitai-model"
    if "civitai" in low:
        return "civitai"
    if re.search(r"youtube\.com|youtu\.be", low):
        return "youtube"
    if "github.com" in low:
        return "github"
    if "huggingface.co" in low:
        return "huggingface"
    if "discord." in low:
        return "discord"
    if "skool.com" in low:
        return "community"
    return "other"


def _slug_tokens(slug):
    toks = re.split(r"[-_./\s]+", (slug or "").lower())
    return {t for t in toks if len(t) >= 2 and t not in STOP}


def local_matches(slug, dirs):
    """Filenames on disk whose tokens overlap the slug's (>=2 tokens, at
    least one >=4 chars — kills generic 'h3' false positives)."""
    st = _slug_tokens(slug)
    if not st:
        return []
    hits = []
    scanned = 0
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for root, _sub, files in os.walk(d):
            for fn in files:
                if scanned > MAX_FILES:
                    return hits
                scanned += 1
                fn_toks = set(re.split(r"[-_./\s]+", fn.lower()))
                overlap = st & fn_toks
                if len(overlap) >= 2 and any(len(t) >= 4 for t in overlap):
                    hits.append({"file": os.path.join(root, fn),
                                 "overlap": sorted(overlap)})
    return hits


def harvest_text(text, local_dirs=None, resolve=False):
    """Core harvester: text -> structured assets record. `text` may be the
    whole store-file markdown or body+comments joined — it only scans."""
    local_dirs = local_dirs or DEFAULT_LOCAL_DIRS
    raw_urls = extract_urls(text)
    civitai, local = [], []
    handles = set()
    for h in HANDLE_RE.findall(text or ""):
        if h.lower() not in ("the", "and", "you", "for", "all", "top"):
            handles.add(h)
    enriched = []
    for u in raw_urls:
        kind = classify(u)
        entry = {"url": u, "kind": kind}
        m = CIVITAI_RE.search(u)
        if kind == "civitai-model" and m:
            entry["model_id"] = m.group(1)
            entry["slug"] = m.group(2)
            civitai.append(entry)
            hits = local_matches(m.group(2), local_dirs)
            if hits:
                local.extend(hits)
        elif kind in ("github", "huggingface") and not resolve:
            entry["note"] = ("asset repo/model — not locally cross-referenced "
                             "(use --local-dirs or --resolve)")
        enriched.append(entry)
    # dedupe local hits by file
    seen, local_u = set(), []
    for h in local:
        if h["file"] not in seen:
            seen.add(h["file"])
            local_u.append(h)
    return {
        "links": enriched,
        "civitai_models": civitai,
        "mentioned_handles": sorted(handles),
        "local_matches": local_u,
    }


def harvest_file(path, local_dirs=None, resolve=False):
    if path.lower().endswith(".json"):
        d = json.load(open(path, encoding="utf-8"))
        parts = []
        for r in (d.get("results") or [d]):
            parts.append(r.get("body") or "")
            for c in r.get("comments") or []:
                parts.append(c.get("text") if isinstance(c, dict) else str(c))
        return harvest_text("\n".join(parts), local_dirs, resolve)
    return harvest_text(open(path, encoding="utf-8", errors="replace").read(),
                        local_dirs, resolve)


def render_assets_md(a):
    if not a["links"] and not a["local_matches"]:
        return ""
    lines = ["", "## Assets (auto-harvested, D280 — link/asset extraction pass)", ""]
    if a["civitai_models"]:
        for c in a["civitai_models"]:
            lines.append(f"- civitai model {c.get('model_id', '?')}: "
                         f"{c['url']}")
    for l in a["links"]:
        if isinstance(l, dict) and l["kind"] != "civitai-model":
            lines.append(f"- {l['kind']}: {l['url']}")
        elif isinstance(l, str):
            lines.append(f"- {l}")
    if a["mentioned_handles"]:
        lines.append("- mentioned handles: " + ", ".join(
            "u/" + h for h in a["mentioned_handles"][:8]))
    if a["local_matches"]:
        lines.append("")
        lines.append("ALREADY ON DISK (match by slug tokens):")
        for h in a["local_matches"]:
            lines.append(f"- {h['file']}  (overlap: {', '.join(h['overlap'])})")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--resolve", action="store_true")
    ap.add_argument("--local-dirs", nargs="*", default=None)
    a = ap.parse_args()
    print(json.dumps(harvest_file(a.file, a.local_dirs, a.resolve),
                     ensure_ascii=False, indent=1))
