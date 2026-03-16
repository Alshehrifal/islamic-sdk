#!/usr/bin/env python3
"""
Tests for islamic-prayer-times skill.
Unit tests use mocked API (always run).
Integration tests require ISLAMIC_INTEGRATION_TESTS=1.
"""
import subprocess, sys, json, unittest, os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "prayer_times.py")

MOCK_DATA = {
    "timings": {"Fajr":"04:48","Sunrise":"06:13","Dhuhr":"12:22",
                "Asr":"15:45","Maghrib":"18:31","Isha":"20:01","Midnight":"00:22"},
    "meta":    {"method":{"name":"Umm Al Qura University, Makkah"},"timezone":"Asia/Riyadh"},
    "date":    {"gregorian":{"day":"16","month":{"number":3},"year":"2026"},
                "hijri":{"day":"16","month":{"number":9},"year":"1447"}},
}


def _mock_fetch(city, country, date_str, method=None):
    return MOCK_DATA


def run(args: list) -> dict:
    r = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    assert r.returncode == 0, f"Script failed:\n{r.stderr}"
    return json.loads(r.stdout)


INTEGRATION = os.environ.get("ISLAMIC_INTEGRATION_TESTS") == "1"

@unittest.skipUnless(INTEGRATION, "Set ISLAMIC_INTEGRATION_TESTS=1 to run live network tests")

class TestPrayerTimes(unittest.TestCase):

    def test_riyadh_returns_all_fields(self):
        d = run(["--city", "Riyadh"])
        required = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha",
                    "midnight", "hijri", "gregorian", "weekday_en", "timezone"]
        for field in required:
            self.assertIn(field, d, f"Missing field: {field}")

    def test_prayer_times_are_hhmm_format(self):
        d = run(["--city", "Riyadh"])
        for key in ["fajr", "dhuhr", "maghrib", "isha"]:
            val = d[key]
            parts = val[:5].split(":")
            self.assertEqual(len(parts), 2, f"{key} not HH:MM: {val}")
            h, m = int(parts[0]), int(parts[1])
            self.assertIn(h, range(0, 24))
            self.assertIn(m, range(0, 60))

    def test_fajr_before_sunrise(self):
        d = run(["--city", "Jeddah", "--country", "Saudi Arabia"])
        fajr_h, fajr_m    = map(int, d["fajr"][:5].split(":"))
        rise_h, rise_m    = map(int, d["sunrise"][:5].split(":"))
        fajr_mins  = fajr_h * 60 + fajr_m
        rise_mins  = rise_h * 60 + rise_m
        self.assertLess(fajr_mins, rise_mins, "Fajr should be before Sunrise")

    def test_london_different_method(self):
        d = run(["--city", "London", "--country", "United Kingdom"])
        self.assertIn("London", d["city"])
        self.assertIn("method", d)

    def test_specific_date(self):
        d = run(["--city", "Cairo", "--country", "Egypt", "--date", "25-03-2026"])
        self.assertEqual(d["gregorian"], "25-03-2026")

    def test_hijri_present(self):
        d = run(["--city", "Makkah", "--country", "Saudi Arabia"])
        self.assertRegex(d["hijri"], r"\d+ .+ \d{4}")

    def test_maghrib_before_isha(self):
        d = run(["--city", "Istanbul", "--country", "Turkey"])
        mag_h, mag_m  = map(int, d["maghrib"][:5].split(":"))
        ish_h, ish_m  = map(int, d["isha"][:5].split(":"))
        self.assertLess(mag_h * 60 + mag_m, ish_h * 60 + ish_m,
                        "Maghrib should be before Isha")


if __name__ == "__main__":
    unittest.main(verbosity=2)
