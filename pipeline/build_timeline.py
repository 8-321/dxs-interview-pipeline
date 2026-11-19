#!/usr/bin/env python3
"""第 5 步：按选段表生成 timeline_clips.json 和剪辑对照表。

选段表格式（JSON 数组）：
    [["u001", "hook", "字幕文字", 0, 0], ...]
字段：单元 id、所属段落、字幕、开头切掉秒数、结尾切掉秒数。

用法：
    python pipeline/build_timeline.py --units work/units.json --select work/select.json \
        --out work/timeline_clips.json --edit-map work/edit_map.json
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", default="work/units.json")
    ap.add_argument("--select", required=True)
    ap.add_argument("--out", default="work/timeline_clips.json")
    ap.add_argument("--edit-map", default="work/edit_map.json")
    ap.add_argument("--src", default="clips/source.mp4", help="写进 timeline 的素材相对路径")
    args = ap.parse_args()

    units = {u["id"]: u for u in json.load(open(args.units, encoding="utf-8"))}
    sel = json.load(open(args.select, encoding="utf-8"))

    tl, beats = [], {}
    for i, row in enumerate(sel, 1):
        if isinstance(row, dict):
            uid, beat, sub = row["unit"], row["beat"], row["sub"]
            tin_t, tout_t = row.get("tin", 0), row.get("tout", 0)
        else:
            uid, beat, sub, tin_t, tout_t = row
        u = units[uid]
        a = max(0.0, u["t0"] + tin_t - 0.05)
        b = u["t1"] - tout_t + 0.08
        if b <= a:
            raise SystemExit(f"{uid}: 裁剪后时长 <= 0，检查 tin/tout")
        cid = f"S{i:02d}"
        tl.append({"id": cid, "kind": "clip", "src": args.src,
                   "tin": round(a, 2), "tout": round(b, 2), "say": sub, "sub": sub})
        beats.setdefault(beat, {"ids": [], "t0": None, "t1": None})
        beats[beat]["ids"].append(cid)
        beats[beat]["t0"] = a if beats[beat]["t0"] is None else beats[beat]["t0"]
        beats[beat]["t1"] = b

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(tl, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    acc = 0.0
    for e in tl:
        e["_t0"] = round(acc, 2)
        acc += e["tout"] - e["tin"]
        e["_t1"] = round(acc, 2)
    json.dump({"clips": tl, "beats": beats, "total": round(acc, 2)},
              open(args.edit_map, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("clips", len(tl), "total", round(acc, 2), "s =", round(acc / 60, 2), "min")
    for b, v in beats.items():
        print(b, len(v["ids"]))


if __name__ == "__main__":
    main()
