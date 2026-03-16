---
name: islamic-prayer-times
description: >
  Get Islamic prayer times (Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha, Midnight) for any city
  and country worldwide. Use this skill whenever the user asks: "متى أذان المغرب؟", "what time is
  Fajr in London?", "prayer times for Tokyo", "صلاة العشاء في دبي", or any query about salah /
  prayer schedule — even if phrased casually like "when does Maghrib start?". Also use for
  tomorrow's or a specific date's prayer times.
---

# Islamic Prayer Times

Returns accurate prayer times via the Aladhan API with the correct calculation method for the country.

## Script

```
islamic-prayer-times/scripts/prayer_times.py
```

## Usage

```bash
python scripts/prayer_times.py --city Riyadh
python scripts/prayer_times.py --city London --country "United Kingdom"
python scripts/prayer_times.py --city Istanbul --country Turkey --date 25-03-2026
```

| Argument    | Required | Notes                          |
|-------------|----------|--------------------------------|
| `--city`    | ✅        | Any city name in English       |
| `--country` | optional | Defaults to Saudi Arabia       |
| `--date`    | optional | DD-MM-YYYY; defaults to today  |

## Output fields

`city`, `country`, `gregorian`, `hijri`, `weekday_en`, `weekday_ar`,  
`fajr`, `sunrise`, `dhuhr`, `asr`, `maghrib`, `isha`, `midnight`,  
`method`, `timezone`

## Agent workflow

1. Run the script with the requested city/country/date.
2. If the user asked for a specific prayer only (e.g. "متى المغرب؟"), reply with just that prayer + city + Hijri date.
3. If all times were requested, present a clean table.
4. Always mention the Hijri date alongside the Gregorian one.

## Calculation methods by country

| Region / Country          | Method                      |
|---------------------------|-----------------------------|
| Saudi Arabia, Gulf states | Umm al-Qura (method 4)      |
| Egypt                     | Egyptian General Auth (5)   |
| Pakistan                  | Karachi (1)                 |
| Turkey                    | Diyanet (13)                |
| France                    | Union des Mosquées (12)     |
| Others                    | Muslim World League (3)     |
