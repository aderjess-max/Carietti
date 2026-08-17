#!/usr/bin/env python3
"""One-time Gmail authorization for the prospecting agent.

Run once on your own machine:

    python3 scripts/gmail_auth.py

Opens a browser, asks you to grant access, and writes .gmail/token.json.
After that, gmail_draft.py works without further prompting.

Requires .gmail/credentials.json from a Google Cloud OAuth client — see SETUP.md.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GMAIL_DIR = ROOT / ".gmail"
CREDENTIALS = GMAIL_DIR / "credentials.json"
TOKEN = GMAIL_DIR / "token.json"

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def main():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Missing dependencies. Install them first:\n")
        print("    pip install -r requirements.txt\n")
        return 1

    if not CREDENTIALS.exists():
        print(f"No OAuth client at {CREDENTIALS.relative_to(ROOT)}\n")
        print("Create one in Google Cloud Console (5 minutes, free) — SETUP.md has")
        print("the click-by-click. Download the JSON and save it to that path.")
        return 1

    if TOKEN.exists():
        answer = input(f"{TOKEN.relative_to(ROOT)} already exists. Replace it? [y/N] ")
        if answer.strip().lower() != "y":
            print("Left the existing token alone.")
            return 0

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS), SCOPES)
    creds = flow.run_local_server(port=0)

    GMAIL_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN.write_text(creds.to_json(), encoding="utf-8")
    TOKEN.chmod(0o600)

    print(f"\nAuthorized. Token written to {TOKEN.relative_to(ROOT)}")
    print("This grants draft access. The agent's code has no send path —")
    print("every message waits in your Gmail drafts until you send it.\n")
    print("Test it:")
    print('    python3 scripts/gmail_draft.py --to you@example.com \\')
    print('        --subject "test" --body "it works" --company "Test"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
