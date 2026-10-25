import io
t = io.open(r"D:\models\vsCodeMcp\project-memory\EXPERIMENTS.md", encoding="utf-8").read().split("\n")
print("=== EXPERIMENTS.md first 40 lines ===")
for i, l in enumerate(t[:40]):
    print("%4d: %s" % (i+1, l[:160]))
print()
print("total lines:", len(t))
