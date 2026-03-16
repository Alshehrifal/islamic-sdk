#!/usr/bin/env python3
"""Tests for islamic-hilal skill."""
import subprocess, sys, json, unittest, os, re

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "hilal.py")


def run(args: list) -> dict:
    r = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    assert r.returncode == 0, f"Script failed:\n{r.stderr}"
    return json.loads(r.stdout)


DATE_RE = re.compile(r"^\d{2}-\d{2}-20\d{2}$")


INTEGRATION = os.environ.get("ISLAMIC_INTEGRATION_TESTS") == "1"

@unittest.skipUnless(INTEGRATION, "Set ISLAMIC_INTEGRATION_TESTS=1 to run live network tests")

class TestHilal(unittest.TestCase):

    def test_required_fields(self):
        d = run(["--country", "Saudi Arabia", "--month", "shawwal"])
        for f in ["country", "month", "hijri_year", "calculated_start_gregorian",
                  "date_used", "date_status", "moon_sighting_news"]:
            self.assertIn(f, d)

    def test_calculated_date_is_valid_format(self):
        d = run(["--country", "Saudi Arabia", "--month", "shawwal"])
        self.assertRegex(d["calculated_start_gregorian"], DATE_RE)

    def test_date_used_is_valid_format(self):
        d = run(["--country", "Saudi Arabia", "--month", "ramadan"])
        self.assertRegex(d["date_used"], DATE_RE)

    def test_date_status_values(self):
        d = run(["--country", "Saudi Arabia", "--month", "shawwal"])
        self.assertIn(
            d["date_status"],
            ["announced", "calculated (Umm al-Qura — unconfirmed)"]
        )

    def test_news_is_list(self):
        d = run(["--country", "Egypt", "--month", "ramadan"])
        self.assertIsInstance(d["moon_sighting_news"], list)

    def test_month_ar_present(self):
        d = run(["--country", "Morocco", "--month", "ramadan"])
        self.assertEqual(d["month_ar"], "رمضان")

    def test_dhulhijja(self):
        d = run(["--country", "Saudi Arabia", "--month", "dhulhijja"])
        self.assertEqual(d["month"], "dhulhijja")
        self.assertRegex(d["calculated_start_gregorian"], DATE_RE)

    def test_hijri_year_reasonable(self):
        d = run(["--country", "Saudi Arabia", "--month", "shawwal"])
        self.assertIn(d["hijri_year"], [1447, 1448])


if __name__ == "__main__":
    unittest.main(verbosity=2)
