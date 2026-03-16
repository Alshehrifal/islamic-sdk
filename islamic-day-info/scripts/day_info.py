#!/usr/bin/env python3
"""
islamic-day-info/scripts/day_info.py
Usage:
  python day_info.py --city Riyadh
  python day_info.py --city Cairo --country Egypt --date 25-04-2026
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

DAY_VIRTUES = {
    "Friday": {
        "virtues": [
            "خير يوم طلعت فيه الشمس يوم الجمعة. (مسلم)",
            "فيه ساعة لا يوافقها عبد مسلم وهو قائم يصلي يسأل الله شيئاً إلا أعطاه إياه. (البخاري، مسلم)",
            "من قرأ سورة الكهف في يوم الجمعة أضاء له من النور ما بين الجمعتين. (الحاكم)",
            "أكثروا الصلاة عليّ يوم الجمعة. (أبو داود)",
        ],
        "recommended_acts": [
            "قراءة سورة الكهف.",
            "الإكثار من الصلاة على النبي ﷺ.",
            "الاغتسال والتطيب والتهيؤ لصلاة الجمعة.",
            "التبكير إلى صلاة الجمعة.",
            "الدعاء في الساعة الأخيرة بعد العصر.",
        ],
    },
    "Monday": {
        "virtues": [
            "تُعرض الأعمال يوم الاثنين والخميس. (الترمذي)",
            "ولدت يوم الاثنين، وبُعثت يوم الاثنين، وأُنزل عليّ فيه. (مسلم)",
        ],
        "recommended_acts": [
            "صيام يوم الاثنين — سنة النبي ﷺ.",
            "الإكثار من الأعمال الصالحة لأنها تُعرض على الله.",
        ],
    },
    "Thursday": {
        "virtues": [
            "تُعرض الأعمال يوم الاثنين والخميس. (الترمذي)",
        ],
        "recommended_acts": [
            "صيام يوم الخميس — سنة النبي ﷺ.",
            "الإكثار من الأعمال الصالحة لأنها تُعرض على الله.",
        ],
    },
    "default": {
        "virtues": ["لا فضيلة خاصة مذكورة في السنة لهذا اليوم، لكن كل يوم فرصة للطاعة."],
        "recommended_acts": ["الإكثار من الذكر والاستغفار.", "صيام أيام البيض (13، 14، 15) من كل شهر."],
    },
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city",    required=True)
    ap.add_argument("--country", default="")
    ap.add_argument("--date",    default=None)
    args = ap.parse_args()

    date_str = parse_date_arg(args.date)
    country  = args.country or "Saudi Arabia"

    data    = fetch_prayer_times(args.city, country, date_str)
    t       = data["timings"]
    gd      = data["date"]["gregorian"]
    day_dt  = datetime.strptime(date_str, "%d-%m-%Y")
    weekday = day_dt.strftime("%A")
    h       = gregorian_to_hijri(int(gd["day"]), int(gd["month"]["number"]), int(gd["year"]))

    day_data = DAY_VIRTUES.get(weekday, DAY_VIRTUES["default"])

    result = {
        "city":        args.city,
        "country":     country,
        "gregorian":   date_str,
        "hijri":       h["hijri_string"],
        "weekday_en":  weekday,
        "weekday_ar":  WEEKDAY_AR.get(weekday, weekday),
        "virtues":          day_data["virtues"],
        "recommended_acts": day_data["recommended_acts"],
        "prayer_times": {
            "fajr":    t["Fajr"],
            "sunrise": t["Sunrise"],
            "dhuhr":   t["Dhuhr"],
            "asr":     t["Asr"],
            "maghrib": t["Maghrib"],
            "isha":    t["Isha"],
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
