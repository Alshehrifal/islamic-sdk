#!/usr/bin/env python3
"""Tests for islamic-eid skill."""
import subprocess, sys, json, unittest, os, re

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "eid.py")
DATE_RE = re.compile(r"^\d{2}-\d{2}-20\d{2}$")


def run(args: list) -> dict:
    r = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    assert r.returncode == 0, f"Script failed:\n{r.stderr}"
    return json.loads(r.stdout)


INTEGRATION = os.environ.get("ISLAMIC_INTEGRATION_TESTS") == "1"

@unittest.skipUnless(INTEGRATION, "Set ISLAMIC_INTEGRATION_TESTS=1 to run live network tests")

class TestEid(unittest.TestCase):

    def test_required_fields_fitr(self):
        d = run(["--city", "Riyadh", "--eid", "fitr"])
        for f in ["city", "eid", "calculated_date", "date_used",
                  "date_status", "estimated_prayer_time"]:
            self.assertIn(f, d)

    def test_required_fields_adha(self):
        d = run(["--city", "Cairo", "--country", "Egypt", "--eid", "adha"])
        self.assertIn("estimated_prayer_time", d)

    def test_eid_al_fitr_name(self):
        d = run(["--city", "Riyadh", "--eid", "fitr"])
        self.assertIn("Fitr", d["eid"])

    def test_eid_al_adha_name(self):
        d = run(["--city", "Riyadh", "--eid", "adha"])
        self.assertIn("Adha", d["eid"])

    def test_calculated_date_format(self):
        d = run(["--city", "Istanbul", "--country", "Turkey", "--eid", "fitr"])
        self.assertRegex(d["calculated_date"], DATE_RE)

    def test_prayer_time_format(self):
        d = run(["--city", "Riyadh", "--eid", "fitr"])
        t = d["estimated_prayer_time"]
        if t != "unknown":
            h, m = map(int, t.split(":"))
            # Eid prayer is always in the morning
            self.assertGreater(h, 5)
            self.assertLess(h, 12)

    def test_date_status_valid(self):
        d = run(["--city", "Riyadh", "--eid", "adha"])
        self.assertIn(
            d["date_status"],
            ["announced", "calculated (Umm al-Qura — unconfirmed)"]
        )

    def test_adha_date_after_fitr(self):
        """Eid al-Adha is always after Eid al-Fitr."""
        from datetime import datetime
        fitr = run(["--city", "Riyadh", "--eid", "fitr"])
        adha = run(["--city", "Riyadh", "--eid", "adha"])
        fitr_dt = datetime.strptime(fitr["calculated_date"], "%d-%m-%Y")
        adha_dt = datetime.strptime(adha["calculated_date"], "%d-%m-%Y")
        self.assertGreater(adha_dt, fitr_dt)


if __name__ == "__main__":
    unittest.main(verbosity=2)
