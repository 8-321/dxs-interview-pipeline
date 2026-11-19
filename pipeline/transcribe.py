#!/usr/bin/env python3
"""第 1 步：采访原声转写，输出带时间戳的分段。

用法：
    python pipeline/transcribe.py --audio work/source.wav --out work/raw_segments.json

依赖：pip install faster-whisper
"""
import argparse
import json
import time
from pathlib import Path


def make_logger(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    def log(msg: str):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", default="work/source.wav")
    ap.add_argument("--out", default="work/raw_segments.json")
    ap.add_argument("--log", default=None, help="默认写到 <out>.log")
    ap.add_argument("--model", default="medium")
    ap.add_argument("--language", default="zh")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--prompt", default="以下是普通话采访对话，请输出简体中文。")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    log = make_logger(Path(args.log) if args.log else out.with_suffix(".log"))

    log(f"loading {args.model} int8 ...")
    model = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=args.threads)
    log("model loaded, start transcribe")

    segments, info = model.transcribe(
        args.audio,
        language=args.language,
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 350, "speech_pad_ms": 150},
        condition_on_previous_text=False,
        initial_prompt=args.prompt,
    )
    log(f"duration={info.duration:.1f}s lang={info.language} p={info.language_probability:.2f}")

    rows = []
    t0 = time.time()
    for i, s in enumerate(segments):
        rows.append({"id": i, "start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
        if i % 10 == 0:
            log(f"seg {i} @ {s.start:.1f}s elapsed={time.time() - t0:.0f}s :: {s.text.strip()[:40]}")
        if i % 50 == 0:
            json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log(f"done segments={len(rows)} elapsed={time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
