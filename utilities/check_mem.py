from PIL import Image
import os, ctypes

INP = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input'
names = ['jaisal_1_longshot.png','jaisal_2_closeup.png','jaisal_3_running.png',
         'jaisal_4_middle.png','jaisal_5_jump.png','jaisal_6_underwater.png','jaisal_7_title.png']
print('=== Reference image dimensions ===')
for n in names:
    p = os.path.join(INP, n)
    if os.path.exists(p):
        print(f'{n}: {Image.open(p).size}')
    else:
        print(f'{n}: MISSING')

class M(ctypes.Structure):
    _fields_ = [('dwLength', ctypes.c_uint32), ('dwMemoryLoad', ctypes.c_uint32),
                ('ullTotalPhys', ctypes.c_uint64), ('ullAvailPhys', ctypes.c_uint64),
                ('ullTotalPage', ctypes.c_uint64), ('ullAvailPage', ctypes.c_uint64),
                ('ullTotalVirtual', ctypes.c_uint64), ('ullAvailVirtual', ctypes.c_uint64),
                ('ullAvailExtendedVirtual', ctypes.c_uint64)]
m = M()
m.dwLength = ctypes.sizeof(m)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
print('=== System RAM ===')
print('RAM total GB:', round(m.ullTotalPhys/1e9, 1))
print('RAM avail GB:', round(m.ullAvailPhys/1e9, 1))
print('RAM load %:', m.dwMemoryLoad)
