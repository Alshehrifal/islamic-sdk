#!/usr/bin/env python3
"""Tests for islamic-arafah skill."""
import subprocess, sys, json, unittest, os, re

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "arafah.py")
DATE_RE = re.compile(r"^\d{2}-\d{2}-20\d{2}$")


def run(args: list) -> dict:
    r = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    assert r.returncode == 0, f"Script failed:\n{r.stderr}"
    return json.loads(r.stdout)


INTEGRATION = os.environ.get("ISLAMIC_INTEGRATION_TESTS") == "1"

@unittest.skipUnless(INTEGRATION, "Set ISLAMIC_INTEGRATION_TESTS=1 to run live network tests")

class TestArafah(unittest.TestCase):

    def test_required_fields(self):
        d = run(["--city", "Riyadh"])
        for f in ["event", "hijri_date", "calculated_date", "date_used",
                  "date_status", "fasting_virtue", "note"]:
            self.assertIn(f, d)

    def test_calculated_date_format(self):
        d = run(["--city", "Riyadh"])
        self.assertRegex(d["calculated_date"], DATE_RE)

    def test_arafah_is_9th_dhulhijja(self):
        d = run(["--city", "Riyadh"])
        self.assertIn("9", d["hijri_date"])
        self.assertIn("ذو الحجة", d["hijri_date"])

    def test_fasting_virtue_mentions_two_years(self):
        d = run(["--city", "Jakarta", "--country", "Indonesia"])
        self.assertIn("سنتين", d["fasting_virtue"])

    def test_note_mentions_saudi(self):
        d = run(["--city", "London", "--country", "United Kingdom"])
        self.assertIn("السعودية", d["note"])

    def test_prayer_times_present(self):
        d = run(["--city", "Riyadh"])
        # prayer_times may be empty dict on error but should be a dict
        self.assertIsInstance(d["prayer_times"], dict)

    def test_arafah_one_day_before_adha(self):
        """Arafah = 9 Dhul Hijjah; Eid al-Adha = 10 Dhul Hijjah, so 1 day apart."""
        from datetime import datetime
        d = run(["--city", "Riyadh"])
        arafah_dt = datetime.strptime(d["calculated_date"], "%d-%m-%Y")

        # Eid al-Adha = 10 Dhul Hijjah = Arafah + 1 day
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
        from hijri_utils import current_hijri_year, hijri_to_gregorian
        adha_str = hijri_to_gregorian(1, 12, current_hijri_year())["gregorian_string"]
        # Arafah is 9th; Dhul Hijjah 1st + 8 days = Arafah
        from datetime import timedelta
        dh1 = datetime.strptime(adha_str, "%d-%m-%Y")
        expected_arafah = dh1 + timedelta(days=8)
        self.assertEqual(arafah_dt, expected_arafah)


if __name__ == "__main__":
    unittest.main(verbosity=2)
