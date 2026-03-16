"""
Shared: Aladhan API wrapper for prayer times.
"""
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, date


METHODS = {
    "Saudi Arabia": 4,   # Umm al-Qura
    "Egypt":        5,
    "Pakistan":     1,
    "Turkey":       13,
    "France":       12,
    "default":      3,   # Muslim World League
}

COUNTRY_METHOD = {
    "saudi arabia": 4, "uae": 4, "qatar": 4, "kuwait": 4, "bahrain": 4,
    "oman": 4, "yemen": 4, "jordan": 11, "egypt": 5, "pakistan": 1,
    "turkey": 13, "france": 12, "malaysia": 3, "indonesia": 20,
}


def get_method(country: str) -> int:
    return COUNTRY_METHOD.get(country.lower(), METHODS["default"])


def fetch_prayer_times(city: str, country: str, date_str: str | None = None, method: int | None = None) -> dict:
    """
    Fetch prayer times from Aladhan API.
    date_str: DD-MM-YYYY or None for today
    Returns full timings dict + meta.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%d-%m-%Y")

    if method is None:
        method = get_method(country)

    params = urllib.parse.urlencode({
        "city":    city,
        "country": country,
        "method":  method,
        "date":    date_str,
    })
    url = f"https://api.aladhan.com/v1/timingsByCity/{date_str}?{params}"

    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read())

    if data.get("code") != 200:
        raise RuntimeError(f"Aladhan API error: {data}")

    return data["data"]


def parse_date_arg(date_str: str | None) -> str:
    """Return DD-MM-YYYY string; today if None."""
    if not date_str:
        return datetime.now().strftime("%d-%m-%Y")
    # accept YYYY-MM-DD too
    for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%d-%m-%Y")
        except ValueError:
            pass
    raise ValueError(f"Unrecognised date format: {date_str!r}  (use DD-MM-YYYY)")
