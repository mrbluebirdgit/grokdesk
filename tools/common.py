#!/usr/bin/env python3
"""Shared helpers for GrokDesk CLIs. No signing."""
from __future__ import annotations
import json, os, sys, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_RPC = "https://api.mainnet-beta.solana.com"
WSOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
JUPITER_QUOTE_LITE = "https://lite-api.jup.ag/swap/v1/quote"
JUPITER_QUOTE = "https://api.jup.ag/swap/v1/quote"
BIRDEYE_PRICE = "https://public-api.birdeye.so/defi/price"
SOLSCAN_TOKEN_META = "https://pro-api.solscan.io/v2.0/token/meta"
GMGN_TOKEN = "https://gmgn.ai/api/v1/token_stat/sol/{mint}"
DESK_CHILDREN = ("proposals", "briefs", "leads", "research", "journal", "incidents", "positions", "watch")

def _load_dotenv() -> None:
    roots = [Path.cwd() / ".env", Path(__file__).resolve().parents[1] / ".env"]
    seen = set()
    for path in roots:
        path = path.resolve()
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val

_load_dotenv()

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def emit(payload: dict[str, Any], ok: bool | None = None) -> int:
    if ok is not None:
        payload["ok"] = ok
    payload.setdefault("utc", utc_now())
    sys.stdout.write(json.dumps(payload, indent=2, default=str) + "\n")
    return 0 if payload.get("ok", False) else 1

def fail(error: str, **extra: Any) -> int:
    return emit({"ok": False, "error": error, **extra}, ok=False)

def desk_root() -> Path:
    env = os.environ.get("GROKDESK") or os.environ.get("GROKDESK_DESK")
    if env:
        return Path(env).expanduser().resolve()
    workspace = Path("/workspace/trading-desk")
    if workspace.exists() or Path("/workspace").exists():
        return workspace
    return (Path.cwd() / "trading-desk").resolve()

def ensure_desk(root: Path | None = None) -> Path:
    root = root or desk_root()
    for child in DESK_CHILDREN:
        (root / child).mkdir(parents=True, exist_ok=True)
    if not (root / "desk.md").exists():
        (root / "desk.md").write_text(
            f"# GrokDesk Record\nDate: {utc_now()}\nEngagement: research\nThrowaway wallet: not yet connected\nDaily loss limit: 5%\nHalt: off\nRPC: helius-or-public\n",
            encoding="utf-8",
        )
    if not (root / "risk-limits.md").exists():
        (root / "risk-limits.md").write_text(
            "# Risk Limits\nStatus: interview pending\nMax ticket USD: TBD\nMax concurrent positions: TBD\nMax slippage bps: 100\nTop-10 holder concentration kill: 25%\nDaily loss halt: 5%\n",
            encoding="utf-8",
        )
    return root

def rpc_url(override: str | None = None) -> str:
    if override:
        return override
    if os.environ.get("GROKDESK_RPC"):
        return os.environ["GROKDESK_RPC"]
    helius = os.environ.get("HELIUS_API_KEY")
    if helius:
        return f"https://mainnet.helius-rpc.com/?api-key={helius}"
    return DEFAULT_RPC

def jupiter_quote_url() -> str:
    return os.environ.get("JUPITER_QUOTE_URL") or (JUPITER_QUOTE if os.environ.get("JUPITER_API_KEY") else JUPITER_QUOTE_LITE)

def http_json(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "GrokDesk/0.2", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"ok": True, "status": resp.status, "data": json.loads(resp.read().decode())}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="ignore")[:400]
        return {"ok": False, "status": exc.code, "error": f"http {exc.code}", "body": body, "url": url}
    except Exception as exc:
        return {"ok": False, "error": str(exc), "url": url}

def rpc_call(url: str, method: str, params: Any) -> dict[str, Any]:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        return {"error": {"message": str(exc)}}
