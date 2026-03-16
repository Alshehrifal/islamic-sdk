---
name: islamic-eid
description: >
  Get the Eid al-Fitr or Eid al-Adha date and estimated prayer time for any city, hilal-aware.
  Use this skill whenever the user asks: "متى صلاة عيد الفطر في الرياض؟",
  "Eid al-Adha prayer time in Cairo 2026", "كم باقي على العيد في تركيا؟",
  "when is Eid in London?", "موعد صلاة العيد", "متى العيد الكبير في مصر؟",
  or any question about Eid date, Eid prayer time, or days remaining until Eid —
  for any city or country worldwide.
---

# Islamic Eid Prayer Times

Returns hilal-aware Eid date (announced if found, otherwise calculated) and estimated prayer time for any city.

## Script

```
islamic-eid/scripts/eid.py
```

## Usage

```bash
python scripts/eid.py --city Riyadh --eid fitr
python scripts/eid.py --city Damascus --country Syria --eid fitr --year 2026
python scripts/eid.py --city Cairo --country Egypt --eid adha
python scripts/eid.py --city Istanbul --country Turkey --eid adha
```

| Argument    | Required | Values            |
|-------------|----------|-------------------|
| `--city`    | ✅        |                   |
| `--country` | optional | Defaults to Saudi Arabia |
| `--eid`     | ✅        | `fitr` or `adha`  |
| `--year`    | optional | Gregorian year    |

## Output fields

`city`, `country`, `eid`, `eid_ar`,  
`calculated_date`, `announced_date` (or null), `date_used`, `date_status`,  
`estimated_prayer_time` ← **Sunrise + 15 min**,  
`prayer_basis` (explains the estimate),  
`supporting_news`,  
`announcement_source`, `announcement_link` (when found)

## Agent workflow

1. Run `eid.py` for the requested city/eid/country.
2. Check `date_status`:
   - `"announced"` → state confirmed date + source.
   - `"calculated..."` → clearly label as **estimated**, not yet confirmed for that country.
3. Present `estimated_prayer_time` as an approximation — always tell user to verify with local mosque.
4. Note that different countries may observe Eid on different days.

## Prayer time estimation

Eid prayer is typically performed shortly after sunrise. This skill estimates:  
**Eid prayer ≈ Sunrise + 15 minutes**  
⚠️ Always verify with the local mosque or official Islamic authority.
