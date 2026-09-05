import importlib.util as u
mods = ['PIL', 'dora_search', 'dora', 'soundfile', 'librosa', 'laion_clap', 'open_clip',
        'nnAudio', 'torchdiffeq', 'torchlibrosa', 'julius', 'flashy', 'submitit',
        'treetable', 'retrying', 'num2words', 'spacy', 'colorlog']
res = {}
for m in mods:
    try:
        res[m] = 'OK' if u.find_spec(m) else 'MISSING'
    except Exception as e:
        res[m] = 'ERR:' + type(e).__name__
missing = [m for m, v in res.items() if v != 'OK']
print('RESULT:', res)
print('MISSING:', missing if missing else 'none')
