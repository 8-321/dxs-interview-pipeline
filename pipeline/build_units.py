#!/usr/bin/env python3
"""第 4 步：切成 14-26 字的口播单元，供人工挑选。

用法：
    python pipeline/build_units.py --in work/refined_segments.json \
        --out work/units.json --txt work/units.txt
"""
import argparse
import json
import re
from pathlib import Path


def clean(t: str) -> str:
    return re.sub(r"\s+", "", t).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default="work/refined_segments.json")
    ap.add_argument("--out", default="work/units.json")
    ap.add_argument("--txt", default="work/units.txt")
    ap.add_argument("--max", type=int, default=26)
    ap.add_argument("--min-chars", type=int, default=14)
    ap.add_argument("--min-dur", type=float, default=2.2)
    args = ap.parse_args()

    rows = json.load(open(args.src, encoding="utf-8"))
    rows.sort(key=lambda r: r["start"])

    parts = []
    for r in rows:
        t = clean(r["text"])
        if not t:
            continue
        if len(t) <= args.max:
            parts.append({"t0": r["start"], "t1": r["end"], "text": t})
            continue
        chunks, s = [], t
        while len(s) > args.max:
            cut = -1
            for i in range(args.max, 8, -1):
                if s[i - 1] in ",，。!?！？;；":
                    cut = i
                    break
            if cut < 0:
                cut = args.max
            chunks.append(s[:cut])
            s = s[cut:]
        if s:
            chunks.append(s)
        total, pos = len(t), 0
        for c in chunks:
            a = r["start"] + (r["end"] - r["start"]) * pos / total
            pos += len(c)
            b = r["start"] + (r["end"] - r["start"]) * pos / total
            parts.append({"t0": round(a, 2), "t1": round(b, 2), "text": c})

    units, buf, st, en, chars = [], [], None, None, 0
    for p in parts:
        if st is None:
            st = p["t0"]
        if chars + len(p["text"]) > args.max and buf:
            units.append({"t0": round(st, 2), "t1": round(en, 2), "text": "".join(buf)})
            buf, chars, st = [], 0, p["t0"]
        buf.append(p["text"])
        chars += len(p["text"])
        en = p["t1"]
        if chars >= args.min_chars and en - st >= args.min_dur:
            units.append({"t0": round(st, 2), "t1": round(en, 2), "text": "".join(buf)})
            buf, chars, st, en = [], 0, None, None
    if buf:
        units.append({"t0": round(st, 2), "t1": round(en, 2), "text": "".join(buf)})

    for i, u in enumerate(units):
        u["id"] = f"u{i + 1:03d}"
        u["chars"] = len(u["text"])

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(units, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(args.txt, "w", encoding="utf-8", newline="\n") as f:
        for u in units:
            f.write(f"{u['id']} {u['t0']:7.2f}-{u['t1']:7.2f} ({u['chars']:2d}) {u['text']}\n")
    print("units", len(units), "chars", sum(u["chars"] for u in units),
          "max", max((u["chars"] for u in units), default=0))


if __name__ == "__main__":
    main()
