---
name: islamic-ashura
description: >
  Get Yawm Ashura (10th Muharram) and Tasu'a (9th Muharram) dates, fasting virtue, and prayer times.
  Use this skill whenever the user asks: "متى يوم عاشوراء 2026؟", "When is Ashura?",
  "فضل صيام عاشوراء", "should I fast on Ashura?", "متى صيام تاسوعاء وعاشوراء؟",
  "Ashura date in Turkey", "10th Muharram 1447", or any question about Yawm Ashura,
  Tasu'a (9th Muharram), or fasting in Muharram.
---

# Yawm Ashura — 10th Muharram

Returns Ashura and Tasu'a dates (country-specific hilal), fasting virtue, and prayer times.

## Script

```
islamic-ashura/scripts/ashura.py
```

## Usage

```bash
python scripts/ashura.py --city Riyadh
python scripts/ashura.py --city Damascus --country Syria --year 2026
python scripts/ashura.py --city London --country "United Kingdom"
python scripts/ashura.py --city Ankara --country Turkey
```

## Output fields

`city`, `country`, `event`, `event_ar`, `hijri_date`,  
`calculated_ashura`, `calculated_tasua`,  
`announced_date` (or null), `announced_tasua` (or null),  
`date_used`, `date_status`, `tasu_a_date`,  
`weekday_en`, `weekday_ar`,  
`fasting_virtue`, `tasua_note`, `note`,  
`prayer_times`,  
`announcement_source`, `announcement_link` (when found)

## Agent workflow

1. Run the script for the requested city/country.
2. Report `date_used` as the Ashura date (10th Muharram).
3. Report `tasu_a_date` as the recommended Tasu'a fast (9th Muharram).
4. Present the fasting virtues:
   - **Ashura:** Expiates the previous year's sins. (Muslim 1162)
   - **Tasu'a:** Recommended to differ from Jewish practice. (Muslim 1134)
5. Recommend fasting **both days** (9th + 10th).
6. Check `date_status` — if unconfirmed, note the date may differ by country.

## Key distinction from Arafah

Unlike Arafah (which always follows Saudi Arabia), Ashura follows the **country's own Muharram hilal announcement**. Different countries may observe it on different days.
