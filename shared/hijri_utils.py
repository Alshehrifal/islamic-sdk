"""
Shared: Hijri ↔ Gregorian conversion helpers using hijridate.
"""
import subprocess, sys

def _ensure_hijridate():
    try:
        import hijridate  # noqa
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "hijridate", "-q",
                               "--break-system-packages"])

_ensure_hijridate()

from hijridate import Hijri, Gregorian  # type: ignore


def gregorian_to_hijri(day: int, month: int, year: int) -> dict:
    h = Gregorian(year, month, day).to_hijri()
    return {
        "hijri_day":   h.day,
        "hijri_month": h.month,
        "hijri_year":  h.year,
        "hijri_month_name": h.month_name(),
        "hijri_string": f"{h.day} {h.month_name()} {h.year}",
    }


def hijri_to_gregorian(day: int, month: int, year: int) -> dict:
    g = Hijri(year, month, day).to_gregorian()
    return {
        "gregorian_day":   g.day,
        "gregorian_month": g.month,
        "gregorian_year":  g.year,
        "gregorian_string": g.strftime("%d-%m-%Y"),
        "gregorian_iso":    g.isoformat(),
    }


HIJRI_MONTHS = {
    "muharram":    1,  "safar":       2,  "rabiulawal":  3,
    "rabiulakhir": 4,  "jumadalawal": 5,  "jumadalakhir":6,
    "rajab":       7,  "shaban":      8,  "ramadan":     9,
    "shawwal":    10,  "dhulqada":   11,  "dhulhijja":  12,
}
HIJRI_MONTH_AR = {
    1: "محرم",     2: "صفر",      3: "ربيع الأول",
    4: "ربيع الآخر", 5: "جمادى الأولى", 6: "جمادى الآخرة",
    7: "رجب",      8: "شعبان",    9: "رمضان",
    10: "شوال",   11: "ذو القعدة", 12: "ذو الحجة",
}


def month_key_to_number(month_key: str) -> int:
    k = month_key.lower().replace(" ", "").replace("-", "").replace("'", "")
    if k not in HIJRI_MONTHS:
        raise ValueError(f"Unknown Hijri month: {month_key!r}. "
                         f"Valid keys: {list(HIJRI_MONTHS)}")
    return HIJRI_MONTHS[k]


def hijri_month_start_gregorian(hijri_month: int, hijri_year: int) -> str:
    """Return Gregorian date (DD-MM-YYYY) for the 1st of a Hijri month."""
    return hijri_to_gregorian(1, hijri_month, hijri_year)["gregorian_string"]


def current_hijri_year() -> int:
    from datetime import date
    t = date.today()
    return gregorian_to_hijri(t.day, t.month, t.year)["hijri_year"]
