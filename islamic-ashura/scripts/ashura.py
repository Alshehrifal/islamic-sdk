#!/usr/bin/env python3
"""
islamic-ashura/scripts/ashura.py
Yawm Ashura (10th Muharram) + Tasu'a (9th Muharram).

Usage:
  python ashura.py --city Riyadh
  python ashura.py --city Damascus --country Syria --year 2026
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from hijri_utils import current_hijri_year, hijri_to_gregorian, HIJRI_MONTH_AR
from prayer_api import fetch_prayer_times, parse_date_arg
from news_utils import search_news, extract_announced_date
from datetime import datetime, timedelta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city",    required=True)
    ap.add_argument("--country", default="Saudi Arabia")
    ap.add_argument("--year",    type=int, default=None)
    args = ap.parse_args()

    hijri_year = current_hijri_year()
    greg_year  = args.year or datetime.now().year

    calc_ashura = hijri_to_gregorian(10, 1, hijri_year)["gregorian_string"]
    calc_tasua  = hijri_to_gregorian(9, 1, hijri_year)["gregorian_string"]

    # Search for country's Muharram announcement
    queries = [
        f"هلال محرم {greg_year} {args.country}",
        f"{args.country} Muharram {greg_year} moon sighting announced",
        f"عاشوراء {greg_year} {args.country}",
    ]
    all_news = []
    for q in queries:
        all_news.extend(search_news(q, max_results=4))

    keywords = ["muharram", "محرم", "ashura", "عاشوراء", args.country]
    announced = extract_announced_date(all_news, keywords)

    if announced:
        muh1 = datetime.strptime(announced["date_str"], "%d-%m-%Y")
        tasua_dt  = muh1 + timedelta(days=8)
        ashura_dt = muh1 + timedelta(days=9)
        date_used   = ashura_dt.strftime("%d-%m-%Y")
        tasua_used  = tasua_dt.strftime("%d-%m-%Y")
        date_status = "announced"
    else:
        date_used   = calc_ashura
        tasua_used  = calc_tasua
        date_status = "calculated (Umm al-Qura — unconfirmed)"
        announced   = None

    weekday = datetime.strptime(date_used, "%d-%m-%Y").strftime("%A")
    WEEKDAY_AR = {"Monday":"الاثنين","Tuesday":"الثلاثاء","Wednesday":"الأربعاء",
                  "Thursday":"الخميس","Friday":"الجمعة","Saturday":"السبت","Sunday":"الأحد"}

    try:
        prayer_data = fetch_prayer_times(args.city, args.country, parse_date_arg(date_used))
        t = prayer_data["timings"]
        prayers = {"fajr": t["Fajr"], "dhuhr": t["Dhuhr"], "asr": t["Asr"],
                   "maghrib": t["Maghrib"], "isha": t["Isha"]}
    except Exception:
        prayers = {}

    result = {
        "city":              args.city,
        "country":           args.country,
        "event":             "Yawm Ashura — 10 Muharram",
        "event_ar":          "يوم عاشوراء — العاشر من المحرم",
        "hijri_date":        f"10 {HIJRI_MONTH_AR[1]} {hijri_year}",
        "calculated_ashura": calc_ashura,
        "calculated_tasua":  calc_tasua,
        "announced_date":    announced["date_str"] if announced else None,
        "announced_tasua":   tasua_used if announced else None,
        "date_used":         date_used,
        "date_status":       date_status,
        "weekday_en":        weekday,
        "weekday_ar":        WEEKDAY_AR.get(weekday, weekday),
        "fasting_virtue": (
            "صيام يوم عاشوراء يُكفِّر السنة الماضية. (مسلم 1162)"
        ),
        "tasua_note": (
            "قال النبي ﷺ: 'لئن بقيت إلى قابل لأصومن التاسع'. (مسلم 1134) — "
            "يُستحب صيام التاسع مع العاشر مخالفةً لليهود."
        ),
        "tasu_a_date": tasua_used,
        "note": "تحقق من إعلان هلال المحرم في بلدك.",
        "prayer_times": prayers,
    }
    if announced:
        result["announcement_source"] = announced.get("source_title")
        result["announcement_link"]   = announced.get("source_link")

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
