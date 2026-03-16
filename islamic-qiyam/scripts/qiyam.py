#!/usr/bin/env python3
"""
islamic-qiyam/scripts/qiyam.py
Calculates the last third of the night (Qiyam al-Layl window).

Usage:
  python qiyam.py --city Riyadh
  python qiyam.py --city Istanbul --country Turkey --date 01-04-2026
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from prayer_api import fetch_prayer_times, parse_date_arg
from datetime import datetime, timedelta


def next_day_str(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%d-%m-%Y") + timedelta(days=1)
    return dt.strftime("%d-%m-%Y")


def time_to_minutes(t: str) -> int:
    """Convert HH:MM to total minutes since midnight."""
    h, m = map(int, t[:5].split(":"))
    return h * 60 + m


def minutes_to_hhmm(mins: int) -> str:
    mins = mins % (24 * 60)
    return f"{mins // 60:02d}:{mins % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city",    required=True)
    ap.add_argument("--country", default="Saudi Arabia")
    ap.add_argument("--date",    default=None)
    args = ap.parse_args()

    date_str  = parse_date_arg(args.date)
    next_str  = next_day_str(date_str)
    country   = args.country

    today_data  = fetch_prayer_times(args.city, country, date_str)
    tomorrow_data = fetch_prayer_times(args.city, country, next_str)

    maghrib = today_data["timings"]["Maghrib"]
    isha    = today_data["timings"]["Isha"]
    fajr    = tomorrow_data["timings"]["Fajr"]

    mag_min  = time_to_minutes(maghrib)
    fajr_min = time_to_minutes(fajr) + 24 * 60  # next day

    night_duration  = fajr_min - mag_min          # total minutes
    third_duration  = night_duration // 3
    last_third_min  = mag_min + 2 * third_duration

    result = {
        "city":                   args.city,
        "country":                country,
        "date":                   date_str,
        "maghrib":                maghrib,
        "isha":                   isha,
        "fajr_next_day":          fajr,
        "night_duration_minutes": night_duration,
        "last_third_starts":      minutes_to_hhmm(last_third_min),
        "last_third_ends_at_fajr": fajr,
        "note": (
            "الثلث الأخير من الليل هو أفضل وقت لصلاة القيام والتهجد والدعاء. "
            "يبدأ من " + minutes_to_hhmm(last_third_min) +
            " وينتهي بأذان الفجر " + fajr + "."
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
