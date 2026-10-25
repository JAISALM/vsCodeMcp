import io
base = r"D:\models\vsCodeMcp\project-memory"
for f in ("EXPERIMENTS.md", "CURRENT_TASK.md"):
    p = base + "\\" + f
    t = io.open(p, encoding="utf-8").read()
    n = t.count("\\\\")
    print(f, "double-backslash count:", n)
    if n:
        t2 = t.replace("\\\\", "\\")
        io.open(p, "w", encoding="utf-8").write(t2)
        print(f, "-> fixed")
