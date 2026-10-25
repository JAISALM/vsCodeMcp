import io
base = r"D:\models\vsCodeMcp\project-memory"
for f in ("EXPERIMENTS.md", "CURRENT_TASK.md", "DECISIONS.md"):
    t = io.open(base + "\\" + f, encoding="utf-8").read()
    print("=" * 20, f, "(%d chars)" % len(t))
    print(t[-1200:])
    print()
