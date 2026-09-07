#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from common import emit, utc_now

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="logs/trades.jsonl")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    path = Path(args.log)
    if not path.exists():
        return emit({"ok": True, "empty": True, "path": str(path), "note": "No pipeline log. Do not invent scores."})
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                rows.append({"ok": False, "error": "bad jsonl line"})
    print("PIPELINE-EVIDENCE")
    print("These scores are evidence only. Not RISK CLEAR. Not human approval.")
    return emit({"ok": True, "path": str(path), "count": len(rows), "tail": rows[-args.limit :]})

if __name__ == "__main__":
    sys.exit(main())
