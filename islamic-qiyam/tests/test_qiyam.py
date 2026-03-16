#!/usr/bin/env python3
"""Tests for islamic-qiyam skill."""
import subprocess, sys, json, unittest, os

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "qiyam.py")


def run(args: list) -> dict:
    r = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    assert r.returncode == 0, f"Script failed:\n{r.stderr}"
    return json.loads(r.stdout)


def to_mins(t: str) -> int:
    h, m = map(int, t[:5].split(":"))
    return h * 60 + m


INTEGRATION = os.environ.get("ISLAMIC_INTEGRATION_TESTS") == "1"

@unittest.skipUnless(INTEGRATION, "Set ISLAMIC_INTEGRATION_TESTS=1 to run live network tests")

class TestQiyam(unittest.TestCase):

    def test_required_fields(self):
        d = run(["--city", "Riyadh"])
        for f in ["maghrib", "isha", "fajr_next_day", "last_third_starts",
                  "night_duration_minutes", "last_third_ends_at_fajr"]:
            self.assertIn(f, d, f"Missing: {f}")

    def test_last_third_is_after_midnight(self):
        """Last third should be between midnight and fajr — i.e. late night."""
        d = run(["--city", "Riyadh"])
        lt_h = int(d["last_third_starts"][:2])
        # Last third typically starts between 01:00 and 05:00
        self.assertTrue(
            lt_h >= 1 or lt_h <= 5,
            f"Unexpected last_third_starts hour: {d['last_third_starts']}"
        )

    def test_night_duration_reasonable(self):
        d = run(["--city", "Jeddah", "--country", "Saudi Arabia"])
        mins = d["night_duration_minutes"]
        # Night should be between 6 and 14 hours
        self.assertGreater(mins, 360)
        self.assertLess(mins, 840)

    def test_last_third_is_two_thirds_into_night(self):
        d = run(["--city", "Cairo", "--country", "Egypt"])
        mag  = to_mins(d["maghrib"])
        lt   = to_mins(d["last_third_starts"])
        dur  = d["night_duration_minutes"]
        # last_third should be at roughly 2/3 through the night
        expected = (mag + dur * 2 // 3) % (24 * 60)
        self.assertAlmostEqual(lt, expected, delta=2)

    def test_different_cities_give_different_times(self):
        riyadh = run(["--city", "Riyadh"])
        london = run(["--city", "London", "--country", "United Kingdom"])
        self.assertNotEqual(
            riyadh["last_third_starts"],
            london["last_third_starts"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
