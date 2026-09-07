# Signer on iPhone / iPad

`sign_swap.py` and `desk_loop.py` need Python + a key file.
Safari is not used. Chrome or the GitHub app.

iOS cannot keep `~/.config/grokdesk/wallet.json` as a 24/7 process.
Run the loop on GitHub Codespaces (your account) or any always-on box.

## Codespaces (Chrome or GitHub app)

1. https://github.com/mrbluebirdgit/grokdesk
2. Code → Codespaces → Create codespace on main
3. In the terminal:

```bash
pip install -r requirements.txt
mkdir -p ~/.config/grokdesk
nano ~/.config/grokdesk/wallet.json
```

Paste Phantom **private key JSON array** only. Save.
Do not commit. Do not screenshot.

4. Copy repo `env.example` values into Codespace env or `.env` using the same secret names as Actions.

5. Dry run:

```bash
python tools/ticket_helper.py create --mint <MINT> --size 0.1 --slippage 1500
python tools/ticket_helper.py approve --ticket SOL-YYYYMMDD-001 --mint <MINT> --size 0.1 --slippage 1500
python tools/desk_loop.py --once
```

6. Live send:

```bash
python tools/desk_loop.py --live
```

Stop the codespace when you are not trading. A live loop with a funded key is a hot wallet.

Wallet file never goes in git. Never into Actions secrets if you can avoid it.
