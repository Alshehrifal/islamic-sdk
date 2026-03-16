<div align="center">

<img src="docs/assets/logo.svg" width="160" alt="Islamic SDK Logo" />

# Islamic SDK

**A modular Claude skill collection for Islamic calendar, prayer times, moon sighting & religious occasions**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-62%20passing-2e7d32?style=flat-square&logo=pytest&logoColor=white)](./run_tests.py)
[![Skills](https://img.shields.io/badge/Skills-10%20modules-d4a843?style=flat-square)](./README.md#skills)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](./LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Docs-Live-4CAF50?style=flat-square&logo=github)](https://alshas0e.github.io/islamic-sdk)

*Works for any city · Any country · Arabic & English*

[**Live Demo**](https://alshas0e.github.io/islamic-sdk) · [**Skills Reference**](#skills) · [**Quick Start**](#quick-start) · [**Contributing**](CONTRIBUTING.md)

</div>

---

## What is this?

Islamic SDK is a collection of 10 focused Claude skills that give AI assistants deep, accurate Islamic calendar and prayer knowledge — for any city in the world.

Each skill is **hilal-aware**: it searches for official moon sighting announcements per country before falling back to calculated (Umm al-Qura) dates, and always makes clear whether a date is confirmed or estimated.

```
User: "متى صلاة الفجر في مكة المكرمة اليوم؟"
User: "When is Eid al-Adha in Istanbul this year?"
User: "Should I fast on Arafah? What date is it?"
User: "هل أُعلن هلال شوال في المغرب؟"
```

---

## Skills

| Skill | Description | Example triggers |
|-------|-------------|-----------------|
| 🕌 **islamic-prayer-times** | Daily salah schedule for any city | "prayer times Cairo", "متى المغرب في جدة؟" |
| 📖 **islamic-day-info** | Islamic significance of each weekday | "فضائل يوم الجمعة", "what's special about Monday?" |
| 🌙 **islamic-qiyam** | Last-third-of-night (Tahajjud) window | "Tahajjud time tonight", "متى وقت القيام؟" |
| 📅 **islamic-hijri** | Gregorian ↔ Hijri conversion | "convert March 20 to Hijri", "1 شوال 1447 ميلادي؟" |
| 🌙 **islamic-hilal** | Moon sighting & month start per country | "did Morocco sight the hilal?", "هلال رمضان في سوريا" |
| 🎉 **islamic-eid** | Eid date + prayer time, hilal-aware | "Eid date Turkey", "متى صلاة العيد في الرياض؟" |
| 🕋 **islamic-arafah** | Yawm Arafah + fasting virtue | "when is Arafah?", "فضل صيام يوم عرفة" |
| 📿 **islamic-ashura** | Ashura + Tasu'a dates | "Ashura 2026", "متى عاشوراء 1447؟" |
| 📆 **islamic-next-events** | Upcoming Islamic events dashboard | "next Eid and Arafah", "المناسبات القادمة" |
| 🗞️ **islamic-news** | Islamic news search + web reader | "search for Eid announcement", "هلال شوال الأخبار" |

---

## Quick Start

### Install a skill

Download the `.skill` files from [Releases](https://github.com/alshas0e/islamic-sdk/releases) and upload via the Claude skill manager.

The `shared.skill` package must be installed alongside the other skills — it provides the shared calendar, API, and news utilities all skills depend on.

### Run a script directly

```bash
# Install the one dependency
pip install hijridate

# Prayer times
python islamic-prayer-times/scripts/prayer_times.py --city Riyadh

# Hijri conversion
python islamic-hijri/scripts/hijri.py --date 20-03-2026

# Eid date for your city
python islamic-eid/scripts/eid.py --city Istanbul --country Turkey --eid fitr

# Upcoming events
python islamic-next-events/scripts/next_events.py --city London --country "United Kingdom"

# Check hilal
python islamic-hilal/scripts/hilal.py --country Morocco --month ramadan
```

### Run the tests

```bash
# Unit tests — always run offline
python run_tests.py

# Full integration tests (requires internet: aladhan.com + Google News)
ISLAMIC_INTEGRATION_TESTS=1 python run_tests.py

# Single skill
python run_tests.py --skill hijri
```

---

## Architecture

```
islamic-sdk/
├── shared/                   ← shared utilities (auto-imported)
│   ├── prayer_api.py         ← Aladhan API wrapper
│   ├── hijri_utils.py        ← Hijri↔Gregorian (hijridate)
│   └── news_utils.py         ← Google News RSS + web reader
│
├── islamic-prayer-times/     ── scripts/ ── tests/
├── islamic-day-info/         ── scripts/ ── tests/
├── islamic-qiyam/            ── scripts/ ── tests/
├── islamic-hijri/            ── scripts/ ── tests/
├── islamic-hilal/            ── scripts/ ── tests/
├── islamic-eid/              ── scripts/ ── tests/
├── islamic-arafah/           ── scripts/ ── tests/
├── islamic-ashura/           ── scripts/ ── tests/
├── islamic-next-events/      ── scripts/ ── tests/
├── islamic-news/             ── scripts/ ── tests/
│
└── run_tests.py              ← master test runner
```

Each skill is **self-contained**: its own `SKILL.md` (trigger description), `scripts/` (executable logic), and `tests/` (unit + integration tests).

---

## Design Principles

### 1. Hilal-aware dates
Eid, Ramadan, and Ashura depend on actual moon sighting. Every skill that involves a Hijri month start:
- Returns the **calculated** date (Umm al-Qura)
- Searches Google News for the **officially announced** date per country
- Sets `date_status` = `"announced"` or `"calculated (Umm al-Qura — unconfirmed)"`

```json
{
  "date_used": "20-03-2026",
  "date_status": "announced",
  "announcement_source": "الرئاسة العامة لشؤون المسجد الحرام",
  "announcement_link": "https://spa.gov.sa/..."
}
```

### 2. Never present unconfirmed dates as official
If no announcement is found, the agent workflow clearly labels the result as *estimated*. Claude checks `date_status` before presenting any date.

### 3. Arafah always follows Saudi Arabia
Hajj is performed in Mecca. Therefore Yawm Arafah is always determined by Saudi Arabia's Dhul Hijjah announcement, regardless of the user's country.

### 4. Shared utilities — DRY
All API calls, Hijri math, and news scraping live in `shared/`. No duplication across skills.

---

## API Dependencies

| Service | Domain | Used by |
|---------|--------|---------|
| Aladhan Prayer Times API | `api.aladhan.com` | prayer-times, qiyam, eid, arafah, ashura |
| Google News RSS | `news.google.com` | hilal, eid, arafah, ashura, news |

Both are free and require no API key.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

---

## License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

Made with ☾ for the global Muslim community

*اللَّهُمَّ بَارِكْ لَنَا فِي رَجَبَ وَشَعْبَانَ وَبَلِّغْنَا رَمَضَانَ*

</div>
