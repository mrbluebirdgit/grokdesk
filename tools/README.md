# Tools

Fail-closed JSON on stdout. No private keys. No signing. No /swap.

Reads `.env` or process env:

- `HELIUS_API_KEY` → RPC (`GROKDESK_RPC` wins if set)
- `JUPITER_API_KEY` → `jupiter_quote.py` header `x-api-key`
- `GMGN_API_KEY` → `gmgn_token.py`
- `BIRDEYE_API_KEY` → `birdeye_price.py`
- `SOLSCAN_API_KEY` → `solscan_token.py`
- `TOP10_MAX_PCT` `MAX_SLIPPAGE_BPS`

```bash
python tools/authority_check.py --mint <MINT>
python tools/holder_check.py --mint <MINT>
python tools/jupiter_quote.py --output-mint <MINT> --amount 100000000
python tools/birdeye_price.py --mint <MINT>
python tools/gmgn_token.py --mint <MINT>
python tools/solscan_token.py --mint <MINT>
```
