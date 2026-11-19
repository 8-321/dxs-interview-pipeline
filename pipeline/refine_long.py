#!/usr/bin/env python3
"""第 2 步：把超过 MAX 秒的长段切出来重新转写，减少丢句。

用法：
    python pipeline/refine_long.py --audio work/source.wav \
        --segments work/raw_segments.json --out work/refined_segments.json
"""
import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", default="work/source.wav")
    ap.add_argument("--segments", default="work/raw_segments.json")
    ap.add_argument("--out", default="work/refined_segments.json")
    ap.add_argument("--model", default="medium")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--max", type=float, default=12.0, help="超过多少秒就重切")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    rows = json.load(open(args.segments, encoding="utf-8"))
    model = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=args.threads)

    out = []
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = os.path.join(tmpdir, "slice.wav")
        for r in rows:
            dur = r["end"] - r["start"]
            if dur <= args.max:
                out.append(r)
                continue
            print("refine", r["start"], r["end"], flush=True)
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-ss", str(r["start"]), "-t", str(dur),
                 "-i", args.audio, "-ac", "1", "-ar", "16000", tmp],
                check=True,
            )
            segs, _ = model.transcribe(
                tmp, language="zh", beam_size=5, vad_filter=True,
                vad_parameters={"min_silence_duration_ms": 120, "speech_pad_ms": 80},
                condition_on_previous_text=False,
            )
            for s in segs:
                out.append({"start": round(r["start"] + s.start, 2),
                            "end": round(r["start"] + s.end, 2),
                            "text": s.text.strip()})

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("total", len(out))


if __name__ == "__main__":
    main()
