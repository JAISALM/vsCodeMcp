# Local font overrides for lesson-shorts Template B

The renderer (`utilities\lesson_shorts_template_b.py`) checks this directory
FIRST, then falls back to system fonts:

| file to drop here | replaces (system fallback) | used for |
|---|---|---|
| `caption.ttf` | Palatino italic (`palai.ttf`) | caption + hook lines (italic serif) |
| `big.ttf` | Palatino italic | big hook lines |
| `close.ttf` | Baskerville (`BASKVILL.TTF`) | closing line (upright serif) |
| `label.ttf` | Arial Bold (`arialbd.ttf`) | card labels / stat labels |
| `handle.ttf` | Arial (`arial.ttf`) | @handle watermark |

Rules:
- Any .ttf/.otf works (name it as above). No install/admin needed — the engine
  just loads it from this folder.
- **Offline constraint (D228):** the machine is offline until **2026-11-24** —
  no font downloads. Either copy a .ttf from another machine into this folder,
  or the agent installs a chosen font (e.g. Source Serif 4 / EB Garamond /
  Cormorant Garamond) after the window opens.
- Re-render after dropping a file: `python utilities\lesson_shorts_ubu_al_amal.py`
  (fonts are loaded at render start).
