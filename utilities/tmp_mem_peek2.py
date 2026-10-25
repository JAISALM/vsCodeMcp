import io, sys
def safe(s):
    return s.encode("cp1252", "replace").decode("cp1252")
t = io.open(r"D:\models\vsCodeMcp\project-memory\EXPERIMENTS.md", encoding="utf-8").read().split("\n")
print("=== EXPERIMENTS.md first 30 lines ===")
for i, l in enumerate(t[:30]):
    print("%4d: %s" % (i+1, safe(l)[:150]))
print("total lines:", len(t))
print()
print("=== last 20 lines ===")
for i, l in enumerate(t[-20:]):
    print("%4d: %s" % (len(t)-20+i+1, safe(l)[:150]))
