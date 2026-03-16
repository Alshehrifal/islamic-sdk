#!/usr/bin/env python3
"""
islamic-hijri/scripts/hijri.py
Gregorian ↔ Hijri date conversion.

Usage (Gregorian → Hijri):
  python hijri.py --date 20-03-2026

Usage (Hijri → Gregorian):
  python hijri.py --day 1 --month 10 --year 1447
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from hijri_utils import gregorian_to_hijri, hijri_to_gregorian
from datetime import datetime


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date",  help="Gregorian date DD-MM-YYYY (for G→H conversion)")
    ap.add_argument("--day",   type=int, help="Hijri day (for H→G conversion)")
    ap.add_argument("--month", type=int, help="Hijri month number (for H→G conversion)")
    ap.add_argument("--year",  type=int, help="Hijri year (for H→G conversion)")
    args = ap.parse_args()

    if args.date:
        # Gregorian → Hijri
        for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(args.date, fmt)
                break
            except ValueError:
                pass
        else:
            print(json.dumps({"error": f"Cannot parse date: {args.date!r}"}, ensure_ascii=False))
            sys.exit(1)

        h = gregorian_to_hijri(dt.day, dt.month, dt.year)
        result = {
            "mode":            "gregorian_to_hijri",
            "gregorian_input": args.date,
            **h,
        }

    elif args.day and args.month and args.year:
        # Hijri → Gregorian
        g = hijri_to_gregorian(args.day, args.month, args.year)
        result = {
            "mode":         "hijri_to_gregorian",
            "hijri_input":  f"{args.day}/{args.month}/{args.year}",
            **g,
        }

    else:
        result = {"error": "Provide --date for G→H, or --day/--month/--year for H→G"}

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
