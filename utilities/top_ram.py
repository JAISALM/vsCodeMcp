import os

# Try psutil first
try:
    import psutil
    procs = []
    for p in psutil.process_iter(['name', 'memory_info', 'pid']):
        try:
            mem = p.info['memory_info'].rss
            procs.append((p.info['name'], p.info['pid'], mem))
        except Exception:
            pass
    procs.sort(key=lambda x: x[2], reverse=True)
    print('=== Top 25 RAM-consuming processes (psutil) ===')
    total = sum(p[2] for p in procs)
    for name, pid, mem in procs[:25]:
        print(f'{name} (pid {pid}): {mem/1e9:.2f} GB')
    print(f'\nTotal across all processes: {total/1e9:.1f} GB')
except ImportError:
    print('psutil not available -> falling back to tasklist')
    import subprocess
    out = subprocess.check_output(['tasklist', '/FO', 'CSV', '/NH'], text=True)
    rows = []
    for line in out.splitlines():
        parts = line.split('","')
        if len(parts) >= 5:
            name = parts[0].strip('"')
            mem = parts[4].strip('"').replace(',', '')
            try:
                rows.append((name, int(mem)))
            except ValueError:
                pass
    rows.sort(key=lambda x: x[1], reverse=True)
    print('=== Top 25 RAM-consuming processes (tasklist) ===')
    for name, mem in rows[:25]:
        print(f'{name}: {mem/1e6:.2f} GB')
