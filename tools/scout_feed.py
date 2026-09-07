#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, urllib.error, urllib.request
from common import emit, fail, utc_now
ENDPOINTS = [
    "https://frontend-api-v3.pump.fun/coins?offset=0&limit=20&sort=created_timestamp&order=desc&includeNsfw=false",
    "https://frontend-api.pump.fun/coins?offset=0&limit=20&sort=created_timestamp&order=desc&includeNsfw=false",
]

def fetch(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "GrokDesk/0.1 research"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return {"ok": True, "url": url, "data": json.loads(resp.read().decode())}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "url": url, "error": f"http {exc.code}"}
    except Exception as exc:
        return {"ok": False, "url": url, "error": str(exc)}

def normalize(item):
    return {"mint": item.get("mint") or item.get("address") or item.get("tokenAddress"), "name": item.get("name"), "symbol": item.get("symbol"), "creator": item.get("creator") or item.get("deployer"), "created": item.get("created_timestamp") or item.get("createdAt"), "usd_market_cap": item.get("usd_market_cap") or item.get("market_cap"), "complete": item.get("complete"), "website": item.get("website"), "twitter": item.get("twitter"), "telegram": item.get("telegram")}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--url")
    args = parser.parse_args()
    urls = [args.url] if args.url else ENDPOINTS
    last_error = None
    for url in urls:
        result = fetch(url)
        if not result.get("ok"):
            last_error = result
            continue
        data = result["data"]
        rows = data if isinstance(data, list) else data.get("coins") or data.get("data") or []
        if not isinstance(rows, list):
            last_error = {"ok": False, "error": "unexpected shape", "url": url}
            continue
        leads = [normalize(x) for x in rows[: args.limit] if isinstance(x, dict)]
        leads = [x for x in leads if x.get("mint")]
        return emit({"ok": True, "source": result["url"], "count": len(leads), "leads": leads, "fetched": utc_now()})
    return fail("public pump.fun feed blocked or changed; use browser discovery-tools", last_error=last_error)

if __name__ == "__main__":
    sys.exit(main())
