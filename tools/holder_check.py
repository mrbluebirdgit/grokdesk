#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, urllib.error, urllib.request
from common import emit, fail, rpc_url

def rpc_call(url, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        return {"error": {"message": str(exc)}}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mint", required=True)
    parser.add_argument("--rpc")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--kill-pct", type=float, default=25.0)
    args = parser.parse_args()
    url = rpc_url(args.rpc)
    payload = rpc_call(url, "getTokenLargestAccounts", [args.mint])
    if payload.get("error"):
        return fail(str(payload["error"]), mint=args.mint)
    value = (payload.get("result") or {}).get("value") or []
    accounts = []
    total = 0.0
    for item in value[: args.limit]:
        amount = float(item.get("uiAmount") or 0)
        total += amount
        accounts.append({"address": item.get("address"), "uiAmount": amount, "decimals": item.get("decimals")})
    top10 = sum(a["uiAmount"] for a in accounts[:10])
    top10_share = (top10 / total * 100.0) if total else 0.0
    return emit({"ok": True, "mint": args.mint, "rpc": url, "accounts": accounts, "top10PctOfReturned": round(top10_share, 2), "killSignal": top10_share >= args.kill_pct})

if __name__ == "__main__":
    sys.exit(main())
