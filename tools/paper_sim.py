#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
from common import emit, ensure_desk, utc_now

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--desk")
    parser.add_argument("--action", required=True, choices=["buy", "sell"])
    parser.add_argument("--ticket", required=True)
    parser.add_argument("--mint", required=True)
    parser.add_argument("--size-usd", required=True)
    parser.add_argument("--price", required=True)
    parser.add_argument("--slippage-bps", type=int, default=100)
    parser.add_argument("--reason", default="")
    parser.add_argument("--note", default="")
    args = parser.parse_args()
    root = Path(args.desk).resolve() if args.desk else ensure_desk()
    journal = root / "journal"
    journal.mkdir(parents=True, exist_ok=True)
    day = utc_now()[:10]
    path = journal / f"paper-{day}.md"
    line = f"- {utc_now()} PAPER {args.action.upper()} ticket={args.ticket} mint={args.mint} size_usd={args.size_usd} price={args.price} slippage_bps={args.slippage_bps}\n"
    if not path.exists():
        path.write_text(f"# Paper journal {day}\n\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)
    return emit({"ok": True, "mode": "paper", "path": str(path), "ticket": args.ticket, "action": args.action, "mint": args.mint, "desk": str(root)})

if __name__ == "__main__":
    sys.exit(main())
