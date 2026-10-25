import io, re
t = io.open(r"E:\Krea2\notes\NOTES.md", encoding="utf-8").read()
lines = t.split("\n")
pats = re.compile(r"rain|water|droplet|mist|splash|monsoon|wet", re.I)
opus = re.compile(r"opus|claude|restructur", re.I)
print("=== rain/water/mist lines ===")
for i, l in enumerate(lines):
    if pats.search(l):
        print("%4d: %s" % (i+1, l[:200]))
print()
print("=== opus/claude/restructure lines ===")
for i, l in enumerate(lines):
    if opus.search(l):
        print("%4d: %s" % (i+1, l[:200]))
