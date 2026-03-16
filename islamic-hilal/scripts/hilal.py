#!/usr/bin/env python3
"""
islamic-hilal/scripts/hilal.py
Moon sighting check — announced vs. calculated Hijri month start.

Usage:
  python hilal.py --country "Saudi Arabia" --month shawwal
  python hilal.py --country Syria --month ramadan
  python hilal.py --country Morocco --month dhulhijja --year 2026
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from hijri_utils import (
    gregorian_to_hijri, hijri_to_gregorian, month_key_to_number,
    current_hijri_year, HIJRI_MONTH_AR, hijri_month_start_gregorian,
)
from news_utils import search_news, extract_announced_date
from datetime import datetime


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--country", required=True)
    ap.add_argument("--month",   required=True, help="e.g. shawwal, ramadan, dhulhijja")
    ap.add_argument("--year",    type=int, default=None, help="Gregorian year (defaults to current)")
    args = ap.parse_args()

    month_num  = month_key_to_number(args.month)
    hijri_year = current_hijri_year()

    # Calculated start (Umm al-Qura)
    calc_start = hijri_month_start_gregorian(month_num, hijri_year)

    # Eve = 29th of previous month
    prev_month = 12 if month_num == 1 else month_num - 1
    prev_year  = hijri_year - 1 if month_num == 1 else hijri_year
    eve_29     = hijri_to_gregorian(29, prev_month, prev_year)["gregorian_string"]

    month_ar = HIJRI_MONTH_AR[month_num]

    # Build news search queries
    greg_year = args.year or datetime.now().year
    queries = [
        f"هلال {month_ar} {greg_year} {args.country}",
        f"hilal {args.month} {greg_year} {args.country} sighting",
        f"{args.country} moon sighting {args.month} {greg_year} announced",
    ]

    all_news = []
    for q in queries:
        all_news.extend(search_news(q, max_results=4))

    keywords = [args.month, month_ar, args.country, "announced", "confirmed", "أُعلن", "ثبت", "رؤية"]
    announced = extract_announced_date(all_news, keywords)

    if announced:
        date_used   = announced["date_str"]
        date_status = "announced"
        source      = announced["source_title"]
        link        = announced["source_link"]
    else:
        date_used   = calc_start
        date_status = "calculated (Umm al-Qura — unconfirmed)"
        source      = None
        link        = None

    result = {
        "country":                   args.country,
        "month":                     args.month,
        "month_ar":                  month_ar,
        "hijri_year":                hijri_year,
        "calculated_start_gregorian": calc_start,
        "hilal_eve_gregorian":        eve_29,
        "announced_start_gregorian":  announced["date_str"] if announced else None,
        "date_used":                  date_used,
        "date_status":                date_status,
        "moon_sighting_news":         all_news[:5],
    }
    if source:
        result["announcement_source"] = source
        result["announcement_link"]   = link

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
