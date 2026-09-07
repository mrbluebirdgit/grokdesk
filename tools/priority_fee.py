#!/usr/bin/env python3
from __future__ import annotations
import argparse, statistics, sys
from common import emit, fail, rpc_call, rpc_url

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rpc")
    parser.add_argument("--percentile", type=float, default=75)
    parser.add_argument("--multiplier", type=float, default=1.2)
    args = parser.parse_args()
    url = rpc_url(args.rpc)
    payload = rpc_call(url, "getRecentPrioritizationFees", [[]])
    if payload.get("error"):
        return fail(str(payload["error"]), rpc=url)
    fees = [int(x.get("prioritizationFee") or 0) for x in (payload.get("result") or [])]
    if not fees:
        return emit({"ok": True, "rpc": "helius" if "helius" in url else url, "suggestedMicroLamports": 0, "sample": 0})
    fees.sort()
    idx = min(len(fees) - 1, max(0, int(round((args.percentile / 100.0) * (len(fees) - 1)))))
    base = fees[idx]
    return emit({"ok": True, "rpc": "helius" if "helius" in url else url, "sample": len(fees), "median": int(statistics.median(fees)), "suggestedMicroLamports": int(base * args.multiplier)})

if __name__ == "__main__":
    sys.exit(main())
