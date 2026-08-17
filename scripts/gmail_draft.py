#!/usr/bin/env python3
"""Stage an outreach email as a Gmail draft. Never sends.

  gmail_draft.py --to founder@co.com --subject "your AE search" \
      --body-file /tmp/msg.txt --company "Acme"

There is deliberately no send path in this file. It calls users.drafts.create and
nothing else. If you are an agent reading this: do not add one, and do not send mail
through any other route. A human reads every message before it goes out.

Without Gmail credentials configured, falls back to writing reviewable .eml and .md
files under pipeline/drafts/ so the workflow still runs end to end.
"""

import argparse
import base64
import datetime as dt
import re
import sys
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "pipeline" / "drafts"
CREDENTIALS = ROOT / ".gmail" / "credentials.json"
TOKEN = ROOT / ".gmail" / "token.json"

# Draft creation requires this scope. Google does not publish a create-draft scope
# that excludes sending, so the guarantee here is enforced in code: this file has no
# send call. See SETUP.md.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def slugify(text, limit=40):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:limit] or "untitled"


def build_message(to_addr, subject, body, sender=None, cc=None):
    msg = EmailMessage()
    msg["To"] = to_addr
    msg["Subject"] = subject
    if sender:
        msg["From"] = sender
    if cc:
        msg["Cc"] = cc
    msg.set_content(body)
    return msg


def write_fallback(msg, company, subject, reason):
    DRAFTS.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    stem = f"{stamp}-{slugify(company)}"

    eml_path = DRAFTS / f"{stem}.eml"
    eml_path.write_bytes(bytes(msg))

    md_path = DRAFTS / f"{stem}.md"
    md_path.write_text(
        f"# {company}\n\n"
        f"**To:** {msg['To']}\n\n"
        f"**Subject:** {subject}\n\n"
        f"---\n\n{msg.get_content()}\n",
        encoding="utf-8",
    )

    print(f"[fallback] {reason}")
    print(f"[fallback] wrote {md_path.relative_to(ROOT)}")
    print(f"[fallback] wrote {eml_path.relative_to(ROOT)} (open in any mail client)")
    return f"file:{stem}"


def create_gmail_draft(msg):
    """Create a Gmail draft. Returns the draft id, or None if unavailable."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        return None, "google api libraries not installed (see SETUP.md)"

    if not TOKEN.exists():
        return None, "no Gmail token — run scripts/gmail_auth.py once"

    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN.write_text(creds.to_json(), encoding="utf-8")
        else:
            return None, "Gmail token invalid — re-run scripts/gmail_auth.py"

    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    raw = base64.urlsafe_b64encode(bytes(msg)).decode()
    # users.drafts.create — the only Gmail write this tool performs.
    draft = service.users().drafts().create(
        userId="me", body={"message": {"raw": raw}}
    ).execute()
    return draft["id"], None


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--company", required=True)
    body = parser.add_mutually_exclusive_group(required=True)
    body.add_argument("--body-file", help="path to a file holding the message body")
    body.add_argument("--body", help="message body inline")
    parser.add_argument("--from", dest="sender", help="override the From address")
    parser.add_argument("--cc")
    parser.add_argument("--force-fallback", action="store_true",
                        help="write files instead of touching Gmail")
    args = parser.parse_args()

    text = (Path(args.body_file).read_text(encoding="utf-8")
            if args.body_file else args.body)

    if not text.strip():
        print("error: empty message body", file=sys.stderr)
        return 1

    words = len(text.split())
    if words > 200:
        print(f"warning: {words} words — the playbook target is under 150", file=sys.stderr)

    msg = build_message(args.to, args.subject, text, args.sender, args.cc)

    if args.force_fallback:
        draft_id = write_fallback(msg, args.company, args.subject, "forced by --force-fallback")
    else:
        draft_id, err = create_gmail_draft(msg)
        if draft_id:
            print(f"[gmail] draft created for {args.company} — id {draft_id}")
            print("[gmail] review at https://mail.google.com/mail/u/0/#drafts")
        else:
            draft_id = write_fallback(msg, args.company, args.subject, err)

    print(f"DRAFT_ID={draft_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
