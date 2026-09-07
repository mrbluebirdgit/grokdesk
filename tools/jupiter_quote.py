#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, urllib.error, urllib.parse, urllib.request
from common import JUPITER_QUOTE, WSOL, emit, fail

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-mint", default=WSOL)
    parser.add_argument("--output-mint", required=True)
    parser.add_argument("--amount", required=True)
    parser.add_argument("--slippage-bps", type=int, default=100)
    parser.add_argument("--quote-url", default=JUPITER_QUOTE)
    args = parser.parse_args()
    qs = urllib.parse.urlencode({"inputMint": args.input_mint, "outputMint": args.output_mint, "amount": args.amount, "slippageBps": args.slippage_bps})
    url = f"{args.quote_url}?{qs}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        return fail(f"jupiter http {exc.code}: {exc.read().decode(errors='ignore')[:300]}", url=url)
    except urllib.error.URLError as exc:
        return fail(f"jupiter unreachable: {exc}", url=url)
    return emit({"ok": True, "url": url, "inputMint": data.get("inputMint"), "outputMint": data.get("outputMint"), "inAmount": data.get("inAmount"), "outAmount": data.get("outAmount"), "priceImpactPct": data.get("priceImpactPct"), "slippageBps": args.slippage_bps, "routePlanLen": len(data.get("routePlan") or []), "note": "Quote only. GrokDesk never calls /swap."})

if __name__ == "__main__":
    sys.exit(main())
