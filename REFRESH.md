# Refresh procedure

Instructions for the monthly refresh (run by Claude as a scheduled task, or on request). The goal is to keep `headwear-events.ics` accurate for an analyst covering intelligent headwear: AI glasses, smart glasses, XR glasses and VR/MR/XR headsets.

## Files

- `events.json`: items that appear in the calendar. Each has a stable `id` (never change it; Outlook uses it to update events in place), `status`, `start`/`end` (inclusive, all-day), `notes`, `sources`, `updated` (date last checked) and an optional `sequence`.
- `tracker.json`: items without a firm date (`kind` is `launch` or `event`), plus the `changelog`.
- `build.py`: rebuilds `headwear-events.ics` and `README.md`. Run `python3 build.py` (needs `pip install icalendar`).

## Status rules

- **Confirmed**: the organiser or company has stated the date.
- **Expected**: credible reporting, partner statements or third-party listings, not yet confirmed by the company; also use when a source needs checking.
- **Rumoured**: analyst or press reporting only.
- **TBA**: placeholder on the 1st of the expected month for a major recurring event whose dates aren't out yet. Keep these to the biggest events (Google I/O, WWDC, Meta Connect); everything else waits in the tracker.

## Each refresh

1. Re-check every item in `events.json` and `tracker.json` against current sources. Look first at official organiser and company pages, then at reputable trade press (Road to VR, UploadVR, The Verge, Engadget, Bloomberg, Reuters and the like).
2. Search for new launches, confirmed or speculated, and for newly announced event dates. Cover Meta, Google/Samsung (Android XR), Apple, Snap, XREAL, Amazon, Pico/ByteDance, Valve, Sony, Xiaomi, Alibaba, Rokid, RayNeo, Huawei, Even Realities, Vuzix and other eyewear brands (EssilorLuxottica, Warby Parker, Gentle Monster, Kering). Also cover events where these companies make announcements.
3. When a tracker item gets a firm date, move it into `events.json`. When a TBA placeholder gets real dates, replace its dates, title and status but keep the same `id`.
4. For any changed calendar item, set `updated` to today and increment `sequence`. For items you re-checked with no change, set `updated` to today.
5. Leave past events in the calendar for three months after they end, then remove them and note it in the changelog.
6. Use only figures and dates from sources you have read. If sources conflict, say so in the notes and use Expected. Never invent a date to fill a gap.
7. Set `last_checked` in `events.json` to today, add a dated `changelog` entry in `tracker.json` summarising what changed, and run `python3 build.py`.
8. Validate: the .ics must parse with `icalendar`, every UID must be unique, and every all-day event must have the correct length.
9. Commit and push to `main`, then confirm the raw file URL serves the new version:
   `https://raw.githubusercontent.com/GioKinto/headwear-calendar/main/headwear-events.ics`
10. Send Gio a short summary: what was added, moved, changed or removed, and anything that needs a human check.

## Writing style for notes

Plain, professional analyst prose. Name the source of each claim (for example, "per Bloomberg's Mark Gurman"). No hype words, and use em-dashes rarely.
