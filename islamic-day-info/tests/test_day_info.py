#!/usr/bin/env python3
"""Tests for islamic-day-info skill."""
import subprocess, sys, json, unittest, os

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "day_info.py")


def run(args: list) -> dict:
    r = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    assert r.returncode == 0, f"Script failed:\n{r.stderr}"
    return json.loads(r.stdout)


INTEGRATION = os.environ.get("ISLAMIC_INTEGRATION_TESTS") == "1"

@unittest.skipUnless(INTEGRATION, "Set ISLAMIC_INTEGRATION_TESTS=1 to run live network tests")

class TestDayInfo(unittest.TestCase):

    def test_required_fields(self):
        d = run(["--city", "Riyadh"])
        for f in ["virtues", "recommended_acts", "weekday_en", "weekday_ar", "prayer_times"]:
            self.assertIn(f, d)

    def test_virtues_is_list(self):
        d = run(["--city", "Makkah"])
        self.assertIsInstance(d["virtues"], list)
        self.assertGreater(len(d["virtues"]), 0)

    def test_friday_has_kahf_reference(self):
        """Friday should mention Surah Al-Kahf."""
        # 20-03-2026 is a Friday
        d = run(["--city", "Riyadh", "--date", "20-03-2026"])
        all_text = " ".join(d["virtues"] + d["recommended_acts"]).lower()
        self.assertIn("كهف", all_text, "Friday virtues should mention Surah Al-Kahf")

    def test_friday_weekday(self):
        d = run(["--city", "Riyadh", "--date", "20-03-2026"])
        self.assertEqual(d["weekday_en"], "Friday")
        self.assertEqual(d["weekday_ar"], "الجمعة")

    def test_monday_has_fasting(self):
        # Find a Monday — 16-03-2026 is a Monday
        d = run(["--city", "Cairo", "--country", "Egypt", "--date", "16-03-2026"])
        all_text = " ".join(d["recommended_acts"]).lower()
        self.assertIn("صيام", all_text)

    def test_prayer_times_present(self):
        d = run(["--city", "Istanbul", "--country", "Turkey"])
        pt = d["prayer_times"]
        for key in ["fajr", "dhuhr", "maghrib", "isha"]:
            self.assertIn(key, pt)


if __name__ == "__main__":
    unittest.main(verbosity=2)
