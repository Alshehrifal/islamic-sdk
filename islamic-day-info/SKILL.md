---
name: islamic-day-info
description: >
  Returns the Islamic virtues, recommended acts, and significance of a specific weekday, along
  with prayer times. Use this skill whenever the user asks about the Islamic importance or fadl
  of a day — "ما فضل يوم الجمعة؟", "what is special about Monday in Islam?",
  "فضائل يوم الاثنين", "هل ليوم الأربعاء فضل خاص؟", "Islamic significance of Thursday",
  or any query combining a day of the week with Islamic practice, sunnah acts, or recommended deeds.
---

# Islamic Day Info

Returns Hadith-backed virtues and recommended Sunnah acts for any weekday, plus prayer times.

## Script

```
islamic-day-info/scripts/day_info.py
```

## Usage

```bash
python scripts/day_info.py --city Riyadh
python scripts/day_info.py --city Cairo --country Egypt --date 25-04-2026
```

## Output fields

`city`, `country`, `gregorian`, `hijri`, `weekday_en`, `weekday_ar`,  
`virtues` (list of Hadith-backed virtues), `recommended_acts` (list),  
`prayer_times` (fajr/sunrise/dhuhr/asr/maghrib/isha)

## Day coverage

| Day       | Key virtue / act                                      |
|-----------|-------------------------------------------------------|
| Friday    | Best day; Surah Al-Kahf; du'aa hour; salah on Prophet |
| Monday    | Deeds presented; Prophet born; fasting Sunnah         |
| Thursday  | Deeds presented; fasting Sunnah                       |
| Other     | General reminder + Ayyam al-Bid fasting note          |

## Agent workflow

1. Run the script for the city/date.
2. Present `virtues` with their Hadith references.
3. List `recommended_acts` clearly.
4. Include prayer times if relevant.
5. For Friday: highlight Surah Al-Kahf, the du'aa hour (after Asr), and salah 'ala al-nabi.
