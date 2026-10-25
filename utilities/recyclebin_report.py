"""List D: recycle-bin files ($R*) with sizes + original paths from $I metadata."""
import os

base = r"D:\$RECYCLE.BIN"
entries = []
total = 0
for root, dirs, files in os.walk(base):
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
print()
for sz, rid, bucket in entries[:30]:
    orig = "?"
    iid = rid.replace("$R", "$I")
    ip = os.path.join(bucket, iid)
    if os.path.exists(ip):
        data = open(ip, "rb").read()
        if len(data) > 0x64:
            # $I format: 0x00-0x03 file size, 0x04-0x07 size on disk, 0x08-0x0B deleted time,
            # 0x0C-0x0F volume serial, 0x10-0x23 original size..., 0x24+ flags/attrs,
            # 0x4C+ original path as UTF-16LE
            try:
                path = data[0x4C:0x4C + 512].decode("utf-16-le", errors="ignore").split("\x00")[0]
                orig = path
            except Exception:
                orig = "parse-fail"
    print("{:9.1f} MB  {:<24} orig={}".format(sz / 1e6, rid, orig[:90]))
