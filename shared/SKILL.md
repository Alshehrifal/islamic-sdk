---
name: islamic-shared
description: >
  Shared utility library for the Islamic SDK. Provides: Aladhan API prayer-time fetching
  (prayer_api), bidirectional Hijri↔Gregorian calendar conversion (hijri_utils), and
  Google News RSS search + webpage reading (news_utils). This is an internal dependency
  — it is not invoked directly by users. Other Islamic skills (islamic-prayer-times,
  islamic-eid, islamic-hilal, etc.) import from this package automatically.
---

# Islamic Shared Utilities

Internal library used by all Islamic SDK skills. Install path: `islamic-sdk/shared/`.

## Modules

### `prayer_api.py`
- `fetch_prayer_times(city, country, date_str, method)` → Aladhan API data dict
- `get_method(country)` → correct calculation method integer for country
- `parse_date_arg(date_str)` → normalised DD-MM-YYYY string

### `hijri_utils.py`
- `gregorian_to_hijri(day, month, year)` → hijri dict
- `hijri_to_gregorian(day, month, year)` → gregorian dict
- `month_key_to_number(key)` → int (e.g. `"shawwal"` → `10`)
- `hijri_month_start_gregorian(month, year)` → DD-MM-YYYY string
- `current_hijri_year()` → int
- `HIJRI_MONTHS`, `HIJRI_MONTH_AR` — lookup dicts

### `news_utils.py`
- `search_news(query, max_results, site)` → `[{title, link, snippet, published}]`
- `read_webpage(url, max_chars)` → plain-text string
- `extract_announced_date(news_results, keywords)` → `{date_str, source_title, source_link}` or `None`

## Dependency
```bash
pip install hijridate --break-system-packages
```
(auto-installed on first import of `hijri_utils`)

## Usage in skills
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from prayer_api import fetch_prayer_times, parse_date_arg
from hijri_utils import gregorian_to_hijri, current_hijri_year
from news_utils   import search_news, extract_announced_date
```
