#!/usr/bin/env python3
"""
islamic-eid/scripts/eid.py
Eid prayer time — hilal-aware.

Usage:
  python eid.py --city Riyadh --eid fitr
  python eid.py --city Damascus --country Syria --eid fitr --year 2026
  python eid.py --city Cairo --country Egypt --eid adha
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from hijri_utils import (
    current_hijri_year, hijri_month_start_gregorian,
    month_key_to_number, HIJRI_MONTH_AR,
)
from prayer_api import fetch_prayer_times, parse_date_arg
from news_utils import search_news, extract_announced_date
from datetime import datetime


EID_CONFIG = {
    "fitr": {
        "month":    "shawwal",
        "month_num": 10,
        "name_ar":  "عيد الفطر",
        "name_en":  "Eid al-Fitr",
    },
    "adha": {
        "month":    "dhulhijja",
        "month_num": 12,
        "name_ar":  "عيد الأضحى",
        "name_en":  "Eid al-Adha",
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city",    required=True)
    ap.add_argument("--country", default="Saudi Arabia")
    ap.add_argument("--eid",     required=True, choices=["fitr", "adha"])
    ap.add_argument("--year",    type=int, default=None)
    args = ap.parse_args()

    cfg        = EID_CONFIG[args.eid]
    hijri_year = current_hijri_year()
    greg_year  = args.year or datetime.now().year

    # Calculated date
    calc_date = hijri_month_start_gregorian(cfg["month_num"], hijri_year)

    # Search for announcement
    queries = [
        f"هلال {HIJRI_MONTH_AR[cfg['month_num']]} {greg_year} {args.country}",
        f"{args.country} {cfg['name_en']} {greg_year} date announced",
        f"{cfg['name_en']} {greg_year} {args.country} moon sighting",
    ]
    all_news = []
    for q in queries:
        all_news.extend(search_news(q, max_results=4))

    keywords = [cfg["month"], cfg["name_en"], cfg["name_ar"], args.country, "announced", "أُعلن"]
    announced = extract_announced_date(all_news, keywords)

    date_used   = announced["date_str"] if announced else calc_date
    date_status = "announced" if announced else "calculated (Umm al-Qura — unconfirmed)"

    # Prayer time = Sunrise + 15 min on Eid day
    try:
        prayer_data = fetch_prayer_times(args.city, args.country, parse_date_arg(date_used))
        sunrise_str = prayer_data["timings"]["Sunrise"]
        h, m = map(int, sunrise_str[:5].split(":"))
        prayer_mins = h * 60 + m + 15
        prayer_time = f"{prayer_mins // 60:02d}:{prayer_mins % 60:02d}"
    except Exception as e:
        sunrise_str = "unknown"
        prayer_time = "unknown"

    result = {
        "city":              args.city,
        "country":           args.country,
        "eid":               cfg["name_en"],
        "eid_ar":            cfg["name_ar"],
        "calculated_date":   calc_date,
        "announced_date":    announced["date_str"] if announced else None,
        "date_used":         date_used,
        "date_status":       date_status,
        "estimated_prayer_time": prayer_time,
        "prayer_basis":      f"Sunrise ({sunrise_str}) + 15 minutes (estimated — verify with local mosque)",
        "supporting_news":   all_news[:4],
    }
    if announced:
        result["announcement_source"] = announced["source_title"]
        result["announcement_link"]   = announced["source_link"]

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
