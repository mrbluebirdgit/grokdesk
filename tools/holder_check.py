#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, sys
from common import emit, fail, rpc_call, rpc_url

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mint", required=True)
    parser.add_argument("--rpc")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--kill-pct", type=float, default=float(os.environ.get("TOP10_MAX_PCT") or 25.0))
    args = parser.parse_args()
    url = rpc_url(args.rpc)
    payload = rpc_call(url, "getTokenLargestAccounts", [args.mint])
    if payload.get("error"):
        return fail(str(payload["error"]), mint=args.mint, rpc=url)
    value = (payload.get("result") or {}).get("value") or []
    accounts = []
    total = 0.0
    for item in value[: args.limit]:
        amount = float(item.get("uiAmount") or 0)
        total += amount
        accounts.append({"address": item.get("address"), "uiAmount": amount, "decimals": item.get("decimals")})
    top10 = sum(a["uiAmount"] for a in accounts[:10])
    top10_share = (top10 / total * 100.0) if total else 0.0
    return emit({"ok": True, "mint": args.mint, "rpc": "helius" if "helius" in url else url, "accounts": accounts, "top10PctOfReturned": round(top10_share, 2), "killSignal": top10_share >= args.kill_pct})

if __name__ == "__main__":
    sys.exit(main())
