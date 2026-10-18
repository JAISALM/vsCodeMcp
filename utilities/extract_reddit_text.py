r"""Extract the post body text from a saved rendered Reddit DOM (P*_dsh.html).
Usage: python extract_reddit_text.py <in.html> <out.txt>
Strips the shreddit-post element's tags -> readable text. No network access.
"""
import sys, re, html as h

def extract(path):
    raw = open(path, encoding="utf-8").read()
    m = re.search(r"<shreddit-post\b[^>]*>", raw)
    if not m:
        return "(shreddit-post element not found)"
    start = m.end()
    end = raw.find("</shreddit-post>", start)
    seg = raw[start:end if end > start else start + 400000]
    seg = re.sub(r"<!--.*?-->", " ", seg, flags=re.S)
    seg = re.sub(r"<(script|style)\b.*?</\1>", " ", seg, flags=re.S | re.I)
    # keep block boundaries as newlines
    seg = re.sub(r"</(p|div|h[1-6]|li|tr|section)>", "\n", seg, flags=re.I)
    seg = re.sub(r"<br\s*/?>", "\n", seg, flags=re.I)
    text = re.sub(r"<[^>]+>", "", seg)
    text = h.unescape(text)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    # de-dup consecutive identical lines (Reddit DOM repeats some labels)
    out = []
    for ln in lines:
        if not out or out[-1] != ln:
            out.append(ln)
    return "\n".join(out)

if __name__ == "__main__":
    txt = extract(sys.argv[1])
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"{len(txt)} chars -> {sys.argv[2]}")
