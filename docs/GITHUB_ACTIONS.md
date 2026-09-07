# Run GrokDesk on GitHub

Workflow: https://github.com/mrbluebirdgit/grokdesk/actions/workflows/desk.yml
File: `.github/workflows/desk.yml`

## One-time secrets

https://github.com/mrbluebirdgit/grokdesk/settings/secrets/actions

Add:
- `AGE_SECRET_KEY` — full text of `~/.config/grokdesk/age.key` (`AGE-SECRET-KEY-1...`)

Optional extras with the same names as `env.example`:
- `AXIOM_ACCESS_TOKEN`
- `AXIOM_REFRESH_TOKEN`
- `JITO_UUID`
- `GROKDESK_RPC`

## Encrypted file in git

Commit `secrets/env.age` (see `secrets/README.md`).
Runner decrypts only if both that file and `AGE_SECRET_KEY` exist.

## Trigger

Push to `main`, or Actions → grokdesk → Run workflow.

This job is pack check + smoke. It does not sign trades.
