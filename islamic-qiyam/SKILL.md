---
name: islamic-qiyam
description: >
  Calculates the last third of the night — the optimal window for Qiyam al-Layl and Tahajjud prayer.
  Use this skill whenever the user asks: "متى يبدأ وقت القيام الليلة؟", "What time is Tahajjud in
  Makkah?", "وقت الثلث الأخير من الليل في جدة", "when should I wake up for Qiyam?",
  "best time for night prayer in [city]", or any question about Qiyam, Tahajjud, or the last third
  of the night for any city worldwide.
---

# Islamic Qiyam al-Layl Calculator

Calculates the start of the last third of the night (from Maghrib to Fajr) — the best time for voluntary night prayer, du'aa, and seeking forgiveness.

## Script

```
islamic-qiyam/scripts/qiyam.py
```

## Usage

```bash
python scripts/qiyam.py --city Riyadh
python scripts/qiyam.py --city Istanbul --country Turkey
python scripts/qiyam.py --city "Kuala Lumpur" --country Malaysia --date 01-04-2026
```

## Output fields

`city`, `country`, `date`,  
`maghrib`, `isha`, `fajr_next_day`,  
`night_duration_minutes`,  
`last_third_starts` ← **the key field**,  
`last_third_ends_at_fajr`,  
`note` (Arabic summary)

## Calculation method

Night duration = Fajr (next day) − Maghrib (today)  
Last third starts at: Maghrib + ⌊2/3 × night duration⌋

## Agent workflow

1. Run the script for the requested city and date.
2. Report `last_third_starts` prominently — this is when to wake up.
3. Also give `last_third_ends_at_fajr` as the deadline.
4. Remind the user this is the best time for du'aa, istighfar, and voluntary prayer (2 rak'ahs at a time).
5. Mention: "يَنْزِلُ رَبُّنَا إِلَى السَّمَاءِ الدُّنْيَا كُلَّ لَيْلَةٍ حِينَ يَبْقَى ثُلُثُ اللَّيْلِ الآخِرُ." (البخاري، مسلم)
