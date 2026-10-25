import io
t = io.open(r"E:\Krea2\notes\NOTES.md", encoding="utf-8").read()
lines = t.split("\n")
print("### NOTES.md lines 1675-1780 (Claude personal take)")
for i in range(1674, min(1780, len(lines))):
    print("%4d: %s" % (i+1, lines[i][:230]))
print()
print("### SUMMARY.md (full)")
s = io.open(r"E:\Krea2\notes\SUMMARY.md", encoding="utf-8").read()
print(s)
