#!/usr/bin/env python3
"""
islamic-next-events/scripts/next_events.py
Returns the next Yawm Arafah, Eid al-Fitr, and Eid al-Adha — sorted by date.

Usage:
  python next_events.py --city Riyadh
  python next_events.py --city "Kuala Lumpur" --country Malaysia
"""
import sys, os, json, argparse, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from hijri_utils import current_hijri_year, hijri_to_gregorian
from datetime import datetime, date

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "..")


def run_script(script_path: str, extra_args: list) -> dict:
    result = subprocess.run(
        [sys.executable, script_path] + extra_args,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city",    required=True)
    ap.add_argument("--country", default="Saudi Arabia")
    args = ap.parse_args()

    today = date.today()

    # Collect events
    events = []

    # Eid al-Fitr
    eid_fitr = run_script(
        os.path.join(SCRIPTS, "islamic-eid", "scripts", "eid.py"),
        ["--city", args.city, "--country", args.country, "--eid", "fitr"]
    )
    fitr_dt = datetime.strptime(eid_fitr["date_used"], "%d-%m-%Y").date()
    events.append({
        "event":       "Eid al-Fitr",
        "event_ar":    "عيد الفطر",
        "date":        eid_fitr["date_used"],
        "date_status": eid_fitr["date_status"],
        "days_until":  (fitr_dt - today).days,
        "prayer_time": eid_fitr.get("estimated_prayer_time"),
    })

    # Eid al-Adha
    eid_adha = run_script(
        os.path.join(SCRIPTS, "islamic-eid", "scripts", "eid.py"),
        ["--city", args.city, "--country", args.country, "--eid", "adha"]
    )
    adha_dt = datetime.strptime(eid_adha["date_used"], "%d-%m-%Y").date()
    events.append({
        "event":       "Eid al-Adha",
        "event_ar":    "عيد الأضحى",
        "date":        eid_adha["date_used"],
        "date_status": eid_adha["date_status"],
        "days_until":  (adha_dt - today).days,
        "prayer_time": eid_adha.get("estimated_prayer_time"),
    })

    # Arafah
    arafah = run_script(
        os.path.join(SCRIPTS, "islamic-arafah", "scripts", "arafah.py"),
        ["--city", args.city, "--country", args.country]
    )
    arafah_dt = datetime.strptime(arafah["date_used"], "%d-%m-%Y").date()
    events.append({
        "event":       "Yawm Arafah",
        "event_ar":    "يوم عرفة",
        "date":        arafah["date_used"],
        "date_status": arafah["date_status"],
        "days_until":  (arafah_dt - today).days,
        "fasting_virtue": "صوم يوم عرفة يُكفِّر سنتين.",
    })

    # Filter future events and sort
    future = [e for e in events if e["days_until"] >= 0]
    future.sort(key=lambda x: x["days_until"])

    result = {
        "city":    args.city,
        "country": args.country,
        "today":   today.strftime("%d-%m-%Y"),
        "events":  future,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
