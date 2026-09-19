#!/usr/bin/env python3
"""daily/YYYY-MM-DD.json の形式チェック。使い方: python3 tools/validate_daily.py daily/2026-09-19.json
- 正解は必ず ch[0]（アプリ側で選択肢をシャッフルする）
- p5: 12問（4択・空所は ___）/ p2: 8問（3択）/ p3: 会話2つ（計4問・4択）/ p7: 長文2つ（計6問・4択）
- 過去の daily/*.json と問題文が重複していないこと
"""
import json, sys, glob, os, re

def err(msgs, m): msgs.append(m)

def check_q(msgs, tag, x, n):
    for k in ("q", "ch", "exp"):
        if k not in x: err(msgs, f"{tag}: '{k}' がない"); return
    if not isinstance(x["ch"], list) or len(x["ch"]) != n: err(msgs, f"{tag}: 選択肢は{n}個")
    elif len(set(x["ch"])) != n: err(msgs, f"{tag}: 選択肢が重複している")
    if not x["q"].strip() or not x["exp"].strip(): err(msgs, f"{tag}: q/exp が空")

def validate(path):
    msgs = []
    d = json.load(open(path, encoding="utf-8"))
    date = os.path.basename(path)[:-5]
    if d.get("date") != date: err(msgs, f"date が {date} と一致しない")
    if not d.get("theme"): err(msgs, "theme がない")
    p5, p2, p3, p7 = d.get("p5", []), d.get("p2", []), d.get("p3", []), d.get("p7", [])
    if len(p5) != 12: err(msgs, f"p5 は12問（現在{len(p5)}）")
    if len(p2) != 8: err(msgs, f"p2 は8問（現在{len(p2)}）")
    for i, x in enumerate(p5):
        check_q(msgs, f"p5[{i}]", x, 4)
        if "___" not in x.get("q", ""): err(msgs, f"p5[{i}]: 空所 ___ がない")
    for i, x in enumerate(p2): check_q(msgs, f"p2[{i}]", x, 3)
    if len(p3) != 2: err(msgs, f"p3 は会話2つ（現在{len(p3)}）")
    q3 = 0
    for i, c in enumerate(p3):
        sc = c.get("script", [])
        if len(sc) < 4 or any(l.get("w") not in ("M", "W") or not l.get("t") for l in sc): err(msgs, f"p3[{i}]: script は4行以上・各行 w(M/W) と t が必要")
        qs = c.get("qs", []); q3 += len(qs)
        if len(qs) != 2: err(msgs, f"p3[{i}]: 設問は2問")
        for j, x in enumerate(qs): check_q(msgs, f"p3[{i}].qs[{j}]", x, 4)
    q7 = 0
    for i, c in enumerate(p7):
        if len(c.get("passage", "")) < 200: err(msgs, f"p7[{i}]: passage が短い（200字以上）")
        qs = c.get("qs", []); q7 += len(qs)
        if len(qs) != 3: err(msgs, f"p7[{i}]: 設問は3問")
        for j, x in enumerate(qs): check_q(msgs, f"p7[{i}].qs[{j}]", x, 4)
    if len(p7) != 2: err(msgs, f"p7 は長文2つ（現在{len(p7)}）")
    # 過去分との重複
    mine = set(x["q"] for x in p5 + p2) | set(x["q"] for c in p3 for x in c.get("qs", [])) | set(c.get("passage", "")[:60] for c in p7)
    for f in glob.glob("daily/2*.json"):
        if os.path.abspath(f) == os.path.abspath(path): continue
        o = json.load(open(f, encoding="utf-8"))
        prev = set(x["q"] for x in o.get("p5", []) + o.get("p2", [])) | set(x["q"] for c in o.get("p3", []) for x in c.get("qs", [])) | set(c.get("passage", "")[:60] for c in o.get("p7", []))
        dup = mine & prev
        if dup: err(msgs, f"{f} と重複: {sorted(dup)[:2]}")
    return msgs

if __name__ == "__main__":
    bad = False
    for p in sys.argv[1:]:
        m = validate(p)
        print(("NG " if m else "OK ") + p)
        for x in m: print("  -", x)
        bad = bad or bool(m)
    sys.exit(1 if bad else 0)
