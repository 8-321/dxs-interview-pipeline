#!/usr/bin/env python3
"""第 3 步：按标点和停顿把分段合并成完整句子。

用法：
    python pipeline/make_sentences.py --in work/refined_segments.json --out work/sentences.json
"""
import argparse
import json
import re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default="work/refined_segments.json")
    ap.add_argument("--out", default="work/sentences.json")
    ap.add_argument("--pause", type=float, default=0.9, help="停顿超过多少秒就断句")
    args = ap.parse_args()

    rows = json.load(open(args.src, encoding="utf-8"))
    sentences = []
    buf, buf_start, buf_end = [], None, None

    def flush():
        nonlocal buf, buf_start, buf_end
        text = "".join(buf).strip()
        if text:
            sentences.append({"t0": round(buf_start, 2), "t1": round(buf_end, 2), "text": text})
        buf, buf_start, buf_end = [], None, None

    for r in rows:
        t = r["text"].strip()
        if not t:
            continue
        if buf_start is None:
            buf_start = r["start"]
        if buf and r["start"] - buf_end > args.pause:
            flush()
            buf_start = r["start"]
        buf.append(t)
        buf_end = r["end"]

        joined = "".join(buf)
        parts = re.split(r"(?<=[。！？!?])", joined)
        if len(parts) > 1:
            closed = [p for p in parts[:-1] if p.strip()]
            tail = parts[-1]
            n = len(joined)
            cursor = buf_start
            for p in closed:
                dur = (buf_end - buf_start) * len(p) / max(n, 1)
                sentences.append({"t0": round(cursor, 2), "t1": round(cursor + dur, 2), "text": p.strip()})
                cursor += dur
            buf = [tail] if tail.strip() else []
            buf_start = cursor if buf else None
    flush()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(sentences, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("sentences", len(sentences), "chars", sum(len(s["text"]) for s in sentences))


if __name__ == "__main__":
    main()
