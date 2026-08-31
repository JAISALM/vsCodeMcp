import urllib.request, json, ctypes, psutil

BASE = 'http://127.0.0.1:8188'

def get(path):
    try:
        with urllib.request.urlopen(BASE + path, timeout=5) as r:
            return json.load(r)
    except Exception as e:
        return {'ERROR': str(e)}

# 1. ComfyUI's actual launch args (argv) — verify --lowvram is gone
ss = get('/system_stats')
argv = ss.get('system', {}).get('argv', [])
print('=== ComfyUI launch args (live) ===')
print(' '.join(argv) if argv else '(no argv)')
print()

# 2. Current RAM
class M(ctypes.Structure):
    _fields_ = [('dwLength', ctypes.c_uint32), ('dwMemoryLoad', ctypes.c_uint32),
                ('ullTotalPhys', ctypes.c_uint64), ('ullAvailPhys', ctypes.c_uint64),
                ('ullTotalPage', ctypes.c_uint64), ('ullAvailPage', ctypes.c_uint64),
                ('ullTotalVirtual', ctypes.c_uint64), ('ullAvailVirtual', ctypes.c_uint64),
                ('ullAvailExtendedVirtual', ctypes.c_uint64)]
m = M(); m.dwLength = ctypes.sizeof(m)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
print('=== System RAM (now) ===')
print(f'total {m.ullTotalPhys/1e9:.1f} GB | free {m.ullAvailPhys/1e9:.1f} GB | load {m.dwMemoryLoad}%')
print()

# 3. Top RAM processes (now)
procs = []
for p in psutil.process_iter(['name', 'memory_info', 'pid']):
    try:
        procs.append((p.info['name'], p.info['pid'], p.info['memory_info'].rss))
    except Exception:
        pass
procs.sort(key=lambda x: x[2], reverse=True)
print('=== Top 12 RAM processes (now) ===')
for name, pid, mem in procs[:12]:
    print(f'{name} (pid {pid}): {mem/1e9:.2f} GB')
print(f'total: {sum(p[2] for p in procs)/1e9:.1f} GB')
print()

# 4. ComfyUI's own VRAM/RAM view
dev = ss.get('devices', [{}])[0] if ss.get('devices') else {}
print('=== ComfyUI device view ===')
print(f'vram_free {dev.get("vram_free",0)/1e9:.1f} GB / vram_total {dev.get("vram_total",0)/1e9:.1f} GB')
print(f'ram_free {ss.get("system",{}).get("ram_free",0)/1e9:.1f} GB')
