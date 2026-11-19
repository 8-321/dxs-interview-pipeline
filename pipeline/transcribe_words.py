#!/usr/bin/env python3
"""可选：带词级时间戳的转写，用来给字幕做逐词高亮。

用法：
    python pipeline/transcribe_words.py --audio work/source.wav --out work/words.json
"""
import argparse
import json
import time
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--audio", default="work/source.wav")
ap.add_argument("--out", default="work/words.json")
ap.add_argument("--model", default="medium")
ap.add_argument("--threads", type=int, default=8)
args = ap.parse_args()

from faster_whisper import WhisperModel

m = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=args.threads)
segs, info = m.transcribe(
    args.audio, language="zh", beam_size=5, vad_filter=True,
    vad_parameters={"min_silence_duration_ms": 350, "speech_pad_ms": 150},
    condition_on_previous_text=False, word_timestamps=True,
    initial_prompt="以下是普通话采访对话，请输出简体中文。",
)

rows = []
t0 = time.time()
for i, s in enumerate(segs):
    for wd in (s.words or []):
        rows.append({"start": round(wd.start, 3), "end": round(wd.end, 3), "word": wd.word})
    if i % 40 == 0:
        print(f"seg {i} @ {s.start:.1f}s words={len(rows)} elapsed={time.time() - t0:.0f}s", flush=True)

Path(args.out).parent.mkdir(parents=True, exist_ok=True)
json.dump(rows, open(args.out, "w", encoding="utf-8"), ensure_ascii=False)
print("done words=", len(rows))
