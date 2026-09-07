#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, statistics, sys, urllib.error, urllib.request
from common import emit, fail, rpc_url

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rpc")
    parser.add_argument("--percentile", type=float, default=75)
    parser.add_argument("--multiplier", type=float, default=1.2)
    args = parser.parse_args()
    url = rpc_url(args.rpc)
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getRecentPrioritizationFees", "params": [[]]}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        return fail(f"rpc unreachable: {exc}", rpc=url)
    fees = [int(x.get("prioritizationFee") or 0) for x in (payload.get("result") or [])]
    if not fees:
        return emit({"ok": True, "rpc": url, "suggestedMicroLamports": 0, "sample": 0})
    fees.sort()
    idx = min(len(fees) - 1, max(0, int(round((args.percentile / 100.0) * (len(fees) - 1)))))
    base = fees[idx]
    return emit({"ok": True, "rpc": url, "sample": len(fees), "median": int(statistics.median(fees)), "suggestedMicroLamports": int(base * args.multiplier)})

if __name__ == "__main__":
    sys.exit(main())
