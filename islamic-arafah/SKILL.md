---
name: islamic-arafah
description: >
  Get Yawm Arafah (9th Dhul Hijjah) date and prayer times, with fasting virtue.
  Use this skill whenever the user asks: "متى يوم عرفة 2026؟", "When is Yawm Arafah?",
  "should I fast on Arafah?", "يوم عرفة 1447 كم يوافق ميلادي؟",
  "what date is Arafah this year?", "فضل صيام يوم عرفة", or any question about
  Yawm Arafah, the 9th of Dhul Hijjah, or fasting on Arafah.
  Note: Arafah ALWAYS follows Saudi Arabia's Dhul Hijjah announcement regardless of the user's country.
---

# Yawm Arafah — 9th Dhul Hijjah

Returns the date of Yawm Arafah with prayer times and the fasting virtue. Always uses Saudi Arabia's Dhul Hijjah announcement (Hajj is in Mecca).

## Script

```
islamic-arafah/scripts/arafah.py
```

## Usage

```bash
python scripts/arafah.py --city Riyadh
python scripts/arafah.py --city Jakarta --country Indonesia
python scripts/arafah.py --city London --country "United Kingdom" --year 2026
```

## Output fields

`city`, `country`, `event`, `event_ar`, `hijri_date`,  
`calculated_date`, `announced_date` (or null), `date_used`, `date_status`,  
`weekday_en`, `weekday_ar`,  
`fasting_virtue`, `note`,  
`prayer_times` (fajr/dhuhr/asr/maghrib/isha for that city on Arafah day),  
`announcement_source`, `announcement_link` (when found)

## Agent workflow

1. Run the script for the requested city/country.
2. State the date clearly with `date_status`.
3. Present the fasting virtue:
   > "صيام يوم عرفة يُكفِّر سنتين: الماضية والقادمة." (مسلم 1162)
4. **Only for non-pilgrims** — remind the user that pilgrims performing Hajj do NOT fast on Arafah.
5. Note that the date always follows Saudi Arabia regardless of the user's country.

## Why Saudi Arabia?

Hajj takes place in Mecca. Therefore Yawm Arafah is determined by Saudi Arabia's Dhul Hijjah hilal announcement, not local moon sighting.
