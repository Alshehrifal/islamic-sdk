#!/usr/bin/env python3
"""
islamic-arafah/scripts/arafah.py
Yawm Arafah (9th Dhul Hijjah) — always follows Saudi Arabia's announcement.

Usage:
  python arafah.py --city Riyadh
  python arafah.py --city Jakarta --country Indonesia
  python arafah.py --city London --country "United Kingdom" --year 2026
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from hijri_utils import current_hijri_year, hijri_to_gregorian, HIJRI_MONTH_AR
from prayer_api import fetch_prayer_times, parse_date_arg
from news_utils import search_news, extract_announced_date
from datetime import datetime


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city",    required=True)
    ap.add_argument("--country", default="Saudi Arabia")
    ap.add_argument("--year",    type=int, default=None)
    args = ap.parse_args()

    hijri_year = current_hijri_year()
    greg_year  = args.year or datetime.now().year

    # 9th Dhul Hijjah = calculated Arafah
    calc_arafah = hijri_to_gregorian(9, 12, hijri_year)["gregorian_string"]

    # Always search SA for official Dhul Hijjah announcement
    queries = [
        f"هلال ذي الحجة {greg_year} السعودية",
        f"Saudi Arabia Dhul Hijjah {greg_year} moon sighting",
        f"Yawm Arafah {greg_year} Saudi Arabia date announced",
    ]
    all_news = []
    for q in queries:
        all_news.extend(search_news(q, max_results=4))

    keywords = ["dhulhijja", "ذو الحجة", "arafah", "عرفة", "Saudi Arabia", "السعودية"]
    announced = extract_announced_date(all_news, keywords)

    # If SA announced Dhul Hijjah 1 = X, then Arafah = X + 8 days
    if announced:
        from datetime import timedelta
        dh1 = datetime.strptime(announced["date_str"], "%d-%m-%Y")
        arafah_dt = dh1 + timedelta(days=8)
        date_used   = arafah_dt.strftime("%d-%m-%Y")
        date_status = "announced (based on Saudi Dhul Hijjah announcement)"
    else:
        date_used   = calc_arafah
        date_status = "calculated (Umm al-Qura — unconfirmed)"
        announced   = None

    weekday = datetime.strptime(date_used, "%d-%m-%Y").strftime("%A")
    WEEKDAY_AR = {"Monday":"الاثنين","Tuesday":"الثلاثاء","Wednesday":"الأربعاء",
                  "Thursday":"الخميس","Friday":"الجمعة","Saturday":"السبت","Sunday":"الأحد"}

    # Prayer times for requested city on Arafah day
    try:
        prayer_data = fetch_prayer_times(args.city, args.country, parse_date_arg(date_used))
        t = prayer_data["timings"]
        prayers = {"fajr": t["Fajr"], "dhuhr": t["Dhuhr"], "asr": t["Asr"],
                   "maghrib": t["Maghrib"], "isha": t["Isha"]}
    except Exception:
        prayers = {}

    result = {
        "city":             args.city,
        "country":          args.country,
        "event":            "Yawm Arafah — 9 Dhul Hijjah",
        "event_ar":         "يوم عرفة — التاسع من ذي الحجة",
        "hijri_date":       f"9 {HIJRI_MONTH_AR[12]} {hijri_year}",
        "calculated_date":  calc_arafah,
        "announced_date":   announced["date_str"] if announced else None,
        "date_used":        date_used,
        "date_status":      date_status,
        "weekday_en":       weekday,
        "weekday_ar":       WEEKDAY_AR.get(weekday, weekday),
        "fasting_virtue": (
            "صيام يوم عرفة يُكفِّر سنتين: الماضية والقادمة. (مسلم 1162) — للحجاج غير المؤدين فريضة الحج."
        ),
        "note": "تاريخ عرفة يتبع إعلان المملكة العربية السعودية دائماً، لأن الحج في مكة المكرمة.",
        "prayer_times": prayers,
    }
    if announced:
        result["announcement_source"] = announced.get("source_title")
        result["announcement_link"]   = announced.get("source_link")

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
