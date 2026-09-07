#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, sys, urllib.parse
from common import WSOL, emit, fail, http_json, jupiter_quote_url

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-mint", default=WSOL)
    parser.add_argument("--output-mint", required=True)
    parser.add_argument("--amount", required=True)
    parser.add_argument("--slippage-bps", type=int, default=int(os.environ.get("MAX_SLIPPAGE_BPS") or 100))
    parser.add_argument("--quote-url")
    args = parser.parse_args()
    base = args.quote_url or jupiter_quote_url()
    qs = urllib.parse.urlencode({"inputMint": args.input_mint, "outputMint": args.output_mint, "amount": args.amount, "slippageBps": args.slippage_bps})
    url = f"{base}?{qs}"
    headers = {}
    key = os.environ.get("JUPITER_API_KEY")
    if key:
        headers["x-api-key"] = key
    result = http_json(url, headers=headers)
    if not result.get("ok"):
        return fail(result.get("error") or "jupiter quote failed", url=url, body=result.get("body"), keyed=bool(key))
    data = result.get("data") or {}
    return emit({"ok": True, "url": url, "keyed": bool(key), "inputMint": data.get("inputMint"), "outputMint": data.get("outputMint"), "inAmount": data.get("inAmount"), "outAmount": data.get("outAmount"), "priceImpactPct": data.get("priceImpactPct"), "slippageBps": args.slippage_bps, "routePlanLen": len(data.get("routePlan") or []), "note": "Quote only. GrokDesk never calls /swap."})

if __name__ == "__main__":
    sys.exit(main())
