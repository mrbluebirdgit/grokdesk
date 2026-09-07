# Encrypted secrets

Public repo. Only `*.age` files belong here. Never plaintext keys.

Tool: https://github.com/FiloSottile/age

## You (once)

```bash
age-keygen -o ~/.config/grokdesk/age.key
# public key prints as age1...
```

Keep `age.key` OFF git. That file is what decrypts.

Encrypt a local file:

```bash
age -r age1YOURPUBLICKEY -o secrets/env.age .env
# or a keypair json:
age -r age1YOURPUBLICKEY -o secrets/jito-auth.json.age ./jito-auth.json
```

Commit only `secrets/*.age`.

## Grok Bot (your machine)

```bash
export AGE_KEY_FILE=$HOME/.config/grokdesk/age.key
age -d -i "$AGE_KEY_FILE" secrets/env.age > .env
```

Then load `.env`. Do not echo values into chat or commit the output.

## This chat / Grok on xAI servers

Cannot decrypt `*.age` without `age.key`.
Do not paste `age.key` or seed phrases here.

## Allowed in `*.age`

- `AXIOM_ACCESS_TOKEN` / `AXIOM_REFRESH_TOKEN`
- `JITO_UUID`
- `GROKDESK_RPC` / Helius key

Wallet seed / Phantom private key: encrypt if you want a backup. GrokDesk does not sign with it. Human signs on Axiom/Photon.
