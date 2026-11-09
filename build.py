"""Build headwear-events.ics and README.md from events.json and tracker.json.

Run: python3 build.py
"""
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from icalendar import Calendar, Event

HERE = Path(__file__).parent
UID_DOMAIN = "headwear-calendar"


def build_ics(data):
    cal = Calendar()
    cal.add("prodid", "-//Headwear Calendar//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", data["calendar_name"])
    cal.add(
        "x-wr-caldesc",
        "Industry events and product launch dates for AI glasses and XR headwear. "
        f"Last checked {data['last_checked']}. Status tags: Confirmed, Expected, Rumoured, TBA.",
    )
    cal.add("refresh-interval", timedelta(hours=12), parameters={"VALUE": "DURATION"})
    cal.add("x-published-ttl", "PT12H")

    stamp = datetime.now(timezone.utc).replace(microsecond=0)
    for it in data["items"]:
        ev = Event()
        ev.add("uid", f"{it['id']}@{UID_DOMAIN}")
        ev.add("summary", f"[{it['status']}] {it['title']}")
        start = date.fromisoformat(it["start"])
        end = date.fromisoformat(it["end"]) + timedelta(days=1)  # DTEND is exclusive
        ev.add("dtstart", start)
        ev.add("dtend", end)
        ev.add("dtstamp", stamp)
        upd = date.fromisoformat(it["updated"])
        ev.add("last-modified", datetime(upd.year, upd.month, upd.day, tzinfo=timezone.utc))
        ev.add("sequence", it.get("sequence", 0))
        if it.get("location"):
            ev.add("location", it["location"])
        desc = [
            f"Status: {it['status']}",
            f"Type: {it['type']}",
            "",
            it["notes"],
            "",
            "Sources:",
            *[f"- {u}" for u in it["sources"]],
            "",
            f"Last checked: {data['last_checked']}",
        ]
        ev.add("description", "\n".join(desc))
        ev.add("categories", [it["type"].capitalize()])
        ev.add("transp", "TRANSPARENT")
        ev.add("x-microsoft-cdo-busystatus", "FREE")
        ev.add("x-microsoft-cdo-alldayevent", "TRUE")
        cal.add_component(ev)
    return cal.to_ical()


def build_readme(data, tracker):
    def fmt(d):
        return date.fromisoformat(d).strftime("%-d %b %Y")

    def cell(s):
        return (s or "").replace("|", "\\|")

    lines = [
        f"# {data['calendar_name']}",
        "",
        "Subscribe to `headwear-events.ics` from this repo in Outlook (Add calendar > Subscribe from web). "
        "Everything in the calendar is all-day and shows as Free, so it never blocks availability.",
        "",
        f"Last checked: {fmt(data['last_checked'])}",
        "",
        "Status tags: **Confirmed** (organiser or company has said so), **Expected** (reported or "
        "partner-sourced but not confirmed by the company, or a source needs checking), **Rumoured** "
        "(analyst or press reporting only), **TBA** (placeholder on the 1st of the expected month).",
        "",
        "## In the calendar",
        "",
        "| Dates | Status | Item | Where |",
        "|---|---|---|---|",
    ]
    for it in sorted(data["items"], key=lambda x: x["start"]):
        dates = fmt(it["start"]) if it["start"] == it["end"] else f"{fmt(it['start'])} to {fmt(it['end'])}"
        if it["status"] == "TBA":
            dates = date.fromisoformat(it["start"]).strftime("%b %Y") + " (TBA)"
        lines.append(f"| {dates} | {it['status']} | [{cell(it['title'])}]({it['sources'][0]}) | {cell(it.get('location'))} |")

    lines += ["", "## Tracker (no firm date yet, so not in the calendar)", "", tracker["note"], "",
              "| Item | Status | Window | Detail |", "|---|---|---|---|"]
    for t in tracker["items"]:
        lines.append(f"| [{cell(t['name'])}]({t['sources'][0]}) | {t['status']} | {cell(t['window'])} | {cell(t['detail'])} |")

    lines += ["", "## Change log", ""]
    for c in tracker["changelog"]:
        lines.append(f"- **{fmt(c['date'])}**: {c['entry']}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    data = json.loads((HERE / "events.json").read_text())
    tracker = json.loads((HERE / "tracker.json").read_text())
    (HERE / "headwear-events.ics").write_bytes(build_ics(data))
    (HERE / "README.md").write_text(build_readme(data, tracker))
    print(f"Built {len(data['items'])} calendar entries, {len(tracker['items'])} tracker items.")
