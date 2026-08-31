import struct, os

def mp4_info(path):
    with open(path, 'rb') as f:
        data = f.read()
    info = {}
    # frame count from stsz (sample size) box
    i = data.find(b'stsz')
    if i != -1:
        box_start = i - 4
        size = struct.unpack('>I', data[box_start:box_start+4])[0]
        payload = data[i+4:i+4+size-4]
        # stsz: version/flags(4) + sample_size(4) + sample_count(4)
        sample_count = struct.unpack('>I', payload[8:12])[0]
        info['frame_count'] = sample_count
    # duration from mvhd
    i = data.find(b'mvhd')
    if i != -1:
        payload = data[i+4:]
        version = payload[0]
        if version == 0:
            timescale = struct.unpack('>I', payload[12:16])[0]
            duration = struct.unpack('>I', payload[16:20])[0]
        else:
            timescale = struct.unpack('>I', payload[20:24])[0]
            duration = struct.unpack('>Q', payload[24:32])[0]
        info['duration_s'] = round(duration / timescale, 2)
        info['fps'] = round(info.get('frame_count', 0) / (duration/timescale), 2) if duration else None
    # resolution from tkhd
    i = data.find(b'tkhd')
    if i != -1:
        box_start = i - 4
        size = struct.unpack('>I', data[box_start:box_start+4])[0]
        payload = data[i+4:i+4+size-4]
        w = struct.unpack('>I', payload[-8:-4])[0] >> 16
        h = struct.unpack('>I', payload[-4:])[0] >> 16
        info['width'] = w
        info['height'] = h
    return info

for name in ['jaisal_prod1_ref.mp4']:
    p = os.path.join(r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input', name)
    print(name, '->', mp4_info(p))
