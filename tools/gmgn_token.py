#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, sys
from common import emit, fail, http_json

URLS = [
    "https://gmgn.ai/api/v1/token_stat/sol/{mint}",
    "https://openapi.gmgn.ai/v1/token/sol/{mint}",
]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mint", required=True)
    args = parser.parse_args()
    key = os.environ.get("GMGN_API_KEY")
    if not key:
        return fail("GMGN_API_KEY missing")
    headers = {"x-api-key": key, "Authorization": f"Bearer {key}"}
    last = None
    for tmpl in URLS:
        url = tmpl.format(mint=args.mint)
        result = http_json(url, headers=headers)
        last = result
        if result.get("ok"):
            return emit({"ok": True, "mint": args.mint, "source": url, "data": result.get("data")})
    return fail("gmgn token lookup failed", mint=args.mint, last=last)

if __name__ == "__main__":
    sys.exit(main())
