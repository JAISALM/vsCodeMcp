"""Markdown chunking with section awareness + stable ids (idempotent re-ingest)."""
import hashlib
import os
import re
from datetime import datetime


def section_chunks(text: str, max_chars: int = 1600, overlap: int = 150):
    """Split markdown into section-aware chunks.

    Sections start at ## / ### headings. Each section is split into
    max_chars pieces with overlap. Chunk context = file H1 + section heading
    so embeddings know what the text is about.
    Yields (section_title, chunk_text_with_context_prefix).
    """
    lines = text.split("\n")
    h1 = None
    for ln in lines:
        if ln.startswith("# "):
            h1 = ln[2:].strip()
            break

    sections = []
    cur_title, buf = "(intro)", []
    for ln in lines:
        if re.match(r"^#{2,6}\s", ln):
            if buf:
                sections.append((cur_title, "\n".join(buf).strip()))
            cur_title = re.sub(r"^#{2,6}\s*", "", ln).strip()
            buf = []
        else:
            buf.append(ln)
    if buf:
        sections.append((cur_title, "\n".join(buf).strip()))

    for title, body in sections:
        if not body:
            continue
        prefix = f"[{h1 or 'doc'} > {title}]\n"
        if len(body) <= max_chars:
            yield title, prefix + body
            continue
        start = 0
        while start < len(body):
            piece = body[start:start + max_chars]
            yield title, prefix + piece
            if start + max_chars >= len(body):
                break
            start += max_chars - overlap


def file_chunks(path: str, max_chars: int = 1600, overlap: int = 150):
    """All chunks of a file as (chunk_id, text, metadata)."""
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    h1 = None
    for ln in text.split("\n")[:50]:
        if ln.startswith("# "):
            h1 = ln[2:].strip()
            break
    mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")
    out = []
    for i, (title, ctext) in enumerate(section_chunks(text, max_chars, overlap)):
        cid = hashlib.sha1(f"{os.path.basename(path)}|{title}|{i}|{len(text)}".encode()).hexdigest()[:16]
        out.append((cid, ctext, {
            "file": os.path.basename(path),
            "section": title,
            "doc": h1 or os.path.basename(path),
            "modified": mtime,
        }))
    return out
