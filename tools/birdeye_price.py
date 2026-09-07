#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, sys, urllib.parse
from common import BIRDEYE_PRICE, emit, fail, http_json

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mint", required=True)
    args = parser.parse_args()
    key = os.environ.get("BIRDEYE_API_KEY")
    if not key:
        return fail("BIRDEYE_API_KEY missing")
    url = f"{BIRDEYE_PRICE}?{urllib.parse.urlencode({'address': args.mint})}"
    result = http_json(url, headers={"X-API-KEY": key, "x-chain": "solana"})
    if not result.get("ok"):
        return fail(result.get("error") or "birdeye failed", mint=args.mint, body=result.get("body"))
    return emit({"ok": True, "mint": args.mint, "source": url, "data": result.get("data")})

if __name__ == "__main__":
    sys.exit(main())
