# GrokDesk

Eight-role Solana memecoin desk packaged for **Grok Bot**.

This is an instruction pack plus read-only Python tools. It is not a signer, not an exchange client, and not a strategy. Private keys never enter the system. Only a human-approved ticket may become a send, and this repo does not build swap transactions.

## What you get

- 8 Bot profiles: CHIEF, SCOUT, RISK, WHALE, SNIPER, RUG, EXIT, SHILL
- Skills Grok Bot can install from `skills/`
- Always-on rule `rules/grokdesk-team.mdc`
- Working CLIs under `tools/` (JSON, fail-closed)
- `SETUP.md` a Bot can execute unattended in research mode
- Dual manifests: open `plugin.json` + `.grok-plugin/plugin.json`

## Grok Bot first run

On the Bot computer:

```bash
git clone https://github.com/mrbluebirdgit/grokdesk.git
cd grokdesk
python tools/bootstrap_desk.py
./scripts/check.sh
```

Then tell CHIEF: `Follow SETUP.md and skill grokdesk-setup. Stay in research.`

Details: [SETUP.md](SETUP.md), [GAMEPLAN.md](GAMEPLAN.md), [AGENTS.md](AGENTS.md).

## Tools

```bash
python tools/ticket_helper.py next
python tools/authority_check.py --mint <MINT>
python tools/holder_check.py --mint <MINT>
python tools/jupiter_quote.py --output-mint <MINT> --amount 100000000
python tools/scout_feed.py --limit 5
python tools/desk_state.py show
```

## Safety

- Engagement starts at `research`
- Approval phrase must include ticket ID + mint + size + slippage
- RISK KILL is final
- Daily loss halt at 5 percent
- No `/swap` client ships here

MIT. Not financial advice.
