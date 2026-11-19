#!/usr/bin/env python3
"""把转写分段导成可读文本，方便快速通读。

用法：
    python pipeline/dump_segments.py --in work/refined_segments.json --out work/segments.txt
"""
import argparse
import json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="src", default="work/raw_segments.json")
ap.add_argument("--out", default="work/segments.txt")
args = ap.parse_args()

rows = json.load(open(args.src, encoding="utf-8"))
Path(args.out).parent.mkdir(parents=True, exist_ok=True)
with open(args.out, "w", encoding="utf-8", newline="\n") as f:
    for i, r in enumerate(rows):
        f.write(f"s{i + 1:03d} {r['start']:7.2f}-{r['end']:7.2f} {r['text']}\n")
print("ok", len(rows))
