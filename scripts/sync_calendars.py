#!/usr/bin/env python3
"""Pull published calendar feeds (.ics) into the weekday planner.

Reads the planner's calendar list (the `config/calendars` document), fetches each
feed, expands recurring events, and writes one document per calendar per week to
the planner's `events` collection, plus a `config/calsync` status document.

The output is a JSON array of writes in the shape the ArtifactData `batch`
action takes, so a scheduled Claude session can apply it in one call:

    python3 scripts/sync_calendars.py --config calendars.json --out writes.json

Feed URLs are secrets (anyone holding one can read that calendar). They live only
in the planner's private database, never in this repo.

Requires: pip install icalendar recurring-ical-events
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.request
from zoneinfo import ZoneInfo

import icalendar
import recurring_ical_events

LOCAL = ZoneInfo("America/New_York")
UA = "Mozilla/5.0 (compatible; CariettiPlanner/1.0)"


def load_calendars(path: str) -> list[dict]:
    with open(path) as f:
        doc = json.load(f)
    # Accept the bare document, or an ArtifactData read that wraps it in {"data": ...}
    if isinstance(doc, dict) and "data" in doc and "list" not in doc:
        doc = doc["data"]
    return [c for c in doc.get("list", []) if c.get("url") and c.get("id")]


def fetch(url: str) -> bytes:
    if url.startswith("webcal://"):
        url = "https://" + url[len("webcal://"):]
    # A published Outlook link ends in calendar.html; the feed sits beside it.
    if url.endswith("/calendar.html"):
        url = url[: -len("calendar.html")] + "reachcalendar.ics"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def monday_of(d: dt.date) -> dt.date:
    return d - dt.timedelta(days=d.weekday())


def to_local(v) -> tuple[dt.datetime | None, dt.date]:
    """Return (local datetime or None for all-day, local date)."""
    if isinstance(v, dt.datetime):
        if v.tzinfo is None:
            v = v.replace(tzinfo=LOCAL)
        v = v.astimezone(LOCAL)
        return v, v.date()
    return None, v


def expand(ics: bytes, start: dt.date, end: dt.date) -> list[dict]:
    cal = icalendar.Calendar.from_ical(ics)
    out = []
    for ev in recurring_ical_events.of(cal, skip_bad_series=True).between(start, end + dt.timedelta(days=1)):
        if str(ev.get("STATUS", "")).upper() == "CANCELLED":
            continue
        title = str(ev.get("SUMMARY", "") or "Busy").strip() or "Busy"
        s_dt, s_day = to_local(ev.decoded("DTSTART"))
        e_raw = ev.decoded("DTEND") if ev.get("DTEND") else None
        if e_raw is None:
            dur = ev.decoded("DURATION") if ev.get("DURATION") else dt.timedelta(minutes=30 if s_dt else 0)
            e_raw = (s_dt or s_day) + dur
        e_dt, e_day = to_local(e_raw)
        free = str(ev.get("TRANSP", "")).upper() == "TRANSPARENT"
        uid = str(ev.get("UID", ""))[:120]
        loc = str(ev.get("LOCATION", "") or "").strip()[:120]

        if s_dt is None:  # all-day: DTEND is exclusive
            last = (e_day - dt.timedelta(days=1)) if e_day > s_day else s_day
            day = s_day
            while day <= last:
                if start <= day <= end and day.weekday() < 5:
                    out.append({"uid": uid, "title": title, "date": day.isoformat(), "start": "", "end": "", "allDay": True, "free": free})
                day += dt.timedelta(days=1)
            continue

        # Timed: split across days so each weekday gets its own block
        day = s_day
        while day <= e_day:
            if start <= day <= end and day.weekday() < 5:
                a = s_dt if day == s_day else dt.datetime.combine(day, dt.time(0, 0), LOCAL)
                b = e_dt if day == e_day else dt.datetime.combine(day, dt.time(23, 59), LOCAL)
                if b > a:
                    out.append({"uid": uid, "title": title, "date": day.isoformat(), "start": a.strftime("%H:%M"), "end": b.strftime("%H:%M"),
                                "allDay": False, "free": free, **({"location": loc} if loc else {})})
            day += dt.timedelta(days=1)
    out.sort(key=lambda x: (x["date"], x["start"] or "00:00", x["title"]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="JSON of the config/calendars document")
    ap.add_argument("--out", required=True, help="where to write the ArtifactData batch writes")
    ap.add_argument("--ics", action="append", default=[], metavar="ID=FILE", help="read a local .ics for a calendar id instead of fetching (testing)")
    ap.add_argument("--weeks-back", type=int, default=1)
    ap.add_argument("--weeks-ahead", type=int, default=4)
    ap.add_argument("--today", help="override today (YYYY-MM-DD), for testing")
    args = ap.parse_args()

    local_files = dict(x.split("=", 1) for x in args.ics)
    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(LOCAL).date()
    first = monday_of(today) - dt.timedelta(weeks=args.weeks_back)
    weeks = [first + dt.timedelta(weeks=i) for i in range(args.weeks_back + args.weeks_ahead + 1)]
    last = weeks[-1] + dt.timedelta(days=4)
    now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)

    writes, status = [], {}
    for cal in load_calendars(args.config):
        cid = cal["id"]
        try:
            raw = open(local_files[cid], "rb").read() if cid in local_files else fetch(cal["url"])
            events = expand(raw, first, last)
        except Exception as e:  # keep the last good copy in the planner; report the failure
            status[cid] = {"ok": False, "error": f"{type(e).__name__}: {e}"[:300], "label": cal.get("label", cid)}
            print(f"{cid}: FAILED {e}", file=sys.stderr)
            continue
        for wk in weeks:
            wk_end = wk + dt.timedelta(days=4)
            items = [e for e in events if wk.isoformat() <= e["date"] <= wk_end.isoformat()]
            writes.append({"op": "set", "collection": "events", "doc_id": f"{cid}--{wk.isoformat()}", "data": {
                "calendar": cid, "label": cal.get("label", cid), "company": cal.get("company", ""),
                "week": wk.isoformat(), "events": items, "syncedAt": now_ms}})
        status[cid] = {"ok": True, "events": len(events), "label": cal.get("label", cid)}
        print(f"{cid}: {len(events)} events from {first} to {last}", file=sys.stderr)

    writes.append({"op": "set", "collection": "config", "doc_id": "calsync", "data": {"at": now_ms, "calendars": status}})
    with open(args.out, "w") as f:
        json.dump(writes, f, indent=1)
    print(f"wrote {len(writes)} writes to {args.out}", file=sys.stderr)
    return 0 if all(s["ok"] for s in status.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
