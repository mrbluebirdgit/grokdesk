#!/usr/bin/env python3
"""Sign + send a Jupiter swap from a local key file. Never commit the key."""
from __future__ import annotations
import argparse, base64, json, os, sys, time
from pathlib import Path
from common import WSOL, emit, fail, jupiter_quote_url, rpc_url

def wallet_path() -> Path:
    raw = os.environ.get("GROKDESK_WALLET") or str(Path.home() / ".config/grokdesk/wallet.json")
    return Path(raw).expanduser()

def load_keypair(path: Path):
    try:
        from solders.keypair import Keypair
    except ImportError:
        raise SystemExit("pip install -r requirements.txt")
    if not path.is_file():
        raise FileNotFoundError(f"wallet missing: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "secretKey" in data:
        data = data["secretKey"]
    if isinstance(data, str):
        try:
            return Keypair.from_base58_string(data)
        except Exception:
            data = json.loads(data)
    return Keypair.from_bytes(bytes(data))

def sol_to_lamports(size: str) -> int:
    size = str(size).strip().lower().replace("sol", "")
    return int(float(size) * 1_000_000_000)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mint", required=True)
    parser.add_argument("--size", required=True, help="SOL amount, e.g. 0.1")
    parser.add_argument("--slippage-bps", type=int, default=int(os.environ.get("MAX_SLIPPAGE_BPS") or 1500))
    parser.add_argument("--ticket")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--wallet")
    args = parser.parse_args()
    path = Path(args.wallet).expanduser() if args.wallet else wallet_path()
    try:
        kp = load_keypair(path)
    except FileNotFoundError as exc:
        return fail(str(exc), hint="put Phantom private key JSON on the box running this, not git")
    except Exception as exc:
        return fail(f"wallet load failed: {exc}")

    try:
        import httpx
        from solders.transaction import VersionedTransaction
    except ImportError:
        return fail("pip install -r requirements.txt")

    amount = sol_to_lamports(args.size)
    quote_base = jupiter_quote_url()
    headers = {"Accept": "application/json"}
    jkey = os.environ.get("JUPITER_API_KEY")
    if jkey:
        headers["x-api-key"] = jkey
    quote_url = f"{quote_base}?inputMint={WSOL}&outputMint={args.mint}&amount={amount}&slippageBps={args.slippage_bps}"
    with httpx.Client(timeout=30.0) as client:
        q = client.get(quote_url, headers=headers)
        if q.status_code >= 400:
            return fail(f"jupiter quote http {q.status_code}", body=q.text[:300])
        quote = q.json()
        if not args.live:
            return emit({"ok": True, "dryRun": True, "ticket": args.ticket, "mint": args.mint, "sizeSol": args.size, "inAmount": quote.get("inAmount"), "outAmount": quote.get("outAmount"), "priceImpactPct": quote.get("priceImpactPct"), "pubkey": str(kp.pubkey()), "note": "pass --live to send"})
        swap_url = os.environ.get("JUPITER_SWAP_URL") or "https://api.jup.ag/swap/v1/swap"
        payload = {"quoteResponse": quote, "userPublicKey": str(kp.pubkey()), "wrapAndUnwrapSol": True, "dynamicSlippage": False}
        s = client.post(swap_url, headers={**headers, "Content-Type": "application/json"}, json=payload)
        if s.status_code >= 400:
            return fail(f"jupiter swap http {s.status_code}", body=s.text[:300])
        swap_tx = (s.json() or {}).get("swapTransaction")
        if not swap_tx:
            return fail("jupiter returned no swapTransaction", body=str(s.json())[:300])
        tx = VersionedTransaction.from_bytes(base64.b64decode(swap_tx))
        signed = VersionedTransaction(tx.message, [kp])
        raw = base64.b64encode(bytes(signed)).decode()
        rpc = rpc_url()
        sent = client.post(rpc, json={"jsonrpc": "2.0", "id": 1, "method": "sendTransaction", "params": [raw, {"encoding": "base64", "skipPreflight": True, "maxRetries": 3}]})
        body = sent.json()
        if body.get("error"):
            return fail(str(body["error"]), rpc="helius" if "helius" in rpc else rpc)
        sig = body.get("result")
        return emit({"ok": True, "dryRun": False, "ticket": args.ticket, "mint": args.mint, "sizeSol": args.size, "signature": sig, "pubkey": str(kp.pubkey()), "sentAt": int(time.time())})

if __name__ == "__main__":
    sys.exit(main())
