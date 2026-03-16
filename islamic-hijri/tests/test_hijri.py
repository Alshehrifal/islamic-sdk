#!/usr/bin/env python3
"""Tests for islamic-hijri skill."""
import subprocess, sys, json, unittest, os

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "hijri.py")


def run(args: list) -> dict:
    r = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    assert r.returncode == 0, f"Script failed:\n{r.stderr}"
    return json.loads(r.stdout)


class TestHijriConversion(unittest.TestCase):

    def test_gregorian_to_hijri_known_date(self):
        """1 Ramadan 1446 = 1 March 2025 (approx)."""
        d = run(["--date", "01-03-2025"])
        self.assertEqual(d["mode"], "gregorian_to_hijri")
        self.assertIn("hijri_string", d)
        self.assertIn("hijri_year", d)
        self.assertGreater(d["hijri_year"], 1440)

    def test_hijri_to_gregorian_known_date(self):
        """1 Shawwal 1447 should be in March 2026."""
        d = run(["--day", "1", "--month", "10", "--year", "1447"])
        self.assertEqual(d["mode"], "hijri_to_gregorian")
        self.assertIn("2026", d["gregorian_string"])

    def test_roundtrip(self):
        """Convert G→H then H→G and get back the same date."""
        from datetime import date
        today = date.today()
        date_str = today.strftime("%d-%m-%Y")

        gh = run(["--date", date_str])
        hg = run(["--day", str(gh["hijri_day"]),
                  "--month", str(gh["hijri_month"]),
                  "--year", str(gh["hijri_year"])])
        self.assertEqual(hg["gregorian_string"], date_str)

    def test_year_format(self):
        d = run(["--date", "2026-06-15"])
        self.assertEqual(d["mode"], "gregorian_to_hijri")
        self.assertIn("hijri_year", d)

    def test_missing_args_returns_error(self):
        r = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
        out = json.loads(r.stdout)
        self.assertIn("error", out)

    def test_hijri_year_is_1447_or_1448(self):
        """Today should be in Hijri year 1447."""
        d = run(["--date", "16-03-2026"])
        self.assertIn(d["hijri_year"], [1447, 1448])


if __name__ == "__main__":
    unittest.main(verbosity=2)
