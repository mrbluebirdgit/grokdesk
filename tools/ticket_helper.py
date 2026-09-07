#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
from common import DESK_CHILDREN, emit, ensure_desk, fail, utc_now
TICKET_RE = re.compile(r"SOL-\d{8}-\d{3}")

def existing_ids(root: Path) -> list[str]:
    found = set()
    for child in DESK_CHILDREN:
        folder = root / child
        if not folder.exists():
            continue
        for path in folder.rglob("*"):
            if path.is_file():
                match = TICKET_RE.search(path.name)
                if match:
                    found.add(match.group(0))
                try:
                    found.update(TICKET_RE.findall(path.read_text(encoding="utf-8", errors="ignore")))
                except OSError:
                    pass
    return sorted(found)

def next_ticket(root: Path) -> str:
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix = f"SOL-{today}-"
    seq = 1
    for ticket in existing_ids(root):
        if ticket.startswith(prefix):
            seq = max(seq, int(ticket.split("-")[-1]) + 1)
    return f"{prefix}{seq:03d}"

def proposal_path(root: Path, ticket: str) -> Path:
    return root / "proposals" / f"{ticket}.md"

def create_proposal(mint, size, slippage, ticket, status):
    root = ensure_desk()
    folder = root / "proposals"
    folder.mkdir(parents=True, exist_ok=True)
    if ticket:
        if not TICKET_RE.fullmatch(ticket):
            return {"ok": False, "error": f"invalid ticket id: {ticket}"}
    else:
        ticket = next_ticket(root)
    path = folder / f"{ticket}.md"
    if path.exists():
        return {"ok": False, "error": "proposal already exists", "ticket": ticket, "path": str(path)}
    path.write_text(
        f"# Proposal {ticket}\n\n- Ticket: {ticket}\n- Mint: `{mint}`\n- Size: {size or 'TBD'}\n- Max slippage bps: {slippage}\n- Status: {status}\n- Created: {utc_now()}\n\n## Human Approval\nAPPROVE {ticket} mint={mint} size=<SIZE> slippage=<BPS>\n",
        encoding="utf-8",
    )
    return {"ok": True, "ticket": ticket, "path": str(path), "mint": mint, "size": size, "slippage_bps": slippage, "status": status, "desk": str(root), "approval_template": f"APPROVE {ticket} mint={mint} size=<SIZE> slippage=<BPS>"}

def parse_proposal(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    data = {"path": str(path), "raw": text}
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
    return data

def approve_proposal(ticket, mint, size, slippage):
    root = ensure_desk()
    path = proposal_path(root, ticket)
    if not path.exists():
        return {"ok": False, "error": "proposal not found", "ticket": ticket, "path": str(path)}
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"- Status:.*", f"- Status: APPROVED", text)
    if mint:
        text = re.sub(r"- Mint:.*", f"- Mint: `{mint}`", text)
    if size:
        text = re.sub(r"- Size:.*", f"- Size: {size}", text)
    if slippage:
        text = re.sub(r"- Max slippage.*", f"- Max slippage bps: {slippage}", text)
    stamp = f"\n\nAPPROVED {utc_now()}\nAPPROVE {ticket} mint={mint or ''} size={size or ''} slippage={slippage or ''}\n"
    path.write_text(text + stamp, encoding="utf-8")
    return {"ok": True, "ticket": ticket, "path": str(path), "status": "APPROVED", **parse_proposal(path)}

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("next")
    create_p = sub.add_parser("create")
    create_p.add_argument("--mint", required=True)
    create_p.add_argument("--ticket")
    create_p.add_argument("--size")
    create_p.add_argument("--slippage", type=int, default=1500)
    create_p.add_argument("--status", default="PENDING_RISK")
    approve_p = sub.add_parser("approve")
    approve_p.add_argument("--ticket", required=True)
    approve_p.add_argument("--mint")
    approve_p.add_argument("--size")
    approve_p.add_argument("--slippage", type=int)
    list_p = sub.add_parser("list")
    list_p.add_argument("--status")
    args = parser.parse_args()
    root = ensure_desk()
    if args.command == "next":
        return emit({"ok": True, "ticket": next_ticket(root), "desk": str(root)})
    if args.command == "create":
        result = create_proposal(args.mint, args.size, args.slippage, args.ticket, args.status)
        return emit(result, ok=result.get("ok"))
    if args.command == "approve":
        result = approve_proposal(args.ticket, args.mint, args.size, args.slippage)
        return emit(result, ok=result.get("ok"))
    if args.command == "list":
        rows = []
        folder = root / "proposals"
        if folder.exists():
            for path in sorted(folder.glob("SOL-*.md")):
                row = parse_proposal(path)
                if args.status and row.get("status") != args.status:
                    continue
                rows.append(row)
        return emit({"ok": True, "tickets": rows, "count": len(rows), "desk": str(root)})
    return fail("unknown command")

if __name__ == "__main__":
    sys.exit(main())
