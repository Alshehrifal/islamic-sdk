#!/usr/bin/env python3
"""Tests for islamic-ashura skill."""
import subprocess, sys, json, unittest, os, re
from datetime import datetime

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "ashura.py")
DATE_RE = re.compile(r"^\d{2}-\d{2}-20\d{2}$")


def run(args: list) -> dict:
    r = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    assert r.returncode == 0, f"Script failed:\n{r.stderr}"
    return json.loads(r.stdout)


INTEGRATION = os.environ.get("ISLAMIC_INTEGRATION_TESTS") == "1"

@unittest.skipUnless(INTEGRATION, "Set ISLAMIC_INTEGRATION_TESTS=1 to run live network tests")

class TestAshura(unittest.TestCase):

    def test_required_fields(self):
        d = run(["--city", "Riyadh"])
        for f in ["event", "calculated_ashura", "calculated_tasua",
                  "date_used", "tasu_a_date", "fasting_virtue", "tasua_note"]:
            self.assertIn(f, d)

    def test_ashura_date_format(self):
        d = run(["--city", "Riyadh"])
        self.assertRegex(d["calculated_ashura"], DATE_RE)

    def test_tasua_is_one_day_before_ashura(self):
        d = run(["--city", "Riyadh"])
        ashura = datetime.strptime(d["calculated_ashura"], "%d-%m-%Y")
        tasua  = datetime.strptime(d["calculated_tasua"],  "%d-%m-%Y")
        from datetime import timedelta
        self.assertEqual(ashura - tasua, timedelta(days=1))

    def test_fasting_virtue_mentions_one_year(self):
        d = run(["--city", "Cairo", "--country", "Egypt"])
        self.assertIn("السنة الماضية", d["fasting_virtue"])

    def test_tasua_note_mentions_prophet(self):
        d = run(["--city", "Istanbul", "--country", "Turkey"])
        self.assertIn("النبي", d["tasua_note"])

    def test_date_status_valid(self):
        d = run(["--city", "Riyadh"])
        self.assertIn(
            d["date_status"],
            ["announced", "calculated (Umm al-Qura — unconfirmed)"]
        )

    def test_hijri_date_mentions_muharram(self):
        d = run(["--city", "Riyadh"])
        self.assertIn("محرم", d["hijri_date"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
