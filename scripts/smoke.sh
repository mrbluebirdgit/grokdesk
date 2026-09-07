#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export GROKDESK="$ROOT/trading-desk"
python3 tools/bootstrap_desk.py
python3 tools/ticket_helper.py next
python3 tools/ticket_helper.py create --mint So11111111111111111111111111111111111111112 --size 25
python3 tools/ticket_helper.py list
python3 tools/desk_state.py show
echo smoke ok
