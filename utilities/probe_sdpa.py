import torch, time

dev = 'cuda'
torch.cuda.init()
print('device:', torch.cuda.get_device_name(0), 'capability:', torch.cuda.get_device_capability(0))

# Realistic video attention shape: batch=1, heads=12, seq=1024 (video latent frames x spatial), dim=128
# MiniMax H3 video: latent is large; use a representative shape
shapes = [
    ('small  (1,12,512,128)',  (1, 12, 512, 128)),
    ('video (1,12,1024,128)', (1, 12, 1024, 128)),
    ('big   (1,12,2048,128)', (1, 12, 2048, 128)),
]

def bench(shape, dtype, iters=3):
    b,h,s,d = shape
    q = torch.randn(b,h,s,d, device=dev, dtype=dtype)
    k = torch.randn(b,h,s,d, device=dev, dtype=dtype)
    v = torch.randn(b,h,s,d, device=dev, dtype=dtype)
    # warmup
    for _ in range(1):
        out = torch.nn.functional.scaled_dot_product_attention(q,k,v)
    torch.cuda.synchronize()
    t0 = time.time()
    for _ in range(iters):
        out = torch.nn.functional.scaled_dot_product_attention(q,k,v)
    torch.cuda.synchronize()
    dt = (time.time()-t0)/iters
    return dt

for name, shape in shapes:
    for dtype in (torch.float16, torch.bfloat16):
        try:
            dt = bench(shape, dtype)
            print(f'{name} {str(dtype):20s} -> {dt*1000:.1f} ms/iter')
        except Exception as e:
            print(f'{name} {str(dtype):20s} -> ERROR {e}')

# Which backend does torch pick? Use the SDPAParams probe
from torch.nn.attention import SDPBackend
print()
print('=== backend availability for video shape (1,12,1024,128) fp16 ===')
q = torch.randn(1,12,1024,128, device=dev, dtype=torch.float16)
params = torch.backends.cuda.SDPAParams(q, q, q, None, 0.0, False, True)
for name, fn in [('flash', torch.backends.cuda.can_use_flash_attention),
                 ('cudnn', torch.backends.cuda.can_use_cudnn_attention),
                 ('efficient', torch.backends.cuda.can_use_efficient_attention)]:
    try:
        print(f'  {name}:', fn(params))
    except Exception as e:
        print(f'  {name}: ERROR {e}')
