import re
for p in [r"D:\models\Gemma\Gemma4-31B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf",
          r"D:\models\Gemma\gemma-4-Ortenzya-The-Creative-Wordsmith-31B-it-uncensored-heretic-Q5_K_M.gguf",
          r"D:\models\Gemma\mtp-gemma-4-31B-it.gguf"]:
    with open(p, "rb") as f:
        head = f.read(4 * 1024 * 1024)
    names = re.findall(rb"[\x20-\x7e]{4,60}", head[:2_000_000])
    mtp = [n.decode() for n in names if b"mtp" in n.lower() or b"assistant" in n.lower()]
    import os
    print(os.path.basename(p))
    print(f"  mtp/assistant tokens in header: {len(mtp)}")
    for m in mtp[:15]:
        print(f"    {m}")
    print()
