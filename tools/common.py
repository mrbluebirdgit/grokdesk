#!/usr/bin/env python3
"""Shared helpers for GrokDesk CLIs. No signing. No keys."""
from __future__ import annotations
import json, os, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_RPC = "https://api.mainnet-beta.solana.com"
WSOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
JUPITER_QUOTE = "https://lite-api.jup.ag/swap/v1/quote"
DESK_CHILDREN = ("proposals", "briefs", "leads", "research", "journal", "incidents", "positions", "watch")

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
            f"# GrokDesk Record\nDate: {utc_now()}\nEngagement: research\nThrowaway wallet: not yet connected\nDaily loss limit: 5%\nHalt: off\nRPC: public\n",
            encoding="utf-8",
        )
    if not (root / "risk-limits.md").exists():
        (root / "risk-limits.md").write_text(
            "# Risk Limits\nStatus: interview pending\nMax ticket USD: TBD\nMax concurrent positions: TBD\nMax slippage bps: 100\nTop-10 holder concentration kill: 25%\nDaily loss halt: 5%\n",
            encoding="utf-8",
        )
    return root

def rpc_url(override: str | None = None) -> str:
    return override or os.environ.get("GROKDESK_RPC") or DEFAULT_RPC
