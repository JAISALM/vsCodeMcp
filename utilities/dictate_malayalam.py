#!/usr/bin/env python
"""LIVE read-aloud dictation -> Malayalam text types itself into the active window.

The alternative to the batch Whisper flow (transcribe_malayalam.py) for WRITING:
you just KEEP SPEAKING (read the scene out loud, in Malayalam), and every
pause in your speech transcribes the sentence and types it into whatever
window is in front of you (Notepad / VS Code / browser). Everything is also
appended to a log file, so the spoken take doubles as a recording.

100% local: mic -> faster-whisper large-v3 (GPU, RTX 5090) -> Unicode typing
via SendInput. No cloud, no keys.

USAGE
-----
  # quick visible test (opens Notepad, types a Malayalam test line, done):
  python dictate_malayalam.py --test

  # AUTO mode (no button): just start speaking; pauses end sentences.
  python dictate_malayalam.py

  # PTT mode (BUTTON — hold F9 = record, release = transcribe+type):
  python dictate_malayalam.py --ptt

  ...switch to your editor first. Esc (anywhere) stops the session.

OPTIONS
-------
  --ptt           push-to-talk: hold F9 to record, release to capture.
                  (Default = AUTO mode: the tool arms itself on your voice.)
  --device N      input device index (default: auto-pick "Microphone (Realtek")
  --threshold X   voice RMS trigger, 0.005 (sensitive) .. 0.03 (strict); default 0.012
  --silence S     seconds of silence that end a sentence; default 0.9
  --lang CODE     whisper language OUTCOME. DEFAULT = "en": you SPEAK Malayalam
                  (or mixed), the transcript LANDS IN ENGLISH — by user choice
                  (English is Gemma-friendly; the LLM pass converts to
                  Malayalam). "ml" = Malayalam script instead. "" = auto
                  (avoid: misfires to Tamil/Devanagari for Malayalam speech).
  --log PATH      log file (default D:\\models\\vsCodeMcp\\data\\dictation_log.txt)
  --test          type a test string into a fresh Notepad window and exit.

WORKFLOW (screenplay, D121)
---------------------------
  1. Read the scene out loud in Malayalam (or dictate new lines as they come).
  2. The Malayalam script types itself into your editor — you watch it land.
  3. When a scene is done, run the bilingual pass:
     prompts\\screenplay_bilingual_malayalam_english.txt (Malayalam + English
     for every line, character names consistent).
  4. Then your Gemma 31b QAT pass for suggestions/improvements.
  Typing route (fast fingers): type Manglish in Notepad (or use the Google
  Input Tools desktop IME for Malayalam script), then the same bilingual pass
  converts Manglish -> Malayalam + keeps English.
"""
import argparse
import ctypes
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import sounddevice as sd

RATE = 16000
LOG_DEFAULT = r"D:\models\vsCodeMcp\data\dictation_log.txt"


# ---------------------------------------------------------------------- typing
def _input_event():
    # KEYBDINPUT struct for SendInput (64-bit)
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [
            ("wVk", ctypes.c_ushort),
            ("wScan", ctypes.c_ushort),
            ("dwFlags", ctypes.c_ulong),
            ("time", ctypes.c_ulong),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        ]

    class INPUT(ctypes.Structure):
        _fields_ = [
            ("type", ctypes.c_ulong),
            ("ki", KEYBDINPUT),
        ]

    return INPUT, KEYBDINPUT


_INPUT, _KEYBD = _input_event()
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004


def type_unicode(text: str):
    """Type `text` into the FOREGROUND window via SendInput (any Unicode)."""
    for ch in text:
        code = ord(ch)
        for flags in (0, KEYEVENTF_KEYUP):
            inp = _INPUT(type=0, ki=_KEYBD(wVk=0, wScan=code, dwFlags=KEYEVENTF_UNICODE | flags,
                                            time=0, dwExtraInfo=ctypes.pointer(ctypes.c_ulong(0))))
            ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(_INPUT))
        time.sleep(0.004)  # keep the foreground app from dropping chars


# ----------------------------------------------------------------------- mic
def pick_device():
    try:
        idx = next(i for i, d in enumerate(sd.query_devices())
                   if d["max_input_channels"] > 0 and "Realtek" in d["name"] and "Microphone" in d["name"])
        return idx
    except StopIteration:
        return None  # sounddevice default


def rms_block(block: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(block, dtype=np.float32))))


# --------------------------------------------------------------------- main
def run(args):
    from faster_whisper import WhisperModel
    from pynput import keyboard

    device, compute = "cuda", "float16"
    try:
        import torch
        if not torch.cuda.is_available():
            device, compute = "cpu", "int8"
    except ImportError:
        device, compute = "cpu", "int8"
    print(f"Loading whisper large-v3 on {device}/{compute} (first run downloads ~1.5 GB)...")
    model = WhisperModel("large-v3", device=device, compute_type=compute)
    print("Model ready.")

    dev_idx = args.device if args.device is not None else pick_device()
    dev_name = sd.query_devices(dev_idx)["name"] if dev_idx is not None else "default"
    print(f"Mic: [{dev_idx}] {dev_name}")
    if args.ptt:
        print("PTT MODE: hold F9 = record, release F9 = capture. Esc stops. Log:", args.log)
    else:
        print("AUTO MODE: just start speaking; a pause ends the sentence. Esc stops. Log:", args.log)

    logf = open(args.log, "a", encoding="utf-8")
    buf = []           # queued float32 samples
    armed = True       # waiting for voice? (auto mode only)
    recording = {"on": False}  # F9 held (ptt mode)
    voiced_frames = 0
    SILENCE_FRAMES = int(args.silence * RATE / 300)  # 30 ms frames
    stop = {"done": False}

    def transcribe_now(samples: np.ndarray):
        if len(samples) > int(RATE * 0.8):  # > 0.8 s — short fragments hallucinate
            transcribe_and_type(samples)

    def on_press(key):
        if key == keyboard.Key.esc:
            stop["done"] = True
        elif args.ptt and key == keyboard.Key.f9:
            if not recording["on"]:
                buf.clear()
                recording["on"] = True
                print(">> F9: recording...")

    def on_release(key):
        if args.ptt and key == keyboard.Key.f9 and recording["on"]:
            recording["on"] = False
            samples = np.concatenate(buf) if buf else np.zeros(1600, dtype=np.float32)
            buf.clear()
            print(">> F9: released, transcribing...")
            transcribe_now(samples)

    listener = keyboard.Listener(on_press=on_press,
                                 on_release=on_release if args.ptt else None)
    listener.start()

    def transcribe_and_type(samples: np.ndarray):
        t0 = time.time()
        audio = np.asarray(samples, dtype=np.float32)
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        if peak < 1e-4:
            print(">> silence only — skipped")
            return
        audio = audio / max(1e-6, peak)
        # Tuned 2026-10-12 for colloquial code-switched Keralite speech:
        # beam_size=5 (vs greedy 1 — much better word choice),
        # vad_filter=True (chops silence/noise — kills most hallucinations),
        # condition_on_previous_text=False (no hallucination chaining).
        # language: DEFAULT "en" — user wants the English transcript of
        # their Malayalam speech (Gemma-friendly; LLM pass converts to
        # Malayalam). Auto-detect misfires to Tamil/Devanagari; "ml" =
        # Malayalam script if ever wanted.
        kw = dict(beam_size=5, vad_filter=True, without_timestamps=True,
                  condition_on_previous_text=False)
        if args.lang:
            kw["language"] = args.lang
        segments, _ = model.transcribe(audio, **kw)
        text = " ".join(s.text.strip() for s in segments).strip()
        dt = time.time() - t0
        if text:
            print(f"[{time.strftime('%H:%M:%S')}] typed in {dt:.1f}s: {text}")
            logf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")
            logf.flush()
            type_unicode(text)

    with sd.RawInputStream(samplerate=RATE, channels=1, dtype="float32",
                           device=dev_idx, blocksize=480) as stream:
        if args.ptt:
            print(">> PTT READY — hold F9 to talk, release to capture (Esc to stop) <<")
        else:
            print(">> LISTENING — speak now (Esc to stop) <<")
        while not stop["done"]:
            raw, overflowed = stream.read(480)  # cffi buffer of float32 bytes
            block = np.frombuffer(raw, dtype=np.float32).copy()  # shape (480,)
            if args.ptt:
                # BUTTON mode: only buffer while F9 is held (30 s auto-flush cap)
                if recording["on"]:
                    buf.append(block)
                    if len(buf) * 480 / RATE > 30:
                        recording["on"] = False
                        samples = np.concatenate(buf)
                        buf.clear()
                        print(">> 30s cap hit, transcribing...")
                        transcribe_now(samples)
            else:
                # AUTO mode: voice RMS arms the capture, silence ends it
                buf.append(block)
                r = rms_block(block)
                if armed:
                    if r > args.threshold:
                        armed = False
                        voiced_frames = 0
                        buf = buf[-3:]  # keep a little lead-in
                    # else: discard idle buffer
                    if len(buf) > 40:
                        buf = buf[-40:]
                else:
                    voiced_frames = 0 if r < args.threshold else voiced_frames + 1
                    if voiced_frames >= SILENCE_FRAMES or len(buf) * 480 / RATE > 25:
                        # sentence complete -> transcribe
                        samples = np.concatenate(buf) if buf else np.zeros(1600, dtype=np.float32)
                        armed = True
                        buf = []
                        if len(samples) > int(RATE * 0.8):  # > 0.8 s — short fragments hallucinate
                            transcribe_and_type(samples)

    listener.stop()
    logf.close()
    print("Session ended. Esc-out logged to:", args.log)


def test_mode():
    print("Opening Notepad and typing a test line...")
    notepad = subprocess.Popen(["notepad"])
    time.sleep(2.0)
    type_unicode("\n\nDictation test — namaste in Malayalam script:\n")
    time.sleep(0.3)
    type_unicode("നമസ്തേ — dictation is working, Malayalam types itself.")
    print("Done. Check the Notepad window. (Notepad left open for you to verify.)")


def main():
    p = argparse.ArgumentParser(description="Live Malayalam dictation (local Whisper, read-aloud).")
    p.add_argument("--device", type=int, default=None, help="input device index (default: auto Realtek mic)")
    p.add_argument("--threshold", type=float, default=0.012, help="RMS voice trigger (default 0.012)")
    p.add_argument("--silence", type=float, default=0.9, help="silence seconds that end a sentence (default 0.9)")
    p.add_argument("--lang", default="en", help="whisper LANGUAGE OUTCOME; DEFAULT 'en' = ENGLISH "
                    "TRANSCRIPT of your Malayalam speech (user choice 2026-10-12: English transcript "
                    "is fine — LLM pass converts to Malayalam, and English feeds Gemma best). "
                    "Use 'ml' for Malayalam script, '' for auto (auto misfires to Tamil/Devanagari).")
    p.add_argument("--log", default=LOG_DEFAULT)
    p.add_argument("--ptt", action="store_true", help="push-to-talk: hold F9 = record, release = capture")
    p.add_argument("--test", action="store_true", help="type a test string into a fresh Notepad window")
    args = p.parse_args()
    if args.test:
        test_mode()
    else:
        run(args)


if __name__ == "__main__":
    main()
