import struct, sys, os, glob

def mp4_dims(path):
    """Parse width/height from an mp4 file (tkhd box)."""
    with open(path, 'rb') as f:
        data = f.read()
    # search for 'tkhd'
    i = data.find(b'tkhd')
    if i == -1:
        return None
    # tkhd box: version(1) + flags(3) ... for v0: creation, modification, reserved, reserved, reserved(4), next_track_id(4), data(8), width(4), height(4)
    # The width/height are the last 8 bytes of the box payload (16.16 fixed point)
    # Find the box start (4 bytes before 'tkhd' is the size)
    box_start = i - 4
    size = struct.unpack('>I', data[box_start:box_start+4])[0]
    # payload after 'tkhd'(4) + version/flags(4)
    payload = data[i+4:i+4+size-4]
    version = payload[0]
    if version == 0:
        # creation_time(4) mod_time(4) track_id(4) reserved(4) duration(4) reserved(8) layer(2) alt(2) volume(2) reserved(2) matrix(36) width(4) height(4)
        w = struct.unpack('>I', payload[-8:-4])[0] >> 16
        h = struct.unpack('>I', payload[-4:])[0] >> 16
    else:
        # v1: creation(8) mod(8) track_id(4) reserved(4) duration(8) reserved(8) layer(2) alt(2) volume(2) reserved(2) matrix(36) width(4) height(4)
        w = struct.unpack('>I', payload[-8:-4])[0] >> 16
        h = struct.unpack('>I', payload[-4:])[0] >> 16
    return (w, h)

base = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\video'
files = [p for p in glob.glob(base + r'\Jaisal_Production_1_*.mp4')]
files.sort(key=os.path.getmtime, reverse=True)
for p in files[:5]:
    d = mp4_dims(p)
    print(os.path.basename(p), '->', d)
