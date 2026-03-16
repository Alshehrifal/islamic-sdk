#!/usr/bin/env python3
"""
islamic-prayer-times/scripts/prayer_times.py
Usage:
  python prayer_times.py --city Riyadh
  python prayer_times.py --city London --country "United Kingdom" --date 25-03-2026
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from prayer_api import fetch_prayer_times, parse_date_arg
from hijri_utils import gregorian_to_hijri
from datetime import datetime

WEEKDAY_AR = {
    "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
    "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city",    required=True)
    ap.add_argument("--country", default="")
    ap.add_argument("--date",    default=None, help="DD-MM-YYYY")
    args = ap.parse_args()

    date_str = parse_date_arg(args.date)
    country  = args.country or "Saudi Arabia"

    data = fetch_prayer_times(args.city, country, date_str)
    t    = data["timings"]
    meta = data["meta"]
    d    = data["date"]

    day_dt  = datetime.strptime(date_str, "%d-%m-%Y")
    weekday = day_dt.strftime("%A")

    # hijri
    gd = d["gregorian"]
    h  = gregorian_to_hijri(int(gd["day"]), int(gd["month"]["number"]), int(gd["year"]))

    result = {
        "city":       args.city,
        "country":    country,
        "gregorian":  date_str,
        "hijri":      h["hijri_string"],
        "weekday_en": weekday,
        "weekday_ar": WEEKDAY_AR.get(weekday, weekday),
        "fajr":       t["Fajr"],
        "sunrise":    t["Sunrise"],
        "dhuhr":      t["Dhuhr"],
        "asr":        t["Asr"],
        "maghrib":    t["Maghrib"],
        "isha":       t["Isha"],
        "midnight":   t["Midnight"],
        "method":     meta["method"]["name"],
        "timezone":   meta["timezone"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
