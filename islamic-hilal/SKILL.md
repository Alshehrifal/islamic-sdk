---
name: islamic-hilal
description: >
  Check the hilal (crescent moon) sighting and announced start date of any Hijri month for any
  country. Use this skill whenever the user asks: "هل رأت السعودية هلال شوال؟",
  "when does Ramadan start in Morocco 2026?", "متى بداية ذي الحجة في سوريا؟",
  "did Turkey announce the Muharram hilal?", "هلال رمضان 1447 في مصر", or any query
  about moon sighting, hilal announcement, or Hijri month start date for a specific country.
  Always compare calculated (Umm al-Qura) vs. officially announced dates.
---

# Islamic Hilal — Moon Sighting & Month Start

Compares the calculated Umm al-Qura start date with the officially announced date (from news search) for any Hijri month and country.

## Script

```
islamic-hilal/scripts/hilal.py
```

## Usage

```bash
python scripts/hilal.py --country "Saudi Arabia" --month shawwal
python scripts/hilal.py --country Syria --month ramadan
python scripts/hilal.py --country Morocco --month dhulhijja --year 2026
python scripts/hilal.py --country Turkey --month muharram
```

## Valid month keys

`muharram` · `safar` · `rabiulawal` · `rabiulakhir` · `jumadalawal` · `jumadalakhir`  
`rajab` · `shaban` · `ramadan` · `shawwal` · `dhulqada` · `dhulhijja`

## Output fields

`country`, `month`, `month_ar`, `hijri_year`,  
`calculated_start_gregorian` — Umm al-Qura calculation,  
`hilal_eve_gregorian` — 29th of the previous month (night of sighting),  
`announced_start_gregorian` — from news (or `null`),  
`date_used`, `date_status` (`"announced"` or `"calculated (Umm al-Qura — unconfirmed)"`),  
`moon_sighting_news` — top news snippets,  
`announcement_source`, `announcement_link` — when found

## Agent workflow

1. Run the script for the requested country and month.
2. Check `date_status`:
   - `"announced"` → present as confirmed, cite `announcement_source`.
   - `"calculated..."` → clearly say the date is **estimated** and the official announcement has not been found.
3. Explain that different countries can have different Eid/Ramadan dates due to local hilal sighting.
4. Never present a calculated date as an official announcement.

## Key principle

> Different countries sight the hilal independently. Saudi Arabia may declare Eid on Wednesday while Syria declares it on Thursday. Always check `date_status`.
