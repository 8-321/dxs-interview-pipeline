#!/usr/bin/env python3
"""第 6 步：在正片前后插入片名卡和片尾卡，得到分镜编译器的输入。

用法：
    python pipeline/finalize_timeline.py --in work/timeline_clips.json --out work/timeline.json
"""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="src", default="work/timeline_clips.json")
ap.add_argument("--out", default="work/timeline.json")
ap.add_argument("--title", type=float, default=3.6, help="片名卡时长（秒）")
ap.add_argument("--end", type=float, default=4.0, help="片尾卡时长（秒）")
args = ap.parse_args()

tl = json.load(open(args.src, encoding="utf-8"))
out = [{"id": "TITLE", "kind": "card", "dur": args.title}] + out + [
    {"id": "END", "kind": "card", "dur": args.end}
]
json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
total = sum(e["tout"] - e["tin"] if e.get("kind") == "clip" else e.get("dur", 0) for e in out)
print("timeline", len(out), "entries", "total", round(total, 2), "s")
