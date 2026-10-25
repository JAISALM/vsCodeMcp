"""Report: D:\models subdirectory sizes + D: recycle-bin contents with original paths."""
import os
import sys

def dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total

print("=" * 70)
print("D:\\models — subdirectory sizes")
print("=" * 70)
base = r"D:\models"
subs = []
for name in os.listdir(base):
    p = os.path.join(base, name)
    if os.path.isdir(p):
        subs.append((dir_size(p), name))
    else:
        try:
            subs.append((os.path.getsize(p), name))
        except OSError:
            pass
subs.sort(reverse=True)
for sz, name in subs:
    print("{:10.1f} GB   D:\\models\\{}".format(sz / 1e9, name))
print()

print("=" * 70)
print("D:\\$RECYCLE.BIN — contents with original paths")
print("=" * 70)
rbase = r"D:\$RECYCLE.BIN"
entries = []
total = 0
for root, dirs, files in os.walk(rbase):
    for f in files:
        if f.startswith("$R"):
            p = os.path.join(root, f)
            try:
                sz = os.path.getsize(p)
                total += sz
                entries.append((sz, f, root))
            except OSError:
                pass
entries.sort(reverse=True)
print("total: %.1f GB  files: %d" % (total / 1e9, len(entries)))
for sz, rid, bucket in entries[:30]:
    orig = "?"
    iid = rid.replace("$R", "$I")
    ip = os.path.join(bucket, iid)
    if os.path.exists(ip):
        data = open(ip, "rb").read()
        if len(data) > 0x64:
            try:
                path = data[0x4C:0x4C + 512].decode("utf-16-le", errors="ignore").split("\x00")[0]
                orig = path
            except Exception:
                orig = "parse-fail"
    print("{:9.1f} MB  {:<26} orig={}".format(sz / 1e6, rid, orig[:90]))
