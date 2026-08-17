#!/usr/bin/env python3
"""Pipeline state for the prospecting agent.

Plain CSV so it opens in Excel. Standard library only.

  pipeline.py add --company X --vertical health --score 65 [...]
  pipeline.py update --company X --field value
  pipeline.py due [--days 0]
  pipeline.py touched --company X --play 1 --touch 1 [--subject S] [--draft-id D]
  pipeline.py status
  pipeline.py list [--status active] [--vertical health]
"""

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "pipeline"
TARGETS = PIPELINE / "targets.csv"
TOUCHES = PIPELINE / "touches.csv"

FIELDS = [
    "company", "domain", "vertical", "contact_name", "contact_title",
    "contact_email", "linkedin", "stage_read", "signals", "score", "status",
    "play", "observation", "added", "last_touch", "next_touch", "touch_num",
    "notes",
]

TOUCH_FIELDS = [
    "timestamp", "company", "contact_email", "play", "touch_num",
    "channel", "subject", "draft_id",
]

# Days after touch 1 that each subsequent touch is due.
CADENCE = {1: 0, 2: 4, 3: 11, 4: 18}
MAX_TOUCH = 4

VALID_STATUS = {
    "new", "researching", "watch", "nurture", "active", "hot",
    "sequenced", "replied", "meeting", "won", "dead",
}


def today():
    return dt.date.today()


def parse_date(value):
    if not value:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def ensure_files():
    PIPELINE.mkdir(parents=True, exist_ok=True)
    if not TARGETS.exists():
        with TARGETS.open("w", newline="", encoding="utf-8") as fh:
            csv.DictWriter(fh, fieldnames=FIELDS).writeheader()
    if not TOUCHES.exists():
        with TOUCHES.open("w", newline="", encoding="utf-8") as fh:
            csv.DictWriter(fh, fieldnames=TOUCH_FIELDS).writeheader()


def read_targets():
    ensure_files()
    with TARGETS.open(newline="", encoding="utf-8") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def write_targets(rows):
    with TARGETS.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})


def find(rows, company):
    key = company.strip().lower()
    for row in rows:
        if row.get("company", "").strip().lower() == key:
            return row
    return None


def cmd_add(args):
    rows = read_targets()
    if find(rows, args.company):
        print(f"exists: {args.company} — use `update` instead")
        return 1

    score = args.score if args.score is not None else 0
    if score < 40:
        print(f"rejected: {args.company} scored {score}, below the 40 threshold")
        return 1

    status = args.status or (
        "hot" if score >= 70 else "active" if score >= 55 else "nurture"
    )
    if status not in VALID_STATUS:
        print(f"bad status '{status}' — one of: {', '.join(sorted(VALID_STATUS))}")
        return 1

    rows.append({
        "company": args.company,
        "domain": args.domain or "",
        "vertical": args.vertical or "",
        "contact_name": args.contact_name or "",
        "contact_title": args.contact_title or "",
        "contact_email": args.contact_email or "",
        "linkedin": args.linkedin or "",
        "stage_read": args.stage_read or "",
        "signals": args.signals or "",
        "score": str(score),
        "status": status,
        "play": str(args.play) if args.play else "",
        "observation": args.observation or "",
        "added": today().isoformat(),
        "last_touch": "",
        "next_touch": args.next_touch or today().isoformat(),
        "touch_num": "0",
        "notes": args.notes or "",
    })
    write_targets(rows)
    print(f"added: {args.company} — score {score}, status {status}")
    return 0


def cmd_update(args):
    rows = read_targets()
    row = find(rows, args.company)
    if not row:
        print(f"not found: {args.company}")
        return 1

    changed = []
    for field in FIELDS:
        value = getattr(args, field.replace("-", "_"), None)
        if field in ("company", "added") or value is None:
            continue
        row[field] = str(value)
        changed.append(field)

    if not changed:
        print("nothing to update")
        return 1

    if "score" in changed and "status" not in changed:
        score = int(row["score"] or 0)
        row["status"] = (
            "hot" if score >= 70 else "active" if score >= 55
            else "nurture" if score >= 40 else "dead"
        )
        changed.append("status")

    write_targets(rows)
    print(f"updated: {args.company} — {', '.join(changed)}")
    return 0


def cmd_due(args):
    rows = read_targets()
    horizon = today() + dt.timedelta(days=args.days)
    terminal = {"dead", "won", "replied", "meeting", "watch"}

    due, needs_research = [], []
    for row in rows:
        if row.get("status") in terminal:
            continue
        touch_num = int(row.get("touch_num") or 0)
        if touch_num >= MAX_TOUCH:
            continue
        next_date = parse_date(row.get("next_touch"))
        if not next_date or next_date > horizon:
            continue
        # A target is only draftable once research has produced a contact,
        # a play, and an observation worth opening on.
        if (row.get("status") in {"new", "researching"}
                or not row.get("contact_email")
                or not row.get("play")
                or not row.get("observation")):
            needs_research.append(row)
            continue
        due.append((next_date, touch_num + 1, row))

    if due:
        due.sort(key=lambda item: (item[0], -int(item[2].get("score") or 0)))
        print(f"{len(due)} touch(es) ready to draft through {horizon.isoformat()}\n")
        for next_date, touch, row in due:
            print(
                f"  {next_date.isoformat()}  {row['company']}"
                f"  · play {row['play']} touch {touch}"
                f"  · score {row.get('score')}"
                f"  · {row.get('contact_name') or '?'} <{row['contact_email']}>"
            )
            print(f"      obs: {row['observation']}")
    else:
        print("nothing ready to draft")

    if needs_research:
        needs_research.sort(key=lambda r: -int(r.get("score") or 0))
        print(f"\n{len(needs_research)} need research before drafting:\n")
        for row in needs_research:
            missing = []
            if not row.get("contact_email"):
                missing.append("email")
            if not row.get("play"):
                missing.append("play")
            if not row.get("observation"):
                missing.append("observation")
            gap = f"missing {', '.join(missing)}" if missing else row.get("status", "")
            print(f"  {int(row.get('score') or 0):>3}  {row['company']:<20} {gap}")
    return 0


def cmd_touched(args):
    rows = read_targets()
    row = find(rows, args.company)
    if not row:
        print(f"not found: {args.company}")
        return 1

    stamp = today()
    row["last_touch"] = stamp.isoformat()
    row["touch_num"] = str(args.touch)
    row["play"] = str(args.play)
    if args.touch < MAX_TOUCH:
        offset = CADENCE[args.touch + 1] - CADENCE[args.touch]
        row["next_touch"] = (stamp + dt.timedelta(days=offset)).isoformat()
        row["status"] = "sequenced"
    else:
        row["next_touch"] = ""
        row["status"] = "dead"
    write_targets(rows)

    with TOUCHES.open("a", newline="", encoding="utf-8") as fh:
        csv.DictWriter(fh, fieldnames=TOUCH_FIELDS).writerow({
            "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
            "company": args.company,
            "contact_email": row.get("contact_email", ""),
            "play": args.play,
            "touch_num": args.touch,
            "channel": args.channel,
            "subject": args.subject or "",
            "draft_id": args.draft_id or "",
        })

    nxt = row["next_touch"] or "none — sequence complete"
    print(f"logged: {args.company} play {args.play} touch {args.touch} · next: {nxt}")
    return 0


def cmd_status(args):
    rows = read_targets()
    if not rows:
        print("pipeline empty")
        return 0

    by_status, by_vertical = {}, {}
    stalled, no_email = [], []
    for row in rows:
        by_status[row.get("status", "?")] = by_status.get(row.get("status", "?"), 0) + 1
        vert = row.get("vertical") or "?"
        by_vertical[vert] = by_vertical.get(vert, 0) + 1
        if not row.get("contact_email"):
            no_email.append(row["company"])
        nxt = parse_date(row.get("next_touch"))
        if nxt and nxt < today() - dt.timedelta(days=7):
            stalled.append((row["company"], row["next_touch"]))

    print(f"PIPELINE — {len(rows)} companies\n")
    print("  by status")
    for key in sorted(by_status, key=lambda k: -by_status[k]):
        print(f"    {key:<12} {by_status[key]}")
    print("\n  by vertical")
    for key in sorted(by_vertical, key=lambda k: -by_vertical[k]):
        print(f"    {key:<12} {by_vertical[key]}")

    touch_total = 0
    if TOUCHES.exists():
        with TOUCHES.open(newline="", encoding="utf-8") as fh:
            touch_total = sum(1 for _ in csv.DictReader(fh))
    print(f"\n  touches logged: {touch_total}")

    if no_email:
        print(f"\n  MISSING EMAIL ({len(no_email)}): {', '.join(no_email[:10])}")
    if stalled:
        print(f"\n  STALLED >7 DAYS ({len(stalled)}):")
        for company, when in stalled[:10]:
            print(f"    {company} — due {when}")
    return 0


def cmd_list(args):
    rows = read_targets()
    if args.status:
        rows = [r for r in rows if r.get("status") == args.status]
    if args.vertical:
        rows = [r for r in rows if r.get("vertical") == args.vertical]
    rows.sort(key=lambda r: -int(r.get("score") or 0))
    if not rows:
        print("no matches")
        return 0
    for row in rows:
        print(
            f"  {int(row.get('score') or 0):>3}  {row.get('status', ''):<10}"
            f"  {row.get('vertical', ''):<12}  {row['company']}"
        )
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="add a scored target")
    add.add_argument("--company", required=True)
    add.add_argument("--score", type=int, required=True)
    for opt in ("domain", "vertical", "contact-name", "contact-title", "contact-email",
                "linkedin", "stage-read", "signals", "status", "observation",
                "next-touch", "notes"):
        add.add_argument(f"--{opt}")
    add.add_argument("--play", type=int)
    add.set_defaults(func=cmd_add)

    upd = sub.add_parser("update", help="update fields on an existing target")
    upd.add_argument("--company", required=True)
    for field in FIELDS:
        if field in ("company", "added"):
            continue
        upd.add_argument(f"--{field.replace('_', '-')}")
    upd.set_defaults(func=cmd_update)

    due = sub.add_parser("due", help="what needs drafting")
    due.add_argument("--days", type=int, default=0, help="look ahead N days")
    due.set_defaults(func=cmd_due)

    touched = sub.add_parser("touched", help="log a staged touch and advance the cadence")
    touched.add_argument("--company", required=True)
    touched.add_argument("--play", type=int, required=True)
    touched.add_argument("--touch", type=int, required=True, choices=[1, 2, 3, 4])
    touched.add_argument("--channel", default="email")
    touched.add_argument("--subject")
    touched.add_argument("--draft-id")
    touched.set_defaults(func=cmd_touched)

    stat = sub.add_parser("status", help="pipeline report")
    stat.set_defaults(func=cmd_status)

    lst = sub.add_parser("list", help="list targets")
    lst.add_argument("--status")
    lst.add_argument("--vertical")
    lst.set_defaults(func=cmd_list)

    args = parser.parse_args()
    ensure_files()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
