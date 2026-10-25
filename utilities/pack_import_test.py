"""Pack import test for a core update — standalone-context import of every
custom_nodes pack; reports class-count deltas + failures.

Usage (from the ComfyUI root, embedded python):
  python pack_import_test.py [out_json]

Rebuild of the lost `rag/baseline_tmp2.py` (2026-10-25). Harness caveats
(same as the original baseline):
- run with cwd = ComfyUI root so `utils`/`app`/`nodes` resolve;
- stdout is forced to UTF-8 (packs print emoji at import; a cp1252 console
  raises UnicodeEncodeError INSIDE the import and fakes a FAIL);
- entry-point selection is approximate ([dirname].py, then sorted *.py, then
  __init__.py) — the class COUNT is not comparable to the original baseline
  for most packs, but the OK/FAIL STATUS is the meaningful signal;
- known standalone artifacts (NOT server-state): `PromptServer.instance`
  AttributeError on module-level server access, `mediapipe.solutions` on
  controlnetaux, 0-class packs that only register lazily.
"""
import importlib.util, json, os, sys

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"
CN = os.path.join(ROOT, "custom_nodes")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "pack_import_results.json")

sys.path.insert(0, ROOT)
import nodes as core_nodes  # noqa
MAPPINGS = core_nodes.NODE_CLASS_MAPPINGS


def try_import_pack(full, name):
    """Return (module_name, error) trying the usual pack entry points in
    <full> (absolute pack dir)."""
    candidates = [name]
    for f in sorted(os.listdir(full)):
        if f.endswith(".py"):
            candidates.append(f[:-3])
    seen = set()
    last_err = None
    for cand in candidates:
        path = os.path.join(full, cand + ".py")
        if cand != name and not os.path.exists(path):
            continue
        if cand in seen or cand in sys.modules:
            continue
        seen.add(cand)
        modname = f"{name}::{cand}"
        try:
            spec = importlib.util.spec_from_file_location(modname, path)
            if spec is None:
                last_err = f"no spec for {cand}.py"
                continue
            mod = importlib.util.module_from_spec(spec)
            sys.modules[modname] = mod
            spec.loader.exec_module(mod)
            return modname, None
        except Exception as e:
            sys.modules.pop(modname, None)
            last_err = f"{type(e).__name__}: {str(e)[:120]}"
    if os.path.exists(os.path.join(full, "__init__.py")):
        try:
            spec = importlib.util.spec_from_file_location(
                f"{name}::init", os.path.join(full, "__init__.py"),
                submodule_search_locations=[full])
            mod = importlib.util.module_from_spec(spec)
            sys.modules[f"{name}::init"] = mod
            spec.loader.exec_module(mod)
            return f"{name}::__init__", None
        except Exception as e:
            sys.modules.pop(f"{name}::init", None)
            last_err = f"__init__: {type(e).__name__}: {str(e)[:120]}"
    return None, last_err or "no candidates"


results = {}
for d in sorted(os.listdir(CN)):
    full = os.path.join(CN, d)
    if not os.path.isdir(full) or d.startswith(".") or d == "__pycache__":
        continue
    before = len(MAPPINGS)
    sys.path.insert(0, full)
    try:
        modname, err = try_import_pack(full, d)
        after = len(MAPPINGS)
        results[d] = f"OK ({after - before} classes)" if err is None else f"FAIL {err}"
    except Exception as e:
        results[d] = f"FAIL uncaught {type(e).__name__}: {str(e)[:120]}"
    finally:
        sys.path.remove(full)

json.dump(results, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"pack import results -> {OUT} ({len(results)} packs)")
fails = [k for k, v in results.items() if v.startswith("FAIL")]
print(f"FAIL ({len(fails)}): {', '.join(fails) if fails else 'none'}")
