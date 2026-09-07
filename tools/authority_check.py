#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, urllib.error, urllib.request
from common import emit, fail, rpc_url

def rpc_call(url, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        return {"ok": False, "error": f"rpc unreachable: {exc}"}
    if payload.get("error"):
        return {"ok": False, "error": payload["error"]}
    return {"ok": True, "result": payload.get("result")}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mint", required=True)
    parser.add_argument("--rpc")
    args = parser.parse_args()
    url = rpc_url(args.rpc)
    raw = rpc_call(url, "getAccountInfo", [args.mint, {"encoding": "jsonParsed"}])
    if not raw.get("ok"):
        return fail(str(raw.get("error")), mint=args.mint, rpc=url)
    value = (raw.get("result") or {}).get("value")
    if not value:
        return fail("mint account not found", mint=args.mint, rpc=url)
    info = ((value.get("data") or {}).get("parsed") or {}).get("info") or {}
    mint_auth = info.get("mintAuthority")
    freeze_auth = info.get("freezeAuthority")
    return emit({"ok": True, "mint": args.mint, "rpc": url, "hasMintAuthority": bool(mint_auth), "hasFreezeAuthority": bool(freeze_auth), "mintAuthority": mint_auth, "freezeAuthority": freeze_auth, "supply": info.get("supply"), "decimals": info.get("decimals"), "extensions": info.get("extensions") or [], "killSignal": bool(mint_auth) or bool(freeze_auth)})

if __name__ == "__main__":
    sys.exit(main())
