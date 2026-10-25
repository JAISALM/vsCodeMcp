import struct

p = r"D:\models\Gemma\mtp-gemma-4-31B-it.gguf"
with open(p, "rb") as f:
    buf = f.read(512)

print("offset  hex (16 bytes per row)")
for row in range(0, 512, 16):
    chunk = buf[row:row+16]
    hexs = " ".join(f"{b:02x}" for b in chunk)
    asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    print(f"{row:4d}  {hexs:<48s}  {asc}")
