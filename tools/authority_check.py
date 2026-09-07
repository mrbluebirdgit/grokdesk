#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from common import emit, fail, rpc_call, rpc_url

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mint", required=True)
    parser.add_argument("--rpc")
    args = parser.parse_args()
    url = rpc_url(args.rpc)
    payload = rpc_call(url, "getAccountInfo", [args.mint, {"encoding": "jsonParsed"}])
    if payload.get("error"):
        return fail(str(payload["error"]), mint=args.mint, rpc=url)
    value = (payload.get("result") or {}).get("value")
    if not value:
        return fail("mint account not found", mint=args.mint)
    info = ((value.get("data") or {}).get("parsed") or {}).get("info") or {}
    mint_auth = info.get("mintAuthority")
    freeze_auth = info.get("freezeAuthority")
    return emit({"ok": True, "mint": args.mint, "rpc": "helius" if "helius" in url else url, "hasMintAuthority": bool(mint_auth), "hasFreezeAuthority": bool(freeze_auth), "mintAuthority": mint_auth, "freezeAuthority": freeze_auth, "supply": info.get("supply"), "decimals": info.get("decimals"), "extensions": info.get("extensions") or [], "killSignal": bool(mint_auth) or bool(freeze_auth)})

if __name__ == "__main__":
    sys.exit(main())
