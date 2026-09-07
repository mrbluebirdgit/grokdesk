---
name: risk-audit
description: Fail-closed ten-check audit. RISK only. Returns CLEAR, CONDITIONAL, or KILL.
---

Use authority_check.py and holder_check.py. Checks: mint auth, freeze auth, LP, tax, honeypot, concentration, clusters, deployer, token-2022, liquidity vs size. Missing live data is not CLEAR.
