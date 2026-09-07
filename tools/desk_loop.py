#!/usr/bin/env python3
"""Consume APPROVED tickets. Default dry-run. --live sends via sign_swap.py."""
from __future__ import annotations
import argparse, os, subprocess, sys, time
from pathlib import Path
from common import emit, ensure_desk, utc_now

def parse_proposal(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    data = {"path": str(path)}
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- Ticket:"):
            data["ticket"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Mint:"):
            data["mint"] = line.split(":", 1)[1].strip().strip("`")
        elif line.startswith("- Size:"):
            data["size"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Max slippage"):
            data["slippage_bps"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Status:"):
            data["status"] = line.split(":", 1)[1].strip()
    data["sent"] = "SENT" in text or data.get("status") == "SENT"
    return data

def mark_sent(path: Path, payload: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("- Status: APPROVED", "- Status: SENT")
    path.write_text(text + f"\n\nSENT {utc_now()}\n{payload}\n", encoding="utf-8")

def run_sign(mint, size, slippage, ticket, live) -> subprocess.CompletedProcess:
    tools = Path(__file__).resolve().parent
    cmd = [sys.executable, str(tools / "sign_swap.py"), "--mint", mint, "--size", str(size), "--slippage-bps", str(slippage), "--ticket", ticket]
    if live:
        cmd.append("--live")
    return subprocess.run(cmd, cwd=str(tools.parent), capture_output=True, text=True)

def cycle(live: bool) -> dict:
    root = ensure_desk()
    folder = root / "proposals"
    acted = []
    if folder.exists():
        for path in sorted(folder.glob("SOL-*.md")):
            row = parse_proposal(path)
            if row.get("status") != "APPROVED" or row.get("sent"):
                continue
            mint = row.get("mint")
            size = row.get("size")
            slip = row.get("slippage_bps") or os.environ.get("MAX_SLIPPAGE_BPS") or "1500"
            if not mint or not size or size in {"TBD", ""}:
                acted.append({"ticket": row.get("ticket"), "skipped": "size or mint missing"})
                continue
            proc = run_sign(mint, size, slip, row.get("ticket"), live)
            out = (proc.stdout or "") + (proc.stderr or "")
            if live and proc.returncode == 0:
                mark_sent(path, out[:2000])
            acted.append({"ticket": row.get("ticket"), "live": live, "code": proc.returncode, "out": out[:1500]})
    return {"ok": True, "acted": acted, "count": len(acted), "live": live, "utc": utc_now()}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=int, default=20)
    args = parser.parse_args()
    if args.once:
        return emit(cycle(args.live))
    print(f"desk_loop start live={args.live} interval={args.interval}", flush=True)
    while True:
        payload = cycle(args.live)
        print(payload, flush=True)
        time.sleep(max(5, args.interval))

if __name__ == "__main__":
    sys.exit(main())
