# GrokDesk project rules

This repository is an instruction pack plus read-only Python CLIs for a Grok Bot trading desk.

## Always

- Follow `rules/grokdesk-team.mdc`.
- Start in research. Do not send transactions from this repo.
- Never request or store private keys or seeds.
- Tools print JSON. Treat `ok: false` as stop.
- Only SNIPER (buy) and EXIT (sell) may talk about sending. They still need exact human approval.

## First command from the user

If the user says set up, bootstrap, or "build the desk", run skill `grokdesk-setup` and `SETUP.md`.
