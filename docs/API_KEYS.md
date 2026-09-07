# API keys for GrokDesk

Live values go in local `.env` or GitHub Actions secrets.
Do not commit them. This repo is public: https://github.com/mrbluebirdgit/grokdesk

Copy `env.example` → `.env`.

## Axiom Trade

- Terminal: https://axiom.trade
- Status (no official public trading API): https://tradeonaxiom.com/axiom-trade-api/
- Community SDK: https://pypi.org/project/axiomtradeapi/
- Auth docs: https://docs.chipatrade.com/docs/axiomtradeapi/authentication/
- Endpoints: https://docs.chipatrade.com/docs/axiomtradeapi/api/endpoints/

Variables:
- `AXIOM_ACCESS_TOKEN`
- `AXIOM_REFRESH_TOKEN`
- optional `AXIOM_EMAIL` / `AXIOM_PASSWORD` for SDK login

How: log in on axiom.trade, pull access + refresh tokens the SDK documents, paste into `.env`.

Do not confuse with:
- https://docs.axiom.xyz (ZK proving `AXIOM_API_KEY`)
- https://axiom.ai (browser automation)

## Photon

- Terminal: https://photon-sol.tinyastro.io/
- Must be `*.tinyastro.io`
- No published first-party developer API / secret key
- Data-style Photon routes (Bitquery, not Tiny Astro): https://docs.bitquery.io/docs/blockchain/Solana/solana-photon-api/

Variables:
- `PHOTON_BASE_URL=https://photon-sol.tinyastro.io`
- `PHOTON_SESSION` only if you later add a session cookie yourself

## Jito

- Send API: https://docs.jito.wtf/lowlatencytxnsend/
- Searcher examples: https://github.com/jito-labs/searcher-examples
- Python client: https://github.com/jito-labs/jito-python
- Tip accounts: https://jito-foundation.gitbook.io/mev/mev-payment-and-distribution/on-chain-addresses
- Rate-limit form: https://web.miniextensions.com/WV3gZjFwqNqITsMufIEp
- Access note: https://docs.google.com/document/d/e/2PACX-1vRZoiYWNvIdX4r6lf-8E5E0l8SEPKeXXRYRcviwQJjmizeJkeQ_YM4IWGQne-C_8_lFFXv-z6yI6y4K/pub

JSON-RPC works with no key at 5 rps/region.
Higher limits: UUID in `x-jito-auth` or `?uuid=`.

Variables:
- `JITO_BLOCK_ENGINE_URL`
- `JITO_BUNDLE_URL`
- `JITO_TX_URL`
- `JITO_UUID` (optional)
- `JITO_TIP_ACCOUNT`
- `JITO_AUTH_KEYPAIR_PATH` (local file, never commit the json)

Mainnet bundle POST:
`https://mainnet.block-engine.jito.wtf/api/v1/bundles`

## GitHub Actions secrets (if you add CI later)

Repo → Settings → Secrets and variables → Actions.
Add the same names as in `env.example`.
No Actions-secret write tool from this chat; you click those in the UI:
https://github.com/mrbluebirdgit/grokdesk/settings/secrets/actions
