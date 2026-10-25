"""List contents of D: recycle bin (user SID folder) — biggest files first."""
import os

rb = "D:\\$RECYCLE.BIN"
for name in os.listdir(rb):
    p = os.path.join(rb, name)
    if os.path.isdir(p):
        rows = []
        total = 0
        for root, dirs, files in os.walk(p):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    sz = os.path.getsize(fp)
                    total += sz
                    rows.append((sz, os.path.relpath(fp, p)))
                except OSError as e:
                    print("  UNREADABLE:", fp, e)
        rows.sort(reverse=True)
        print("\n### {}  ->  {:.1f} GB, {} files".format(name, total / 1e9, len(rows)))
        for sz, rel in rows[:25]:
            print("  {:9.1f} MB  {}".format(sz / 1e6, rel[:100]))
