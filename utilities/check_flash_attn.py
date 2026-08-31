import torch

print('torch:', torch.__version__)
print('cuda available:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('device:', torch.cuda.get_device_name(0))
    print('capability:', torch.cuda.get_device_capability(0))
    # Flash attention availability
    try:
        print('flash_attention available:', torch.backends.cuda.flash_attention)
    except Exception as e:
        print('flash_attention attr error:', e)
    try:
        print('cudnn_sdp available:', torch.backends.cuda.cudnn_sdp_enabled())
    except Exception as e:
        print('cudnn_sdp error:', e)
    try:
        print('mem_efficient available:', torch.backends.cuda.mem_efficient_sdp_enabled())
    except Exception as e:
        print('mem_efficient error:', e)
    # Probe flash attention with a small tensor
    try:
        q = torch.randn(1, 16, 64, device='cuda', dtype=torch.float16)
        print('can_use_flash_attention:', torch.backends.cuda.can_use_flash_attention(q, q, q, None, 0.0, False))
    except Exception as e:
        print('can_use_flash_attention error:', e)
    # Check sageattention
    try:
        import sageattention
        print('sageattention installed:', sageattention.__version__ if hasattr(sageattention,'__version__') else 'yes')
    except Exception as e:
        print('sageattention NOT installed:', e)
    # Check xformers
    try:
        import xformers
        print('xformers installed:', xformers.__version__)
    except Exception as e:
        print('xformers NOT installed')
