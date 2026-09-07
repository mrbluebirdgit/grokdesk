#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from common import DESK_CHILDREN, emit, ensure_desk, utc_now

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--desk")
    args = parser.parse_args()
    if args.desk:
        import os
        os.environ["GROKDESK"] = args.desk
    root = ensure_desk()
    return emit({"ok": True, "desk": str(root), "folders": [str(root / c) for c in DESK_CHILDREN], "desk_md": str(root / "desk.md"), "risk_limits": str(root / "risk-limits.md"), "engagement": "research", "created": utc_now()})

if __name__ == "__main__":
    sys.exit(main())
