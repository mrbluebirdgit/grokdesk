#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DESK = ROOT / "trading-desk-test"

def run(args):
    merged = os.environ.copy()
    merged["GROKDESK"] = str(DESK)
    return subprocess.run([sys.executable, *args], cwd=str(TOOLS), capture_output=True, text=True, env=merged)

def load(proc):
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return json.loads(proc.stdout)

def main():
    if DESK.exists():
        import shutil
        shutil.rmtree(DESK)
    assert load(run(["bootstrap_desk.py"]))["ok"]
    nxt = load(run(["ticket_helper.py", "next"]))
    assert nxt["ticket"].startswith("SOL-")
    created = load(run(["ticket_helper.py", "create", "--mint", "So11111111111111111111111111111111111111112", "--size", "10"]))
    assert created["ok"]
    print("test_local ok", created["ticket"])

if __name__ == "__main__":
    main()
