---
name: islamic-next-events
description: >
  Get all upcoming major Islamic events (Eid al-Fitr, Yawm Arafah, Eid al-Adha) sorted by date
  with days remaining. Use this skill whenever the user asks: "ما هي المناسبات الإسلامية القادمة؟",
  "show me the next Eid and Arafah dates", "كم باقي على العيد والحج؟",
  "what Islamic events are coming up?", "next Eid date for [city]",
  "upcoming Islamic occasions 2026", or any request for a combined overview of upcoming
  Islamic holidays or events for any city/country.
---

# Islamic Next Events — Upcoming Calendar

Returns the next Yawm Arafah, Eid al-Fitr, and Eid al-Adha sorted by how soon they arrive, with days remaining.

## Script

```
islamic-next-events/scripts/next_events.py
```

**Dependency:** Calls `islamic-eid` and `islamic-arafah` scripts internally.

## Usage

```bash
python scripts/next_events.py --city Riyadh
python scripts/next_events.py --city "Kuala Lumpur" --country Malaysia
python scripts/next_events.py --city Istanbul --country Turkey
```

## Output fields

`city`, `country`, `today`,  
`events` — sorted list, each entry contains:
- `event` (English name)
- `event_ar` (Arabic name)
- `date` (DD-MM-YYYY)
- `date_status` (`"announced"` or `"calculated..."`)
- `days_until` (integer — 0 means today)
- `prayer_time` or `fasting_virtue` (event-specific)

## Agent workflow

1. Run the script for the city/country.
2. Present results as a clean table sorted by date:

```
Eid al-Fitr        20-03-2026   5 days
Yawm Arafah        26-05-2026  72 days
Eid al-Adha        27-05-2026  73 days
```

3. For each event, note `date_status` — if unconfirmed, mention it's estimated.
4. For Arafah, add the fasting reminder (expiates 2 years).
5. For Eid, note that prayer time is estimated (Sunrise + 15 min).
