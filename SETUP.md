# Set up GrokDesk on Grok Bot

You are a Grok Bot building the user's Solana memecoin desk from this repository.
Follow this file top to bottom. Setup is research-only. No keys in git. No real trades from Bots.

Clone: `git clone https://github.com/mrbluebirdgit/grokdesk.git`

API variable names and obtain links: `docs/API_KEYS.md`
Template: `env.example` → local `.env` (gitignored).

1. Read `rules/grokdesk-team.mdc` and `agents/_constitution.md`.
2. `python tools/bootstrap_desk.py`
3. Install skills from `skills/*/SKILL.md`.
4. Create eight Bots from `agents/*.md`. Paste constitution first.
5. Create group Trading Floor: CHIEF, SCOUT, RISK, WHALE, SNIPER, RUG.
6. Smoke-test SCOUT, RISK, SNIPER, CHIEF.
7. Reply with GROKDESK SETUP COMPLETE. Stay in research.
