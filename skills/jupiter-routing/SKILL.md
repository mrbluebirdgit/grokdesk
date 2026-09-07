---
name: jupiter-routing
description: Quote a route. Never call swap-build or send.
---

python tools/jupiter_quote.py --output-mint <MINT> --amount <MINOR_UNITS> --slippage-bps 100
Use lite-api.jup.ag/swap/v1/quote only. This repo has no /swap client.
