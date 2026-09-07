#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys
from common import emit, ensure_desk, fail, utc_now
ALLOWED = {"research", "paper", "micro-live"}

def parse_desk(text):
    fields = {}
    for line in text.splitlines():
        if ":" in line and not line.startswith("#"):
            key, val = line.split(":", 1)
            fields[key.strip().lower()] = val.strip()
    return fields

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["show", "set-engagement", "halt", "resume"])
    parser.add_argument("--value")
    parser.add_argument("--reason", default="")
    args = parser.parse_args()
    root = ensure_desk()
    path = root / "desk.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    fields = parse_desk(text)
    if args.command == "show":
        return emit({"ok": True, "desk": str(root), "path": str(path), "fields": fields, "raw": text})
    if args.command == "set-engagement":
        if args.value not in ALLOWED:
            return fail(f"engagement must be one of {sorted(ALLOWED)}")
        current = (fields.get("engagement") or "research").lower()
        if args.value == "micro-live" and current == "research":
            return fail("cannot jump research -> micro-live; set paper first after risk interview")
        lines = []
        seen = False
        for line in text.splitlines():
            if line.lower().startswith("engagement:"):
                lines.append(f"Engagement: {args.value}")
                seen = True
            else:
                lines.append(line)
        if not seen:
            lines.append(f"Engagement: {args.value}")
        path.write_text("\n".join(lines) + f"\nUpdated: {utc_now()} set-engagement {args.value}\n", encoding="utf-8")
        return emit({"ok": True, "engagement": args.value, "path": str(path)})
    if args.command == "halt":
        updated = re.sub(r"(?im)^Halt:.*$", "Halt: on", text) if re.search(r"(?im)^Halt:", text) else text + "\nHalt: on\n"
        path.write_text(updated + f"\nUpdated: {utc_now()} FLOOR HALTED \u2013 DAILY LOSS LIMIT {args.reason}\n", encoding="utf-8")
        return emit({"ok": True, "halt": "on", "banner": "FLOOR HALTED \u2013 DAILY LOSS LIMIT"})
    if args.command == "resume":
        if not args.reason:
            return fail("resume requires --reason from the human")
        updated = re.sub(r"(?im)^Halt:.*$", "Halt: off", text) if re.search(r"(?im)^Halt:", text) else text + "\nHalt: off\n"
        path.write_text(updated + f"\nUpdated: {utc_now()} halt reset: {args.reason}\n", encoding="utf-8")
        return emit({"ok": True, "halt": "off"})
    return fail("unknown command")

if __name__ == "__main__":
    sys.exit(main())
