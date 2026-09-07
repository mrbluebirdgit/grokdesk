#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
fail=0
need=(SETUP.md AGENTS.md README.md GAMEPLAN.md plugin.json rules/grokdesk-team.mdc agents/_constitution.md agents/chief.md agents/scout.md agents/risk.md agents/whale.md agents/sniper.md agents/rug.md agents/exit.md agents/shill.md .grok-plugin/plugin.json)
for f in "${need[@]}"; do
  if [[ ! -f "$f" ]]; then echo "MISSING $f"; fail=1; fi
done
writers=0
for f in agents/*.md; do
  base="$(basename "$f")"
  [[ "$base" == "README.md" || "$base" == "_constitution.md" ]] && continue
  if ! grep -q '^name:' "$f"; then echo "NO name frontmatter $f"; fail=1; fi
  if grep -q 'writes_to_exchange: true' "$f"; then
    writers=$((writers + 1))
    case "$base" in sniper.md|exit.md) ;; *) echo "unexpected writer $f"; fail=1 ;; esac
  fi
done
if [[ "$writers" -ne 2 ]]; then echo "expected 2 writers, got $writers"; fail=1; fi
for skill in skills/*/SKILL.md; do
  dir="$(basename "$(dirname "$skill")")"
  name="$(grep -m1 '^name:' "$skill" | awk '{print $2}' | tr -d '\r')"
  if [[ "$name" != "$dir" ]]; then echo "skill name mismatch $dir vs $name"; fail=1; fi
done
python3 - <<'PY'
import json, pathlib
for path in [pathlib.Path('plugin.json'), pathlib.Path('.grok-plugin/plugin.json')]:
    json.loads(path.read_text())
print('json ok')
PY
echo check complete
exit "$fail"
