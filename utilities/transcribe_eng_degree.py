# -*- coding: utf-8 -*-
"""Transcribe eng-degree script video with the OmniVoice app's faster-whisper
model (local snapshot, GPU float16). Usage (app venv python):
  .venv\Scripts\python.exe transcribe_eng_degree.py <wav> <out_txt>
"""
import sys
from faster_whisper import WhisperModel

SNAP = (r"C:\Users\user\AppData\Local\OmniVoice\hf_cache"
        r"\models--deepdml--faster-whisper-large-v3-turbo-ct2"
        r"\snapshots\4df90f75321148c3a29a9e2351b7ddf8f5b115a8")

wav, out_txt = sys.argv[1], sys.argv[2]
model = WhisperModel(SNAP, device="cuda", compute_type="float16")
segments, info = model.transcribe(wav, vad_filter=True)
lines = [f"[lang={info.language} prob={info.language_probability:.2f} dur={info.duration:.1f}]"]
for s in segments:
    lines.append(f"[{s.start:6.1f} - {s.end:6.1f}] {s.text.strip()}")
text = "\n".join(lines)
with open(out_txt, "w", encoding="utf-8") as f:
    f.write(text)
print(text)
